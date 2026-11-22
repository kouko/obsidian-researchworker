# Taiwan quarterly equity research — acceptance test evidence

Tried on 2026-11-23, in a clean copy of the project at b1d1116. The six research publications were produced in disposable vaults before this integration and independently verified with the installed integrated package.

```sh
git archive b1d1116 | tar -xf - -C /tmp/tw-accept-independent-b1d1116/src
CODEX_HOME=/tmp/tw-accept-independent-b1d1116/profile codex plugin marketplace add /tmp/tw-accept-independent-b1d1116/src --json
CODEX_HOME=/tmp/tw-accept-independent-b1d1116/profile codex plugin add obsidian-finance@obsidian-researchworker --json
python3 -m pytest obsidian-finance/tests/{test_tw_equity_acquire,test_tw_equity_workflow,test_tw_equity_conference,test_research_continuation,test_research_markdown_templates}.py -q -p no:cacheprovider
python3 -m pytest obsidian-finance/tests/{test_quarter_publication,test_research_publication}.py -q -p no:cacheprovider
python3 /tmp/tw-accept-independent-b1d1116/verify.py
```

Installation returned obsidian-finance 0.1.0. The two focused test runs passed 118 and 31 tests, respectively. The package test command is `python3 -m pytest obsidian/tests obsidian-finance/tests -q -p no:cacheprovider`, run separately by closing review.

## 1. 能透過獨立的台股公司研究入口，在 Obsidian 建立及接續台灣上市公司的季度研究，並以三家台灣上市公司各連續兩季的完整研究驗收。每家公司都須驗證一次跨季接續。

- How I tried it: Imported `verify_quarter` and `workflow.assess` from the installed package, verified each saved overview, counted numbered files, recomputed SHA-256 for every referenced acquisition payload, and read each Q3 continuation.
- What came back: All six overviews were marked complete, all had eight stable numbered reports, and portable verification returned zero gaps. Reusable unit counts were 11 each for Hon Hai, 7 each for TSMC, and 7 each for Delta. Raw manifest checks passed 126/89, 108/110 and 44/53 references for the respective Q2/Q3 pairs, 530 total. Blanking either an in-quarter or a reviewed post-quarter disclosure body made readiness fail in all six cases. The portable check verifies saved coverage and source integrity, while readiness and substantive note inspection establish the stronger completion claim.
- Evidence: [Final acceptance cohort](final-cohort.md), `/tmp/tw-accept-independent-b1d1116/verified.log`. Hon Hai Q3 directly links Q2 valuation and reuses FY25 EPS cases 11.67, 13.04 and 14.25. TSMC Q3 records the Q2 forecast origin and separately compares dated original company guidance. Delta Q3 compares the Q2 replay baseline of NT$140 billion, 15.6%, and NT$6.73 EPS against NT$150.318 billion, 16.50%, and NT$7.16. Replay scenarios carry the actual authoring date.

## 2. 能在季報公布前看到當季已公布的月營收，並對照上一季對當季的預測。

