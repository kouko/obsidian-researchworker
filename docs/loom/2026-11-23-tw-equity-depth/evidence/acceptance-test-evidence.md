# Taiwan equity research depth — acceptance test evidence

Tried on 2026-11-23, in a clean copy of the project at 6c878d5.

The initial run at `cded465` is documented in sections 1–9. The final run at `6c878d5` is documented in the dated section below. The isolated Codex profiles loaded `obsidian-finance` 0.1.0 through the local marketplace. I checked the final installed scripts and Taiwan skill against the clean source copy, excluding generated Python caches. The clean source copy was used for focused package tests. No full package-suite execution is attributed to this review. The automated package suite runs as a separate pre-acceptance check.

## 1. Readable quarter and supporting notes

- How I tried it: Ran `python3 /private/tmp/tw-depth-cded465/verify_notes.py` against the installed output. Read all six overviews as notes and checked the visible judgments, cutoff, gaps, and seven analysis links. Parsed the properties, rendered the Markdown, checked local link targets, and followed the separate JSON reference for portable verification.
- What came back: The quarter folders contain 48 fixed reader-facing notes. A separate recursive scan counted 18 Markdown files for each issuer, including both navigational notes, and found a prose heading, valid local link targets and no inline machine-data fence in all 54 files. The overview properties hold compact identifiers and cutoffs. The detailed research records live separately under `data/reviews`. Every quarter exposes its applicable evidence gaps and report links.
- Evidence: Obsidian 1.15.1 Reading view on the generated Delta Q3 overview displayed the headings and clickable financial-analysis link. The opened note displayed its financial tables and the balance-sheet and cash-flow heading. The observed trial used `/private/tmp/tw-depth-cded465/2308/investing/assets/equities/twse-2308/cycles/2025Q3`. The independent script verifies the complete set rather than relying on this single native visual check.

## 2. Analysis depth

- How I tried it: Read the seven note roles for each of the six quarters. Checked the material reasoning, named source or prior role, the effect of missing evidence, and the condition that would change the judgment. Recomputed representative arithmetic and compared current text with the stored date-scoped evidence. A heading or a successful save did not count as proof of analysis.
- What came back: TSMC Q3 separates the +318 thousand TWD monthly-versus-filing difference from earnings quality. Its cash-flow reconstruction subtracts 287.452 from 426.829 to get 139.377 billion TWD, and the balance-sheet discussion connects receivables and inventory to cash conversion. Hon Hai Q3 reconciles 2,057.445 billion TWD of monthly revenue to its higher quarterly filing and separates its operating margin from volatile investment and disposal income. Delta Q3 separates the Q2 comparison printed in its Q3 slide from the original Q2 filing. Its expense bridge subtracts 22.27 from 83.67 to explain 61.40 hundred million TWD of operating-profit growth.
- Evidence: The remaining roles are designed around different questions: operating drivers and management claims, direct-versus-adjacent competition, dated management guidance versus replay forecasts, price implied by explicit assumptions, price and volume confirmation, and conditional conclusions by horizon. The Delta industry note, for example, explains that revenue differences could reflect recognition, stockpiling, or mix and keeps market share and pricing power pending until comparable direct-competitor data are available. The three Q3 forecast notes explicitly distinguish archived or reconstructed expectations from contemporaneous guidance.
- Follow-up: The initial Hon Hai Q2 synthesis lacked clickable analysis evidence and its Q3 synthesis linked only the prior forecast. The final two synthesis notes link all six current-quarter subreports and include linked evidence for unresolved items. The links are at line 28 in both final notes and were checked against local targets.

## 3. Installed replay

- How I tried it: Checked the earlier TSMC Q3 reading sample and independently reran the installed-output verifier for the three issuer sessions. Read each cutoff and the company-specific gaps. Matched each Q3's stored reference to the actual current Q2 forecast file digest.
- What came back: The three initial session logs and two follow-up logs each end in `turn.completed`. After the follow-ups, the independent verifier finished at exit zero:

  ```text
  2330 2025Q2 complete 8 notes 7 verified 4 supplemental gaps
  2330 2025Q3 complete 8 notes 7 verified 4 supplemental gaps
  2317 2025Q2 complete 8 notes 7 verified 6 supplemental gaps
  2317 2025Q3 complete 8 notes 7 verified 7 supplemental gaps
  2308 2025Q2 complete 8 notes 7 verified 7 supplemental gaps
  2308 2025Q3 complete 8 notes 7 verified 6 supplemental gaps
  ```

  The Q2 and Q3 cutoffs are August 16 and November 16, respectively, at Taipei end of day. Each Q3 reference matches the written Q2 forecast path and digest. The two follow-up sessions republished the existing stable paths with revisions after verifying the distinction between supplementary limitations and unsatisfied required questions. The resulting notes still report the limitations, such as long-window adjusted price, like-for-like market-share or pricing evidence, and some source publication times.
- Evidence: The earlier reading trial is documented in [reading-pilot.md](reading-pilot.md) and remains at `/private/tmp/tsmc-q3-analysis-pilot/研究筆記`. The final input and output directories are `/private/tmp/tw-depth-cded465/{2330,2317,2308}`. All replay forecast text and evidence were checked against the archived forecast rather than assuming that the replay was contemporaneous.

