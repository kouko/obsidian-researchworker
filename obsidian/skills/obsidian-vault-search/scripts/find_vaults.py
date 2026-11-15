#!/usr/bin/env python3
"""Print one absolute Obsidian vault path per line. Stdlib only; never raises.

OBSIDIAN_VAULT (os.pathsep-separated) replaces the registry when set.
Otherwise reads Obsidian's obsidian.json registry (macOS / Linux;
OBSIDIAN_CONFIG_DIR overrides its directory), newest-opened first.
Only existing directories are printed. Windows is unsupported.
"""

import json
import os
import sys
from pathlib import Path


def _config_dir():
    override = os.environ.get("OBSIDIAN_CONFIG_DIR")
    if override:
        return Path(override)
    if sys.platform == "darwin":
        return Path.home() / "Library/Application Support/obsidian"
    base = os.environ.get("XDG_CONFIG_HOME") or str(Path.home() / ".config")
    return Path(base) / "obsidian"


def _candidates():
    env = os.environ.get("OBSIDIAN_VAULT")
    if env:
        return env.split(os.pathsep)
    try:
        data = json.loads((_config_dir() / "obsidian.json").read_text(encoding="utf-8"))
        entries = [v for v in data.get("vaults", {}).values() if isinstance(v, dict)]
    except Exception:
        return []
    entries.sort(key=lambda v: v.get("ts") if isinstance(v.get("ts"), (int, float)) else 0, reverse=True)
    return [v.get("path") for v in entries if isinstance(v.get("path"), str)]


def find_vaults():
    seen, out = set(), []
    for raw in _candidates():
        if not raw or any(ord(c) < 32 or ord(c) == 127 for c in raw):
            continue  # control chars would inject extra output lines
        expanded = os.path.expanduser(raw)
        if not os.path.isabs(expanded):
            continue  # relative paths would resolve against cwd
        path = os.path.normpath(expanded)
        if path not in seen and os.path.isdir(path):
            seen.add(path)
            out.append(path)
    return out


def main():
    try:
        for path in find_vaults():
            print(path)
    except Exception:
        pass
    return 0


if __name__ == "__main__":
    sys.exit(main())
