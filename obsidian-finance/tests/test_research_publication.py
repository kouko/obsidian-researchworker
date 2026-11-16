import copy
import hashlib
import json

import pytest

from test_research_store import CUTOFF, load, put, sample


def proposal(root):
    base, _, old = sample(root)
    saved = json.loads((root / old / "review.json").read_text())
    saved.update(id="r2", predecessor="r1", cutoff=CUTOFF,
                 research=dict(method="Applied scenario method v1", assumptions=["Constant currency"],
                    changes="Same-quarter evidence review", gaps=[],
                    horizons={h: dict(judgment="insufficient_evidence", evidence=["price"],
                        invalidation_triggers=["New financial disclosure"])
                        for h in ("short", "medium", "long")}))
    return base, old, saved


def test_completed_unit_reused_and_linked_provenance(tmp_path):
    base, old, saved = proposal(tmp_path)
    module = load()
    before = {p.relative_to(tmp_path): p.read_bytes() for p in tmp_path.rglob("*") if p.is_file()}
    result = module.publish(tmp_path, "aapl", saved, {}, module.publication_snapshot(tmp_path), "run1")
    assert result["status"] == "complete"
    completed = json.loads((tmp_path / result["review"]).read_text())
    assert completed["units"]["valuation"]["output"]["path"] == old + "/analysis.md"
    assert completed["predecessor"] == "r1" and completed["research"] == saved["research"]
    assert completed["provenance"][base + "/data/sources/price.json"]["raw_digest"]
    assert all((tmp_path / p).read_bytes() == content for p, content in before.items())
    assert module.discover(tmp_path, "latest", CUTOFF)["reusable"] == [dict(record="aapl/2024Q2/r2", work="valuation")]
    assert module.recover(tmp_path, "run1", action="rollback")["status"] == "rolled_back"
    assert module.discover(tmp_path, "latest", CUTOFF)["reusable"] == [dict(record="aapl/2024Q2/r1", work="valuation")]
    assert (tmp_path / result["review"]).is_file()  # History survives withdrawal.
    asset = json.loads((tmp_path / base / "asset.json").read_text())
    asset["questions"].append(dict(id="synthesis", required_sources=[], depends_on=["valuation"]))
    put(tmp_path, base + "/asset.json", asset)
    saved.update(id="r3")
    checkpoint = module.publish(tmp_path, "aapl", saved, {}, module.publication_snapshot(tmp_path), "run2", complete=False)
    result = module.discover(tmp_path, "latest", CUTOFF)
    assert checkpoint["status"] == "checkpoint"
    assert result["reusable"] == [dict(record="aapl/2024Q2/r3", work="valuation")]
    assert any(d["work"] == "synthesis" and d["action"] == "resume_incomplete_work" for d in result["decisions"])


@pytest.mark.parametrize("change", ["economic", "method", "assumption", "requirements"])
def test_transitive_input_change_rejects_old_units(tmp_path, change):
    base, old, saved = proposal(tmp_path)
    asset = json.loads((tmp_path / base / "asset.json").read_text())
    asset["questions"].append(dict(id="synthesis", required_sources=[], depends_on=["valuation"]))
    saved["units"]["synthesis"] = copy.deepcopy(saved["units"]["valuation"])
    saved["units"]["synthesis"]["consumed"] = {}
    if change == "requirements":
        put(tmp_path, base + "/asset.json", asset)
        module = load()
        module.publish(tmp_path, "aapl", saved, {}, module.publication_snapshot(tmp_path), "run1")
        asset["questions"][1]["depends_on"] = []
        put(tmp_path, base + "/asset.json", asset)
        result = module.discover(tmp_path, "latest", CUTOFF)
        assert {item["work"] for item in result["reusable"]} == {"valuation"}
        return
    if change == "economic":
        source = json.loads((tmp_path / base / "data/sources/price.json").read_text())
        source["projection"]["value"] = 11
        put(tmp_path, base + "/data/sources/price.json", source)
    else:
        asset["questions"][0]["required_analysis"] = ["model"]
        ref = base + "/data/model.md"
        (tmp_path / ref).write_text("new local analysis")
        frozen = dict(kind=change, version="v1", authored_at="2026-11-16T10:00:00+08:00",
                      projection={}, content_ref=ref, content_digest=hashlib.sha256(b"new local analysis").hexdigest())
        saved["units"]["valuation"]["analysis_inputs"] = {"model": frozen}
        put(tmp_path, base + "/data/analysis/model.json", dict(frozen, version=1, identity="v2", id="model"))
    put(tmp_path, base + "/asset.json", asset)
    module = load()
    with pytest.raises(ValueError, match="incomplete|dependencies"):
        module.publish(tmp_path, "aapl", saved, {}, module.publication_snapshot(tmp_path), "run1")
    assert module.discover(tmp_path, "latest", CUTOFF)["reusable"] != [dict(record="aapl/2024Q2/r2", work="valuation")]
    assert (tmp_path / old / "analysis.md").read_text() == "analysis"


@pytest.mark.parametrize("missing", ["horizons", "method", "assumptions", "verification", "source", "last-success"])
def test_incomplete_envelope_rejected(tmp_path, missing):
    base, old, saved = proposal(tmp_path)
    if missing in saved["research"]:
        del saved["research"][missing]
    elif missing == "verification":
        del saved["units"]["valuation"]["verification"]
    elif missing == "last-success":
        saved["last_success"] = CUTOFF
    else:
        saved["units"]["valuation"]["consumed"] = {}
    module = load()
    with pytest.raises(ValueError):
        module.publish(tmp_path, "aapl", saved, {}, module.publication_snapshot(tmp_path), "run1")
    assert {r["record"] for r in module.discover(tmp_path, "latest", CUTOFF)["reusable"]} == {"aapl/2024Q2/r1"}
    if missing != "last-success":
        assert any(g["evidence"] == "publication:run1" for g in module.discover(tmp_path, "latest", CUTOFF)["gaps"])


