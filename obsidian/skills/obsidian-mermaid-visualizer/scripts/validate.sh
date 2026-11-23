#!/usr/bin/env bash
# validate.sh — render every ```mermaid block of a markdown note with Pele,
# the Mermaid engine Obsidian 1.15+ uses, and report PASS/FAIL per block.
# Thin wrapper: installs the pinned pele into scripts/node_modules on first
# use, then runs validate.mjs (see its header for the pinned version).
#
# Usage:
#   scripts/validate.sh path/to/note.md
#
# Exit: 0 = all blocks render (or none found), 1 = at least one FAIL, 2 = bad usage.
set -euo pipefail

[ $# -eq 1 ] || { grep '^#' "$0" | sed 's/^# \{0,1\}//'; exit 2; }
dir="$(cd "$(dirname "$0")" && pwd)"

command -v node >/dev/null || { echo "validate.sh: node is required" >&2; exit 2; }
if [ ! -d "$dir/node_modules/pele" ]; then
  npm install --prefix "$dir" --no-audit --no-fund --silent >&2 \
    || { echo "validate.sh: npm install of pele failed" >&2; exit 2; }
fi
exec node "$dir/validate.mjs" "$1"
