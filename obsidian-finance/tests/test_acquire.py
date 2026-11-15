import hashlib
import importlib.util
import json
from pathlib import Path
import sys

import pytest

SCRIPTS = Path(__file__).parents[1] / 'skills/sec-data/scripts'
sys.path.insert(0, str(SCRIPTS))


def module():
    spec = importlib.util.spec_from_file_location('finance_acquire', SCRIPTS / 'acquire.py')
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def payloads():
    return [
        {'0': {'ticker': 'AAPL', 'cik_str': 320193, 'title': 'Apple Inc.'}},
        {'cik': 320193, 'tickers': ['AAPL'], 'filings': {'files': [], 'recent': {
            'accessionNumber': ['0000320193-24-000001'], 'form': ['10-K'],
            'filingDate': ['2024-11-01'], 'reportDate': ['2024-09-28'],
            'acceptanceDateTime': ['2024-11-01T10:00:00Z']}}},
        {'cik': 320193, 'entityName': 'Apple Inc.', 'facts': {'us-gaap': {'Revenues': {
            'units': {'USD': [{'start': '2023-10-01', 'end': '2024-09-28',
                'filed': '2024-11-01', 'accn': '0000320193-24-000001', 'val': 100}]}}}}},
    ]


def execute(tmp_path, monkeypatch, data=None, extra=()):
    monkeypatch.setenv('SEC_USER_AGENT', 'Test Operator test@example.org')
    data = payloads() if data is None else data
    calls = []
    def fetch(url, headers):
        calls.append(url)
        item = data.pop(0)
        if isinstance(item, bytes):
            return item
        return json.dumps(item).encode()
    args = ['--ticker', 'AAPL', '--period-start', '2024-01-01', '--period-end', '2024-12-31',
            '--as-of', '2024-12-31', '--output-dir', str(tmp_path), *extra]
    summary = module().run(args, fetch=fetch)
    path = Path(summary['run_path']) if summary.get('run_path') else None
    return summary, path, calls


def read(path, filename):
    return json.loads((path / filename).read_text())


def test_traceable_package(tmp_path, monkeypatch, capsys):
    summary, path, calls = execute(tmp_path, monkeypatch)
    assert summary['status'] == 'complete' and summary['exit_code'] == 0
    rows = read(path, 'eligible-facts.json')
    assert rows[0]['val'] == 100 and rows[0]['unit'] == 'USD'
    assert rows[0]['start'] == '2023-10-01' and rows[0]['filed'] == '2024-11-01'
    assert rows[0]['accession_in_inventory'] and rows[0]['retrieved_at']
    assert rows[0]['source_url'].startswith('https://www.sec.gov/Archives/')
    manifest = read(path, 'manifest.json')
    assert manifest['company']['cik'] == 320193
    for source in manifest['sources']:
        assert hashlib.sha256((path / source['path']).read_bytes()).hexdigest() == source['sha256']
    assert 'test@example.org' not in json.dumps(manifest)
    assert read(path, 'completion.json')['status'] == 'complete'
    captured = capsys.readouterr()
    assert captured.out == '' and 'SEC' in captured.err


@pytest.mark.parametrize('field', ['filed', 'end'])
def test_missing_source_date(tmp_path, monkeypatch, field):
    data = payloads()
    del data[2]['facts']['us-gaap']['Revenues']['units']['USD'][0][field]
    summary, path, _ = execute(tmp_path, monkeypatch, data)
    assert summary['status'] == 'empty'
    assert read(path, 'eligible-facts.json') == []
    assert read(path, 'coverage.json')['excluded'][f'invalid_{field}'] == 1


@pytest.mark.parametrize('mode,status,code', [
    ('normal', 'complete', 0), ('archive', 'partial', 2), ('empty', 'empty', 3),
    ('all', 'failed', 1), ('empty_archive', 'partial', 2), ('no_filings', 'complete', 0),
    ('bad_structure_all', 'failed', 1),
])
def test_status_precedence(tmp_path, monkeypatch, mode, status, code):
    data = payloads()
    if mode in ('archive', 'empty_archive'):
        data[1]['filings']['files'] = [{'name': 'CIK0000320193-submissions-001.json'}]
        data.insert(2, b'not-json')
    if mode in ('empty', 'empty_archive'):
        data[-1]['facts'] = {}
    if mode == 'all':
        data[1:] = [b'bad', b'bad']
    if mode == 'bad_structure_all':
        data[1] = b'bad'
        data[2]['facts'] = {'us-gaap': []}
    if mode == 'no_filings':
        data[1]['filings']['recent'] = {}
    summary, path, _ = execute(tmp_path, monkeypatch, data)
    assert (summary['status'], summary['exit_code']) == (status, code)
    assert (path / 'completion.json').exists() == (status != 'failed')
    assert (path / 'eligible-facts.json').exists() == (status != 'failed')


