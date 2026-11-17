import hashlib
import importlib.util
import json
import shutil
from pathlib import Path

import pytest

SPEC = importlib.util.spec_from_file_location("research_store", Path(__file__).parents[1] / "scripts/research_store.py")
CUTOFF = "2024-08-31T23:59:59+00:00"


def load():
    module = importlib.util.module_from_spec(SPEC)
    SPEC.loader.exec_module(module)
    return module


def put(root, path, value):
    target = root / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(value))


def sample(root):
    base = "investing/assets/equities/aapl"
    fiscal = dict(year=2024, period="Q2", period_end="2024-03-30", original_accession="q2-original")
    put(root, "investing/research.json", dict(version=1, assets=["aapl"]))
    put(root, base + "/asset.json", dict(version=1, id="aapl", issuer="AAPL", questions=[dict(id="valuation", required_sources=["price"], depends_on=[])]))
    source = dict(version=1, id="price", issuer="AAPL", kind="price", identity="price-v1", available_at="2024-05-03", projection=dict(value=10, unit="USD", raw_text="raw"), raw_format="text", raw_ref=base + "/data/price.txt", raw_digest=hashlib.sha256(b"raw").hexdigest())
    put(root, base + "/data/sources/price.json", source)
    (root / base / "data/price.txt").write_text("raw")
    review = base + "/cycles/2024Q2/2024-05-03-r1"
    put(root, review + "/verification.json", dict(version=1, output_digest=hashlib.sha256(b"analysis").hexdigest(), checks={k: True for k in ("sources", "citations", "calculations", "counterevidence")}, unresolved=[]))
    (root / review / "analysis.md").write_text("analysis")
    unit = dict(consumed={"price": dict(version="price-v1", projection=dict(value=10, unit="USD", raw_text="raw"))}, output=dict(path=review + "/analysis.md", digest=hashlib.sha256(b"analysis").hexdigest()), verification=review + "/verification.json")
    put(root, review + "/review.json", dict(version=1, id="r1", fiscal=fiscal, cutoff="2024-05-03T23:59:59+00:00", units={"valuation": unit}))
    return base, source, review


def test_folder_discovers_cycles(tmp_path):
    base, _, review = sample(tmp_path)
    asset = json.loads((tmp_path / base / "asset.json").read_text())
    asset["questions"].append(dict(id="synthesis", depends_on=["valuation"], required_sources=[]))
    put(tmp_path, base + "/asset.json", asset)
    result = load().discover(tmp_path, "latest", CUTOFF)
    assert result["reusable"] == [dict(record="aapl/2024Q2/r1", work="valuation")]
    assert any(d["work"] == "synthesis" and d["action"] == "resume_incomplete_work" for d in result["decisions"])
    saved = json.loads((tmp_path / review / "review.json").read_text())
    saved.update(id="r2", predecessor="r1", cutoff=CUTOFF)
    put(tmp_path, base + "/cycles/2024Q2/2024-08-31-r2/review.json", saved)
    latest = load().discover(tmp_path, "latest", CUTOFF)
    assert {d["record"] for d in latest["decisions"]} == {"aapl/2024Q2/r2"}
    historical = load().discover(tmp_path, "historical", "2024-05-03T23:59:59+00:00")
    assert {d["record"] for d in historical["decisions"]} == {"aapl/2024Q2/r1"}
    source = json.loads((tmp_path / base / "data/sources/price.json").read_text())
    source.update(id="price-2024Q2", kind="financial_original", fiscal=saved["fiscal"])
    asset["questions"][0]["required_sources"] = ["price-{fiscal}"]
    put(tmp_path, base + "/asset.json", asset)
    put(tmp_path, base + "/data/sources/price.json", source)
    (tmp_path / base / "cycles").rename(tmp_path / "archived-cycles")
    initial = load().discover(tmp_path, "latest", CUTOFF)
    assert {d["work"] for d in initial["decisions"] if d["action"] == "resume_incomplete_work"} == {"valuation", "synthesis"}
    assert initial["reusable"] == []
    assert any("consumed identity: aapl:price-2024Q2" in g["reason"] for g in initial["gaps"])


