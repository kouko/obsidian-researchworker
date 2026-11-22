# concern: quarter-local evidence must remain independently verifiable; unreviewed quarters and interrupted publications must remain discoverable.
"""Folder integration, not research-quality or fresh-host acceptance tests.

Non-Apple records below are invented mechanical fixtures, not issuer facts.
The Apple case copies retained public pilot inputs and authored partial prose.
Verification files are author self-check fixtures, never independent approval.
"""
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
import shutil
from pathlib import Path
from string import Template

import pytest

from test_research_store import CUTOFF, load, put


def digest(content):
    return hashlib.sha256(content.encode()).hexdigest()


def source(root, base, sid, identity, available, projection, fiscal=None):
    ref = base + "/data/" + identity + ".json"
    put(root, ref, projection)
    # put uses the same JSON serialization as the bytes whose digest is retained.
    raw = (root / ref).read_text()
    value = dict(version=1, id=sid, issuer=base.rsplit("/", 1)[1],
                 kind="financial_original" if fiscal else "market", identity=identity,
                 available_at=available, projection=projection, raw_format="json",
                 raw_ref=ref, raw_digest=digest(raw))
    if fiscal:
        value["fiscal"] = fiscal
    put(root, base + "/data/sources/" + identity + ".json", value)
    return dict(version=identity, projection=projection)


def unit(root, directory, name, content, consumed):
    ref = directory + "/" + name + ".md"
    put(root, directory + "/" + name + "-check.json", dict(version=1, output_digest=digest(content),
        checks={k: True for k in ("sources", "citations", "calculations", "counterevidence")}, unresolved=[]))
    (root / ref).write_text(content)
    return dict(output=dict(path=ref, digest=digest(content)),
                verification=directory + "/" + name + "-check.json", consumed=consumed)


@pytest.mark.parametrize("update", [
    "normal", "interrupted", "edited", "edited-before-read", "duplicate-role", "shared-report",
    "substituted-capture",
])
def test_fixed_quarter_updates_and_historical_read(tmp_path, monkeypatch, update):
    asset = two_issuers(tmp_path)[0]
    cycle = f"investing/assets/equities/{asset}/cycles/2024Q2"
    old = tmp_path / cycle / "2024-08-01-r1/review.json"
    original = old.read_bytes()
    source_review = json.loads(original)
    module = load()

    def publish(rid, cutoff, title, finding, company, predecessor=None, expected=None):
        review = dict(source_review, id=rid, cutoff=cutoff, research=dict(
            method="Retained public evidence", assumptions=[], changes="Updated credit assessment",
            gaps=["Synthesis pending"], horizons={h: dict(judgment="insufficient_evidence",
                evidence=[], invalidation_triggers=[]) for h in ("short", "medium", "long")}))
        if predecessor:
            review["predecessor"] = predecessor
        body = f"""---
finance_schema: 1
finance_role: financial-analysis
title: {title}
asset_id: {asset}
fiscal_quarter: 2024Q2
as_of: "{cutoff}"
review_id: {rid}
status: partial
---

# {title}

{finding}
"""
        target = f"{cycle}/{cutoff[:10]}-{rid}/analysis.md"
        review["units"] = {"credit": dict(source_review["units"]["credit"],
            output=dict(path=target, digest=digest(body)),
            verification=dict(version=1, output_digest=digest(body),
                checks={k: True for k in ("sources", "citations", "calculations", "counterevidence")},
                unresolved=[]))}
        if update == "shared-report":
            review["units"]["governance"] = dict(review["units"]["credit"])
        return module.publish(tmp_path, asset, review, {"analysis.md": body},
            expected if expected is not None else module.publication_snapshot(tmp_path),
            rid, complete=False, storage="quarterly",
            company_name=company, ticker="BANK")

    first_cutoff = "2024-08-12T23:59:59+00:00"
    first = publish("fixed1", first_cutoff, "初版", "Original conclusion", "Example / Bank")
    note = next((tmp_path / cycle).glob("*Financial Analysis.md"))
    overview = tmp_path / first["review"]
    _, stored = module._markdown.record(overview.read_text(), "quarter-overview")
    assert "fixture_value" not in overview.read_text()
    bindings = stored["quarter_evidence"]["units"]
    sid = "filing-2024Q2"
    ref = bindings["credit"]["sources"][sid]
    if update == "shared-report":
        assert bindings["governance"]["sources"][sid] == ref
    if update == "substituted-capture":
        quarter_root = tmp_path / cycle
        capture = quarter_root / ref
        original_capture = capture.read_text()
        capture.unlink()
        with pytest.raises(ValueError, match=sid):
            module.verify_quarter(quarter_root, overview.name)
        discovered = module.discover(tmp_path, "latest", CUTOFF, storage="quarterly")
        assert {"record": f"{asset}/2024Q2/fixed1", "work": "credit"} not in discovered["reusable"]
        assert any(sid in gap["reason"] and "original-2024Q2" in gap["reason"]
                   for gap in discovered["gaps"])
        capture.write_text(original_capture)
        _, registration = module._markdown.record(original_capture, "source-registration")
        isolated = tmp_path / "portable-quarter"
        shutil.copytree(quarter_root, isolated)
        changed = dict(registration, projection={"fixture_value": 11, "unit": "fixture"})
        altered_note = module._markdown.render_registration(asset, "source", changed)
        changed_ref = (isolated / ref).with_name(digest(altered_note) + ".md")
        changed_ref.write_text(altered_note)
        isolated_overview = isolated / overview.name
        isolated_overview.write_text(overview.read_text().replace(ref, changed_ref.relative_to(isolated).as_posix()))
        with pytest.raises(ValueError, match="source capture mismatch"):
            module.verify_quarter(isolated, overview.name)
        registration["identity"] = "substitute"
        registration["available_at"] = "2024-08-02"
        replacement = module._markdown.render_registration(asset, "source", registration)
        substitute = capture.with_name(digest(replacement) + ".md")
        substitute.write_text(replacement)
        overview.write_text(overview.read_text().replace(ref, substitute.relative_to(quarter_root).as_posix()))
        with pytest.raises(ValueError, match=sid):
            module.verify_quarter(quarter_root, overview.name)
        discovered = module.discover(tmp_path, "latest", CUTOFF, storage="quarterly")
        assert {"record": f"{asset}/2024Q2/fixed1", "work": "credit"} not in discovered["reusable"]
        assert any(sid in gap["reason"] and "original-2024Q2" in gap["reason"]
                   for gap in discovered["gaps"])
        return
    args = ("fixed2", CUTOFF, "Update", "Revised conclusion", "Renamed Bank", "fixed1")
    if update == "duplicate-role":
        duplicate = note.with_name("2024Q2 BANK Duplicate - 01 Financial Analysis.md")
        duplicate.write_bytes(note.read_bytes())
        with pytest.raises(ValueError, match="duplicate quarterly note role"):
            publish(*args)
        view = module.discover(tmp_path, "latest", CUTOFF, storage="quarterly")
        assert any("duplicate quarterly note role" in gap["reason"] for gap in view["gaps"])
        return
    if update == "edited":
        expected = module.publication_snapshot(tmp_path)
        note.write_bytes(note.read_bytes() + b"\nA user's added observation.\n")
        before = note.read_bytes()
        with pytest.raises(ValueError, match="Publication conflict"):
            publish(*args, expected=expected)
        assert note.read_bytes() == before
        assert "fixed1" in overview.read_text()
        return
    if update == "edited-before-read":
        note.write_bytes(note.read_bytes() + b"\nAn unchecked manual hypothesis.\n")
        publish(*args)
        text = note.read_text()
        assert "Previous editable report (unverified)" in text
        assert "> An unchecked manual hypothesis." in text
        assert "Sources: filing-2024Q2" not in text
        assert f"Previous report as of {first_cutoff}" not in text
        return
    if update == "interrupted":
        exchange = module._update._exchange
        before = overview.read_bytes()

        def interrupt(*args):
            exchange(*args)
            raise RuntimeError("interrupted just after financial note swap")

        monkeypatch.setattr(module._update, "_exchange", interrupt)
        with pytest.raises(RuntimeError, match="interrupted"):
            publish(*args)
        assert overview.read_bytes() == before
        with pytest.raises(ValueError, match="pending"):
            module.discover(tmp_path, "latest", CUTOFF, storage="quarterly")
        monkeypatch.setattr(module._update, "_exchange", exchange)
        assert module._update.recover(tmp_path) is False
        for wrong_asset, wrong_quarter in [(asset, "2024Q1"), ("software-fixture", "2024Q2")]:
            with pytest.raises(ValueError, match="outside the selected quarter"):
                module.recover_quarterly(tmp_path, wrong_asset, wrong_quarter)
            assert overview.read_bytes() == before
        assert module.recover_quarterly(tmp_path, asset, "2024Q2") is True
        assert module.recover_quarterly(tmp_path, asset, "2024Q2") is False

        industry_note = tmp_path / "industry-note.md"
        industry_note.write_bytes(b"Original industry note")
        monkeypatch.setattr(module._update, "_exchange", interrupt)
        with pytest.raises(RuntimeError, match="interrupted"):
            module._update.apply(tmp_path, {"industry-note.md": b"Original industry note"},
                                 {"industry-note.md": b"Updated industry note"})
        monkeypatch.setattr(module._update, "_exchange", exchange)
        assert module.recover_quarterly(tmp_path, asset, "2024Q2") is False
        assert module._update.recover(tmp_path) is True
    else:
        second = publish(*args)
        assert first["review"] == second["review"]
    assert first["review"] == f"{cycle}/2024Q2 BANK Example - Bank - 00 Research Overview.md"
    assert note.name == "2024Q2 BANK Example - Bank - 01 Financial Analysis.md"
    assert "Original conclusion" in note.read_text() and "Revised conclusion" in note.read_text()
    assert "filing-2024Q2" in note.read_text() and first_cutoff in note.read_text()
    assert "Financial%20Analysis.md" in (tmp_path / first["review"]).read_text()
    assert old.read_bytes() == original
    view = module.discover(tmp_path, "latest", CUTOFF, storage="quarterly")
    assert {"record": f"{asset}/2024Q2/fixed2", "work": "credit"} in view["reusable"]
    if update == "shared-report":
        assert {"record": f"{asset}/2024Q2/fixed2", "work": "governance"} in view["reusable"]
        assert list((tmp_path / cycle).glob("*Financial Analysis.md")) == [note]
    before = note.read_bytes()
    historical = module.discover(tmp_path, "historical", first_cutoff, storage="quarterly")
    assert not any("/fixed2" in item["record"] for item in historical["reusable"])
    assert any("earlier cutoff" in gap["reason"] for gap in historical["gaps"])
    assert note.read_bytes() == before
    with pytest.raises(ValueError, match="stale predecessor, fiscal identity or cutoff"):
        publish("backdated", first_cutoff, "Earlier", "Would replace current findings",
                "Example Bank", "fixed2")
    assert note.read_bytes() == before
    verified = module.verify_quarter(tmp_path / cycle, overview.name)
    assert {"record": f"{asset}/2024Q2/fixed2", "work": "credit"} in verified["reusable"]
    if update == "normal":
        _, compact = module._markdown.record(overview.read_text(), "quarter-overview")
        credit = compact["units"]["credit"]
        credit["output"]["path"] = cycle + "/" + credit["output"]["path"]
        retained = {key: compact[key] for key in ("version", "fiscal", "cutoff", "research", "units")}
        retained.update(id="fixed3", predecessor="fixed2")
        module.publish(tmp_path, asset, retained, {}, module.publication_snapshot(tmp_path),
                       "fixed3", complete=False, storage="quarterly", company_name="Example Bank", ticker="BANK")
        assert note.read_bytes() == before
        verified = module.verify_quarter(tmp_path / cycle, overview.name)
        assert {"record": f"{asset}/2024Q2/fixed3", "work": "credit"} in verified["reusable"]