@pytest.mark.parametrize('section', [1, 2])
def test_unavailable_sections(tmp_path, monkeypatch, section):
    data = payloads()
    data[section] = b'bad'
    summary, path, _ = execute(tmp_path, monkeypatch, data)
    assert summary['status'] == 'partial'
    assert read(path, 'manifest.json')['errors'][0]['code'] == 'INVALID_SOURCE_DATA'


def test_cutoff_filter(tmp_path, monkeypatch):
    data = payloads()
    facts = data[2]['facts']['us-gaap']['Revenues']['units']['USD']
    facts.extend([
        dict(facts[0], filed='2025-01-01'),
        dict(facts[0], end='2023-12-31'),
        dict(facts[0], accn='0000320193-24-000002', val=90),
        dict(facts[0], filed='2024-12-31', accn='0000320193-24-000003', val=110),
    ])
    summary, path, _ = execute(tmp_path, monkeypatch, data)
    assert [r['val'] for r in read(path, 'eligible-facts.json')] == [100, 90, 110]
    assert not read(path, 'eligible-facts.json')[1]['accession_in_inventory']
    coverage = read(path, 'coverage.json')
    assert coverage['excluded']['after_cutoff'] == 1
    assert coverage['excluded']['outside_period'] == 1
    assert len(read(path, 'raw/companyfacts.json')['facts']['us-gaap']['Revenues']['units']['USD']) == 5


@pytest.mark.parametrize('mode', ['date', 'acceptance', 'duplicate'])
def test_amendment_conflict(tmp_path, monkeypatch, mode):
    data = payloads()
    block = data[1]['filings']['recent']
    if mode == 'date':
        data[2]['facts']['us-gaap']['Revenues']['units']['USD'][0]['filed'] = '2024-11-02'
    elif mode == 'acceptance':
        block['acceptanceDateTime'] = ['2025-01-01T10:00:00Z']
    else:
        for key, values in block.items():
            values.append('2024-11-02' if key == 'filingDate' else values[0])
    summary, path, _ = execute(tmp_path, monkeypatch, data)
    assert summary['status'] == 'empty'
    assert read(path, 'coverage.json')['excluded']['conflicting_publication'] == 1
    if mode != 'date':
        assert read(path, 'filings.json') == []


def test_repeat_preserves(tmp_path, monkeypatch):
    marker = tmp_path / 'research.md'
    marker.write_text('keep')
    first, path, _ = execute(tmp_path, monkeypatch)
    original = (path / 'manifest.json').read_bytes()
    second, other, _ = execute(tmp_path, monkeypatch)
    assert path != other and original == (path / 'manifest.json').read_bytes()
    assert marker.read_text() == 'keep'


@pytest.mark.parametrize('mode', ['identity', 'issuer', 'dates', 'destination', 'write'])
def test_invalid_identity_output(tmp_path, monkeypatch, mode):
    mod = module()
    monkeypatch.setenv('SEC_USER_AGENT', '' if mode == 'identity' else 'Test test@example.org')
    calls = []
    data = payloads()
    if mode == 'issuer':
        data[2]['cik'] = 1
    if mode == 'write':
        def fail_write(*args):
            raise OSError('private identity must not appear')
        monkeypatch.setattr(mod, '_write_json', fail_write)
    def fetch(url, headers):
        calls.append(url)
        return json.dumps(data.pop(0)).encode()
    dest = tmp_path / 'missing-parent' / 'output' if mode == 'destination' else tmp_path
    result = mod.run(['--ticker', 'AAPL', '--period-start', '2025-01-01' if mode == 'dates' else '2024-01-01',
        '--period-end', '2024-12-31', '--as-of', '2024-12-31', '--output-dir', str(dest)], fetch)
    assert result['exit_code'] == (1 if mode in ('issuer', 'write') else 64)
    if mode in ('issuer', 'write'):
        assert not (Path(result['run_path']) / 'completion.json').exists()
        assert 'private identity' not in json.dumps(result)
    else:
        assert calls == []
