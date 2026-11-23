"""Every per-type Mermaid file's examples render in Obsidian 1.15 (Pele) and
the unsupported types stay out of the skill."""

import re
import shutil
import subprocess
from pathlib import Path

import pytest

SKILL = Path(__file__).resolve().parents[1] / "skills" / "obsidian-mermaid-visualizer"
CATEGORIES = ["flow", "data-viz", "structural", "time"]
NEW_TYPES = [
    "venn", "treemap", "radar", "sankey", "kanban", "journey", "ishikawa",
    "treeview", "swimlane", "wardley", "usecase", "packet", "requirement",
]
TYPE_FILES = sorted(p for c in CATEGORIES for p in (SKILL / c).glob("*.md"))


@pytest.mark.skipif(
    shutil.which("node") is None or shutil.which("npm") is None,
    reason="node/npm unavailable: the Pele validator cannot run",
)
def test_every_type_example_passes_validator():
    stems = {p.stem.lower() for p in TYPE_FILES}
    assert set(NEW_TYPES) <= stems, sorted(set(NEW_TYPES) - stems)
    failures = []
    for path in TYPE_FILES:
        r = subprocess.run(
            ["bash", str(SKILL / "scripts" / "validate.sh"), str(path)],
            capture_output=True, text=True, timeout=300,
        )
        if r.returncode != 0 or "PASS" not in r.stdout:
            failures.append(f"{path.relative_to(SKILL)}: {r.stdout}{r.stderr}")
    assert not failures, "\n".join(failures)
    assert not (SKILL / "scripts" / "node_modules").exists(), "install must live outside the skill"


def test_excluded_types_absent():
    for path in TYPE_FILES:
        text = path.read_text(encoding="utf-8")
        assert not re.search(r"eventmodeling|cynefin", text, re.I), path
        assert not re.search(r"```mermaid\s*\n[^`]*candlestick", text), path
        assert not re.search(r"11\.4\.1", text), path
    skill = (SKILL / "SKILL.md").read_text(encoding="utf-8")
    assert re.search(r"[Cc]andlestick[^\n]*not supported", skill)
