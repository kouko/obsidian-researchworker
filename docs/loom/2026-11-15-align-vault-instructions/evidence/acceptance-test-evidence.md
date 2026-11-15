# Shared vault instructions — acceptance test evidence

Tried on 2026-11-15, in a clean copy of the project at 3f8bb499ae6086d6b4b8353d253bef24c2eac27c.

## Earlier run on 2026-11-15, at 1a5cb697700f81d47485b1c6072d30e356724651

The following original evidence is retained unchanged through UI-10. Its host-loading and concurrent-workspace limitations remain historical evidence. The current re-run follows it below.

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

## Re-run on 2026-11-15, at 3f8bb499ae6086d6b4b8353d253bef24c2eac27c

Reviewed the confirmed revised spec/plan, unchanged six Acceptance lines, current acceptance contract/template and functional diff from the earlier report commit. The approved refinement changes generated instructions and the private common body, so all six criteria and all ten UI rows were revisited; no earlier success was silently carried forward.

Created a new clean archive:

```sh
git archive 3f8bb499ae6086d6b4b8353d253bef24c2eac27c -o /private/tmp/vault-acceptance-r2.tar
mkdir -p /private/tmp/vault-acceptance-r2-clean
tar -xf /private/tmp/vault-acceptance-r2.tar -C /private/tmp/vault-acceptance-r2-clean
```

Followed README's existing-Python/pytest prerequisites and read the current skill from the clean archive. Repeated only the same focused command from the clean repository root, using the existing environment's Python:

```sh
python3 -m pytest obsidian/tests/test_canvas_plugin_docs.py obsidian/tests/test_skill_inventory.py -q -p no:cacheprovider
```

Captured `4 passed in 0.09s`. The full suite was not run by this tester; finalize-review will run the automated test suite before acceptance and block acceptance on failure.

Ran `python3 /private/tmp/vault-acceptance-r2-operator.py`; new synthetic files, approved preview and captured assertions are at `/private/tmp/vault-acceptance-r2-synthetic/`. This is independent reader-operated filesystem evidence, not an autonomous host benchmark or a shipped executable initializer.

### 1. Re-tested — compact personalized output and contextual boundaries

- Used the same synthetic ecology-student profile, first-person owner voice, study/personal scope, explicit `build it`, listed folders/ancillary files and vault-only context. Created and read back the actual files in a new directory.
- Extracted current generated body measured four sections, 29 lines, 1,738 characters before personalization, versus the earlier 56-line, 3,328-character body. It preserves owner context, scoped naming, existing-target links, source verification and mandatory skill use without a full catalog or duplicated syntax/dependency/host manual.
- Executed an evergreen note edit after reading current `obsidian-markdown` and the synthetic relevant note. No daily read or inbox prompt was selected.
- For an explicit recent-personal-voice request, read the relevant synthetic daily note. For explicit daily/inbox organization, read `obsidian-daily`, the daily note and list the inbox, then recorded the sorting question. The ordinary daily workflow remains available.
- These selected reads demonstrate how a fresh reader can follow the rule; they do not prove models in every host will independently choose the same behavior.

### 2. Re-tested — required skills and current capabilities

- Actually read matching authoring guidance for the note edit; read `using-obsidian` for an ambiguous vault request. Read file-intel prerequisites for an unavailable-processing scenario and explicitly recorded the missing external script/credentials; performed no substitute processing.
- Current body says to read and follow matching installed skills before execution, use the router when unclear, follow authoring metadata/writing/visual guidance, and disclose missing skills/prerequisites. No nonexistent note link was generated.
- Focused inventory/documentation tests passed. Read the final private body and checked obsolete wiki/news/stale routes remained absent. Prerequisite and host execution claims remain bounded, as in the earlier run.

### 3. Re-tested — shared file entry

- New synthetic common body resolved from exact `@AGENTS.md\n` bytes. Actual private wrapper remains byte-identical to the pre-refinement wrapper and has the same exact bytes.
- Result remains partly: no fresh Claude Code or Codex session or automatic-trigger experiment was run. The UI host-entry row remains not verified.

### 4. Re-tested — preservation, backups and restoration

