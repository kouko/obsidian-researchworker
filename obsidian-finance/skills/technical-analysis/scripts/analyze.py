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


METHOD = "stock-technical-v2"
HORIZONS = (
    ("short", "3 calendar weeks", 3, 0, 20),
    ("medium", "3 calendar months", 0, 3, 50),
    ("long", "1 calendar year", 0, 12, 200),
)
VOLUME_BASELINE = 20
SLOPE_SESSIONS = 5
SWING_RADIUS = 2
PATTERN_LEVEL_TOLERANCE = 0.03
PATTERN_MIN_HEIGHT = 0.05
PATTERN_BREAK_BUFFER = 0.005
PATTERN_MIN_SESSIONS = 9


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


def _crosses_missing_session(bars, missing_sessions):
    return bool(bars) and any(bars[0]["date"] <= day <= bars[-1]["date"]
                              for day in missing_sessions)


def _daily_indicators(bars, missing_sessions):
    averages = {}
    previous = {}
    ranges = {}
    for period in (20, 50, 200):
        window = bars[-period:]
        current_valid = len(window) == period and not _crosses_missing_session(window, missing_sessions)
        averages[str(period)] = mean(bar["close"] for bar in window) if current_valid else None
        ranges[f"sma_{period}"] = _range(window) if current_valid else [None, None]
        earlier = bars[:-SLOPE_SESSIONS][-period:]
        slope_window = bars[-period - SLOPE_SESSIONS:]
        previous_valid = len(earlier) == period and not _crosses_missing_session(slope_window, missing_sessions)
        previous[str(period)] = mean(bar["close"] for bar in earlier) if previous_valid else None
        ranges[f"sma_{period}_previous"] = _range(earlier) if previous_valid else [None, None]

    baseline = bars[-VOLUME_BASELINE - 1:-1]
    volumes = [bar["volume"] for bar in baseline]
    latest_volume = bars[-1]["volume"] if bars else None
    enough_volume = (
        len(volumes) == VOLUME_BASELINE and None not in volumes
        and not _crosses_missing_session(bars[-VOLUME_BASELINE - 1:], missing_sessions)
    )
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


def _swings(bars, missing_sessions):
    points = []
    for index in range(SWING_RADIUS, len(bars) - SWING_RADIUS):
        window = bars[index - SWING_RADIUS:index + SWING_RADIUS + 1]
        if _crosses_missing_session(window, missing_sessions):
            continue
        center = window[SWING_RADIUS]
        neighbors = window[:SWING_RADIUS] + window[SWING_RADIUS + 1:]
        for field, significant in (("high", max), ("low", min)):
            edge = significant(bar[field] for bar in neighbors)
            if center[field] != edge and significant(center[field], edge) == center[field]:
                points.append({
                    "kind": field, "date": center.get(f"{field}_date", center["date"]),
                    "price": center[field], "confirmed_on": window[-1]["date"],
                })
    return points


def _pattern_candidates(points, *, min_reversal=0):
    """Yield formations as each confirmed pivot becomes available."""
    alternating = []
    for _, same_day in groupby(points, key=lambda point: point["date"]):
        anchors = list(same_day)
        if len(anchors) != 1:
            # An outside bar does not tell us which extreme happened first.
            continue
        point = anchors[0]
        if not alternating:
            alternating.append(point)
            continue
        prior = alternating[-1]
        if prior["kind"] == point["kind"]:
            if (point["price"] < prior["price"] if point["kind"] == "high" else point["price"] > prior["price"]):
                continue
            alternating[-1] = point
        elif abs(point["price"] - prior["price"]) >= min_reversal * mean((point["price"], prior["price"])):
            alternating.append(point)
        else:
            continue
        for size in (3, 4, 5):
            if len(alternating) >= size:
                yield alternating[-size:]


