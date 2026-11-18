# Executable benchmark helper in the reserved evidence store

Normal finalization at `ce38a6065e5c9584a6a4e6a1a840f18de28d06d1` returned
exit 1 before generating an attestation or running its package/probe executions:

```text
BLOCK adversarial.proportionate: docs/loom/2026-11-16-finance-research-continuation/evidence/skill-eval/make_fixture.py is a program in this change's store outside docs/loom/2026-11-16-finance-research-continuation/evidence/probes/, where the cap and the `concern:` line cannot see it; commit probe programs there
```

No rule was modified, ignored or treated as a passing warning. This is not a
confirmation-only refusal: return to Build, then obtain terminal Round 3
verdicts on the repaired functional content before deliberately finalizing
again. Same requirements, same episode, no round or retry reset.

## Main-agent class sweep before fix

Class: **executable benchmark helper in the reserved evidence store**.
Using the installed checker's `tree_programs` classification (suffix,
executable mode and shebang), inspect all 680 changed paths from
`af839ddc6ace9580cf94276ae60fa47697ea7979` through the failed target.
There are 30 programs; exactly one lies in this change's reserved store:
`evidence/skill-eval/make_fixture.py`. Whole-content reference search across
all changed files finds only `cases.md:8`, `invocation.md:36` and
`preparation.md:16` in that skill-evaluation directory. This also covers the
Acceptance 2/6 behavioral-trial and host-evidence surfaces.

The helper creates synthetic trial inputs; it is not an adversarial probe and
has never earned a red probe. Moving it into `evidence/probes` or disguising its
extension would misclassify it. Deleting it would lose reproduction. Place the
same real helper in `obsidian-finance/tests/fixtures/make_skill_fixture.py`,
adjust its repository-root resolution and update usable references. Preserve
the original preparation failure and clearly identify its original filename.

## Bounded verification

W2-01 follow-up 1 owns the move, root-path adjustment and reference corrections;
it changes neither research method nor trial results. Before moving, run each
of the three cases into fresh temporary roots using the existing interpreter;
after moving, run each case again and compare every generated file byte.
Do not overwrite any retained trial or original failure. No new permanent test
of a one-time move is warranted. Confirm only the existing reused adversarial
program is declared; do not invent a new probe or helper framework.

Normal plan validation, full package tests and the existing adversarial program
must pass on committed repaired content. Independent acceptance checks setup
again, retests affected surfaces and supplies checked carry-over reasons.
Both existing reviewers verify the fix delta in Round 3; no Round 4 is allowed.