- How I tried it: Replayed TSMC Q3 at August 9, 2025 Taipei day-end with the installed `acquire` and `assess` functions, original archived dated monthly payloads, and other endpoints deliberately unavailable. Inspected the Q2 issuer guidance preserved as `prior-guidance-2025Q3.md` and checked the complete Q3 forecast against it.
- What came back: July NT$323,166,000 thousand was eligible August 8. August, September and the Q3 filing remained unavailable at the cutoff. The July 17 forecast range of US$31.8–33.0 billion was available before the monthly actual. It applied to the whole quarter in USD, so it was displayed separately and could not score a July TWD actual. Once available, the same-period company-reported USD result of US$33.1 billion exceeded the guidance high by US$0.1 billion. A period-original analyst forecast for an individual month was unavailable in the observed cohort. A second installed-skill session saved a prefiling report at August 10 Taipei day-end, preserved this real forecast gap, and recorded the lookup progress. An isolated synthetic forecast version test used the same TWD consolidated July scope. Its test script selected the August 7 forecast of NT$320,000,000 thousand, excluded the August 9 revision made after the actual, and calculated +NT$3,166,000 thousand (+0.989375%). The installed store published the update in the same note and verified the retained revision.
- Evidence: `verified.log`, TSMC 2025Q3 forecasts and the prior-guidance source registration, [earlier actual prefiling snapshots](acceptance-progress.md#isolated-notebook-publication), `test_pre_filing_cutoff_excludes_quarterly_filing_and_future_disclosures`, and `/private/tmp/tw-month-version-proof/acceptance-result.txt` with `acceptance/logs/forecast-search.json` and `synthetic-selection.json`.

## 3. 能查到報告所用的季報、年報版本及分析採用的截至日期，並辨識尚缺的資料。

- How I tried it: Verified six quarterly release registrations, checked the archived China Electric annual index result, and ran the independent annual gate check.
- What came back: The tested quarterly cutoffs were 2025-08-16 and 2025-11-16 at 23:59:59 +08:00. The 1611 FY2024 annual index distinguished May 7 16:21:54 and August 8 13:39:57 original and corrected releases. The installed acquisition helper fetched both original PDFs, and an installed-skill session published 1611 2025Q1 checkpoints at June 15 and August 16, keeping the same Q1 original filing, research paths and dated annual versions. The checkpoints expose the missing January–March monthly revenue and material disclosure records.
- Evidence: `test_annual_gate_is_independent_and_requires_annual_report` [source acquisition evidence](acceptance-progress.md#source-acquisition), and `/tmp/tw-annual-version-proof/versions.json` with the two cutoff logs and `verify.log` under `vault/.acceptance/`.

## 4. 能看到法說會簡報、逐字稿與影音各自的取得狀態。取得的資料可回查，未取得的資料有查找紀錄。僅有可取得的影音時，能依時間戳從機器逐字稿回聽原音。

- How I tried it: Reopened the 1611 Q3 disposable vault's actual stored SRT, source record and conference analysis and checked the resulting SHA-256, timestamps and transcript statuses. Reran the fallback tests in the integrated tree.
- What came back: The archived TWSE recording produced 190 timestamped segments with no usable captions. The stored SRT matched its claimed SHA-256. The report traces 00:06:28–00:06:34 to the recording and explicitly records the missing slides and formal transcript. This is an independent inspection of the stored output of the earlier real Whisper run.
- Evidence: [Conference recording evidence](acceptance-progress.md#conference-recording), [TWSE recording](https://www.youtube.com/watch?v=bMWy8nvERVY), and `test_derived_timestamp_and_recording_provenance` plus `test_failed_transcription_and_search_gaps_are_explicit`.

## 5. 季度報告的財務實績數字可回查原始財報或官方量化揭露。能回查研究所用的 PDF 頁面，包括文字、圖片表格及圖表，並辨識無法可靠判讀的內容。引用法說會的展望、預期或策略時，能回查發言來源，並辨識其中的量化指引。

- How I tried it: Followed the references in TSMC Q3 financial analysis and forecast notes to the original registered filing and company briefing material and checked the notes for separation of actual and guidance figures.
- What came back: TSMC Q3 cites the original quarterly filing p.5 and notes 20 and 25, uses company presentation p.8 for labeled cash-flow figures, and identifies p.9's Q4 US$32.2–33.4 billion revenue guidance as a forecast. The 1611 managed note points to the relevant recording timestamp, using the filing for the financial actual. In a fresh installed-skill Codex session, a one-page controlled image-only PDF returned the correct table row, column, unit, both chart values and the page number. It named the covered cost-of-revenue cell, left its value unresolved, and withheld gross profit and gross margin.
- Evidence: TSMC quarterly vault, original PDF registrations and the Q3 `01 財務分析` and `04 預測` notes. The controlled fixture is `/tmp/tw-accept-independent-b1d1116/edge/pdf/filing.pdf` and the fresh-session log is `turn-auth.jsonl` in the same directory. It cited p.1 and reported revenue NT$158,420 thousand, Q2 shipments 84 thousand units and Q3 shipments 113 thousand units. [1611 source acquisition evidence](acceptance-progress.md#conference-recording).

## 6. 既有美股研究仍可接續。

- How I tried it: Confirmed that the renamed `equity-research-us` skill and templates are present in the merged installation. Ran the existing public-adjacent-quarter and fixed-quarter update tests using the renamed entry's templates.
- What came back: The tests passed and use the existing saved research layout. This check covered the installed entry files and their continuation contract.
- Evidence: `test_equity_skill_uses_fixed_quarter_publication_and_recovery`, `test_public_pilot_adjacent_quarters_and_competition_cutoffs`, `test_fixed_quarter_updates_and_historical_read`.

## 7. Start with an issuer and quarter

- How I tried it and what came back: The six real Taiwan saved overviews showed the selected issuer, quarter, cutoff and stable numbered report links. See item 1.

## 8. Resume before the filing is public

- How I tried it and what came back: The original TSMC and Hon Hai prefiling checkpoints show available months; the controlled check in item 2 records the real quarter-only forecast and explicit gaps. The second replay recorded lookup progress, source gaps and a partial quarter awaiting the remaining months and filing. The same-path update and period-matched comparison were exercised in the isolated synthetic case in item 2.

## 9. Resume after the filing is public

- How I tried it and what came back: Rechecked the observed pre/post-filing update evidence, plus the completed TSMC Q3 note. The same dated report paths were retained. TSMC's three monthly revenues sum to NT$989,918,000 thousand versus filed NT$989,918,318 thousand. Both source types are identified and the observed report attributes the gap to the published precision boundary without claiming an exact cause.
- Evidence: [Isolated notebook publication](acceptance-progress.md#isolated-notebook-publication), TSMC Q3 financial and forecast notes, and `test_report_keeps_monthly_and_filed_figures_with_separate_sources`.

## 10. Resume after an official correction

- How I tried it and what came back: The second checkpoint updated the same financial, risk and synthesis paths, retaining the June revisions, sources and judgment. The official August correction expanded the director eligibility and information security disclosures. The four reviewed annual figures matched both releases, including NT$1,160,834 thousand in revenue and NT$207,928 thousand in operating cash inflow. Verification found three reusable units and both original PDF digests. After August publication, discovery at the June cutoff no longer reused the current August units. The June evidence remained in dated revisions and the June execution log.

## 11. Inspect conference evidence

- How I tried it and what came back: Verified actual transcript provenance, timestamp and missing evidence, and reran conference status tests. See item 4.

## 12. Enter an ambiguous issuer

- How I tried it and what came back: Checked that the installed acquisition entry rejects an ambiguous string in place of a four-digit ticker. Opened a fresh installed-skill Codex session with a fully synthetic local fixture containing public issuer identities for 1611 and 2308, placeholders and no research inputs. With no chosen issuer in the prompt, it listed both and requested one. After the same session received 1611, it narrowed scope to that issuer and identified its missing sources, preserving quarter, cutoff and read-only boundaries. Neither turn fetched data. An earlier prompt inviting research on “one of” two named companies and containing just one saved company was interpreted as permission to pick it.
- Evidence: `/tmp/tw-accept-independent-b1d1116/edge/synthetic-choice/turn1.jsonl` and `turn2.jsonl`, plus installed Taiwan `scripts/acquire.py` and `SKILL.md`.

## 13. Encounter unavailable evidence

- How I tried it and what came back: Read the initial partial and final Delta publications. Missing trading data were identified and the same report paths became complete after original data and briefing PDFs were supplied. Verified the final notes and missing-evidence classification.
- Evidence: [Delta verified publications and live finding](final-cohort.md#delta-verified-publications-and-live-finding) and `test_empty_failed_and_missing_body_are_distinct`.

## 14. Encounter a conflicting edit

- How I tried it and what came back: The focused tests attempted publication after a conflicting edit and verified that publication was rejected and the edited content survived.
- Evidence: `test_user_edit_and_symlink_preserved` and `test_publication_snapshot_protects_quarter_managed_note_transitions`.

## 15. Resume US research

- How I tried it and what came back: See item 6 for the installed entry and existing quarter continuity tests. No further fresh US host dialogue was needed to exercise the unchanged shared continuation procedure.

## Re-run on 2026-11-23, at b1d1116

- 5: re-tested — Rechecked actual official sources and exercised a fresh installed-skill session on an image-only table and chart with an intentionally obscured cell. It cited the rendered page and checked values, identified the unavailable value, and excluded unsupported calculations.
- 12: re-tested — Used a fresh installed-skill session with an unselected issuer and two available public identities in a synthetic vault. It requested an issuer choice, then scoped the follow-up to ticker 1611 using the unchanged cutoff and evidence boundary.

## Public tool and source contracts

- The retained 2330 disclosure index response (digest `3c43e880a83e9d9a815557b1bc2b22eacecc6d934bc12d2fd5cbb7c618a70b20`) was requested with `companyId=2330, year=114, month=all, firstDay="", lastDay=""`. Its `code=200` envelope contains `result.companyId`, `marketName` and `data`. Row positions 0, 2, 3, 4 and 5 identify the issuer, ROC day, time, title and detail reference. The reference for 114/07/01 19:59:54 provides `serialNumber=1, enterDate=1140701, marketKind=sii, companyId=2330`. The official detail response (digest `156f1824754ff7f11d14a24e118bbf9440082da0f50eaf5da40409ca1c574bfd`) uses positions 0–2 for serial, day and time, and position 9 for the body. These are observed response shapes. [MOPS disclosure search](https://mops.twse.com.tw/mops/#/web/t05st01).
- The document index provides the `readfile2` arguments for a quarterly `A` or annual `F` document. The quarterly row for 2330 points to `202503_2330_AI1.pdf`. Its landing link adds a server suffix to the filename under `/pdf/`. The annual 1611 index exposes separate `2024_1611_20250526F04.pdf` and `2024_1611_20250526F11.pdf` rows, whose release dates were read from the rows as described in item 3. The filename date alone does not identify each publication timestamp. [Quarterly 2330 index](https://doc.twse.com.tw/server-java/t57sb01?step=1&colorchg=1&co_id=2330&year=114&seamon=&mtype=A) · [Quarterly PDF landing](https://doc.twse.com.tw/server-java/t57sb01?step=9&colorchg=1&kind=A&co_id=2330&filename=202503_2330_AI1.pdf) · [Annual 1611 index](https://doc.twse.com.tw/server-java/t57sb01?step=1&colorchg=1&co_id=1611&year=114&seamon=&mtype=F).
- yt-dlp 2026.08.19 documents `--extract-audio`, `--audio-format`, `--postprocessor-args` and the subtitle-only options. The `ExtractAudio+ffmpeg_o` selector applies the arguments to FFmpeg output. FFmpeg 9.0.2 uses `-ac 1 -ar 16000` to normalize channel count and sample rate. Yap's local `transcribe --help` confirms `--locale`, `--srt` and `-o`. The installed `whisper-cli --help` confirms `-ng -m -f -l -osrt -of`, including that `-of` takes a basename. [yt-dlp options](https://github.com/yt-dlp/yt-dlp#usage-and-options) · [FFmpeg options](https://ffmpeg.org/ffmpeg.html#Options) · [Yap project](https://github.com/finnvoor/yap) · [Whisper CLI source](https://github.com/ggml-org/whisper.cpp/blob/master/examples/cli/cli.cpp).
