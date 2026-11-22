# Optional earnings-call evidence — plan
intent: 2026-11-22-equity-earnings-call-evidence@8f26dab
spec: docs/loom/2026-11-22-equity-earnings-call-evidence/spec.md@395796d
charter: 1.1

## Task DAG

### Wave 1

**W1-01 Guide optional call evidence use** acceptance: 1, 2, 3, 4
- Files: obsidian-finance/skills/equity-research/SKILL.md, obsidian-finance/skills/equity-research/references/earnings-call-sources.md
- Test: A1 positive: attributed-qa; boundary: analyst-question. A2 positive: summary-labeled; negative: missing-call. A3 positive: eligible-call; negative: later-publication. A4 positive: formal-actual; boundary: call-only-guidance.
- Risk: REQ-1 through REQ-4. Agent-decided — keep source selection and numeric rules in a single reference so the shipped entry can route there without a new data contract.

## Simplicity check

- reuse existing source registration — taken

## Questions asked

① — what — 這個範圍符合你的意思嗎？
① — what — 請確認加入這條後的需求範圍。
② — behaviour — 請確認這就是你希望看到的研究行為，我再繼續實作。

## Risks

- Compare only matching period, basis and metric. A later correction must not leak into an earlier cutoff.
- Missing optional evidence must not block independent work. Already adopted and unverifiable evidence limits only affected conclusions.
