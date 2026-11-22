# Stable equity quarterly notes — plan
intent: 2026-11-22-equity-quarterly-notes@7824c3c
spec: docs/loom/2026-11-22-equity-quarterly-notes/spec.md@2ca5e2a
charter: 1.1

## Task DAG

### Wave 1 — Quarterly storage

**W1-01 Stable company quarter persistence** after: none acceptance: 1, 2, 3, 4
- Files: obsidian-finance/scripts/research_store.py, obsidian-finance/scripts/research_markdown.py, obsidian-finance/tests/test_quarter_publication.py, obsidian-finance/tests/test_research_continuation.py
- Test: A1 positive: stable-role-update; boundary: duplicate-role. A2 positive: language-independent-path; boundary: unsafe-company-name. A3 positive: revision-and-next-quarter; boundary: earlier-cutoff-read. A4 positive: interrupted-save-recovery; boundary: concurrent-edit-preserved.
- Risk: REQ-1–5. Reuse verified update primitives and quarter data validation. Preserve historical evidence and stop ambiguous or incomplete publication.

### Wave 2 — Skill integration

**W2-01 Guide the fixed quarterly workflow** after: W1-01 acceptance: 1, 2, 3, 4
- Files: obsidian-finance/skills/equity-research/SKILL.md, obsidian-finance/skills/equity-research/README.md, obsidian-finance/skills/equity-research/templates, obsidian-finance/README.md, obsidian-finance/tests/test_research_markdown_templates.py
- Test: A1 positive: overview-links; boundary: partial-quarter. A2 positive: numbered-English-labels; boundary: localized-title. A3 positive: traceable-material-revision; boundary: insufficient-historical-evidence. A4 positive: recovery-guidance; boundary: unowned-note.
- Risk: REQ-1–5. Keep SEC acquisition and the seven analytical frameworks intact. Align templates and instructions with stored paths and report roles.

## Simplicity check

- Reuse the existing note update and recovery primitive without modifying it — taken

## Questions asked

① — what — 請確認更新後的範圍，我會接著整理詳細規格。
② — behaviour — 請確認以下使用方式：

## Risks

1. An earlier-cutoff read must not rewrite the current report. An interruption after a child report write must not make the overview report completion.
2. Old-format compatibility is outside acceptance. Existing files remain untouched. Use isolated fixtures for update and recovery.
