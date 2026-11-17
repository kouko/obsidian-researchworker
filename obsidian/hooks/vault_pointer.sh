#!/bin/sh
# SessionStart hook: one line naming local Obsidian vaults, or nothing.
# Plain stdout on SessionStart is added to Claude's context. Always exits 0.
set -u

script_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
vaults=$("$script_dir/../skills/obsidian-knowledge/scripts/vault.sh" locate 2>/dev/null)
[ -n "$vaults" ] || exit 0

joined=$(printf '%s\n' "$vaults" | awk 'NR>1{printf "; "} {printf "%s", $0}')
printf 'Local Obsidian vault(s): %s. When a question may be answered by the user'\''s own notes, or when dispatching research subagents, use the obsidian-knowledge skill (read-only).\n' "$joined"
exit 0
