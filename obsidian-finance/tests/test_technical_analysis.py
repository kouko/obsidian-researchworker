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


def test_a_known_missing_latest_session_withholds_direction_promptly(analyzer):
    local = {
        **snapshot(stop="2024-02-28"),
        "cutoff": "2024-02-29T23:00:00Z",
        "latest_expected_session": "2024-02-29",
    }
    report = analyzer.analyze(local)
    for horizon in report["horizons"]:
        assert horizon["trend"] == "insufficient"
        assert "completed session 2024-02-29" in " ".join(horizon["limitations"])


def test_known_gap_keeps_recent_inputs_usable(analyzer):
    local = snapshot(start="2023-01-01")
    missing = "2024-01-12"
    local["bars"] = [bar for bar in local["bars"] if bar["date"] != missing]
    local["missing_completed_sessions"] = [missing]
    short, medium, long = analyzer.analyze(local)["horizons"]
    assert short["trend"] == "up"
    assert medium["trend"] == long["trend"] == "insufficient"
    assert set(short["metrics"]["sma"]) == {"20", "50", "200"}
    assert short["metrics"]["sma"]["20"] is not None
    assert short["metrics"]["sma"]["50"] is None
    assert short["metrics"]["volume_ratio"] == 2.0
    assert any(missing in message for message in medium["limitations"])


def test_known_gap_does_not_confirm_a_swing(analyzer):
    local = snapshot()
    candidate = next(bar for bar in local["bars"] if bar["date"] == "2024-02-19")
    candidate["high"] += 10
    assert any(point["date"] == candidate["date"] for point in analyzer.analyze(local)["horizons"][0]["swings"])
    missing = "2024-02-20"
    local["bars"] = [bar for bar in local["bars"] if bar["date"] != missing]
    local["missing_completed_sessions"] = [missing]
    short = analyzer.analyze(local)["horizons"][0]
    assert all(point["date"] != candidate["date"] for point in short["swings"])


PATTERN_CASES = [
    ("double_top", [110, 90, 111], "down"),
    ("double_bottom", [90, 110, 89], "up"),
    ("head_and_shoulders_top", [110, 92, 118, 91, 111], "down"),
    ("head_and_shoulders_bottom", [90, 108, 82, 109, 89], "up"),
    ("rectangle", [110, 90, 111, 91], "up"),
    ("rectangle", [110, 90, 111, 91], "down"),
    ("ascending_triangle", [110, 91, 111, 95], "up"),
    ("descending_triangle", [113, 90, 108, 91], "down"),
    ("symmetrical_triangle", [115, 87, 110, 92], "up"),
]


def pattern_snapshot(anchors):
    local = snapshot(start="2023-01-01", stop="2024-03-01")
    prices = [100.0] * 2
    for anchor in anchors:
        prices.extend((anchor, 100.0))
    prices.extend((100.0, 100.0))
    for bar, price in zip(local["bars"], [100.0] * (len(local["bars"]) - len(prices)) + prices):
        set_price(bar, price)
    return local, local["bars"][-len(prices):][2:-2:2]


def set_price(bar, price):
    bar.update(open=price, high=price + 0.1, low=price - 0.1, close=price)


def pattern_match(horizon, kind):
    return next(item for item in horizon["patterns"]["matches"] if item["kind"] == kind)


