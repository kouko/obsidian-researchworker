import importlib.util
from pathlib import Path

import pytest

SCRIPT = Path(__file__).parents[1] / "scripts/market_evidence.py"
SPEC = importlib.util.spec_from_file_location("market_evidence", SCRIPT)
evidence = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(evidence)

SOURCES = {
    "idc-initial": {"published_at": "2024-10-14"},
    "counterpoint-initial": {"published_at": "2024-10-15"},
    "counterpoint-final": {"published_at": "2024-11-01"},
    "timed-release": {"published_at": "2024-10-14T13:00:00+02:00"},
    "unverified-release": {},
}
CUTOFF = "2024-10-31"


def test_all_material_source_versions_must_be_eligible():
    assert evidence.claim_is_eligible(
        {"source_ids": ["idc-initial", "counterpoint-initial"], "authored_at": "2026-11-21"},
        SOURCES,
        CUTOFF,
    )
    assert not evidence.claim_is_eligible(
        {"source_ids": ["idc-initial", "counterpoint-final"]}, SOURCES, CUTOFF
    )
    assert not evidence.claim_is_eligible({"source_ids": ["idc-initial"]}, SOURCES, "2024-09-28")


@pytest.mark.parametrize("ids", [[], ["missing"], ["unverified-release"], "idc-initial"])
def test_missing_or_unverified_dependencies_cannot_support_citation(ids):
    assert not evidence.claim_is_eligible({"source_ids": ids}, SOURCES, CUTOFF)


def test_date_only_release_cannot_establish_same_day_intraday_availability():
    claim = {"source_ids": ["idc-initial"]}
    assert evidence.claim_is_eligible(claim, SOURCES, "2024-10-14")
    assert not evidence.claim_is_eligible(claim, SOURCES, "2024-10-14T23:59:00Z")
    assert evidence.claim_is_eligible(claim, SOURCES, "2024-10-15T00:00:00Z")


def test_timed_release_uses_actual_instant():
    claim = {"source_ids": ["timed-release"]}
    assert not evidence.claim_is_eligible(claim, SOURCES, "2024-10-14T10:59:59Z")
    assert evidence.claim_is_eligible(claim, SOURCES, "2024-10-14T11:00:00Z")
    with pytest.raises(ValueError):
        evidence.claim_is_eligible(claim, SOURCES, "2024-10-14T11:00:00")


def observation(version, value, source, **overrides):
    return {
        "version": version,
        "value": value,
        "source_ids": [source],
        "scope": "worldwide-smartphones",
        "metric": "shipments",
        "unit": "million devices",
        "target_period": "2024",
        **overrides,
    }


def test_compare_forecast_preserves_original_and_actual_versions():
    forecast = observation("may-forecast", 1250.1, "idc-initial")
    actual = observation("annual-initial", 1283.7, "counterpoint-final")
    original = forecast.copy()
    assert evidence.compare_forecast(forecast, actual, SOURCES, "2024-11-02") == {
        "status": "compared",
        "forecast_version": "may-forecast",
        "actual_version": "annual-initial",
        "error": 33.6,
    }
    assert forecast == original


@pytest.mark.parametrize("overrides", [
    {"scope": "united-states"},
    {"metric": "end-user-sales"},
    {"unit": "devices"},
    {"target_period": "2024-Q3"},
])
def test_noncomparable_actual_remains_pending(overrides):
    forecast = observation("may-forecast", 1250, "idc-initial")
    actual = observation("q3-initial", 300, "counterpoint-initial", **overrides)
    assert evidence.compare_forecast(forecast, actual, SOURCES, CUTOFF) == {
        "status": "pending",
        "forecast_version": "may-forecast",
        "reason": "noncomparable-actual",
    }


def test_absent_or_late_actual_remains_pending():
    forecast = observation("may-forecast", 1250, "idc-initial")
    late = observation("annual-initial", 1280, "counterpoint-final")
    assert evidence.compare_forecast(forecast, None, SOURCES, CUTOFF)["reason"] == "missing-actual"
    assert evidence.compare_forecast(forecast, late, SOURCES, CUTOFF)["reason"] == "ineligible-actual"
