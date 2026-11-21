# concern: unreviewed fiscal quarters and interrupted publications must remain discoverable without losing independent research.
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
        template = pilot.parents[3] / "obsidian-finance/skills/finance-research/templates/financial-analysis.md"
        content = Template(template.read_text()).substitute(
            title_yaml="Apple quarterly financial checkpoint", title="Apple quarterly financial checkpoint",
            asset_id_yaml=asset, fiscal_quarter_yaml=quarter, as_of_yaml=json.dumps(cutoff),
            review_id_yaml="checkpoint", status_yaml="partial", findings=financial_text,
            source_and_comparison=pack["source_url"], unresolved="Synthesis is pending.")
        current = saved["units"]["financial"]
        check = json.loads((tmp_path / current["verification"]).read_text())
        check["output_digest"] = digest(content)
        output = f"{base}/cycles/{quarter}/{cutoff[:10]}-checkpoint/financial.md"
        current.update(output=dict(path=output, digest=digest(content)), verification=check)
        ordinary = f"{base}/cycles/{quarter}/observations.md"
        claim = "The original filing is available for the third quarter."
        (tmp_path / ordinary).write_text(claim)
        notes = module.discover(tmp_path, "latest", cutoff, candidate_for=(asset, quarter))["candidate_notes"]
        assert notes == [{"path": ordinary, "digest": digest(claim)}]
        current["candidate_notes"] = [dict(notes[0], claim=claim, source_id="filing-" + quarter,
                                           source_version="filing-" + quarter, source_available_at=pack["cutoff"])]
        files["financial.md"] = content
    baseline = module.publication_snapshot(tmp_path)
    result = module.publish(tmp_path, asset, saved, files, baseline, "public-pilot", complete=False, storage=storage)
    assert result["status"] == "checkpoint"
    saved_text = (tmp_path / result["review"]).read_text()
    if storage == "markdown":
        published = module._markdown.record(saved_text, "review")[1]
        after = module.publication_snapshot(tmp_path)
        assert baseline.items() <= after.items()
        assert {path for path in after.keys() - baseline.keys() if path.endswith(".json")} == set()
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
        (tmp_path / ordinary).write_text("Changed note")
        changed = load().discover(tmp_path, "latest", cutoff)
        assert dict(record="aapl/2024Q3/checkpoint", work="financial") not in changed["reusable"]
        assert dict(record="aapl/2024Q3/checkpoint", work="competition") in changed["reusable"]


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


@pytest.mark.parametrize("scenario", ["publish", "interrupt", "race", "mixed-race", "edited-output"])
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
    saved["units"]["credit"].update(
        output=dict(path=quarter + "/2024-08-31-r2/analysis.md", digest=digest(output)),
        verification=dict(version=1, output_digest=digest(output),
                          checks={k: True for k in ("sources", "citations", "calculations", "counterevidence")},
                          unresolved=[]))
    def publish():
        return module.publish(tmp_path, asset, saved, {"analysis.md": output}, previous,
                              "pilot", complete=False, storage="markdown")

    if scenario == "interrupt":
        def interrupt(*args):
            raise RuntimeError("interrupt before marker")

        monkeypatch.setattr(module, "_link_staged", interrupt)
        with pytest.raises(RuntimeError, match="interrupt before marker"):
            publish()
        interrupted = load().discover(tmp_path, "latest", CUTOFF)
        assert {"record": f"{asset}/2024Q2/r1", "work": "credit"} in interrupted["reusable"]
        assert any("Unfinished Markdown draft" in gap["reason"] for gap in interrupted["gaps"])
        assert (tmp_path / "investing/.research-drafts/pilot/analysis.md").is_file()
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
    result = publish()
    assert result["review"].endswith("/review.md")
    assert (tmp_path / result["review"]).is_file()
    after = load().discover(tmp_path, "latest", CUTOFF)
    assert {"record": f"{asset}/2024Q2/r2", "work": "credit"} in after["reusable"]
    current = module.publication_snapshot(tmp_path)
    assert all(current[path] == checksum for path, checksum in previous.items())
    assert not any(path.endswith(".json") for path in current.keys() - previous.keys())
    if scenario == "edited-output":
        (tmp_path / quarter / "2024-08-31-r2/analysis.md").write_text("Edited")
        assert {"record": f"{asset}/2024Q2/r2", "work": "credit"} not in load().discover(
            tmp_path, "latest", CUTOFF)["reusable"]


@pytest.mark.parametrize("case", ["ordinary", "marked", "malformed", "duplicate"])
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
        text = properties + body
        if case == "malformed":
            text = text.replace("finance_schema: 1", "finance_schema: unsupported")
        (base / "Overview.md").write_text(text)
        if case == "duplicate":
            (base / "Second.md").write_text(text)
    if case in ("malformed", "duplicate"):
        with pytest.raises(ValueError, match="invalid Obsidian properties|duplicate Markdown asset"):
            module.discover(tmp_path, "latest", CUTOFF)
    else:
        if case == "marked":
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

    def sync_after_preflight(root, expected, target):
        preflight(root, expected, target)
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