@pytest.mark.parametrize("case", ["unsupported", "escape", "symlink", "duplicate", "incomplete-check", "missing-output", "ambiguous-reviews"])
def test_unsupported_folder_preserved(tmp_path, case):
    base, source, review = sample(tmp_path)
    if case == "unsupported":
        (tmp_path / "investing/research.json").unlink()
    elif case == "escape":
        source["raw_ref"] = "../outside"
        put(tmp_path, base + "/data/sources/price.json", source)
    elif case == "symlink":
        target = tmp_path / base / "data/sources"
        target.rename(target.with_name("real"))
        target.symlink_to(target.with_name("real"), target_is_directory=True)
    elif case == "duplicate":
        put(tmp_path, base + "/data/sources/duplicate.json", source)
    elif case in ("incomplete-check", "missing-output"):
        put(tmp_path, review + "/verification.json", dict(version=1, checks={}))
        if case == "missing-output":
            (tmp_path / review / "analysis.md").unlink()
        assert load().discover(tmp_path, "latest", CUTOFF)["reusable"] == []
        return
    elif case == "ambiguous-reviews":
        saved = json.loads((tmp_path / review / "review.json").read_text())
        saved["id"] = "r2"
        put(tmp_path, base + "/cycles/2024Q2/2024-08-31-r2/review.json", saved)
        result = load().discover(tmp_path, "latest", CUTOFF)
        assert result["status"] == "partial" and result["gaps"]
        assert result["reusable"] == []
        return
    before = (tmp_path / review / "analysis.md").read_bytes()
    with pytest.raises(ValueError):
        load().discover(tmp_path, "latest", CUTOFF)
    assert (tmp_path / review / "analysis.md").read_bytes() == before


@pytest.mark.parametrize("future", [False, True])
def test_new_quarter_and_changed_source(tmp_path, future):
    base, source, _ = sample(tmp_path)
    source["projection"]["value"] = True
    put(tmp_path, base + "/data/sources/price.json", source)
    quarter = dict(source, id="q3", kind="financial_original", identity="q3-original", available_at="2024-09-02" if future else "2024-08-02", fiscal=dict(year=2024, period="Q3", period_end="2024-06-29", original_accession="q3-original"))
    put(tmp_path, base + "/data/sources/q3.json", quarter)
    result = load().discover(tmp_path, "latest", CUTOFF)
    actions = {d["action"] for d in result["decisions"]}
    assert "append_revision_same_quarter" in actions
    new_work = {(d["record"], d["work"]) for d in result["decisions"]
                if d["action"] == "resume_incomplete_work"}
    assert new_work == (set() if future else {("aapl/2024Q3/new", "valuation")})
    if future:
        assert result["excluded"] == [dict(evidence="aapl:q3", reason="after_cutoff")]


@pytest.mark.parametrize("format_only", [False, True])
def test_unchanged_no_work(tmp_path, format_only):
    base, source, _ = sample(tmp_path)
    module = load()
    before = module.discover(tmp_path, "latest", CUTOFF)
    if format_only:
        (tmp_path / base / "data/sources/price.json").write_text(json.dumps(source, indent=4))
        (tmp_path / base / "data/price.txt").touch()
    assert module.discover(tmp_path, "latest", CUTOFF) == before
    assert {d["action"] for d in before["decisions"]} == {"no_analysis_update"}
    assert before["external_freshness"] == "unverified"
    future = dict(source, identity="future-price", available_at="2024-09-02", projection=dict(value=12, unit="USD", raw_text="raw"))
    put(tmp_path, base + "/data/sources/future.json", future)
    historical = module.discover(tmp_path, "historical", "2024-05-03T23:59:59+00:00")
    assert historical["reusable"] == before["reusable"]
    assert historical["excluded"]


