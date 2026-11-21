# Independent industry and market research — acceptance test evidence

## Re-run on 2026-11-22, at e51c4ea

The independent tester used a clean detached clone at
`e51c4ea18f175c3633bbf68272acfa3e7604df5e`. The package README
points to the bundled market skill and Python 3.11+ source entry point.
`python3 -B obsidian-finance/scripts/market_research.py --help` loaded
under Python 3.15.0 and listed publish, recover, resume, cite, aggregate
and compare. The default interpreter lacked pytest. The existing isolated
test environment was used for these focused checks:

```text
PYTHONDONTWRITEBYTECODE=1 /private/tmp/sec-package-evaluation-venv/bin/python -m pytest obsidian-finance/tests/test_industry_notes.py obsidian-finance/tests/test_industry_update.py obsidian-finance/tests/test_market_research_workflow.py obsidian-finance/tests/test_market_research.py::test_cli_read_barrier_refuses_resume_and_cite_until_recovery -q -p no:cacheprovider
25 passed in 2.73s
PYTHONDONTWRITEBYTECODE=1 /private/tmp/sec-package-evaluation-venv/bin/python -m pytest docs/loom/2026-11-21-finance-industry-market-research/evidence/probes/test_industry_{displaced_writer,history_scope}.py -q -p no:cacheprovider
3 passed in 0.30s
```

The package check reserved for closing review is
`python3 -m pytest obsidian/tests obsidian-finance/tests -q -p no:cacheprovider`.
The independent tester did not run the full package suite.

The disposable native replay root was
`/private/tmp/industry-final-replay.d5vqi9`. I compared all 16 staged
package files (both complete skill directories and all four helper scripts)
byte-for-byte against the clean clone for each of the Q2, Q3 and issuer
projects. The two helpers changed since the initial in-place replay have
SHA-256 hashes `a7c9aa6aabe5c06f7f9c86a25eb2de81d8a3052659d72afdd11e6134764ff9af`
(`market_research.py`) and
`47bd4ada32c5735c619d10dc1db2eb3a298c63f5c19c25cc5bf7557e482801d1`
(`industry_update.py`). The disposable projects used local skill copies
and public-source packets. They do not establish installation or automatic
selection in a normal user session.

### 1. 可獨立產出全球智慧型手機市場相鄰兩個市場季度的研究紀錄，交代出貨量、主要品牌市占、涵蓋範圍與來源口徑，並指出可比較的變化、可能原因與證據限制。

- How I tried it: Inspected the completed Q2 and Q3 outputs, read all four
  published market-quarter groups using the clean clone's
  `resume VAULT MARKET QUARTER`, and compared numbers and source limits
  to the public-release packets supplied to the runs.
- What came back: The notes identify worldwide new branded smartphone
  shipments estimated by IDC. Worldwide shipments are the share
  denominator. IDC's July preliminary data give 285.4 million, with
  Samsung 18.9%, Apple 15.8% and Xiaomi 14.8%. October's data give
  316.1 million, with Samsung 18.3%, Apple 17.7% and Xiaomi 13.5%.
  Recomputing from the archived preliminary values gives +30.7 million
  (+10.76%, displayed as 10.8%) and a 1.9-point increase in Apple share.
  Stronger Android demand is plausible. The notes leave regional demand,
  channel and inventory attribution unresolved, distinguish shipment
  estimates from end-customer sales and lack an exact revised Q2 series.
