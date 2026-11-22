# concern: A malformed quarter overview must not abort vault-wide discovery.
"""Probe read-only handling of an edited overview with an incorrect units type."""
from pathlib import Path
import re
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[5] / "obsidian-finance/tests"))

import test_research_continuation as continuation
from test_research_store import CUTOFF, load


def test_discovery_malformedunits_reports_gap(tmp_path, monkeypatch):
    """Recognize a malformed saved overview without mutating the user's edit."""
    continuation.test_fixed_quarter_updates_and_historical_read(tmp_path, monkeypatch, "normal")
    overview = next(tmp_path.rglob("*00 Research Overview.md"))
    modified, count = re.subn(r"(?ms)^units:\n.*?(?=^\S)", "units: []\n", overview.read_text())
    assert count == 1
    overview.write_text(modified)

    view = load().discover(tmp_path, "latest", CUTOFF, storage="quarterly")

    assert any(gap["evidence"] == "quarterly overview" for gap in view["gaps"])
    assert not any("/fixed2" in item["record"] for item in view["reusable"])
    assert overview.read_text() == modified
