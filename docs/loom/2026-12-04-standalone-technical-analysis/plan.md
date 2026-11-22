# Standalone stock technical analysis — plan
intent: 2026-12-04-standalone-technical-analysis@71811c5
spec: docs/loom/2026-12-04-standalone-technical-analysis/spec.md@39769fc
charter: 1.1

The standalone skill owns the new entry point. Use evidence and note protection from quarterly research as design references. Keep the existing quarterly entry point and storage contract intact.

## Task DAG

**W0-01 Validate and normalize a local snapshot**  acceptance: 2, 3
- Files: `obsidian-finance/skills/technical-analysis/scripts/snapshot.py` (entry), `obsidian-finance/tests/test_technical_snapshot.py`
- Test: A2 positive: stable-input-identity; boundary: different-adjustment-version. A3 positive: evidenced-historical-version; negative: later-adjusted-download-trimmed-to-cutoff.
- Risk: REQ-2/3 agent-decided — require snapshot capture/publication by cutoff or traceable point-in-time evidence for the exact data version and adjustments. Session completion and row dates alone cannot establish availability.

**W1-01 Compute indicators and evaluate technical rules**  after: W0-01  acceptance: 1, 2
- Files: `obsidian-finance/skills/technical-analysis/scripts/analyze.py` (entry), `obsidian-finance/tests/test_technical_analysis.py`
- Test: A1 positive: chart-structure-volume-and-momentum; boundary: warmup-and-unconfirmed-pattern. A2 positive: repeat-identical-input; negative: future-bar-changes-past-confirmation.
- Risk: REQ-1/2 agent-decided — use Python for returns, SMA, and volume; compare TA-Lib against monkey-skills fixtures before adding any selected indicators that justify the dependency. Keep rules distinct from indicator calculations and bind levels and observations to dated bars.

**W1-02 Acquire latest completed US daily bars**  after: W0-01  acceptance: 1, 3
- Files: `obsidian-finance/skills/technical-analysis/scripts/fetch_daily.py` (entry), `obsidian-finance/tests/test_technical_fetch.py`
- Test: A1 positive: provider-to-local-snapshot; negative: isolation-dependency-or-provider-failure. A3 positive: completed-shortened-session; negative: valid-looking-in-progress-bar.
- Risk: REQ-1/3 agent-decided — isolate yfinance, choose an explicit adjustment basis and verify exchange schedule including holidays and early closes. Record fetch time and settings; keep live network outside ordinary tests.

**W2-01 Publish dated outlooks and evidence**  after: W1-01, W1-02  acceptance: 2, 4, 5
- Files: `obsidian-finance/skills/technical-analysis/scripts/report.py` (entry), `obsidian-finance/tests/test_technical_report.py`
- Test: A2 positive: note-links-exact-source-and-method; boundary: partial-evidence. A4 positive: localized-note-with-chart; negative: collision-symlink-and-partial-write. A5 positive: three-dated-outlooks; boundary: month-end-leap-year-and-insufficient-long-history.
- Risk: REQ-2/4/5 agent-decided — separate evidence and outlook dates. Confine output to the designated vault, reuse no-clobber staging patterns, and publish the note after its assets are ready.

**W3-01 Verify the shipped skill entry point**  after: W2-01  acceptance: 1, 3, 4, 5
- Files: `obsidian-finance/skills/technical-analysis/SKILL.md` (entry), `obsidian-finance/README.md`, `obsidian-finance/.codex-plugin/plugin.json`, `obsidian-finance/.claude-plugin/plugin.json`
- Test: A1 positive: ticker-only-latest; negative: network-unavailable. A3 positive: local-historical-replay; negative: unverifiable-version. A4 positive: save-on-request; negative: read-only-conversation. A5 positive: three-horizons; boundary: one-unavailable-horizon.
- Risk: REQ-1/3/4/5 agent-decided — document isolated setup and import/smoke checks for external dependencies. Verify live fetching separately and run the two-package regression suite. Check publication metadata against supported behavior.

## Simplicity check

- Keep the first calculations dependency-free and benchmark TA-Lib only for required indicators — taken
- Reuse existing vault-confinement and no-clobber staging patterns with report-scoped cleanup — taken

## Questions asked

① — what — 你確認先按離線首版規劃嗎？
② — behaviour — 這三個預設長度和呈現方式符合你的意思嗎？
① — what — 確認把這項語言規則納入首版嗎？
② — behaviour — 這三種存檔行為符合你的預期嗎？

## Risks

1. Live data may be stale, adjusted retroactively, or incomplete. Capture raw response provenance and eligibility decisions. Report unreliable coverage without deriving unsupported findings.
2. Pattern labels and numerical indicators do not establish future outcomes. Require dated evidence and conditional outlooks, and keep a horizon present when evidence is too sparse.
3. Reuse confinement and staging patterns in `research_store.py` and `industry_update.py` with cleanup scoped to newly created report assets. Test concurrent collisions and escaping symlinks for note and attachments; verify existing files survive.
4. Installation and public entry behavior may vary by host. Record the tested package versions and host, and distinguish source regressions, live acquisition, and a fresh-session skill invocation.

5. Localize presentation in the agent using the same verified report values, then publish the Markdown through the guarded writer with reproducible evidence and chart links. Verify Traditional Chinese, Japanese, and an explicit English override.
