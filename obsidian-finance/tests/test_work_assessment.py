import copy
import hashlib
import importlib.util
from pathlib import Path

import pytest

SPEC = importlib.util.spec_from_file_location(
    "work_assessment", Path(__file__).parents[1] / "scripts/work_assessment.py"
)
module = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(module)
assess = module.assess


def snapshot():
    source = dict(id="price", issuer="issuer", kind="price", version="v1",
                  projection={"value": 10, "unit": "USD"},
                  available_at="2024-05-03", consumers=["valuation"])
    item = dict(id="valuation", status="complete", depends_on=[],
                consumed={"price": {k: copy.deepcopy(source[k]) for k in ("version", "projection")}},
                output={"content": "checked", "digest": hashlib.sha256(b"checked").hexdigest()},
                completion_evidence="review-1")
    return {"version": 1, "sources": [source], "records": [dict(
        id="q2", issuer="issuer", fiscal={"year": 2024, "period": "Q2",
        "period_end": "2024-03-30", "original_accession": "original-q2"},
        cutoff="2024-05-03T23:59:59+00:00", required_sources=["price"],
        work=[item])]}


def run(data, mode="latest", cutoff="2024-08-31T23:59:59+00:00"):
    return assess(data, mode, cutoff)


def actions(result):
    return {d["action"] for d in result["decisions"]}


def test_work_classes():
    data = snapshot()
    assert actions(run(data)) == {"no_analysis_update"}
    data["records"][0]["work"].append(dict(id="synthesis", status="missing", depends_on=["valuation"], consumed={}))
    result = run(data)
    assert "resume_incomplete_work" in actions(result)
    assert result["reusable"] == [{"record": "q2", "work": "valuation"}]
    assert all(d["reason"] and d["evidence"] for d in result["decisions"])
    assert result["external_freshness"] == "unverified"


def test_independent_gaps():
    data = snapshot()
    data["records"][0]["required_sources"] += ["consensus", "peers"]
    result = run(data)
    assert {g["evidence"] for g in result["gaps"]} == {"consensus", "peers"}
    assert "no_analysis_update" not in actions(result)
    assert all(g["recovery"] for g in result["gaps"])
    data = snapshot()
    data["records"][0]["work"] = []
    assert "no_analysis_update" not in actions(run(data))


def test_relevant_change():
    data = snapshot()
    data["sources"][0]["projection"]["value"] = 11
    # Saved consumption is independent of current source values.
    data["records"][0]["work"][0]["consumed"]["price"]["projection"] = {"value": 10, "unit": "USD"}
    result = run(data)
    assert "append_revision_same_quarter" in actions(result)
    assert result["reusable"] == []
    assert result["decisions"][0]["affected"] == ["valuation"]
    data = snapshot()
    data["sources"][0]["projection"] = {"nested": [{"value": True}]}
    data["records"][0]["work"][0]["consumed"]["price"]["projection"] = {"nested": [{"value": 1}]}
    assert run(data)["reusable"] == []
    data["sources"][0]["projection"] = {"nested": [{"value": 1.0}]}
    assert actions(run(data)) == {"no_analysis_update"}


def test_timestamp_only():
    data = snapshot()
    before = run(data)
    data["sources"][0].update(mtime="later", fetched_at="later", vendor_metadata="new")
    assert run(data) == before


def test_new_quarter():
    data = snapshot()
    data["sources"].append(dict(id="q3", issuer="issuer", kind="financial_original",
        version="q3-original", projection={"revenue": 20}, available_at="2024-08-02",
        fiscal=dict(year=2024, period="Q3", period_end="2024-06-29", original_accession="q3-original")))
    result = run(data)
    assert "create_next_quarter_analysis" in actions(result)
    represented = copy.deepcopy(data["records"][0])
    represented.update(id="q3-record", fiscal=copy.deepcopy(data["sources"][-1]["fiscal"]))
    data["records"].append(represented)
    assert "create_next_quarter_analysis" not in actions(run(data))
    represented["work"][0]["status"] = "missing"
    assert "create_next_quarter_analysis" not in actions(run(data))
    assert "resume_incomplete_work" in actions(run(data))
    data["records"].pop()
    older = copy.deepcopy(data["records"][0])
    older.update(id="q1", fiscal=dict(year=2024, period="Q1", period_end="2023-12-30", original_accession="q1-original"))
    data["records"].append(older)
    duplicate = copy.deepcopy(data["sources"][-1])
    duplicate["id"] = "q3-copy"
    data["sources"].append(duplicate)
    proposals = [d for d in run(data)["decisions"] if d["action"] == "create_next_quarter_analysis"]
    assert len(proposals) == 1
    assert proposals[0]["evidence"] == ["q3", "q3-copy"]
    data["records"].pop()
    data["sources"].pop()
    data["sources"][-1]["fiscal"]["period_end"] = "2024-12-31"
    assert "create_next_quarter_analysis" not in actions(run(data))
    data["sources"][-1]["fiscal"]["period_end"] = "2024-06-29"
    data["sources"][-1]["fiscal"].pop("original_accession")
    assert "create_next_quarter_analysis" not in actions(run(data))
    assert run(data)["gaps"]

    data["sources"][-1]["fiscal"]["original_accession"] = "  \t"
    assert "create_next_quarter_analysis" not in actions(run(data))
    assert run(data)["gaps"]


def test_historical_exclusion():
    data = snapshot()
    data["sources"][0]["available_at"] = "2024-05-06"
    result = run(data, "historical", "2024-05-03T23:59:59+00:00")
    assert result["excluded"] == [{"evidence": "price", "reason": "after_cutoff"}]
    assert result["gaps"]
    data["sources"][0]["available_at"] = None
    assert run(data)["excluded"][0]["reason"] == "unverified_availability"
    data["records"][0]["required_sources"] = []
    data["records"][0]["work"][0]["consumed"] = {}
    assert run(data)["gaps"]
    data = snapshot()
    data["sources"][0]["available_at"] = "2024-05-03"
    assert run(data, "latest", "2024-05-03T12:00:00+00:00")["gaps"]
    with pytest.raises(ValueError, match="historical cutoff"):
        run(data, "historical")


def test_valid_checkpoint():
    data = snapshot()
    data["records"][0]["work"] += [dict(id="synthesis", status="missing", depends_on=["valuation"], consumed={})]
    original = copy.deepcopy(data)
    result = run(data)
    assert result["reusable"] == [{"record": "q2", "work": "valuation"}]
    assert result == run(data)
    assert data == original


def test_invalid_checkpoint():
    data = snapshot()
    data["records"][0]["work"][0]["output"] = {"path": "valuation.md"}
    data["records"][0]["work"].append(dict(id="synthesis", status="complete", depends_on=["valuation"], consumed={}))
    result = run(data)
    assert result["reusable"] == []
    assert {d["work"] for d in result["decisions"]} == {None, "valuation", "synthesis"}
    assert "invalidate_dependent_checkpoint_and_recompute" in actions(result)
    assert result["gaps"]
