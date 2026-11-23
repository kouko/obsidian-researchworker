#!/usr/bin/env bash
# validate.sh — render every ```mermaid block of a markdown note with Pele,
# the Mermaid engine Obsidian 1.15+ uses, and report PASS/FAIL per block.
# Thin wrapper: on first use installs the pinned pele into a cache directory
# outside the skill folder (${XDG_CACHE_HOME:-$HOME/.cache}/obsidian-mermaid-
# visualizer/pele-1.13.0), then runs validate.mjs with PELE_DIR pointing there
# (see validate.mjs's header for the pinned version).
#
# Usage:
#   scripts/validate.sh path/to/note.md
#
# Exit: 0 = all blocks render (or none found), 1 = at least one FAIL, 2 = bad usage.
set -euo pipefail

[ $# -eq 1 ] || { grep '^#' "$0" | sed 's/^# \{0,1\}//'; exit 2; }
dir="$(cd "$(dirname "$0")" && pwd)"
cache="${XDG_CACHE_HOME:-$HOME/.cache}/obsidian-mermaid-visualizer/pele-1.13.0"

command -v node >/dev/null || { echo "validate.sh: node is required" >&2; exit 2; }
if [ ! -f "$cache/node_modules/pele/package.json" ]; then
  mkdir -p "$cache" && cp "$dir/package.json" "$cache/package.json"
  npm install --prefix "$cache" --no-audit --no-fund --silent >&2 \
    || { echo "validate.sh: npm install of pele failed" >&2; exit 2; }
fi
PELE_DIR="$cache/node_modules/pele" exec node "$dir/validate.mjs" "$1"
