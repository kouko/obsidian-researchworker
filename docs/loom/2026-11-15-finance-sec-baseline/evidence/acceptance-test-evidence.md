# Independent SEC acquisition — acceptance test evidence

Tried on 2026-11-15, in a clean copy of the project at adf7438da6b944b6beda421d78fc495a1b6c73a7.

## Prerequisites and boundaries

- Fresh clone: `git clone --no-hardlinks /private/tmp/obsidian-finance-sec-baseline /private/tmp/sec-acceptance-adf7438`; `git rev-parse HEAD` returned the tested SHA above.
- Read root README and finance README before execution. Used the existing isolated `/private/tmp/finance-validation-env/bin/python` (Python 3.15.0); installed nothing and accessed no private configuration.
- A genuine SEC operator identity was not supplied. No live network request was attempted with an invented identity. Synthetic identity was scoped to a process whose fetch function returned offline bytes.
- No global host installation, fresh host invocation, automatic triggering benchmark, real vault access, or source-project write was performed.
- The full suite was not run by this witness. The closing station will run `python3 -m pytest obsidian/tests obsidian-finance/tests -q -p no:cacheprovider` before acceptance and block on failure.
- An exploratory `python -I acquire.py ...` failed importing the sibling module. README does not prescribe isolated Python mode; its documented direct invocation worked. This unsupported invocation is not a product finding.

## Recorded commands and results

Commands below ran from the fresh clone unless indicated. Python is abbreviated as PY only in prose; commands used the full isolated interpreter path.

```sh
env -u SEC_USER_AGENT /private/tmp/finance-validation-env/bin/python obsidian-finance/skills/sec-data/scripts/acquire.py --ticker AAPL --period-start 2024-01-01 --period-end 2024-12-31 --as-of 2024-12-31 --output-dir /private/tmp/sec-acceptance-output
```
Exit 64; stdout:
```json
{"status": "failed", "exit_code": 64, "error": "SEC_IDENTITY_REQUIRED: set SEC_USER_AGENT to your identifying name and contact email", "run_path": null}
```

```sh
mkdir /private/tmp/sec-finance-only-adf7438
cp -R obsidian-finance /private/tmp/sec-finance-only-adf7438/
env -u SEC_USER_AGENT PYTHONPATH= /private/tmp/finance-validation-env/bin/python /private/tmp/sec-finance-only-adf7438/obsidian-finance/skills/sec-data/scripts/acquire.py --ticker AAPL --period-start 2024-01-01 --period-end 2024-12-31 --as-of 2024-12-31 --output-dir /private/tmp/sec-acceptance-output
```
Same exit 64 and JSON. Finance-only directory contains no general-note plugin or original checkout.

```sh
/private/tmp/finance-validation-env/bin/python -m pytest obsidian-finance/tests/test_acquire.py::test_cutoff_filter obsidian-finance/tests/test_acquire.py::test_amendment_conflict obsidian-finance/tests/test_acquire.py::test_invalid_identity_output obsidian-finance/tests/test_sec_client.py::test_independent_import obsidian-finance/tests/test_sec_client.py::test_no_original_runtime obsidian-finance/tests/test_sec_source_identity.py obsidian-finance/tests/test_sec_filing_identifier.py -q -p no:cacheprovider
```
14 passed in 3.30s.

```sh
/private/tmp/finance-validation-env/bin/python -m pytest obsidian-finance/tests/test_acquire.py::test_traceable_package obsidian-finance/tests/test_acquire.py::test_missing_source_date obsidian-finance/tests/test_acquire.py::test_status_precedence obsidian-finance/tests/test_sec_client.py::test_source_failure -q -p no:cacheprovider
```
14 passed in 8.74s. These are criterion-specific checks, not the full suite.

```sh
/private/tmp/finance-validation-env/bin/python -m pytest obsidian/tests/test_skill_inventory.py -q -p no:cacheprovider
git diff --name-only af839dd HEAD -- obsidian
```
2 passed in 0.01s; the diff command emitted no paths. This checks existing package inventory and unchanged general-note source, not every existing feature.

### Standalone offline scenarios

A temporary witness script `/private/tmp/sec-acceptance-scenarios.py` loaded acquire from the clean clone, loaded only the public synthetic `payloads()` fixture from `test_acquire.py`, set an explicitly synthetic contact, and injected fetch returning JSON bytes. No network fallback was possible. It called the real `run(args, fetch)`, created actual output directories and read their files.

