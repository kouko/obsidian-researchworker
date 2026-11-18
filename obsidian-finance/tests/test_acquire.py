import hashlib
import importlib.util
import json
import os
import pty
import select
import signal
import stat
import subprocess
from pathlib import Path
import sys
import termios

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


def execute(tmp_path, monkeypatch, data=None, extra=(), selectors=None, contact=None):
    configure_contact(tmp_path, monkeypatch, saved=contact is None)
    if contact is not None:
        import sec_contact
        sec_contact.save(contact)
    data = payloads() if data is None else data
    calls = []
    def fetch(url, headers):
        calls.append(url)
        item = data.pop(0)
        if isinstance(item, bytes):
            return item
        return json.dumps(item).encode()
    selectors = (['--period-start', '2024-01-01', '--period-end', '2024-12-31',
                  '--as-of', '2024-12-31'] if selectors is None else selectors)
    args = ['--ticker', 'AAPL', *selectors, '--output-dir', str(tmp_path), *extra]
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


@pytest.mark.parametrize('section,bad', [
    (1, b'bad'), (2, b'bad'),
    ('accession', '../untrusted'), ('accession', None),
    ('accession', []), ('accession', {}), ('accession', True),
    ('accession', '００００３２０１９３-２４-０００００１'),
])
def test_unavailable_sections(tmp_path, monkeypatch, section, bad):
    data = payloads()
    if section == 'accession':
        data[1]['filings']['recent']['accessionNumber'][0] = bad
    else:
        data[section] = bad
    summary, path, _ = execute(tmp_path, monkeypatch, data)
    assert summary['status'] == 'partial'
    assert read(path, 'manifest.json')['errors'][0]['code'] == 'INVALID_SOURCE_DATA'
    if section == 'accession':
        assert read(path, 'filings.json') == []
        assert read(path, 'coverage.json')['filing_excluded']['invalid_accession'] == 1
        assert read(path, 'eligible-facts.json')[0]['accession_in_inventory'] is False


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


def test_after_hours_apple_replay(tmp_path, monkeypatch):
    data = payloads()
    block = data[1]['filings']['recent']
    block.update(accessionNumber=['0000320193-24-000081'], form=['10-Q'],
        filingDate=['2024-08-02'], reportDate=['2024-06-29'],
        acceptanceDateTime=['2024-08-01T22:03:34Z'])
    data[2]['facts']['us-gaap']['Revenues']['units']['USD'][0].update(
        accn='0000320193-24-000081', filed='2024-08-02', end='2024-06-29')
    summary, path, _ = execute(tmp_path, monkeypatch, data)
    assert summary['status'] == 'complete'
    assert read(path, 'eligible-facts.json')[0]['accession_in_inventory']
    filing = read(path, 'filings.json')[0]
    assert (filing['acceptanceDateTime'], filing['filingDate']) == (
        '2024-08-01T22:03:34Z', '2024-08-02')


@pytest.mark.parametrize('mode', ['date', 'acceptance', 'malformed_acceptance', 'duplicate'])
def test_amendment_conflict(tmp_path, monkeypatch, mode):
    data = payloads()
    block = data[1]['filings']['recent']
    if mode == 'date':
        data[2]['facts']['us-gaap']['Revenues']['units']['USD'][0]['filed'] = '2024-11-02'
    elif mode == 'acceptance':
        block['acceptanceDateTime'] = ['2025-01-01T10:00:00Z']
    elif mode == 'malformed_acceptance':
        block['acceptanceDateTime'] = ['not-a-timestamp']
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
    configure_contact(tmp_path, monkeypatch, saved=mode != 'identity')
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


