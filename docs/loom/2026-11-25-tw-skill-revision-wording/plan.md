# Align Taiwan skill revision wording with republish behaviour — plan
intent: 2026-11-25-tw-skill-revision-wording@9ec5fc1
charter: 1.1

## Current State Evidence
- Forward: `obsidian-finance/skills/tw-equity-research/SKILL.md:48` tells the agent to read prior 04 forecast's dated revision record.
- Reverse: `obsidian-finance/skills/tw-equity-research/SKILL.md:61` tells the agent to keep original values in an in-note dated revision record.
- Error: no test guards this wording; `test_tw_equity_workflow.py::test_skill_entry_exposes_the_packaged_workflow` only checks entry names.
- Data: since PR #40 (9f6aba7) Taiwan republish keeps only the latest conclusion; prior file goes to a backup copy.
- Boundary: correction must still record original value, original source and the judgement at that time.

## Task DAG

**W1-01 Reword Taiwan skill revision instructions**  after: none  acceptance: 1, 2, 3
- Files: obsidian-finance/skills/tw-equity-research/SKILL.md, obsidian-finance/tests/test_tw_equity_workflow.py
- Test: A1 positive: test_skill_drops_in_note_dated_revision_record; negative: test_skill_entry_exposes_the_packaged_workflow. A2 positive: test_skill_drops_in_note_dated_revision_record; boundary: test_skill_drops_in_note_dated_revision_record. A3 positive: full package suite; negative: test_tw_equity_workflow.
- Risk: agent-decided — reword two sentences only; new text assertion widens coverage of test_tw_equity_workflow.py; existing entry test preserved.

## Simplicity check
- Wording edit without a test — declined: a one-function text assertion prevents the stale wording returning in a later merge.

## Questions asked
① — consequence — 確認修改目標（兩處台股說明措辭、驗收、範圍）並授權通過審查後自動開 PR、合併另由使用者決定

## Risks
1. Agent wording may still imply a revision log; the test checks the phrase 修訂紀錄 is absent from the whole skill.
