import hashlib
import importlib.util
import json
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
    assert ("create_next_quarter_analysis" in actions) is not future
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
