from datetime import date, datetime, timezone
from pathlib import Path
from types import SimpleNamespace
import importlib.util

import pytest


SCRIPT = Path(__file__).parents[1] / "skills/technical-analysis/scripts/fetch_daily.py"


def load_module(script):
    spec = importlib.util.spec_from_file_location(script.stem, script)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def fetch_module():
    return load_module(SCRIPT)


class FakeHistory(list):
    def iterrows(self):
        return iter(self)


class FakeTicker:
    def __init__(self, **metadata):
        self.metadata = {
            "symbol": "AAPL",
            "instrumentType": "EQUITY",
            "exchangeName": "NMS",
            "exchangeTimezoneName": "America/New_York",
            "currency": "USD",
            **metadata,
        }

    def history(self, **options):
        assert options["interval"] == "1d"
        assert options["auto_adjust"] is True
        assert options["prepost"] is False
        return FakeHistory(
            (datetime.fromisoformat(day), {
                "Open": 101, "High": 104, "Low": 99, "Close": 103, "Volume": volume,
            })
            for day, volume in [
                ("2026-11-25", 1000), ("2026-11-26", 10),
                ("2026-11-27", float("nan")),
            ]
        )

    def get_history_metadata(self):
        return self.metadata


class Calendar:
    def is_session(self, day):
        return day != "2026-11-26"

    def session_close(self, day):
        hour = 18 if day == "2026-11-27" else 21
        return datetime.combine(date.fromisoformat(day), datetime.min.time(), timezone.utc).replace(hour=hour)

    def sessions_in_range(self, start, end):
        return [
            datetime.fromisoformat(day)
            for day in ("2026-11-25", "2026-11-27", "2026-11-30")
            if start <= day <= end
        ]


def dependencies(start, end, **metadata):
    clock = iter(datetime.fromisoformat(value) for value in (start, end))
    return {
        "provider": SimpleNamespace(Ticker=lambda _: FakeTicker(**metadata), __version__="test"),
        "calendar": Calendar(),
        "now": lambda: next(clock),
    }


def test_completed_shortened_session_and_holiday():
    result = fetch_module().fetch_daily("aapl", **dependencies(
        "2026-11-27T18:01:00+00:00", "2026-11-27T18:02:00+00:00",
    ))
    assert result["ticker"] == "AAPL"
    assert result["available_at"] == "2026-11-27T18:02:00+00:00"
    assert result["evidence"]
    assert [bar["date"] for bar in result["bars"]] == ["2026-11-25", "2026-11-27"]
    assert result["bars"][-1]["volume"] is None


def test_in_progress_at_request_start_stays_excluded_after_close():
    result = fetch_module().fetch_daily("AAPL", **dependencies(
        "2026-11-27T17:59:00+00:00", "2026-11-27T18:01:00+00:00",
    ))
    assert [bar["date"] for bar in result["bars"]] == ["2026-11-25"]


def test_non_equity_or_non_us_listing_rejected():
    module = fetch_module()
    for metadata in ({"instrumentType": "ETF"}, {"exchangeName": "TOR"}):
        with pytest.raises(ValueError, match="U.S. equity"):
            module.fetch_daily("AAPL", **dependencies(
                "2026-11-27T18:01:00+00:00", "2026-11-27T18:02:00+00:00", **metadata,
            ))


def test_missing_completed_session_is_reported():
    result = fetch_module().fetch_daily("AAPL", **dependencies(
        "2026-11-30T21:01:00+00:00", "2026-11-30T21:02:00+00:00",
    ))
    assert "2026-11-30: completed exchange session missing from provider data." in (
        result["fetch_exclusions"]
    )
    assert result["missing_completed_sessions"] == ["2026-11-30"]


def test_snapshot_preserves_fetch_evidence_and_admits_valid_bars():
    result = fetch_module().fetch_daily("AAPL", **dependencies(
        "2026-11-30T21:01:00+00:00", "2026-11-30T21:02:00+00:00",
    ))
    normalized = load_module(SCRIPT.with_name("snapshot.py")).validate_snapshot(
        result, result["available_at"],
    )
    assert normalized["fetch_settings"] == result["fetch_settings"]
    assert normalized["latest_expected_session"] == "2026-11-30"
    assert normalized["missing_completed_sessions"] == ["2026-11-30"]
    assert normalized["exclusions"] == result["fetch_exclusions"]
    assert len(normalized["bars"]) == 2


def test_missing_sessions_are_canonical_and_part_of_source_identity():
    result = fetch_module().fetch_daily("AAPL", **dependencies(
        "2026-11-30T21:01:00+00:00", "2026-11-30T21:02:00+00:00",
    ))
    validate = load_module(SCRIPT.with_name("snapshot.py")).validate_snapshot
    cutoff = result["available_at"]
    normalized = validate(result, cutoff)
    assert normalized["snapshot_id"] != validate(
        {**result, "missing_completed_sessions": []}, cutoff
    )["snapshot_id"]
    with pytest.raises(ValueError, match="missing_completed_sessions"):
        validate({**result, "missing_completed_sessions": ["20261128"]}, cutoff)
