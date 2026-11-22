import importlib.util
from datetime import date, timedelta
from pathlib import Path

import pytest


@pytest.fixture(scope="module")
def analyzer():
    path = Path(__file__).resolve().parents[1] / "skills/technical-analysis/scripts/analyze.py"
    spec = importlib.util.spec_from_file_location("finance_technical_analyze", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def snapshot(start="2023-10-01", stop="2024-02-29"):
    session = date.fromisoformat(start)
    last = date.fromisoformat(stop)
    bars = []
    while session <= last:
        if session.weekday() < 5:
            price = 100.0 + len(bars) / 2
            bars.append({
                "date": session.isoformat(), "session_close": f"{session}T21:00:00Z",
                "open": price - 0.25, "high": price + 1, "low": price - 1,
                "close": price, "volume": 200 if session == last else 100,
            })
        session += timedelta(days=1)
    return {
        "ticker": "TEST", "timezone": "America/New_York", "source": "fixture",
        "adjustment": "unadjusted", "available_at": f"{last}T22:00:00Z",
        "snapshot_id": "fixture-v1", "cutoff": f"{last}T23:00:00Z",
        "bars": bars, "exclusions": [],
    }


def test_indicators_levels_and_warmup_are_separate(analyzer):
    local = snapshot()
    report = analyzer.analyze(local)
    assert report == analyzer.analyze(local)
    short, medium, long = report["horizons"]
    assert short["trend"] == medium["trend"] == "up"
    assert short["metrics"]["volume_ratio"] == 2.0
    assert short["metrics"]["sma"]["20"] == pytest.approx(local["bars"][-1]["close"] - 4.75)
    assert short["metrics"]["sma"]["200"] is None
    assert short["levels"]["resistance"]["date"] == "2024-02-29"
    assert short["trigger"] and short["invalidation"]
    assert "pullback" in short["alternative"]
    assert long["trend"] == "insufficient"
    assert long["limitations"]


def test_forward_lengths_and_chronology(analyzer):
    short, medium, long = analyzer.analyze(snapshot())["horizons"]
    assert all(item["outlook_start"] == "2024-03-01" for item in (short, medium, long))
    assert [item["outlook_end"] for item in (short, medium, long)] == [
        "2024-03-21", "2024-05-29", "2025-02-28",
    ]
    assert short["observed_start"] == "2024-02-08"
    assert short["observed_end"] == "2024-02-29"


def test_future_bars_do_not_confirm_a_past_swing(analyzer):
    local = snapshot()
    pivot = local["bars"][-2]
    pivot["high"] += 10
    original = analyzer.analyze(local)
    assert all(point["date"] != pivot["date"] for point in original["horizons"][0]["swings"])
    future = {**local["bars"][-1], "date": "2024-03-01", "session_close": "2024-03-01T21:00:00Z"}
    assert analyzer.analyze({**local, "bars": local["bars"] + [future]}) == original


def test_empty_snapshot_keeps_all_outlook_windows(analyzer):
    local = {**snapshot(), "bars": [], "exclusions": ["No eligible version at cutoff"]}
    report = analyzer.analyze(local)
    assert report["exclusions"] == local["exclusions"]
    for horizon in report["horizons"]:
        assert horizon["trend"] == "insufficient"
        assert horizon["observed_start"] is None
        assert horizon["outlook_end"] is not None


def test_missing_volume_and_sparse_history_are_exposed(analyzer):
    local = snapshot()
    local["bars"][-1]["volume"] = None
    local["bars"] = local["bars"][:-13] + local["bars"][-1:]
    short = analyzer.analyze(local)["horizons"][0]
    assert short["trend"] == "insufficient"
    assert short["metrics"]["volume_ratio"] is None
    assert any("gap" in message.lower() for message in short["limitations"])
    assert any("volume" in message.lower() for message in short["limitations"])


def test_stale_data_remains_visible(analyzer):
    local = {**snapshot(), "cutoff": "2024-03-08T23:00:00Z",
             "fetch_exclusions": ["The provider did not return the last completed session."]}
    report = analyzer.analyze(local)
    assert report["fetch_exclusions"] == local["fetch_exclusions"]
    for horizon in report["horizons"]:
        assert horizon["trend"] == "insufficient"
        assert "latest usable close was 2024-02-29" in " ".join(horizon["limitations"])
