"""Adversarial probe for parity between vault.sh's two search engines.

Three concerns, each measured once against the real Obsidian CLI first:

- a hit under a dot-directory must be dropped by both engines or neither;
- a query word is operator syntax unless it is quoted (`file:alpha` bare
  returned 13 operator hits, quoted returned 0), so the script must hand the
  CLI quoted phrases or the two engines answer different questions;
- the CLI indexes `.md` notes only, so a grep hit in a `.yaml` file would make
  the result set depend on whether the app is running.

# concern: the two search engines disagree on hidden-directory hits, on how a
# query word is parsed, or on which file types count, so the result set depends
# on whether the Obsidian app happens to be running.
"""

import json
import os
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[5]
VAULT_SH = REPO_ROOT / "obsidian/skills/obsidian-knowledge/scripts/vault.sh"

# A fake CLI that reproduces the real one's measured query grammar: OR-joins
# terms, treats a double-quoted term as a literal phrase, treats a bare
# `file:`/`path:` prefix as an operator, and matches notes only.
FAKE_CLI = '''#!/usr/bin/env python3
import sys, pathlib
query = vault = ""
for arg in sys.argv[1:]:
    if arg.startswith("query="):
        query = arg[len("query="):]
    elif arg.startswith("vault="):
        vault = arg[len("vault="):]
root = pathlib.Path(vault)
notes = sorted(p for p in root.rglob("*.md") if not any(c.startswith(".") for c in p.relative_to(root).parts))
def literal(term, note):
    return term in note.read_text(encoding="utf-8", errors="replace")
hits = set()
for term in query.split(" OR ") if query else []:
    if len(term) > 1 and term.startswith('"') and term.endswith('"'):
        phrase = term[1:-1]
        for note in notes:
            if literal(phrase, note):
                hits.add(str(note.relative_to(root)))
    elif ":" in term:
        kind, _, value = term.partition(":")
        for note in notes:
            hay = str(note.relative_to(root)) if kind == "file" else str(note.parent.relative_to(root))
            if value.lower() in hay.lower():
                hits.add(str(note.relative_to(root)))
    else:
        words = term.split()
        for note in notes:
            if all(literal(w, note) for w in words):
                hits.add(str(note.relative_to(root)))
print("\\n".join(sorted(hits)) if hits else "No matches found.")
'''


def _run_search(tmp_path, vault, open_vault, *query):
    config = tmp_path / "config"
    config.mkdir(exist_ok=True)
    (config / "obsidian.json").write_text(json.dumps(
        {"vaults": {"v": {"path": str(vault), "ts": 5, "open": open_vault}}}))
    cli = tmp_path / "obsidian-cli"
    cli.write_text(FAKE_CLI, encoding="utf-8")
    cli.chmod(0o755)
    env = {k: v for k, v in os.environ.items() if k != "OBSIDIAN_VAULT"}
    env.update(HOME=str(tmp_path), OBSIDIAN_CONFIG_DIR=str(config),
               OBSIDIAN_CLI_BIN=str(cli))
    result = subprocess.run(
        [str(VAULT_SH), "search", str(vault), *query],
        env=env, capture_output=True, text=True,
    )
    assert result.returncode == 0, result.stderr
    return result.stdout.splitlines()


def _both(tmp_path, vault, *query):
    return (_run_search(tmp_path, vault, True, *query),
            _run_search(tmp_path, vault, False, *query))


def test_search_engines_agree_on_hidden_dir_hits(tmp_path):
    """A hit under a dot-directory must be dropped by both engines or neither."""
    vault = tmp_path / "vault"
    (vault / ".claudian" / "sessions").mkdir(parents=True)
    (vault / "alpha.md").write_text("DuckDB", encoding="utf-8")
    (vault / ".claudian" / "sessions" / "s.md").write_text("DuckDB", encoding="utf-8")
    cli_hits, grep_hits = _both(tmp_path, vault, "DuckDB")
    assert cli_hits == grep_hits == [str(vault / "alpha.md")], (
        f"engines disagree: CLI={cli_hits} grep={grep_hits}")


def test_search_engines_agree_on_operator_looking_word(tmp_path):
    """`file:alpha` must be a literal search for both engines, not an operator."""
    vault = tmp_path / "vault"
    vault.mkdir()
    (vault / "alpha.md").write_text("nothing here", encoding="utf-8")
    (vault / "beta.md").write_text("see file:alpha for details", encoding="utf-8")
    cli_hits, grep_hits = _both(tmp_path, vault, "file:alpha")
    assert cli_hits == grep_hits == [str(vault / "beta.md")], (
        f"engines disagree: CLI={cli_hits} grep={grep_hits}")


def test_search_engines_agree_on_multi_word_phrase(tmp_path):
    """A phrase word is one literal string for both engines, not AND-of-terms."""
    vault = tmp_path / "vault"
    vault.mkdir()
    (vault / "phrase.md").write_text("a vector database approach", encoding="utf-8")
    (vault / "split.md").write_text("vector marker, then database later", encoding="utf-8")
    cli_hits, grep_hits = _both(tmp_path, vault, "vector database")
    assert cli_hits == grep_hits == [str(vault / "phrase.md")], (
        f"engines disagree: CLI={cli_hits} grep={grep_hits}")


def test_search_engines_agree_on_note_file_type(tmp_path):
    """A non-note file the CLI never indexes must not appear from grep."""
    vault = tmp_path / "vault"
    vault.mkdir()
    (vault / "alpha.md").write_text("DuckDB", encoding="utf-8")
    (vault / "config.yaml").write_text("DuckDB", encoding="utf-8")
    cli_hits, grep_hits = _both(tmp_path, vault, "DuckDB")
    assert cli_hits == grep_hits == [str(vault / "alpha.md")], (
        f"engines disagree: CLI={cli_hits} grep={grep_hits}")
