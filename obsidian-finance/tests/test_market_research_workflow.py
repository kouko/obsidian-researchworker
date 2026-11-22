"""Exercise the packaged workflow in independent Python processes.

Market revenue and shipments are sourced pilot observations, not live queries or
fresh conversations. See the Loom runtime replay for host-specific evidence.
"""

import json
from pathlib import Path
import subprocess
import sys

import pytest


PACKAGE = Path(__file__).resolve().parents[1]
SCRIPT = PACKAGE / "scripts" / "market_research.py"
IDC_Q2 = "https://www.idc.com/resource-center/press-releases/worldwide-smartphone-market-grew-6-5-in-the-second-quarter-of-2024-as-momentum-continues-to-build-according-to-idc-tracker/"
IDC_Q3 = "https://www.idc.com/resource-center/press-releases/worldwide-smartphone-market-grows-4-with-316-1-million-units-shipped-in-the-third-quarter-of-2024-according-to-idc/"
SIA_Q2 = "https://www.semiconductors.org/global-semiconductor-sales-increase-18-3-in-q2-2024-compared-to-q2-2023-quarter-to-quarter-sales-up-6-5/"
SIA_Q3 = "https://www.semiconductors.org/global-semiconductor-sales-increase-23-2-in-q3-2024-compared-to-q3-2023-quarter-to-quarter-sales-up-10-7/"


def run_market(*args, record=None):
    result = subprocess.run(
        [sys.executable, str(SCRIPT), *map(str, args)],
        input=json.dumps(record) if record is not None else None,
        text=True, capture_output=True, check=False,
    )
    assert result.returncode == 0, result.stderr or result.stdout
    return json.loads(result.stdout)


def sample_record(market, quarter, cutoff, identity, url, metric, unit, value):
    source = dict(url=url, published_at=cutoff, version=identity,
                  observation_period=quarter, locator="quarterly market total")
    claim = dict(text=f"{quarter} worldwide {metric}: {value} {unit}.",
                 source_ids=[identity], observation_period=quarter)
    return dict(market=market, quarter=quarter, cutoff=cutoff, revision=1,
                overview=f"# {market}\n\nWorldwide market, calendar quarters.",
                analysis=f"# Analysis\n\n{claim['text']}",
                outlook="# Outlook\n\nRevisit the growth comparison next quarter.",
                sources={identity: source}, claims={"market-total": claim},
                pending=["Revisit the growth comparison next quarter."])


def test_skill_package_lists_industry_entry_and_issuer_reference():
    skill = PACKAGE / "skills" / "industry-research" / "SKILL.md"
    assert "\nname: industry-research\n" in skill.read_text()
    for host in ("codex", "claude"):
        metadata = json.loads((PACKAGE / f".{host}-plugin" / "plugin.json").read_text())
        assert "quarterly market research" in metadata["description"].lower()
    issuer_reference = PACKAGE / "skills/equity-research/references/industry-and-competition.md"
    assert "industry-research" in issuer_reference.read_text()


def test_two_market_workflow_resumes_in_new_processes(tmp_path):
    markets = (
        ("smartphones", "shipments", "million units", (
            ("2024Q2", "2024-07-15", "idc-q2-initial", IDC_Q2, 285.4),
            ("2024Q3", "2024-10-14", "idc-q3-initial", IDC_Q3, 316.1),
        )),
        ("semiconductors", "sales", "billion USD", (
            ("2024Q2", "2024-08-05", "sia-q2-initial", SIA_Q2, 149.9),
            ("2024Q3", "2024-11-05", "sia-q3-initial", SIA_Q3, 166.0),
        )),
    )
    for market, metric, unit, periods in markets:
        for quarter, cutoff, identity, url, value in periods:
            record = sample_record(market, quarter, cutoff, identity, url, metric, unit, value)
            run_market("publish", tmp_path, record=record)
            resumed = run_market("resume", tmp_path, market, quarter)
            assert resumed["record"]["quarter"] == quarter
            assert resumed["record"]["pending"] == record["pending"]
            assert resumed["record"]["sources"][identity]["url"] == url

    apple = run_market("cite", tmp_path, "smartphones", "2024Q3", "market-total", "2024-10-31")
    assert apple["sources"]["idc-q3-initial"]["url"] == IDC_Q3
    early = run_market("cite", tmp_path, "smartphones", "2024Q3", "market-total", "2024-09-28")
    assert early is None
    assert len(list(tmp_path.rglob("review.md"))) == 4


