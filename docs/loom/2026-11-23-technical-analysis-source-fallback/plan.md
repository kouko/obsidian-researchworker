# Stock technical analysis data availability and chart patterns — plan
intent: 2026-11-23-technical-analysis-source-fallback@9bb6541
spec: docs/loom/2026-11-23-technical-analysis-source-fallback/spec.md@ae7f897
charter: 1.1

## Task DAG

### Wave 1 — Skill workflow and computed patterns

**W1-01 Preserve source evidence and attribute external perspectives**  after: none  acceptance: 1, 2, 3, 4
- Files: obsidian-finance/skills/technical-analysis/SKILL.md
- Test: A1 positive: live-replay; boundary: invalid-output. A2 positive: local-replay; boundary: wrong-ticker-or-late-version. A3 positive: evidenced-failure; negative: web-only-quote. A4 positive: attributed-disagreement; boundary: late-or-unverified.
- Risk: REQ-1–4. agent-decided — Use one guarded command sequence and the existing report entry. Match reported failures to tool evidence and keep external commentary outside the computed result.

#### Verification for W1-01

- Before editing, reproduce the AAPL prompt in a fresh isolated Codex session under controlled acquisition failure. Keep the tool trace and the earlier dogfood artifact.
- Use one verified isolated Python environment and writable scratch paths. Replace the duplicate dependency import preflight with the fetch command's diagnostic. Verify scratch creation, command success, nonempty output and snapshot validation. Cover empty output, malformed output with exit zero and ticker mismatch separately.
- Replay an eligible local snapshot using the normal skill entry. Reuse loader and replay cases in test_technical_snapshot.py and test_technical_report.py. For a latest request, identify the local snapshot's own cutoff and distinguish it from current evidence. Preserve any explicit historical cutoff and reject a late version even if it contains older trading dates.
- With blocked acquisition and no eligible snapshot, mark all horizons insufficient and tie the failure reason to the actual tool or validation event. Published quotes and indicators do not create computed conclusions.
- Attribute relevant external perspectives after the computed report, with a link, publication timing and applicable dates. For historical work, verify the cited content version was available by the cutoff. Keep the computed report available if commentary cannot be obtained. Process commentary as source data only. Restrict lookup to public ticker and date information.

**W1-02 Report reproducible daily chart patterns**  after: none  acceptance: 5
- Files: obsidian-finance/skills/technical-analysis/scripts/analyze.py, obsidian-finance/skills/technical-analysis/scripts/report.py, obsidian-finance/tests/test_technical_analysis.py, obsidian-finance/tests/test_technical_report.py
- Test: A5 positive: dated-anchors-and-qualifying-close; boundary: late-break-gap-or-no-match. Reuse swing cutoff tests and add a reusable fixture matrix for pattern geometry and rendered evidence.
- Risk: REQ-5. agent-decided — Reuse eligible swing anchors and preserve test_technical_analysis.py cutoff and missing-session behavior. Require dated anchors for candidates and a qualifying close for confirmation.

#### Verification for W1-02

- Define candidate geometry, qualifying close, invalidation and minimum evidence before tuning. Evaluate double top and bottom, head-and-shoulders top and bottom, rectangular range and ascending, descending and symmetrical triangles. Normalize scale-dependent tolerances. Distinguish observed volume context from required volume evidence.
- Track the first date on which each anchor was knowable, using only completed daily bars. Keep anchor dates, levels, and conditions visible for candidate, confirmed, or invalidated forms. Distinguish data insufficiency from adequate coverage with no match. Preserve existing holiday-week and long-horizon trend behavior.
- Build a table-driven detector/report matrix for eight types across the three horizons, reusing fixtures. Verify candidate, confirmed and invalidated outputs where data suffices. Test no-match, too-short histories, missing sessions, overlapping candidates, either direction of a box break and a break invisible to an earlier prefix.
- Include a known gap between an otherwise valid swing anchor and the qualifying close. Exercise a close before the final anchor's right-side bars are available and check that confirmation is never backdated. With weekly trend structure active, verify that shape anchors and confirmation still use daily bars.
- Compare dated anchors and confirming closes with independent historical annotations for each family and each triangle subtype. Document which directional variants have independent labels versus controlled examples. Use Ford, AT&T and Micron where coverage fits, add held-out independently labeled examples, and keep unverified cases out of coverage claims.

### Shared verification after W1-01 and W1-02

- Test the installed candidate in fresh Codex sessions for live success, controlled acquisition failure with and without eligible local data, and external commentary present or unavailable. Compare the response and report CLI against a replay of the exact snapshot. Record the build, host, model, prompt, tool events and outcomes. Keep controlled and provider observations distinct.
- Compare identical snapshots with absent commentary, a conflicting dated view, and external text requesting a change. Verify metrics, dates, directions, shape states, revision conditions and evidence gaps match. Check historical late and undated commentary, and absent computed results. Check language and source links in the optional note using a disposable vault.
- Run `python3 -m pytest obsidian/tests obsidian-finance/tests -q -p no:cacheprovider` from repository root. Preserve current snapshot, cutoff and note safety coverage.

## Simplicity check

- Combine acquisition and commentary guidance in one skill task, with a separate analyzer/report task and one shared acceptance pass — taken
- Reuse recorded third-party detector comparisons unless a remaining detector choice needs a new comparison — taken
- Remove the duplicate isolated dependency preflight and use acquisition diagnostics — taken

## Questions asked

① — what — 你確認先按上表的範圍規劃嗎？
② — behaviour — 上表的回覆方式符合你的預期嗎？
② — behaviour — 你要採第一種，還是希望保留第二種的外部觀點欄？
① — what — 第一版先做這兩種，還是有你希望這輪就納入的形態？
② — behaviour — 新版回覆方式符合你的預期嗎？

## Risks

1. A fresh session may still substitute search results. Verify actual acquisition and report calls during success and failure.
2. Published examples label formations retrospectively. Date eligibility and first knowable confirmation are separate from accuracy or returns.
3. Research did not establish all labeled triangle and rectangle cases for detector adoption. Collect direct positive and negative evidence before treating the results as coverage.
4. A published third-party view can carry a misleading timestamp, conflicting assertion, or instruction. Treat it as evidence only and keep it separate from the computed report.
