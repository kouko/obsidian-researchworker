import json
import sys
from pathlib import Path

import pytest

sys.path.insert(
    0, str(Path(__file__).resolve().parents[1] / "skills/technical-analysis/scripts")
)
from snapshot import load_snapshot, validate_snapshot

CUTOFF = "2026-07-06T19:00:00-04:00"


@pytest.fixture
def payload():
    return {
        "ticker": "TEST",
        "timezone": "America/New_York",
        "source": "Test provider",
        "adjustment": "unadjusted",
        "available_at": "2026-07-06T18:00:00-04:00",
        "evidence": "capture record one",
        "bars": [
            {
                "date": "2026-07-06",
                "session_close": "2026-07-06T16:00:00-04:00",
                "open": 100,
                "high": 102,
                "low": 99,
                "close": 101,
                "volume": None,
            }
        ],
    }


def test_snapshot_identity_and_historical_version(payload, tmp_path):
    source = tmp_path / "snapshot.json"
    source.write_text(json.dumps(payload))
    result = load_snapshot(source, CUTOFF)
    assert result == validate_snapshot(payload, CUTOFF)
    assert result["bars"][0]["volume"] is None
    assert result["exclusions"] == []

    payload["adjustment"] = "split-adjusted"
    assert validate_snapshot(payload, CUTOFF)["snapshot_id"] != result["snapshot_id"]


def test_retroactively_downloaded_or_unverifiable_version_is_ineligible(payload):
    payload["available_at"] = "2026-07-07T18:00:00-04:00"
    result = validate_snapshot(payload, CUTOFF)
    assert result["bars"] == []
    assert "cutoff" in result["exclusions"][0]

    payload["available_at"] = "2026-07-06T18:00:00-04:00"
    del payload["evidence"]
    result = validate_snapshot(payload, CUTOFF)
    assert result["bars"] == []
    assert "evidence" in result["exclusions"][0]


def test_excludes_incomplete_and_future_sessions(payload):
    bar = payload["bars"][0]
    bar["complete"] = False
    payload["bars"].append(
        dict(bar, date="2026-07-07", session_close="2026-07-07T16:00:00-04:00")
    )
    result = validate_snapshot(payload, CUTOFF)
    assert result["bars"] == []
    assert len(result["exclusions"]) == 2
    assert result["missing_completed_sessions"] == ["2026-07-06"]


def test_completed_but_ineligible_row_is_a_known_gap(payload):
    payload["bars"][0]["available_at"] = "2026-07-06T15:00:00-04:00"
    result = validate_snapshot(payload, CUTOFF)
    assert result["bars"] == []
    assert result["missing_completed_sessions"] == ["2026-07-06"]


def test_rejects_invalid_prices_and_duplicates(payload):
    payload["bars"][0]["high"] = float("nan")
    with pytest.raises(ValueError, match="high"):
        validate_snapshot(payload, CUTOFF)
    payload["bars"][0]["high"] = 102
    payload["bars"].append(payload["bars"][0])
    with pytest.raises(ValueError, match="Duplicate"):
        validate_snapshot(payload, CUTOFF)