def test_revision_does_not_supersede_eligible_citation_or_broken_resume(tmp_path):
    baseline = sample_record(
        "smartphones", "2024Q3", "2024-10-14", "idc-q3-initial",
        IDC_Q3, "shipments", "million units", 316.1,
    )
    original = Path(run_market("publish", tmp_path, record=baseline)["review"])
    revision = sample_record(
        "smartphones", "2024Q3", "2024-11-01", "counterpoint-q3",
        "https://counterpointresearch.com/en/insights/q3-2024-global-smartphone-shipments-grow-2-revenues-and-asp-reach-highest-ever-for-a-third-quarter",
        "shipments", "million units", 307.0,
    )
    revision["revision"] = 2
    updated = Path(run_market("publish", tmp_path, record=revision)["review"])
    earlier = run_market("cite", tmp_path, "smartphones", "2024Q3", "market-total", "2024-10-31")
    assert Path(earlier["review"]) == original
    later = run_market("cite", tmp_path, "smartphones", "2024Q3", "market-total", "2024-11-01")
    assert Path(later["review"]) == updated

    (updated.parent / "analysis.md").write_text("Interrupted or damaged content")
    recovered = run_market("resume", tmp_path, "smartphones", "2024Q3")
    assert recovered["issues"]
    assert Path(recovered["review"]) == original
    assert (updated.parent / "analysis.md").read_text() == "Interrupted or damaged content"


def test_eu_aggregate_withholds_quarter_until_third_month_is_eligible():
    periods = (
        ("2024-07", "2024-08-29", 102705, 852051),
        ("2024-08", "2024-09-19", 92627, 643637),
        ("2024-09", "2024-10-22", 139702, 809163),
    )
    sources = {month: {"published_at": release} for month, release, _, _ in periods}
    observations = [
        dict(month=month, scope="European Union", metric="BEV share",
             definition="BEV share of new passenger car registrations",
             unit="ratio", numerator=top, denominator=bottom, source_ids=[month])
        for month, _, top, bottom in periods
    ]
    record = dict(sources=sources, observations=observations)
    partial = run_market("aggregate", "2024Q3", "2024-10-21", "--ratio", record=record)
    assert partial["status"] == "partial"
    assert partial["missing_months"] == ["2024-09"]
    complete = run_market("aggregate", "2024Q3", "2024-10-31", "--ratio", record=record)
    assert complete["value"] == pytest.approx(335034 / 2304851)
    assert complete["source_ids"] == list(sources)


def test_prior_outlook_round_trip_and_target_horizon_comparison(tmp_path):
    (tmp_path / ".obsidian").mkdir()
    q2 = sample_record(
        "semiconductors", "2024Q2", "2024-08-05", "sia-q2-initial",
        SIA_Q2, "sales", "billion USD", 149.9,
    )
    forecast = dict(version="wsts-spring-2024", target_period="2024", scope="worldwide",
                    metric="sales", unit="billion USD", value=611.0, source_ids=["wsts-spring"])
    q2["market_name"] = "Worldwide semiconductor sales"
    q2["forecasts"] = [forecast]
    q2["sources"]["wsts-spring"] = dict(
        url="https://www.wsts.org/76/103/WSTS-Semiconductor-Market-Forecast-Spring-2024",
        published_at="2024-06-04", version="wsts-spring", observation_period="2024",
        locator="2024 Forecast",
    )
    run_market("publish", tmp_path, record=q2)
    prior = run_market("resume", tmp_path, "semiconductors", "2024Q2")["record"]
    carried = prior["forecasts"][0]
    assert carried == forecast

    q3 = sample_record(
        "semiconductors", "2024Q3", "2024-11-05", "sia-q3-initial",
        SIA_Q3, "sales", "billion USD", 166.0,
    )
    q3["sources"].update(prior["sources"])
    quarter_actual = dict(carried, version="sia-q3-initial", target_period="2024Q3",
                          value=166.0, source_ids=["sia-q3-initial"])
    comparison = run_market("compare", q3["cutoff"], record=dict(
        forecast=carried, actual=quarter_actual, sources=q3["sources"],
    ))
    assert comparison["reason"] == "noncomparable-actual"
    q3["actuals"] = [quarter_actual, dict(quarter_actual, scope="North America")]
    q3["forecasts"] = [carried]
    q3["comparisons"] = [comparison]
    altered = dict(q3, forecasts=[dict(carried, value=612.0)])
    result = subprocess.run(
        [sys.executable, str(SCRIPT), "publish", str(tmp_path)],
        input=json.dumps(altered), text=True, capture_output=True,
    )
    assert result.returncode != 0
    assert "changed a carried-forward forecast" in result.stderr
    run_market("publish", tmp_path, record=q3)
    updated = run_market("resume", tmp_path, "semiconductors", "2024Q3")["record"]
    assert updated["comparisons"] == [comparison]
    assert updated["forecasts"] == [forecast]

    annual_actual = dict(carried, version="sia-2024", value=627.6, source_ids=["sia-2024"])
    later_sources = dict(q3["sources"], **{"sia-2024": {"published_at": "2025-02-07"}})
    comparison_input = dict(forecast=carried, actual=annual_actual, sources=later_sources)
    assert run_market("compare", q3["cutoff"], record=comparison_input)["status"] == "pending"
    scored = run_market("compare", "2025-02-07", record=comparison_input)
    assert scored["forecast_version"] == "wsts-spring-2024"
    assert scored["actual_version"] == "sia-2024"

    refreshed = dict(
        q3, revision=2, cutoff="2025-02-07", sources=later_sources,
        actuals=[quarter_actual, dict(annual_actual, scope="North America"), annual_actual],
        comparisons=[scored],
    )
    run_market("publish", tmp_path, record=refreshed)
    assert run_market("resume", tmp_path, "semiconductors", "2024Q3")["record"][
        "comparisons"
    ] == [scored]
    assert run_market("resume", tmp_path, "semiconductors", "2024Q3", "--cutoff", "2024-11-05")[
        "record"
    ]["comparisons"] == [comparison]
    assert scored["error"] == pytest.approx(16.6)


