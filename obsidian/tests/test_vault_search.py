"""Vault locator tests (loom change 2026-11-15-search-vault-from-other-projects).

Each test runs find_vaults.py in a subprocess with a temp HOME and
OBSIDIAN_CONFIG_DIR, so the real vault registry is never read.
"""

import json
import os
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
FIND_VAULTS = REPO_ROOT / "obsidian/skills/obsidian-vault-search/scripts/find_vaults.py"


def _run(tmp_path, vaults=None, env_vault=None):
    config = tmp_path / "config"
    config.mkdir()
    if vaults is not None:
        (config / "obsidian.json").write_text(json.dumps({"vaults": vaults}))
    env = {k: v for k, v in os.environ.items() if k != "OBSIDIAN_VAULT"}
    env.update(HOME=str(tmp_path), OBSIDIAN_CONFIG_DIR=str(config))
    if env_vault is not None:
        env["OBSIDIAN_VAULT"] = env_vault
    result = subprocess.run(
        [sys.executable, str(FIND_VAULTS)], env=env, capture_output=True, text=True
    )
    assert result.returncode == 0, result.stderr
    return result.stdout.splitlines()


def test_registry_lists_existing_vault(tmp_path):
    old, new = tmp_path / "old", tmp_path / "new"
    old.mkdir()
    new.mkdir()
    vaults = {
        "a": {"path": str(old), "ts": 1},
        "b": {"path": str(new), "ts": 2},
        "c": {"path": str(new), "ts": 0},
    }
    assert _run(tmp_path, vaults) == [str(new), str(old)]


def test_missing_registry_prints_nothing(tmp_path):
    assert _run(tmp_path) == []


def test_env_override_replaces_registry(tmp_path):
    reg, a, b = tmp_path / "reg", tmp_path / "a", tmp_path / "b"
    for d in (reg, a, b):
        d.mkdir()
    env_vault = os.pathsep.join([str(a), str(tmp_path / "gone"), str(b)])
    out = _run(tmp_path, {"r": {"path": str(reg), "ts": 9}}, env_vault)
    assert out == [str(a), str(b)]


def test_registry_entry_with_deleted_path_skipped(tmp_path):
    live = tmp_path / "live"
    live.mkdir()
    vaults = {"x": {"path": str(tmp_path / "deleted"), "ts": 5}, "y": {"path": str(live), "ts": 1}}
    assert _run(tmp_path, vaults) == [str(live)]


HOOKS_DIR = REPO_ROOT / "obsidian/hooks"


def _run_hook(tmp_path, env_vault=None):
    env = {k: v for k, v in os.environ.items() if k != "OBSIDIAN_VAULT"}
    env.update(HOME=str(tmp_path), OBSIDIAN_CONFIG_DIR=str(tmp_path / "noconfig"))
    if env_vault is not None:
        env["OBSIDIAN_VAULT"] = env_vault
    result = subprocess.run(
        [sys.executable, str(HOOKS_DIR / "vault_pointer.py")],
        env=env, capture_output=True, text=True, cwd=str(tmp_path),
    )
    assert result.returncode == 0
    assert result.stderr == ""
    return result.stdout


def test_hook_emits_one_line_with_vault_paths(tmp_path):
    a, b = tmp_path / "a", tmp_path / "b"
    a.mkdir()
    b.mkdir()
    lines = _run_hook(tmp_path, os.pathsep.join([str(a), str(b)])).splitlines()
    assert len(lines) == 1
    assert lines[0].startswith(f"Local Obsidian vault(s): {a}; {b}. ")
    assert "obsidian-vault-search skill (read-only)" in lines[0]


def test_hook_silent_and_exit0_without_vault(tmp_path):
    assert _run_hook(tmp_path) == ""
    hooks = json.loads((HOOKS_DIR / "hooks.json").read_text())
    command = hooks["hooks"]["SessionStart"][0]["hooks"][0]["command"]
    assert "vault_pointer.py" in command and "|| true" in command
