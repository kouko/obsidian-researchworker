import importlib.util
import json
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[2]
PACKAGE = ROOT / "obsidian-finance"
SKILL = PACKAGE / "skills/tw-equity-research"
SCRIPT = SKILL / "scripts/workflow.py"


@pytest.fixture
def workflow():
    spec = importlib.util.spec_from_file_location("tw_equity_workflow", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture
def acquired():
    return {
        "issuer": "twse-1611", "quarter": "2025Q3",
        "monthly_revenue": [
            {"month": month, "status": "available", "amount_ntd_thousands": amount,
             "url": f"https://example.com/{month}", "scope": "consolidated"}
            for month, amount in zip(
                ["2025-07", "2025-08", "2025-09"], [350, 400, 420],
            )
        ],
        "quarterly_filing": {"status": "available", "url": "https://example.com/filing"},
        "annual_report": {"status": "not_available_at_cutoff"},
        "material_disclosures": {"status": "none_found", "entries": []},
    }


def test_skill_entry_exposes_the_packaged_workflow():
    skill = (SKILL / "SKILL.md").read_text()
    assert "name: tw-equity-research" in skill
    assert "台灣上市公司" in skill
    for filename in ("acquire.py", "conference.py", "workflow.py"):
        assert f"scripts/{filename}" in skill
        assert (SKILL / "scripts" / filename).is_file()
    for name in (".codex-plugin", ".claude-plugin"):
        manifest = json.loads((PACKAGE / name / "plugin.json").read_text())
        assert "tw-equity-research" in json.dumps(manifest)
    assert (PACKAGE / "skills/equity-research-us/SKILL.md").is_file()


def test_report_keeps_monthly_and_filed_figures_with_separate_sources(workflow, acquired):
    result = workflow.assess(acquired, filed_ntd_thousands=1180, filed_scope="consolidated")

    assert result["quarterly_source_gate"]
    assert result["revenue"]["monthly_total_ntd_thousands"] == 1170
    assert result["revenue"]["filed_ntd_thousands"] == 1180
    assert result["revenue"]["filed_minus_monthly_ntd_thousands"] == 10
    assert result["revenue"]["filing_url"] == "https://example.com/filing"
    assert result["revenue"]["monthly_urls"] == [
        "https://example.com/2025-07", "https://example.com/2025-08",
        "https://example.com/2025-09",
    ]


@pytest.mark.parametrize("scope", [None, "individual"])
def test_monthly_and_filed_reports_remain_separate_when_filed_scope_is_unmatched(
    workflow, acquired, scope,
):
    result = workflow.assess(acquired, filed_ntd_thousands=1180, filed_scope=scope)

    assert result["revenue"]["monthly_total_ntd_thousands"] == 1170
    assert result["revenue"]["filed_ntd_thousands"] == 1180
    assert result["revenue"]["filed_minus_monthly_ntd_thousands"] is None


@pytest.mark.parametrize("attribute, value", [("scope", None), ("currency", "USD")])
def test_monthly_total_requires_known_common_scope_and_ntd(workflow, acquired, attribute, value):
    acquired["monthly_revenue"][0][attribute] = value

    result = workflow.assess(acquired, filed_ntd_thousands=1180, filed_scope="consolidated")

    assert result["revenue"]["monthly_total_ntd_thousands"] is None
    assert result["revenue"]["filed_minus_monthly_ntd_thousands"] is None


def test_annual_gate_is_independent_and_requires_annual_report(workflow, acquired):
    result = workflow.assess(acquired, annual=True)

    assert result["quarterly_source_gate"]
    assert not result["annual_source_gate"]
    assert "annual_report" in result["gaps"]
    acquired["annual_report"]["status"] = "available"
    assert workflow.assess(acquired, annual=True)["annual_source_gate"]


@pytest.mark.parametrize("status", ["retrieval_failed", "missing_body"])
def test_failed_disclosure_is_distinct_from_verified_empty_search(workflow, acquired, status):
    acquired["material_disclosures"]["status"] = status

    result = workflow.assess(acquired)

    assert not result["quarterly_source_gate"]
    assert "material_disclosures" in result["gaps"]


def test_post_quarter_body_must_be_reviewed_for_relevance(workflow, acquired):
    acquired["material_disclosures"] = {
        "status": "available",
        "entries": [{
            "status": "needs_quarter_relevance_review",
            "relevance": "post_quarter",
            "body": "季後發布的更正本文",
        }],
    }

    assert not workflow.assess(acquired)["quarterly_source_gate"]
    assert workflow.assess(acquired, reviewed_post_quarter=[0])["quarterly_source_gate"]


@pytest.mark.parametrize(("relevance", "status", "body"), [
    ("quarter", "detail_unavailable", ""),
    ("quarter", "available", " \n\t"),
    ("quarter", "detail_unavailable", "只有標題"),
    ("post_quarter", "needs_quarter_relevance_review", ""),
    ("post_quarter", "available", "季後發布的更正本文"),
])
def test_disclosure_without_usable_full_text_cannot_pass(
    workflow, acquired, relevance, status, body,
):
    acquired["material_disclosures"] = {
        "status": "available", "entries": [
            {"relevance": relevance, "status": status, "body": body},
        ],
    }

    result = workflow.assess(acquired, reviewed_post_quarter=[0])

    assert not result["quarterly_source_gate"]
    assert "material_disclosure:0" in result["gaps"]


def test_successful_empty_disclosure_search_passes(workflow, acquired):
    assert workflow.assess(acquired)["quarterly_source_gate"]


def test_current_month_observation_does_not_meet_historical_gate(workflow, acquired):
    acquired["monthly_revenue"][0]["status"] = "publication_unverified"

    result = workflow.assess(acquired)

    assert not result["quarterly_source_gate"]
    assert result["revenue"]["monthly_total_ntd_thousands"] is None


def test_latest_research_may_use_a_current_month_observation(workflow, acquired):
    acquired["mode"] = "latest"
    acquired["monthly_revenue"][0]["status"] = "observed"

    result = workflow.assess(acquired)

    assert result["quarterly_source_gate"]
    assert result["revenue"]["monthly_total_ntd_thousands"] == 1170