- Re-executed two-source synthetic merge, both unique requirements, exact originals, restore mapping, preserved custom memory/local skill/historical bytes, no-write re-entry and exact synthetic restore.
- Independently read the actual final private common body, both original pre-first-update backup bodies, and the pre-refinement body. This comparison was not limited to the new draft or its self-reported audit.
- Actual private body reduced from 270 to 151 lines. Personal folder/work sections, naming, source protection and full video-delivery section were byte-identical to pre-refinement content; personal diagram subsections also matched. Original pre-first-update naming and unique original-language plain-text transcript/link/URL/incomplete-delivery requirements remain satisfied.
- Specifically verified final explicit non-Markdown extension-link handling and bounded ASCII restrictions. The private operation history records an intermediate omission of these two obligations, detected and restored before this acceptance run; the final file contains both. No unfixed omission was found.
- New backup exactly matches pre-refinement common-body bytes. Old instruction and retired-entry backup hashes remain valid; wrapper was unchanged, with no unnecessary replacement.

### 5. Re-tested — protected content and retired entry

- Independently confirmed retired active shortcut remained absent and its original backup remains valid.
- Compared complete before/after protected path sets and entries, then independently rebuilt the live protected manifest, excluding only the two approved instruction targets and the new backup directory as in the recorded scope. All 17,560 protected paths matched; zero path-set, content/symlink or modification-time differences. Old backups, memory, local skills, notes and settings are included in this protected scope.
- This is the refinement window only. The earlier 17,554-file window had one unexplained workspace-state difference; that limitation is retained and was not reclassified or restored. Acceptance remains partly across the overall change. No actual vault writes were performed by this tester.
- Verification-witness history: two initial assertions failed because the new manifest values contain `sha256` and `mtime_ns`, whereas the witness compared the whole object with a hash string. Stopped that comparison, inspected schema and corrected the witness lookup. A separate full-scope verifier then checked complete paths, hashes/symlinks and timestamps with no reduced coverage. These were witness errors, not demonstrated vault changes; their history remains in private local evidence.

### 6. Re-tested — reproducibility and private delivery

- Current clean archive, focused tests, reader inputs and actual synthetic results are recorded above. Private semantic and full-manifest verification were independently performed read-only; detailed bodies, backups, paths and identifying taxonomy remain outside the repository.
- Public publication files contain only reusable synthetic examples, known public project identifiers and bounded aggregate findings. Exact publication files and commit text receive deterministic privacy scans; no private-party ambiguity is added.

### UI-1. Re-tested — new vault

Created approved folders and missing named ancillary files with compact personalized common body and exact wrapper. Did not open Obsidian or alter globals.

### UI-2. Re-tested — empty answer or decline

Stopped before building without approval; actual synthetic directory remained empty.

### UI-3. Re-tested — existing instructions

Performed the full distinct-body merge/backup/preservation scenario again using current body, including customized memory/local skill bytes.

### UI-4. Re-tested boundary — host entry

Rechecked current file resolution and exact wrapper; runtime part remains not verified because no new host session was launched. The approved removal of duplicate host explanation does not add runtime evidence.

### UI-5. Re-tested — current local vault

Read final actual instructions against original and pre-refinement baselines, checked mandatory skill use, scoped daily/inbox context and unique personal obligations; retired route remains absent. Intermediate omission and restoration are disclosed under 4.

### UI-6. Re-tested — existing output

Synthetic historical note unchanged. Complete protected manifest, live paths, content and timestamps match for the current window. UI remains partly: no app-based note opening was executed, and the earlier concurrency limitation remains.

### UI-7. Re-tested — re-entry

Reused correct common body/import with no writes; all synthetic file bytes and backup count unchanged, including memory/local skills.

### UI-8. Re-tested — failure, concurrency and conflict

Actual backup-parent obstruction produced `NotADirectoryError: Not a directory`; instruction-directory read produced `IsADirectoryError: Is a directory`. Both preserved original bytes. Changed-file and newly-appeared-file preview comparisons stopped without replacement. Contradictory language requirements stayed untouched pending resolution. No completion claim or partial-write recovery injection.

### UI-9. Re-tested — restore

Checked current synthetic bytes, restored both instruction originals via mapping and compared exact bytes. Inspected new/old actual private backups and restore notices without restoring the real vault.

### UI-10. Re-tested — delivery boundary

Only the report and sanitized evidence are committed by this tester. Earlier dated partial outcomes and concurrency limitation remain above; new full-scope equality is restricted to its own window. Fresh host loading, autonomous skill triggering, app opening and external prerequisite execution remain unverified. No important-or-higher dismissed finding was supplied, and the tester made no product or private-vault repair.
