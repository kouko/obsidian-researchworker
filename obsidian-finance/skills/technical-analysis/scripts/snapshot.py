"""Validate a daily stock snapshot and select rows admissible at a cutoff."""

import hashlib
import json
import math
import re
from datetime import date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError


def parse_timestamp(value, field):
    """Require a timestamp with an explicit UTC offset."""
    try:
        timestamp = datetime.fromisoformat(value) if isinstance(value, str) else value
        if not isinstance(timestamp, datetime) or timestamp.utcoffset() is None:
            raise ValueError
        return timestamp
    except (ValueError, OverflowError) as exc:
        raise ValueError(f"{field} must be a timezone-aware ISO timestamp.") from exc


def _text_field(document, field):
    value = document.get(field)
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field} must be a nonempty string.")
    return value.strip()


def _calendar_date(value, field):
    try:
        result = date.fromisoformat(value)
        if result.isoformat() == value:
            return result
    except (TypeError, ValueError):
        pass
    raise ValueError(f"{field} must have the YYYY-MM-DD form.")


def _number(document, field, *, allow_zero=False, allow_missing=False):
    value = document.get(field)
    if value is None and allow_missing:
        return None
    if type(value) not in (int, float):
        raise ValueError(f"{field} must be numeric.")
    try:
        number = float(value)
    except OverflowError as exc:
        raise ValueError(f"{field} must be finite.") from exc
    if not math.isfinite(number) or number < 0 or (number == 0 and not allow_zero):
        raise ValueError(f"{field} must be finite and {'nonnegative' if allow_zero else 'positive'}.")
    return number


def _read_bar(bar, timezone, snapshot_available_at):
    if not isinstance(bar, dict):
        raise ValueError("Each bar must be an object.")
    day_text = _text_field(bar, "date")
    day = _calendar_date(day_text, "Bar date")
    session_close = parse_timestamp(bar.get("session_close"), "session_close")
    if session_close.astimezone(timezone).date() != day:
        raise ValueError(f"{day}: session_close falls outside the trading date in the listing timezone.")
    available_at = parse_timestamp(bar.get("available_at", snapshot_available_at), "bar available_at")
    complete = bar.get("complete", True)
    if type(complete) is not bool:
        raise ValueError(f"{day}: complete must be true or false.")
    normalized = {
        "date": day_text,
        "session_close": session_close.isoformat(),
        "available_at": available_at.isoformat(),
        "complete": complete,
        **{field: _number(bar, field) for field in ("open", "high", "low", "close")},
        "volume": _number(bar, "volume", allow_zero=True, allow_missing=True),
    }
    if not (
        normalized["low"] <= min(normalized["open"], normalized["close"])
        <= max(normalized["open"], normalized["close"]) <= normalized["high"]
    ):
        raise ValueError(f"{day}: open and close must fall between low and high.")
    return normalized, session_close, available_at