def two_issuers(root):
    assets = ["bank-fixture", "software-fixture"]
    put(root, "investing/research.json", dict(version=1, assets=assets))
    for asset, periods, primary in [(assets[0], ("Q1", "Q2"), "credit"),
                                    (assets[1], ("Q3", "Q4"), "retention")]:
        base = "investing/assets/equities/" + asset
        put(root, base + "/asset.json", dict(version=1, id=asset, issuer=asset, questions=[
            dict(id=primary, required_sources=["filing-{fiscal}"], depends_on=[]),
            dict(id="governance", required_sources=[], depends_on=[]),
            dict(id="synthesis", required_sources=[], depends_on=[primary])]))
        for period, end, available in zip(periods, ("2024-03-31", "2024-06-30"), ("2024-05-01", "2024-08-01")):
            quarter = "2024" + period
            fiscal = dict(year=2024, period=period, period_end=end, original_accession=asset + "-" + quarter)
            sid = "filing-" + quarter
            consumed = source(root, base, sid, "original-" + quarter, available, {"fixture_value": 10, "unit": "fixture"}, fiscal)
            directory = base + "/cycles/" + quarter + "/" + available + "-r1"
            units = {name: unit(root, directory, name, "Mechanical fixture for " + asset + ": " + name,
                     {sid: consumed} if name == primary else {}) for name in (primary, "governance", "synthesis")}
            put(root, directory + "/review.json", dict(version=1, id="r1", fiscal=fiscal,
                cutoff=available + "T23:59:59+00:00", units=units))
        # Equal local source IDs across issuers must remain isolated.
        source(root, base, "market", "future-market", "2024-09-01", {"fixture_value": 100, "unit": "fixture"})
    return assets


def test_discover_markdown_scope_and_source_registration(tmp_path):
    import yaml

    assets = two_issuers(tmp_path)
    module = load()
    initial = module.discover(tmp_path, "latest", CUTOFF)

    def convert(relative, role, extras, filename):
        original = tmp_path / relative
        record = json.loads(original.read_text())
        properties = dict(finance_schema=1, finance_role=role, title=role, **extras)
        content = ("---\n" + yaml.safe_dump(properties) + "---\n\n# " + role
                   + "\n\n## Research record\n\n" + "```finance-" + role + "\n"
                   + yaml.safe_dump(record) + "```\n")
        original.with_name(filename).write_text(content)
        original.unlink()

    (tmp_path / "investing/index.md").write_text("# Ordinary overview")
    assert module.discover(tmp_path, "latest", CUTOFF)["reusable"] == initial["reusable"]
    convert("investing/research.json", "research-overview", {}, "index.md")
    for asset in assets:
        base = f"investing/assets/equities/{asset}"
        convert(base + "/asset.json", "asset-entry", {"asset_id": asset}, "Asset overview.md")
        for source in (tmp_path / base / "data/sources").glob("*.json"):
            record = json.loads(source.read_text())
            convert(source.relative_to(tmp_path), "source-registration", {
                "asset_id": asset, "source_id": record["id"], "source_version": record["identity"],
            }, source.with_suffix(".md").name)

    overview = tmp_path / "investing/index.md"
    overview.write_text(overview.read_text().replace("finance_role:", r'"finance\u005frole":', 1))
    migrated = module.discover(tmp_path, "latest", CUTOFF)
    assert migrated["reusable"] == initial["reusable"]
    assert migrated["excluded"] == initial["excluded"]
    source = next((tmp_path / f"investing/assets/equities/{assets[0]}/data/sources").glob("original-*.md"))
    content = source.read_text().replace("finance_role:", 'available_at: "2024-09-01"\nfinance_role:', 1)
    source.write_text(content)
    with pytest.raises(ValueError, match="Markdown source availability mismatch"):
        module.discover(tmp_path, "latest", CUTOFF)



def test_markdown_method_preserves_retained_apple_dependencies(tmp_path):
    import shutil
    import yaml

    fixture = (Path(__file__).parents[2] / "docs/finance/pilots/apple-2024q2-q3"
               / "host-continuation/cases/clean/investing")
    shutil.copytree(fixture, tmp_path / "investing")
    module = load()
    cutoff = "2024-08-02T23:59:59+00:00"
    before = module.discover(tmp_path, "historical", cutoff)
    method = tmp_path / "investing/assets/equities/aapl/data/analysis/growth-method.json"
    record = json.loads(method.read_text())
    props = dict(finance_schema=1, finance_role="method-registration", title="Growth method",
                 asset_id="aapl", method_id=record["id"], method_version=record["identity"])
    method.with_suffix(".md").write_text(
        "---\n" + yaml.safe_dump(props) + "---\n\n# Growth method\n\n## Research record\n\n"
        + "```finance-method-registration\n" + yaml.safe_dump(record) + "```\n")
    method.unlink()

    after = module.discover(tmp_path, "historical", cutoff)
    assert before["reusable"] == after["reusable"]
    assert {"record": "aapl/2024Q3/run-03-q3", "work": "growth"} in after["reusable"]


def test_cold_multi_issuer_calendars_repeat_and_amendment(tmp_path):
    assets = two_issuers(tmp_path)
    module = load()
    before_bytes = {p: p.read_bytes() for p in tmp_path.rglob("*") if p.is_file()}
    cold = load().discover(tmp_path, "latest", CUTOFF)
    assert len(cold["reusable"]) == 12
    assert {d["action"] for d in cold["decisions"]} == {"no_analysis_update"}
    assert {e["evidence"] for e in cold["excluded"]} == {a + ":market" for a in assets}
    for asset, current in zip(assets, ("2024Q2", "2024Q4")):
        assert any(r["record"] == asset + "/" + current + "/r1" for r in cold["reusable"])
    early = load().discover(tmp_path, "historical", "2024-05-01T23:59:59+00:00")
    assert {r["record"] for r in early["reusable"]} == {assets[0] + "/2024Q1/r1", assets[1] + "/2024Q3/r1"}
    for p, content in before_bytes.items():
        if p.suffix == ".json" and "/data/" not in str(p):
            p.write_text(json.dumps(json.loads(content), indent=4))
        p.touch()
    assert load().discover(tmp_path, "latest", CUTOFF) == cold
    assert len(list(tmp_path.rglob("review.json"))) == 4
    assert all(json.loads(p.read_bytes()) == json.loads(content) if p.suffix == ".json" else p.read_bytes() == content
               for p, content in before_bytes.items())
    changed = tmp_path / ("investing/assets/equities/" + assets[0] + "/data/sources/original-2024Q2.json")
    amendment = json.loads(changed.read_text())
    amendment["identity"] = "amended-2024Q2"
    amendment["available_at"] = "2024-08-15"
    amendment["projection"]["fixture_value"] = 11
    put(tmp_path, "investing/assets/equities/" + assets[0] + "/data/amendment.json", amendment["projection"])
    amendment["raw_ref"] = "investing/assets/equities/" + assets[0] + "/data/amendment.json"
    amendment["raw_digest"] = digest((tmp_path / amendment["raw_ref"]).read_text())
    put(tmp_path, str(changed.relative_to(tmp_path)), amendment)
    revised = module.discover(tmp_path, "latest", CUTOFF)
    recompute = {(d["record"], d["work"]) for d in revised["decisions"] if d["action"] in ("append_revision_same_quarter", "invalidate_dependent_checkpoint_and_recompute")}
    assert recompute == {(assets[0] + "/2024Q2/r1", q) for q in ("credit", "synthesis")}
    assert {tuple(r.values()) for r in revised["reusable"]} == {tuple(r.values()) for r in cold["reusable"]} - recompute
    assert all((tmp_path / r).exists() for r in ["investing/assets/equities/" + a + "/cycles" for a in assets])