def test_industry_notes_keep_two_corrections_and_original_citations(tmp_path):
    (tmp_path / ".obsidian").mkdir()
    record = sample_record(
        "smartphones", "2024Q3", "2024-10-14", "idc-q3-initial",
        IDC_Q3, "shipments", "million units", 316.1,
    )
    record.update(market_name="全球智慧型手機市場", language="zh-TW", updated="2026-11-21")
    overview = Path(run_market("publish", tmp_path, record=record)["review"])
    expected = tmp_path / "investing/industries/smartphones/2024Q3"
    assert overview == expected / "2024Q3 全球智慧型手機市場-總覽.md"
    size = expected / "2024Q3 全球智慧型手機市場-規模與市佔率.md"
    with size.open("a") as handle:
        handle.write("\nPersonal note after the managed section.\n")
    for revision, cutoff, value in [(2, "2024-11-01", 316.2), (3, "2024-11-04", 316.3)]:
        candidate = sample_record(
            "smartphones", "2024Q3", cutoff, f"idc-q3-r{revision}",
            IDC_Q3, "shipments", "million units", value,
        )
        candidate.update(revision=revision, market_name="Smartphones", language="en",
                         updated="2026-11-21")
        assert Path(run_market("publish", tmp_path, record=candidate)["review"]) == overview
    assert "Personal note after the managed section." in size.read_text()
    assert all(str(value) in size.read_text() for value in (316.1, 316.2, 316.3))
    assert not list(expected.glob("r[0-9]*"))
    for cutoff, source in [("2024-10-31", "idc-q3-initial"), ("2024-11-02", "idc-q3-r2")]:
        cited = run_market("cite", tmp_path, "smartphones", "2024Q3", "market-total", cutoff)
        assert list(cited["sources"]) == [source]
    current = run_market("resume", tmp_path, "smartphones", "2024Q3")
    assert current["record"]["revision"] == 3
    assert current["record"]["pending"]
    overview.write_text(overview.read_text().replace('"revision": 3', '"revision": "broken"'))
    recovered = run_market("resume", tmp_path, "smartphones", "2024Q3")
    assert recovered["record"]["revision"] == 2
    assert recovered["issues"] == ["r3: Industry quarter revisions must be contiguous"]


