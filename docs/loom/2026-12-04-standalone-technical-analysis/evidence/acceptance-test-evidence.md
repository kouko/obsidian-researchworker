# Standalone stock technical analysis — acceptance test evidence

Tried on 2026-12-04, in a clean copy of the project at 81af4ad24ece773ab97c96ca27b1c39807cef7f5.

The clean clone was at `/private/tmp/obsidian-ta-accept.5kdjw3/source`. Its review input was the committed tree. Followed the package README to the standalone skill and checked its isolated interpreter imports, yielding yfinance 1.8.0 and exchange-calendars 4.13.3. The captured provider timestamp below is the executing environment's reported clock, separate from the project acceptance date. The full suite is owned by finalization: `python3 -m pytest obsidian/tests obsidian-finance/tests -q -p no:cacheprovider`.

## 1. Standalone U.S. daily stock analysis

- How I tried it: invoked the clean copy's `fetch_daily.py AAPL` with the isolated interpreter, then ran `python3 report.py independent-live.json` without the provider environment.
- What came back: successful fetch produced 501 bars, newest 2026-11-20. The short horizon reported +1.33%, SMA 347.307, volume 1.69× and a sideways assessment. Medium and long showed rising confirmed swings.
- Evidence: `independent-live.json` and `independent-live-report.md` under the temporary acceptance root. Independently computed SMA 347.3065719604492 and volume ratio 1.6868354147766491 from the input rows.

## 2. Reproducible dates, numbers and provenance

- How I tried it: reran `report.py` with `--cutoff 2026-11-22T12:43:08.087097+00:00` and compared stdout to the default analysis from the same snapshot. Also reran against an attachment saved by the report command.
- What came back: both byte comparisons passed. Report identified Yahoo Finance, America/New_York, the actual observed date windows, the adjusted price method, snapshot identity and calculation settings.
- Evidence: `independent-live-report.md`, `live-report.md`, `replay.md` and `vault/Independent AAPL.source.json` under the temporary root.

## 3. Data eligibility and gaps

- How I tried it: replayed the public data with `--cutoff 2024-02-29T16:30:00-05:00` and ran the stock snapshot and fetch tests. Marked the last bar incomplete in a disposable copy and reran.
- What came back: all three historical windows remained visible and insufficient, with the captured version excluded. The incomplete case excluded November 20 and the observation ended November 19. Ten focused tests passed, including post-cutoff and unverifiable local versions, early close and latest completed session handling.
- Evidence: `historical-ineligible.md`, `incomplete-report.md`, `test_technical_fetch.py` and `test_technical_snapshot.py`.

## 4. Conversation output and separate note

- How I tried it: opened a fresh Codex conversation with the clean-copy skill explicitly supplied and prompted it to execute the local report, present all three time scales in Traditional Chinese, and avoid storage. Independently ran the save command with `--vault /private/tmp/obsidian-ta-accept.5kdjw3/vault --note 'Reproduced outlook.md'`.
- What came back: usable Markdown on stdout. Opt-in save produced a separate 3,373-byte note, a 44,237-byte price/volume SVG, and a 127,125-byte snapshot attachment. The same-name retry exited 1 with a file exists error.
- Evidence: `fresh-conversation.log`, `fresh-conversation.txt`, `independent-live-report.md` and the three `Reproduced outlook` files in the isolated vault. Codex session `01a20349-860c-77e3-90e0-24cfeb5f011f` executed `python3 -B obsidian-finance/skills/technical-analysis/scripts/report.py /private/tmp/obsidian-ta-accept.5kdjw3/independent-live.json` (exit 0) and returned the three observed and forward windows, directions, price levels and latest volume in Traditional Chinese. Installed discovery was not exercised by this source invocation.

## 5. Short, medium and long outlooks

- How I tried it: inspected the full Markdown, repeated with a 25-row fixture and checked the leap-day historical cutoff case.
- What came back: full windows were 2026-11-23 through 2026-12-13, 2027-02-22 and 2027-11-22. Observed sessions were separately listed. The short fixture retained all three ranges and marked the medium and long outlooks insufficient. Long leap-day forward window ended on 2025-02-28.
- Evidence: `independent-live-report.md`, `short-report.md` and `historical-ineligible.md`.

## 6. Latest analysis

- How I tried it: followed the live CLI path in section 1.
- What came back: the raw snapshot included the provider capture time and latest completed session. Standard-library report ran from the resulting snapshot.
- Evidence: `independent-live.json`.

## 7. Historical or local analysis

- How I tried it: used the explicit cutoff equal to the captured snapshot version, then an earlier cutoff, as in sections 2 and 3.
- What came back: the eligible version reproduced the report and the earlier cutoff retained all outlook windows with exclusions.
- Evidence: `independent-live-report.md` and `historical-ineligible.md`.

## 8. Missing input

- How I tried it: attempted the public fetch with the normal outer sandbox, then used an existing local snapshot. Separately tested a shortened snapshot.
- What came back: the sandbox prevented DNS resolution and the fetch exited 1 with a clear error. The local path still produced a report and disclosed insufficient coverage for the shortened windows. The retried public fetch with network permission succeeded.
- Evidence: DNS exception `Could not resolve host: query2.finance.yahoo.com` and `short-report.md`.

## 9. Save

- How I tried it: used the temporary vault and repeated the same filename as in section 4.
- What came back: first save generated readable attachments and the second refused the collision.
- Evidence: `vault/Reproduced outlook.md` and its two attachments.

## 10. Intraday and partially covered week