@pytest.mark.parametrize("storage", ["legacy", "markdown"])
def test_public_pilot_adjacent_quarters_and_competition_cutoffs(tmp_path, storage):
    pilot = Path(__file__).parents[2] / "docs/finance/pilots/apple-2024q2-q3"
    packs = json.loads((pilot / "data/quarter-packs.json").read_text())
    evidence = json.loads((pilot / "competition-v1/evidence.json").read_text())
    prose = (pilot / "competition-v1/跨季競爭補充.md").read_text()
    asset = "aapl"
    base = "investing/assets/equities/" + asset
    put(tmp_path, "investing/research.json", dict(version=1, assets=[asset]))
    put(tmp_path, base + "/asset.json", dict(version=1, id=asset, issuer=asset, questions=[
        dict(id="financial", required_sources=["filing-{fiscal}"], depends_on=[]),
        dict(id="competition", required_sources=["competition"], depends_on=[]),
        dict(id="synthesis", required_sources=[], depends_on=["financial", "competition"])]))
    for index, quarter in enumerate(("2024Q2", "2024Q3")):
        pack, row = packs[quarter], evidence["idc"][index]
        fiscal = dict(year=2024, period=quarter[4:], period_end=pack["end"], original_accession=pack["original_accession"])
        filing = source(tmp_path, base, "filing-" + quarter, "filing-" + quarter, pack["cutoff"],
                        dict(metrics=pack["metrics"], source_url=pack["source_url"]), fiscal)
        competition = source(tmp_path, base, "competition", "idc-" + str(index), row["published_at"], row)
        cutoff = evidence["cutoffs"][quarter]
        directory = base + "/cycles/" + quarter + "/" + cutoff[:10] + "-pilot"
        financial_text = (pilot / quarter / "財務分析.md").read_text()
        units = {"financial": unit(tmp_path, directory, "financial", financial_text, {"filing-" + quarter: filing}),
                 "competition": unit(tmp_path, directory, "competition", prose.split("## 2024Q3 新增了什麼")[0] if index == 0 else prose, {"competition": competition})}
        # Midnight is fixture normalization of the retained authoring DATE,
        # not evidence of an actual authoring time or a 2024 publication.
        local_ref = base + "/data/competition-method.md"
        method_text = prose.split("## 2024Q2 截止時的市場反證")[0]
        (tmp_path / local_ref).write_text(method_text)
        method = dict(kind="method", version="v1", authored_at=evidence["authored_at"] + "T00:00:00+00:00", projection={"status": evidence["status"]},
                      content_ref=local_ref, content_digest=digest(method_text))
        put(tmp_path, base + "/data/analysis/competition-method.json", dict(method, version=1, identity="v1", id="competition-method"))
        units["competition"]["analysis_inputs"] = {"competition-method": method}
        meta = json.loads((tmp_path / base / "asset.json").read_text())
        meta["questions"][1]["required_analysis"] = ["competition-method"]
        put(tmp_path, base + "/asset.json", meta)
        put(tmp_path, directory + "/review.json", dict(version=1, id="pilot", fiscal=fiscal, cutoff=cutoff, units=units))
    historical = load().discover(tmp_path, "historical", evidence["cutoffs"]["2024Q2"])
    assert "45.2" not in (tmp_path / base / "cycles/2024Q2/2024-05-03-pilot/competition.md").read_text()
    assert {r["record"] for r in historical["reusable"]} == {"aapl/2024Q2/pilot"}
    assert "aapl:filing-2024Q3" in {e["evidence"] for e in historical["excluded"]}
    assert any(e["evidence"].startswith("aapl:competition@") for e in historical["excluded"])
    assert dict(record="aapl/2024Q2/pilot", work="competition") in historical["reusable"]
    late = load().discover(tmp_path, "latest", evidence["cutoffs"]["2024Q3"])
    assert any(r == dict(record="aapl/2024Q3/pilot", work="competition") for r in late["reusable"])
    assert any(d["work"] == "synthesis" and d["action"] == "resume_incomplete_work" for d in late["decisions"])
    assert late["external_freshness"] == "unverified"
    # Honest historical fixture remains partial: no investment-completion assertion.
    assert len(list(tmp_path.rglob("review.json"))) == 2
    saved = json.loads((tmp_path / directory / "review.json").read_text())
    saved.update(id="checkpoint", predecessor="pilot", research=dict(
        method="Retained public pilot; historical reconstruction authored in 2026; 0-3/3-12/12-60 month horizons",
        assumptions=["IDC preliminary shipments are not revenue or end-user sell-through"],
        changes="Q3 adds July IDC evidence excluded at Q2 cutoff",
        gaps=["Synthesis and full investment research remain incomplete"],
        horizons={h: dict(judgment="insufficient_evidence", evidence=["competition", "filing-2024Q3"],
            invalidation_triggers=["Revised IDC estimate or new original filing"])
            for h in ("short", "medium", "long")}))
    module = load()
    files = {}
    if storage == "markdown":
        template = pilot.parents[3] / "obsidian-finance/skills/equity-research-us/templates/financial-analysis.md"
        content = Template(template.read_text()).substitute(
            title_yaml="Apple quarterly financial checkpoint", title="Apple quarterly financial checkpoint",
            asset_id_yaml=asset, fiscal_quarter_yaml=quarter, as_of_yaml=json.dumps(cutoff),
            review_id_yaml="checkpoint", status_yaml="partial", findings=financial_text,
            source_and_comparison=pack["source_url"], unresolved="Synthesis is pending.")
        current = saved["units"]["financial"]
        comparator_metadata = f"{base}/data/sources/filing-2024Q2.json"
        comparator = json.loads((tmp_path / comparator_metadata).read_text())
        original = b"<html><title>Public pilot filing evidence fixture</title></html>"
        original_path = f"{base}/data/filing-2024Q2.html"
        (tmp_path / original_path).write_bytes(original)
        comparator.update(original_ref=original_path, original_digest=hashlib.sha256(original).hexdigest())
        put(tmp_path, comparator_metadata, comparator)
        current["consumed"]["filing-2024Q2"] = dict(version=comparator["identity"], projection=comparator["projection"])
        check = json.loads((tmp_path / current["verification"]).read_text())
        check["output_digest"] = digest(content)
        output = f"{base}/cycles/{quarter}/{cutoff[:10]}-checkpoint/financial.md"
        current.update(output=dict(path=output, digest=digest(content)), verification=check)
        ordinary = f"{base}/cycles/{quarter}/observations.md"
        claim = "The original filing is available for the third quarter."
        (tmp_path / ordinary).write_text(claim)
        notes = module.discover(tmp_path, "latest", cutoff, candidate_for=(asset, quarter))["candidate_notes"]
        assert notes == [{"path": ordinary}]
        current["candidate_notes"] = [dict(notes[0], claim=claim, source_id="filing-" + quarter,
                                           source_version="filing-" + quarter, source_available_at=pack["cutoff"])]
        files["financial.md"] = content
        synthesis_text = content.replace("financial-analysis", "synthesis")
        synthesis_path = f"{base}/cycles/{quarter}/{cutoff[:10]}-checkpoint/synthesis.md"
        saved["units"]["synthesis"] = dict(
            consumed={}, output=dict(path=synthesis_path, digest=digest(synthesis_text)),
            verification=dict(check, output_digest=digest(synthesis_text)))
        files["synthesis.md"] = synthesis_text
    baseline = module.publication_snapshot(tmp_path)
    if storage == "markdown":
        assert ordinary not in baseline
        (tmp_path / ordinary).write_text("# Formatting only\n\n> " + claim)
    result = module.publish(tmp_path, asset, saved, files, baseline, "public-pilot", complete=False, storage=storage)
    assert result["status"] == "checkpoint"
    saved_text = (tmp_path / result["review"]).read_text()
    if storage == "markdown":
        published = module._markdown.record(saved_text, "review")[1]
        assert "digest" not in published["units"]["financial"]["candidate_notes"][0]
        after = module.publication_snapshot(tmp_path)
        assert baseline.items() <= after.items()
        assert all(f"/cycles/{quarter}/data/raw/" in path
                   for path in after.keys() - baseline.keys() if path.endswith(".json"))
    else:
        published = json.loads(saved_text)
    assert published["research"] == saved["research"]
    assert published["predecessor"] == "pilot" and published["publication"]["complete"] is False
    assert published["provenance"][base + "/data/sources/idc-1.json"]["available_at"] == evidence["idc"][1]["published_at"]
    before = {p: p.read_bytes() for p in tmp_path.rglob("*") if p.is_file()}
    repeat = load().discover(tmp_path, "latest", evidence["cutoffs"]["2024Q3"])
    if storage == "legacy":
        assert module.recover(tmp_path, "public-pilot") == result
    assert load().discover(tmp_path, "latest", evidence["cutoffs"]["2024Q3"]) == repeat
    assert all(p.read_bytes() == value for p, value in before.items())
    if storage == "markdown":
        assert dict(record="aapl/2024Q3/checkpoint", work="financial") in repeat["reusable"]
        quarter_root = tmp_path / base / "cycles" / quarter
        isolated = tmp_path / "standalone" / "copied-quarter"
        shutil.copytree(quarter_root, isolated)
        portable = published["quarter_evidence"]
        assert portable["version"] == 1
        local_inputs = portable["units"]["financial"]["sources"]
        assert {"filing-2024Q2", "filing-2024Q3"} == local_inputs.keys()
        assert all(ref.startswith("data/sources/") for ref in local_inputs.values())
        assert published["units"]["financial"]["output"]["path"] == f"{cutoff[:10]}-checkpoint/financial.md"
        assert not any(path.name == "review.json" for path in isolated.glob("data/**/*"))
        validation = load().verify_quarter(isolated, f"{cutoff[:10]}-checkpoint/review.md")
        assert validation["status"] == "verified"
        assert {record["record"] for record in validation["reusable"]} == {"aapl/2024Q3/checkpoint"}
        _, registration = module._markdown.record(
            (isolated / local_inputs["filing-2024Q2"]).read_text(), "source-registration")
        assert registration["fiscal"]["original_accession"] == comparator["fiscal"]["original_accession"]
        assert (isolated / registration["original_ref"]).read_bytes() == original
        (isolated / Path(ordinary).name).unlink()
        assert module.verify_quarter(isolated, f"{cutoff[:10]}-checkpoint/review.md") == validation
        legacy_record = json.loads(json.dumps(published))
        legacy_record["units"]["financial"]["candidate_notes"][0]["digest"] = digest(claim)
        (isolated / f"{cutoff[:10]}-checkpoint/review.md").write_text(
            module._markdown.render_review(asset, quarter, legacy_record))
        assert module.verify_quarter(isolated, f"{cutoff[:10]}-checkpoint/review.md") == validation

        # A second vault assembled from just this quarter (plus configuration)
        # must not start a Q2 cycle for a copied Q2 comparator.
        local_vault = tmp_path / "quarter-owned"
        for config in ("investing/research.json", base + "/asset.json"):
            put(local_vault, config, json.loads((tmp_path / config).read_text()))
        shutil.copytree(quarter_root, local_vault / base / "cycles" / quarter)
        local_readback = load().discover(local_vault, "latest", cutoff)
        assert {item["record"] for item in local_readback["decisions"]} == {"aapl/2024Q3/checkpoint"}
        assert {item["work"] for item in local_readback["reusable"]} == {"financial", "competition", "synthesis"}
        local_quarter = local_vault / base / "cycles" / quarter
        damaged_vault = tmp_path / "damaged-leaf"
        shutil.copytree(local_vault, damaged_vault)
        (damaged_vault / base / "cycles" / quarter / registration["original_ref"]).unlink()
        damaged_baseline = module.publication_snapshot(damaged_vault)
        recovered = module._rebase_review(published, f"{base}/cycles/{quarter}", portable=False)
        recovered.update(id="independent", predecessor="checkpoint")
        stale_synthesis = json.loads(json.dumps(recovered))
        stale_synthesis["units"].pop("financial")
        with pytest.raises(ValueError, match="damaged unit or dependent output"):
            module.publish(damaged_vault, asset, stale_synthesis, {}, damaged_baseline,
                           "stale-synthesis", complete=False, storage="markdown")
        recovered["units"] = {"competition": recovered["units"]["competition"]}
        damaged_output = damaged_vault / base / "cycles" / quarter / published["units"]["financial"]["output"]["path"]
        output_before = damaged_output.read_bytes()
        damaged_output.write_text("Damaged historical output")
        with pytest.raises(ValueError, match="Publication conflict"):
            module.publish(damaged_vault, asset, recovered, {}, module.publication_snapshot(damaged_vault),
                           "corrupt-output", complete=False, storage="markdown")
        damaged_output.write_bytes(output_before)
        checkpoint = module.publish(damaged_vault, asset, recovered, {}, damaged_baseline,
                                    "independent", complete=False, storage="markdown")
        assert checkpoint["status"] == "checkpoint"
        resumed = module.discover(damaged_vault, "latest", cutoff)
        assert {"record": "aapl/2024Q3/independent", "work": "competition"} in resumed["reusable"]
        recovered.update(id="independent-next", predecessor="independent")
        follow_up_baseline = module.publication_snapshot(damaged_vault)
        stale_synthesis.update(id="resurrect-stale", predecessor="independent")
        with pytest.raises(ValueError, match="damaged unit or dependent output"):
            module.publish(damaged_vault, asset, stale_synthesis, {}, follow_up_baseline,
                           "resurrect-stale", complete=False, storage="markdown")
        checkpoint = module.publish(damaged_vault, asset, recovered, {}, follow_up_baseline,
                                    "independent-next", complete=False, storage="markdown")
        assert checkpoint["status"] == "checkpoint"
        resumed = module.discover(damaged_vault, "latest", cutoff)
        assert {"record": "aapl/2024Q3/independent-next", "work": "competition"} in resumed["reusable"]
        old_marker = local_quarter / f"{cutoff[:10]}-checkpoint/review.md"
        old_marker.write_text(module._markdown.render_review(asset, quarter, legacy_record))
        carried = module._rebase_review(legacy_record, f"{base}/cycles/{quarter}", portable=False)
        carried.update(id="legacy-carry", predecessor="checkpoint")
        carried_result = module.publish(local_vault, asset, carried, {}, module.publication_snapshot(local_vault),
                                        "legacy-carry", complete=False, storage="markdown")
        _, carried_marker = module._markdown.record((local_vault / carried_result["review"]).read_text(), "review")
        assert carried_marker["units"]["financial"]["candidate_notes"] == published["units"]["financial"]["candidate_notes"]
        assert module._markdown.record(old_marker.read_text(), "review")[1] == legacy_record

        # A newer accession version cannot replace the frozen local older copy.
        late_cutoff = "2024-10-01T23:59:59+00:00"
        later_projection = dict(saved["units"]["financial"]["consumed"]["filing-2024Q3"]["projection"],
                                revision="later supplemental disclosure")
        later_identity = source(tmp_path, base, "filing-2024Q3", "filing-2024Q3-later", late_cutoff,
                                later_projection, saved["fiscal"])
        assert dict(record="aapl/2024Q3/checkpoint", work="financial") in load().discover(
            tmp_path, "historical", cutoff)["reusable"]
        assert dict(record="aapl/2024Q3/checkpoint", work="financial") not in load().discover(
            tmp_path, "latest", late_cutoff)["reusable"]
        assert module.verify_quarter(isolated, f"{cutoff[:10]}-checkpoint/review.md") == validation

        later = module._rebase_review(published, f"{base}/cycles/{quarter}", portable=False)
        later.update(id="amended", cutoff=late_cutoff, predecessor="checkpoint")
        amended = content.replace(cutoff, late_cutoff).replace("review_id: checkpoint", "review_id: amended")
        refreshed = later["units"]["financial"]
        refreshed["consumed"]["filing-2024Q3"] = later_identity
        refreshed.pop("candidate_notes")
        refreshed["output"].update(path=f"{base}/cycles/{quarter}/{late_cutoff[:10]}-amended/financial.md",
                                   digest=digest(amended))
        refreshed["verification"]["output_digest"] = digest(amended)
        amended_result = module.publish(tmp_path, asset, later, {"financial.md": amended},
                                       module.publication_snapshot(tmp_path), "amended",
                                       complete=False, storage="markdown")
        local_amended = f"{late_cutoff[:10]}-amended/review.md"
        assert amended_result["review"].endswith(local_amended)
        _, amended_record = module._markdown.record((quarter_root / local_amended).read_text(), "review")
        later_sources = amended_record["quarter_evidence"]["units"]["financial"]["sources"]
        assert later_sources["filing-2024Q2"] == local_inputs["filing-2024Q2"]
        assert later_sources["filing-2024Q3"] != local_inputs["filing-2024Q3"]
        assert module.verify_quarter(quarter_root, f"{cutoff[:10]}-checkpoint/review.md") == validation
        assert dict(record="aapl/2024Q3/amended", work="financial") in module.verify_quarter(
            quarter_root, local_amended)["reusable"]

        original_copy = isolated / registration["original_ref"]
        original_copy.unlink()
        with pytest.raises(ValueError, match="quarter evidence"):
            module.verify_quarter(isolated, f"{cutoff[:10]}-checkpoint/review.md")
        active_original = quarter_root / registration["original_ref"]
        active_original.unlink()
        damaged = module.discover(tmp_path, "historical", cutoff)
        reusable = {r["work"] for r in damaged["reusable"] if r["record"] == "aapl/2024Q3/checkpoint"}
        assert reusable == {"competition"}
        assert {decision["work"] for decision in damaged["decisions"]
                if decision["record"] == "aapl/2024Q3/checkpoint"
                and decision["action"] == "invalidate_dependent_checkpoint_and_recompute"} == {"financial", "synthesis"}
        assert any(registration["original_ref"] in gap["reason"] for gap in damaged["gaps"])
        with pytest.raises(ValueError, match="quarter evidence"):
            module.verify_quarter(quarter_root, f"{cutoff[:10]}-checkpoint/review.md")
        active_original.write_bytes(original)
        (tmp_path / ordinary).unlink()
        changed = load().discover(tmp_path, "historical", cutoff, candidate_for=(asset, quarter))
        assert dict(record="aapl/2024Q3/checkpoint", work="financial") in changed["reusable"]
        assert dict(record="aapl/2024Q3/checkpoint", work="competition") in changed["reusable"]
        assert changed["candidate_notes"] == []
        assert changed["adopted_claims"] == [
            dict(saved["units"]["financial"]["candidate_notes"][0], record="aapl/2024Q3/checkpoint",
                 work="financial", note_present=False, dependent_work=["synthesis"], review_path=result["review"])]
        assert load().discover(tmp_path, "latest", late_cutoff, candidate_for=(asset, quarter))["adopted_claims"] == []

        assert module.verify_quarter(quarter_root, f"{cutoff[:10]}-checkpoint/review.md") == validation
        follow_up = module._rebase_review(amended_record, f"{base}/cycles/{quarter}", portable=False)
        follow_up.update(id="follow-up", predecessor="amended")
        stale_predecessor = dict(follow_up, predecessor="checkpoint")
        with pytest.raises(ValueError, match="Publication conflict"):
            module.publish(tmp_path, asset, stale_predecessor, {}, module.publication_snapshot(tmp_path),
                           "wrong-parent", complete=False, storage="markdown")
        checkpoint_output = quarter_root / published["units"]["financial"]["output"]["path"]
        checkpoint_bytes = checkpoint_output.read_bytes()
        checkpoint_output.write_bytes(b"Corrupt saved output")
        with pytest.raises(ValueError, match="Publication conflict"):
            module.publish(tmp_path, asset, follow_up, {}, module.publication_snapshot(tmp_path),
                           "corrupt-past", complete=False, storage="markdown")
        checkpoint_output.write_bytes(checkpoint_bytes)

        stale_citation = json.loads(json.dumps(follow_up))
        stale_citation["id"] = "stale-citation"
        stale_text = amended.replace("review_id: amended", "review_id: stale-citation")
        stale_unit = stale_citation["units"]["financial"]
        stale_unit["output"].update(path=f"{base}/cycles/{quarter}/{late_cutoff[:10]}-stale-citation/financial.md",
                                    digest=digest(stale_text))
        stale_unit["verification"]["output_digest"] = digest(stale_text)
        stale_unit["candidate_notes"] = [dict(saved["units"]["financial"]["candidate_notes"][0],
            source_version=later_identity["version"], source_available_at=cutoff)]
        (tmp_path / ordinary).write_text("Changed note")
        with pytest.raises(ValueError, match="candidate evidence must be independently cutoff eligible and frozen"):
            module.publish(tmp_path, asset, stale_citation, {"financial.md": stale_text},
                           module.publication_snapshot(tmp_path), "stale-citation", complete=False, storage="markdown")

        appended = module.publish(tmp_path, asset, follow_up, {}, module.publication_snapshot(tmp_path),
                                  "follow-up", complete=False, storage="markdown")
        assert appended["review"].endswith("/review.md")
        assert module.verify_quarter(quarter_root, appended["review"].split(f"/{quarter}/", 1)[1])["status"] == "verified"

        # Ambiguous saved source identities must not be accepted as one
        # unit's local file damage even if that unit already has a gap.
        conflict = json.loads(json.dumps(published))
        evidence_units = conflict["quarter_evidence"]["units"]
        source_id = "filing-2024Q2"
        conflicting = dict(conflict["units"]["financial"]["consumed"][source_id], version="different-version")
        conflict["units"]["synthesis"]["consumed"][source_id] = conflicting
        evidence_units["synthesis"]["sources"][source_id] = local_inputs[source_id]
        marker = quarter_root / f"{cutoff[:10]}-checkpoint/review.md"
        marker.write_text(module._markdown.render_review(asset, quarter, conflict))
        fail_closed = module.discover(tmp_path, "historical", cutoff)
        assert not any(r["record"] == "aapl/2024Q3/checkpoint" for r in fail_closed["reusable"])
        assert any("conflicting quarter evidence source bindings" in gap["reason"] for gap in fail_closed["gaps"])
        with pytest.raises(ValueError, match="conflicting quarter evidence source bindings"):
            module.verify_quarter(quarter_root, f"{cutoff[:10]}-checkpoint/review.md")