def test_industry_resume_keeps_legacy_and_prior_forecast_versions(tmp_path):
    old = sample_record(
        "smartphones", "2024Q2", "2024-07-15", "idc-q2-initial",
        IDC_Q2, "shipments", "million units", 285.4,
    )
    legacy = Path(run_market("publish", tmp_path, record=old)["review"])
    bytes_before = {path: path.read_bytes() for path in legacy.parent.glob("*.md")}
    (tmp_path / ".obsidian").mkdir()
    baseline = sample_record(
        "smartphones", "2024Q3", "2024-10-14", "idc-q3-initial",
        IDC_Q3, "shipments", "million units", 316.1,
    )
    baseline.update(market_name="Smartphones", supply_chain="Independent assembly assumptions.",
                    companies=[{"company": "aapl", "name": "Apple", "body": "Channel watch."}])
    known_forecast = {
        "version": "idc-q3-outlook", "scope": "global", "metric": "shipments",
        "target_period": "2024Q4", "unit": "million units", "value": 315.0,
        "source_ids": ["idc-q3-initial"],
    }
    baseline["forecasts"] = [known_forecast]
    run_market("publish", tmp_path, record=baseline)
    revised = sample_record(
        "smartphones", "2024Q3", "2024-11-01", "idc-q3-correction",
        IDC_Q3, "shipments", "million units", 316.2,
    )
    revised.update(revision=2, forecasts=[
        dict(known_forecast, version="idc-q3-outlook-correction", value=320.0,
             source_ids=["idc-q3-correction"]),
    ])
    run_market("publish", tmp_path, record=revised)
    assert run_market("resume", tmp_path, "smartphones", "2024Q2")["review"] == str(legacy)
    assert all(path.read_bytes() == old_bytes for path, old_bytes in bytes_before.items())
    previous = run_market("resume", tmp_path, "smartphones", "2024Q3", "--cutoff", "2024-10-31")
    current = run_market("resume", tmp_path, "smartphones", "2024Q3")
    assert previous["record"]["forecasts"] == [known_forecast]
    assert current["record"]["forecasts"][0]["value"] == 320.0
    assert current["record"]["supply_chain"] == baseline["supply_chain"]
    assert current["record"]["companies"] == baseline["companies"]


def test_industry_explicit_vault_destination_discovery(tmp_path):
    (tmp_path / ".obsidian").mkdir()
    record = sample_record(
        "smartphones", "2024Q3", "2024-10-14", "idc-q3-initial",
        IDC_Q3, "shipments", "million units", 316.1,
    )
    alternate = "Research/Industry Studies/Phone Market"
    record["market_name"] = "Smartphones"
    published = run_market("publish", tmp_path, "--destination", alternate, record=record)
    assert Path(published["review"]).parent == tmp_path / alternate / "2024Q3"
    assert run_market("resume", tmp_path, "smartphones", "2024Q3", "--destination", alternate)[
        "review"
    ] == published["review"]
    assert run_market("cite", tmp_path, "smartphones", "2024Q3", "market-total", "2024-10-31",
                      "--destination", alternate)["sources"]["idc-q3-initial"]["url"] == IDC_Q3
    assert run_market("resume", tmp_path, "smartphones", "2024Q3")["review"] is None


def test_industry_edit_and_late_source_leave_committed_research_readable(tmp_path):
    (tmp_path / ".obsidian").mkdir()
    baseline = sample_record(
        "smartphones", "2024Q3", "2024-10-14", "idc-q3-initial",
        IDC_Q3, "shipments", "million units", 316.1,
    )
    baseline["market_name"] = "Smartphones"
    overview = Path(run_market("publish", tmp_path, record=baseline)["review"])
    late = json.loads(json.dumps(baseline))
    late.update(revision=2, cutoff="2024-10-31")
    late["sources"]["later"] = dict(late["sources"]["idc-q3-initial"], published_at="2024-11-01")
    late["claims"]["market-total"]["source_ids"].append("later")
    failure = subprocess.run(
        [sys.executable, str(SCRIPT), "publish", str(tmp_path)],
        input=json.dumps(late), text=True, capture_output=True,
    )
    assert failure.returncode != 0
    assert "Ineligible source version" in failure.stderr
    assert run_market("resume", tmp_path, "smartphones", "2024Q3")["record"]["revision"] == 1

    before = overview.read_text()
    changed = before.replace("Worldwide market, calendar quarters.", "Manual change in analysis.")
    changed = changed.replace("<!-- industry-research:end -->",
                              "A manual addition after the history block.\n<!-- industry-research:end -->")
    overview.write_text(changed)
    readback = run_market("resume", tmp_path, "smartphones", "2024Q3")
    assert readback["record"]["claims"] == baseline["claims"]
    assert readback["issues"] == []
    cited = run_market("cite", tmp_path, "smartphones", "2024Q3", "market-total", "2024-10-31")
    assert cited["claim"] == baseline["claims"]["market-total"]
    assert overview.read_text() == changed
