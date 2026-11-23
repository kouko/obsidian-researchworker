#!/usr/bin/env bash
# Characterization test for validate.sh (Pele engine). Run: bash scripts/validate.test.sh
set -uo pipefail
V="$(cd "$(dirname "$0")" && pwd)/validate.sh"
tmp="$(mktemp -d)"; trap 'rm -rf "$tmp"' EXIT
pass=0; fail=0
expect() { # desc  expected_substr  actual
  if printf '%s' "$3" | grep -q -- "$2"; then echo "ok   - $1"; pass=$((pass+1))
  else echo "FAIL - $1"; echo "       wanted /$2/ in: $3"; fail=$((fail+1)); fi
}
note() { printf '# n\n\n```mermaid\n%s\n```\n' "$1" > "$tmp/n.md"; }

# 1) quoted label with parens -> PASS, exit 0
note 'flowchart TD
  A["Call API (v2)"] --> B'
out="$(bash "$V" "$tmp/n.md" 2>&1)"; rc=$?
expect "quoted parens label -> PASS" "PASS  block 1" "$out"
expect "quoted parens label -> exit 0" "^0$" "$rc"

# 2) unquoted parens label -> FAIL, exit 1
note 'flowchart TD
  A[Call API (v2)] --> B'
out="$(bash "$V" "$tmp/n.md" 2>&1)"; rc=$?
expect "unquoted parens label -> FAIL" "FAIL  block 1" "$out"
expect "unquoted parens label -> exit 1" "^1$" "$rc"

# 3) no diagrams -> message, exit 0
printf '# empty\n' > "$tmp/e.md"
out="$(bash "$V" "$tmp/e.md" 2>&1)"; rc=$?
expect "no diagrams -> message" "no mermaid diagrams found in" "$out"
expect "no diagrams -> exit 0" "^0$" "$rc"

echo "--- $pass passed, $fail failed"
[ "$fail" -eq 0 ]