@pytest.mark.parametrize("change", [
    "managed-edit", "ordinary-to-managed", "managed-to-ordinary", "role-malformed",
    "escaped-role-key", "truncated-tagged-role",
])
def test_publication_snapshot_protects_quarter_managed_note_transitions(tmp_path, change):
    asset = two_issuers(tmp_path)[0]
    module = load()
    path = f"investing/assets/equities/{asset}/cycles/2024Q2/Notes.md"
    ordinary = "# Personal observations\n"
    managed = "---\nfinance_role: quarter-navigation\n---\n\n# Quarter navigation\n"
    malformed = "---\nfinance_role: quarter-navigation [\n"
    initial = ordinary if change == "ordinary-to-managed" else managed
    if change == "role-malformed":
        initial = malformed
    if change == "escaped-role-key":
        initial = managed.replace("finance_role", r'"finance\u005frole"')
    if change == "truncated-tagged-role":
        initial = malformed.replace("quarter-navigation", "!!str quarter-navigation")
    (tmp_path / path).write_text(initial)
    expected = module.publication_snapshot(tmp_path)
    assert (path in expected) == (initial != ordinary)
    changed = initial + "\n## Edited"
    if change == "ordinary-to-managed":
        changed = managed
    if change == "managed-to-ordinary":
        changed = ordinary
    (tmp_path / path).write_text(changed)
    prior = (tmp_path / path).parent / "2024-08-01-r1/review.json"
    proposal = dict(json.loads(prior.read_text()), id="managed-edit-check", predecessor="r1", cutoff=CUTOFF)
    with pytest.raises(ValueError, match="Publication conflict"):
        module.publish(tmp_path, asset, proposal, {}, expected, "managed-edit-check",
                       complete=False, storage="markdown")


