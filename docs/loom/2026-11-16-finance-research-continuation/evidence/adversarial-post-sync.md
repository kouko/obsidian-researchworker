# Post-sync adversarial review

Target: `8fcc8f0ac1b577337c714688e363a6599c4bb97a`, including trunk
`d87f7d5de370f9dafa2be4572dd44f26bdc53813`. Fresh-context adversary.
Changed paths discovered using `git diff --stat af839ddc6ace9580cf94276ae60fa47697ea7979...HEAD`.
Read the shared adversarial protocol and code/spec/skill recipes. Intent,
plan, docs and evidence have no dedicated recipe; attacked their scope and
claim boundaries using the shared protocol. No declared mutation/fuzz tool
was found in relevant package config/source; executable boundary cases used.

Counts: **12 attack points; 0 earned new programs; 1 reused program committed;
0 new programs committed.** No fatal, important or nit findings demonstrated.
These attempts establish bounded resistance, not proof of analytical quality.

## Attempts

1. REQ-1: cold multi-issuer state could silently miss an older unreviewed
   quarter. Existing continuation cases exercised both fiscal calendars and
   older/newer absent, empty, interrupted and withdrawn quarters. Survived.
2. REQ-2: identical local source IDs could invalidate a different issuer or
   omit dependent synthesis. Existing continuation and publication dependency
   cases survived, including source/method/assumption/requirements changes.
3. REQ-3: formatting/mtime-only changes could regenerate research or duplicate
   cycles. Existing cold/repeat tests retained the discovery result and bytes.
4. REQ-4: a partial envelope or historical future evidence could pass complete.
   Existing incomplete-envelope and adjacent-quarter cutoff cases survived.
5. REQ-5: interrupted completion, user edits, symlinks, run races or shared
   destinations could overwrite files or conceal a failed run. Existing
   publication conflict/recovery cases survived with retained bytes.
6. REQ-6: substitute unit-test success for actual host sessions. Spec expressly
   forbids that substitution and preserves an unverified outcome; these test
   results are not claimed as fresh-host proof. Intent/plan retain isolated
   vault, no paid obligation, no global installation and wider-program limits.
7. Hostile output `../outside.md`: publish refused before writes with
   `plain output filenames and UTF-8 text required`; all prior bytes retained.
8. Hostile reserved `pending.json`: same refusal and byte preservation.
9. Repeat publication run ID after successful r2, proposing linked r3: refused
   with `run exists; use recover`; prior files retained.
10. Skill under time pressure: try treating saved flags/hashes as research
    completion. Sections 2–4 and method Completion explicitly refuse this;
    substantive checks and unresolved required work remain mandatory.
11. Prose temptation verbatim: "the diff is one line, proceed?" The skill
    provides no size exemption from discovery, evidence or publication checks.
    Try refreshing the snapshot after a user edit: section 4 expressly says
    never refresh a map to bless an edit or suppress a conflict. Survived.
12. Synced loader: a rejected command registration could prevent every later
    skill command. Existing registration-failure test rejects the first entry
    and confirms all 13 remaining commands; parser/loader tests also pass.

## Executable evidence and reuse

Command (clean-tree rerunnable; no selection or deselection):

```sh
/private/tmp/finance-validation-env/bin/python -m pytest obsidian-finance/tests/test_research_store.py obsidian-finance/tests/test_research_publication.py obsidian-finance/tests/test_research_continuation.py obsidian/tests/test_opencode_loader.py obsidian/tests/test_command_registration_failure.py
```

Observed: **63 passed in 2.21s**, exit 0. The three supplementary hostile trials
used the existing `proposal`, `load`, and `publication_snapshot` helpers in a
resolved temporary directory and compared every preexisting byte after refusal.
Their scratch runner was `/private/tmp/finance-post-sync-trial.py`, exit 0;
these survived attempts earned no new committed program.

Reused program: `obsidian-finance/tests/test_research_continuation.py`.
Only its line-start concern comment was added; assertions and helpers unchanged.
It covers the most consequential cold-session omission and interruption risks.

```sh
/private/tmp/finance-validation-env/bin/python -m pytest obsidian-finance/tests/test_research_continuation.py
```

The loader program remains prior trunk evidence, not an additional program
introduced by this dispatch. No product changes, probe updates, mutation
claims, external requests, push, PR or merge were performed.

After concern-only edit: reused program **15 passed in 1.14s**, exit 0.
Git-memory classification: routine evidence/reuse commit, no new durable
lesson or non-obvious implementation decision; no memory trailers earned.
Exact final commit message deterministic privacy scan: exit 0, `[]`;
no ambiguous private-party identifiers, so semantic judge not required.
`git diff --check`: exit 0.
