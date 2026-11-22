# Taiwan quarterly equity research — plan
intent: 2026-11-22-tw-equity-research@0bcc3bb
spec: docs/loom/2026-11-22-tw-equity-research/spec.md@0cb232d
charter: 1.1

## Task DAG

**W1-01 Taiwan disclosure acquisition** after: none acceptance: 2, 3
- Files: obsidian-finance/skills/tw-equity-research/scripts/acquire.py, obsidian-finance/tests/test_tw_equity_acquire.py
- Test: A2 positive: monthly-as-of; boundary: future-month; A3 positive: full-disclosure-body-and-filing; negative: failed-query-or-missing-body.
- Risk: REQ-2/3 — agent-decided: distinguish public-time revisions, successful empty returns, and retrieval failures.

**W1-02 Conference acquisition and locally timed transcript** after: none acceptance: 4, 5
- Files: obsidian-finance/skills/tw-equity-research/scripts/conference.py, obsidian-finance/tests/test_tw_equity_conference.py
- Test: A4 positive: transcript-or-local-recording-fallback; negative: transcription-failure; A5 positive: timestamp-and-source; boundary: unavailable-evidence.
- Risk: REQ-4/5 — agent-decided: keep the acquisition status and original recording independently of derived text.

**W2-01 Stable Traditional Chinese notes** after: W1-01, W1-02 acceptance: 1, 6
- Files: obsidian-finance/scripts/research_store.py, obsidian-finance/tests/test_research_continuation.py
- Test: A1 positive: numbered-tw-stable-path; boundary: ticker-collision-and-edit-conflict; A6 positive: existing-us-resume; boundary: legacy-us-path.
- Risk: REQ-1/6 — agent-decided: select a fixed Taiwan role map from the market-scoped issuer key and preserve existing US path handling and test_research_continuation.py coverage.

**W3-01 Public Taiwan skill and integration** after: W2-01 acceptance: 1, 2, 3, 4, 5, 6
- Files: obsidian-finance/skills/tw-equity-research/SKILL.md, obsidian-finance/README.md, obsidian-finance/tests/test_tw_equity_workflow.py, obsidian-finance/.codex-plugin/plugin.json, obsidian-finance/.claude-plugin/plugin.json, .claude-plugin/marketplace.json
- Test: A1 positive: six-quarters; boundary: three-transitions; A2 positive: filed-vs-monthly; boundary: quarter-only-forecast; A3 positive: correction-revision; boundary: historical-cutoff; A4 positive: no-caption-fallback; negative: unavailable-recording; A5 positive: page-and-guidance; boundary: unreadable-cell; A6 positive: us-entry-resume; boundary: cross-market-routing.
- Risk: REQ-1–6 — agent-decided: reuse quarterly publication and recovery APIs and verify through a fresh session.

## Acceptance cohort

W3-01 runs six real company-quarter cases through the fresh packaged Taiwan skill and records evidence separately from deterministic fixtures. Run 2025Q2–Q3 for each issuer, retaining contemporaneous cutoff evidence and three quarter transitions. Use early monthly and post-filing observations in at least one transition. Cover the annual-report gate with a dedicated fixture and exercise corrections and missing announcement bodies in controlled cases unless matching public cases are verified.

- TSMC (2330). [Monthly releases](https://investor.tsmc.com/chinese/monthly-revenue/2025) and [financial calendar](https://investor.tsmc.com/english/financial-calendar) provide issuer-side reference dates and materials.
- Hon Hai (2317). [Company IR](https://www.foxconn.com.tw/zh-tw/investor-relations/investor-relations-activities/investor-conference) provides conference slides and transcripts for cross-checking.
- Delta Electronics (2308). Dated issuer releases support historical monthly revenue for both quarters. [Cohort evidence](evidence/final-cohort.md). China Electric remains the independently exercised no-caption recording case.

## Simplicity check

- Reuse stable quarterly storage — taken
- Separate analyst entry from public download entry — declined: one Taiwan research entry covers the confirmed workflow

## Questions asked

① — what — 可以把這版草案定稿，開始寫規格嗎？
② — behaviour — 以上是你要的使用行為嗎？
② — behaviour — 這兩個情況的處理符合你的預期嗎？
② — behaviour — 你希望採用「查到研究截至日，季後公告只納入與當季相關的項目」嗎？
② — behaviour — 差異發生時，你希望在報告正文並列兩筆數字，還是讓正文只顯示正式季報數字？
② — behaviour — 這個處理方式符合你的預期嗎？

## Risks

1. The current issuer pages establish example coverage. Verify all historical source versions and actual publication timestamps before asserting acceptance.
2. Source availability, absent transcripts, corrections and concurrent edits can alter completion without changing note names.
