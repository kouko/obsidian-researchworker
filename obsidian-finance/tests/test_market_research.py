import json
import subprocess
import sys
from pathlib import Path

import pytest

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))
from market_research import aggregate_quarter, cite, publish, resume


def record(market="phones", quarter="2024Q3", revision=1, cutoff="2024-10-31"):
    return {
        "market": market,
        "quarter": quarter,
        "revision": revision,
        "cutoff": cutoff,
        "overview": "# Market overview",
        "analysis": "# Market analysis",
        "outlook": "# Market outlook",
        "sources": {"release-v1": {
            "published_at": "2024-10-14", "version": "v1", "url": "https://example.org/releases",
            "locator": "Table 1", "observation_period": quarter,
        }},
        "claims": {"size": {"text": "Published market size", "source_ids": ["release-v1"]}},
        "pending": ["Further release expected"],
    }


def test_publish_same_note_structure_for_two_markets_and_reopen_in_fresh_process(tmp_path):
    for market in ("phones", "chips"):
        snapshot = record(market=market)
        review = publish(tmp_path, snapshot)
        assert review == tmp_path / market / "2024Q3/r1/review.md"
        assert {p.name for p in review.parent.iterdir()} == {
            "analysis.md", "sources.md", "outlook.md", "review.md",
        }
        assert (tmp_path / market / "overview.md").is_file()
        result = subprocess.run(
            [sys.executable, str(SCRIPTS / "market_research.py"), "resume",
             str(tmp_path), market, "2024Q3"],
            capture_output=True, text=True, check=True,
        )
        assert json.loads(result.stdout)["record"]["pending"] == snapshot["pending"]


def test_resume_ignores_interrupted_and_tampered_records_without_masking_other_scope(tmp_path):
    first = publish(tmp_path, record())
    second = publish(tmp_path, record(revision=2, cutoff="2024-11-02"))
    assert "[Previous snapshot](../r1/review.md)" in second.read_text()
    (second.parent / "analysis.md").write_text("changed")
    interrupted = second.parent.with_name("r3")
    interrupted.mkdir()
    (interrupted / "analysis.md").write_text("incomplete")
    (first.parent.parent / "personal.md").write_text("ordinary note")
    publish(tmp_path, record(quarter="2024Q4", cutoff="2025-01-31"))
    publish(tmp_path, record(market="chips"))
    recovered = resume(tmp_path, "phones", "2024Q3")
    assert recovered["review"] == str(first)
    assert len(recovered["issues"]) == 2
    assert (first.parent.parent / "personal.md").read_text() == "ordinary note"
    assert resume(tmp_path, "phones", "2024Q2")["record"] is None


def test_publish_preserves_existing_records_and_ordinary_overview(tmp_path):
    overview = tmp_path / "phones" / "overview.md"
    overview.parent.mkdir()
    overview.write_text("existing")
    review = publish(tmp_path, record())
    before = review.read_bytes()
    with pytest.raises(FileExistsError):
        publish(tmp_path, record())
    assert review.read_bytes() == before
    assert overview.read_text() == "existing"


def test_citation_checks_every_dependency_at_original_cutoff(tmp_path):
    early = publish(tmp_path, record())
    revised = record(revision=2, cutoff="2024-11-05")
    revised["sources"]["late-v1"] = {"version": "v1", "published_at": "2024-11-01"}
    revised["claims"]["size"]["source_ids"].append("late-v1")
    publish(tmp_path, revised)
    result = cite(tmp_path, "phones", "2024Q3", "size", "2024-10-31")
    assert result["review"] == str(early)
    assert list(result["sources"]) == ["release-v1"]
    assert cite(tmp_path, "phones", "2024Q3", "size", "2024-09-28") is None
    assert resume(tmp_path, "phones", "2024Q3", "2024-10-31")["review"] == str(early)


def test_aggregate_requires_complete_unique_months_and_recomputes_ratio():
    months = [
        {"month": month, "scope": "eu", "metric": "bev-share", "unit": "ratio",
         "definition": "BEV share of new passenger car registrations",
         "numerator": top, "denominator": bottom, "source_ids": [month]}
        for month, top, bottom in [("2024-07", 10, 100), ("2024-08", 40, 100), ("2024-09", 20, 400)]
    ]
    sources = {row["month"]: {"published_at": "2024-10-22"} for row in months}
    run = lambda items, cutoff: aggregate_quarter(
        "2024Q3", items, cutoff, sources=sources, ratio=True,
    )
    complete = run(months, "2024-10-31")
    assert complete["status"] == "complete"
    assert complete["value"] == pytest.approx(70 / 600)
    assert complete["source_ids"] == list(sources)
    assert run(months[:2], "2024-10-31")["missing_months"] == ["2024-09"]
    assert run(months, "2024-10-20")["status"] == "partial"
    assert run(months + [dict(months[0], numerator=11)], "2024-10-31")["status"] == "partial"
    assert run(months[:2] + [dict(months[2], scope="europe")], "2024-10-31")["status"] == "partial"
