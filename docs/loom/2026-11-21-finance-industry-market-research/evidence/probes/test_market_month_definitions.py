# concern: Matching scope, metric, and units can conceal inconsistent monthly denominator definitions.
from pathlib import Path
import sys

FINANCE_TESTS = Path(__file__).resolve().parents[5] / "obsidian-finance" / "tests"
sys.path.insert(0, str(FINANCE_TESTS))
from test_market_research import aggregate_quarter


def test_eu_bev_months_with_incompatible_denominators_cannot_form_quarter():
    months = ("2024-07", "2024-08", "2024-09")
    sources = {month: {"published_at": "2024-10-22"} for month in months}
    observations = [
        {
            "month": month, "scope": "European Union", "metric": "BEV share",
            "unit": "ratio", "source_ids": [month], "numerator": 10, "denominator": 100,
            "definition": "BEV share of new passenger car registrations",
        }
        for month in months
    ]

    def aggregate():
        return aggregate_quarter("2024Q3", observations, "2024-10-31", sources=sources, ratio=True)

    assert aggregate()["status"] == "complete"
    observations[-1]["definition"] = "BEV share of new and used passenger car registrations"
    result = aggregate()
    assert result["status"] == "partial"
    assert result["issues"]
