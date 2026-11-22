# Finance recovery and text-only research pilot
intent: 2026-11-21-finance-recovery-and-text-pilot@459f029
charter: 1.1

## Current State Evidence

- Forward: `obsidian-finance/scripts/research_store.py:1243` treats historical review gaps as publication conflicts.
- Reverse: `obsidian-finance/skills/finance-research/SKILL.md:44` starts research discovery through the helper.
- Error: `obsidian-finance/tests/test_research_continuation.py:373` checks discovery after an edited note but does not append from the valid successor.
- Data: `docs/loom/2026-11-21-finance-quarter-note-continuity/evidence/acceptance-test-evidence.md` records three adjacent-quarter public SEC cases.
- Boundary: `obsidian-finance/skills/sec-data/SKILL.md:12` owns acquisition. The experiment changes local research only in isolated copies.

## Task DAG

### Wave 1

**W1-01 Repair follow-up publication** acceptance: 1
- Files: obsidian-finance/scripts/research_store.py (publish entry point), obsidian-finance/tests/test_research_continuation.py
- Test: A1 positive: publish after historical candidate edit; boundary: reject a changed predecessor.
- Risk: Preserve test_research_continuation.py coverage. Keep candidate-note staleness separate from integrity conflicts and retain strict standalone checks.

### Wave 2

**W2-01 Exercise a text-only agent workflow** after: W1-01 acceptance: 2, 3
- Files: docs/loom/2026-11-21-finance-recovery-and-text-pilot/evidence/
- Test: A2 positive: three issuer write and fresh read; boundary: cutoff, interruption, relocation. A3 positive: record observed behavior; boundary: competing writes.
- Risk: Reuse public filings and note templates. Measure concurrency without inferring atomic protection from single-agent success.

## Simplicity check

- none found

## Questions asked

① — what — 請確認這份範圍符合你的意思。

## Risks

- user-decided — Repair first and verify the text-only workflow without adopting it.
- Retain the original review result. The new obligation is an isolated text-only pilot across three issuers. Prior dialogue artifacts provide fixture inputs only.
