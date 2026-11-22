#!/usr/bin/env python3
"""Deterministic technical analysis of a validated, completed-session snapshot."""

import argparse
from calendar import monthrange
from datetime import date, datetime, timedelta
from itertools import groupby, pairwise
import json
from pathlib import Path
from statistics import mean
import sys
from zoneinfo import ZoneInfo


METHOD = "stock-technical-v1"
HORIZONS = (
    ("short", "3 calendar weeks", 3, 0, 20),
    ("medium", "3 calendar months", 0, 3, 50),
    ("long", "1 calendar year", 0, 12, 200),
)
VOLUME_BASELINE = 20
SLOPE_SESSIONS = 5
SWING_RADIUS = 2


def _time(value):
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def _offset_day(day, weeks, months):
    if not months:
        return day + timedelta(weeks=weeks)
    year, month_index = divmod(day.year * 12 + day.month - 1 + months, 12)
    month = month_index + 1
    return date(year, month, min(day.day, monthrange(year, month)[1]))


def _range(bars):
    return [bars[0]["date"], bars[-1]["date"]] if bars else [None, None]


def _daily_indicators(bars):
    averages = {}
    previous = {}
    ranges = {}
    for period in (20, 50, 200):
        window = bars[-period:]
        averages[str(period)] = mean(bar["close"] for bar in window) if len(window) == period else None
        ranges[f"sma_{period}"] = _range(window) if len(window) == period else [None, None]
        earlier = bars[:-SLOPE_SESSIONS][-period:]
        previous[str(period)] = mean(bar["close"] for bar in earlier) if len(earlier) == period else None
        ranges[f"sma_{period}_previous"] = _range(earlier) if len(earlier) == period else [None, None]

    baseline = bars[-VOLUME_BASELINE - 1:-1]
    volumes = [bar["volume"] for bar in baseline]
    latest_volume = bars[-1]["volume"] if bars else None
    enough_volume = len(volumes) == VOLUME_BASELINE and None not in volumes
    baseline_average = mean(volumes) if enough_volume else None
    ratio = latest_volume / baseline_average if latest_volume is not None and baseline_average else None
    ranges["volume_baseline"] = _range(baseline) if enough_volume else [None, None]
    return averages, previous, ratio, ranges


def _full_weeks(bars):
    """Aggregate unambiguous full Mon–Fri weeks, or leave structure on daily bars."""
    weeks = []
    for _, group in groupby(bars, key=lambda bar: date.fromisoformat(bar["date"]).isocalendar()[:2]):
        week = list(group)
        weekdays = [date.fromisoformat(bar["date"]).weekday() for bar in week]
        if weekdays != list(range(5)):
            continue
        high = max(week, key=lambda bar: bar["high"])
        low = min(week, key=lambda bar: bar["low"])
        weeks.append({
            "date": week[-1]["date"], "high": high["high"], "low": low["low"],
            "high_date": high["date"], "low_date": low["date"],
        })
    if any(date.fromisoformat(b["date"]) - date.fromisoformat(a["date"]) != timedelta(weeks=1)
           for a, b in pairwise(weeks)):
        return []
    return weeks


def _swings(bars):
    points = []
    for index in range(SWING_RADIUS, len(bars) - SWING_RADIUS):
        center = bars[index]
        right = bars[index + 1:index + SWING_RADIUS + 1]
        neighbors = bars[index - SWING_RADIUS:index] + right
        for field, significant in (("high", max), ("low", min)):
            edge = significant(bar[field] for bar in neighbors)
            if center[field] != edge and significant(center[field], edge) == center[field]:
                points.append({
                    "kind": field, "date": center.get(f"{field}_date", center["date"]),
                    "price": center[field], "confirmed_on": right[-1]["date"],
                })
    return points


def _level(bars, field, extreme):
    if not bars:
        return None
    bar = extreme(bars, key=lambda item: item[field])
    return {"price": bar[field], "date": bar["date"]}


def _coverage_gap(bars, start, end):
    if not bars:
        return "No eligible completed sessions in this observation window."
    first, last = map(date.fromisoformat, _range(bars))
    span = (end - start).days + 1
    weekday_count = sum((start + timedelta(days=i)).weekday() < 5 for i in range(span))
    large_gap = any((date.fromisoformat(b["date"]) - date.fromisoformat(a["date"])).days > 7
                    for a, b in pairwise(bars))
    if (end - last).days > 5:
        return f"Coverage gap: the latest usable close was {last}, more than five days before cutoff."
    if (first - start).days > 5 or len(bars) * 5 < weekday_count * 4 or large_gap:
        return "Coverage gap: the snapshot does not adequately cover this observation window."
    return None


def _trend(points, close, average, previous):
    highs = [point["price"] for point in points if point["kind"] == "high"]
    lows = [point["price"] for point in points if point["kind"] == "low"]
    if len(highs) >= 2 and len(lows) >= 2:
        if highs[-1] > highs[-2] and lows[-1] > lows[-2]:
            return "up", "Two confirmed swing highs and lows are rising."
        if highs[-1] < highs[-2] and lows[-1] < lows[-2]:
            return "down", "Two confirmed swing highs and lows are falling."
        return "sideways", "Confirmed swing highs and lows do not agree on direction."
    if average is None or previous is None:
        return "insufficient", "Not enough confirmed swings or moving-average history for direction."
    if close > average > previous:
        return "up", "The close is above a rising moving average."
    if close < average < previous:
        return "down", "The close is below a falling moving average."
    return "sideways", "The close and moving-average slope do not agree on direction."


