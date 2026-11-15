"""Adversarial probes for find_vaults.py against hostile registry entries.

Runs the locator in a subprocess with a temp HOME and OBSIDIAN_CONFIG_DIR;
the real vault registry is never read.
"""

import json
import os
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[5]
FIND_VAULTS = REPO_ROOT / "obsidian/skills/obsidian-vault-search/scripts/find_vaults.py"


def _run(tmp_path, vaults, cwd):
    config = tmp_path / "config"
    config.mkdir()
    (config / "obsidian.json").write_text(json.dumps({"vaults": vaults}))
    env = {k: v for k, v in os.environ.items() if k != "OBSIDIAN_VAULT"}
    env.update(HOME=str(tmp_path / "home"), OBSIDIAN_CONFIG_DIR=str(config))
    result = subprocess.run(
        [sys.executable, str(FIND_VAULTS)], env=env, cwd=cwd, capture_output=True, text=True
    )
    assert result.returncode == 0, result.stderr
    return result.stdout.splitlines()


# concern: a relative registry path is resolved against the caller's cwd, so the current project is reported as a vault
def test_find_vaults_relative_registry_path_not_reported(tmp_path):
    """A relative registry path must not be resolved against the working directory."""
    project = tmp_path / "project"
    (project / "notes").mkdir(parents=True)
    assert _run(tmp_path, {"a": {"path": "notes", "ts": 1}}, project) == []


# concern: a vault path containing a newline breaks the one-path-per-line output contract
def test_find_vaults_newline_in_path_never_splits_line(tmp_path):
    """Every printed line must be an existing absolute directory."""
    odd = tmp_path / "v\nevil"
    odd.mkdir()
    lines = _run(tmp_path, {"a": {"path": str(odd), "ts": 1}}, tmp_path)
    assert all(os.path.isabs(line) and os.path.isdir(line) for line in lines), lines
