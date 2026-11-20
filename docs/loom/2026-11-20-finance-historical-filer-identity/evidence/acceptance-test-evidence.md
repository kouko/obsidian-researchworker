# Historical SEC filer selection — acceptance test evidence

Tried on 2026-11-21, in a clean copy of the project at b1aa889 (b1aa889e7aed4b509b64e23795d0863b7e620abd).

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