def test_publication_snapshot_leaves_role_mentions_in_ordinary_notes_unprotected(tmp_path):
    asset = two_issuers(tmp_path)[0]
    module = load()
    path = f"investing/assets/equities/{asset}/cycles/2024Q2/Notes.md"
    (tmp_path / path).write_text('---\ntitle: "Mention {finance_role: quarter-navigation}"\n---\n\n# Ordinary\n')
    expected = module.publication_snapshot(tmp_path)
    assert path not in expected
    (tmp_path / path).write_text("# Changed ordinary note")
    assert module.publication_snapshot(tmp_path) == expected


def test_source_declared_new_quarters_without_saved_conversation(tmp_path):
    assets = two_issuers(tmp_path)
    for asset, quarter in zip(assets, ("2024Q2", "2024Q4")):
        current = tmp_path / ("investing/assets/equities/" + asset + "/cycles/" + quarter)
        current.rename(tmp_path / (asset + "-retained-fixture"))
    result = load().discover(tmp_path, "latest", CUTOFF)
    new_work = {(d["record"], d["work"]) for d in result["decisions"] if d["action"] == "resume_incomplete_work"}
    assert new_work == {(asset + "/" + quarter + "/new", question)
                        for asset, quarter, primary in zip(assets, ("2024Q2", "2024Q4"), ("credit", "retention"))
                        for question in (primary, "governance", "synthesis")}
    assert {e["evidence"] for e in result["excluded"]} == {a + ":market" for a in assets}
    assert len(list((tmp_path / "investing").rglob("review.json"))) == 2