@pytest.mark.parametrize('quarter,focus', [('2024Q3', 'Q3'), ('2024Q4', 'FY')])
def test_quarter_package(tmp_path, monkeypatch, quarter, focus):
    from datetime import datetime, timezone
    from test_fiscal_quarter import declaration, evidence
    data = payloads()
    sample = evidence(focus)
    data[1]['filings']['recent'] = {k: [v] for k, v in sample['filings'][0].items()}
    facts = data[2]['facts']['us-gaap']['Revenues']['units']['USD']
    facts[0].update(accn='0000320193-24-000081', filed='2024-08-02', end='2024-06-29', fy=2024, fp=focus)
    facts.extend([dict(facts[0], start='2024-03-31', val=20),
                  dict(facts[0], end='2023-06-29', val=90)])
    html = declaration(focus).replace('name="dei:DocumentPeriodEndDate"',
        'name="dei:DocumentPeriodEndDate" format="ixt:date-monthname-day-year-en"').replace(
            '2024-06-29', 'June&nbsp;29, 2024')
    data.append(html.encode())
    summary, path, calls = execute(tmp_path, monkeypatch, data, selectors=['--fiscal-quarter', quarter])
    assert (summary['status'], summary['exit_code']) == ('complete', 0)
    assert summary['mode'] == 'retrospective'
    assert summary['effective_cutoff'] == datetime.now(timezone.utc).date().isoformat()
    assert summary['resolution']['period_end'] == '2024-06-29'
    rows = read(path, 'eligible-facts.json')
    assert [row['val'] for row in rows] == [100, 20]
    assert [row['start'] for row in rows] == ['2023-10-01', '2024-03-31']
    manifest = read(path, 'manifest.json')
    assert manifest['resolution'] == summary['resolution']
    source = manifest['sources'][-1]
    assert source['path'].endswith('.html')
    assert (path / source['path']).read_bytes() == html.encode()
    assert 'test@example.org' not in json.dumps(manifest)
    assert len(calls) == 4


@pytest.mark.parametrize('mode', ['future', 'contradictory', 'source_failure'])
def test_quarter_unresolved(tmp_path, monkeypatch, mode):
    from test_fiscal_quarter import declaration, evidence
    data = payloads()
    sample = evidence()
    data[1]['filings']['recent'] = {k: [v] for k, v in sample['filings'][0].items()}
    data[2]['facts'] = sample['facts']['facts']
    html = declaration(end='2024-06-30' if mode == 'contradictory' else '2024-06-29')
    data.append(b'bad html' if mode == 'source_failure' else html.encode())
    summary, path, calls = execute(tmp_path, monkeypatch, data,
        selectors=['--fiscal-quarter', '2024Q3', '--as-of', '2024-08-01' if mode == 'future' else '2024-12-31'])
    assert (summary['status'], summary['exit_code']) == ('failed', 1)
    assert summary['mode'] == 'historical'
    assert any(e['code'] == 'FISCAL_PERIOD_UNRESOLVED' for e in summary['errors'])
    assert not (path / 'eligible-facts.json').exists() and not (path / 'completion.json').exists()
    assert (path / 'raw/companyfacts.json').exists()
    assert len(calls) == (3 if mode == 'future' else 4)


@pytest.mark.parametrize('selectors', [
    ['--fiscal-quarter', '2024Q5'], ['--fiscal-quarter', '2024Q3', '--period-start', '2024-01-01'],
    ['--period-start', '2024-01-01', '--period-end', '2024-12-31'],
])
def test_quarter_invalid_selectors(tmp_path, monkeypatch, selectors):
    summary, path, calls = execute(tmp_path, monkeypatch, selectors=selectors)
    assert summary['exit_code'] == 64 and calls == [] and path is None


CONTACT = {'name': '測試 Operator', 'email': 'test@example.org'}


def configure_contact(tmp_path, monkeypatch, *, saved=True):
    monkeypatch.setenv('HOME', str(tmp_path))
    monkeypatch.setenv('SEC_USER_AGENT', 'Ignored old@example.org')
    if saved:
        import sec_contact
        sec_contact.save(CONTACT)


def run_cli(*args, payload=None):
    return subprocess.run([sys.executable, *args], input=payload, text=True,
                          capture_output=True, check=False)


def test_setup_cli_and_later_acquisition(tmp_path, monkeypatch):
    configure_contact(tmp_path, monkeypatch, saved=False)
    acquire_script = str(SCRIPTS / 'acquire.py')
    setup = run_cli(acquire_script, '--setup-contact', payload=json.dumps(CONTACT))
    assert setup.returncode == 0, setup
    profile = tmp_path / '.config/obsidian-finance/sec-contact.json'
    assert stat.S_IMODE(profile.stat().st_mode) == 0o600
    assert json.loads(profile.read_text()) == CONTACT
    assert setup.stderr == ''
    assert all(value not in setup.stdout for value in CONTACT.values())

    # Separate Python process, real argv and stored contact, offline transport.
    later = run_cli('-c', """
import json
import os
import pty
import select
import signal
import sys
sys.path.insert(0, sys.argv[1])
import acquire
def fetch(url, headers):
    assert headers['User-Agent'] == '測試 Operator test@example.org'
    return b'{}'
result = acquire.run(sys.argv[2:], fetch)
assert result['errors'][0]['code'] == 'ISSUER_NOT_FOUND'
print(json.dumps(result))
""", str(SCRIPTS), '--ticker', 'AAPL', '--fiscal-quarter', '2024Q3',
                    '--output-dir', str(tmp_path / 'runs'))
    assert later.returncode == 0, later
    assert all(value not in later.stdout + later.stderr for value in CONTACT.values())


