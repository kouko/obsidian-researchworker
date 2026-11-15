# Shared vault instructions — acceptance test evidence

Tried on 2026-11-15, in a clean copy of the project at 1a5cb697700f81d47485b1c6072d30e356724651.

## Setup and method

An independent fresh reader inspected the current README, intent, spec and setup skill. A clean source archive was created with `git archive 1a5cb697700f81d47485b1c6072d30e356724651 -o /private/tmp/vault-acceptance-clean.tar`, then extracted with `mkdir -p /private/tmp/vault-acceptance-clean` and `tar -xf /private/tmp/vault-acceptance-clean.tar -C /private/tmp/vault-acceptance-clean`.

The README prescribes Python and pytest for repository checks, and explicitly does not claim host installation. With the existing project Python environment, ran from the clean root:

```sh
python3 -m pytest obsidian/tests/test_canvas_plugin_docs.py obsidian/tests/test_skill_inventory.py -q -p no:cacheprovider
```

Here `python3` denotes the existing environment's Python executable used for the run; its private absolute path is intentionally omitted. Captured result: `4 passed in 0.09s`. The full package suite was not run by this acceptance tester; finalize-review is responsible for the automated test suite, which runs before acceptance and blocks it on failure.

The shipped artifact is a prose skill, not an executable initializer. The fresh reader consumed its current steps, used synthetic profile and preview approval inputs, and executed the resulting filesystem operations with a temporary witness script. This script is test-operator scaffolding, not an added product implementation. Run: `python3 /private/tmp/vault-acceptance-operator.py`; synthetic files and captured assertions: `/private/tmp/vault-acceptance-synthetic/`, including `approved-preview.json` and `results.json`. No external model, network, host CLI invocation, actual app opening, global setting changes, ingestion, or live skill-trigger claim was involved. Actual private outcomes were independently inspected read-only; their detailed evidence remains outside this repository.

## 1. Personalized reusable rules

- Input: ecology student; field observations fall through the cracks; study and personal scope; no imported files; explicit `build it`; vault-only context.
- Preview listed seven role-appropriate folders, both instruction files, missing memory and three named local skills. Executed those creations in a fresh synthetic directory.
- Read back personalized background and structure, the complete naming/quality/current-routing policy, and exact `CLAUDE.md` bytes `@AGENTS.md\n` with a real final newline. No unresolved profile placeholders remained.
- Result: personalized shared body, approved ancillary paths, no owner-specific default.

## 2. Current skills and valid links

- Read generated policy and current skill inventory; focused documentation/inventory checks passed (command above).
- Generated instructions contained no note wikilinks; no nonexistent note targets were emitted. Policy requires real existing targets rather than numeric quotas and keeps ordinary wikilinks.
- Read-only private common-body check found the retired wiki/news routes and obsolete advertisements absent. Actual prerequisite text distinguishes Defuddle CLI, running Obsidian/CLI, and external file-processing script plus credentials; none of those integrations was executed or certified here.

## 3. Shared entry and host boundary

- New synthetic vault and updated private outcome both had a full `AGENTS.md` and exact one-line `CLAUDE.md` import, resolving to that common body.
- This is a file/import check only. Fresh Claude Code and Codex sessions, settings-dependent discovery and automatic skill triggering were not run. Acceptance is partly; the actual host-start flow is not verified.

## 4. Preserve and recover custom rules

- Synthetic existing vault started with distinct instruction bodies: one required field-station codes, the other preservation of quoted source language. Customized memory, a local skill and a historical note were also present.
- Recorded preview bytes, saved byte-identical originals with a restore mapping, checked current bytes before replacement, merged both unique requirements, then verified exact import. Customized memory/local skill and historical note stayed byte-identical.
- Re-entry reused correct common body/import, with no writes, duplicate policy or additional backups.
- Restored both synthetic instruction originals using the mapping only after checking current bytes; exact original bytes matched.
- Read actual private common body and both pre-update instruction snapshots independently. Valid naming, quality, mandatory skill use and personal requirements were retained, including the unique complete original-language transcript and linked plain-text delivery outcome. No private body or taxonomy is copied here.
- Independently checked original backup hashes and the two instruction backups against pre-update snapshots. All matched. Fourteen protected memory/local-skill files were unchanged between protected snapshots and live inspection.