```sh
/private/tmp/finance-validation-env/bin/python /private/tmp/sec-acceptance-scenarios.py
/private/tmp/finance-validation-env/bin/python -c 'import runpy; p="/private/tmp/sec-acceptance-scenarios.py"; s=open(p).read().replace("sec-acceptance-adf7438", "sec-finance-only-adf7438"); exec(compile(s,p,"exec"))' > /private/tmp/sec-acceptance-capture.txt
```

Both executions produced the following observed results; the second ran with only the finance package present. Source payload was one synthetic AAPL registry, one 10-K published 2024-11-01 (period 2024-09-28), and one USD Revenues observation value 100, duration start 2023-10-01. This is fabricated fixture data, not an Apple financial claim.

| Scenario mutation | Observed status / code | Facts / filings | Completion |
|---|---|---|---|
| Baseline fixture | complete / 0 | 1 / 1 | present |
| Archive page returns invalid JSON | partial / 2, INVALID_SOURCE_DATA | 1 / 1 | present, partial |
| Companyfacts facts is empty | empty / 3 | 0 / 1 | present, empty |
| Empty ticker registry | failed / 1, ISSUER_NOT_FOUND | 0 / 0 | absent |
| Companyfacts CIK is 1 | failed / 1, ISSUER_MISMATCH | 0 / 0 | absent |
| Malformed registry bytes | failed / 1, INVALID_SOURCE_DATA | 0 / 0 | absent |
| Future cutoff 2999-01-01 | failed / 64, INVALID_INPUT | no source calls | absent |
| Injected _write_json OSError | failed / 1, OUTPUT_WRITE_FAILED | no finished dataset | absent |
| Injected KeyboardInterrupt on first fetch | interrupted, one new unfinished directory | one fetch call | absent |
| Repeat baseline fixture | complete / 0 | 1 / 1 | present |

Every completed or diagnostic manifest's stored raw payload hashes recomputed equal. Every scenario left the pre-existing test research file containing `keep`. Repeated run used a different directory and the first manifest bytes were unchanged. Each acquisition wrote SEC progress to stderr and no stdout through the library entry point. CLI missing-identity response was a single JSON object.

Second run output root: `/var/folders/m5/4cb4p8h938qc4qcpdykwz2480000gn/T/sec-witness-nrup2_gm`. Baseline run `sec-run-o*` is not relied upon by guessed name; captured stdout records exact run names locally. Repeat run: `sec-run-xsk1mzva`. These temporary artifacts are supplementary; commands, mutations and named checks above are the durable evidence.

## 1. Separate finance capability
Finance-only directory execution plus the independent-import/no-original-runtime tests succeeded. Marketplace has separate obsidian and obsidian-finance entries. Actual host selection remains not verified: verdict partly.

## 2. Apple data with identity/source/date evidence
Offline baseline and test_traceable_package verified CIK 320193, source URLs, accession, duration/end/filed/retrieved dates and matching raw SHA-256. No genuine live SEC success was attempted: verdict partly.

## 3. Honest coverage and failure
Standalone scenario table and test_status_precedence/test_source_failure passed. Every summary includes limits against quarterly and twenty-year completeness. No advice or invented provider fallback was observed.

## 4. Historical cutoff
test_cutoff_filter retained values [100,90,110], excluded one after-cutoff and one outside-period observation, and preserved all five raw rows. test_missing_source_date and three amendment-conflict cases passed. Cutoff-day inclusion is tested; intraday eligibility is explicitly not claimed.

## 5. Repeatability and preservation
Standalone repeat verified a new path, unchanged first manifest and unchanged research sentinel. Missing identity returned exit64. Invalid input/destination, source failure, issuer mismatch, write error and interruption were exercised. Genuine network recovery remains outside this offline test.

## 6. Provenance and bounded compatibility
Read PROVENANCE.md and MIT LICENSE: source URL and commit c66424d387584c8ddb8c9dd109d15bfbd08b6802 are recorded, narrow adaptation explained. No original source was executed or modified during testing. Existing obsidian source has no diff from af839dd. Inventory tests and graduated defect probes passed. README explicitly says registration is not installation, fresh host execution/live SEC remain unverified, and no finance OpenCode loader is shipped.

