"""Folder integration, not research-quality or fresh-host acceptance tests.

Non-Apple records below are invented mechanical fixtures, not issuer facts.
The Apple case copies retained public pilot inputs and authored partial prose.
Verification files are author self-check fixtures, never independent approval.
"""
import hashlib
import json
from pathlib import Path

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


def test_public_pilot_adjacent_quarters_and_competition_cutoffs(tmp_path):
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
    result = module.publish(tmp_path, asset, saved, {}, module.publication_snapshot(tmp_path), "public-pilot", complete=False)
    assert result["status"] == "checkpoint"
    published = json.loads((tmp_path / result["review"]).read_text())
    assert published["research"] == saved["research"]
    assert published["predecessor"] == "pilot" and published["publication"]["complete"] is False
    assert published["provenance"][base + "/data/sources/idc-1.json"]["available_at"] == evidence["idc"][1]["published_at"]
    before = {p: p.read_bytes() for p in tmp_path.rglob("*") if p.is_file()}
    repeat = load().discover(tmp_path, "latest", evidence["cutoffs"]["2024Q3"])
    assert module.recover(tmp_path, "public-pilot") == result
    assert load().discover(tmp_path, "latest", evidence["cutoffs"]["2024Q3"]) == repeat
    assert all(p.read_bytes() == value for p, value in before.items())


def test_source_declared_new_quarters_without_saved_conversation(tmp_path):
    assets = two_issuers(tmp_path)
    for asset, quarter in zip(assets, ("2024Q2", "2024Q4")):
        current = tmp_path / ("investing/assets/equities/" + asset + "/cycles/" + quarter)
        current.rename(tmp_path / (asset + "-retained-fixture"))
    result = load().discover(tmp_path, "latest", CUTOFF)
    assert {d["record"].split("/")[0] for d in result["decisions"] if d["action"] == "create_next_quarter_analysis"} == set(assets)
    assert len(list((tmp_path / "investing").rglob("review.json"))) == 2


@pytest.mark.parametrize("action", ["resume", "rollback", "user-edit"])
def test_generic_publication_interruption_preserves_other_issuer(tmp_path, monkeypatch, action):
    assets = two_issuers(tmp_path)
    base = "investing/assets/equities/" + assets[0]
    old = base + "/cycles/2024Q2/2024-08-01-r1"
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
