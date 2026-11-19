# Resumed review: independent passes, mechanical refusal retained

The user explicitly authorized temporary unlimited review rounds and an
exception to the five-program cap for the original Stage A-G program. This
resumed fourth round keeps the original episode, reviewer identities, retry
history and prior terminal outcome; no step was skipped.

Committed reviewed target: `4c649a6c3b3197aa3598afc39bc1720144c6c3b9`.
The same original code and skill reviewers returned conforming
PASS_WITH_NOTES, no findings. Exact returned YAML is retained as raw evidence
in the two adjacent `2026-11-17-resumed-round4-*-raw.yaml` files, not as a
second attestation. Code review independently ran five integrated test files:
54 passed in 2.71s, no skipped cases. Prior external-source/Decimal audit
limitations remain. No important/fatal finding was dismissed.

The independent clean acceptance target is `bfee85e`; the canonical report
fully re-tests changed entry rows 1/7/16 and carries unaffected actual host
behavior with explicit reasons. Its preceding report is archived exactly,
and detailed evidence preserves the entire earlier prefix. Build at the
same functional tree observed 232 package passes in 31.59s followed by 15
reused-program passes in 1.22s. These are not finalizer executions.

## Normal finalization attempt

After both current-target verdicts were validated, the normal installed
finalizer ran with the existing isolated pytest interpreter on PATH and the
new temporary input `/private/tmp/finance-continuation-finalize-resumed-round4.json`:

```sh
PATH=/private/tmp/finance-validation-env/bin:$PATH /Users/kouko/.codex/plugins/cache/loom/loom-code/3.82.0/scripts/loom-python --repair finalize-review 2026-11-16-finance-research-continuation --input /private/tmp/finance-continuation-finalize-resumed-round4.json
```

Exit 1:

```text
BLOCK adversarial.proportionate: 6 probe programs for this change (committed under its store, executed by finalize-review, or graduated into the package suite); at most 5 are allowed
Help: "<loom-code>/scripts/loom-python" --ready finalize-review --help (replace <loom-code> with the installed loom-code plugin directory).
Suggested next step: Resolve the reported review or execution evidence through its owning workflow before deliberately rerunning finalization.
```

The implementation still compares a fixed constant; it has not represented
the user's exception. Refusal precedes this finalizer's package/probe runs
and attestation generation. No checker/cache patch, test deletion, alternate
trunk, runtime injection, hand-written attestation or success substitution
was used. No current attestation exists. Do not repeatedly re-run the same
unchanged failing check or generate another review round solely to retry it.

## Separate delivery identity observation

The normal installed `loom-python --ready delivery --json` returned exit 0
but JSON `state: unconfirmed`, `reason: cannot identify a committed change`,
`evidence: {}`, `complete: false`. Successful process exit does not mean
successful delivery. This retained stacked-change identity limitation is
separate from the cap failure and from passing behavior tests.

## Continuation

The previous terminal outcome remains a true historical failure; this later
record supersedes only the claim that no further round was authorized. Both
exceptions are now explicit, yet formal completion still lacks normal tool
support/evidence. C/F delivery remains unconfirmed. Original Stage E and other
independent required research can continue; no A-G completion, publication,
global installation, paid-provider obligation or formal vault change follows.
