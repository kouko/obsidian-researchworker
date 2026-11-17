"""Adversarial probe: the Codex-facing plugin metadata was left at 4.1.0 /
"14 skills" while the Claude-facing metadata and CHANGELOG moved to 4.2.0 /
15 skills and advertise the vault search, so the two entry points disagree on
the version and on whether the new capability exists.

# concern: the renamed skill and the 4.2.0 version bump miss the Codex plugin
# manifest, which still advertises the pre-rename 14-skill plugin.
"""

import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[5]
OBSIDIAN = REPO_ROOT / "obsidian"

CLAUDE_PLUGIN = OBSIDIAN / ".claude-plugin/plugin.json"
CODEX_PLUGIN = OBSIDIAN / ".codex-plugin/plugin.json"
CHANGELOG = OBSIDIAN / "CHANGELOG.md"


def test_codex_plugin_metadata_matches_claude_plugin_and_changelog():
    """Version and skill count must agree across every shipped manifest."""
    claude = json.loads(CLAUDE_PLUGIN.read_text())
    codex = json.loads(CODEX_PLUGIN.read_text())
    assert codex["version"] == claude["version"], (
        f"codex {codex['version']} != claude {claude['version']}")
    assert codex["description"] == claude["description"], (
        "codex description diverges from the claude-plugin description")
    # The changelog's newest entry is the version both manifests carry.
    head = CHANGELOG.read_text().splitlines()
    latest = next(l for l in head if l.startswith("## ["))
    version = latest.split("]")[0].split("[")[1]
    assert codex["version"] == version, (
        f"codex {codex['version']} != changelog {version}")
    # The renamed skill must appear in the codex long description too.
    long_desc = codex["interface"]["longDescription"]
    assert "obsidian-knowledge" in long_desc, (
        "codex longDescription still describes the pre-rename skill set")