def _conditions(trend, support, resistance):
    if trend == "insufficient" or support is None or resistance is None:
        return None, None, None
    upper = f"a daily close above {resistance['price']:.6g} (high on {resistance['date']})"
    lower = f"a daily close below {support['price']:.6g} (low on {support['date']})"
    if trend == "up":
        return (f"Watch for {upper}.", f"Reassess the upward outlook after {lower}.",
                f"After {lower}, consider a deeper pullback and check for lower highs.")
    if trend == "down":
        return (f"Watch for {lower}.", f"Reassess the downward outlook after {upper}.",
                f"After {upper}, consider a recovery and check for higher lows.")
    return (f"Watch for {upper} or {lower}.",
            "Reassess the sideways outlook after either boundary is crossed.",
            "A close outside the range would shift attention to a directional move on that side.")


def _horizon(bars, cutoff_day, settings, indicators, stale_gap):
    name, length, weeks, months, average_period = settings
    averages, previous, volume_ratio, metric_ranges = indicators
    start = _offset_day(cutoff_day, -weeks, -months)
    end = _offset_day(cutoff_day, weeks, months)
    observed = [bar for bar in bars if bar["date"] >= start.isoformat()]
    observed_start, observed_end = _range(observed)
    support = _level(observed, "low", min)
    resistance = _level(observed, "high", max)
    limitations = []
    evidence = []
    frequency = "daily"
    structure = observed
    if name == "long":
        complete_weeks = _full_weeks(observed)
        if len(complete_weeks) >= SWING_RADIUS * 2 + 1:
            structure = complete_weeks
            frequency = "weekly"
        elif observed:
            limitations.append("Complete consecutive exchange weeks are unverified, so structure uses daily bars.")
    points = _swings(structure)
    period_return = None
    if len(observed) >= 2:
        period_return = (observed[-1]["close"] / observed[0]["close"] - 1) * 100
        evidence.append(f"Observed close-to-close return {period_return:+.2f}% from {observed_start} to {observed_end}.")
    average = averages[str(average_period)]
    prior_average = previous[str(average_period)]
    if average is not None:
        evidence.append(f"{average_period}-session moving average {average:.6g} as of {bars[-1]['date']}.")
    else:
        limitations.append(f"Fewer than {average_period} daily closes for this horizon's moving average.")
    if volume_ratio is None:
        limitations.append("Relative volume requires a valid latest volume and a positive 20-session prior average.")
    else:
        evidence.append(f"Latest volume is {volume_ratio:.2f}× the prior {VOLUME_BASELINE}-session average.")
    coverage_gap = stale_gap or _coverage_gap(observed, start, cutoff_day)
    if coverage_gap is None:
        trend, explanation = _trend(points, observed[-1]["close"], average, prior_average)
        (limitations if trend == "insufficient" else evidence).append(explanation)
    else:
        trend = "insufficient"
        explanation = coverage_gap
        limitations.append(explanation)
    trigger, invalidation, alternative = _conditions(trend, support, resistance)
    return {
        "name": name, "length": length, "observed_start": observed_start,
        "observed_end": observed_end, "outlook_start": (cutoff_day + timedelta(days=1)).isoformat(),
        "outlook_end": end.isoformat(), "trend": trend, "conclusion": explanation,
        "metrics": {"return_pct": period_return, "sma": averages, "volume_ratio": volume_ratio},
        "metric_ranges": {**metric_ranges, "return": [observed_start, observed_end]},
        "levels": {"support": support, "resistance": resistance}, "swings": points,
        "structure_frequency": frequency, "evidence": evidence, "limitations": limitations,
        "trigger": trigger, "invalidation": invalidation, "alternative": alternative,
    }


def analyze(snapshot):
    """Return analysis for an already validated snapshot, without network or writes."""
    cutoff = _time(snapshot["cutoff"])
    cutoff_day = cutoff.astimezone(ZoneInfo(snapshot["timezone"])).date()
    bars = [bar for bar in snapshot["bars"] if _time(bar["session_close"]) <= cutoff]
    indicators = _daily_indicators(bars)
    expected = snapshot.get("latest_expected_session")
    stale_gap = None
    if bars and expected and bars[-1]["date"] < expected <= cutoff_day.isoformat():
        stale_gap = (f"Coverage gap: completed session {expected} is missing. "
                     f"The latest usable close was {bars[-1]['date']}.")
    return {
        **snapshot, "bars": bars, "schema_version": 1, "method": METHOD,
        "settings": {"slope_sessions": SLOPE_SESSIONS, "swing_radius": SWING_RADIUS,
                     "volume_baseline": VOLUME_BASELINE},
        "horizons": [_horizon(bars, cutoff_day, settings, indicators, stale_gap) for settings in HORIZONS],
    }


def main(argv=None):
    from snapshot import load_snapshot

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("snapshot", type=Path)
    parser.add_argument("--cutoff", required=True, help="Timezone-aware ISO-8601 analysis cutoff")
    args = parser.parse_args(argv)
    try:
        result = analyze(load_snapshot(args.snapshot, args.cutoff))
        print(json.dumps(result, allow_nan=False, ensure_ascii=False))
    except (OSError, ValueError, OverflowError) as exc:
        print(exc, file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
