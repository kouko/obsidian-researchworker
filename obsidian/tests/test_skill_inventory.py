# concern: removed skill rediscovery and dangling dependencies in retained skills
# concern: shared vault setup routing reintroduces retired wiki/news dependencies
"""The shipped skills remain usable without the retired wiki/news mechanisms."""
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RETAINED = {
    "dashboard-design", "defuddle", "obsidian-bases", "obsidian-canvas",
    "obsidian-cli", "obsidian-daily", "obsidian-excalidraw-diagram",
    "obsidian-file-intel", "obsidian-knowledge", "obsidian-markdown", "obsidian-mermaid-visualizer",
    "obsidian-research", "obsidian-research-resume", "obsidian-tldr", "obsidian-vault-setup", "using-obsidian",
}
REMOVED = {
    "wiki-setup", "wiki-ingest", "wiki-query", "wiki-cross-linker",
    "wiki-merge", "wiki-lint", "wiki-auto-research", "wiki-update",
    "daily-news-digest",
}


def test_shipped_skill_inventory():
    assert {p.parent.name for p in (ROOT / "skills").glob("*/SKILL.md")} == RETAINED


def test_retained_skills_have_no_retired_dependencies():
    for name in REMOVED:
        assert not (ROOT / "skills" / name).exists()
    for name in ("distribute.py", "verify-drift.py", "test_distribute.py", "test_verify_drift.py"):
        assert not (ROOT / "scripts" / name).exists()
    assert not (ROOT / "tests/wiki_ingest").exists()
    for name in RETAINED:
        for path in (ROOT / "skills" / name).rglob("*.md"):
            if path.name.startswith("README"):
                continue  # Release-facing descriptions are verified with the release docs.
            text = path.read_text()
            assert not any(removed in text for removed in REMOVED), path
