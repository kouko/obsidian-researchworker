# concern: stale skill identifiers and changes to historical records
"""Ownership guard for the obsidian-canvas rename of plugin-level docs
(loom change 2026-10-06-rename-canvas-skill, task W2-01, acceptance A2/A5).

W1-01 renamed the skill directory and W1-02 the per-skill cross-references.
What these tests check (and only this): the plugin-root and skill-index
documentation — the three plugin READMEs, the three skills/READMEs,
ATTRIBUTION.md and the CHANGELOG's new entry — name the renamed skill
`obsidian-canvas` and no longer carry the old id, while the CHANGELOG's
new entry and its historical entries record the rename / the old name by
design. Monkey-only plans, dogfood reports and worktrees were not transferred,
so this guard checks the retained documentation without migration-only history
fixtures or restrictions on this repository's evolving plans and worktrees.

Per-skill READMEs, the router, the obsidian-research reference and the
skill's own SKILL.md belong to W1-01/W1-02; test-path updates belong to
W2-02 — deliberately out of scope here.
"""

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
OBSIDIAN = REPO_ROOT / "obsidian"

PLUGIN_README_FILES = [
    OBSIDIAN / "README.md",
    OBSIDIAN / "README.ja.md",
    OBSIDIAN / "README.zh-TW.md",
]
SKILL_INDEX_FILES = [
    OBSIDIAN / "skills" / "README.md",
    OBSIDIAN / "skills" / "README.ja.md",
    OBSIDIAN / "skills" / "README.zh-TW.md",
]
ATTRIBUTION = REPO_ROOT / "ATTRIBUTION.md"
CHANGELOG = OBSIDIAN / "CHANGELOG.md"

OLD_ID = "obsidian-canvas-creator"
NEW_ID = "obsidian-canvas"
# The exact table-cell spellings, so the assertion cannot pass on the old id
# (which contains NEW_ID as a substring).
PLUGIN_TABLE_CELL = f"| `{NEW_ID}` |"      # backticked, e.g. `obsidian-canvas`
INDEX_TABLE_CELL = f"| {NEW_ID} |"         # bare, e.g. | obsidian-canvas |
TREE_LINE = f"{NEW_ID}/ #"                  # repository-structure tree entry
ATTRIBUTION_PATH = f"obsidian/skills/{NEW_ID}/"
NEW_CHANGELOG_HEADING = (
    f"## [3.24.0] — 2026-10-06 rename {OLD_ID} skill to {NEW_ID}"
)


def test_plugin_docs_use_new_name():
    """A2 positive: the six READMEs and ATTRIBUTION.md point at obsidian-canvas."""
    for readme in PLUGIN_README_FILES:
        text = readme.read_text(encoding="utf-8")
        assert PLUGIN_TABLE_CELL in text, (
            f"{readme.name} skill table row must be `` | `{NEW_ID}` | ``"
        )
        assert TREE_LINE in text, (
            f"{readme.name} repository tree must list `{NEW_ID}/`"
        )
    for readme in SKILL_INDEX_FILES:
        text = readme.read_text(encoding="utf-8")
        assert INDEX_TABLE_CELL in text, (
            f"{readme.name} attribution table row must be `| {NEW_ID} |`"
        )
    attribution = ATTRIBUTION.read_text(encoding="utf-8")
    assert ATTRIBUTION_PATH in attribution, (
        f"ATTRIBUTION.md must list `{ATTRIBUTION_PATH}`"
    )
    # The license file moved with the directory; the row's link follows it.
    assert f"[LICENSE]({ATTRIBUTION_PATH}LICENSE)" in attribution, (
        "ATTRIBUTION.md license link must resolve under the renamed path"
    )
    # MIT attribution and license cell survive the rename unchanged.
    assert "License: MIT, Copyright (c) 2025 Axton Liu" in attribution


def test_stale_name_absent_from_live_docs():
    """A2 negative: no live doc outside CHANGELOG carries the old id."""
    for readme in [*PLUGIN_README_FILES, *SKILL_INDEX_FILES]:
        text = readme.read_text(encoding="utf-8")
        assert OLD_ID not in text, (
            f"{readme.name} still names {OLD_ID}"
        )
    assert OLD_ID not in ATTRIBUTION.read_text(encoding="utf-8"), (
        f"ATTRIBUTION.md still names {OLD_ID}"
    )
    # The rename entry and older history may contain the old id; newer
    # entries above it must not.
    changelog = CHANGELOG.read_text(encoding="utf-8").splitlines()
    heading_line = changelog.index(NEW_CHANGELOG_HEADING)
    first_old = next(
        i for i, line in enumerate(changelog) if OLD_ID in line
    )
    assert first_old >= heading_line, (
        f"old id appears above the new rename entry (line {first_old + 1})"
    )

