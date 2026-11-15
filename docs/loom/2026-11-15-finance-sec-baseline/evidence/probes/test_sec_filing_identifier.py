# concern: malformed filing accessions must not enter traceable analytical inventory
"""Exercise invalid filing identifiers through the offline acquisition pipeline."""

import importlib.util
from pathlib import Path

ROOT = next(parent for parent in Path(__file__).resolve().parents
            if (parent / 'obsidian-finance/tests/test_acquire.py').is_file())
SPEC = importlib.util.spec_from_file_location(
    'finance_test_helpers', ROOT / 'obsidian-finance/tests/test_acquire.py')
HELPERS = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(HELPERS)


def test_inventory_invalidaccession_excluded(tmp_path, monkeypatch):
    """Do not mark an untraceable filing as eligible analytical inventory."""
    data = HELPERS.payloads()
    data[1]['filings']['recent']['accessionNumber'][0] = '../untrusted'
    summary, path, _ = HELPERS.execute(tmp_path, monkeypatch, data)
    inventory = HELPERS.read(path, 'filings.json')
    assert all(row.get('source_url') for row in inventory)
