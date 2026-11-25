# concern: An interrupted Taiwan quarter must not become current while its bound source evidence is unavailable.
"""Check recovery before a pending overview becomes the current review."""

import json
from pathlib import Path
import sys

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[5] / "obsidian-finance" / "tests"))
import test_research_continuation as continuation


def test_recovery_missing_bound_source_preserves_overview(tmp_path, monkeypatch):
    """An intact review companion is insufficient when its bound source is missing."""
    module = continuation.load()
    recover = module.recover_quarterly
    monkeypatch.setattr(continuation, "load", lambda: module)
    folder = tmp_path / "investing/assets/equities/twse-1611/cycles/2024Q2"
    checked = False

    def recover_with_missing_source(root, asset, quarter):
        nonlocal checked
        companions = list((folder / "data/reviews").glob("*.json"))
        if checked or (asset, quarter) != ("twse-1611", "2024Q2") or len(companions) != 2:
            return recover(root, asset, quarter)
        checked = True
        pending = next(review for path in companions
                       if (review := json.loads(path.read_text())["review"])["id"] == "fixed2")
        reference = next(iter(pending["quarter_evidence"]["units"]["credit"]["sources"].values()))
        captured = folder / reference
        original = captured.read_bytes()
        overview, = folder.glob("*00 季度研究總覽.md")
        before = overview.read_bytes()
        captured.unlink()
        try:
            with pytest.raises((OSError, ValueError), match="evidence|source|No such file"):
                recover(root, asset, quarter)
            assert overview.read_bytes() == before
        finally:
            captured.write_bytes(original)
        return recover(root, asset, quarter)

    monkeypatch.setattr(module, "recover_quarterly", recover_with_missing_source)
    continuation.test_fixed_quarter_updates_and_historical_read(
        tmp_path, monkeypatch, "interrupted", "twse-1611",
    )
    assert checked
