# concern: malformed SEC issuer identities must not produce completed analytical datasets
"""Exercise hostile issuer and filing identifiers through the offline pipeline."""

import importlib.util
from pathlib import Path

import pytest

ROOT = next(parent for parent in Path(__file__).resolve().parents
            if (parent / 'obsidian-finance/tests/test_acquire.py').is_file())
SPEC = importlib.util.spec_from_file_location(
    'finance_test_helpers', ROOT / 'obsidian-finance/tests/test_acquire.py')
HELPERS = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(HELPERS)


@pytest.mark.parametrize('section', [1, 2])
def test_issuer_fractionalcik_rejected(tmp_path, monkeypatch, section):
    """Reject a fractional issuer number instead of truncating its identity."""
    data = HELPERS.payloads()
    data[section]['cik'] = 320193.5
    summary, path, _ = HELPERS.execute(tmp_path, monkeypatch, data)
    assert summary['status'] != 'complete'
    assert any(error['code'] in ('INVALID_SOURCE_DATA', 'ISSUER_MISMATCH')
               for error in summary['errors'])
