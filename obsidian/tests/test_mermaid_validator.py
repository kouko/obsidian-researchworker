"""Pele-based Mermaid validator (validate.sh -> validate.mjs) gives Obsidian 1.15's verdict."""

import shutil
import subprocess
from pathlib import Path

import pytest

SCRIPTS = Path(__file__).resolve().parents[1] / "skills" / "obsidian-mermaid-visualizer" / "scripts"
VALIDATE = SCRIPTS / "validate.sh"

pytestmark = pytest.mark.skipif(
    shutil.which("node") is None or shutil.which("npm") is None,
    reason="node/npm unavailable: the Pele validator cannot run, so its verdicts are untested",
)


def _run(tmp_path, diagrams):
    note = tmp_path / "note.md"
    note.write_text(
        "# note\n\n" + "\n".join(f"```mermaid\n{d}\n```\n" for d in diagrams), encoding="utf-8"
    )
    return subprocess.run(
        ["bash", str(VALIDATE), str(note)], capture_output=True, text=True, timeout=300
    )


@pytest.mark.parametrize(
    "src",
    [
        'flowchart TD\n A["Call API (v2)"] --> B',
        "flowchart TD\n A[1. 知覺] --> B[中文]",
        'pie\n "a" : 1',
    ],
)
def test_renders_ok_samples_pass(tmp_path, src):
    r = _run(tmp_path, [src])
    assert r.returncode == 0, r.stdout + r.stderr
    assert "PASS  block 1" in r.stdout


@pytest.mark.parametrize(
    "src",
    [
        "flowchart TD\n A[Call API (v2)] --> B",
        "timeline\n 9:00 : x",
        "gitGraph\n commit\n branch 開發",
    ],
)
def test_pele_rejected_samples_fail(tmp_path, src):
    r = _run(tmp_path, ['pie\n "ok" : 1', src])
    assert r.returncode == 1, r.stdout + r.stderr
    assert "PASS  block 1" in r.stdout
    assert "FAIL  block 2" in r.stdout


BROKEN = "flowchart TD\n A[Call API (v2)] --> B"


@pytest.mark.parametrize(
    "text,code",
    [
        (f"~~~mermaid\n{BROKEN}\n~~~\n", 1),
        ("> [!note]\n> > ```mermaid\n" + "".join(f"> > {l}\n" for l in BROKEN.splitlines()) + "> > ```\n", 1),
        (f"```mermaid\n{BROKEN}\n", 1),
        (f"````markdown\n```mermaid\n{BROKEN}\n```\n````\n", 0),
        (f"    ```mermaid\n    {BROKEN}\n    ```\n", 0),
    ],
    ids=["tilde", "nested-callout", "unclosed", "inside-outer-fence", "indented-code"],
)
def test_fence_forms_follow_obsidian(tmp_path, text, code):
    note = tmp_path / "note.md"
    note.write_text(text, encoding="utf-8")
    r = subprocess.run(["bash", str(VALIDATE), str(note)], capture_output=True, text=True, timeout=300)
    assert r.returncode == code, r.stdout + r.stderr
