# Independent industry and market research — acceptance test evidence

Tried on 2026-11-21 in a clean detached clone at `fee2dc0d86347c876d0dd413bfa3944752ef35f0`. The README points to the source skill and requires Python 3.11+. The clone's `python3 -B obsidian-finance/scripts/market_research.py --help` loaded the source successfully and listed `publish`, `resume`, `cite`, `aggregate` and `compare`. The tests used disposable vaults and the public-source packets supplied to the two native Codex executions. This was source invocation, without evidence of fresh marketplace installation or automatic skill routing.

Focused tests from the clean clone:

```text
PYTHONDONTWRITEBYTECODE=1 python3 -m pytest obsidian-finance/tests/test_market_{evidence,research,research_workflow}.py -q -p no:cacheprovider
.......................                                                  [100%]
23 passed in 0.85s
```

The automated package check before acceptance is `python3 -m pytest obsidian/tests obsidian-finance/tests -q -p no:cacheprovider`. The independent tester did not run the whole package suite.

## 1. 可獨立產出全球智慧型手機市場相鄰兩個市場季度的研究紀錄，交代出貨量、主要品牌市占、涵蓋範圍與來源口徑，並指出可比較的變化、可能原因與證據限制。

- How I tried it: Read both smartphone Markdown snapshots produced by the native executions. Independently ran the clean clone's `resume "$replay_vault" smartphones 2024Q2` and `resume "$replay_vault" smartphones 2024Q3`, piped each recovered `.record` into `publish "$empty_vault"`, and opened the published reviews and linked notes. Compared the data to the original tables.
- What came back: Both readbacks reported `issues: []` and republished as `r1`. The overview identifies the worldwide new branded smartphone shipment measure and worldwide shipments as the share denominator. Both original tables exclude refurbished units and OEM sales. The notes preserve the preliminary versions and state that the exact revised Q2 series was missing. Regional Android demand and channel replenishment are possible explanations with no attribution from these data alone.

| Calendar quarter | IDC publication dateline | Worldwide shipments (millions) | Samsung share | Apple share | Xiaomi share |
|---|---|---:|---:|---:|---:|
| 2024Q2 | 2024-07-15 | 285.4 | 18.9% | 15.8% | 14.8% |
| 2024Q3 | 2024-10-14 | 316.1 | 18.3% | 17.7% | 13.5% |

