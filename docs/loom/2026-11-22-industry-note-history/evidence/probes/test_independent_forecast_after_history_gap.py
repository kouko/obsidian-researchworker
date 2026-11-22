# concern: Unreadable prior notes block forecasts independently sourced for the next quarter.
from pathlib import Path
import sys

FINANCE_TESTS = Path(__file__).resolve().parents[5] / "obsidian-finance" / "tests"
sys.path.insert(0, str(FINANCE_TESTS))
from test_market_research import publish, record, resume


def test_new_forecast_can_be_saved_after_prior_history_gap(tmp_path):
    (tmp_path / ".obsidian").mkdir()
    prior = publish(tmp_path, dict(record(), market_name="Phones"))
    prior.write_text(prior.read_text().replace("industry-research-data", "damaged-history"))
    recovered = resume(tmp_path, "phones", "2024Q3")
    assert recovered["record"] is None
    assert recovered["issues"]

    current = record(quarter="2024Q4", cutoff="2024-12-15")
    current["sources"]["fresh-forecast"] = {
        "url": "https://example.org/december-forecast",
        "published_at": "2024-12-15",
        "observation_period": "2025Q1",
        "locator": "Forecast table",
    }
    current["forecasts"] = [{
        "version": "fresh-forecast",
        "scope": "global",
        "metric": "shipments",
        "unit": "million",
        "target_period": "2025Q1",
        "value": 123,
        "source_ids": ["fresh-forecast"],
    }]
    current["comparisons"] = [{
        "forecast_version": "fresh-forecast",
        "status": "pending",
        "reason": "missing-actual",
    }]
    publish(tmp_path, current)
    assert resume(tmp_path, "phones", "2024Q4")["record"]["forecasts"] == current["forecasts"]
