# On-demand technical analysis snapshots — plan
intent: 2026-11-23-technical-analysis-optional-snapshot@aa4378d
spec: docs/loom/2026-11-23-technical-analysis-optional-snapshot/spec.md@d4ec85b
charter: 1.1

## Task DAG

**W1-01 Select snapshot retention at the existing publisher** after: none acceptance: 1, 2
- Files: obsidian-finance/skills/technical-analysis/scripts/report.py, obsidian-finance/skills/technical-analysis/SKILL.md, obsidian-finance/README.md, obsidian-finance/tests/test_technical_report.py
- Test: A1 positive: routine save retains chart and source details; boundary: reject stale snapshot placeholder before publication.
- Test: A2 positive: existing CLI retained input reproduces output; boundary: existing zero-bar save retains source without chart.
- Risk: agent-decided — preserve existing direct callers and exercise both modes in test_technical_report.py; these tests widen coverage without changing existing expectations.

## Simplicity check

- One per-save option without new configuration — taken

## Questions asked

① — what — 這兩項驗收條件符合你的意思嗎？
② — behaviour — 這兩種存檔行為符合你的預期嗎？

## Risks

second-vendor: suggest

1. Prepared Markdown can refer to an omitted attachment. Validate placeholders before publishing any file.
