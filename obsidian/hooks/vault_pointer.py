#!/usr/bin/env python3
"""SessionStart hook: print one line naming local Obsidian vaults, or nothing.

Plain stdout on SessionStart is added to Claude's context. Always exits 0.
"""

import sys


def main():
    sys.dont_write_bytecode = True  # keep __pycache__ out of the skill folder
    try:
        import importlib.util
        from pathlib import Path

        script = Path(__file__).resolve().parent.parent / "skills/obsidian-vault-search/scripts/find_vaults.py"
        spec = importlib.util.spec_from_file_location("find_vaults", script)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        vaults = module.find_vaults()
        if vaults:
            line = (
                f"Local Obsidian vault(s): {'; '.join(vaults)}. When a question may be answered "
                "by the user's own notes, or when dispatching research subagents, use the "
                "obsidian-vault-search skill (read-only)."
            )
            print(" ".join(line.splitlines()))  # never more than one line
    except Exception:
        pass
    return 0


if __name__ == "__main__":
    sys.exit(main())
