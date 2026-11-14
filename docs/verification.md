# W3-01 isolated Codex verification

Date: 2026-11-14. Source revision: `5df7f6ce3c34098ca9c45590ce943967a199409b`.
Host: actual Codex CLI `0.169.0`; no mocks used.

## Isolated installation — passed

Temporary `CODEX_HOME`: `/private/tmp/researchworker-w3-01.wpiw3q/codex-home`.
Temporary fixture vault: `/private/tmp/researchworker-w3-01.wpiw3q/vault`.

Both commands used that temporary home and `-c 'model_provider="openai"'`:

```sh
codex plugin marketplace add /Users/kouko/GitHub/obsidian-researchworker --json
codex plugin add obsidian@obsidian-researchworker --json
```

Both exited 0. Marketplace registration returned
`marketplaceName: obsidian-researchworker` and `alreadyAdded: false`.
Plugin installation returned `pluginId: obsidian@obsidian-researchworker`,
version `3.27.0`, and installed path
`/private/tmp/researchworker-w3-01.wpiw3q/codex-home/plugins/cache/obsidian-researchworker/obsidian/3.27.0`.
This verifies local-source installation only, not remote distribution or runtime use.

## Real model session and note creation — unmet

The initial attempt failed before execution because Codex rejects overriding the
reserved built-in `openai` provider. It provides no runtime evidence.

The corrected attempt selected the normal built-in OpenAI provider, requested
`gpt-5.4`, retained safeguards, and did not use `--ignore-rules` or override
`model_providers`. It requested a representative Markdown note in the fixture
vault containing properties, a heading, a wikilink, a callout and a task.
The host emitted repeated DNS failures:
`failed to lookup address information: nodename nor servname provided, or not known`.
It also reported unavailable model metadata and transport fallback. The retry
was stopped; no successful model response, skill execution or note creation was
observed. The fixture vault contained no note when inspected.

The user additionally confirmed that the isolated home is not logged in and
`OPENAI_API_KEY` is absent from the environment. Authentication is therefore
unavailable independently of DNS; no successful authentication was established.
No credentials were copied. No further connection or retry was attempted after
the instruction to stop.

Raw attempt output remains in
`/private/tmp/researchworker-w3-01.wpiw3q/host-run.{jsonl,stderr}` and
`/private/tmp/researchworker-w3-01.wpiw3q/host-retry.{jsonl,stderr}`.

## Existing test evidence

- Existing functional suite: **155 passed before removal of the three
  migration-only tests**, as recorded in the retained plan. This is not a full
  suite result for the post-cleanup tree.
- Focused retained Canvas checks: **4 passed after cleanup**, as reported by
  the user for this record; not rerun during W3-01.
- No permanent migration tests, verification programs or new tests were added.

## Scope and remaining limits

Installation writes were confined to the temporary Codex home. The actual user
vault and existing plugin installations were not used for host verification or
modified. No installation switch, rollback, other-vendor access or readiness
command was performed. No other hosts were verified.

W3-01 and Acceptance #2 remain unmet: successful isolated installation does not
establish a working model session or representative note creation. This record
does not claim overall completion, full acceptance, or compatibility on other
hosts.
