# Trial invocation and reproducibility

All nine no-skill runs completed before `skill-v1.json` was drafted. Then the
matched nine with-skill runs used that exact snapshot. Native agents were fresh
contexts (`fork_turns: none`), sequential, with inherited model/effort. Native
task names are `baseline_{case}_{n}` and `skill_{case}_{n}`; artifact run names
are `{case}-baseline-{n}` and `{case}-skill-{n}`.
No external CLI, network, installation, private data or paid provider call was
used. Native completion notifications did not expose token/duration fields;
those metrics are null, not estimated or reported as zero cost.

Frozen helper revision: `56d276a15bfaf44b949d90612c0f0dfa9d80a6b3`.
SHA256 values used in both configurations:

- research_store.py: `d84d675b02381bce91d60ff407f62c34a6c2a68f50190ea5670f5eab69f43898`
- work_assessment.py: `caa2ca6e4b15308110e0e7ae7b1ef59386f5d9c210da2a3a3577f4d99e07aaae`
- assess_work.py: `cfe0948609ebb6c1c687ed37f64a0ae2b750af8e00df2f879e91cace9c1d8653`
- evaluated README.md: `c43ddc434e2bf21a1373c45162ae3979677980746b7d1309b627a22a70095d74`
- v1 SKILL.md: `603d9f952fccca7e8e803d723883903833cc1d0011f80c3cec3f9d1c03c154dc`
- v1 research-method.md: `4693d6bdc2dc5c08f90652495d9b75c979cd0f3f3b143bf1e1f3d0e576e24163`

Before every dispatch the installed Loom `dispatch_profile.py` received:

```json
{"event":"initial","main_profile":{"model":null,"effort":null},"task_evidence":{"trust_boundary":true},"capabilities":{},"inheritance_guaranteed":true,"completed_redispatches":0}
```

Observed result: complex task, `unobservable-main-profile`, `overrides: null`,
`effective_profile: inherited`, outcome dispatch. Exact host model ID was not
returned; no model/provider substitution was requested.

Recreate a root from the repository with an existing pytest environment:

```sh
/private/tmp/finance-validation-env/bin/python \
  obsidian-finance/tests/fixtures/make_skill_fixture.py \
  missing /private/tmp/new-isolated-finance-root
```

The other fixture names are `noop` and `conflict`; destination must not already
exist. The named environment is local test infrastructure, not a package runtime
dependency. Prompts/assertions are retained verbatim in each `eval_metadata.json`
and readable in `cases.md`. Each case has three independent run roots per
configuration under `/private/tmp/finance-skill-trials/`. Programmatic initial/
final SHA256 comparisons, created output contents and operator commands/errors
are retained in the run JSON artifacts. Original fixture bytes are reproducible
from the generator and frozen test helpers. Journals remain in the isolated
roots; selected attempt identities/field values and hashes preserve failed-run
evidence without treating a later target file as that run's completion.

Each trial packet supplied the same task from its metadata, ROOT/RESULT paths,
the same README/helper access and local shell tools. It prohibited other repo
docs/skills/eval cases, network, installs, external services, questions, agents
and writes outside ROOT/RESULT. It requested `result.md` and `commands.md`,
apply_patch edits, read-before-edit, stopping after a twice-blocked guard, and
a final response of at most eight lines. The with-skill packet additionally
made the skill/reference available and requested reading/applying them. ROOT
and RESULT are the only task substitutions; no expected assertions were given
to the executor. The author graded retained behavior inline, not as an
independent closing reviewer.

## Fixture placement follow-up 1

The executable benchmark helper was moved from this reserved evidence store to
`obsidian-finance/tests/fixtures/make_skill_fixture.py`; only its repository-root
lookup changed (`parents[5]` to `parents[3]`). It remains a real fixture CLI,
not a probe. Original preparation failures and trial outputs were preserved.
At repository revision `d2dd22b`, the existing interpreter generated fresh
`missing`, `noop` and `conflict` roots before and after the move: all six
commands exited 0. Relative file sets matched, and direct byte comparisons
matched every file: 11 missing-case files, 8 no-op files and 10 conflict files
(29 total). This verifies placement equivalence, not a new behavioral trial or
final package/adversarial acceptance.

Full commands, stdout/stderr, before hashes and per-file byte-comparison results
remain outside the evidence store at
`/private/tmp/finance-fixture-placement-zbmc7cxj/equivalence-proof.json`.