@pytest.mark.parametrize("action", ["resume", "rollback", "user-edit"])
def test_generic_publication_interruption_preserves_other_issuer(tmp_path, monkeypatch, action):
    assets = two_issuers(tmp_path)
    base = "investing/assets/equities/" + assets[0]
    old = base + "/cycles/2024Q2/2024-08-01-r1"
    ordinary = tmp_path / base / "cycles/2024Q2/Ordinary note.md"
    ordinary.write_text("# Preserve this observation")
    saved = json.loads((tmp_path / old / "review.json").read_text())
    saved.update(id="r2", predecessor="r1", cutoff=CUTOFF,
        research=dict(method="Mechanical integration fixture; not investment research", assumptions=[], changes="Recovery exercise",
            gaps=[], horizons={h: dict(judgment="insufficient_evidence", evidence=[], invalidation_triggers=["New source"])
                              for h in ("short", "medium", "long")}))
    module = load()
    write = module._write_new
    def interrupt(root, ref, content):
        if ref.endswith("2024-08-31-r2/review.json"):
            raise OSError("integration interruption")
        return write(root, ref, content)
    monkeypatch.setattr(module, "_write_new", interrupt)
    with pytest.raises(OSError, match="integration interruption"):
        module.publish(tmp_path, assets[0], saved, {}, module.publication_snapshot(tmp_path), "generic-run")
    interrupted = load().discover(tmp_path, "latest", CUTOFF)
    assert any(g["evidence"] == "publication:generic-run" for g in interrupted["gaps"])
    assert len(interrupted["reusable"]) == 12
    other_files = {p: p.read_bytes() for p in (tmp_path / ("investing/assets/equities/" + assets[1])).rglob("*") if p.is_file()}
    monkeypatch.setattr(module, "_write_new", write)
    if action == "user-edit":
        user_file = tmp_path / old / "credit.md"
        user_file.write_text("User correction must survive recovery")
        before = {p: p.read_bytes() for p in tmp_path.rglob("*") if p.is_file()}
        for recovery in ("resume", "rollback"):
            with pytest.raises(ValueError, match="conflict"):
                module.recover(tmp_path, "generic-run", action=recovery)
            assert all(p.read_bytes() == value for p, value in before.items())
    else:
        result = module.recover(tmp_path, "generic-run", action=action)
        assert result["status"] == ("complete" if action == "resume" else "rolled_back")
        repeat = load().discover(tmp_path, "latest", CUTOFF)
        assert len(repeat["reusable"]) == 12
        assert not any(g["evidence"] == "publication:generic-run" for g in repeat["gaps"])
        before = {p: p.read_bytes() for p in tmp_path.rglob("*") if p.is_file()}
        assert module.recover(tmp_path, "generic-run", action=action) == result
        assert all(p.read_bytes() == value for p, value in before.items())
    assert all(p.read_bytes() == value for p, value in other_files.items())
    assert (tmp_path / old / "review.json").is_file()
    assert ordinary.read_text() == "# Preserve this observation"


def test_equal_local_source_ids_invalidate_only_own_issuer(tmp_path):
    assets = two_issuers(tmp_path)
    for asset, primary in zip(assets, ("credit", "retention")):
        base = "investing/assets/equities/" + asset
        identity = source(tmp_path, base, "market", "current-market", "2024-04-01", {"fixture_value": 10})
        metadata = json.loads((tmp_path / base / "asset.json").read_text())
        metadata["questions"][0]["required_sources"].append("market")
        put(tmp_path, base + "/asset.json", metadata)
        for review in (tmp_path / base / "cycles").rglob("review.json"):
            saved = json.loads(review.read_text())
            saved["units"][primary]["consumed"]["market"] = identity
            put(tmp_path, str(review.relative_to(tmp_path)), saved)
    cold = load().discover(tmp_path, "latest", CUTOFF)
    assert len(cold["reusable"]) == 12
    source(tmp_path, "investing/assets/equities/" + assets[0], "market", "amended-market", "2024-08-15", {"fixture_value": 11})
    revised = load().discover(tmp_path, "latest", CUTOFF)
    affected = {(d["record"], d["work"]) for d in revised["decisions"]
                if d["action"] in ("append_revision_same_quarter", "invalidate_dependent_checkpoint_and_recompute")}
    assert affected == {(assets[0] + "/" + quarter + "/r1", work)
                        for quarter in ("2024Q1", "2024Q2") for work in ("credit", "synthesis")}
    assert {r["work"] for r in revised["reusable"] if r["record"].startswith(assets[0] + "/")} == {"governance"}
    assert len([r for r in revised["reusable"] if r["record"].startswith(assets[1] + "/")]) == 6


@pytest.mark.parametrize("position", ["older", "newer"])
@pytest.mark.parametrize("state", ["absent", "empty", "interrupted", "withdrawn"])
def test_individually_unreviewed_quarters_remain_visible(tmp_path, position, state):
    assets = two_issuers(tmp_path)
    module = load()
    expected_new, expected_saved = set(), set()
    for asset, periods in zip(assets, (("2024Q1", "2024Q2"), ("2024Q3", "2024Q4"))):
        missing, retained = periods if position == "older" else reversed(periods)
        base = "investing/assets/equities/" + asset
        quarter = tmp_path / base / "cycles" / missing
        archive = tmp_path / base / "data/archived-quarter"
        quarter.rename(archive)
        if state in ("empty", "interrupted"):
            quarter.mkdir()
        if state == "interrupted":
            put(tmp_path, str(quarter.relative_to(tmp_path)) + "/unfinished/pending.json",
                dict(version=1, run="interrupted-" + asset, review_digest="not-written"))
        if state == "withdrawn":
            saved_path = next(archive.rglob("review.json"))
            saved = json.loads(saved_path.read_text())
            old_directory = str(saved_path.parent.relative_to(tmp_path))
            for unit_value in saved["units"].values():
                unit_value["output"]["path"] = old_directory + "/" + unit_value["output"]["path"].rsplit("/", 1)[1]
                unit_value["verification"] = old_directory + "/" + unit_value["verification"].rsplit("/", 1)[1]
            saved.update(id="withdrawable", research=dict(method="Mechanical withdrawal fixture", assumptions=[], changes="Boundary exercise", gaps=[],
                horizons={h: dict(judgment="insufficient_evidence", evidence=[], invalidation_triggers=["New original"])
                          for h in ("short", "medium", "long")}))
            module.publish(tmp_path, asset, saved, {}, module.publication_snapshot(tmp_path), "withdraw-" + asset)
            module.recover(tmp_path, "withdraw-" + asset, action="rollback")
        expected_new.add(asset + "/" + missing + "/new")
        expected_saved.add(asset + "/" + retained + "/r1")
    before = {p: p.read_bytes() for p in tmp_path.rglob("*") if p.is_file()}
    # Fresh module, only the root/cutoff; no conversation or supplied work list.
    result = load().discover(tmp_path, "latest", CUTOFF)
    pending = {d["record"] for d in result["decisions"] if d["action"] == "resume_incomplete_work"}
    assert pending == expected_new
    assert {r["record"] for r in result["reusable"]} == expected_saved
    assert not any(d["record"].endswith("/new") and d["record"].rsplit("/", 1)[0] + "/r1" in expected_saved
                   for d in result["decisions"])
    assert {e["evidence"] for e in result["excluded"]} == {a + ":market" for a in assets}
    if state in ("empty", "interrupted", "withdrawn"):
        assert result["gaps"]
    if state == "interrupted":
        assert any(g["evidence"].startswith("publication:interrupted-") for g in result["gaps"])
    assert all(p.read_bytes() == value for p, value in before.items())


