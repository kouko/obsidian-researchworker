import hashlib
import importlib.util
import io
import json
from pathlib import Path
import socket

import pytest

SCRIPT = Path(__file__).parents[1] / "scripts/assess_work.py"
SPEC = importlib.util.spec_from_file_location("assess_work", SCRIPT)
module = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(module)
CUTOFF = "2024-05-03T23:59:59+00:00"


def sample(root):
    (root / "output.md").write_text("checked")
    (root / "review.txt").write_text("Reviewed against supplied inputs")
    data = dict(version=1, sources=[], records=[dict(id="q2", issuer="AAPL",
        fiscal=dict(year=2024, period="Q2", period_end="2024-03-30", original_accession="original"),
        cutoff=CUTOFF, required_sources=[], work=[dict(id="forecast", status="complete",
        depends_on=[], consumed={}, output=dict(path="output.md", digest=hashlib.sha256(b"checked").hexdigest()),
        completion_evidence="review.txt")])])
    (root / "snapshot.json").write_text(json.dumps(data))
    return data


def invoke(root, **kwargs):
    out, err = io.StringIO(), io.StringIO()
    code = module.run(root, "snapshot.json", "latest", CUTOFF, stdout=out, stderr=err, **kwargs)
    return code, json.loads(out.getvalue()) if out.getvalue() else None, err.getvalue()


def test_explicit_gaps(tmp_path):
    data = sample(tmp_path)
    data["records"][0]["required_sources"] = ["missing"]
    (tmp_path / "snapshot.json").write_text(json.dumps(data))
    code, result, _ = invoke(tmp_path)
    assert code == 2 and result["gaps"][0]["recovery"]
    assert all(d["action"] != "no_analysis_update" for d in result["decisions"])
    (tmp_path / "output.md").write_text("changed")
    assert invoke(tmp_path)[1]["reusable"] == []


@pytest.mark.parametrize("case", ["absolute", "escape", "symlink", "malformed", "version", "nested-type", "bool-version"])
def test_invalid_input_and_escape(tmp_path, case):
    data = sample(tmp_path)
    if case in ("absolute", "escape", "symlink"):
        outside = tmp_path.parent / "outside.txt"
        outside.write_text("must not read")
        (tmp_path / "link").symlink_to(outside)
        data["records"][0]["work"][0]["output"]["path"] = {
            "absolute": str(outside), "escape": "../outside.txt", "symlink": "link"}[case]
    elif case == "version":
        data["version"] = 2
    elif case == "bool-version":
        data["version"] = True
    elif case == "nested-type":
        data["records"][0]["work"][0]["consumed"] = []
    (tmp_path / "snapshot.json").write_text("[" if case == "malformed" else json.dumps(data))
    code, result, error = invoke(tmp_path)
    assert code == 1 and result is None and "retry" in error
    if case in ("absolute", "escape", "symlink"):
        assert "Reference outside assessment root" in error


def test_deterministic_readonly(tmp_path):
    sample(tmp_path)
    before = {p.name: p.read_bytes() for p in tmp_path.iterdir()}
    first = invoke(tmp_path)
    assert first[0] == 0 and first[1]["reusable"]
    assert invoke(tmp_path) == first
    assert {p.name: p.read_bytes() for p in tmp_path.iterdir()} == before


def test_interrupted_retry(tmp_path, monkeypatch):
    sample(tmp_path)
    before = (tmp_path / "snapshot.json").read_bytes()
    original = module.assess
    with monkeypatch.context() as patch:
        patch.setattr(module, "assess", lambda *args: (_ for _ in ()).throw(KeyboardInterrupt()))
        with pytest.raises(KeyboardInterrupt):
            invoke(tmp_path)
    assert module.assess is original and invoke(tmp_path)[0] == 0
    assert (tmp_path / "snapshot.json").read_bytes() == before


def test_independent_cli(tmp_path, capsys):
    sample(tmp_path)
    assert module.main(["--root", str(tmp_path), "--snapshot", "snapshot.json", "--mode", "latest", "--cutoff", CUTOFF]) == 0
    assert json.loads(capsys.readouterr().out)["external_freshness"] == "unverified"
    assert module.main(["--root", str(tmp_path)]) == 64
    assert "Invalid assessment request" in capsys.readouterr().err


def test_no_external_access(tmp_path, monkeypatch):
    sample(tmp_path)
    monkeypatch.setattr(socket, "socket", lambda *a, **k: pytest.fail("network access"))
    assert invoke(tmp_path)[0] == 0
    out, err = io.StringIO(), io.StringIO()
    assert module.run(tmp_path, "snapshot.json", "latest", "bad", stdout=out, stderr=err) == 64
    assert not out.getvalue() and "cutoff" in err.getvalue()
