# Trunk sync authorization boundary

Status: local sync requires user authorization; no rejected action was executed.

## Observed rejection

At feature HEAD `8ae200a`, invoking the normal mandated command
`loom-python --repair sync-trunk` through normal outer sandbox escalation was
rejected before process creation by automatic approval review:

> The requested sync-trunk operation may mutate the feature branch by merging
> or rebasing trunk, conflicting with the explicit constraint not to merge;
> its exact side effects are not established.

The rejection also prohibited bypass through indirect execution. No raw merge,
rebase, cherry-pick, alternate-worktree integration, rule change or hook bypass
was attempted. The feature HEAD and files remained unchanged by the rejected
command. This is not a checker `WARN review.sync` or a successful unsynced gate.

## Read-only investigation

The installed 3.82.0 handler
`scripts/loom_checker/command_handlers/sync.py`, lines 209–336, fetches trunk and
can merge or rebase when its tip is not already contained. The local branch
does not contain the current main tip: `merge-base --is-ancestor` returned 1;
the common ancestor remains `af839dd`.

The GitHub connector independently resolved current `main` to
`d87f7d5de370f9dafa2be4572dd44f26bdc53813`, matching the existing remote-tracking
ref. Its sole intervening commit is
[the OpenCode identity/commands update](https://github.com/kouko/obsidian-researchworker/commit/d87f7d5de370f9dafa2be4572dd44f26bdc53813).
The read-only local diff lists ten paths: root README, migration documentation,
the other change's retained Loom records, the Obsidian OpenCode loader/package
and two loader tests. Finance code is not among that trunk delta. This does not
prove conflict-free integration or authorize performing it.

Current own-versus-unpushed commit counts are 71 and 38, respectively, with
zero own merge commits. Under the inspected `_may_rebase` condition this state
does not qualify for automatic rebase; commit IDs must remain preserved. Recheck
remote state before any subsequently authorized action rather than assuming
this observation remains current.

## Unaffected verification

The current feature branch's complete suite ran independently as a diagnostic:

```text
/private/tmp/finance-validation-env/bin/python -m pytest obsidian/tests obsidian-finance/tests -q -p no:cacheprovider
180 passed in 27.15s
```

It does not satisfy the ordered end-of-Build verification on synchronized trunk.
No adversary or closing reviewer was dispatched past this unmet sync boundary.
After authorized integration, rerun the required end-of-Build sequence. Existing
host sessions, source evidence, original failures and accepted prerequisite
records remain intact. Publication, PR creation and PR merge stay unauthorized.

The ordinary `loom-python --ready delivery --json` was also rerun read-only:
exit 1, `state=unconfirmed`, `reason=cannot identify a committed change`,
`complete=false`. The existing stacked-attribution investigation remains
applicable; trunk sync is not claimed to solve that independent limitation.
