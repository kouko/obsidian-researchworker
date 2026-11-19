---
title: Stacked local changes and delivery identification
type: loom-research
status: concluded
created: 2026-11-16
updated: 2026-11-16
tags: [loom/research]
change: 2026-11-16-finance-research-continuation
---

# Stacked local changes and delivery identification

## Question and scope

Why does local delivery remain unconfirmed on a correctly named, confirmed
change branch, and can current supported observation disambiguate the accepted
unmerged prerequisites without removing evidence or changing trunk refs?
Conditions: installed loom-code 3.82.0, this branch at 912bac8, original local
and remote trunk af839ddc6ace9580cf94276ae60fa47697ea7979. No publication,
upstream plugin repair, ref rewrite or false completion is authorized.

## Method and rationale

Read the installed delivery handler, identification function and connected
branch-delta implementation; compare the actual CLI observation with direct
read-only function diagnostics. This isolates attribution from project tests.
An explicit function-base comparison is diagnostic only, not a substitute
delivery command, attestation or permission to alter the base.

## Findings

The branch name and intent are recognized. Identification then rejects the
whole trunk delta because it contains prerequisite attestations for two other
accepted local changes. The CLI discards that detailed reason and reports only
`cannot identify a committed change`. Supplying `--intent` does not fix it:
the handler identifies the change first and compares the intent afterward.

The current delivery CLI accepts only goal, intent and JSON options; no explicit
stacked-base option is documented. The underlying function does accept a base,
but the ordinary delivery handler does not supply one. Existing attestations
cannot be removed merely to make the branch match. Adding the new attestation
later will not by itself remove the two predecessor identities from the delta.

## Evidence

Installed source inspected (read-only, 3.82.0):

- `scripts/loom_checker/verification.py`, `_delta` and `identify_change`:
  default delta uses `changed_paths`; recognized branch intent is followed by
  the condition that delta attestations equal only the selected change ID.
- `scripts/loom_checker/helpers.py`, `branch_base` and `changed_paths`:
  trunk candidates determine the merge-base; committed, dirty and untracked
  paths all enter the delta. No selected stacked prerequisite is supplied here.
- `scripts/loom_checker/command_handlers/publish.py`, `observe_delivery`:
  `identify_change(repo)` runs before the optional canonical-intent comparison;
  its detailed diagnostic is not retained in the user-facing result.

Actual observation:

```sh
/Users/kouko/.codex/plugins/cache/loom/loom-code/3.82.0/scripts/loom-python --ready delivery --goal local --intent docs/loom/intent/2026-11-16-finance-research-continuation.md --json
```

Exit 1; state `unconfirmed`, reason `cannot identify a committed change`,
`complete: false`. A read-only Python call of the same installed function gave:

```text
branch_base af839ddc6ace9580cf94276ae60fa47697ea7979
identify_change (None, "the branch identifies change '2026-11-16-finance-research-continuation' but its attestation names 2026-11-15-finance-sec-baseline, 2026-11-15-finance-work-assessment; rename the branch to <type>/<change-id> or commit the intent docs/loom/intent/<change-id>.md")
diagnostic_explicit_stacked_base ('2026-11-16-finance-research-continuation', None)
```

The last line passed actual accepted prerequisite `e7faf87` to the underlying
function's `base` argument. It confirms the attribution condition, not CLI
delivery success. No refs, installed plugin files or attestations were edited.

## Decision impact

Agent-decided — preserve prerequisite evidence and continue authorized local
research/implementation with explicit delivery-unconfirmed status. Branch
renaming does not solve the demonstrated condition because its intent is
already recognized. Do not fake origin/main, delete attestations, monkey-patch
the installed checker or reinterpret a diagnostic function call as delivery.
Publication/merge of prerequisites would change trunk attribution but remains
outside current authorization; it is not a technical default to take here.

This question is resolved as a documented unsupported stacked-attribution path
in the installed command, not a repaired checker. A separately authorized
upstream fix or legitimate prerequisite integration could change it; neither
has happened. Functional and research verification must still run independently.

## Limitations and open questions

No claim about later checker versions or every possible repository follows.
No issue/comment was sent externally. Final delivery must run the required
ordinary command and disclose its actual result; this record cannot pre-approve
that later observation or waive independent acceptance. The full A-G objective
remains incomplete for substantive reasons as well as unresolved delivery status.
