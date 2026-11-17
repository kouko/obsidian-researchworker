---
name: validate-subprocess-values-before-lossy-capture
description: A shell guard that rejects control characters must run on the raw subprocess output, not on `$( )` capture — command substitution silently strips every trailing newline, so a value that ends in one is validated as its clean prefix.
type: gotcha
sources:
  - resource: "obsidian/skills/obsidian-knowledge/scripts/vault.sh"
  - resource: "obsidian/tests/test_find_vaults_hostile_registry.py"
---

# Validate subprocess values before lossy capture

**Trigger**: shell code that reads a value from another program (`plutil`, `jq`, a CLI's stdout) and then checks it for control characters, compares it for equality, or prints it on a one-value-per-line contract.

**The trap**: `v=$(tool …)` strips *all* trailing newlines. A value that genuinely ends in a newline — `"/tmp/real\n"` in a registry file, a trailing `\n` in a `ts` field — becomes byte-identical to the clean value, so the downstream `case "$v" in *[[:cntrl:]]*)` guard never sees the control byte and the truncated value passes as legitimately named. Trailing-newline stripping is exactly what makes `$( )` convenient for assigning tool output, so the guard silently protects a narrower input class than its comment claims.

**Correct path**: capture with a line-reading pair instead of `$( )`, and treat a leftover second line as a defect rather than data. `plutil -extract … raw` always terminates output with exactly one newline, so a second readable line means the value itself contained one:

```sh
read_pair() {
    tool "$1" | { IFS= read -r v || exit 2   # absent: no first line
                   IFS= read -r x && exit 1   # value itself had a newline
                   printf '%s\n' "$v"; }
}
```

Callers then distinguish the two exit codes: absent (`2`) means "fall back to a default", malformed (`1`) means "drop this record". Collapsing them loses the distinction — falling back to `0` for a `ts` that spanned lines keeps an entry the registry never validly named.

**Why**: a code review found this on `vault.sh` twice (2026-11-16): first the guard was added at emission but ran on `$( )` values, so a registry path `<existing dir>\n` was accepted as that directory. Reproduced by writing the JSON value and running the locator — the clean prefix was printed.

**Limits**: the read-pair idiom needs an extractor whose output shape is predictable (one terminator newline). For a tool that emits a trailing blank line by design, use an explicit sentinel line instead, and say in the comment which invariant the helper relies on.