- Evidence: Both `規模與市佔率` notes, the public packets and clean readback.
  [IDC Q2 preliminary release](https://www.idc.com/resource-center/press-releases/worldwide-smartphone-market-grew-6-5-in-the-second-quarter-of-2024-as-momentum-continues-to-build-according-to-idc-tracker/) ·
  [IDC Q3 preliminary release](https://www.idc.com/resource-center/press-releases/worldwide-smartphone-market-grows-4-with-316-1-million-units-shipped-in-the-third-quarter-of-2024-according-to-idc/) ·
  [IDC August forecast](https://www.idc.com/resource-center/press-releases/worldwide-smartphone-market-forecast-to-grow-nearly-6-in-2024-driven-by-stronger-growth-for-android-in-china-and-emerging-markets-according-to-idc/).

### 2. 另一段對話能讀回已存的 Markdown 研究進度、來源版本與未完成事項，接續同季研究或追蹤下一季。

- How I tried it: Checked distinct conversations and terminal events in
  `q2/q2-events.jsonl` and `q3/q3-events.jsonl`, audited the second
  conversation's actual readback and publication output, compared the
  two copies of all Q2 Markdown by SHA-256, and ran clean readbacks.
- What came back: Q2 thread `01a1ff06-6607-7971-9e6b-8ea6a1664704` and Q3
  thread `01a1ff07-e049-7990-a929-9387040a18a6` ended in `turn.completed`.
  The Q3 conversation read Q2 versions and open work from Markdown,
  created both Q3 groups and continued phone Q3 to revision 2. The
  independent readback found `issues: []` for all four groups, and the
  Q2 quarter notes stayed byte-identical. Smartphone Q2 retained
  `idc-2024q2-preliminary` and `idc-may-2024`, with the exact Q2 revision,
  Android/channel evidence and annual actual pending. Semiconductor Q2
  retained `sia-wsts-2024q2` and `wsts-spring-2024`, with disaggregation
  and the annual actual pending.
- Evidence: Q2 events `item_10` and `item_11`, Q3 events `item_4`,
  `item_6`, and `item_8`. Q2's first smoke check assumed a top-level
  language field in the resume result. Its next command read both studies
  successfully before an inapplicable git status reported the sandbox was
  not a repository. Independent readbacks passed. A focused interruption
  test confirmed readback stops during an incomplete batch and can continue
  after recovery. Collision tests preserved displaced editor text.

### 3. Apple 的公司分析可引用其資訊截止時間前已公開的市場研究依據，並能查回引用版本與原始來源。公司財季與市場季度各自標示。

- How I tried it: Checked the issuer terminal event, inspected the actual
  Apple note and ran the clean clone's `cite VAULT smartphones 2024Q3 apple-shipments`
  against the September 28 and October 31 Pacific cutoffs. The replay
  verifier confirmed the issuer's market Markdown matched the Q3 copy.
- What came back: Issuer thread `01a1ff0b-2c89-7700-8254-faca3ed5d9eb`
  ended at `turn.completed` and saved an isolated Apple FY2024 Q4 note
  identifying the market data as calendar 2024Q3. September 28 returned
  `null`. October 31 selected the October 14 release, original IDC URL
  and table locator, 56.0 million and 17.7%, and
  `claim_version: 98b1436c20cb27c1f01581d120f4f8ebad04a0454e642ec12f4474e67490db04`.
  The issuer note carries the same exact claim and explains the exclusion
  of November 1 evidence. It explicitly limits the claim to shipments.
- Evidence: `issuer/issuer/AAPL/FY2024Q4/industry-and-competition.md`
  and `issuer/issuer-events.jsonl` under the replay root, the clean-clone
  outputs, and the [native replay record](../research/10-in-place-runtime-replay.md).
  [Apple FY2024 Q4 release](https://www.apple.com/newsroom/2024/10/apple-reports-fourth-quarter-results/) ·
  [IDC original release](https://www.idc.com/resource-center/press-releases/worldwide-smartphone-market-grows-4-with-316-1-million-units-shipped-in-the-third-quarter-of-2024-according-to-idc/).

### 4. 至少兩個市場各有相鄰兩季紀錄，可回顧前季證據與展望、核對已公布實績，並更新後續展望。

- How I tried it: Compared the Q2/Q3 analysis, outlooks and the corresponding
  readback fields, and ran the focused annual comparison test at pre- and
  post-release cutoffs.
- What came back: Smartphones used IDC's 285.4 → 316.1 million series and
  retained the annual forecast increase from 1,210 to 1,230 million, or
  4.0% to 5.8% annual growth, with the updated Android assumptions.
  Semiconductors checked USD 149.9 → 166.0 billion (+10.74%, displayed as
  10.7%) against SIA/WSTS releases, retained the USD 611 billion spring
  outlook and updated the logic/memory and pricing/volume limitations.
  Annual errors remained `pending / missing-actual` at the quarterly
  cutoffs. The focused test withheld SIA's initial annual release until
  available and then paired USD 627.6 billion with the USD 611 billion
  forecast (+USD 16.6 billion).
- Evidence: Both markets' `指引與展望` and `規模與市佔率` notes and
  `test_prior_outlook_round_trip_and_target_horizon_comparison`.
  [SIA Q2 release](https://www.semiconductors.org/global-semiconductor-sales-increase-18-3-in-q2-2024-compared-to-q2-2023-quarter-to-quarter-sales-up-6-5/) ·
  [SIA Q3 release](https://www.semiconductors.org/global-semiconductor-sales-increase-23-2-in-q3-2024-compared-to-q3-2023-quarter-to-quarter-sales-up-10-7/).

### 5. 同季更新後可從季度主筆記找到各項子研究，並在更新的原筆記查回最新分析與重要修訂。重要修訂保留舊數值、判斷或預測及其來源與時間，供歷史引用。

- How I tried it: Audited the Q3 trace's update and late-source negative
  control, repeated cutoff-specific `cite` in the clean clone, opened
  the Q3 size/share note in the disposable Desktop vault, and ran
  correction and displaced-editor tests.
- What came back: Q3 retained the standard note paths and its optional
  Apple note, with no visible revision directories. The November 1
  release was rejected at the October 31 cutoff and accepted at November
  2. The original size/share file shows the separate Counterpoint 307
  million estimate and its November 1 source. Its `重要修訂` section
  preserves the October 31 cutoff, prior IDC 316.1 million estimate and
  its original October 14 source. Clean CLI claim versions were
  `9f7aa59d08af0bd2eded8b9e662cee81a693f9b07f395581af95f68a658db3b0`
  for IDC and
  `f0d46cb7be5045869cb132bfd258bce3b77ab836096fa2f3131130940f9ecffd`
  for Counterpoint.
- Evidence: Q3 `item_6` published at the same paths and initially looked
  for the wrong history heading. `item_8` verified the actual heading
  and provenance. Desktop opened the same path, and the overview resolved
  its linked substudies. The named
  `test_industry_notes_keep_two_corrections_and_original_citations` test
  covered two controlled corrections. The market replay added a
  separately sourced estimate. Focused tests covered interrupted
  writes, untouched user text and frontmatter, and recovery of a write
  made to a displaced file still open in an external editor.

### 6. 首次在已選定的 Obsidian vault 開始研究且未指定位置時，可在 vault 的投資研究區找到產業專案及當季筆記。

- How I tried it: The native Q2 project started with an empty `vault/`
  containing `.obsidian` and no location override. In a separate empty
  vault at `/private/tmp/industry-accept-vault.pzL20T`, I used the clean
  clone's `resume`, supplied the documented name and language needed for
  first publication, and passed its JSON record to `publish` with the
  vault as the only argument.
- What came back: The independent publication produced, at the default
  location, the market overview and the four quarter-level notes for
  smartphones, plus the optional Apple supply-chain note under
  `companies/`. New-process readback returned `issues: []`,
  `idc-2024q2-preliminary`, `idc-may-2024`, and four pending items.
  The native Q2 project also produced both markets under the default
  `vault/investing/industries/` location.
- Evidence: `test_vault_default_and_relative_override`,
  `test_missing_vault_traversal_and_symlink_escapes`,
  `test_unrelated_existing_destination_is_preserved`, and
  `test_industry_explicit_vault_destination_discovery` passed. These
  checks cover rejection of missing, escaping, and unrelated destinations
  as well as a usable vault-local override.

### 7. 同一市場同一季的主筆記與子研究，在 Obsidian 中以共同前綴辨識與分組，並能以筆記屬性篩選市場、季度及研究進度。

- How I tried it: Preserved the previous UI fixture outside the disposable
  Obsidian Desktop vault, then copied in the completed exact-version Q2
  Markdown outputs. `obsidian vault=industryreplay vault` confirmed the
  active target was `/private/tmp/industry-obsidian-ui.5L40g8/vault`. The
  CLI ran a property search, listed the Q2 smartphone overview's outbound
  links, read its indexed properties, and opened its size/share note.
- What came back: `[market:smartphones] [quarter:2024Q2] [status:partial]`
  returned five records: the overview, size/share, supply-chain and outlook
  notes plus the optional Apple supply-chain note. All five filenames
  begin `2024Q2 全球智慧型手機市場-`. The overview's indexed links resolved
  all four of those related notes and the project overview. Its properties
  were `type: industry-overview`, `market: smartphones`, `quarter: 2024Q2`,
  `status: partial`, `as_of: 2024-07-15` and `updated: 2026-11-22`.
  The active leaf rendered `2024Q2 全球智慧型手機市場-規模與市佔率` and
  its Properties widget rendered all six keys.
- Evidence: `obsidian vault=industryreplay search 'query=[market:smartphones] [quarter:2024Q2] [status:partial]' format=json`,
  `links path=<quarter overview>`, `properties path=<quarter overview> format=json`,
  `open path=<size/share note>`, and
  `dev:dom 'selector=.workspace-leaf.mod-active .inline-title' text`.
  The earlier [provisional Obsidian interface run](obsidian-interface.md)
  remains separately attributed to b66a90f. The focused naming tests
  also covered language continuity, name collisions, vault-relative
  links, and a property-type conflict without overwriting user data.

- Q3 UI recheck: Copied the completed Q3 notes to the disposable vault.
  The reused profile initially indexed metadata from the older Q3 copy.
  After `obsidian vault=industryreplay reload`, the Q3 property query
  included all five smartphone notes with the shared prefix. All five
  links from the overview resolved, and the overview showed
  `as_of: 2024-11-02` and `updated: 2026-11-22`. Its size/share note
  showed the correct Q3 title, dated revision and source history.

## Earlier acceptance evidence for the former revision layout

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

## Re-run on 2026-11-21, at 27a31001

The clean detached clone was at `27a31001f22781cbc7b1b5b6f95b61ea5cda2f6f`. The earlier sections retain their original execution attribution. The README's source entry point ran under Python 3.12.11. The focused market command above produced `26 passed in 1.40s`; it includes the two damaged-overview cases and the legacy shared-overview case.

- 1 and 5: re-tested. For smartphones and semiconductors, read each Q2 and Q3 legacy record with `resume`, then piped the returned `.record` into `publish` in a new empty vault. All four records passed readback and linked to `[Market overview](overview.md)`. Independently recomputed SHA-256 with `shasum -a 256` and matched each result to the review's stored overview digest. The re-published user-facing scope and observations came from the verified earlier run in sections 1 and 4.
- 2 and 7: re-tested. A genuine schema-1 review from the earlier native run resumed at r1 with `issues: []` when its shared overview matched the saved record. Appending a user edit to the copied shared overview returned `review: null` with `r1: Legacy shared overview.md differs from the saved snapshot`. The edit was still present. For schema 2, editing the market-root navigation note kept the latest valid revision selectable. Moving aside its revision-local overview returned r1 with `r2: Missing or invalid overview.md`; replacing it with changed contents returned r1 with `r2: Content changed in overview.md`. The market-root note stayed intact.
- 3 and 10: re-tested. The clean CLI returned `null` at the timezone-aware 2024-09-28 issuer cutoff. At 2024-10-31T23:59:59-07:00 it returned the issuer `cutoff`, market `snapshot_cutoff: 2024-10-31`, `retrospective: false`, market `quarter: 2024Q3`, and the IDC source `published_at: 2024-10-14`, original URL, version and locator. At 2024-10-14 the same eligible IDC original was returned with `retrospective: true` because the market review cutoff was later. The revised issuer guidance explicitly requires all four date and retrospective fields and separate fiscal and market periods.
- 4 and 8: re-tested. The same two markets and quarters were independently re-published and checked in the new note format. The analysis and outlook bytes matched the originals in all four cases. All four fresh native records passed independent readback as well, with the Q3 records carrying forward the original forecasts and leaving the unresolved annual comparisons pending. The focused forecast test also passed at this commit.
- 6: re-tested. The re-published quarters retained their original pending items and `Partial` headings. A missing or changed overview prevents the affected revision from being selected as verified progress.
- 9: re-tested. Published a same-quarter revision in the new format with a changed overview in the isolated vault and independently confirmed `[Previous snapshot](../r1/review.md)`. The latest intact revision won on readback, and both missing and changed overview cases fell back to the original with a diagnostic. The prior round separately demonstrated a dated revision.

### Fresh native market runs at 27a31001

The Q2 thread `01a1fd6b-ab68-7973-832a-040716dcb67f` and Q3 thread `01a1fd6c-b133-7ef0-a3e7-0825cc479444` ended with `turn.completed`. I compared both staged Python helpers byte-for-byte with the clean commit, independently ran `resume` on both markets and both quarters in the Q3 vault and received `issues: []` for all four. `diff -rq` found no differences between the Q2 and Q3 sessions' Q2 revision directories, which now include the revision-local overviews. The Q3 replay also attempted a November 1 source against the October 31 smartphone review and reported the rejected publication and intact r1. The detailed run and captured paths are in [the native replay record](../research/08-runtime-replay.md).

### Fresh native issuer run at 27a31001

Issuer thread `01a1fd6e-0300-79a0-ac65-93867b34ec3f` ended with `turn.completed` and wrote the isolated Apple note `issuer/AAPL/FY2024Q4/industry-and-competition.md`. I independently checked that the staged helper and issuer guidance matched the clean commit and that the copied smartphone evidence matched the Q3 session byte-for-byte. The note separately records Apple FY2024 Q4 and calendar 2024Q3, issuer `cutoff: 2024-10-31T23:59:59-07:00`, `snapshot_cutoff: 2024-10-31`, `retrospective: false`, and source `published_at: 2024-10-14`. It preserves the exact claim, original IDC URL and release version `idc-2024q3-preliminary`, and records the September 28 `null` result and later Counterpoint exclusion. This was adoption into an isolated issuer note.

## Re-run on 2026-11-21, at 7f2c126

The clean detached clone was at `7f2c1269f52d4c75bf0bd3cbae12e3b2576eaf6b`. The final commit changed the plan and the market test module. It moved the missing-quarter, pre-release citation and cutoff-aware resume assertions to the public CLI. The source entry point loaded, and the focused market command recorded above reported `26 passed in 1.65s`.

`git diff --exit-code 27a31001 HEAD -- obsidian-finance/scripts obsidian-finance/skills` returned 0. An independent `cmp` matched both staged Python helpers from all three native sessions to the final clone, matched the two market-session skill and record documents, and matched the issuer session's industry guidance to the final clone. The earlier native executions retain their original commit attribution.

- 2 and 7: re-tested. Ran `resume "$final_q3_vault" MARKET QUARTER` using the final clone on all four saved schema-2 records. Each returned revision 1 with `issues: []` and retained its source versions and pending comparisons. `diff -rq` again confirmed both Q2 revision directories were identical across the original Q2 and Q3 sessions. The affected CLI test also passed the interrupted, altered and absent-quarter cases.
- 3 and 10: re-tested. Ran `cite "$final_issuer_market_vault" smartphones 2024Q3 apple-shipments CUTOFF` from the final clone. September 28 at 23:59:59 Pacific returned `null`. October 31 at 23:59:59 Pacific returned the original IDC source, exact version, October 14 publication date, market calendar Q3, `snapshot_cutoff: 2024-10-31` and `retrospective: false`. The affected CLI test also passed historical selection when a later revision exists. The prior issuer execution wrote the Apple FY2024 Q4 note using byte-identical source.
- 1: carried over — no change to quarterly note publication or source and metric definitions.
- 4: carried over — no change to the actuals or forecast comparisons and their eligibility rules.
- 5: carried over — no change to first-quarter publication, links or overview verification.
- 6: carried over — no change to the partial status or the representation of pending work.
- 8: carried over — no change to next-quarter update or target-period matching.
- 9: carried over — no change to revision publication, predecessor links or integrity validation. The affected tests were rerun at the final commit.
