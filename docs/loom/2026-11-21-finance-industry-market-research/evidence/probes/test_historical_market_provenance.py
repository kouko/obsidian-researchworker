# concern: A saved historical cutoff or bare date can authorize unreproducible market claims.
from pathlib import Path
import sys

import pytest

FINANCE_TESTS = Path(__file__).resolve().parents[5] / "obsidian-finance" / "tests"
sys.path.insert(0, str(FINANCE_TESTS))
from test_market_research import cite, publish, record, resume


def historical_record(**kwargs):
    snapshot = record(**kwargs)
    snapshot["sources"]["release-v1"].update(
        locator="Table 1", observation_period="2024Q3", classification="preliminary",
    )
    return snapshot


def test_historical_resume_does_not_promote_a_claim_using_november_data(tmp_path):
    cutoff = "2024-10-31"
    original = publish(tmp_path, historical_record(cutoff=cutoff))
    candidate = historical_record(revision=2, cutoff=cutoff)
    candidate["sources"]["release-v2"] = dict(
        candidate["sources"]["release-v1"], published_at="2024-11-01", version="v2",
    )
    candidate["claims"]["size"]["source_ids"].append("release-v2")

    try:
        publish(tmp_path, candidate)
    except ValueError:
        pass  # Rejecting a record with an ineligible claim also protects resume.

    recovered = resume(tmp_path, "phones", "2024Q3", cutoff)
    assert recovered["review"] == str(original)


@pytest.mark.parametrize("missing", ["url", "locator", "observation_period"])
def test_company_citation_requires_traceable_original(tmp_path, missing):
    cutoff = "2024-10-31"
    snapshot = historical_record(cutoff=cutoff)
    del snapshot["sources"]["release-v1"][missing]

    try:
        publish(tmp_path, snapshot)
    except ValueError:
        return
    assert cite(tmp_path, "phones", "2024Q3", "size", cutoff) is None
