import importlib.util
import hashlib
import json
from pathlib import Path
import subprocess
import sys

import pytest

SCRIPT = Path(__file__).parents[1] / 'skills/sec-data/scripts/sec_client.py'


def client():
    spec = importlib.util.spec_from_file_location('sec_client', SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def responses():
    return [
        {'0': {'ticker': 'AAPL', 'cik_str': 320193, 'title': 'Apple Inc.'}},
        {'cik': '0000320193', 'name': 'Apple Inc.', 'tickers': ['AAPL'],
         'filings': {'recent': {'accessionNumber': ['new'], 'form': ['10-K'],
                                'filingDate': ['2024-11-01']}, 'files': []}},
        {'cik': 320193, 'entityName': 'Apple Inc.', 'facts': {'us-gaap': {}}},
    ]


def run(data):
    calls = []
    def fetch(url, headers):
        calls.append((url, headers))
        value = data.pop(0)
        if isinstance(value, Exception):
            raise value
        if isinstance(value, bytes):
            return value
        return json.dumps(value).encode()
    return client().acquire('AAPL', '2024-12-31', 'Test Operator test@example.org', fetch), calls


def test_issuer_acquisition():
    result, calls = run(responses())
    assert result['company']['cik'] == 320193
    assert result['facts']['facts'] == {'us-gaap': {}}
    assert not result['errors']
    assert all(s['sha256'] and s['retrieved_at'] and s['payload'] for s in result['sources'])
    assert all(hashlib.sha256(s['raw_bytes']).hexdigest() == s['sha256'] for s in result['sources'])
    assert all(c[1]['User-Agent'] == 'Test Operator test@example.org' for c in calls)


@pytest.mark.parametrize('section', [1, 2])
@pytest.mark.parametrize('value,code', [
    (1, 'ISSUER_MISMATCH'), (320193.5, 'INVALID_SOURCE_DATA'),
    (320193.0, 'INVALID_SOURCE_DATA'), (True, 'INVALID_SOURCE_DATA'),
    ('320193.5', 'INVALID_SOURCE_DATA'), (' 320193', 'INVALID_SOURCE_DATA'),
])
def test_mismatched_issuer(section, value, code):
    data = responses()
    data[section]['cik'] = value
    result, _ = run(data)
    assert any(e['code'] == code for e in result['errors'])
    if code == 'ISSUER_MISMATCH':
        assert result['identity_valid'] is False


def test_archived_filings():
    data = responses()
    data[1]['filings']['files'] = [
        {'name': 'CIK0000320193-submissions-001.json', 'filingFrom': '2020-01-01'},
        {'name': 'CIK0000320193-submissions-002.json', 'filingFrom': '2025-01-01'},
        {'name': 'CIK0000320193-submissions-003.json', 'filingFrom': 'invalid'},
    ]
    data[2:2] = [
        {'accessionNumber': ['old', 'older'], 'form': ['10-Q', '10-K'],
         'filingDate': ['2023-01-01', '2022-01-01'], 'reportDate': ['2022-12-31']},
        {'accessionNumber': ['oldest'], 'form': ['10-K/A'], 'filingDate': ['2021-01-01']},
    ]
    result, calls = run(data)
    assert [r['accessionNumber'] for r in result['filings']] == ['new', 'old', 'older', 'oldest']
    assert [r.get('reportDate') for r in result['filings']] == [None, '2022-12-31', None, None]
    assert len(calls) == 5


@pytest.mark.parametrize('bad', [OSError('offline'), [], {'name': '../escape.json'},
                                     {'name': 'CIK0000000001-submissions-001.json'}])
def test_source_failure(bad):
    data = responses()
    if isinstance(bad, dict):
        data[1]['filings']['files'] = [bad]
    else:
        data[1]['filings']['files'] = [{'name': 'CIK0000320193-submissions-001.json'}]
        data[2:2] = [bad] * (3 if isinstance(bad, OSError) else 1)
    result, _ = run(data)
    assert result['errors']
    assert result['facts'] is not None
    assert any(s['status'] == 'error' for s in result['sources'])


def test_independent_import():
    result = subprocess.run([sys.executable, '-I', '-c',
                             f"import runpy; runpy.run_path({str(SCRIPT)!r})"], capture_output=True)
    assert result.returncode == 0, result.stderr


def test_no_original_runtime(monkeypatch):
    module = client()
    def forbidden(*args):
        pytest.fail('network request before input validation')
    with pytest.raises(ValueError, match='SEC_IDENTITY_REQUIRED'):
        module.acquire('AAPL', '2024-12-31', '', forbidden)
    assert not any('monkey' in str(v).lower() for v in vars(module).values() if hasattr(v, '__file__'))


@pytest.mark.parametrize('document', ['aapl.htm', '../aapl.htm', 'aapl.htm?x=1'])
def test_primary_document_transport(document, monkeypatch):
    from test_fiscal_quarter import declaration, evidence
    module = client()
    monkeypatch.setattr(module.time, 'sleep', lambda _: None)
    sample = evidence()
    data = responses()
    data[1]['filings']['recent'] = {k: [v] for k, v in sample['filings'][0].items()}
    data[1]['filings']['recent']['primaryDocument'] = [document]
    data[2]['facts'] = sample['facts']['facts']
    data.append(declaration().encode())
    calls = []
    def fetch(url, headers):
        calls.append(url)
        value = data.pop(0)
        return value if isinstance(value, bytes) else json.dumps(value).encode()
    result = module.acquire('AAPL', '2024-12-31', 'Test test@example.org', fetch,
                            fiscal_quarter='2024Q3')
    if document == 'aapl.htm':
        source = result['sources'][-1]
        assert source['status'] == 'valid' and source['raw_bytes'] == declaration().encode()
        assert source['sha256'] == hashlib.sha256(source['raw_bytes']).hexdigest()
        assert calls[-1] == 'https://www.sec.gov/Archives/edgar/data/320193/000032019324000081/aapl.htm'
    else:
        assert len(calls) == 3
        assert result['errors'][-1]['code'] == 'FISCAL_PERIOD_UNRESOLVED'
