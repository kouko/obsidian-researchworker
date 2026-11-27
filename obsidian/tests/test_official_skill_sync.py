# concern: forked skills stay aligned with upstream obsidianmd/obsidian-skills fixes
"""Shipped skills carry the upstream fixes while keeping repo extensions."""
import re
from pathlib import Path

SKILLS = Path(__file__).resolve().parents[1] / "skills"


def _text(name):
    return (SKILLS / name / "SKILL.md").read_text()


def test_obsidian_cli_has_upstream_cautions_and_no_silent_flag():
    text = _text("obsidian-cli")
    assert "## Before using the CLI" in text
    assert "exits with status 0" in text
    assert "Obsidian.com" in text
    assert "don't install the unrelated npm package" in text
    assert "no escape" in text and "include the extension" in text
    for line in text.splitlines():
        if "There is no `silent` flag" in line:
            continue
        assert not re.search(r"\bsilent\b", line), line


def test_obsidian_cli_vault_targeting_asks_and_handles_duplicate_names():
    text = _text("obsidian-cli")
    assert "ask which one before changing files" in text
    assert "obsidian vaults verbose" in text
    assert "share a name" in text and "by path" in text
