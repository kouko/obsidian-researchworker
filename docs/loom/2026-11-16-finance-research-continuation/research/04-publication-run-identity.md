# Publication run identity follow-up

Status: reproduced observation; repair deferred until the frozen W2-01 trials
finish. This does not revise their baseline or count a helper repair as skill
improvement.

## Evidence

At helper HEAD `56d276a`, the retained `missing-skill-3` trial has two immutable
run requests targeting review `partial3`. The first run
`missing-skill-3-checkpoint` failed research-envelope validation. A second run,
`missing-skill-3-checkpoint-fixed`, corrected `research.changes` from a list to a
string and published the partial checkpoint. Both requests retain their own
distinct `review.publication.run` identities.

Main-agent read-only reproduction on the existing trial root on 2026-11-16:
`discover(root, 'latest', '2024-08-31T23:59:59+00:00')` returns no publication
gaps, despite the retained failed first request. Overall status remains partial
for other research gaps; no claim of globally completed research follows.
The first inspection command mistakenly accessed a nonexistent `fiscal.quarter`
key and raised `KeyError`; removing that unnecessary lookup yielded the
observation without changing trial data.

## Class and bounded search

Class: publication lifecycle inferred from a shared destination instead of
matching the immutable run identity. The discovery loop in `research_store.py`
skips a journal whenever its target contains any `review.json` or
`abandoned.json`, without checking whether that destination belongs to that
run. This can conceal the earlier unfinished attempt after a different run
publishes the same destination.

The main agent searched whole contents of every committed changed file against
trunk `af839dd`, plus the publication tests and the plan's Acceptance 5 recovery
surfaces, for `abandoned.json`, publication/run identity, unfinished publication,
pending markers and existing-run checks. Results are retained locally at
`/private/tmp/finance-publication-identity-sweep.txt`. The concrete flagged
instance is the discovery journal loop. Recovery already checks several marker
and request identities; W2-02 must test those boundaries rather than assume all
markers are equally affected. No code change has been made by the main agent.

## W2-02 obligation

Add a failing integration example for distinct failed/successful runs sharing
a destination. Discovery must retain a truthful recovery/conflict observation
for the failed run, preserve the successful checkpoint and all drafts, and
never let rollback of the older failed run withdraw another run's publication.
The implementer should decide the smallest compatible repair after checking
the complete lifecycle. Preserve frozen-trial results and original failures.
