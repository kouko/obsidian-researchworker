# Forecast framework — plan
intent: 2026-11-20-finance-forecast-framework@05b54f0
charter: 1.1

## Current State Evidence

- Forward: finance-research SKILL.md section 3 routes fundamentals into valuation.
- Reverse: SKILL.md section 2 verifies saved applied inputs before reuse.
- Error: research-method.md keeps unsupported questions pending.
- Data: obsidian-finance/README.md gives the existing version-1 forecast work example.
- Boundary: research-method.md excludes sources unavailable at the cutoff.

## Task DAG

### Wave 1

**W1-01 Route reusable quarterly forecasts**  acceptance: 1, 2, 3, 4
- Files: obsidian-finance/skills/finance-research/SKILL.md, obsidian-finance/skills/finance-research/references/
- Test: A1 positive: choose-supported-model; boundary: unsupported-scenario. A2 positive: prior-forecast-check; negative: overwritten-vintage. A3 positive: bind-adopted-forecast; boundary: quote-only. A4 positive: dated-expectations; negative: late-consensus.
- Risk: Agent-decided reuse version-1 metadata and prefer evidence-driven models over one industry-specific method. See research/01-forecasting-methods.md.

## Simplicity check

- Use existing review assets and dependency identities — taken
- Add a fixed financial model or new note format — declined: sector choices and existing store suffice

## Questions asked

① — what — 可以按這個範圍開始嗎？

## Risks

1. A late market observation must not leak into an earlier forecast. Keep market-implied expectations downstream and check original availability separately from current reconstruction authorship.
