# Trunk registry conflict during authorized resumption

This is a same-task Build repair for the original Stage A-G program. Earlier
failures, counters and the terminal outcome remain retained. No runtime finance
behavior, architecture, global installation, provider execution or publication
is added by this local integration.

## Observed state and defect class

Pre-merge HEAD: `216254bc707b7b961bf09ff72849c496f7d3741d`.
Fetched trunk: `aa1c0cb259b393571b70bd270b56e25ddb70ff7a`.
The parent observed normal `loom-python --repair sync-trunk` refusing with
`BLOCK review.sync` because `.claude-plugin/marketplace.json` would conflict;
it did not merge. This refusal is preserved, not represented as a successful
sync. Ordinary local integration is explicitly authorized for this task.

The exact command was
`/Users/kouko/.codex/plugins/cache/loom/loom-code/3.82.0/scripts/loom-python --repair sync-trunk`.
Before ordinary metadata escalation it returned exit 0 with a fetch warning
because shared `FETCH_HEAD` could not be opened (`Operation not permitted`).
After ordinary escalation, it returned exit 1:

```text
BLOCK review.sync: conflict: .claude-plugin/marketplace.json
BLOCK review.sync: the merge was not attempted; feat/2026-11-16-finance-research-continuation is still at 216254bc707b7b961bf09ff72849c496f7d3741d and the worktree is untouched.
BLOCK review.sync: Conflicts are never resolved automatically -- resolve them in a new build round.
Suggested next step: Preserve outstanding work and resolve the reported trunk condition before deliberately rerunning the existing sync workflow.
```

Class: **competing updates to shared plugin registry**. Before editing, the
whole content of branch-touched files was searched with:

```sh
git diff --name-only -z origin/main...HEAD | xargs -0 rg -l '14 Obsidian skills|"version": "4\.1\.0"'
```

The sole matching branch-touched file was `.claude-plugin/marketplace.json`.
The root README, finance README, both finance plugin manifests and both
Obsidian manifests were also inspected in full/search context as live package
surfaces. The two older Obsidian manifests were 4.1.0 before integration and
are updated verbatim by trunk to 4.2.0. The root README's existing 4.1.0 prose
is outside this registry-conflict repair; no historical records are rewritten.
Scoped git-memory recall found the earlier separate finance-registration
decision in `0b7030f`; this repair preserves that package boundary.

## Resolution and direct verification

`git merge --no-commit --no-ff aa1c0cb259b393571b70bd270b56e25ddb70ff7a`
returned exit 1 with these literal status lines:

```text
Auto-merging .claude-plugin/marketplace.json
CONFLICT (content): Merge conflict in .claude-plugin/marketplace.json
Automatic merge failed; fix conflicts and then commit the result.
```

This was the only unmerged path. Keep the upstream Obsidian 4.2.0/15-skills
entry exactly and the pre-merge finance 0.1.0 entry exactly. No new permanent
test is warranted for this merge-only metadata resolution.

- JSON/object assertions returned exit 0: exactly two distinct plugin names;
  upstream Obsidian entry equality; pre-merge finance entry equality; existing
  source directories; matching Claude/Codex manifest names and versions; 15
  actual Obsidian skill directories.
- `/private/tmp/finance-validation-env/bin/python -m pytest obsidian/tests/test_skill_inventory.py obsidian/tests/test_opencode_loader.py -q -p no:cacheprovider`
  returned exit 0: `5 passed in 0.44s`.
- The merge command also printed `When finished, apply stashed changes with
  git stash pop`; `git stash list -3` returned exit 0 with no entries. No stash
  operation is needed or performed.
- The first supplementary surface-search invocation returned exit 2 because
  `.agents/AGENTS.md` does not exist; the actual named surface files were
  inspected, and a subsequent existing-surface search returned no old manifest
  version/14-skills matches. This is not a test failure hidden as a pass.

The two new independent acceptance resumption reports remain untracked and
must not enter this merge commit. The parent owns ordered post-merge Build
checks, including the complete package suite and reused adversarial programs.
