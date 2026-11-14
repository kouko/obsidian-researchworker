---
title: "Preserve imported history through squash merge"
type: loom-research
status: concluded
created: 2026-11-14
updated: 2026-11-14
change: 2026-11-14-extract-obsidian-plugin
tags:
  - loom/research
---

# Preserve imported history through squash merge

## Question and scope

Can the installed Loom Land command merge PR #1 while preserving the 131
mapped Obsidian history commits required by Acceptance #1? The user authorized
document corrections, checks and conditional merge on 2026-11-14. This is about
Git reachability, not runtime acceptance, which remains unmet.

## Method and rationale

Inspect the exact installed merge implementation and current Git graph, then
use a bounded reachability check. These sources settle the local behavior;
no broader external research or new permanent verification program is needed.
Compare the existing squash route alone with retaining a dedicated history
reference. Do not change the installed merge implementation or use an alternate
merge route.

## Findings

- Source observation: installed loom-code 3.78.0
  `scripts/loom_checker/command_handlers/land.py:814-844` calls
  `gh pr merge --squash --match-head-commit`, with the PR title/body.
  Its history cleanup removes the feature branch; it does not create an
  archival history reference.
- Git observation: `git show -s --format='%H %P %s' 5812fa7` shows the original
  join parents as `9814589dbe025bcac73e35d0263995a18b8be62b` and imported tip
  `3c95872cb266a54af38f5a43485da4b9aa0c06fd`.
- Measured: `git rev-list 3c95872cb266a54af38f5a43485da4b9aa0c06fd` returned
  131 commits. Comparing that set with all destination values in
  [the durable mapping](../../../provenance-commits.json) found zero missing
  mapped commits. This uses the existing imported inventory; it does not redo
  predecessor discovery or prove exhaustive semantic history.
- Inference from the merge operation: squash preserves the final tree but
  does not make the imported commits ancestors of the new main commit.
  Relying on an eventually deleted feature branch would not preserve ordinary
  clone access to those commits.
- Live observation: the GitHub matching-ref query for
  `heads/archive/obsidian-3.27.0-history` returned an empty array. A subsequent
  creation-only `POST /repos/kouko/obsidian-researchworker/git/refs` returned
  `refs/heads/archive/obsidian-3.27.0-history`, object type `commit`, and SHA
  `3c95872cb266a54af38f5a43485da4b9aa0c06fd`. No existing ref was overwritten.

## Evidence

The implementation inspected is the installed version at
`/Users/kouko/.codex/plugins/cache/loom/loom-code/3.78.0/`, not an assumed
upstream HEAD. The graph and mapping came from the clean PR clone at functional
baseline `9acae3c5b261199d7b4601c361d28cb05a7e0993`.

The created ref is
[`archive/obsidian-3.27.0-history`](https://github.com/kouko/obsidian-researchworker/tree/archive/obsidian-3.27.0-history).
The matched ref and creation response were observed through the existing
authenticated GitHub CLI. The connected GitHub app returned 404 for this
Private repository, so it was not treated as evidence that the repository
or PR was absent.

## Decision impact

Keep Land unchanged and retain this dedicated archival branch before merging.
This adds one Git reference, preserves the explicit history requirement and
avoids a manual merge bypass. The alternative of squash alone loses ordinary
history reachability after cleanup; changing the merge tool is outside this
documentation repair. The archive is history, not a released runtime version
or a replacement for main.

## Limitations and open questions

The remote branch must remain available until another verified archival
reference replaces it. Its existence does not prove the subsequent PR merge
or main CI; Ship must observe those independently. The original path-discovery
and signature limitations remain unchanged. Actual note creation is still
unverified and is not supplied by this research.
