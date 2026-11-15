# Read-only research work assessment — acceptance test evidence

Tried on 2026-11-16, in a clean copy of the project at 44ba7fa.

## Setup and scope

Created fresh detached linked worktree `/private/tmp/finance-acceptance-clean` at exact SHA `44ba7fae95a09087ef8cab509cfcb755bdefa540`. Initial working tree was clean. Python 3 runtime and standard library were sufficient; no package installation, credentials or external requests were needed. The README's isolated Apple example was reproduced explicitly in `/private/tmp/readme_apple_acceptance.py` and executed with `python3 /private/tmp/readme_apple_acceptance.py` from the clean repository root. It read committed `reported-inputs.json`, selected `q2.opex`, wrote only a new temporary snapshot/projection, and invoked the documented CLI arguments. Captured result: exit 0, `resume_incomplete_work`, affected `forecast`, evidence `q2-opex`, `external_freshness: unverified`, `reusable: []`, no gaps.

The assessor actually read snapshot JSON, source projection JSON, saved output UTF-8 text and nonempty completion evidence in isolated temporary roots. No arbitrary vault, installed host trigger, live-source freshness, research execution, or actual persisted-resume behavior is established. Subprocess walks asserted exact input-file bytes before and after every invocation. Tests separately covered socket denial and controlled KeyboardInterrupt. No fixes were made. No important-or-worse dismissed findings were supplied. This is a first acceptance run, after the two supplied adversarial fixes; no prior acceptance rows are carried over.

## Focused checks

Command (not the full suite):

```sh
/private/tmp/finance-validation-env/bin/python -m pytest obsidian-finance/tests/test_work_assessment.py obsidian-finance/tests/test_assess_work.py obsidian-finance/tests/test_projection_type.py obsidian-finance/tests/test_fiscal_provenance.py obsidian-finance/tests/test_acquire.py::test_traceable_package obsidian-finance/tests/test_acquire.py::test_quarter_package obsidian/tests/test_skill_inventory.py obsidian/tests/test_validate_canvas.py::test_clean_valid_canvas_exits_zero -q -p no:cacheprovider
```

Captured output: `............................ [100%]` / `28 passed in 1.40s`.

Full-suite command reserved for finalize-review, NOT run by this tester:
`python3 -m pytest obsidian/tests obsidian-finance/tests -q -p no:cacheprovider`.
The automated test suite runs before acceptance and blocks acceptance on failure; no prospective suite result is claimed here.

## 1. 根據隔離範例，可產生不需更新、補資料、同季修訂、新增一期及接續未完成工作等必要判斷，結果附有對應資料依據與原因。

- How I tried it: test_work_classes, test_independent_gaps, test_relevant_change, test_new_quarter; CLI no-work, incomplete, changed-price, new-quarter and missing-evidence outputs below.
- What came back: focused checks passed; actual CLI evidence below supports the bounded verdict.

## 2. 判斷能區分檔案修改時間、實際研究輸入變動及既有研究的完成狀態，不把只有修改時間改變視為需要重做研究的證據。

- How I tried it: test_timestamp_only, test_relevant_change, test_projection_typechange_invalidates; CLI file-touch result exactly matched baseline.
- What came back: focused checks passed; actual CLI evidence below supports the bounded verdict.

## 3. 固定歷史截止日與追蹤最新狀況的判斷有清楚區別，不把晚於截止日的資訊當成歷史分析當時已知，也不把新價格視為新財季。

- How I tried it: test_historical_exclusion, test_new_quarter, test_fiscal_objectaccession_quarantines; CLI historical exclusion, price revision and source-declared Q3.
- What came back: focused checks passed; actual CLI evidence below supports the bounded verdict.

## 4. 對已保存但尚未完成的工作，可指出仍需處理的部分；依賴或輸出無法核對時，不將既有檔案宣稱為可有效沿用的已完成成果。

- How I tried it: test_valid_checkpoint, test_invalid_checkpoint, test_explicit_gaps; CLI incomplete reuse and changed-prerequisite results.
- What came back: focused checks passed; actual CLI evidence below supports the bounded verdict.

## 5. 缺資料、資料無效或來源新鮮度無法確認時有明確結果，不捏造完成狀態、來源或投資建議，也不誤報研究已是最新。

