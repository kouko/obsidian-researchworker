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