## 4. Traceable continuation

- How I tried it: Using the installed API, verified the previous inline-overview Taiwan replay at `/private/tmp/tw-final-a15ac00.R36KDU/{2330,2317,2308}/investing/assets/equities`. Ran `python3 -m pytest obsidian-finance/tests/test_research_continuation.py -q -p no:cacheprovider -k 'fixed_quarter or snapshot'` and `python3 -m pytest docs/loom/2026-11-23-tw-equity-depth/evidence/probes -q -p no:cacheprovider` within the clean copy.
- What came back: All six older inline Taiwan quarters remained verifiable with seven reusable roles and zero validation gaps each. The focused test commands produced `18 passed, 50 deselected` and `1 passed`. Their exercised paths include Taiwan and US continuation, stale or concurrently edited publication, invalid and missing companions, mismatched recovery scope, and removal of a source registration bound by the pending overview.
- Evidence: `obsidian-finance/tests/test_research_continuation.py::test_fixed_quarter_updates_and_historical_read` and `test_publication_snapshot_protects_quarter_managed_note_transitions`; `evidence/probes/test_interrupted_quarter_source.py`. The restored state is evaluated through the public recovery and verification entry points.

## 5. Open the quarter

- Observed Obsidian Reading view displaying dated judgments, gaps and section navigation on the installed Delta Q3 overview. Following its link opened the corresponding financial analysis and rendered the financial tables. Earlier native prototype viewing is recorded in [reading-pilot.md](reading-pilot.md).

## 6. Review evidence

- Followed the report links in the installed output and the stored sources in its companion evidence. The note links distinguish hosted disclosures from the earlier locally saved Q2 report. Portable verification found all expected report and evidence bindings in the six dated folders.

## 7. Continue the research

- Used the Q3 forecast to reach the corresponding Q2 forecast in all three companies' notes. The focused checks exercised continuation at fixed paths, historical reading, user edits before or after a snapshot, and older notes. Continuation of fixture US quarters and inline legacy Taiwan quarters was checked separately.

## 8. Review incomplete analysis

- The earlier TSMC reconstruction includes an unresolved technical question in the 60-day adjusted series alongside supported shorter-window results. In the Delta Q3 industry note, the overall direction is supported, while market-share and pricing-power conclusions stay pending until comparable product-level evidence is available. The completed overview retains these caveats. It does not treat an unavailable publication as a contemporaneous source.

## 9. Recover research

- The focused tests removed or corrupted saved evidence and exercised recovery with the conflicting inputs. The deliberate source-loss case confirmed that a companion's valid structure does not authorize writing over the prior overview when a bound source vanished. The combination of focused tests and artifact reading covers the separate ability to read the prose while withholding unsupported reuse.

## Re-run on 2026-11-23, at 6c878d5

- 1: re-tested — Ran `python3 /private/tmp/tw-depth-6c878d5/verify_notes.py` and recursively inspected all 54 Markdown files, including the six navigation notes. The script verified each overview and its local targets. None of the Markdown files contained machine-data fences.
- 2: re-tested — Re-read the final evidence bindings and independently recomputed the Delta Q3 industry comparison from the filed revenue pairs (150,317,577 / 112,203,112; 989,918,318 / 759,692,143; and 2,058,949,127 / 1,854,569,119, in thousands TWD). The growth rates round to 33.97%, 30.31% and 11.02%. The final Delta Q3 industry note reports that order, links the three filings, and explains that the supply-chain comparison does not establish like-for-like market share, competition or pricing power.
- 3: re-tested — Fresh sessions in `/private/tmp/tw-depth-6c878d5/{2330,2317,2308}.jsonl` all ended in `turn.completed`. Each set of two reports independently verified 7 roles with eight numbered notes per quarter. All three current Q3 records point to the exact Q2 forecast path and digest. The accepted supplemental-gap counts are TSMC 5/5, Hon Hai 8/7, and Delta 7/6 (Q2/Q3).
- 4: re-tested — The unchanged installed continuation and recovery paths were exercised again from the clean source copy. `test_research_continuation.py -k 'fixed_quarter or snapshot'` passed 18 tests, and the interrupted-quarter source probe passed once.
- 5: re-tested — Opened the final installed Delta Q3 vault at `/private/tmp/tw-depth-6c878d5/2308/investing` with Obsidian 1.15.1. Reading view showed the overview gap heading and the Industry and Competition link. Following that link rendered the comparison table and the corrected ranking, 33.97% above 30.31% and 11.02%. All six final note sets also passed static rendering and local link checks.
- 6–7: re-tested — Current source and prior forecast references resolved in all six quarters, including both Hon Hai synthesis sections. The three Q3 record bindings match their actual Q2 files.
- 8: re-tested — The installed TSMC fixture at `/private/tmp/tw-depth-6c878d5/2330/.structured-gap-test.json` treated a missing conference attachment as required for the simulated question. Complete publication was rejected, partial publication verified, and the overview rendered all three fields in order: evidence, reason, and recovery. The focused fixture independently checked that a structured required gap remains visible in the overview.
- 9: re-tested — The final interrupted-source probe still prevents replacement of the prior overview when the pending quarter lacks one of its referenced source records.
