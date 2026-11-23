# concern: validator silently passes (exit 0) broken diagrams written in fence forms Obsidian renders, or fails diagrams Obsidian shows as literal code
"""Adversarial probe: validate.sh must see every mermaid block Obsidian renders, and only those."""

import shutil
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[5]
VALIDATE = ROOT / "obsidian" / "skills" / "obsidian-mermaid-visualizer" / "scripts" / "validate.sh"
BROKEN = "flowchart LR\n  A[Call API (v2)] --> B"

pytestmark = pytest.mark.skipif(
    shutil.which("node") is None or shutil.which("npm") is None,
    reason="node/npm unavailable: the Pele validator cannot run",
)


def _run(tmp_path, text):
    note = tmp_path / "note 中文.md"
    note.write_text(text, encoding="utf-8")
    return subprocess.run(["bash", str(VALIDATE), str(note)], capture_output=True, text=True, timeout=300)


def test_validator_tildefence_reportsfail(tmp_path):
    """A broken diagram in a ~~~mermaid fence (rendered by Obsidian) must be reported as FAIL."""
    r = _run(tmp_path, f"~~~mermaid\n{BROKEN}\n~~~\n")
    assert r.returncode == 1, r.stdout + r.stderr


def test_validator_calloutfence_reportsfail(tmp_path):
    """A broken diagram inside a callout (> ```mermaid) must be reported as FAIL."""
    body = "\n".join("> " + line for line in BROKEN.splitlines())
    r = _run(tmp_path, f"> [!note]\n> ```mermaid\n{body}\n> ```\n")
    assert r.returncode == 1, r.stdout + r.stderr


def test_validator_unterminatedfence_reportsfail(tmp_path):
    """A broken diagram whose fence runs to end of file (Obsidian still renders it) must be reported as FAIL."""
    r = _run(tmp_path, f"# note\n\n```mermaid\n{BROKEN}\n")
    assert r.returncode == 1, r.stdout + r.stderr


def test_validator_nestedinfourbacktick_ignoresinner(tmp_path):
    """A ```mermaid line inside a ````markdown fence is literal code in Obsidian and must not be validated."""
    r = _run(tmp_path, "````markdown\n```mermaid\n<diagram code>\n```\n````\n")
    assert r.returncode == 0, r.stdout + r.stderr