def _pattern_geometry(anchors, indices):
    prices = [anchor["price"] for anchor in anchors]
    level_band = mean(prices) * PATTERN_LEVEL_TOLERANCE
    min_height = mean(prices) * PATTERN_MIN_HEIGHT
    highs = [anchor for anchor in anchors if anchor["kind"] == "high"]
    lows = [anchor for anchor in anchors if anchor["kind"] == "low"]

    def line(points, *, flat=False):
        start = points[0]
        origin = indices[start["date"]]
        if flat:
            extreme = max if start["kind"] == "high" else min
            return extreme(point["price"] for point in points), origin, 0.0
        if len(points) == 1:
            return start["price"], origin, 0.0
        last = points[-1]
        slope = (last["price"] - start["price"]) / (indices[last["date"]] - origin)
        return start["price"], origin, slope

    if len(anchors) in (3, 5):
        top = anchors[0]["kind"] == "high"
        if min(point["price"] for point in highs) - max(point["price"] for point in lows) < min_height:
            return None
        if abs(prices[0] - prices[-1]) > level_band:
            return None
        if len(anchors) == 3:
            kind = "double_top" if top else "double_bottom"
        else:
            head_height = prices[2] - max(prices[0], prices[-1]) if top else min(prices[0], prices[-1]) - prices[2]
            if head_height < level_band:
                return None
            kind = "head_and_shoulders_top" if top else "head_and_shoulders_bottom"
        upper = line([max(highs, key=lambda point: point["price"])]) if top else line(highs)
        lower = line(lows) if top else line([min(lows, key=lambda point: point["price"])])
        return kind, ("down" if top else "up",), upper, lower

    upper_change = highs[-1]["price"] - highs[0]["price"]
    lower_change = lows[-1]["price"] - lows[0]["price"]
    flat_upper = abs(upper_change) <= level_band
    flat_lower = abs(lower_change) <= level_band
    if flat_upper and flat_lower:
        kind, directions = "rectangle", ("up", "down")
    elif flat_upper and lower_change > level_band:
        kind, directions = "ascending_triangle", ("up",)
    elif upper_change < -level_band and flat_lower:
        kind, directions = "descending_triangle", ("down",)
    elif upper_change < -level_band and lower_change > level_band:
        kind, directions = "symmetrical_triangle", ("up", "down")
    else:
        return None
    upper = line(highs, flat=flat_upper)
    lower = line(lows, flat=flat_lower)
    first_pair = max(upper[1], lower[1])
    if _line_at(upper, first_pair) - _line_at(lower, first_pair) < min_height:
        return None
    return kind, directions, upper, lower


def _line_at(line, index):
    level, origin, slope = line
    return level + (index - origin) * slope


def _pattern_match(geometry, anchors, bars, indices):
    kind, directions, upper_line, lower_line = geometry
    known_on = anchors[-1]["confirmed_on"]
    first_index = indices[known_on]
    triangle = kind.endswith("_triangle")
    upper = _line_at(upper_line, first_index)
    lower = _line_at(lower_line, first_index)
    if upper <= lower:
        # By the time the pivots were knowable the shape was already closed.
        return None
    confirmation = invalidation = None
    for index in range(first_index, len(bars)):
        bar = bars[index]
        upper = _line_at(upper_line, index)
        lower = _line_at(lower_line, index)
        close = bar["close"]
        upper_trigger = upper * (1 + PATTERN_BREAK_BUFFER)
        lower_trigger = lower * (1 - PATTERN_BREAK_BUFFER)
        event = {"date": bar["date"], "close": close, "volume": bar["volume"]}
        if confirmation:
            up = confirmation["direction"] == "up"
            if (close < upper if up else close > lower):
                invalidation = {**event, "level": upper if up else lower, "reason": "close back across the break boundary"}
                break
        elif triangle and upper <= lower:
            invalidation = {**event, "level": None, "reason": "triangle boundaries converged without a qualifying close"}
            break
        elif close > upper_trigger or close < lower_trigger:
            up = close > upper_trigger
            direction = "up" if up else "down"
            event.update(direction=direction, level=upper_trigger if up else lower_trigger)
            if direction not in directions:
                invalidation = {**event, "reason": "close beyond the opposite boundary"}
                break
            confirmation = event
    boundary_date = (invalidation or confirmation or bars[-1])["date"]
    boundary_index = indices[boundary_date]
    break_buffer = f"{PATTERN_BREAK_BUFFER:.1%}"
    triggers = {"up": f"{break_buffer} above the upper boundary",
                "down": f"{break_buffer} below the lower boundary"}
    confirmation_condition = "Daily close more than " + " or ".join(triggers[item] for item in directions) + "."
    invalidation_condition = "After confirmation, a daily close back across the break boundary."
    if len(directions) == 1:
        opposite = "down" if directions[0] == "up" else "up"
        invalidation_condition += f" Before confirmation, a daily close more than {triggers[opposite]}."
    if triangle:
        invalidation_condition += " A triangle also expires if its boundaries meet before confirmation."
    return {
        "kind": kind,
        "state": "invalidated" if invalidation else "confirmed" if confirmation else "candidate",
        "anchors": anchors, "known_on": known_on,
        "confirmation": confirmation, "invalidation": invalidation,
        "confirmation_condition": confirmation_condition, "invalidation_condition": invalidation_condition,
        "boundaries": {
            "date": boundary_date, "upper": _line_at(upper_line, boundary_index), "lower": _line_at(lower_line, boundary_index),
            "upper_per_session": upper_line[2], "lower_per_session": lower_line[2],
        },
    }


