# Historical SEC filer selection — acceptance test evidence

## Re-run on 2026-11-21, at 23fa5f6

- Fresh clone at `23fa5f6e6fb240fe754b801ca49a2ac97a9e1ddd`. The README's source CLI entry loaded with `python3 obsidian-finance/skills/sec-data/scripts/acquire.py --help` and exited 0.
- Acceptance 1 and 3, UI-1, UI-2 and UI-4: six offline invocations of the CLI's `run` entry used the actual cached public SEC bytes from the source packages listed below. The replay mapped each request to its recorded URL and recomputed SHA-256 for each response before supplying it. All six exited 0 and reproduced the selected CIK and accession. A separate parse of the four selected primary documents checked CIK, year, quarter and period end and confirmed the recorded filing date did not exceed the requested cutoff. XOM 2024Q2 and Q3 resolved to `0000034088-24-000050` and `0000034088-24-000068` in both modes. AAPL 2024Q2 resolved to `0000320193-24-000069`; JPM 2024Q2 resolved to `0000019617-24-000453`.
- Acceptance 2, UI-3 and UI-4: `PYTHONDONTWRITEBYTECODE=1 python3 -m pytest obsidian-finance/tests/test_acquire.py obsidian-finance/tests/test_research_continuation.py -q -p no:cacheprovider -k 'historical_filer or invalid_cik_preflight or explicit_cik or quarter_unresolved or public_pilot_adjacent_quarters_and_competition_cutoffs'` returned `25 passed, 82 deselected in 1.66s`. This includes unresolved and explicit selection, the early-cutoff diagnostic and the Apple adjacent-quarter continuation pilot.
- Succession boundaries: `PYTHONDONTWRITEBYTECODE=1 python3 -m pytest obsidian-finance/tests/test_acquire.py -q -p no:cacheprovider -k 'current_original_across_succession or same_accession_requires_consistent or shared_accession_metadata_conflict'` returned `8 passed, 84 deselected in 0.25s`. These are simulated responses. They cover an eligible successor original, a distinct competing original, an unavailable predecessor, and matching or conflicting metadata on a shared accession, including conflict in a record outside the requested cutoff.
- XOM continuation: `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=obsidian-finance/tests python3 /private/tmp/finance-pr16-continuation.py` passed using the original Q2 and Q3 2024 HTML checked against the stored digests. The test staged research metadata and placeholder notes in a temporary directory. The earlier cutoff excluded Q3, the later cutoff reused work from both quarters and identified unfinished Q3 synthesis, and repeating discovery returned the same result. This checks the continuation mechanics with real SEC evidence rather than research quality or a full agent-run synthesis.
- Separate live boundary observation: the earlier live CLI run `sec-run-bynkd32q` downloaded [XOM 2026Q2 accession 0000034088-26-000093](https://www.sec.gov/Archives/edgar/data/2115436/000003408826000093/xom-20260630.htm), SHA-256 `775b44f3a5d98491bf35e8fc4db9e708874a054344d2b2299e90a2c7989d7ed9`. The archived run exited 1 with missing or contradictory DEI declarations. This acceptance re-run confirmed the digest and the two filer identifiers in separate contexts (`0000034088` in `c-1`, `0002115436` in `c-2`). Multi-filer declarations remain unsupported by this parser. The live observation is outside the agreed 2024 acceptance and is separate from the simulated selection tests.

Tried on 2026-11-21, in a clean copy of the project at cb34e9a (cb34e9a83f3b0c2c9ec94f036e5eaf182d823e2b).

Setup: cloned without hard links, checked out the exact commit detached, and ran `python3 -B obsidian-finance/skills/sec-data/scripts/acquire.py --help`. The stdlib entry point loaded and advertised mutually exclusive `--ticker` and `--cik` plus `--fiscal-quarter` and `--as-of`. The README uses pytest for offline verification. A setup-and-acquisition test was included below.

## 1. 以 XOM 自動選擇或手動指定原申報實體，均可取得 2024 Q2 和 Q3 原始 SEC 財報；兩期均核對申報實體、季別和資訊截止日。

- How I tried it: called the clean copy's `acquire.run` with the CLI argument combinations below, using a test contact in a temporary directory. The transport returned the previously captured raw public SEC response by exact URL from each source manifest, checking SHA-256 before returning it. This is an offline replay of actual public SEC bytes. Separate live acquisition generated the source packages, and this acceptance process made no network requests.
- Evidence: `sec-run-d6eouvb_` (Q2 both modes), `sec-run-hbkuanp7` (Q3 automatic), `sec-run-j41419bc` (Q3 explicit); captured in the live output directory under `/private/tmp/finance-historical-filer-live` at 17:12 UTC on 2026-11-20. Q2 explicit used the same raw original responses as Q2 automatic. Each run returned exit 0 and agreed with the original manifest's accession. The primary HTML's own year, quarter, end date and CIK were asserted, and the filing date was checked against the effective cutoff.

| Selector | Quarter | Cutoff | Selection | Declared CIK | Period end | Filed | Original accession |
|---|---|---|---|---|---|---|---|
| `--ticker XOM` | 2024Q2 | 2024-08-15 | documented_predecessor | 0000034088 | 2024-06-30 | 2024-08-05 | 0000034088-24-000050 |
| `--ticker XOM` | 2024Q3 | 2024-11-15 | documented_predecessor | 0000034088 | 2024-09-30 | 2024-11-04 | 0000034088-24-000068 |
| `--cik 0000034088` | 2024Q2 | 2024-08-15 | explicit_cik | 0000034088 | 2024-06-30 | 2024-08-05 | 0000034088-24-000050 |
| `--cik 0000034088` | 2024Q3 | 2024-11-15 | explicit_cik | 0000034088 | 2024-09-30 | 2024-11-04 | 0000034088-24-000068 |

- [Q2 original](https://www.sec.gov/Archives/edgar/data/34088/000003408824000050/xom-20240630.htm) SHA-256 `a10098853f682946f2a872858b781c36a53663f50d499bd5714150ca6227da5c`.
- [Q3 original](https://www.sec.gov/Archives/edgar/data/34088/000003408824000068/xom-20240930.htm) SHA-256 `75ee76f92fd2c6a21f216dbee826191cd4b2a15ce42436992b50811bb29b616b`.
- Automatic runs reported effective transition date 2026-07-01 and retained the [SEC succession filing](https://www.sec.gov/Archives/edgar/data/2115436/000119312526291990/d71068d8k12b.htm).

## 2. 自動判斷缺證據或有歧義時，提示手動指定。指定無效或該實體沒有符合截止條件的原文時，明確說明缺口。

- How I tried it: `PYTHONDONTWRITEBYTECODE=1 python3 -m pytest obsidian-finance/tests/test_acquire.py -q -p no:cacheprovider -k 'historical_filer or invalid_cik_preflight or explicit_cik or after_hours_apple_replay or setup_cli_and_later_acquisition'`.
- Output: `23 passed, 61 deselected in 0.77s`. These focused tests use synthetic responses.
- Evidence: `test_historical_filer_does_not_guess` asserted exit 1 and no completion marker or eligible facts. Missing transition, overlap and date boundaries prompted `--cik`. Early cutoff reported `no eligible source-declared original`; transport failure, malformed facts and contradictory publication evidence retained their reasons. `test_invalid_cik_preflight` asserted exit 64 before a request for zero, invalid syntax and incompatible selectors. `test_explicit_cik_does_not_switch_filers` checked early cutoff plus original and submissions identity mismatches.

## 3. 只提供股票代號的現有流程仍可支援 AAPL 和 JPM；輸出可追溯紀錄實際採用的實體。

- How I tried it: same URL-keyed public-response replay as #1. Both exit 0 and report the ticker registry method. Checked HTML identity, year, quarter, end, filing date, cutoff and accession as in #1.
- Output: AAPL 2024Q2, cutoff 2024-05-03, CIK 0000320193, end 2024-03-30, filed 2024-05-03, accession 0000320193-24-000069. JPM 2024Q2, cutoff 2024-08-15, CIK 0000019617, end 2024-06-30, filed 2024-08-02, accession 0000019617-24-000453.
- Evidence: `sec-run-_sr3gwke` and `sec-run-4brxc028` in the same live output directory at 17:13 UTC on 2026-11-20. [Apple original](https://www.sec.gov/Archives/edgar/data/320193/000032019324000069/aapl-20240330.htm) SHA-256 `e9d8940a84e58a5d9f80fc7ca76dda84fff59aac463999a257f3bb61d8574bcf`. [JPMorgan original](https://www.sec.gov/Archives/edgar/data/19617/000001961724000453/jpm-20240630.htm) SHA-256 `5a91329194c87e12635f8998194974322f7915565485bb01fa8015f318653aaf`.

## 4. Ordinary ticker flow

- Evidence: #3 verified both ticker-only inputs with their declared source identities.

## 5. Automatic XOM flow

- Evidence: #1 verified both automatic quarters with `documented_predecessor` selection and the retained succession filing.

## 6. Unresolved automatic flow

- Evidence: #2 verified missing and conflicting succession examples with a manual CIK prompt and no apparently successful package.

## 7. Explicit CIK flow

- Evidence: #1 verified both manual quarters on previously captured SEC responses. #2 verified preflight, identity and cutoff failures through synthetic responses.

## Re-run on 2026-11-21, at c7a5e75

- Fresh detached clone; `acquire.py --help` loaded successfully.
- #1 and UI-2: repeated both automatic XOM quarters using the archived SEC responses. Both selected CIK 0000034088 with the documented transition, original accessions and matching declarations/cutoffs shown above. Also verified both explicit XOM quarters on the same source bytes.
- #2 and UI-3: repeated the missing/overlapping transition checks, malformed current Companyfacts (no predecessor requests), invalid explicit CIK and early cutoff cases. Additional focused tests verified that malformed rows naming the target quarter, and malformed filing metadata for a nominated original, do not qualify as clean absence. Valid post-cutoff, amended and different-report-end records remain clean misses.
- #3 and UI-1: repeated both AAPL and JPM archived SEC response runs, in each case matching the accession, CIK and declaration metadata above.
- UI-4: repeated the two explicit XOM replays and the synthetic invalid CIK, both identity mismatches and early cutoff cases.
- Focused command: `PYTHONDONTWRITEBYTECODE=1 python3 -m pytest obsidian-finance/tests/test_fiscal_quarter.py obsidian-finance/tests/test_acquire.py -q -p no:cacheprovider -k 'malformed or historical_filer or invalid_cik_preflight or explicit_cik or after_hours_apple_replay or setup_cli_and_later_acquisition or nonqualifying_candidate'`. Output: `44 passed, 70 deselected in 1.19s`.

## Re-run on 2026-11-21, at b1aa889

- Fresh detached clone; `acquire.py --help` loaded successfully. Repeated all six URL-keyed SEC response replays in #1 and #3, covering acceptance #1, #3, UI-1, UI-2 and UI-4. All exited 0, reproduced the source hashes and accessions above, and passed the identity, fiscal declaration and cutoff assertions.
- #2, UI-3 and UI-4: re-ran the same focused command as the preceding section. Output: `48 passed, 70 deselected in 1.14s`. The four new `test_submissions_governs_exclusion_of_malformed_fact` cases verified that dates or forms in malformed Companyfacts cannot override a conflicting official filing record, and that the official record can exclude a post-cutoff filing or amendment.
- `test_historical_filer_does_not_guess` also verified that malformed current facts, conflicting original publication evidence and pre-period filing dates prompt `--cik`; transport and issuer-identity failures keep their specific errors. Rechecked the prior ambiguous transition, invalid explicit identifier, explicit issuer mismatch and cutoff examples.

## Re-run on 2026-11-21, at cb34e9a

- The intervening diff contains acceptance documentation and the expanded intent confirmation SHA. Repeated setup and all acceptance checks on a fresh detached clone at this exact commit.
- `acquire.py --help` exited 0. All six archived public SEC response replays in #1 and #3 exited 0 and reproduced the verified filing identities, accessions, checksums, fiscal declarations and cutoffs.
- The same focused test command passed: `48 passed, 70 deselected in 1.17s`, including the unresolved selection, explicit selector and malformed evidence cases in #2.
