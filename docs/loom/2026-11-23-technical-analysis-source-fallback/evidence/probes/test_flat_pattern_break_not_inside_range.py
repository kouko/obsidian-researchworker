# concern: A close inside a pattern's own dated support or resistance can be reported as a breakout.
import json
from pathlib import Path
import subprocess
import sys

import pytest


FINANCE = Path(__file__).resolve().parents[5] / "obsidian-finance"


@pytest.mark.parametrize("kind, pivots, inside_close, outside_close", [
    ("Rectangle", [110, 90, 112.9, 91], 112.3, 115),
    ("Rectangle", [110, 87.1, 111, 90], 87.7, 85),
    ("Ascending triangle", [110, 90, 112.9, 96], 112.3, 115),
    ("Descending triangle", [114, 87.1, 108, 90], 87.7, 85),
])
def test_flat_boundary_inside_close_remains_candidate(
    tmp_path, monkeypatch, kind, pivots, inside_close, outside_close
):
    """A qualifying close clears the full observed horizontal side of a formation."""
    monkeypatch.syspath_prepend(str(FINANCE / "tests"))
    from test_technical_analysis import pattern_snapshot, set_price

    payload, _ = pattern_snapshot(pivots)
    payload["evidence"] = "Synthetic completed-session snapshot for this test."
    snapshot = tmp_path / "snapshot.json"
    command = [sys.executable, str(FINANCE / "skills/technical-analysis/scripts/report.py"), str(snapshot)]
    for close, expected in ((inside_close, "candidate"), (outside_close, "confirmed")):
        set_price(payload["bars"][-1], close)
        snapshot.write_text(json.dumps(payload), encoding="utf-8")
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        short = result.stdout.split("## Short term", 1)[1].split("## Medium term", 1)[0]
        assert f"**{kind} — {expected}**" in short