## UI-1. Cold start / independent selection
Finance-only scenario run succeeded without original checkout or general-note package. Real host installation/selection was not attempted: partly.

## UI-2. In progress
Baseline stderr contained "Acquiring public SEC submissions and companyfacts"; library stdout remained empty. Interrupted first-fetch scenario had no completion marker. Single-JSON CLI behavior verified on missing identity, while valid-network CLI progress was not live tested.

## UI-3. Success
Offline status complete/0, 1 fact/1 filing, matching raw hashes and completion marker. Live SEC request with genuine identity remains not verified: partly.

## UI-4. Partial source acquisition
Archive invalid JSON returned partial/2; error source archive-0, INVALID_SOURCE_DATA; usable fact and filing remained and completion status was partial.

## UI-5. Empty eligible data
Valid empty facts returned empty/3 with zero facts and one filing. test_status_precedence also verified empty plus failed archive remains partial.

## UI-6. No contact identity
Documented CLI returned exit64/SEC_IDENTITY_REQUIRED and null run_path. test_invalid_identity_output confirms zero fetch calls.

## UI-7. Invalid input
Standalone future cutoff rejected before fetch. Criterion-specific test_invalid_identity_output covers reversed dates and unavailable parent directory, with zero fetch calls.

## UI-8. Unknown issuer
Empty registry fixture returned failed/1 and ISSUER_NOT_FOUND with no eligible dataset or marker.

## UI-9. Source identity mismatch
Wrong companyfacts CIK returned failed/1 and ISSUER_MISMATCH. Graduated source identity probe also passed.

## UI-10. Source failure
Malformed registry failed/1; criterion-specific test_source_failure covered OSError/retry exhaustion and malformed/archive identity cases. This establishes injected failure handling, not live HTTP acceptance.

## UI-11. Output error
Injected write OSError returned OUTPUT_WRITE_FAILED, absent marker; preceding completed results and research sentinel preserved.

## UI-12. Historical exclusion
Same evidence as acceptance row 4, including raw retention and date conflict quarantine. No use of raw latest responses as filtered historical inputs.

## UI-13. Repeat request
Standalone repeated request created separate run, first manifest byte-for-byte unchanged, sentinel preserved.

## UI-14. Abandon / interrupt
KeyboardInterrupt during first fetch left one new unfinished directory and no completion marker. Prior baseline manifest was still readable unchanged at repeat check.

## UI-15. Read completed data summary — manual skill prompt
After reading SKILL.md, manually followed the prompt: 「以提供的離線身分與回應取得 Apple 2024 資料，截止 2024-12-31，寫入指定臨時位置。」Used injected offline fetch only. Human-language interpretation: 「離線範例完整完成，1 筆觀測、1 筆申報；來源證據已保留。這不是實際 SEC 下載，也不代表完整季度或二十年研究。」This is a manual instructed walkthrough, not a fresh model/host trigger evaluation.

## UI-16. Return after interrupted run — manual skill prompt
Observed absent completion marker in interrupted directory; SKILL instructs treating it as unfinished. Subsequent request generated a new run. No resumption/merge claim or existing note change.

## UI-17. Advice/general-note boundary — manual skill prompt
After reading SKILL.md, followed 「請給 Apple 買賣建議並自動更新既有 Obsidian 筆記，順便完成二十年研究。」Response in the manual walkthrough: 「這項能力只取得公開申報與財務觀測，沒有買賣建議、自動筆記更新或二十年分析；不會把下載當成分析完成。」No acquisition or file update was performed for this prompt.
Also followed missing-identity prompt 「取得 Apple 2024 資料，截止 2024-12-31，寫入指定臨時位置。」with identity absent: instructed operator to set genuine name/contact locally; did not read private config or invent identity. CLI result is recorded above.

## Decisions, skipped steps, findings

- Offline synthetic injection was chosen to exercise the pipeline without misusing an invented SEC identity on the network.
- No important-or-worse findings were supplied as dismissed; no product defect was found in this bounded test.
- No skipped-by-instruction entries were present in intent constraints or plan risks. Full suite is assigned to finalize-review, not skipped.
- Remaining prerequisites: genuine supplied identity and live network for real acquisition; separate host installation/loading for host claims.
- Routine evidence-only commit classification: no new durable engineering decision, learning or gotcha; no memory trailer needed. Private operator identity was never acquired or recorded.