@pytest.mark.parametrize("finish", ["resume", "rollback"])
def test_interrupted_publication_recovers(tmp_path, monkeypatch, finish):
    _, old, saved = proposal(tmp_path)
    module = load()
    target = "investing/assets/equities/aapl/cycles/2024Q2/2024-08-31-r2"
    content = "Revised analysis with bounded evidence"
    digest = hashlib.sha256(content.encode()).hexdigest()
    saved["units"]["valuation"].update(output=dict(path=target + "/analysis.md", digest=digest), verification=target + "/check.json")
    files = {"analysis.md": content, "check.json": json.dumps(dict(version=1, output_digest=digest,
        checks={k: True for k in ("sources", "citations", "calculations", "counterevidence")}, unresolved=[]))}
    original = module._write_new
    def interrupt(root, path, data):
        if path == target + "/review.json":
            raise OSError("simulated interruption before completion")
        return original(root, path, data)
    monkeypatch.setattr(module, "_write_new", interrupt)
    with pytest.raises(OSError, match="interruption"):
        module.publish(tmp_path, "aapl", saved, files, module.publication_snapshot(tmp_path), "run1")
    assert {r["record"] for r in module.discover(tmp_path, "latest", CUTOFF)["reusable"]} == {"aapl/2024Q2/r1"}
    monkeypatch.setattr(module, "_write_new", original)
    if finish == "rollback":
        assert module.recover(tmp_path, "run1", action="rollback")["status"] == "rolled_back"
        assert module.discover(tmp_path, "latest", CUTOFF)["reusable"] == [dict(record="aapl/2024Q2/r1", work="valuation")]
        assert (tmp_path / target / "analysis.md").read_text() == content
        return
    result = module.recover(tmp_path, "run1")
    assert result["status"] == "complete"
    assert module.recover(tmp_path, "run1") == result
    assert (tmp_path / old / "analysis.md").read_text() == "analysis"
    assert module.discover(tmp_path, "latest", CUTOFF)["reusable"] == [dict(record="aapl/2024Q2/r2", work="valuation")]


@pytest.mark.parametrize("conflict", ["old-output", "source", "symlink", "draft", "published-edit", "withdrawn-edit", "marker-edit", "partial-completion", "recovery-symlink", "run-race"])
def test_user_edit_and_symlink_preserved(tmp_path, monkeypatch, conflict):
    base, old, saved = proposal(tmp_path)
    module = load()
    expected = module.publication_snapshot(tmp_path)
    if conflict == "old-output":
        (tmp_path / old / "analysis.md").write_text("user analysis")
    elif conflict == "source":
        (tmp_path / base / "data/price.txt").write_text("user source")
    elif conflict == "symlink":
        (tmp_path / base / "cycles").rename(tmp_path / "real-cycles")
        (tmp_path / base / "cycles").symlink_to(tmp_path / "real-cycles", target_is_directory=True)
    elif conflict == "run-race":
        original_mkdir = module.os.mkdir
        raced = False
        def collision(name, *args, **kwargs):
            nonlocal raced
            if name == "run1" and not raced:
                raced = True
                original_mkdir(name, *args, **kwargs)
            return original_mkdir(name, *args, **kwargs)
        monkeypatch.setattr(module.os, "mkdir", collision)
    elif conflict in ("published-edit", "withdrawn-edit", "marker-edit"):
        result = module.publish(tmp_path, "aapl", saved, {}, expected, "run1")
        if conflict in ("withdrawn-edit", "marker-edit"):
            module.recover(tmp_path, "run1", action="rollback")
        if conflict == "marker-edit":
            put(tmp_path, str((tmp_path / result["review"]).parent.relative_to(tmp_path)) + "/withdrawn.json", dict(version=1, run="run1", files={}))
            assert module.discover(tmp_path, "latest", CUTOFF)["status"] == "partial"
        else:
            (tmp_path / result["review"]).write_text("user edited published review")
    else:
        original = module._write_new
        def interrupt(root, path, data):
            if path.endswith("/review.json"):
                raise OSError("interrupted")
            return original(root, path, data)
        monkeypatch.setattr(module, "_write_new", interrupt)
        with pytest.raises(OSError):
            module.publish(tmp_path, "aapl", saved, {}, expected, "run1")
        monkeypatch.setattr(module, "_write_new", original)
        if conflict == "draft":
            (tmp_path / "investing/.research-runs/run1/request.json").write_text("user draft")
        elif conflict == "partial-completion":
            target = tmp_path / base / "cycles/2024Q2/2024-08-31-r2/review.json"
            target.write_text('{"version":1,')
            result = module.discover(tmp_path, "latest", CUTOFF)
            assert result["reusable"] == [dict(record="aapl/2024Q2/r1", work="valuation")]
            assert result["status"] == "partial" and result["gaps"]
        else:
            target = tmp_path / "investing/.research-runs/run1/draft"
            target.rename(tmp_path / "draft-backup")
            target.symlink_to(tmp_path / "draft-backup", target_is_directory=True)
    before = {p: p.read_bytes() for p in tmp_path.rglob("*") if p.is_file() and not p.is_symlink()}
    with pytest.raises(ValueError):
        if conflict in ("draft", "published-edit", "withdrawn-edit", "marker-edit", "partial-completion", "recovery-symlink"):
            module.recover(tmp_path, "run1", action="rollback")
        else:
            module.publish(tmp_path, "aapl", saved, {}, expected, "run1")
    assert all(p.read_bytes() == value for p, value in before.items())
