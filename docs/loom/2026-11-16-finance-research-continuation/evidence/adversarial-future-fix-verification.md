# Future-history fix and probe-location verification

Target product: `f4d639aab612f15510f1600319c78b6adcda1b23`.
Counts: **15 previously named attack points rerun; 0 remaining successful
attacks; 0 new programs; 1 existing-program bootstrap update committed.**
The eight previously failing variants now hold. Original RED `a58e8e6` and
the earlier reports/counters remain. No native/vendor calls or study writes ran.

## Actual fix verification

```sh
/private/tmp/finance-validation-env/bin/python -m pytest docs/loom/2026-11-16-finance-research-continuation/evidence/probes/test_future_history_validation.py -p no:cacheprovider
/private/tmp/finance-validation-env/bin/python /private/tmp/finance-future-adversary-trial.py
```

The first command passed both cases. The second completed all fifteen previous
named disposable cases, exit 0. Scalar, missing-field and economic-kind frozen
analysis identities now yield quarter-scoped gaps. Missing/invalid-JSON/failed/
output-mismatched verification and absent verification alongside a saved output
also yield quarter-scoped gaps. Each retains six earlier reusable units and all
preexisting fixture bytes. The structurally complete old frozen method remains
acceptable without comparison to the current selected method. Valid future chain
and equal-cutoff controls remain complete (six/twelve reusable units). Missing
output path remains a safe loud ValueError; escaping output and absent digest
remain explicit gaps. Output-less partial unit remains the previously qualified
boundary, not a new finding.

## Owned bootstrap change

Commit `4f6540b` replaces the fixed `parents[5]` root with the nearest ancestor
containing the actual package script. Only import-location setup changed; every
logical test line, fixture manipulation and assertion is unchanged. The same
committed file runs from the reserved store and intended normal test directory.
The product and test locations in the original checkout were not moved.

Git-memory classification: routine location compatibility, with rationale fully
shown in the diff; no earned durable lesson/trailer. Exact message file
`/private/tmp/finance-bootstrap-commit.txt` passed the required deterministic
privacy scan (exit 0, `[]`), no ambiguous identifiers requiring a semantic judge.
The initial commit used authorized escalation for the worktree git index.

## Actual committed-program regression tests

Created a disposable committed tree using:

```sh
mkdir -p /private/tmp/finance-future-probe-committed-copy
git archive 4f6540b | tar -x -C /private/tmp/finance-future-probe-committed-copy
```

All following runs use that directory. The host edit tool applied exact source
mutations; no copy of probe logic was used and the committed probe stayed intact.
Product mutations were undone using the same edit tool after every run.

1. Replace only `obsidian-finance/scripts/research_store.py` with exact
   `git show eac3f25:obsidian-finance/scripts/research_store.py` bytes. Run the
   unchanged committed store program with the first pytest command above:
   **2 failed**, both `complete != partial`, exit 1. This restores the original
   behavior rejected by the original RED and checks that bootstrap changes do
   not accidentally import the fixed original checkout.
2. Restore fixed product. Replace the future-only `_analysis_identity(frozen)`
   call with `pass`, leaving completion validation intact. Same command:
   **1 failed (malformed-analysis), 1 passed**, exit 1.
3. Restore the analysis validation. Remove only the four-line future completion
   verification block, leaving output integrity intact. Same command:
   **1 passed, 1 failed (missing-check)**, exit 1. Restore that block afterward.
4. Copy the exact committed program bytes to
   `obsidian-finance/tests/test_future_history_validation.py` **in the disposable
   copy only**. Run:

   ```sh
   /private/tmp/finance-validation-env/bin/python -m pytest obsidian-finance/tests/test_future_history_validation.py -p no:cacheprovider
   ```

   Fixed product: **2 passed**, exit 0. Restore exact pre-fix `eac3f25` product
   again and rerun the same normal-home command: **2 failed**, exit 1. Restore
   fixed product afterward. This catches an over-broad bootstrap workaround
   that would bind tests to the fixed original checkout regardless of test home.

SHA-256 of both disposable program copies:
`1db39b6c47b03a4a71dce7f04c91e474f00e71a9cb3ac680589f07f07f955106`.
Final restored disposable product SHA-256:
`526f66a9fbc0204d0ac59ebf969fd39045c5f01984113798287f262d360b1504`.
The copy is retained for inspection; no force/discard command was used.

No remaining fatal/important finding in the requested two-class verification.
This is mechanical fix verification, not investment-quality or native-host
acceptance. Build owns byte-for-byte graduation and parent owns the full suite.
