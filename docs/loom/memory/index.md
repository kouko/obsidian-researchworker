---
okf_version: "0.2"
---

# Memory Store Index

## Guides

- [README](README.md) — Repo-native OKF v0.2-compatible Loom memory store — one durable repository lesson per Markdown file, index.md generated and never hand-edited, Git the sole historical log.

## gotcha

- [validate-subprocess-values-before-lossy-capture](validate-subprocess-values-before-lossy-capture.md) — A shell guard that rejects control characters must run on the raw subprocess output, not on `$( )` capture — command substitution silently strips every trailing newline, so a value that ends in one is validated as its clean prefix.

## practice

- [measure-search-parity-at-the-real-entry](measure-search-parity-at-the-real-entry.md) — When claiming two search/query engines behave the same, measure parity through the shipped entry point against the real engine and record replayable literal keywords — never from a fake's assumed grammar, regex, or prose claims.
- [read-editable-notes-without-hash-gates](read-editable-notes-without-hash-gates.md) — Read user-editable Obsidian prose as it exists now. Validate the research fields a claim depends on and detect conflicting edits during the current write.
