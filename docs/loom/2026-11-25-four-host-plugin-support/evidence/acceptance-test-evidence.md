# Four-host acceptance test evidence

Tried on 2026-11-25, in a clean copy of the project at 16b389b.

The first run was at 8780ae8; sections 1–4 and F1–F7 record that run. The dated rerun at the end records the corrected local update guide.

## 1. Consistent release metadata and inventories

- How I tried it: `python3 -m pytest obsidian/tests/test_opencode_loader.py obsidian/tests/test_command_registration_failure.py obsidian/tests/test_vault_search.py -q -p no:cacheprovider`.
- What came back: 51 passed in 9.65s. Both version and inventory assertions passed; independent installs showed 15 Obsidian and 4 Finance skill files, including `tw-equity-research` and excluding `obsidian-file-intel`.

## 2. Installation and inventories across hosts

- How I tried it: in disposable profiles under `/private/tmp/rw-acceptance-independent-d0nsp2ts`, used local `claude plugin marketplace add` and `plugin install`, `codex plugin marketplace add` and `plugin add`, and `agy plugin install <package directory>`. No global configuration was used. Compared all files under source skills and scripts directories with each installed path.
- What came back: all six installations succeeded. Each host showed 15 and 4 skill files. All 117 Obsidian and 52 Finance skill/script files were present and byte-identical.
- Closing-review orchestrator's isolated OpenCode runtime recheck of the same commit observed both plugins active, 19 exact namespaced skills, and zero package commands (exit 0 after fixing the temporary probe's missing import). This is the actual host inventory evidence.

## 3. Native OpenCode selection and commands

- How I tried it: focused native registry tests above and orchestrator real host check. Prior-candidate TUI evidence: typing each namespaced prefix and pressing Tab completed the exact respective ID. The loader and metadata were unchanged by rebase.
- What came back: tests passed, actual registry contained 19 skills with descriptions and no autoinvoke override, and zero package-generated commands. Actual model invocation unverified; automatic approval review previously rejected session-prompt test because it could send contents externally. No model prompts or external model calls were attempted.

## 4. Guide accuracy, tests and preserved data

- How I tried it: followed the documented local install and update routes in a disposable profile and source archive, starting at 9f6aba7 then staging files from 8780ae8. The focused automated tests passed. The full package suite command `python3 -m pytest obsidian/tests obsidian-finance/tests -q -p no:cacheprovider` is executed by finalization and blocks attestation on failure. Build had 588 passed already on f18667b before the evidence-only update.
- What came back: all six fresh local installations passed. Local Codex `plugin marketplace upgrade obsidian-researchworker --json` failed with `marketplace ... is not configured as a Git marketplace`; the subsequent `plugin add <id>@obsidian-researchworker --json` succeeded for both plugins at 5.0.0 and 0.2.0. Claude documented marketplace update and per-plugin update both succeeded; AGY reinstall replaced both isolated packages. No vault or global configuration accessed. Remote OpenCode Git update and model-backed skill execution unverified.

## F1. Claude and Codex fresh installs

- Evidence: see #2. Exit 0 for all four fresh installs and exact inventories. The package versions match metadata.

## F2. Antigravity fresh installs

- Evidence: see #2. Exit 0, both 15/4 skill inventories verified byte-identical.

## F3. OpenCode fresh load

- Evidence: see #2. Orchestrator runtime record rechecked the candidate in an isolated source snapshot, using `skill.list` and `plugin.list`. Both active, 19 total.

## F4. Native mention selection

- Evidence: prior-candidate actual TUI completed both exact namespaced skill IDs with Tab. The native loader remains byte-identical after rebase. No model prompt was submitted.

## F5. Automatic model selection

- Evidence: native skill registry descriptions and no autoinvoke overrides; no model request was made, following prior approval rejection. No actual model selection observed.

## F6. Slash-command registry

- Evidence: orchestrator `command.list` in warmed isolated runtime returned four commands, zero under these package IDs. The focused test independently asserted no command API is invoked by either loader.

## F7. Update procedure

- How I tried it: installed both prior packages from a local source snapshot of 9f6aba7 in disposable host configurations at `/private/tmp/rw-acceptance-update-vp2qld8w`, then staged the candidate 8780ae8. Used documented commands without remote calls.
- What came back: Codex local marketplace upgrade exits 1 as described in #4. Re-running `codex plugin add obsidian@obsidian-researchworker --json` and `codex plugin add obsidian-finance@obsidian-researchworker --json` each exits 0 with installedPath ending in 5.0.0 and 0.2.0. Claude `plugin marketplace update obsidian-researchworker` and `plugin update <id>@obsidian-researchworker --scope user --json` each succeeded, update messages show old/new versions. AGY reinstall printed `replaced existing installation` and full 15/4 inventories. OpenCode remote-update route not exercised.

## Rerun on 2026-11-25 at 16b389b

- Fix range 8780ae8..16b389b modifies only docs/migration.md: local Codex update now repeats plugin add; Git marketplace refresh is documented separately. It also records the successful local upgrade tests.
- Rows 1, 4 and F7 rerun in fresh disposable profiles under `/private/tmp/rw-acceptance-retest-_5meokvi`. Installed from a local source snapshot of 9f6aba7, staged the candidate 16b389b, then used the corrected documented local commands with no model or remote calls. Codex repeated each plugin add and list: both installed, enabled, at 5.0.0 and 0.2.0. Claude marketplace update + per-plugin update explicitly advanced both prior versions. AGY reinstall printed replaced existing installation. Each of the six updated installations had exact 15/4 inventories and zero missing or changed files under skills and scripts. Focused automated tests rerun: 51 passed in 3.66s.
- Rows 2, F1 and F2 carried over: initial installation instructions and package contents unchanged. Rows 3, F3, F4, F5 and F6 carried over: OpenCode instructions, loader, metadata and skill content unchanged. Remote Git updates, model execution and global refresh remain unverified as disclosed in the guide.
- Closing-review orchestrator separately reran the complete package suite at 16b389b, reporting 588 passed in 57.65s. Finalization still executes its own suite check.
