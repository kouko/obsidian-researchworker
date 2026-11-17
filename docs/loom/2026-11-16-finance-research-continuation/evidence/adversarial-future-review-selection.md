# Future-review-selection adversary

Counts after the requested class sweep: **15 attack points attempted; 8 exposed
the two failure classes and earned coverage; 1 RED
program committed.** Target `eac3f25b94f5d000067298e4fb7bb50434115122`.
The prior dependency-preparation report and all original programs remain.

Read the changed code/tests, research/12, W3-03 scope and the code recipe.
No declared mutation/fuzz configuration was found in the package configuration
inventory. Disposable boundary cases used existing `two_issuers`, `load` and
`put` helpers; no actual study was read or written by the trial runner.

## Actual attacks

1. Future unit `analysis_inputs = {'bad-method': 7}`: **BROKE**. Earlier-cutoff
   discovery returned `complete`, no gaps, six earlier reusable units. The
   future-only branch validates only the outer object, hiding a malformed frozen
   identity. An initial None variant also returned complete; the final RED pins
   an unmistakably malformed scalar rather than a missing optional binding.
2. Delete a future completed unit's referenced verification file: **BROKE**.
   Discovery again returned `complete`, no gaps and six earlier reusable units.
   An incomplete saved unit is treated as valid future-only history.
3. Remove future output's `path`: held by loud refusal, `ValueError` wrapping
   missing `path`. This stops discovery rather than silently ignoring corruption.
4. Future output path `../outside.md`: held, `partial` with an escaping-reference
   review gap. No external content was accessed by the trial.
5. Two future reviews in a valid predecessor chain: held, earlier-cutoff result
   complete with six earlier units and no spurious future-quarter gap.
6. Cutoff exactly equal to the saved later review: held, twelve units reusable;
   the strict future exemption does not exclude the equal-cutoff review.

The scratch runner `/private/tmp/finance-future-adversary-trial.py` executed all
six cases. Its first invocation stopped at case 3's loud refusal; the subsequent
invocation caught expected ValueError and completed, exit 0. Every non-refusal
case compared all existing fixture bytes before/after and found them unchanged.
This runner is a disposable attempt, not an additional committed program.

## RED program and findings

```sh
/private/tmp/finance-validation-env/bin/python -m pytest docs/loom/2026-11-16-finance-research-continuation/evidence/probes/test_future_history_validation.py -p no:cacheprovider
```

Observed: **2 failed**, both `complete != partial`, exit 1 on the unchanged
target. One small parametrized program pins two missing-validation classes;
no green-on-arrival program, text-mirroring assertion or product fix was added.
Existing mechanical regression command additionally passed **48 tests**:

```sh
/private/tmp/finance-validation-env/bin/python -m pytest obsidian-finance/tests/test_research_store.py obsidian-finance/tests/test_research_continuation.py -p no:cacheprovider
```

**Important:** `obsidian-finance/scripts/research_store.py`, future-only validation
before `return []`: malformed frozen analysis entries and absent referenced
verification artifacts bypass the real-gap guard. The ordinary earlier research
is not made stale, but the newly introduced exemption advertises whole-request
completion while concealing malformed/incomplete local history. This is reachable
through ordinary saved-file damage or untrusted metadata; it does not require
deliberately defeating a Loom internal rule. Close by validating the saved
analysis envelope and referenced verification integrity before the exemption;
retain a quarter-scoped gap for defects without making future facts eligible or
requiring current economic dependencies to equal an old historical review.

Commit classification: the failure is directly documented by the executable
probe and evidence; no additional durable lesson or implementation choice is
introduced by this test-only commit. No memory trailers. Exact final commit text
is privacy-scanned before commit; no private-party identifiers require a semantic
judge. Parent owns the product repair, complete suite and subsequent acceptance.

## Requested whole-class extension

Parent requested this extension after the initial RED program was committed as
`a58e8e6`. Reran the disposable runner with fifteen named cases, exit 0.
No probe or product code changed. The first six attempts above remain actual
history; the cumulative named case inventory is below.

| Case | Actual earlier-cutoff result | Assessment |
|---|---|---|
| Scalar frozen analysis identity `7` | complete, no gaps, 6 reusable | Important malformed-envelope failure |
| Frozen identity missing authored_at | complete, no gaps, 6 reusable | Same important malformed-envelope failure |
| Frozen identity kind economic-source | complete, no gaps, 6 reusable | Same important economic/authored distinction failure |
| Structurally complete old method identity differing from current inputs | complete, no gaps, 6 reusable | Held temporal boundary; not a finding |
| Referenced verification file deleted | complete, no gaps, 6 reusable | Important incomplete-evidence failure |
| Referenced verification contains invalid JSON | complete, no gaps, 6 reusable | Same important malformed-evidence failure |
| Verification sources check is false | complete, no gaps, 6 reusable | Same important failed-evidence failure |
| Verification output_digest differs from bound output | complete, no gaps, 6 reusable | Same important unbound-evidence failure |
| Output retained but verification field omitted | complete, no gaps, 6 reusable | Same important absent completion evidence failure |
| Output object omitted, old verification retained | complete, no gaps, 6 reusable | Recorded boundary; no separate finding because output-less units may be partial |
| Output digest omitted | partial with future-review output gap | Held |
| Output path omitted | loud ValueError | Held safe refusal, not silent completion |
| Output path escapes root | partial with escaping-reference gap | Held |
| Valid future predecessor chain | complete, no gaps, 6 reusable | Held |
| Cutoff equals future review cutoff | complete, no gaps, 12 reusable | Held |

All successful-return cases preserved every existing fixture byte. The temporal
control intentionally does not demand that a future frozen method equal the
currently selected method or that its old source still be available today. The
repair must distinguish structural/completion-evidence validation from changing
current economic or method identity. The missing-output-object observation is
not included in the eight demonstrated false-complete cases or promoted into a
new finding. No fatal finding was demonstrated. The two important classes above
are the complete discovered findings for this dispatch; no further native call
or actual-study mutation was performed.
