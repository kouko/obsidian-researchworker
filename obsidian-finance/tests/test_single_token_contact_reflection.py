# concern: accepted single-token operator names leaking into SEC research artifacts
import json
import subprocess
import sys
from pathlib import Path

import test_acquire


def test_single_token_contact_reflection_is_withheld(tmp_path, monkeypatch):
    contact = {'name': 'OperatorProbeZeta', 'email': 'operator@example.invalid'}
    monkeypatch.setenv('HOME', str(tmp_path))
    subprocess.run(
        [sys.executable, str(test_acquire.SCRIPTS / 'acquire.py'), '--setup-contact'],
        input=json.dumps(contact), text=True, capture_output=True, timeout=10, check=True,
    )
    data = test_acquire.payloads()
    data[1]['name'] = contact['name']
    responses = iter(data)
    summary = test_acquire.module().run(
        ['--ticker', 'AAPL', '--period-start', '2024-01-01', '--period-end', '2024-12-31',
         '--as-of', '2024-12-31', '--output-dir', str(tmp_path / 'evidence')],
        fetch=lambda _url, _headers: json.dumps(next(responses)).encode(),
    )
    path = Path(summary['run_path'])
    manifest = test_acquire.read(path, 'manifest.json')
    source = next(source for source in manifest['sources'] if source['id'] == 'submissions')
    assert source['path'] is None and source['sha256'] is None
    assert any(error['code'] == 'CONTACT_REFLECTED' for error in summary['errors'])