## 5. Retired local entry and existing data

- Read-only inspection confirmed the retired daily-news command was absent from active discovery and present in its original hashed private backup, with a restore mapping and a warning to check later edits before restoration.
- Independently compared before/after protected manifests: 17,554 files; one difference, `.obsidian/workspace.json`. Every other protected snapshot entry matched, and independent live hashing found no additional protected mismatch.
- The cause of the concurrent workspace difference is unconfirmed. Inspected local application scripts do not write that path. This is not proof of causation or proof that every vault byte stayed unchanged. No restoration was attempted; legitimate concurrent work must be preserved.
- The synthetic historical note retained its original bytes and location. Actual historical notes were verified by hashes, not opened individually or through Obsidian.

## 6. Reproducibility and publication boundary

- Clean archive, focused pytest command, synthetic input/output paths and operator scope are recorded above. Private verification was independently recomputed; only necessary aggregate outcomes are public.
- Temporary operator/verification scripts, real vault bodies, detailed private evidence, original backups and restore paths are not included in this commit. There was no private-vault Git operation, publication, or global host change by this tester.
- Report/evidence privacy inspection checks exact final text and staged names before committing. The committed intent already names the originator; the report repeats its Acceptance lines verbatim without adding private identifying context.

## UI-1. New vault

Executed the confirmed synthetic preview and read back generated files. Folder/profile customization and explicitly approved ancillary creation worked. Obsidian opening and integration prerequisites remain unexecuted.

## UI-2. Empty answer or declined preview

Used an empty synthetic directory, supplied no approved build input, and verified it remained empty. The operator stopped before Step 3; no instruction replacement occurred.

## UI-3. Existing instructions

Executed the two-body merge with unique synthetic requirements, original backups, exact shared import and byte-identical ancillary checks, as recorded under 4.

## UI-4. Host entry

Not verified: no fresh Claude Code or Codex session was launched. Shared-file bytes and relative import alone cannot establish host discovery or skill triggering.

## UI-5. Current local vault

Independently read actual authorized output and original instruction snapshots, checked exact shared body/import, valid unique requirements and retired-route absence. No writes to the actual vault.

## UI-6. Existing output

Synthetic historical output stayed byte-identical. Actual protected snapshot/live hashes matched except the disclosed concurrent workspace state. No Obsidian open-note flow was executed, so this flow is partly verified.

## UI-7. Re-entry

Read back correct existing files and reused them without writes. Whole synthetic file-byte snapshot and backup count were identical before and after the second pass, including custom memory/local skills.

## UI-8. Backup, read or conflict failure

- Created a regular file at the synthetic backup-parent path and attempted to create a backup directory. Captured `NotADirectoryError: Not a directory`; original remained `ORIGINAL\n`.
- Created a directory at an instruction-file path and attempted reading it. Captured `IsADirectoryError: Is a directory`; the other original remained unchanged.
- Changed an instruction after recording preview bytes and separately created an instruction previously absent at preview. Both comparisons detected different current state and stopped before replacement, preserving later bytes.
- Supplied contradictory English-only and Japanese-only rules. Left both files untouched pending resolution; no success claim or automatic choice.
- These exercise the reader's execution of the prose stop rules, not a shipped program's automated exception handling. Partial-write recovery was not injected.

## UI-9. Restore

Executed a synthetic restore from the private-style mapping after verifying current bytes; both restored instruction byte sequences matched their originals. Actual private instruction and retired-entry backup hashes/mapping were inspected read-only; real originals were not restored over the accepted changes.

## UI-10. Delivery boundary

Public evidence includes synthetic behavior, commands and bounded aggregates only. Detailed private data remains local. This acceptance report cannot certify all hosts, current-session refresh or runtime loading. No important-or-higher dismissed finding was supplied for this completed change; no repair was made by the tester.
