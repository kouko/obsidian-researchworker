# Technical analysis source fallback — acceptance evidence

Tried on 2026-11-23, on functional revision `80e6a82556c3db5ac9fba76c4ac03bad1fc47b19`. The README local marketplace path resolved to the finance package. I compared the isolated clean source export `current-source/obsidian-finance` with the installed finance directory under `current-home/plugins/cache/obsidian-researchworker` recursively, excluding only generated Python cache files. They matched. Run directory: `/private/tmp/technical-analysis-acceptance-20261123`. Fresh sessions used ephemeral Codex, `gpt-6.2-sol`, workspace-write sandbox, disabled memory, and the isolated installed plugin. See the final re-run below. Sections 1–13 retain the first complete trial on `0363964ba87e672e10d4e982e365c4ae2d92e6e1` for comparison. The initial replay harness `verify-installed.py` also ran four separate ephemeral sessions, with public live data enabled for one and deterministic acquisition failure or supplied snapshots for the others.

## 1. Reproducible current analysis

- How tried: `verified-live.jsonl` captured the installed skill's genuine `uv run` provider call, nonempty-file and ticker validation, and installed `report.py` output. I separately ran the installed `python3 report.py /private/tmp/technical-analysis.xvAplNdz/daily.json` and captured stdout at `/private/tmp/ta-acceptance-independent-live.md`.
- Actual: Latest completed session 2026-11-20, close 342.56, volume 1.69×, cutoff 2026-11-23T00:45:00.395620+00:00. Short sideways +1.33%, medium bullish +10.47%, long bullish +24.58%. The live chat reproduced dates, moving averages (347.307, 341.585, 302.786), support (325.083, 307.976, 242.575), and the shared 360.83 resistance. It identified provider, adjusted data, and the precise capture time. The provider version string was present in the snapshot and absent from prose.

## 2. Eligible local fallback

- How tried: `verified-local.jsonl` shows the controlled acquisition stub returning exit 73 and “Controlled outage: daily-data acquisition disabled for replay.” The session read the explicitly supplied local input and ran its installed `report.py`. I separately replayed this input into `/private/tmp/ta-acceptance-independent-local.md`. The two independent CLI reports differ only in cutoff, snapshot availability time, and snapshot identity.
- Actual: Chat and saved note state `yfinance/1.8.0 captured 2026-11-22T17:01:57.991391+00:00`, with the identical instant as cutoff. Local route retained calculations for all three supported horizons and described the failed live attempt.

## 3. Unavailable qualifying data

- How tried: `verified-outage.jsonl` reproduced the exit 73 diagnostic in an empty workspace. `verified-late.jsonl` supplied a local Yahoo snapshot captured on 2026-11-22 to a request for `2026-11-21T00:00:00-05:00`.
- Actual: Both provided all three horizons as insufficient, with no stock direction, moving average, or price-level substitution. The historical response distinguished the date of the last row from when that adjusted data version was available. There was no external lookup or note write.

## 4. External perspective

- How tried: Compared independent CLI replays against the two session replies and local note. Inspected the lookup event records in `verified-live.jsonl` and `verified-local.jsonl`.
- Actual: Live chat attributed TickerLevels' November 20 daily analysis after the computed content and explicitly preserved computed sideways despite external bearishness. Its search trace includes the source link and an opened-page result. The local mode cited the 2026-11-03 Beating The Bull PDF for its 2026-11-02 chart and kept quoted support levels within the separately attributed section. The trace confirms the PDF result and title/date. Query text only used public ticker, date, and market quote. The live session started searching before the report completed, then presented the calculated result first. Neither the captured late-input nor outage case exercised late or undated commentary with a valid computed report. A source text carrying embedded instructions was not run in these four sessions.

## 5. Daily chart patterns

- How tried: In `verified-source`, ran `python3 -m pytest obsidian-finance/tests/test_technical_analysis.py obsidian-finance/tests/test_technical_report.py obsidian-finance/tests/test_technical_snapshot.py -q -p no:cacheprovider`. All 39 passed. The suite covers the eight pattern types, lifecycle, cutoff and missing-session distinctions, rendering, and preservation of notes and assets. The separately recorded independent CLI probe covers the earlier false rectangle-break regression. Package gate command: `python3 -m pytest obsidian/tests obsidian-finance/tests -q -p no:cacheprovider`.
- Actual: AAPL short showed no match. Medium and long both showed candidate double top and invalidated rectangle and ascending triangle. Long additionally showed invalidated double bottom, descending and symmetrical triangles. The rendered live response and local note included dated anchors. The local final chat omitted some matched patterns' dated anchors and conditions. Both localized surfaces used an ambiguous rendering of a downside breakout's recross condition. The underlying rule compares the later daily close with the lower boundary after a downside break.
- Historical check: [Independent reference replay](historical-pattern-replay.md) documents the rule's behavior against eight separately published formations. Same-type signals with different dates and anchors do not establish agreement. Ford, Pfizer, AT&T, Micron and Nucor diverged from the reference, Nvidia showed related geometry but confirmed on a different date, and exact Archer Daniels Midland and Transocean alignment remained unresolved. This retrospective sample establishes neither trading performance nor detection accuracy.

## 6. Current data available

- Actual: Installed skill was selected from the plain prompt. The successful tool trace and independent replay in 1 cover the distinct observed and forward periods.

## 7. Current data unavailable, local snapshot eligible

- Actual: The controlled fallback in 2 created exactly `verified-vault/replay.md`, `replay.chart.svg`, and `replay.source.json`. Note prose is Traditional Chinese with source links, relative chart and snapshot references. Parsing and comparing the JSON sidecar with the authorized input produced equal objects, including every daily bar. The chat gave the requested outlook before creating the file.