def _daily_patterns(bars, points, coverage_gap):
    if coverage_gap or len(bars) < PATTERN_MIN_SESSIONS:
        reason = coverage_gap or f"Requires at least {PATTERN_MIN_SESSIONS} completed daily sessions."
        return {"status": "insufficient", "reason": reason, "matches": []}
    indices = {bar["date"]: index for index, bar in enumerate(bars)}
    latest = {}
    # A second pass can bridge shallow counter-swings. Keep the raw pivots
    # available so that a close pair of late triangle touches can still qualify.
    for reversal in (0, PATTERN_LEVEL_TOLERANCE):
        for anchors in _pattern_candidates(points, min_reversal=reversal):
            geometry = _pattern_geometry(anchors, indices)
            if geometry is None:
                continue
            match = _pattern_match(geometry, anchors, bars, indices)
            if match is None:
                continue
            prior = latest.get(match["kind"])
            if prior is None or match["known_on"] >= prior["known_on"]:
                latest[match["kind"]] = match
    return {"status": "evaluated" if latest else "no_match", "matches": list(latest.values())}


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


def _horizon(bars, cutoff_day, settings, indicators, stale_gap, missing_sessions):
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
    points = _swings(structure, missing_sessions)
    period_return = None
    if len(observed) >= 2:
        period_return = (observed[-1]["close"] / observed[0]["close"] - 1) * 100
        evidence.append(f"Observed close-to-close return {period_return:+.2f}% from {observed_start} to {observed_end}.")
    average = averages[str(average_period)]
    prior_average = previous[str(average_period)]
    if average is not None:
        evidence.append(f"{average_period}-session moving average {average:.6g} as of {bars[-1]['date']}.")
    else:
        limitations.append(f"The {average_period}-session moving average requires a complete input window.")
    if volume_ratio is None:
        limitations.append("Relative volume requires a valid latest volume and a complete, positive 20-session prior average.")
    else:
        evidence.append(f"Latest volume is {volume_ratio:.2f}× the prior {VOLUME_BASELINE}-session average.")
    missing_in_window = [day for day in missing_sessions if start.isoformat() <= day <= cutoff_day.isoformat()]
    known_gap = None
    if missing_in_window:
        known_gap = "Coverage gap: missing completed sessions in this observation window: " + ", ".join(missing_in_window)
    coverage_gap = stale_gap or known_gap or _coverage_gap(observed, start, cutoff_day)
    if coverage_gap is None:
        trend, explanation = _trend(points, observed[-1]["close"], average, prior_average)
        (limitations if trend == "insufficient" else evidence).append(explanation)
    else:
        trend = "insufficient"
        explanation = coverage_gap
        limitations.append(explanation)
    trigger, invalidation, alternative = _conditions(trend, support, resistance)
    daily_points = points if frequency == "daily" else _swings(observed, missing_sessions)
    return {
        "name": name, "length": length, "observed_start": observed_start,
        "observed_end": observed_end, "outlook_start": (cutoff_day + timedelta(days=1)).isoformat(),
        "outlook_end": end.isoformat(), "trend": trend, "conclusion": explanation,
        "metrics": {"return_pct": period_return, "sma": averages, "volume_ratio": volume_ratio},
        "metric_ranges": {**metric_ranges, "return": [observed_start, observed_end]},
        "levels": {"support": support, "resistance": resistance}, "swings": points,
        "structure_frequency": frequency, "evidence": evidence, "limitations": limitations,
        "trigger": trigger, "invalidation": invalidation, "alternative": alternative,
        "patterns": _daily_patterns(observed, daily_points, coverage_gap),
    }


def analyze(snapshot):
    """Return analysis for an already validated snapshot, without network or writes."""
    cutoff = _time(snapshot["cutoff"])
    cutoff_day = cutoff.astimezone(ZoneInfo(snapshot["timezone"])).date()
    bars = [bar for bar in snapshot["bars"] if _time(bar["session_close"]) <= cutoff]
    missing_sessions = set(snapshot.get("missing_completed_sessions", ()))
    legacy_suffix = ": completed exchange session missing from provider data."
    missing_sessions.update(
        item.removesuffix(legacy_suffix) for item in snapshot.get("fetch_exclusions", ())
        if item.endswith(legacy_suffix)
    )
    missing_sessions = sorted(missing_sessions)
    indicators = _daily_indicators(bars, missing_sessions)
    expected = snapshot.get("latest_expected_session")
    stale_gap = None
    if bars and expected and bars[-1]["date"] < expected <= cutoff_day.isoformat():
        stale_gap = (f"Coverage gap: completed session {expected} is missing. "
                     f"The latest usable close was {bars[-1]['date']}.")
    return {
        **snapshot, "bars": bars, "schema_version": 1, "method": METHOD,
        "settings": {"slope_sessions": SLOPE_SESSIONS, "swing_radius": SWING_RADIUS,
                     "volume_baseline": VOLUME_BASELINE,
                     "pattern_level_tolerance": PATTERN_LEVEL_TOLERANCE,
                     "pattern_min_height": PATTERN_MIN_HEIGHT,
                     "pattern_break_buffer": PATTERN_BREAK_BUFFER,
                     "pattern_min_sessions": PATTERN_MIN_SESSIONS},
        "horizons": [
            _horizon(bars, cutoff_day, settings, indicators, stale_gap, missing_sessions)
            for settings in HORIZONS
        ],
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