def validate_snapshot(payload, cutoff):
    """Return sorted admissible bars and explicit exclusions.

    Source evidence is a supplied capture or publication reference for this exact
    version. The loader checks its presence and temporal consistency. It does
    not independently authenticate an upstream provider or user record.
    """
    if not isinstance(payload, dict):
        raise ValueError("Snapshot must be an object.")
    cutoff = parse_timestamp(cutoff, "cutoff")
    ticker = _text_field(payload, "ticker").upper()
    if not re.fullmatch(r"[A-Z][A-Z0-9.-]{0,14}", ticker):
        raise ValueError("ticker must identify one U.S. equity.")
    timezone_name = _text_field(payload, "timezone")
    try:
        timezone = ZoneInfo(timezone_name)
    except (ZoneInfoNotFoundError, ValueError) as exc:
        raise ValueError("timezone must be a valid IANA zone name.") from exc
    available_at = parse_timestamp(payload.get("available_at"), "snapshot available_at")
    metadata = {
        "ticker": ticker,
        "timezone": timezone_name,
        "source": _text_field(payload, "source"),
        "adjustment": _text_field(payload, "adjustment"),
        "available_at": available_at.isoformat(),
    }
    for field in (
        "exchange", "currency", "source_version", "evidence",
        "session_calendar", "session_calendar_version",
    ):
        if payload.get(field) is not None:
            metadata[field] = _text_field(payload, field)
    if "request_started_at" in payload:
        request_started_at = parse_timestamp(payload["request_started_at"], "request_started_at")
        if request_started_at > available_at:
            raise ValueError("request_started_at must precede snapshot availability.")
        metadata["request_started_at"] = request_started_at.isoformat()
    if "latest_expected_session" in payload:
        latest_expected_session = _text_field(payload, "latest_expected_session")
        _calendar_date(latest_expected_session, "latest_expected_session")
        metadata["latest_expected_session"] = latest_expected_session
    if "missing_completed_sessions" in payload:
        missing = payload["missing_completed_sessions"]
        if not isinstance(missing, list):
            raise ValueError("missing_completed_sessions must be a list of dates.")
        latest = metadata.get("latest_expected_session", available_at.astimezone(timezone).date().isoformat())
        for value in missing:
            day = _calendar_date(value, "missing_completed_sessions date")
            if day.weekday() >= 5 or value > latest:
                raise ValueError("missing_completed_sessions contains a date outside completed U.S. sessions.")
        metadata["missing_completed_sessions"] = sorted(set(missing))
    if "fetch_settings" in payload:
        settings = payload["fetch_settings"]
        if not isinstance(settings, dict) or any(
            not isinstance(key, str) or type(value) not in (str, bool, int)
            for key, value in settings.items()
        ):
            raise ValueError("fetch_settings must be an object of string, integer or Boolean values.")
        metadata["fetch_settings"] = dict(settings)
    if "fetch_exclusions" in payload:
        fetch_exclusions = payload["fetch_exclusions"]
        if not isinstance(fetch_exclusions, list) or any(
            not isinstance(item, str) for item in fetch_exclusions
        ):
            raise ValueError("fetch_exclusions must be a list of strings.")
        metadata["fetch_exclusions"] = list(fetch_exclusions)

    rows = payload.get("bars")
    if not isinstance(rows, list):
        raise ValueError("bars must be a list.")
    bars = {}
    for row in rows:
        bar, session_close, bar_available_at = _read_bar(row, timezone, available_at)
        day = bar["date"]
        if day in bars:
            raise ValueError(f"Duplicate trading date: {day}.")
        bars[day] = (bar, session_close, bar_available_at)
    if bars.keys() & set(metadata.get("missing_completed_sessions", ())):
        raise ValueError("missing_completed_sessions includes a supplied bar.")
    ordered = [bars[day] for day in sorted(bars)]
    identity = json.dumps(
        {**metadata, "bars": [bar for bar, _, _ in ordered]},
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    )
    eligible = []
    exclusions = []
    if "evidence" not in metadata:
        exclusions.append("Snapshot lacks a capture or publication evidence reference.")
    if available_at > cutoff:
        exclusions.append("Snapshot version was available after the analysis cutoff.")
    missing_completed_sessions = set(metadata.get("missing_completed_sessions", ()))
    if not exclusions:
        for bar, session_close, bar_available_at in ordered:
            day = bar["date"]
            is_weekday = _calendar_date(day, "Bar date").weekday() < 5
            if not is_weekday:
                exclusions.append(f"{day}: weekend is not a U.S. equity trading session.")
            elif not bar["complete"] or session_close > cutoff:
                exclusions.append(f"{day}: trading session was incomplete at cutoff.")
            elif bar_available_at > cutoff:
                exclusions.append(f"{day}: bar was available after cutoff.")
            elif bar_available_at < session_close or bar_available_at > available_at:
                exclusions.append(f"{day}: bar availability is inconsistent with session close or snapshot capture.")
            else:
                eligible.append(bar)
                continue
            if is_weekday and session_close <= cutoff:
                missing_completed_sessions.add(day)
        exclusions.extend(metadata.get("fetch_exclusions", ()))
    if missing_completed_sessions:
        metadata["missing_completed_sessions"] = sorted(missing_completed_sessions)
    return {
        **metadata,
        "snapshot_id": hashlib.sha256(identity.encode("utf-8")).hexdigest(),
        "cutoff": cutoff.isoformat(),
        "bars": eligible,
        "exclusions": exclusions,
    }


def load_snapshot(path, cutoff):
    """Load and validate a local JSON daily snapshot."""
    return validate_snapshot(json.loads(Path(path).read_text(encoding="utf-8")), cutoff)
