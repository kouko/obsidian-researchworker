"""Check revenue comparability and the quarterly disclosure source gate."""

import importlib.util
from pathlib import Path

import pytest


@pytest.fixture
def workflow():
    root = Path(__file__).resolve().parents[5]
    path = root / "obsidian-finance/skills/tw-equity-research/scripts/workflow.py"
    spec = importlib.util.spec_from_file_location("tw_equity_workflow", path)
    workflow = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(workflow)
    return workflow


@pytest.fixture
def acquired():
    return {
        "issuer": "twse-1611",
        "quarter": "2025Q3",
        "mode": "historical",
        "monthly_revenue": [
            {
                "month": month,
                "status": "available",
                "scope": scope,
                "amount_ntd_thousands": amount,
                "url": f"https://example.com/{month}",
            }
            for month, scope, amount in (
                ("2025-07", "consolidated", 350),
                ("2025-08", "consolidated", 400),
                ("2025-09", "consolidated", 420),
            )
        ],
        "quarterly_filing": {"status": "available", "url": "https://example.com/filing"},
        "material_disclosures": {"status": "none_found", "entries": []},
    }


@pytest.mark.parametrize("different_scope", ["individual", "parent-only"])
def test_mixed_revenue_scopes_do_not_create_a_quarterly_difference(
    workflow, acquired, different_scope,
):
    acquired["monthly_revenue"][1]["scope"] = different_scope
    result = workflow.assess(acquired, filed_ntd_thousands=1180)

    assert result["revenue"]["monthly_total_ntd_thousands"] is None
    assert result["revenue"]["filed_minus_monthly_ntd_thousands"] is None