@pytest.mark.parametrize("kind,prices,direction", PATTERN_CASES)
def test_daily_chart_pattern_lifecycle_in_every_horizon(analyzer, monkeypatch, kind, prices, direction):
    monkeypatch.syspath_prepend(str(Path(analyzer.__file__).parent))
    from report import render_report

    local, anchors = pattern_snapshot(prices)
    latest = local["bars"][-1]
    latest["volume"] = 123456789.125
    known_on = local["bars"][-2]["date"]
    breakout = 130 if direction == "up" else 70
    for state in ("candidate", "confirmed", "invalidated"):
        if state == "confirmed":
            set_price(latest, breakout)
        if state == "invalidated":
            follow_up = snapshot(start="2024-03-04", stop="2024-03-04")["bars"][0]
            set_price(follow_up, 100)
            local["bars"].append(follow_up)
            local["cutoff"] = "2024-03-04T23:00:00Z"
        report = analyzer.analyze(local)
        assert report["horizons"][-1]["structure_frequency"] == "weekly"
        for horizon in report["horizons"]:
            match = pattern_match(horizon, kind)
            assert match["state"] == state
            assert [anchor["date"] for anchor in match["anchors"]] == [bar["date"] for bar in anchors]
            assert match["known_on"] == known_on
            assert match["confirmation_condition"] and match["invalidation_condition"]
            if state != "candidate":
                assert match["confirmation"]["date"] == latest["date"]
                assert match["confirmation"]["close"] == breakout
                assert match["confirmation"]["direction"] == direction
                if direction == "up" and kind in ("rectangle", "ascending_triangle"):
                    highest = max(bar["high"] for bar in anchors[::2])
                    assert match["confirmation"]["level"] == pytest.approx(highest * 1.005)
                if direction == "down" and kind in ("rectangle", "descending_triangle"):
                    lowest = min(bar["low"] for bar in anchors[1::2])
                    assert match["confirmation"]["level"] == pytest.approx(lowest * 0.995)
            if state == "invalidated":
                assert match["invalidation"]["date"] == follow_up["date"]
        rendered = render_report(report)
        assert rendered.count(f"{kind.replace('_', ' ').capitalize()} — {state}") == 3
        both_directions = kind in ("rectangle", "symmetrical_triangle") and state == "candidate"
        condition = match["invalidation_condition"]
        assert ("close below the upper boundary" in condition) == (direction == "up" or both_directions)
        assert ("close above the lower boundary" in condition) == (direction == "down" or both_directions)
        for anchor in match["anchors"]:
            assert f"{anchor['kind']} {anchor['price']:g} on {anchor['date']} (known on {anchor['confirmed_on']})" in rendered
        if state != "candidate":
            assert f"Confirmation ({direction}) on {latest['date']}: close {breakout}" in rendered
            assert "volume 123456789.125" in rendered


def test_pattern_cutoff_gap_and_no_match_remain_distinct(analyzer):
    local, _ = pattern_snapshot([110, 90, 111])
    early, known, latest = local["bars"][-3:]
    set_price(early, 80)
    set_price(latest, 70)
    def short(data):
        return analyzer.analyze(data)["horizons"][0]

    before_known = short({**local, "cutoff": f"{early['date']}T23:00:00Z"})
    assert before_known["patterns"]["status"] == "no_match"
    as_known = short({**local, "cutoff": f"{known['date']}T23:00:00Z"})
    assert pattern_match(as_known, "double_top")["state"] == "candidate"
    assert pattern_match(short(local), "double_top")["confirmation"]["date"] == latest["date"]
    follow_up = snapshot(start="2024-03-04", stop="2024-03-04")["bars"][0]
    set_price(follow_up, 70)
    with_gap = short({**local, "bars": local["bars"][:-1] + [follow_up],
                      "cutoff": "2024-03-04T23:00:00Z", "missing_completed_sessions": [latest["date"]]})
    assert with_gap["patterns"]["status"] == "insufficient"
    assert with_gap["patterns"]["matches"] == []
    assert short(snapshot(start="2024-02-26"))["patterns"]["status"] == "insufficient"
    assert short(snapshot())["patterns"]["status"] == "no_match"

    overlap, _ = pattern_snapshot([110, 90, 111, 91])
    assert pattern_match(short(overlap), "rectangle")
    assert pattern_match(short(overlap), "double_top")

    scaled = {
        **local, "bars": [
            {**bar, **{field: bar[field] / 100 for field in ("open", "high", "low", "close")}, "volume": None}
            for bar in local["bars"]
        ],
    }
    event = pattern_match(short(scaled), "double_top")["confirmation"]
    assert event["date"] == latest["date"]
    assert event["close"] == 0.7 and event["volume"] is None


@pytest.mark.parametrize("kind,prices,anchor_offsets", [
    ("rectangle", {2: 110, 6: 108, 10: 109, 14: 90, 18: 111, 22: 91}, [2, 14, 18, 22]),
    ("ascending_triangle", {2: 110, 10: 88, 18: 111, 34: 106}, [2, 10, 18, 34]),
])
def test_pattern_keeps_meaningful_anchors_through_noise_and_convergence(analyzer, kind, prices, anchor_offsets):
    local, _ = pattern_snapshot([])
    bars = local["bars"][-38:]
    for index, bar in enumerate(bars):
        set_price(bar, prices.get(index, 108.5 if kind == "ascending_triangle" else 100))
    # Put the three bars around the small counter-swing near its price so it
    # becomes a real pair of local turns inside the much larger box.
    if kind == "rectangle":
        for index in (3, 4, 5, 7, 8, 9, 11, 12):
            set_price(bars[index], 108.5)
    medium = analyzer.analyze(local)["horizons"][1]
    match = pattern_match(medium, kind)
    assert [anchor["date"] for anchor in match["anchors"]] == [bars[index]["date"] for index in anchor_offsets]
    assert match["state"] == "candidate"
