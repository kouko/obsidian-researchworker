# Deep quarterly equity research notes — plan
intent: 2026-11-23-equity-deep-research-notes@6a1b95e
spec: docs/loom/2026-11-23-equity-deep-research-notes/spec.md@bf8ac19
charter: 1.1

## Task DAG

### Wave 1 — Compact saved evidence

**W1-01 Compact exact source bindings** after: none acceptance: 3, 4
- Files: obsidian-finance/scripts/research_store.py, obsidian-finance/tests/test_research_continuation.py, obsidian-finance/tests/test_quarter_publication.py
- Test: A3 positive: deduplicate-consumed-projections; boundary: exact-version-substitution. A4 positive: portable-update-and-next-quarter; boundary: missing-capture-cutoff-and-edit-recovery.
- Risk: REQ-3–4. Reuse quarter-local captures and resolve checked evidence before exposing it to existing assessment. Leave legacy readers and report paths intact.

### Wave 2 — Readable notes

**W2-01 Render readable notes and define role-level analysis** after: W1-01 acceptance: 1, 2, 3, 4
- Files: obsidian-finance/scripts/research_markdown.py, obsidian-finance/scripts/research_store.py, obsidian-finance/skills/equity-research-us/SKILL.md, obsidian-finance/skills/equity-research-us/README.md, obsidian-finance/skills/equity-research-us/references, obsidian-finance/skills/equity-research-us/templates, obsidian-finance/README.md, obsidian-finance/tests/test_research_markdown_templates.py
- Test: A1 positive: all-note-roles; boundary: missing-description. A2 positive: seven-role-output-checks; boundary: evidence-gap-affects-judgment. A3 positive: linked-overview-and-comparisons; boundary: unsupported-chart-values. A4 positive: generated-overview-readback; boundary: escaped-metadata.
- Risk: REQ-1–4. Strengthen existing frameworks and templates. Reuse research summaries and evidence. Preserve typed properties and readback. Use evidence-dependent output expectations.

## Simplicity check

- Consolidate overlapping template and guidance changes into a single task with shared verification — taken

## Questions asked

① — what — 請確認這個實作範圍。
② — behaviour — 請確認這些是你想看到的行為。

## Risks

1. Compact records must not accept another source version with the same ID or mask a missing captured record. Check standalone quarter and normal discovery.
2. Use equivalent Fastenal evidence in two isolated runs. Record all seven roles, generated registrations, YAML size, and diagram rendering. Test same-quarter edits, historical cutoffs and resumption.