@pytest.mark.parametrize("change", ["projection", "authorship", "version", "content", "missing"])
def test_local_analysis_dependencies_preserve_actual_authorship(tmp_path, change):
    base, _, review = sample(tmp_path)
    asset = json.loads((tmp_path / base / "asset.json").read_text())
    asset["questions"][0]["required_analysis"] = ["model"]
    asset["questions"] += [dict(id="synthesis", required_sources=[], depends_on=["valuation"]),
                           dict(id="independent", required_sources=[], depends_on=[])]
    put(tmp_path, base + "/asset.json", asset)
    content_ref = base + "/data/model.md"
    (tmp_path / content_ref).write_text("local method")
    identity = dict(kind="method", version="v1", authored_at="2026-11-16T10:00:00+08:00",
                    projection=dict(rate=1, unit="percent"), content_ref=content_ref,
                    content_digest=hashlib.sha256(b"local method").hexdigest())
    metadata = dict(identity, version=1, identity="v1", id="model")
    put(tmp_path, base + "/data/analysis/model.json", metadata)
    saved = json.loads((tmp_path / review / "review.json").read_text())
    saved["units"]["independent"] = dict(saved["units"]["valuation"])
    saved["units"]["synthesis"] = dict(saved["units"]["valuation"])
    saved["units"]["valuation"]["analysis_inputs"] = {"model": identity}
    put(tmp_path, review + "/review.json", saved)
    module = load()
    cutoff = "2024-05-03T23:59:59+00:00"
    before = module.discover(tmp_path, "historical", cutoff)
    assert {item["work"] for item in before["reusable"]} == {"valuation", "synthesis", "independent"}
    assert before["excluded"] == []
    if change == "missing":
        (tmp_path / base / "data/analysis/model.json").unlink()
    elif change == "content":
        (tmp_path / content_ref).write_text("changed method")
    else:
        key, value = {"projection": ("projection", dict(rate=True, unit="percent")),
                      "authorship": ("authored_at", "2026-11-16T11:00:00+08:00"),
                      "version": ("identity", "v2")}[change]
        metadata[key] = value
        put(tmp_path, base + "/data/analysis/model.json", metadata)
    after = module.discover(tmp_path, "historical", cutoff)
    assert {item["work"] for item in after["reusable"]} == {"independent"}
    assert {d["work"] for d in after["decisions"] if "recompute" in d["action"]} == {"valuation", "synthesis"}
    assert any(g["evidence"] == "analysis:model" for g in after["gaps"])


@pytest.mark.parametrize("case", ["templated-price", "missing-source"])
def test_required_economic_inputs_cannot_be_omitted_from_legacy_units(tmp_path, case):
    base, source, review = sample(tmp_path)
    asset = json.loads((tmp_path / base / "asset.json").read_text())
    saved = json.loads((tmp_path / review / "review.json").read_text())
    asset["questions"] += [dict(id="synthesis", required_sources=[], depends_on=["valuation"]),
                           dict(id="independent", required_sources=[], depends_on=[])]
    if case == "templated-price":
        source["id"] = "price-2024Q2"  # A price has no financial fiscal metadata.
        put(tmp_path, base + "/data/sources/price.json", source)
        saved["units"]["valuation"]["consumed"] = {source["id"]: dict(version=source["identity"], projection=source["projection"])}
        asset["questions"][0]["required_sources"] = ["price-{fiscal}"]
    else:
        asset["questions"][0]["required_sources"].append("market")
    saved["units"]["independent"] = dict(saved["units"]["valuation"])
    saved["units"]["synthesis"] = dict(saved["units"]["valuation"])
    if case == "templated-price":
        saved["units"]["valuation"]["consumed"] = {}
    put(tmp_path, base + "/asset.json", asset)
    put(tmp_path, review + "/review.json", saved)  # No frozen requirements in legacy records.
    result = load().discover(tmp_path, "latest", CUTOFF)
    assert {item["work"] for item in result["reusable"]} == {"independent"}
    assert {d["work"] for d in result["decisions"] if "recompute" in d["action"]} == {"valuation", "synthesis"}
    assert result["gaps"] and all(d["action"] != "no_analysis_update" for d in result["decisions"])


