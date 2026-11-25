# concern: Compact evidence must bind the captured source availability alongside its selected observations.
"""Reject a substitute capture with an identical projection and a different publication date."""
from pathlib import Path
import sys

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[5] / "obsidian-finance/tests"))

import test_research_continuation as continuation
from test_research_store import load


def test_capture_retimed_rejects_substitution(tmp_path, monkeypatch):
    """A valid alternate capture cannot rewrite the original availability."""
    continuation.test_fixed_quarter_updates_and_historical_read(tmp_path, monkeypatch, "normal")
    store = load()
    overview = next(tmp_path.rglob("*00 Research Overview.md"))
    original = overview.read_text()
    _, review = store._markdown.record(original, "quarter-overview")
    source_id = "filing-2024Q2"
    reference = review["quarter_evidence"]["units"]["credit"]["sources"][source_id]
    capture = overview.parent / reference
    _, record = store._markdown.record(capture.read_text(), "source-registration")
    assert record["available_at"] == "2024-08-01"

    modified = store._markdown.render_registration("bank-fixture", "source", {
        **record, "available_at": "2024-07-01",
    })
    substitute = capture.with_name(continuation.digest(modified) + ".md")
    substitute.write_text(modified)
    overview.write_text(original.replace(reference, substitute.relative_to(overview.parent).as_posix()))

    with pytest.raises(ValueError, match=source_id):
        store.verify_quarter(overview.parent, overview.name)