@pytest.mark.parametrize(('state', 'expected'), [
    ('missing', 'SEC_CONTACT_REQUIRED'), ('corrupt', 'SEC_CONTACT_UNUSABLE'),
    ('unsafe', 'SEC_CONTACT_UNUSABLE'),
])
def test_contact_preflight_ignores_old_environment(tmp_path, monkeypatch, state, expected):
    configure_contact(tmp_path, monkeypatch, saved=state != 'missing')
    config = tmp_path / '.config/obsidian-finance/sec-contact.json'
    if state == 'corrupt':
        config.write_text(CONTACT['email'])
    if state == 'unsafe':
        config.chmod(0o644)
    destination = tmp_path / 'output'
    result = module().run(['--ticker', 'AAPL', '--fiscal-quarter', '2024Q3',
                           '--output-dir', str(destination)],
                          lambda *args: pytest.fail('Unexpected network request'))
    assert result['error'].startswith(expected)
    assert CONTACT['email'] not in result['error']
    assert not destination.exists()


@pytest.mark.parametrize('payload', [
    {'name': '  ', 'email': 'test@example.org'},
    {'name': 'Synthetic', 'email': 'test@example.org\r\nX-Test: dropped'},
    {'name': 'Synthetic', 'email': 'test@example.org'},
    {'name': 'Synthetic', 'email': 'test..operator@example.org'},
    {'name': 'Synthetic', 'email': 'test@example.org', 'extra': 'unexpected'},
])
def test_invalid_setup_preserves_private_profile(tmp_path, monkeypatch, payload):
    configure_contact(tmp_path, monkeypatch)
    result = run_cli(str(SCRIPTS / 'acquire.py'), '--setup-contact', payload=json.dumps(payload))
    assert result.returncode == 64
    assert json.loads(result.stdout)['error'].startswith('SEC_CONTACT_INVALID')
    assert all(value not in result.stdout + result.stderr for value in CONTACT.values())
    profile = tmp_path / '.config/obsidian-finance/sec-contact.json'
    assert json.loads(profile.read_text()) == CONTACT


def test_denied_replace_preserves_previous_contact(tmp_path, monkeypatch, capsys):
    import io
    import sec_contact
    configure_contact(tmp_path, monkeypatch)
    profile = tmp_path / '.config/obsidian-finance/sec-contact.json'
    old = profile.read_bytes()
    replacement = {'name': 'Other operator', 'email': 'other@example.org'}

    def deny(*args, **kwargs):
        raise PermissionError(replacement['email'])

    monkeypatch.setattr(sec_contact.os, 'replace', deny)
    monkeypatch.setattr(sys, 'stdin', io.StringIO(json.dumps(replacement)))
    assert module().main(['--setup-contact']) == 64
    output = capsys.readouterr()
    assert 'SEC_CONTACT_SAVE_FAILED' in output.out
    assert replacement['email'] not in output.out + output.err
    assert profile.read_bytes() == old
    assert list(profile.parent.iterdir()) == [profile]


@pytest.mark.parametrize(('name', 'response_value'), [
    (CONTACT['name'], CONTACT['name']),
    ('SyntheticOperator', 'SyntheticOperator'),
    ('SyntheticOperator', 'Operator: SyntheticOperator.'),
    ('SyntheticOperator', b'{"message": "Operator: SyntheticOperator."'),
    ('林', rb'{"name": "\u6797"'),
    ('林', '林'),
])
def test_reflected_contact_not_retained(tmp_path, monkeypatch, name, response_value):
    contact = dict(CONTACT, name=name)
    data = payloads()
    if isinstance(response_value, bytes):
        data[1] = response_value
    else:
        data[1]['name'] = response_value
    summary, path, _ = execute(tmp_path, monkeypatch, data, contact=contact)
    assert summary['status'] == 'partial'
    source = read(path, 'manifest.json')['sources'][1]
    assert source['path'] is None and source['sha256'] is None
    assert any(error['code'] == 'CONTACT_REFLECTED' for error in summary['errors'])
    for file in path.rglob('*'):
        if file.is_file():
            assert all(value not in file.read_text() for value in contact.values())


