"""Adversarial probe: the CLI branch prefixes any relative path the Obsidian CLI
prints, including traversal payloads, so a CLI that emits '../x.md' makes
vault.sh search report a note path outside the vault.

# concern: a CLI-emitted relative path with traversal components is joined to
# the vault path and printed as a note path, breaking the cite-only-inside-the-
# vault contract the skill promises its readers.
"""

import json
import os
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[5]
VAULT_SH = REPO_ROOT / "obsidian/skills/obsidian-knowledge/scripts/vault.sh"


def test_search_cli_branch_rejects_traversal_relative_paths(tmp_path):
    """A CLI line such as '../escape.md' must not become <vault>/../escape.md."""
    vault = tmp_path / "vault"
    vault.mkdir()
    (vault / "alpha.md").write_text("DuckDB", encoding="utf-8")
    config = tmp_path / "config"
    config.mkdir()
    (config / "obsidian.json").write_text(json.dumps(
        {"vaults": {"v": {"path": str(vault), "ts": 5, "open": True}}}))
    cli = tmp_path / "obsidian-cli"
    cli.write_text("#!/bin/sh\nprintf '../escape.md\\nalpha.md\\n'\n", encoding="utf-8")
    cli.chmod(0o755)
    env = {k: v for k, v in os.environ.items() if k != "OBSIDIAN_VAULT"}
    env.update(HOME=str(tmp_path), OBSIDIAN_CONFIG_DIR=str(config),
               OBSIDIAN_CLI_BIN=str(cli))
    result = subprocess.run(
        [str(VAULT_SH), "search", str(vault), "DuckDB"],
        env=env, capture_output=True, text=True,
    )
    assert result.returncode == 0, result.stderr
    out = result.stdout.splitlines()
    assert str(vault / "alpha.md") in out
    # No printed path may escape the vault: '../escape.md' joined to the vault
    # resolves above it, which the accept gate must reject before printing.
    for line in out:
        resolved = Path(line).resolve()
        assert resolved == vault or vault in resolved.parents, \
            f"note path escapes the vault: {line}"
