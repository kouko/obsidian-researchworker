"""Adversarial probes for vault.sh locate against hostile registry entries.

Runs the locator in a subprocess with a temp HOME and OBSIDIAN_CONFIG_DIR;
the real vault registry is never read.
"""

import json
import os
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
VAULT_SH = REPO_ROOT / "obsidian/skills/obsidian-knowledge/scripts/vault.sh"


def _run(tmp_path, vaults, cwd):
    config = tmp_path / "config"
    config.mkdir()
    (config / "obsidian.json").write_text(json.dumps({"vaults": vaults}))
    env = {k: v for k, v in os.environ.items() if k != "OBSIDIAN_VAULT"}
    env.update(HOME=str(tmp_path / "home"), OBSIDIAN_CONFIG_DIR=str(config))
    result = subprocess.run(
        [str(VAULT_SH), "locate"], env=env, cwd=cwd, capture_output=True, text=True
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


# concern: a registry path with an embedded newline splits into two lines inside
# plutil_vaults, before emit_vault's per-line check runs, so the tail becomes a
# reported vault the registry never named
def test_find_vaults_newline_plus_real_dir_never_splits_into_two(tmp_path):
    """`<real dir>\\n<another existing dir>` must contribute no vault at all.

    Truncating to the first line would report a directory the registry never
    named, so the malformed entry is dropped whole.
    """
    real = tmp_path / "real"
    other = tmp_path / "other"
    for d in (real, other):
        d.mkdir()
    lines = _run(tmp_path, {"a": {"path": f"{real}\n{other}", "ts": 1}}, tmp_path)
    assert lines == [], lines


# concern: a control character in `ts` is printed on the same entry line as the
# path; a whole-entry control-char check must drop the entry, not just its path
def test_find_vaults_control_char_in_ts_does_not_forge_a_path(tmp_path):
    """A `ts` with a control character must not contribute any vault line."""
    real = tmp_path / "real"
    other = tmp_path / "other"
    for d in (real, other):
        d.mkdir()
    lines = _run(tmp_path, {"a": {"path": str(other), "ts": f"1\n{real}"}}, tmp_path)
    assert lines == [], lines
