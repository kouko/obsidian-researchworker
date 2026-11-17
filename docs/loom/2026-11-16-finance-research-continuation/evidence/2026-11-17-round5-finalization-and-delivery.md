---
title: Round 5 finalization and delivery revalidation
type: loom-research
status: concluded
created: 2026-11-17
updated: 2026-11-17
tags: [loom/research]
change: 2026-11-16-finance-research-continuation
---

# Round 5 finalization and delivery revalidation

Question: does current normal verification establish local delivery after the
full-case trials? Inspect installed 3.84.0 behavior and actual results at
03b38d2/683f128, without editing the checker, refs, prerequisite attestations
or reviewed functional content. This direct verification record preserves the
frozen [earlier investigation](../research/02-stacked-delivery-attribution.md).

The same two original reviewers returned PASS_WITH_NOTES, no findings, at
03b38d2ab4c20740cfddbf27bb69f26ee6a4a5b3. Raw YAML is retained beside this
record. Normal finalize-review with the retained temporary Round5 input and
isolated pytest interpreter on PATH exited0: package-tests passed, then both
declared adversarial commands passed. It generated the unedited attestation
with content_digest65d2b665c806dceb64ef9b0b751a6eedf6c3123c,
tested_commit3547b84 and reviewed_commit03b38d2. All six acceptance rows are
works. The generated file and raw reviews were committed at683f128.

The earlier 6>5 refusal remains historical evidence. Current read-only
check_adversarial_proportionate counts two graduated programs and no stored
programs, and returns no findings. MAX_PROBE_PROGRAMS remains5. Do not claim
the checker now implements the user's exception or reconstruct the historical
count from a later version. No test deletion, checker patch or counter reset
was made to obtain this result.

Both ordinary delivery --json and the explicit --goal local --intent
/private/tmp/finance-research-continuation/docs/loom/intent/2026-11-16-finance-research-continuation.md
observation returned exit1, stateunconfirmed, cannot identify a committed
change, completefalse. The installed verification.identify_change diagnostic
at683f128 recognizes the correct branch/intent, then rejects three attestation
identities in the actual aa1c0cb trunk delta: finance-sec-baseline,
finance-work-assessment and finance-research-continuation. verification_status
reports stale(branch carries3attestations). Supplying an intent cannot bypass
this: observe_delivery identifies the change before comparing that path.

Method: inspect verification.py:identify_change/_delta, helpers.py:changed_paths,
command_handlers/publish.py:observe_delivery and probes.py; execute only their
default read-only diagnostics. The [full result](2026-11-17-round5-delivery-diagnosis.json)
is also retained at /private/tmp/finance-round5-delivery-diagnosis.json, reproduced by
/private/tmp/finance-delivery-diagnosis.py through normal loom-python --ready.
No alternate base was passed. No remote action or global repair was performed.

Decision: current finalizer evidence is real, but delivery remains unconfirmed.
Preserve all three identities; do not rename an already recognized branch,
fake trunk, delete prerequisite evidence or retry unchanged. Legitimate
prerequisite publication/integration or a separately scoped Loom repair could
change attribution, neither is authorized here. Continue substantive A–G
research under the user's workflow-first strategy. Original SEC-reading,
external-freshness, installed loading, Stop-hook and research-coverage limits
remain; neither this local signature nor this investigation completes A–G.