@pytest.mark.parametrize("scenario", [
    "publish", "interrupt", "race", "mixed-race", "edited-output", "operating-output", "not-analysis",
    "method-copy", "method-conflict", "method-newer",
    "damaged-source-registration", "damaged-source-payload", "bad-review-utf8", "bad-review-symlink", "replaced-bad-output",
    "foreign-before-marker", "foreign-during-marker", "foreign-ordinary-after-marker", "foreign-text-after-marker",
    "registration-interruption", "damaged-method-registration",
])
def test_markdown_pilot_append_and_preserve_ordinary_notes(tmp_path, monkeypatch, scenario):
    asset = two_issuers(tmp_path)[0]
    base = f"investing/assets/equities/{asset}"
    quarter = f"{base}/cycles/2024Q2"
    ordinary = tmp_path / quarter / "Observations.md"
    ordinary.write_text("# Keep this note")
    module = load()
    assert {"record": f"{asset}/2024Q2/r1", "work": "credit"} in module.discover(tmp_path, "latest", CUTOFF)["reusable"]

    saved = json.loads((tmp_path / quarter / "2024-08-01-r1/review.json").read_text())
    saved.update(id="r2", predecessor="r1", cutoff=CUTOFF, research=dict(
        method="Read retained source", assumptions=[], changes="Partial update", gaps=["Synthesis pending"],
        horizons={h: dict(judgment="insufficient_evidence", evidence=[], invalidation_triggers=[])
                  for h in ("short", "medium", "long")}))
    if scenario.startswith("method-") or scenario == "damaged-method-registration":
        local = tmp_path / quarter
        directory = local / "data/analysis"
        directory.mkdir(parents=True)
        payload = local / "data/materials/comparison.txt"
        payload.parent.mkdir(parents=True)
        payload.write_text("Retained observed inputs and definitions")
        authored = dict(version=1, id="comparison", identity="v2", kind="method",
                        authored_at="2026-04-02T00:00:00+00:00", projection={"units": "USD"},
                        content_ref="data/materials/comparison.txt", content_digest=digest(payload.read_text()))
        registered = directory / "authored-comparison.md"
        registered.write_text(module._markdown.render_registration(asset, "method", authored))
        frozen = {key: authored[key] for key in module._ANALYSIS_FIELDS - {"version"}}
        frozen.update(version=authored["identity"], content_ref=quarter + "/" + authored["content_ref"])
        saved["units"]["credit"]["analysis_inputs"] = {"comparison": frozen}
        if scenario == "method-newer":
            older_ref = f"{base}/data/comparison.txt"
            older_text = "Legacy method definition"
            (tmp_path / older_ref).write_text(older_text)
            put(tmp_path, f"{base}/data/analysis/comparison.json",
                dict(authored, identity="v1", authored_at="2026-04-01T00:00:00+00:00",
                     content_ref=older_ref, content_digest=digest(older_text)))
    if scenario in ("damaged-source-registration", "damaged-source-payload"):
        # The replacement has no independently completed unit if credit fails.
        saved["units"] = {"credit": saved["units"]["credit"]}
    previous = module.publication_snapshot(tmp_path)
    output = f"""---
finance_schema: 1
finance_role: financial-analysis
title: Updated analysis
asset_id: {asset}
fiscal_quarter: 2024Q2
as_of: "{CUTOFF}"
review_id: r2
status: partial
---

# Updated analysis
"""
    if scenario == "operating-output":
        output = output.replace("financial-analysis", "operating-analysis")
    if scenario == "not-analysis":
        output = output.replace("financial-analysis", "asset-entry")
    saved["units"]["credit"].update(
        output=dict(path=quarter + "/2024-08-31-r2/analysis.md", digest=digest(output)),
        verification=dict(version=1, output_digest=digest(output),
                          checks={k: True for k in ("sources", "citations", "calculations", "counterevidence")},
                          unresolved=[]))
    def publish():
        return module.publish(tmp_path, asset, saved, {"analysis.md": output}, previous,
                              "pilot", complete=False, storage="markdown")

    if scenario.startswith("foreign-"):
        attachments = {"foreign-ordinary-after-marker": "Observations.md",
                       "foreign-text-after-marker": "Observations.txt"}
        attachment = attachments.get(scenario)
        target = tmp_path / quarter / "2024-08-31-r2"
        foreign = target / (attachment or "review.json")
        foreign_content = "# Ordinary observation" if attachment else '{"version":1,"foreign":true}'
        preflight, link = module._preconditions, module._link_staged

        def inject_after_preflight(root, expected, target=None):
            preflight(root, expected, target)
            if target is not None:
                foreign.write_text(foreign_content)

        def inject_during_link(*args):
            link(*args)
            foreign.write_text(foreign_content)

        if scenario == "foreign-before-marker":
            monkeypatch.setattr(module, "_preconditions", inject_after_preflight)
        else:
            monkeypatch.setattr(module, "_link_staged", inject_during_link)
        if attachment:
            assert publish()["status"] == "checkpoint"
            assert foreign.read_text() == foreign_content
            scanned = module.discover(tmp_path, "latest", CUTOFF)
            assert dict(record=f"{asset}/2024Q2/r2", work="credit") in scanned["reusable"]
            return
        with pytest.raises(ValueError, match="Publication conflict"):
            publish()
        assert foreign.read_text() == foreign_content
        assert (tmp_path / "investing/.research-drafts/pilot/review.md").is_file()
        marker = target / "review.md"
        if scenario == "foreign-before-marker":
            assert not marker.exists()
        else:
            with pytest.raises(ValueError, match="conflicting Markdown and legacy review"):
                module.verify_quarter(tmp_path / quarter, "2024-08-31-r2/review.md")
        scanned = module.discover(tmp_path, "latest", CUTOFF)
        assert dict(record=f"{asset}/2024Q2/r1", work="credit") in scanned["reusable"]
        assert not any(r["record"] == f"{asset}/2024Q2/r2" for r in scanned["reusable"])
        assert any("/2024-08-31-r2" in gap["record"] for gap in scanned["gaps"])
        return

    if scenario == "registration-interruption":
        link = module.os.link

        def interrupt_registration(source, destination, *, src_dir_fd, dst_dir_fd, follow_symlinks):
            if destination.endswith(".md") and destination != "review.md":
                with pytest.raises(FileNotFoundError):
                    module.os.stat(destination, dir_fd=dst_dir_fd, follow_symlinks=False)
                fd = module.os.open(source, module.os.O_RDONLY, dir_fd=src_dir_fd)
                with module.os.fdopen(fd, "rb") as payload:
                    assert digest(payload.read().decode("utf-8")) + ".md" == destination
                raise RuntimeError("interrupt before registration link")
            return link(source, destination, src_dir_fd=src_dir_fd, dst_dir_fd=dst_dir_fd,
                        follow_symlinks=follow_symlinks)

        monkeypatch.setattr(module.os, "link", interrupt_registration)
        with pytest.raises(RuntimeError, match="interrupt before registration"):
            publish()
        assert not list((tmp_path / quarter / "data/sources").glob("*.md"))
        assert not (tmp_path / quarter / "2024-08-31-r2/review.md").exists()
        assert {"record": f"{asset}/2024Q2/r1", "work": "credit"} in load().discover(
            tmp_path, "latest", CUTOFF)["reusable"]
        return
    if scenario == "interrupt":
        def interrupt(*args):
            raise RuntimeError("interrupt before marker")

        monkeypatch.setattr(module, "_link_staged", interrupt)
        with pytest.raises(RuntimeError, match="interrupt before marker"):
            publish()
        interrupted = load().discover(tmp_path, "latest", CUTOFF)
        assert {"record": f"{asset}/2024Q2/r1", "work": "credit"} in interrupted["reusable"]
        assert any("Unfinished Markdown draft" in gap["reason"] for gap in interrupted["gaps"])
        draft = tmp_path / "investing/.research-drafts/pilot/analysis.md"
        properties, _ = module._markdown.parse_note(draft.read_text(), "financial-analysis")
        assert properties["status"] == "draft"
        final = tmp_path / quarter / "2024-08-31-r2/analysis.md"
        assert final.read_bytes() == output.encode("utf-8")
        assert not (tmp_path / quarter / "2024-08-31-r2/review.md").exists()
        restarted = json.loads(json.dumps(saved))
        restarted["id"] = "retry"
        retry_output = output.replace("review_id: r2", "review_id: retry")
        retry_unit = restarted["units"]["credit"]
        retry_unit["output"].update(path=quarter + "/2024-08-31-retry/analysis.md", digest=digest(retry_output))
        retry_unit["verification"]["output_digest"] = digest(retry_output)
        monkeypatch.undo()
        resolution = module.publish(tmp_path, asset, restarted, {"analysis.md": retry_output},
                                    module.publication_snapshot(tmp_path), "retry",
                                    complete=False, storage="markdown")
        assert resolution["review"].endswith("-retry/review.md")
        assert {"record": f"{asset}/2024Q2/retry", "work": "credit"} in load().discover(
            tmp_path, "latest", CUTOFF)["reusable"]
        return
    if scenario in ("race", "mixed-race"):
        other = json.loads(json.dumps(saved))
        other["id"] = "r3"
        other_output = output.replace("review_id: r2", "review_id: r3")
        other_unit = other["units"]["credit"]
        other_unit["output"].update(path=quarter + "/2024-08-31-r3/analysis.md", digest=digest(other_output))
        other_unit["verification"]["output_digest"] = digest(other_output)
        storage = "markdown"
        if scenario == "mixed-race":
            storage = "legacy"
            check = other_unit["verification"]
            other_unit["verification"] = quarter + "/2024-08-31-r3/check.json"
            other_output_files = {"analysis.md": other_output, "check.json": json.dumps(check)}
        else:
            other_output_files = {"analysis.md": other_output}
        lock_calls = []
        quarter_lock = module._quarter_lock

        def track_lock(root, cycle):
            lock_calls.append(cycle)
            return quarter_lock(root, cycle)

        monkeypatch.setattr(module, "_quarter_lock", track_lock)
        with ThreadPoolExecutor(max_workers=2) as threads:
            calls = [threads.submit(publish), threads.submit(
                module.publish, tmp_path, asset, other, other_output_files, previous,
                "pilot-other", complete=False, storage=storage)]
        assert sum(call.exception() is None for call in calls) == 1
        if scenario == "mixed-race":
            assert lock_calls == [quarter, quarter]
            assert sum((tmp_path / quarter / d / f).is_file()
                       for d, f in (("2024-08-31-r2", "review.md"), ("2024-08-31-r3", "review.json"))) == 1
            assert module.discover(tmp_path, "latest", CUTOFF)["reusable"]
            return
        assert any("preserve user files/draft" in str(call.exception()) for call in calls)
        assert len(list((tmp_path / quarter).glob("*/review.md"))) == 1
        assert (tmp_path / "investing/.research-drafts/pilot/analysis.md").is_file()
        assert (tmp_path / "investing/.research-drafts/pilot-other/analysis.md").is_file()
        return
    if scenario == "not-analysis":
        with pytest.raises(ValueError, match="invalid Obsidian properties"):
            publish()
        assert not (tmp_path / quarter / "2024-08-31-r2/review.md").exists()
        return
    result = publish()
    assert result["review"].endswith("/review.md")
    assert (tmp_path / result["review"]).is_file()
    if scenario == "damaged-method-registration":
        reference = f"{quarter}/data/analysis/manual.md"
        (tmp_path / reference).write_text("---\nfinance_role: method-registration\n[")
        scan = module.discover(tmp_path, "latest", CUTOFF)
        assert {"record": f"{asset}/2024Q2/r2", "work": "credit"} in scan["reusable"]
        assert any(g["record"] == reference and g["evidence"] == "quarter-method" for g in scan["gaps"])
        assert module.verify_quarter(tmp_path / quarter, "2024-08-31-r2/review.md")["status"] == "verified"
        return
    if scenario in ("damaged-source-registration", "damaged-source-payload", "bad-review-utf8", "bad-review-symlink", "replaced-bad-output"):
        review_path = tmp_path / result["review"]
        isolated = tmp_path / quarter
        if scenario.startswith("damaged-source"):
            _, stored = module._markdown.record(review_path.read_text(), "review")
            reference = next(iter(stored["quarter_evidence"]["units"]["credit"]["sources"].values()))
            registration = isolated / reference
            if scenario == "damaged-source-registration":
                registration.write_text("---\nfinance_role: source-registration")
                damaged_ref = str(registration.relative_to(tmp_path))
            else:
                _, source_record = module._markdown.record(registration.read_text(), "source-registration")
                payload = isolated / source_record["raw_ref"]
                payload.unlink()
                damaged_ref = str(payload.relative_to(tmp_path))
        elif scenario in ("bad-review-utf8", "bad-review-symlink"):
            if scenario == "bad-review-utf8":
                review_path.write_bytes(bytes([255]))
            else:
                target = review_path.with_name("untrusted-marker.md")
                review_path.rename(target)
                review_path.symlink_to(target)
            damaged_ref = result["review"]
        else:
            _, stored = module._markdown.record(review_path.read_text(), "review")
            updated = module._rebase_review(stored, quarter, portable=False)
            updated.update(id="r3", predecessor="r2")
            content = output.replace("review_id: r2", "review_id: r3").replace("Updated analysis", "Replacement analysis")
            current = updated["units"]["credit"]
            current["output"].update(path=quarter + "/2024-08-31-r3/analysis.md", digest=digest(content))
            current["verification"]["output_digest"] = digest(content)
            module.publish(tmp_path, asset, updated, {"analysis.md": content},
                           module.publication_snapshot(tmp_path), "replacement", complete=False, storage="markdown")
            (review_path.parent / "analysis.md").write_text("Damaged previous output")
            damaged_ref = result["review"].rsplit("/", 1)[0]
        after = load().discover(tmp_path, "latest", CUTOFF)
        surviving = "r3" if scenario == "replaced-bad-output" else "r1"
        assert {"record": f"{asset}/2024Q2/{surviving}", "work": "credit"} in after["reusable"]
        assert {"record": "software-fixture/2024Q4/r1", "work": "retention"} in after["reusable"]
        assert any(damaged_ref in gap["record"] or damaged_ref in gap["reason"] for gap in after["gaps"])
        if scenario == "bad-review-symlink":
            assert not any(gap["evidence"] == "publication:pilot" for gap in after["gaps"])
        with pytest.raises(ValueError, match="quarter evidence"):
            module.verify_quarter(isolated, "2024-08-31-r2/review.md")
        return
    if scenario.startswith("method-") or scenario == "damaged-method-registration":
        snapshot = module.verify_quarter(local, "2024-08-31-r2/review.md")
        assert {"record": f"{asset}/2024Q2/r2", "work": "credit"} in snapshot["reusable"]
    if scenario == "method-conflict":
        # Both same-time registrations have valid hashes but genuinely
        # different versions and contents. Neither should win by filename.
        conflict_text = "A different calculation convention"
        conflict_payload = local / "data/materials/conflicting.txt"
        conflict_payload.write_text(conflict_text)
        registered.write_text(module._markdown.render_registration(asset, "method", dict(
            authored, identity="conflicting", content_ref="data/materials/conflicting.txt",
            content_digest=digest(conflict_text))))
        with pytest.raises(ValueError, match="ambiguous quarter method version"):
            load().discover(tmp_path, "latest", CUTOFF)
        assert module.verify_quarter(local, "2024-08-31-r2/review.md") == snapshot
        return
    after = load().discover(tmp_path, "latest", CUTOFF)
    assert {"record": f"{asset}/2024Q2/r2", "work": "credit"} in after["reusable"]
    current = module.publication_snapshot(tmp_path)
    assert all(current[path] == checksum for path, checksum in previous.items())
    assert all("/data/raw/" in path for path in current.keys() - previous.keys() if path.endswith(".json"))
    if scenario == "edited-output":
        (tmp_path / quarter / "2024-08-31-r2/analysis.md").write_text("Edited")
        assert {"record": f"{asset}/2024Q2/r2", "work": "credit"} not in load().discover(
            tmp_path, "latest", CUTOFF)["reusable"]