- How I tried it: test_explicit_gaps, test_invalid_input_and_escape, test_no_external_access; CLI partial, invalid, unsupported, empty and unverified freshness.
- What came back: focused checks passed; actual CLI evidence below supports the bounded verdict.

## 6. 相同已知輸入可重複得到一致的待辦判斷，執行不修改輸入研究資料，不建立重複研究期別或執行所列研究工作。

- How I tried it: test_deterministic_readonly, test_interrupted_retry, test_no_external_access; subprocess walk checks identical bytes and deterministic retry.
- What came back: focused checks passed; actual CLI evidence below supports the bounded verdict.

## 7. 既有一般筆記與金融資料取得能力保留，原型已驗證與未驗證的執行範圍清楚揭露。

- How I tried it: test_shipped_skill_inventory, test_retained_skills_have_no_retired_dependencies, test_clean_valid_canvas_exits_zero, test_traceable_package, parametrized test_quarter_package. README documents prototype boundary; only representative offline regressions, not full note behavior or live acquisition.
- What came back: focused checks passed; actual CLI evidence below supports the bounded verdict.

## 8. UI flow: Ordinary assessment

- How I tried it: Actual CLI scenario captured below; equivalent scenarios share one invocation where their observable behavior is the same.
- What came back: Returned work, reason, evidence and affected dimensions; exit 0.

## 9. UI flow: No required work

- How I tried it: Actual CLI scenario captured below; equivalent scenarios share one invocation where their observable behavior is the same.
- What came back: Returned no_analysis_update within supplied evidence; external freshness unverified.

## 10. UI flow: Only timestamps changed

- How I tried it: Actual CLI scenario captured below; equivalent scenarios share one invocation where their observable behavior is the same.
- What came back: Touching the output did not alter the result.

## 11. UI flow: Frozen history

- How I tried it: Actual CLI scenario captured below; equivalent scenarios share one invocation where their observable behavior is the same.
- What came back: Excluded after_cutoff evidence and reported gaps; exit 2.

## 12. UI flow: Latest price

- How I tried it: Actual CLI scenario captured below; equivalent scenarios share one invocation where their observable behavior is the same.
- What came back: Returned append_revision_same_quarter with no invented fiscal quarter.

## 13. UI flow: New fiscal quarter

- How I tried it: Actual CLI scenario captured below; equivalent scenarios share one invocation where their observable behavior is the same.
- What came back: Returned create_next_quarter_analysis justified by source q3.

## 14. UI flow: Incomplete cycle

- How I tried it: Actual CLI scenario captured below; equivalent scenarios share one invocation where their observable behavior is the same.
- What came back: Returned remaining synthesis work and reusable valuation; no execution claim.

## 15. UI flow: Changed prerequisite

- How I tried it: Actual CLI scenario captured below; equivalent scenarios share one invocation where their observable behavior is the same.
- What came back: Returned same-quarter recomputation and no reusable output.

## 16. UI flow: Missing required evidence

- How I tried it: Actual CLI scenario captured below; equivalent scenarios share one invocation where their observable behavior is the same.
- What came back: Returned gap/recovery and partial status; exit 2.

## 17. UI flow: Freshness unknown

- How I tried it: Actual CLI scenario captured below; equivalent scenarios share one invocation where their observable behavior is the same.
- What came back: external_freshness unverified; no last-success timestamp invented.

## 18. UI flow: No research records

- How I tried it: Actual CLI scenario captured below; equivalent scenarios share one invocation where their observable behavior is the same.
- What came back: Reported No research records supplied; exit 2.

## 19. UI flow: Invalid request

- How I tried it: Actual CLI scenario captured below; equivalent scenarios share one invocation where their observable behavior is the same.
- What came back: Reported missing arguments and correction; exit 64.

## 20. UI flow: Unreadable local data

- How I tried it: Actual CLI scenario captured below; equivalent scenarios share one invocation where their observable behavior is the same.
- What came back: Reported Cannot read assessment input and correction; exit 1.

## 21. UI flow: Unsupported input

- How I tried it: Actual CLI scenario captured below; equivalent scenarios share one invocation where their observable behavior is the same.
- What came back: Reported Unsupported assessment input version; exit 1.

