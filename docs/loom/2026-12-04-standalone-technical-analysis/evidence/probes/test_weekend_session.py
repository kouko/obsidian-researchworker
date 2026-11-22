# concern: A non-trading date cannot be consumed as a completed U.S. daily bar.
from pathlib import Path
import sys


sys.path.insert(0, str(Path(__file__).resolve().parents[5] /
                       "obsidian-finance/skills/technical-analysis/scripts"))
from snapshot import validate_snapshot


def test_saturday_is_not_a_completed_us_equity_session():
    cutoff = "2026-08-23T20:00:00+00:00"
    payload = {
        "ticker": "TEST", "timezone": "America/New_York",
        "source": "Synthetic capture with accidental weekend row",
        "adjustment": "unadjusted", "evidence": "Synthetic retained exact version",
        "available_at": cutoff,
        "bars": [{
            "date": "2026-08-22", "session_close": "2026-08-22T20:00:00+00:00",
            "open": 100, "high": 102, "low": 99, "close": 101, "volume": 1000,
        }],
    }
    try:
        validated = validate_snapshot(payload, cutoff)
    except ValueError:
        return
    assert validated["bars"] == []
    assert validated["exclusions"]