@pytest.mark.parametrize("mode", ["latest", "historical"])
def test_earlier_cutoff_ignores_valid_future_only_saved_quarters(tmp_path, mode):
    from test_research_continuation import two_issuers

    assets = two_issuers(tmp_path)
    before = {p: p.read_bytes() for p in tmp_path.rglob("*") if p.is_file()}
    result = load().discover(tmp_path, mode, "2024-05-01T23:59:59+00:00")
    assert result["gaps"] == []
    assert len(result["reusable"]) == 6
    assert {d["record"] for d in result["decisions"]} == {
        assets[0] + "/2024Q1/r1", assets[1] + "/2024Q3/r1"}
    assert {p: p.read_bytes() for p in tmp_path.rglob("*") if p.is_file()} == before


@pytest.mark.parametrize("state", ["empty", "interrupted", "withdrawn", "fiscal", "units", "consumed", "consumed-entry", "analysis-inputs", "edited-output", "ambiguous"])
def test_future_only_history_does_not_hide_real_gaps(tmp_path, state):
    from test_research_continuation import two_issuers

    assets = two_issuers(tmp_path)
    directory = "investing/assets/equities/" + assets[0] + "/cycles/2024Q2/2024-08-01-r1"
    saved = json.loads((tmp_path / directory / "review.json").read_text())
    if state == "empty":
        shutil.rmtree(tmp_path / directory)
    elif state == "interrupted":
        (tmp_path / directory / "review.json").unlink()
        put(tmp_path, directory + "/pending.json", dict(version=1, run="future-interrupted", review_digest="missing"))
    elif state == "withdrawn":
        put(tmp_path, directory + "/withdrawn.json", dict(version=1, run="missing-run"))
    elif state == "fiscal":
        saved["fiscal"]["period"] = "Q4"
        put(tmp_path, directory + "/review.json", saved)
    elif state == "units":
        saved["units"] = []
        put(tmp_path, directory + "/review.json", saved)
    elif state == "consumed":
        saved["units"]["credit"]["consumed"] = []
        put(tmp_path, directory + "/review.json", saved)
    elif state == "consumed-entry":
        saved["units"]["credit"]["consumed"] = {"filing-2024Q2": None}
        put(tmp_path, directory + "/review.json", saved)
    elif state == "analysis-inputs":
        saved["units"]["credit"]["analysis_inputs"] = []
        put(tmp_path, directory + "/review.json", saved)
    elif state == "edited-output":
        (tmp_path / directory / "credit.md").write_text("user-edited future output")
    elif state == "ambiguous":
        saved["id"] = "r2"
        put(tmp_path, directory.rsplit("/", 1)[0] + "/2024-08-01-r2/review.json", saved)
    result = load().discover(tmp_path, "latest", "2024-05-01T23:59:59+00:00")
    assert result["status"] == "partial"
    assert any("/cycles/2024Q2" in str(g["record"]) for g in result["gaps"])


def test_historical_does_not_fall_back_to_another_past_cutoff(tmp_path):
    from test_research_continuation import two_issuers

    two_issuers(tmp_path)
    result = load().discover(tmp_path, "historical", "2024-05-31T23:59:59+00:00")
    assert result["reusable"] == []
    assert any(g["record"].endswith("bank-fixture/cycles/2024Q1") for g in result["gaps"])


def test_future_only_directories_do_not_hide_absent_initial_fiscal_evidence(tmp_path):
    from test_research_continuation import two_issuers

    assets = two_issuers(tmp_path)
    for asset in assets:
        base = tmp_path / "investing/assets/equities" / asset
        for path in (base / "data/sources").glob("*.json"):
            source = json.loads(path.read_text())
            source["available_at"] = "2024-09-01"
            path.write_text(json.dumps(source))
        for path in (base / "cycles").glob("*/*/review.json"):
            saved = json.loads(path.read_text())
            saved["cutoff"] = "2024-09-01T23:59:59+00:00"
            path.write_text(json.dumps(saved))
    with_future = load().discover(tmp_path, "latest", "2024-05-31T23:59:59+00:00")
    for asset in assets:
        shutil.rmtree(tmp_path / "investing/assets/equities" / asset / "cycles")
    without_future = load().discover(tmp_path, "latest", "2024-05-31T23:59:59+00:00")
    for result in (with_future, without_future):
        assert result["status"] == "partial" and result["reusable"] == []
        assert result["decisions"] == []
        assert {g["record"] for g in result["gaps"] if g["evidence"] == "fiscal"} == set(assets)