- How I tried it: used the incomplete bar fixture, the early-close boundary test in the isolated clean checkout and the independently fetched complete daily snapshot.
- What came back: the incomplete bar was excluded; early-close evidence passed; the long report explained daily fallback where complete consecutive exchange weeks could not be verified.
- Evidence: `incomplete-report.md`, `test_technical_fetch.py`, and the long-horizon limitation in `independent-live-report.md`.

## Re-run on 2026-12-04, at a720144f27874f141d21be522c48ccb668c2e5bb

The clean clone was `/private/tmp/obsidian-ta-retest.vJhlBR/source`. Re-read the revised skill's separate latest and historical CLI examples. Ran the four focused technical test modules in that clone, yielding 27 passes. Paths in the following entries refer to this temporary acceptance root unless otherwise noted.

- 1: re-tested — ran the clean copy's `fetch_daily.py AAPL` with the verified isolated interpreter, and ran `report.py` using both the new capture and the previous retained local snapshot. New capture has 501 bars, latest 2026-11-20. `latest.md` and `historical.md` retain the original price, average, volume and directional evidence.
- 2: re-tested — regenerated the earlier report with explicit cutoff `2026-11-22T12:43:08.087097+00:00`, saved it, then regenerated from `vault/Historical.source.json` with the same cutoff. Both comparisons with the earlier report were byte-identical; source, timezone, observed trading dates, price adjustments and settings remain visible.
- 3: re-tested — exercised unavailable historical version, incomplete latest session, and a disposable capture marking interior 2026-11-09 incomplete. `ineligible.md` excludes the whole newer version. `incomplete.md` stops observations on November 19. `gap.md` excludes November 9, marks all three horizons insufficient and explains why the 20-session average lacks a complete window. Focused tests also cover unverifiable and post-cutoff data.
- 4: re-tested — compared the latest and historical Markdown outputs and saved each using its documented command and a distinct new filename. Fresh-session execution of the latest path carries over from section 4: that user prompt, report command and output are unchanged, and the eligible snapshot's output remained identical. The historical invocation/attachment path was tested again. Installed discovery remains unverified.
- 5: re-tested — `latest.md` retains the three outlooks starting 2026-11-23 and ending 2026-12-13, 2027-02-22 and 2027-11-22. Their observed trading starts are 2026-11-02, 2026-08-24 and 2025-11-24, all ending 2026-11-20. `short.md` retains all three rows with insufficient medium and long coverage. The leap-day historical case again ends the long window on 2025-02-28.
- 6: re-tested — public fetch exited 0 with permitted network access. `live.json` records capture `2026-11-22T12:48:01.091709+00:00` and latest expected session `2026-11-20`; its report includes all horizons.
- 7: re-tested — supplied the earlier eligible capture as the historical snapshot with its explicit cutoff, then a cutoff before capture. The former reproduced the earlier report and the latter reported ineligibility while preserving the three outlook ranges.
- 8: re-tested — fetch in the ordinary outer sandbox exited 1 with a DNS error; offline report and shortened-data report still ran normally.
- 9: re-tested — latest and historical save both created a note, SVG and source attachment in the isolated vault. A same-name latest save exited 1 with a file-exists error.
- 10: re-tested — incomplete-session local input was excluded, the focused fetch tests passed including early close, and the output explained the daily fallback for unverifiable complete consecutive exchange weeks.

## Re-run on 2026-12-04, at 7b81346b7a7ab819bfc0c767ddeaa72bfa971814

Clean clone: `/private/tmp/obsidian-ta-language.1HSBh2/source`. Source input was the previous independently fetched public AAPL capture, copied to `snapshot.json`. No live access was needed for this save-only change. Ran the clean copy's `report.py snapshot.json` to establish the canonical `reference.md`.

- 1: carried over — acquisition, snapshot, and analysis code are unchanged in the diff, and the canonical AAPL report was reproduced.
- 2: re-tested — compared decoded snapshot JSON against the input and replayed each `vault/{zh,ja,en}.source.json` through the clean copy's `report.py`. All three canonical reports were byte-identical. The attachment JSON uses normalized formatting and retains the same decoded data.
- 3: carried over — load, cutoff and exclusion logic are unchanged in the diff.
- 4: re-tested — three fresh Codex sessions explicitly read the clean copy's local skill and used the fixed public snapshot. Session `01a20396-fa6a-7460-8403-925d9fd78fb5` used a Traditional Chinese prompt and saved `vault/zh.md`. Session `01a20396-fa69-7700-b0f7-7c86e88639f7` used a Japanese prompt and saved `vault/ja.md`. Session `01a20396-fa6a-7930-89a7-e0fa0e2c857f` used a Chinese prompt with an explicit English note request, saved `vault/en.md`, and gave a Chinese response. Inspected the notes and verified their local chart and snapshot links resolve, their SVG files parse, and source URL, snapshot identity, dates and exact decimal values from the canonical report occur in all three notes. Initial dynamic temporary-path shell redirects were refused by the host guard. The sessions saved using allowed file-writing tools and the documented publisher. Installed automatic discovery was not tried.
- 5: re-tested — all three notes contain the three outlooks starting 2026-11-23 and ending 2026-12-13, 2027-02-22, and 2027-11-22. Observed trading starts are 2026-11-02, 2026-08-24, and 2025-11-24, all ending 2026-11-20. The directions were sideways, up, and up. Insufficient-coverage behavior carries over because the report and analysis path is unchanged for canonical output.
- Save flow: passed a new localized draft with `--note-markdown` while targeting existing `vault/en.md`. The command exited 1 with a file-exists error. SHA-256 values for the prior note and both attachments matched before and after. Added verification command `python3 -B verify-acceptance.py` in the isolated root.