- Evidence: `smartphones/2024Q{2,3}/r1/{review,analysis,sources,outlook}.md` and `smartphones/overview.md` in the isolated vault. From the displayed values, Q3 volume was up 30.7 million (+10.76%) and Apple share was up 1.9 percentage points. The saved Q2 release uses the press release's July 15 dateline and source table date. The current IDC page header displays July 14, so no eligibility before July 15 was claimed. [IDC's July preliminary release](https://www.idc.com/resource-center/press-releases/worldwide-smartphone-market-grew-6-5-in-the-second-quarter-of-2024-as-momentum-continues-to-build-according-to-idc-tracker/) · [IDC's October preliminary release](https://www.idc.com/resource-center/press-releases/worldwide-smartphone-market-grows-4-with-316-1-million-units-shipped-in-the-third-quarter-of-2024-according-to-idc/).

## 2. 另一段對話能讀回已存的 Markdown 研究進度、來源版本與未完成事項，接續同季研究或追蹤下一季。

- How I tried it: Inspected both native `codex exec --json` streams for thread starts, the actual command output and terminal completion. Used `cmp` against the clone to verify the staged helpers, `diff -rq` for each market's Q2 note tree across vaults, and the clean clone's `resume` in new processes to validate each snapshot.
- What came back: Q2 thread `01a1fd60-d4c3-7f81-991c-49e6b1bafa6d` and Q3 thread `01a1fd63-0790-7583-87f0-0075b49a31b9` each ended in `turn.completed`. The latter recovered Q2 progress from Markdown, preserved both Q2 note trees byte-for-byte and published the Q3 reviews. Q2's `market_research.py` predates the boundary fix; Q3's copy matches the tested commit. Both Q2 records were independently republished and read back with the fixed helper. The two native instances used separate threads and disposable vaults.
- Evidence: Original captured command `item_6` in `/private/tmp/market-research-runtime.dRRjYP/q2-events.jsonl` and command `item_4` in `/private/tmp/market-research-q3-runtime.YXCAxv/q3-events.jsonl`. The independent readback printed the following Q2 source version and pending-work pair for each market:

```text
smartphones: idc-may-2024, idc-q2-2024-preliminary
pending: obtain comparable Q1 and calendar-year 2024 shipments, check revisions,
         regional Android shipments and channel evidence
semiconductors: sia-wsts-q2-2024, wsts-spring-2024
pending: obtain comparable calendar-year 2024 sales, assess logic and memory
         with comparable category data, separate volume, pricing and mix
```

## 3. Apple 的公司分析可引用其資訊截止時間前已公開的市場研究依據，並能查回引用版本與原始來源。公司財季與市場季度各自標示。

- How I tried it: The Q3 conversation distinguished Apple FY2024 Q4 (ends 2024-09-28, reports 2024-10-31) from market calendar 2024Q3. Independently called `cite "$empty_vault" smartphones 2024Q3 apple-shipments CUTOFF` before, on and after publication. Submitted a candidate Q3 revision containing a November 1 Counterpoint claim with the October 31 snapshot cutoff.
- What came back: October 13 returned JSON `null`. October 14 accepted the report as a retrospective reference dated from the source release. October 31 returned `idc-q3-2024-preliminary`, `2024-10-14`, market observation `2024Q3`, locator `Global shipments table` and the original IDC URL, with the preliminary estimate of 56.0 million Apple shipments and 17.7% share. The native session also returned `null` at the September 28 quarter end. The attempted late claim exited 1 with `Ineligible source version at snapshot cutoff for late` and created no revision directory.
- Evidence: Clean clone output and Q3 native `item_4` captured the same issuer lookup. The session exercised issuer-context lookup and printed the citation; no existing Apple issuer research note was opened or edited. [Apple FY2024 Q4 earnings release](https://www.apple.com/newsroom/2024/10/apple-reports-fourth-quarter-results/) · [Original IDC table](https://www.idc.com/resource-center/press-releases/worldwide-smartphone-market-grows-4-with-316-1-million-units-shipped-in-the-third-quarter-of-2024-according-to-idc/).

## 4. 至少兩個市場各有相鄰兩季紀錄，可回顧前季證據與展望、核對已公布實績，並更新後續展望。

- How I tried it: Independently republished and resumed both semiconductor and smartphone quarters. Read each Q3 analysis, outlook and pending comparisons. Piped the prior forecast, source map and either no actual or the published Q3 actual to `compare "$market_cutoff"`. Also ran the named forecast test with the initial full-year SIA release at its actual availability date.
- What came back: Smartphones went from 285.4 to 316.1 million shipments (+10.76%). The full-year outlook moved from 1,210 to 1,230 million and from 4.0% to 5.8% growth; both versions remained pending because the annual actual was unavailable. Semiconductor quarterly sales went from USD 149.9 to USD 166.0 billion (+10.74%). The USD 611 billion annual spring projection stayed in place with updated assumptions and unresolved category attribution. Both markets correctly yielded `pending / missing-actual` without a full-year actual and `pending / noncomparable-actual` when supplied the Q3-only actual.
- Evidence: `semiconductors/2024Q{2,3}/r1/{analysis,outlook,review}.md`, `smartphones/2024Q{2,3}/r1/{analysis,outlook,review}.md`, and `test_prior_outlook_round_trip_and_target_horizon_comparison`. The focused test withheld the original USD 627.6 billion annual release at the November cutoff and scored +USD 16.6 billion against spring when the February 7 cutoff made it eligible. The publisher separately notes the March 3 update to USD 630.5 billion; that is a later vintage. [SIA Q2 figures](https://www.semiconductors.org/market-data/page/3/) · [SIA Q3 release](https://www.semiconductors.org/global-semiconductor-sales-increase-23-2-in-q3-2024-compared-to-q3-2023-quarter-to-quarter-sales-up-10-7/) · [SIA year-end release and update](https://www.semiconductors.org/global-semiconductor-sales-increase-19-1-in-2024-double-digit-growth-projected-in-2025/).

## 5. First quarter

- How I tried it: Inspected both Q2 reviews published by the first native session, then published both to an independently empty vault.
- What came back: Each readback verified a market overview and analysis, sources, and outlook in its quarter folder.
- Evidence: Both Q2 `r1/review.md` outputs had link targets `../../overview.md`, `analysis.md`, `sources.md` and `outlook.md`. See sections 1 and 2 for content and independent CLI results.

## 6. Missing evidence

- How I tried it: Read the Q2 and Q3 review headings and returned `.record.pending` through `resume`.
- What came back: Reviews are labeled `Partial` and enumerate unresolved source checks and missing same-horizon actuals.
- Evidence: `smartphones/2024Q3/r1/review.md` begins `Partial at 2024-10-31`; `semiconductors/2024Q3/r1/review.md` begins `Partial at 2024-11-05`. See pending reasons in sections 2 and 4.

## 7. Resume

- How I tried it: Audited the Q3 thread and repeated the published-note readback independently.
- What came back: Recovered Q2 source versions and pending questions for both markets.
- Evidence: Q3 thread and clean readback in section 2.

## 8. Next quarter

- How I tried it: Audited Q3 against source packets and repeated the horizon comparisons independently.
- What came back: Both latest reviews retained prior outlooks while keeping their unresolved annual targets pending.
- Evidence: Q3 published notes and cutoff comparisons in section 4.

## 9. Revision

- How I tried it: In the independent vault, submitted an eligible `r2` via `publish` with an explicit revision date and a clarification that Apple share means worldwide shipment share. This was a wording correction with figures held constant.
- What came back: `r2/review.md:11` links `../r1/review.md`; `r2/analysis.md:13` dates the correction 2026-11-21 and states that the figures and conclusion are unchanged. A recursive diff against the original Q3 `r1` folder had no output. The focused workflow test `test_revision_does_not_supersede_eligible_citation_or_broken_resume` separately exercises a second snapshot with a later source and different observation, cutoff-specific citation selection, and fallback to the surviving verified record.
- Evidence: Independent test vault `/private/tmp/market-accept-vault.nNLok6`, with the revision body and link summarized above. No new actual market figure was introduced for this wording-correction replay.

## 10. Company citation

- How I tried it: Repeated the Apple cutoff lookup and late-source negative control.
- What came back: The output distinguishes the market quarter and original release from Apple's reporting cutoff, with later evidence withheld.
- Evidence: Native and clean clone outputs in section 3.
