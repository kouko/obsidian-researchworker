"""Cutoff and comparison rules shared by quarterly market research."""

from collections.abc import Mapping
from datetime import date, datetime, timezone
from decimal import Decimal
import math
import re


def _parse_time(value):
    """Parse an ISO day or a timezone-qualified instant normalized to UTC."""
    if isinstance(value, str):
        if re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
            return date.fromisoformat(value)
        if re.match(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}", value):
            if value.endswith("Z"):
                value = value[:-1] + "+00:00"
            instant = datetime.fromisoformat(value)
            if instant.utcoffset() is not None:
                return instant.astimezone(timezone.utc)
    raise ValueError("Expected an ISO date or timezone-qualified datetime")


def _was_available(source, cutoff):
    if not isinstance(source, Mapping):
        return False
    try:
        published = _parse_time(source.get("published_at"))
    except (ValueError, OverflowError):
        return False
    if isinstance(cutoff, datetime):
        if isinstance(published, datetime):
            return published <= cutoff
        # A release day does not establish an intraday time on that day.
        return published < cutoff.date()
    if isinstance(published, datetime):
        return published.date() <= cutoff
    return published <= cutoff


def claim_is_eligible(claim, sources, cutoff):
    """Require every material, exact source version to be available at cutoff.

    Date boundaries use UTC. Claim authorship is independent of the publication
    of its economic inputs. Callers must supply all material dependencies.
    """
    boundary = _parse_time(cutoff)
    source_ids = claim.get("source_ids")
    if not isinstance(source_ids, list) or not source_ids:
        return False
    return all(
        isinstance(source_id, str)
        and bool(source_id.strip())
        and _was_available(sources.get(source_id), boundary)
        for source_id in source_ids
    )


def _version(observation):
    version = observation.get("version")
    if isinstance(version, str) and version.strip():
        return version
    raise ValueError("Each forecast and actual must identify its exact version")


def _value(observation):
    value = observation.get("value")
    if type(value) not in (int, float) or (isinstance(value, float) and not math.isfinite(value)):
        raise ValueError("Each forecast and actual must have a finite numeric value")
    return Decimal(str(value))


def compare_forecast(forecast, actual, sources, cutoff):
    """Return a new comparison, leaving the original forecast untouched.

    Scope, metric and unit identify a comparable series. Target periods must
    match exactly, so annual forecast scoring cannot use interim actuals.
    The signed error is actual minus forecast in the original unit.
    """
    forecast_version = _version(forecast)
    pending = {"status": "pending", "forecast_version": forecast_version}
    if not claim_is_eligible(forecast, sources, cutoff):
        return {**pending, "reason": "ineligible-forecast"}
    if actual is None:
        return {**pending, "reason": "missing-actual"}
    if not claim_is_eligible(actual, sources, cutoff):
        return {**pending, "reason": "ineligible-actual"}
    for key in ("scope", "metric", "unit", "target_period"):
        expected = forecast.get(key)
        if not isinstance(expected, str) or not expected.strip() or actual.get(key) != expected:
            return {**pending, "reason": "noncomparable-actual"}
    error = float(_value(actual) - _value(forecast))
    if not math.isfinite(error):
        raise ValueError("Forecast comparison exceeds the representable range")
    return {
        "status": "compared",
        "forecast_version": forecast_version,
        "actual_version": _version(actual),
        "error": error,
    }