## 22. UI flow: Escaping reference

- How I tried it: Actual CLI scenario captured below; equivalent scenarios share one invocation where their observable behavior is the same.
- What came back: Reported Reference outside assessment root; exit 1.

## 23. UI flow: In progress

- How I tried it: Actual CLI scenario captured below; equivalent scenarios share one invocation where their observable behavior is the same.
- What came back: Synchronous single result returned; exact directory/file-byte inventory unchanged.

## 24. UI flow: Stop and retry

- How I tried it: Focused test_interrupted_retry injects KeyboardInterrupt during assessment, checks original snapshot bytes, then retries; a separate real CLI invocation reproduced baseline.
- What came back: Controlled interruption and fresh CLI retry passed; research execution was not resumed.

## Captured actual CLI walk

`/private/tmp/finance-validation-env/bin/python /private/tmp/acceptance_walk.py` executed subprocess commands against the clean worktree and asserted expected exits and input preservation. Synthetic supplied records are not claims about actual market data or SEC authenticity. Full captured output follows:

```jsonl
{"case": "No required work", "command": ["/private/tmp/finance-validation-env/bin/python", "/private/tmp/finance-acceptance-clean/obsidian-finance/scripts/assess_work.py", "--root", "/private/tmp/acceptance-input-bdt15m4b", "--snapshot", "snapshot.json", "--mode", "latest", "--cutoff", "2024-05-03T23:59:59+00:00"], "exit": 0, "result": {"cutoff": "2024-05-03T23:59:59+00:00", "decisions": [{"action": "no_analysis_update", "affected": [], "evidence": ["price"], "reason": "Completed outputs and relevant dependencies agree within supplied evidence", "record": "q2", "work": null}], "excluded": [], "external_freshness": "unverified", "gaps": [], "mode": "latest", "observations": [], "reusable": [{"record": "q2", "work": "valuation"}], "scope": "supplied_local_evidence", "status": "complete", "version": 1}, "stderr": "", "inputs_unchanged": true}
{"case": "Ordinary assessment / Incomplete cycle / In progress", "command": ["/private/tmp/finance-validation-env/bin/python", "/private/tmp/finance-acceptance-clean/obsidian-finance/scripts/assess_work.py", "--root", "/private/tmp/acceptance-input-bdt15m4b", "--snapshot", "snapshot.json", "--mode", "latest", "--cutoff", "2024-05-03T23:59:59+00:00"], "exit": 0, "result": {"cutoff": "2024-05-03T23:59:59+00:00", "decisions": [{"action": "resume_incomplete_work", "affected": ["synthesis"], "evidence": ["valuation"], "reason": "Work or prerequisites are incomplete", "record": "q2", "work": "synthesis"}], "excluded": [], "external_freshness": "unverified", "gaps": [], "mode": "latest", "observations": [], "reusable": [{"record": "q2", "work": "valuation"}], "scope": "supplied_local_evidence", "status": "complete", "version": 1}, "stderr": "", "inputs_unchanged": true}
{"case": "Only timestamps changed", "command": ["/private/tmp/finance-validation-env/bin/python", "/private/tmp/finance-acceptance-clean/obsidian-finance/scripts/assess_work.py", "--root", "/private/tmp/acceptance-input-bdt15m4b", "--snapshot", "snapshot.json", "--mode", "latest", "--cutoff", "2024-05-03T23:59:59+00:00"], "exit": 0, "result": {"cutoff": "2024-05-03T23:59:59+00:00", "decisions": [{"action": "no_analysis_update", "affected": [], "evidence": ["price"], "reason": "Completed outputs and relevant dependencies agree within supplied evidence", "record": "q2", "work": null}], "excluded": [], "external_freshness": "unverified", "gaps": [], "mode": "latest", "observations": [], "reusable": [{"record": "q2", "work": "valuation"}], "scope": "supplied_local_evidence", "status": "complete", "version": 1}, "stderr": "", "inputs_unchanged": true}
{"case": "Frozen history", "command": ["/private/tmp/finance-validation-env/bin/python", "/private/tmp/finance-acceptance-clean/obsidian-finance/scripts/assess_work.py", "--root", "/private/tmp/acceptance-input-bdt15m4b", "--snapshot", "snapshot.json", "--mode", "historical", "--cutoff", "2024-05-03T23:59:59+00:00"], "exit": 2, "result": {"cutoff": "2024-05-03T23:59:59+00:00", "decisions": [{"action": "invalidate_dependent_checkpoint_and_recompute", "affected": ["valuation"], "evidence": ["price"], "reason": "Missing eligible dependency or consumed identity: price", "record": "q2", "work": "valuation"}, {"action": "record_gap_and_continue_independent_work", "affected": [], "evidence": ["price", "valuation"], "reason": "Evidence requires recovery", "record": "q2", "work": null}], "excluded": [{"evidence": "price", "reason": "after_cutoff"}], "external_freshness": "unverified", "gaps": [{"evidence": "price", "reason": "Required source missing, inconsistent or ineligible", "record": "q2", "recovery": "Supply or verify the identified local evidence and retry"}, {"evidence": "valuation", "reason": "Missing eligible dependency or consumed identity: price", "record": "q2", "recovery": "Supply or verify the identified local evidence and retry"}], "mode": "historical", "observations": [], "reusable": [], "scope": "supplied_local_evidence", "status": "partial", "version": 1}, "stderr": "", "inputs_unchanged": true}
{"case": "Latest price / Changed prerequisite", "command": ["/private/tmp/finance-validation-env/bin/python", "/private/tmp/finance-acceptance-clean/obsidian-finance/scripts/assess_work.py", "--root", "/private/tmp/acceptance-input-bdt15m4b", "--snapshot", "snapshot.json", "--mode", "latest", "--cutoff", "2024-05-03T23:59:59+00:00"], "exit": 0, "result": {"cutoff": "2024-05-03T23:59:59+00:00", "decisions": [{"action": "append_revision_same_quarter", "affected": ["valuation"], "evidence": ["price"], "reason": "Relevant consumed inputs changed", "record": "q2", "work": "valuation"}], "excluded": [], "external_freshness": "unverified", "gaps": [], "mode": "latest", "observations": [], "reusable": [], "scope": "supplied_local_evidence", "status": "complete", "version": 1}, "stderr": "", "inputs_unchanged": true}
{"case": "New fiscal quarter", "command": ["/private/tmp/finance-validation-env/bin/python", "/private/tmp/finance-acceptance-clean/obsidian-finance/scripts/assess_work.py", "--root", "/private/tmp/acceptance-input-bdt15m4b", "--snapshot", "snapshot.json", "--mode", "latest", "--cutoff", "2024-08-31T23:59:59+00:00"], "exit": 0, "result": {"cutoff": "2024-08-31T23:59:59+00:00", "decisions": [{"action": "create_next_quarter_analysis", "affected": ["business-analysis", "financial-analysis", "forecast", "synthesis", "valuation"], "evidence": ["q3"], "reason": "Eligible source declares an unrepresented later fiscal quarter", "record": "q2", "work": null}], "excluded": [], "external_freshness": "unverified", "gaps": [], "mode": "latest", "observations": [], "reusable": [{"record": "q2", "work": "valuation"}], "scope": "supplied_local_evidence", "status": "complete", "version": 1}, "stderr": "", "inputs_unchanged": true}
{"case": "Missing required evidence", "command": ["/private/tmp/finance-validation-env/bin/python", "/private/tmp/finance-acceptance-clean/obsidian-finance/scripts/assess_work.py", "--root", "/private/tmp/acceptance-input-bdt15m4b", "--snapshot", "snapshot.json", "--mode", "latest", "--cutoff", "2024-05-03T23:59:59+00:00"], "exit": 2, "result": {"cutoff": "2024-05-03T23:59:59+00:00", "decisions": [{"action": "record_gap_and_continue_independent_work", "affected": [], "evidence": ["missing"], "reason": "Evidence requires recovery", "record": "q2", "work": null}], "excluded": [], "external_freshness": "unverified", "gaps": [{"evidence": "missing", "reason": "Required source missing, inconsistent or ineligible", "record": "q2", "recovery": "Supply or verify the identified local evidence and retry"}], "mode": "latest", "observations": [], "reusable": [{"record": "q2", "work": "valuation"}], "scope": "supplied_local_evidence", "status": "partial", "version": 1}, "stderr": "", "inputs_unchanged": true}
Freshness unknown: unverified; no last-success invented
{"case": "No research records", "command": ["/private/tmp/finance-validation-env/bin/python", "/private/tmp/finance-acceptance-clean/obsidian-finance/scripts/assess_work.py", "--root", "/private/tmp/acceptance-input-bdt15m4b", "--snapshot", "snapshot.json", "--mode", "latest", "--cutoff", "2024-05-03T23:59:59+00:00"], "exit": 2, "result": {"cutoff": "2024-05-03T23:59:59+00:00", "decisions": [], "excluded": [], "external_freshness": "unverified", "gaps": [{"evidence": "records", "reason": "No research records supplied", "record": null, "recovery": "Supply or verify the identified local evidence and retry"}], "mode": "latest", "observations": [], "reusable": [], "scope": "supplied_local_evidence", "status": "partial", "version": 1}, "stderr": "", "inputs_unchanged": true}
{"case": "Invalid request", "command": ["/private/tmp/finance-validation-env/bin/python", "/private/tmp/finance-acceptance-clean/obsidian-finance/scripts/assess_work.py", "--root", "/private/tmp/acceptance-input-bdt15m4b"], "exit": 64, "result": null, "stderr": "Invalid assessment request: the following arguments are required: --snapshot, --mode, --cutoff; correct arguments and retry", "inputs_unchanged": true}
{"case": "Unreadable local data", "command": ["/private/tmp/finance-validation-env/bin/python", "/private/tmp/finance-acceptance-clean/obsidian-finance/scripts/assess_work.py", "--root", "/private/tmp/acceptance-input-bdt15m4b", "--snapshot", "bad.json", "--mode", "latest", "--cutoff", "2024-05-03T23:59:59+00:00"], "exit": 1, "result": null, "stderr": "Cannot read assessment input bad.json: Expecting value: line 1 column 2 (char 1); supply correct in-root prototype-v1 evidence and retry", "inputs_unchanged": true}
{"case": "Unsupported input", "command": ["/private/tmp/finance-validation-env/bin/python", "/private/tmp/finance-acceptance-clean/obsidian-finance/scripts/assess_work.py", "--root", "/private/tmp/acceptance-input-bdt15m4b", "--snapshot", "snapshot.json", "--mode", "latest", "--cutoff", "2024-05-03T23:59:59+00:00"], "exit": 1, "result": null, "stderr": "Cannot read assessment input snapshot.json: Unsupported assessment input version; supply correct in-root prototype-v1 evidence and retry", "inputs_unchanged": true}
{"case": "Escaping reference", "command": ["/private/tmp/finance-validation-env/bin/python", "/private/tmp/finance-acceptance-clean/obsidian-finance/scripts/assess_work.py", "--root", "/private/tmp/acceptance-input-bdt15m4b", "--snapshot", "snapshot.json", "--mode", "latest", "--cutoff", "2024-05-03T23:59:59+00:00"], "exit": 1, "result": null, "stderr": "Cannot read assessment input snapshot.json: Reference outside assessment root: ../outside.txt; supply correct in-root prototype-v1 evidence and retry", "inputs_unchanged": true}
{"case": "Stop and retry (fresh CLI invocation)", "command": ["/private/tmp/finance-validation-env/bin/python", "/private/tmp/finance-acceptance-clean/obsidian-finance/scripts/assess_work.py", "--root", "/private/tmp/acceptance-input-bdt15m4b", "--snapshot", "snapshot.json", "--mode", "latest", "--cutoff", "2024-05-03T23:59:59+00:00"], "exit": 0, "result": {"cutoff": "2024-05-03T23:59:59+00:00", "decisions": [{"action": "no_analysis_update", "affected": [], "evidence": ["price"], "reason": "Completed outputs and relevant dependencies agree within supplied evidence", "record": "q2", "work": null}], "excluded": [], "external_freshness": "unverified", "gaps": [], "mode": "latest", "observations": [], "reusable": [{"record": "q2", "work": "valuation"}], "scope": "supplied_local_evidence", "status": "complete", "version": 1}, "stderr": "", "inputs_unchanged": true}
ALL CLI CASES PASSED; interruption itself is covered by focused test_interrupted_retry, not this subprocess walk.

```
