---
name: measure-search-parity-at-the-real-entry
description: When claiming two search/query engines behave the same, measure parity through the shipped entry point against the real engine and record replayable literal keywords — never from a fake's assumed grammar, regex, or prose claims.
type: practice
sources:
  - resource: "docs/loom/2026-11-15-search-vault-from-other-projects/spec.md"
  - resource: "docs/loom/2026-11-15-search-vault-from-other-projects/retrieval-check.md"
  - resource: "obsidian/skills/obsidian-knowledge/scripts/vault.sh"
---

# Measure search parity at the real entry point

**Trigger**: any change or doc that asserts two engines return "the same hit set" / "equivalent results", or records search evidence by keyword.

**Correct path**: probe the real engine's grammar first with the words that look dangerous (operator prefixes, quotes, spaces); encode query words so the primary engine reads each as the same literal the fallback engine matches; make the fallback's file-type scope match what the primary indexes; then measure every recorded query through the actual shipped command (both engines, forcing the fallback with a nonexistent binary override) and record the exact literal keywords — regex is never supported by fixed-string engines, so a recorded regex keyword is a recording error, not an engine result. Ship a parity probe whose fake reproduces the measured grammar, and verify the probe fails on the pre-fix script.

**Why**: this repo's vault-search change claimed "the two engines return the same hit set" while the CLI parsed bare words as AND-of-terms and `file:` prefixes as operators, and grep returned `.yaml` files the CLI never indexes — four divergence classes found only by running the real CLI (2026-11-16, fix c6d1652). The same round found a recorded regex keyword that reproduced 0 hits, invalidating a retrieval-check row (fix 06145bf). Fixture-level equality proves nothing about the real engine; prose equality proves less.

**Limits**: substring vs word-boundary matching can remain an irreducible superset difference (CLI-quoted ⊆ grep-fixed); record it as a stated residual instead of chasing full equality.
