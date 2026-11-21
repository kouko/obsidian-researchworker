# Quarterly industry and market research — plan
intent: 2026-11-21-finance-industry-market-research@25ddff0
spec: docs/loom/2026-11-21-finance-industry-market-research/spec.md@4c49831
charter: 1.1

Binding review criteria: research/07-spec-review-criteria.md@0c6dc5d.

## Task DAG

### Wave 1 — Evidence and saved research

**W1-01 Market evidence and outlook rules**  acceptance: 3, 4
- Files: obsidian-finance/scripts/market_evidence.py, obsidian-finance/tests/test_market_evidence.py
- Test: A3 positive: eligible-originals; negative: mixed-vintage-claim. A4 positive: matched-actual; boundary: annual-forecast-quarter-actual.
- Risk: Agent-decided per REQ-3/4 and research/07-spec-review-criteria.md, bind facts to source dates and forecasts to matching target metrics.

**W1-02 Quarterly Markdown publication and resume**  after: W1-01  acceptance: 1, 2
- Files: obsidian-finance/scripts/market_research.py, obsidian-finance/tests/test_market_research.py
- Test: A1 positive: two-market-quarter-structure; boundary: incomplete-months. A2 positive: fresh-read; negative: interrupted-newer-record.
- Risk: Agent-decided per REQ-1/2 and research/07-spec-review-criteria.md, publish a valid record last, retain earlier snapshots and scope discovery to the selected market.

### Wave 2 — Skill and realistic use

**W2-01 Connect skill entry and verify representative runs**  after: W1-02  acceptance: 1, 2, 3, 4
- Files: obsidian-finance/skills/market-research/, obsidian-finance/skills/finance-research/references/industry-and-competition.md, obsidian-finance/README.md, obsidian-finance/tests/test_market_research_workflow.py, obsidian-finance/.codex-plugin/plugin.json, obsidian-finance/.claude-plugin/plugin.json, .claude-plugin/marketplace.json
- Test: A1 positive: smartphone-and-chips; boundary: eu-missing-month. A2 positive: fixture-resume; negative: broken-latest. A3 positive: apple-october-cutoff; negative: late-release. A4 positive: comparable-outlook-review; boundary: not-yet-reported.
- Risk: Agent-decided per REQ-1–4, inspect emitted notes in scripted workflow tests; existing issuer workflow remains usable and issuer integration only adopts eligible market findings.

**W2-02 Replay in fresh Codex conversations**  after: W2-01  acceptance: 1, 2, 3, 4
- Files: docs/loom/2026-11-21-finance-industry-market-research/research/08-runtime-replay.md
- Test: A1 positive: two-markets-two-quarters; boundary: quarterly-layout. A2 positive: fresh-context-resume; negative: no-chat-history. A3 positive: exact-apple-source; negative: post-cutoff-source. A4 positive: outlook-reviewed; boundary: annual-actual-pending.
- Risk: Agent-decided per REQ-1–4, record plugin discovery, commands, transcript excerpts and output paths; scripted fixtures cannot prove real session continuation.

## Simplicity check

- Share one research workflow and vary metrics by market — taken
- Use separate persistence implementations for each industry — declined: the three research cases need the same record lifecycle.
- Use one canonical review record as the publication boundary and derive lookup from it — taken

## Questions asked

① — what — 若需求草稿符合你的預期，回覆「確認，先不開 PR」可繼續在本機做。回覆「確認」也授權驗證與審查通過後推送分支並開 PR，合併另行決定。
② — behaviour — 這些是你預期的使用行為嗎？

## Risks

1. Market period, issuer fiscal quarter and publication time are independent. Preserve original release versions and material dependencies for eligible citations.
2. Existing tests cover issuer research and Obsidian utilities. Separate tests catch market-specific cutoff, aggregation, interruption and outlook mismatches. Run the full dual-package suite.
