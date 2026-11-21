import json
import subprocess
import sys
from pathlib import Path

import pytest

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))
from market_research import publish

# The standalone adversarial probes import these Python entries via this fixture.
from market_research import aggregate_quarter as aggregate_quarter
from market_research import cite as cite
from market_research import resume as resume


def market_cli(*args, record=None, check=True):
    return subprocess.run(
        [sys.executable, str(SCRIPTS / "market_research.py"), *map(str, args)],
        input=json.dumps(record) if record is not None else None,
        capture_output=True, text=True, check=check,
    )


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
        created = market_cli("publish", tmp_path, record=snapshot)
        review = Path(json.loads(created.stdout)["review"])
        assert review == tmp_path / market / "2024Q3/r1/review.md"
        assert {p.name for p in review.parent.iterdir()} == {
            "analysis.md", "sources.md", "outlook.md", "overview.md", "review.md",
        }
        assert (tmp_path / market / "overview.md").is_file()
        result = market_cli("resume", tmp_path, market, "2024Q3")
        assert json.loads(result.stdout)["record"]["pending"] == snapshot["pending"]


@pytest.mark.parametrize("damage", ["missing", "changed"])
def test_resume_requires_verified_revision_local_overview(tmp_path, damage):
    original = Path(json.loads(market_cli("publish", tmp_path, record=record()).stdout)["review"])
    later = record(revision=2, cutoff="2024-11-02")
    later["overview"] = "# Changed market scope"
    revision = Path(json.loads(market_cli("publish", tmp_path, record=later).stdout)["review"])
    assert "[Market overview](overview.md)" in revision.read_text()
    assert (original.parent / "overview.md").read_text() == "# Market overview\n"
    entry = tmp_path / "phones" / "overview.md"
    entry.write_text("User-owned market entry")
    result = market_cli("resume", tmp_path, "phones", "2024Q3")
    assert json.loads(result.stdout)["review"] == str(revision)
    overview = revision.parent / "overview.md"
    if damage == "missing":
        overview.unlink()
    else:
        overview.write_text("Edited revision overview")
    recovered = json.loads(market_cli("resume", tmp_path, "phones", "2024Q3").stdout)
    assert recovered["review"] == str(original)
    assert recovered["issues"] and "overview.md" in recovered["issues"][0]
    assert entry.read_text() == "User-owned market entry"


def test_legacy_resume_verifies_shared_overview_without_rewriting(tmp_path):
    review = publish(tmp_path, record())
    start, marker, body = review.read_text().partition("\n```market-research-record\n")
    manifest = json.loads(body.removesuffix("\n```\n"))
    manifest["schema"] = 1
    del manifest["files"]["overview.md"]
    (review.parent / "overview.md").unlink()
    start = start.replace("(overview.md)", "(../../overview.md)")
    legacy_review = start + marker + json.dumps(manifest, indent=2) + "\n```\n"
    review.write_text(legacy_review)

    result = json.loads(market_cli("resume", tmp_path, "phones", "2024Q3").stdout)
    assert result["review"] == str(review)
    shared_overview = tmp_path / "phones" / "overview.md"
    shared_overview.write_text("User notes with a different overview")
    result = json.loads(market_cli("resume", tmp_path, "phones", "2024Q3").stdout)
    assert result["review"] is None
    assert "Legacy shared overview.md differs" in result["issues"][0]
    assert shared_overview.read_text() == "User notes with a different overview"
    assert review.read_text() == legacy_review


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
    recovered = json.loads(market_cli("resume", tmp_path, "phones", "2024Q3").stdout)
    assert recovered["review"] == str(first)
    assert len(recovered["issues"]) == 2
    assert (first.parent.parent / "personal.md").read_text() == "ordinary note"
    missing = json.loads(market_cli("resume", tmp_path, "phones", "2024Q2").stdout)
    assert missing["record"] is None


