"""Adversarial probe: the CLI branch has no dot-component filter, so with the
Obsidian app open a hit under .claudian/ is returned, while the grep fallback
drops the same hit -- the two engines do not return the same hit set, which
the spec claims they do.

# concern: the two search engines disagree on hidden-directory hits, so the
# result set depends on whether the Obsidian app happens to be running.
"""

import json
import os
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[5]
VAULT_SH = REPO_ROOT / "obsidian/skills/obsidian-knowledge/scripts/vault.sh"


def _run_search(tmp_path, vault, cli_body, open_vault):
    config = tmp_path / "config"
    config.mkdir(exist_ok=True)
    (config / "obsidian.json").write_text(json.dumps(
        {"vaults": {"v": {"path": str(vault), "ts": 5, "open": open_vault}}}))
    cli = tmp_path / "obsidian-cli"
    cli.write_text(cli_body, encoding="utf-8")
    cli.chmod(0o755)
    env = {k: v for k, v in os.environ.items() if k != "OBSIDIAN_VAULT"}
    env.update(HOME=str(tmp_path), OBSIDIAN_CONFIG_DIR=str(config),
               OBSIDIAN_CLI_BIN=str(cli))
    result = subprocess.run(
        [str(VAULT_SH), "search", str(vault), "DuckDB"],
        env=env, capture_output=True, text=True,
    )
    assert result.returncode == 0, result.stderr
    return result.stdout.splitlines()


def test_search_cli_and_grep_engines_agree_on_hidden_dir_hits(tmp_path):
    """A hit under a dot-directory must be dropped by both engines or neither."""
    vault = tmp_path / "vault"
    (vault / ".claudian" / "sessions").mkdir(parents=True)
    (vault / "alpha.md").write_text("DuckDB", encoding="utf-8")
    (vault / ".claudian" / "sessions" / "s.meta.json").write_text(
        "DuckDB", encoding="utf-8")
    cli_body = "#!/bin/sh\nprintf '.claudian/sessions/s.meta.json\\nalpha.md\\n'\n"
    cli_hits = _run_search(tmp_path, vault, cli_body, open_vault=True)
    grep_hits = _run_search(tmp_path, vault, cli_body, open_vault=False)
    assert cli_hits == grep_hits, (
        f"engines disagree: CLI={cli_hits} grep={grep_hits}")