def test_symlinked_profile_directory_is_unusable_and_cannot_store_contact(tmp_path, monkeypatch):
    configure_contact(tmp_path, monkeypatch, saved=False)
    other = tmp_path / 'managed-research'
    other.mkdir()
    config = tmp_path / '.config'
    config.mkdir()
    (config / 'obsidian-finance').symlink_to(other, target_is_directory=True)
    acquisition = ['--ticker', 'AAPL', '--fiscal-quarter', '2024Q3',
                   '--output-dir', str(tmp_path / 'output')]
    setup = run_cli(str(SCRIPTS / 'acquire.py'), '--setup-contact', payload=json.dumps(CONTACT))
    assert setup.returncode == 64
    assert json.loads(setup.stdout)['error'].startswith('SEC_CONTACT_SAVE_FAILED')
    assert list(other.iterdir()) == []

    redirected_profile = other / 'sec-contact.json'
    redirected_profile.write_text(json.dumps(CONTACT))
    redirected_profile.chmod(0o600)
    result = module().run(acquisition, lambda *args: pytest.fail('Unexpected network request'))
    assert result['error'].startswith('SEC_CONTACT_UNUSABLE')
    assert not (tmp_path / 'output').exists()


@pytest.mark.parametrize('mode', ['valid', 'invalid', 'interrupt', 'terminate', 'timeout', 'eof'])
def test_separate_terminal_contact_input(tmp_path, monkeypatch, mode):
    configure_contact(tmp_path, monkeypatch)
    profile = tmp_path / '.config/obsidian-finance/sec-contact.json'
    original_bytes = profile.read_bytes()
    operator = {'name': 'PTY Test Operator', 'email': 'pty@example.org'}
    payload = json.dumps(operator).encode()
    master, slave = pty.openpty()
    initial = termios.tcgetattr(slave)
    initial[3] |= termios.ECHO | termios.ECHONL
    termios.tcsetattr(slave, termios.TCSANOW, initial)
    command = [sys.executable, str(SCRIPTS / 'acquire.py'), '--setup-contact', '--terminal']
    if mode == 'timeout':
        command = [sys.executable, '-c',
                   'import acquire; acquire.sec_contact.TERMINAL_TIMEOUT = 0.5; '
                   'raise SystemExit(acquire.main(["--setup-contact", "--terminal"]))']
    process = subprocess.Popen(command, cwd=SCRIPTS, stdin=slave, stdout=slave, stderr=slave)
    output = b''
    try:
        assert select.select([master], [], [], 5)[0], 'terminal did not signal readiness'
        output += os.read(master, 8192)
        assert output.strip() == b'READY_FOR_SEPARATE_INPUT'
        assert not termios.tcgetattr(slave)[3] & (termios.ECHO | termios.ECHONL)

        if mode == 'valid':
            # More bytes than the usual canonical terminal limit.
            os.write(master, payload + b' ' * 5000 + b'\n')
        elif mode == 'invalid':
            os.write(master, payload[:-1] + b'\n')
        else:
            os.write(master, payload[:-1])
            if mode == 'interrupt':
                process.send_signal(signal.SIGINT)
            elif mode == 'terminate':
                process.send_signal(signal.SIGTERM)
            elif mode == 'eof':
                os.write(master, b'\x04')

        assert process.wait(timeout=5) == (0 if mode == 'valid' else 64)
        while select.select([master], [], [], 0)[0]:
            output += os.read(master, 8192)
        assert termios.tcgetattr(slave) == initial
        assert all(value.encode() not in output for value in operator.values())
        summary = json.loads(output.splitlines()[1])
        if mode == 'valid':
            assert summary['status'] == 'configured'
            assert json.loads(profile.read_bytes()) == operator
        else:
            assert summary['status'] == 'failed'
            assert profile.read_bytes() == original_bytes
    finally:
        if process.poll() is None:
            process.kill()
            process.wait()
        os.close(master)
        os.close(slave)