def test_publish_preserves_existing_records_and_ordinary_overview(tmp_path):
    overview = tmp_path / "phones" / "overview.md"
    overview.parent.mkdir()
    overview.write_text("existing")
    review = publish(tmp_path, record())
    before = review.read_bytes()
    duplicate = market_cli("publish", tmp_path, record=record(), check=False)
    assert duplicate.returncode != 0
    assert review.read_bytes() == before
    assert overview.read_text() == "existing"


def test_citation_checks_every_dependency_at_original_cutoff(tmp_path):
    early = publish(tmp_path, record())
    revised = record(revision=2, cutoff="2024-11-05")
    revised["sources"]["late-v1"] = {"version": "v1", "published_at": "2024-11-01"}
    revised["claims"]["size"]["source_ids"].append("late-v1")
    publish(tmp_path, revised)
    result = json.loads(market_cli("cite", tmp_path, "phones", "2024Q3", "size", "2024-10-31").stdout)
    assert result["review"] == str(early)
    assert list(result["sources"]) == ["release-v1"]
    too_early = market_cli("cite", tmp_path, "phones", "2024Q3", "size", "2024-09-28")
    assert json.loads(too_early.stdout) is None
    historical = market_cli("resume", tmp_path, "phones", "2024Q3", "--cutoff", "2024-10-31")
    assert json.loads(historical.stdout)["review"] == str(early)


def test_aggregate_requires_complete_unique_months_and_recomputes_ratio():
    months = [
        {"month": month, "scope": "eu", "metric": "bev-share", "unit": "ratio",
         "definition": "BEV share of new passenger car registrations",
         "numerator": top, "denominator": bottom, "source_ids": [month]}
        for month, top, bottom in [("2024-07", 10, 100), ("2024-08", 40, 100), ("2024-09", 20, 400)]
    ]
    sources = {row["month"]: {"published_at": "2024-10-22"} for row in months}
    def run(items, cutoff):
        result = market_cli(
            "aggregate", "2024Q3", cutoff, "--ratio",
            record={"observations": items, "sources": sources},
        )
        return json.loads(result.stdout)

    complete = run(months, "2024-10-31")
    assert complete["status"] == "complete"
    assert complete["value"] == pytest.approx(70 / 600)
    assert complete["source_ids"] == list(sources)
    assert run(months[:2], "2024-10-31")["missing_months"] == ["2024-09"]
    assert run(months, "2024-10-20")["status"] == "partial"
    assert run(months + [dict(months[0], numerator=11)], "2024-10-31")["status"] == "partial"
    assert run(months[:2] + [dict(months[2], scope="europe")], "2024-10-31")["status"] == "partial"


def test_cli_read_barrier_refuses_resume_and_cite_until_recovery(tmp_path, monkeypatch):
    import industry_update

    (tmp_path / ".obsidian").mkdir()
    initial = record()
    initial["market_name"] = "Phones"
    market_cli("publish", tmp_path, record=initial)
    revised = dict(initial, revision=2, analysis="This edition preserves the earlier observation.")
    native_exchange = industry_update._exchange

    def interrupted(stage, payload, parent, name):
        native_exchange(stage, payload, parent, name)
        raise OSError("interrupted after exchange")

    with monkeypatch.context() as patches:
        patches.setattr(industry_update, "_exchange", interrupted)
        with pytest.raises(OSError, match="interrupted after exchange"):
            publish(tmp_path, revised)

    for args in [
        ("resume", tmp_path, "phones", "2024Q3"),
        ("cite", tmp_path, "phones", "2024Q3", "size", "2024-10-31"),
    ]:
        failed = market_cli(*args, check=False)
        assert failed.returncode != 0
        assert "update pending" in failed.stderr

    assert json.loads(market_cli("recover", tmp_path).stdout) == {"recovered": True}
    recovered = json.loads(market_cli("resume", tmp_path, "phones", "2024Q3").stdout)
    assert recovered["record"]["revision"] == 2
