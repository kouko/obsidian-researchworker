# Preparation observations (before baselines)

The confirmed intent/spec and reviewed plan already establish the need for a
dedicated research skill rather than expanding acquisition-only `sec-data`.
The minimal agreed layout is `finance-research/SKILL.md` plus
`references/research-method.md`: invocation/discovery/execution/publication in
the body, substantive method and evidence/completion rules in the reference.
This adds instructions and replaces repeated ad-hoc continuation prompts; it
does not remove an existing command or add a workflow engine. Existing package
conventions have no command wrappers, so none is added. Generic rules stay in
the skill, while local assumptions/applied method identities stay in the root.
Missing scope requires a focused question; already supplied scope is reused.
No further user interview or technical-plan approval is required by the
confirmed decisions. Evaluation uses the full path for this multi-step skill.

The system `python3` could not import pytest when running the original
`evidence/skill-eval/make_fixture.py` (now
`obsidian-finance/tests/fixtures/make_skill_fixture.py`).
No package was installed. The existing `/private/tmp/finance-validation-env/bin/python`
has pytest and successfully generated all three preparation fixtures. The
generator reuses existing test fixture helpers; it is not a product entry point.

An early discovery check revealed a real library defect before any trial:
create `test_research_store.sample(root)`, append `market` to the legacy
valuation question's `required_sources`, leave that source absent, and call
`discover(root, "latest", "2024-08-31T23:59:59+00:00")`. The result reports the
market gap but still lists valuation reusable. This was handed to the owning
implementer, not counted as a skill benefit. The final missing-work fixture
uses a distinct `market-scenarios` question to keep method trials focused.
All scored baselines wait for the helper repair and use the same helper tree
as their matched with-skill runs.

Preparation roots named `/private/tmp/finance-eval-*-baseline-1` are unscored;
they were generated before the final fixture adjustment. Scored roots use a
different prefix. The dispatch resolver was first called with `--help` (not
supported: it expects a stdin JSON packet), then corrected to its actual
`initial` event contract. These setup errors are not model trial failures.
The successful packet is recorded with the scored trial runs. It resolves
complex/unobservable-main with empty portable capabilities to inherited model
and effort, without an override or external provider call.
