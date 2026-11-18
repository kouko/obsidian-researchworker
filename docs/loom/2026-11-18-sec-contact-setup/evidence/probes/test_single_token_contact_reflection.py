# concern: accepted single-token operator names leaking into SEC research artifacts
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[5] / 'obsidian-finance/tests'))

import test_acquire


def test_single_token_contact_reflection_is_withheld(tmp_path, monkeypatch):
    contact = {'name': 'OperatorProbeZeta', 'email': 'operator@example.invalid'}
    monkeypatch.setattr(test_acquire, 'CONTACT', contact)
    data = test_acquire.payloads()
    data[1]['name'] = contact['name']
    summary, path, _ = test_acquire.execute(tmp_path, monkeypatch, data)
    manifest = test_acquire.read(path, 'manifest.json')
    source = next(source for source in manifest['sources'] if source['id'] == 'submissions')
    assert source['path'] is None and source['sha256'] is None
    assert any(error['code'] == 'CONTACT_REFLECTED' for error in summary['errors'])
