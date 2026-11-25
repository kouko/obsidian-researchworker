# concern: skill text presents a fenced mermaid example as safe/recommended but it fails to render in Obsidian 1.15 (Pele)
"""Adversarial probe: every ```mermaid example the skill recommends must render under Pele 1.13.0."""

import shutil
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
SKILL = ROOT / "obsidian" / "skills" / "obsidian-mermaid-visualizer"
VALIDATE = SKILL / "scripts" / "validate.sh"

pytestmark = pytest.mark.skipif(
    shutil.which("node") is None or shutil.which("npm") is None,
    reason="node/npm unavailable: the Pele validator cannot run",
)


@pytest.mark.parametrize("rel", ["obsidian-common-quirks.md", "structural/gitgraph.md"])
def test_skillexamples_recommendedblocks_render(rel):
    """Each ```mermaid block in the file renders (validate.sh exit 0, no FAIL line)."""
    r = subprocess.run(["bash", str(VALIDATE), str(SKILL / rel)], capture_output=True, text=True, timeout=300)
    assert "FAIL" not in r.stdout and r.returncode == 0, r.stdout + r.stderr


def test_skillexamples_skillmdstyleexample_renders(tmp_path):
    """The SKILL.md palette 'Example:' mermaid block renders on its own (not a bare fragment)."""
    lines = (SKILL / "SKILL.md").read_text(encoding="utf-8").splitlines()
    i = lines.index("Example:")
    assert lines[i + 1] == "```mermaid"
    end = lines.index("```", i + 2)
    note = tmp_path / "ex.md"
    note.write_text("\n".join(lines[i + 1 : end + 1]) + "\n", encoding="utf-8")
    r = subprocess.run(["bash", str(VALIDATE), str(note)], capture_output=True, text=True, timeout=300)
    assert r.returncode == 0, r.stdout + r.stderr