@pytest.mark.parametrize("case", [
    "ordinary", "marked", "flow", "flow-malformed", "malformed", "duplicate",
    "escaped", "escaped-explicit-continuation", "escaped-duplicate", "escaped-duplicate-key",
    "malformed-tagged-explicit",
])
def test_markdown_pilot_asset_entry_precedence(tmp_path, monkeypatch, case):
    asset = two_issuers(tmp_path)[0]
    base = tmp_path / "investing/assets/equities" / asset
    module = load()
    legacy = base.joinpath("asset.json").read_bytes()
    if case == "ordinary":
        def unavailable():
            pytest.fail("legacy discovery must not require YAML")

        monkeypatch.setattr(module._markdown, "_yaml", unavailable)
        (base / "Overview.md").write_text("---\ntitle: Personal note\n---\n# Personal note\n")
    else:
        properties = ("---\nfinance_schema: 1\nfinance_role: asset-entry\n"
                      f"title: Reordered questions\nasset_id: {asset}\n---\n\n# Reordered questions\n")
        data = json.loads(legacy)
        data["questions"] = data["questions"][:1]
        fence = chr(96) * 3
        body = f"\n## Research record\n\n{fence}finance-asset-entry\n{json.dumps(data)}\n{fence}\n"
        if case in ("flow", "flow-malformed"):
            props = dict(finance_schema=1, finance_role="asset-entry", title="Reordered questions", asset_id=asset)
            header = json.dumps(props)
            if case == "flow-malformed":
                header = header[:-1]
            properties = "---\n" + header + "\n---\n\n# Reordered questions\n"
        text = properties + body
        if case.startswith("escaped"):
            text = text.replace("finance_role:", r'"finance\u005frole":')
        if case == "escaped-explicit-continuation":
            text = properties.replace("finance_role: asset-entry",
                                      '? "finance_' + chr(92) + '\n  role"\n: asset-entry') + body
        if case == "escaped-duplicate-key":
            text = text.replace("finance_schema: 1", "finance_schema: 1\nfinance_role: asset-entry")
        if case == "malformed-tagged-explicit":
            text = text.replace("finance_role: asset-entry", '? !!str "finance_role"\n: !!str asset-entry [')
        if case == "malformed":
            text = text.replace("finance_schema: 1", "finance_schema: unsupported")
        (base / "Overview.md").write_text(text)
        if case in ("duplicate", "escaped-duplicate"):
            (base / "Second.md").write_text(text)
    if case in ("flow-malformed", "malformed", "duplicate", "escaped-duplicate", "escaped-duplicate-key",
                "malformed-tagged-explicit"):
        with pytest.raises(ValueError, match="invalid managed note YAML|invalid Obsidian properties|duplicate Markdown asset|unique text keys"):
            module.discover(tmp_path, "latest", CUTOFF)
    else:
        if case in ("marked", "flow", "escaped", "escaped-explicit-continuation"):
            # Existing reviews use all old question IDs. A marked entry must
            # supply the current metadata rather than silently falling back.
            assert len(module._asset_metadata(tmp_path, f"investing/assets/equities/{asset}")["questions"]) == 1
            with pytest.raises(ValueError, match="unknown saved unit"):
                module.discover(tmp_path, "latest", CUTOFF)
        else:
            assert len(module.discover(tmp_path, "latest", CUTOFF)["reusable"]) == 12
    assert base.joinpath("asset.json").read_bytes() == legacy


def test_legacy_recovery_refuses_markdown_descendant_appearing_after_snapshot(tmp_path, monkeypatch):
    asset = two_issuers(tmp_path)[0]
    cycle = f"investing/assets/equities/{asset}/cycles/2024Q2"
    module = load()
    legacy = json.loads((tmp_path / cycle / "2024-08-01-r1/review.json").read_text())
    legacy.update(id="legacy-parent", predecessor="r1", cutoff=CUTOFF, research=dict(
        method="Read retained source", assumptions=[], changes="Legacy checkpoint", gaps=[],
        horizons={h: dict(judgment="insufficient_evidence", evidence=[], invalidation_triggers=[])
                  for h in ("short", "medium", "long")}))
    parent = module.publish(tmp_path, asset, legacy, {}, module.publication_snapshot(tmp_path), "legacy-parent")
    root = tmp_path / "separate-copy"
    shutil.copytree(tmp_path / "investing", root / "investing")
    child = dict(legacy, id="markdown-child", predecessor="legacy-parent")
    published = module.publish(root, asset, child, {}, module.publication_snapshot(root),
                               "markdown-child", storage="markdown")
    child_dir = Path(published["review"]).parent
    preflight = module._preconditions
    quarter_lock = module._quarter_lock
    locks = []

    def track_lock(root, path):
        locks.append(path)
        return quarter_lock(root, path)

    def sync_after_preflight(root, expected, target, **kwargs):
        preflight(root, expected, target, **kwargs)
        # A sync client does not take the tool's lock. Its newly arrived
        # descendant must still prevent withdrawing the legacy parent.
        if not (root / child_dir).exists():
            shutil.copytree(tmp_path / "separate-copy" / child_dir, root / child_dir)

    monkeypatch.setattr(module, "_preconditions", sync_after_preflight)
    monkeypatch.setattr(module, "_quarter_lock", track_lock)
    with pytest.raises(ValueError, match="descendant review exists"):
        module.recover(tmp_path, "legacy-parent", action="rollback")
    assert locks == [cycle]
    assert not (tmp_path / Path(parent["review"]).parent / "withdrawn.json").exists()
    assert (tmp_path / published["review"]).is_file()
