# Restore US quarterly behaviour after Taiwan merge — plan
intent: 2026-11-25-restore-us-quarterly-after-tw-merge@2fa14f3
charter: 1.1

## Current State Evidence
- Forward: `obsidian-finance/scripts/research_markdown.py` at f139638 equals tw-equity head 6a78dcf; PR #29 (ab04a8a) content absent.
- Reverse: `obsidian-finance/scripts/research_store.py` `_capture_quarter` no longer calls `registration_context`; `compact` mode dropped.
- Error: `test_research_markdown_templates.py:173` AttributeError registration_context; `test_research_continuation.py` KeyError research_question.
- Data: three-way merge base 6bb2411, us ab04a8a, tw 6a78dcf: 1 + 4 + 3 conflict hunks across three files.
- Boundary: Taiwan tests `test_tw_equity_*.py` pass today and must keep passing; overview `record_path` branch is Taiwan-only.

## Task DAG

**W1-01 Three-way merge US and Taiwan quarterly code**  after: none  acceptance: 1, 2, 3
- Files: obsidian-finance/scripts/research_markdown.py, obsidian-finance/scripts/research_store.py, obsidian-finance/tests/test_research_continuation.py
- Test: A1 positive: full package suite; negative: test_portable_source_context_retains_public_links_on_recapture. A2 positive: test_generated_overview_exposes_changes_and_gaps_before_record; boundary: test_public_pilot_adjacent_quarters_and_competition_cutoffs. A3 positive: test_tw_equity_workflow; negative: test_tw_equity_conference.
- Risk: agent-decided — git merge-file from 6bb2411 base; resolve hunks keeping both behaviours; preserves coverage of test_research_markdown_templates.py and test_research_continuation.py; assertions copied from ab04a8a unchanged.

**W2-01 Graduate Taiwan overview gap probe**  after: W1-01  acceptance: 3
- Files: obsidian-finance/tests/test_tw_overview_gaps_shape.py, docs/loom/2026-11-25-restore-us-quarterly-after-tw-merge/evidence/probes/test_tw_overview_gaps_shape.py
- Test: A3 positive: test_render_quarter_overview_taiwan_non_list_gaps_renders_overview[5]; boundary: test_render_quarter_overview_taiwan_non_list_gaps_renders_overview[None].
- Risk: agent-decided — probe caught a real regression; move into package suite unchanged except the repo-root path depth.

## Simplicity check
- Revert PR #28 and re-land — declined: drops shipped Taiwan behaviour, intent requires both.
- Single task over three files — taken

## Questions asked
① — consequence — 確認修正說明（問題、驗收、範圍）並授權通過審查後自動開 PR、合併另由使用者決定

## Risks
1. Taiwan overview and US overview share render_quarter_overview; a wrong branch condition could hide Taiwan gaps or US changes. Both test families must run.
2. Compact capture (quarter_evidence version 2) interacts with Taiwan JSON registrations; keep Taiwan path writing JSON unchanged.
