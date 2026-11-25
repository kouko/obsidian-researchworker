# Four-host candidate installation and baseline checks

Date: 2026-11-25. Candidate: `19d47ca`. Main baseline: `f139638`.

## Host installation

Tests used disposable configurations under `/private/tmp/rw-four-host-verify` and source paths of the candidate working tree. User installations and vaults were outside the test.

| Host | Tool version | Local installation | Obsidian | Finance |
|---|---|---|---|---|
| Claude Code | 2.1.332 | Local marketplace registration and user-scope install in isolated CLAUDE_CONFIG_DIR | 5.0.0, 15 skills | 0.2.0, 4 skills |
| Codex | 0.172.0 | Local marketplace and plugin add in isolated Codex home | 5.0.0, 15 skills | 0.2.0, 4 skills |
| Antigravity CLI | 1.5.16 | Claude plugin conversion from each package directory in a disposable home | 5.0.0, 15 skills, 1 agent, 1 hook | 0.2.0, 4 skills |
| OpenCode | 2.4.1 | Local absolute package directories in isolated configuration and localhost server | Active, 15 namespaced skills | Active, 4 namespaced skills |

Claude, Codex and Antigravity installed all 117 tracked Obsidian skill/script files and 52 tracked Finance skill/script files byte-for-byte. OpenCode's warmed registry reported 19 package skills and zero package-generated commands. The TUI offered both `@obsidian:obsidian-research` and `@obsidian-finance:tw-equity-research` as skills; Tab completed each exact ID. No prompt was submitted. All registrations included a description and did not disable automatic invocation.

Actual model-backed automatic selection and execution are unverified. Automatic approval review rejected the native session-prompt probe because of possible model-service egress. A separate read-only experimental skill-file API request returned 404 in the installed version. The registry and TUI observations are independent of that probe; no successful model execution or remote Git install is claimed.

## Package tests

- Test first: native loader regression tests failed six cases before changes; all eight passed after changes.
- Release metadata test failed on the old version and passed after version synchronization.
- Focused suite: `python3 -m pytest obsidian/tests/test_opencode_loader.py obsidian/tests/test_command_registration_failure.py obsidian/tests/test_vault_search.py -q -p no:cacheprovider` — 51 passed.
- Full candidate suite: `python3 -m pytest obsidian/tests obsidian-finance/tests -q -p no:cacheprovider` — 577 passed, 6 failed.
- Baseline archive: `git archive f139638` extracted into a disposable directory; running the two affected Finance test modules produced exactly the same six failures (97 passed). No candidate change touches the research implementation or these tests.

Baseline failures:

- `test_research_continuation.py::test_public_pilot_adjacent_quarters_and_competition_cutoffs[markdown]`
- `test_research_markdown_templates.py::test_generated_overview_exposes_changes_and_gaps_before_record`
- All four parameterizations of `test_research_markdown_templates.py::test_portable_source_context_retains_public_links_on_recapture` (missing `registration_context`).

The prior main commit `f139638` (PR #28) removed `registration_context` and other source-context/rendering behavior from `obsidian-finance/scripts/research_markdown.py`. The current package support change leaves these research methods untouched. The full suite remains blocked by the baseline failures. Closing review and publication have not completed.

## Independent adversarial check

The independent adversary found no candidate-specific issues: both package loaders are identical, standalone and native-skill-only; actual frontmatter descriptions agreed with PyYAML. Existing tests cover package inventories, body and path registration, failure isolation and absence of command registration. No additional adversarial program was warranted.