## 8. No usable data

- Actual: The exit 73 case in 3 reported the actual local diagnostic and retained three named insufficient-data horizons. An eligible local snapshot or restored acquisition was stated as the needed evidence.

## 9. Retry with new evidence

- Actual: The explicit historical version rejected in 3 never changed the requested cutoff. The separate eligible local fallback in 2 produced calculations.

## 10. Pattern present

- Actual: The live report and saved local note included matched dates and prices. The local chat failed to expose full dated evidence for the other patterns after presenting the double top. See 5.

## 11. Pattern absent or unassessable

- Actual: Short-horizon AAPL had adequate input for evaluation and no matching shape. The outage and late-version cases could not evaluate shapes. See 3 and 5.

## 12. External perspective available

- Actual: The conflicting technical perspective was attributed separately and left the computed short-horizon direction and revision levels intact. See 4.

## 13. External perspective unavailable

- Actual: Both unsupported input cases omitted commentary, but a supported computed report with all external sources unavailable or ineligible was not independently observed for this revision.

## Re-run on 2026-11-23, at `0363964`

- The complete current, local, outage and late-version sessions superseded earlier candidate runs. The former omission was resolved for the live chat and persisted on the local chat surface. No verdict in this record relies on an earlier candidate response.

## Re-run on 2026-11-23, at `80e6a82`

- **1, 6 — Live success.** `current-live.jsonl` shows the same normal AAPL request and a successful real fetch via the installed package, with output at `/tmp/technical-analysis.F0Up0AcU/daily.json`. The adjusted source, source version, snapshot identity, availability and cutoff `2026-11-23T00:49:43.106429+00:00` appear in the chat. The independent replay `/private/tmp/ta-acceptance-current-live.md` matches the displayed moving averages, returns, levels, directions and observed/forward date ranges. The close was 342.56, volume 80,464,200 (1.69×), and the conditional directions remained sideways, up, up.
- **2, 7 — Controlled failure with authorized local fallback and note.** `current-local.jsonl` captures exit 73 on the live arm and the installed report command on the supplied 501-bar input. I independently ran the installed report on `current-local/aapl.json` into `/private/tmp/ta-acceptance-current-local.md`; the replay differs from the live report only by cutoff, availability timestamp and snapshot identity. Both final chat and saved report state all three together with the version and limits. In the disposable `current-vault`, only `replay.md`, `replay.chart.svg` and `replay.source.json` were created. The source sidecar decodes to the same JSON object as the authorized input and both attachment links resolve. The chat contained the requested three-period update before saving.
- **3, 8, 9, 11 — Insufficient evidence and retry behavior.** `current-outage.jsonl` reports the actual exit 73 diagnostic and three unsupported horizons. The session searched the web and read metadata of sibling fixtures outside the selected empty working directory. It did not use those results for conclusions, and it did not write a note. `current-late.jsonl` retains the exact `2026-11-21T00:00:00-05:00` cutoff and explains why the post-cutoff version is ineligible despite containing earlier bars. Neither response borrowed public quotes, directions or levels. Current and local successful CLI replays found sufficient short-period data but no matching pattern.
- **4, 12 — Available external view.** The current live response attributed IndicatorStack's 2026-11-20 19:55 ET source update after the computed report, identifying its 11-20 applicability and leaving the three independently replayed directions and revision criteria intact. The live trace shows a lookup began before the report command even though the final output placed the computed report first. The older fresh live trial demonstrated a directly conflicting TickerLevels opinion. No external source supplied a missing computed indicator or confirmed a computed shape.
- **4, 13 — Ineligible external views with valid historical input.** `current-commentary-boundary.jsonl` used `current-local/aapl.json` and explicitly requested cutoff `2026-11-22T17:01:57.991391+00:00`, chat only, and two supplied test candidates. The first test candidate was initially published on November 20 at 19:00 ET and its supplied version was revised on November 24 at 10:00 ET. The second had no date. The session ran the installed report with the exact cutoff, kept all three computed directions, figures, conditions and dated shapes, and explained that both candidates were excluded. It made no external lookup and no save. Embedded instruction handling was not exercised separately.
- **5, 10 — Dated pattern evidence.** I reconciled live chat, local final chat and local note with their independent CLI replays. All six distinct matched patterns appear on all three surfaces, with the three shared patterns explicitly attributed to both applicable horizons. The dates, anchor prices and availability dates, boundaries, reasons, and historical close/threshold/volume evidence match. For the candidate double top the final report now says the close must return above the lower boundary after a downside break for invalidation; after the rectangle's upside confirmation a close below the upper boundary invalidates. In the captured 2026-06-25 descending-triangle confirmation, the precise 107,013,700 shares equal the original input, removing the prior rendering's significant-digit rounding. For all eight supported pattern types the focused test command in section 5 returned 39 passed on the final clean source. The station's package suite recorded 496 passed and the independent flat-pattern CLI probe recorded four passed. The full suite also runs as a gate before acceptance.
- **5 — External reference replay.** I separately ran `PYTHONDONTWRITEBYTECODE=1 /private/tmp/chart-pattern-pilot-20261123/env/bin/python /private/tmp/chart-pattern-pilot-20261123/candidate-reference.py` from the final branch, capturing `/private/tmp/ta-acceptance-independent-references.jsonl`. The eight ticker records are equal to the prior reference run after excluding only the intentionally clarified invalidation wording. All anchor prices/dates, status transitions and event volumes are unchanged. The five clear deviations, one related geometry with a different confirmation date and two unresolved alignments described in section 5 still apply.
