# Shared vault instructions and safe initialization — spec
intent: 2026-11-15-align-vault-instructions@a87ecbd6c765539bd375eb6816a0e2532ab4b9fb
confirmed-behavior: 2026-11-15 @c7a1f8a
pre-build-review: required — public generated-instruction contract, cross-host loading, private local edits and preservation of existing user rules

## Requirements

REQ-1 — Reusable initialization rules
  WHEN a user confirms the existing setup preview, the initializer shall produce role-personalized vault instructions containing scoped naming and source-quality rules, existing-target links without quotas, and mandatory relevant-skill use; detailed properties, visuals and task routing shall remain owned by the existing authoring and routing skills without hard-coding the owner's identity or private folder taxonomy → Acceptance #1

REQ-2 — Current capability and quality guidance
  The shared instructions shall use the current plugin's skill identifiers, preserve ordinary wikilinks, omit retired wiki/news workflows and stale skill names, and require relevant existing-note links without a numeric link quota or placeholder links → Acceptance #2

REQ-3 — One shared body with two host entry points
  The initializer and local vault update shall put the complete common instructions in AGENTS.md and make CLAUDE.md contain the native relative import @AGENTS.md, with host loading evidence and any unverified version or setting clearly identified → Acceptance #3

REQ-4 — Preserve and recover existing customization
  WHEN either instruction file already exists, the update shall preserve still-valid naming, quality, skill-use and personal requirements from their current contents, retain restorable original copies before replacement, leave existing memory and local skill files unchanged, and avoid silently resetting uncommitted edits or replacing existing content with a generic new-vault profile → Acceptance #4

REQ-5 — Retire instructions and obsolete local entry points without deleting notes
  The local vault update shall remove retired wiki/news routing and stale or unavailable command advertisements, retire the confirmed obsolete daily-news shortcut with a restorable original, and leave existing notes, wiki/news/story content, legacy data settings and unrelated files unchanged → Acceptance #5

REQ-6 — Reproducible checks with private local evidence
  The change shall provide representative new-vault and existing-vault verification, while committing only reusable templates and necessary generic checks, keeping the actual local instruction bodies, backups and private evidence outside the plugin repository and remote publication → Acceptance #6

## Design decision

- user-decided — Keep the complete common rules in AGENTS.md and use exactly `@AGENTS.md` plus a trailing newline as the CLAUDE.md compatibility entry; the user explicitly confirmed the native import syntax and proposed scope.
- agent-decided — Keep one rule body rather than two generated full copies or a synchronization program; the inspected local documents already disagree on link requirements, routing and personal workflows.
- user-decided — After inspecting the generated body, kouko approved the combined simplification with "OK": keep personal context, folder/work preferences, naming/quality and skill-use obligations; remove the duplicated full skill directory and syntax/dependency/host-loading explanations from the generated body. Relevant skills retain ownership of metadata, callouts, embeds and diagrams. Require reading and following matching installed skills, use using-obsidian when routing is unclear, and report unavailable skills rather than silently substituting.
- user-decided — Scope contextual reading to the task: read recent daily notes only when personal voice or recent work context is relevant, and ask about inbox organization only during daily organization or an explicit organizing request. Use the owner's first-person perspective for confirmed personal facts, without a Claude-specific narrator.
- agent-decided — Date prefixes apply to time-sensitive and historical-comparison notes, preserving the owner's existing scope rather than imposing dated filenames on every note. Keep note-type fields appropriate to the content; related_notes and links must resolve to actual notes.
- agent-decided — Preserve current role/scope inference and preview confirmation. Do not bundle a redesign of role-specific commands, ingestion, or global context loading; distinguish any host-specific shortcuts from portable plugin skills and do not present absent local shortcuts as installed.
- agent-decided — Bound all ancillary setup writes as well as the two instruction files: an instruction update or re-entry never rewrites existing memory.md or existing local skill files. Create missing ancillary files only when the setup preview explicitly lists the creations and the user confirms that preview. The local instruction cleanup creates none of these ancillary files and does not invoke the setup's application-opening or global-context branches. Verify with an existing-vault fixture containing customized memory and local skill content, asserting their bytes remain unchanged.
- agent-decided — For the local update, merge still-valid unique requirements from both actual instruction files, including existing video-summary and original-transcript delivery expectations. Assess legacy tool references against actual availability; never substitute invented transcripts or promise unavailable integrations.
- user-decided — Existing content and uncommitted customization are preserved, as pinned by intent Constraints and PRINCIPLES.md non-negotiable 1. Before replacement, save byte-identical originals under `.agent-instruction-backups/<unique timestamp>/` inside the target vault; store any retired shortcut there outside active command discovery. Keep backups private and retain their restore mapping.
- agent-decided — Read both files and recheck their observed bytes before applying edits. On unreadable files, backup failure, a concurrent change or an unresolved conflict, preserve the originals, identify the affected file and resume only after the condition is resolved. Do not advertise successful completion after a partial write.
- agent-decided — Verify and reuse an existing correct import on re-entry, merge existing common instructions and take a fresh backup only for files that actually need changing. Do not append duplicate policies or repeatedly archive an already retired shortcut.
- agent-decided — Do not delete or rewrite legacy wiki/news note directories or their data configuration. Removing active guidance does not remove historical user output. The obsolete shortcut's backup permits an explicit later restore without restoring retired claims into the common rules.
- agent-decided — Keep private before/after files, hashes and restore instructions local. Public tests use synthetic personas, folders and conflicting-rule fixtures. Local vault edits receive no Git commit or push as part of this plugin delivery.
- agent-decided — Documentation establishes compatibility strategy, not observed host execution: Codex discovers AGENTS.md; Claude supports @ imports, including configurations that do not directly load AGENTS.md. Never claim that every host version, policy or active session has loaded the new body.

## Alternatives considered

- Keep the reviewed 56-line body unchanged: viable but retains a duplicated 14-skill directory and broad daily/inbox triggers. Removing only the directory is smaller work but leaves those triggers. The user approved combining both reductions while preserving substantive quality and skill-use obligations.

- AGENTS.md alone: smaller, but Claude's direct discovery depends on version, built-in support, settings and ancestor/local instruction files; the confirmed one-line import avoids that narrower compatibility boundary without another rule body.
- CLAUDE.md alone: does not provide Codex's default project instruction entry; adding a global fallback setting would exceed the confirmed scope.
- Two complete hand-maintained files or generated copies: preserves the demonstrated drift risk and adds synchronization ownership; rejected in favor of the native import.
- Copy the actual owner's complete vault instructions into the plugin: rejected because private details are not generic initialization defaults.
- Replace both existing files with a fresh generic profile: rejected because unique personal and uncommitted requirements would be lost.
- Rewrite all setup features or build a migration framework: rejected; update the instruction contract and the specifically authorized local files without new synchronization or integration machinery.

## Current state evidence

- Forward: `obsidian/skills/obsidian-vault-setup/SKILL.md`, STEP 1 and STEP 2, asks about the owner and previews a role-based vault before creation.
- Reverse: `obsidian/skills/using-obsidian/SKILL.md`, Available Skills and Quick Start, advertises the setup skill as the vault configurator.
- Error: `obsidian/skills/obsidian-vault-setup/SKILL.md`, Write CLAUDE.md, says to write directly to an existing pathname without specifying merge, backup or conflict behavior.
- Data: `obsidian/skills/obsidian-vault-setup/SKILL.md`, generated markdown block, contains Who I Am, My Vault Structure, How I Work and Context Rules; the quality/routing policy is not part of that initial block.
- Boundary: `PRINCIPLES.md`, Non-negotiables 1–3, protects existing data, current capability claims and bounded changes. The actual local instruction and shortcut snapshots are private inputs, not publication artifacts.

Relevant primary loading contracts, inspected 2026-11-15: [Codex instruction discovery](https://developers.openai.com/codex/guides/agents-md) and [Claude shared-file imports](https://code.claude.com/docs/en/memory#share-one-file-with-other-coding-tools). Host settings that suppress project instructions remain outside this change's control.

## UI flows

Complete the existing setup preview and confirm creation → receive personalized common vault rules and the two compatible instruction entry files.

| Case | What the user does | What they see or what changes |
|---|---|---|
| New vault | Describes work and needs, reads the existing preview and confirms it | Personalized background and folders plus reusable naming, note-quality and available-skill rules; any additional new memory or local skill files are listed before creation. The actual generated files and verification limits are reported. |
| Empty answer or declined preview | Has not provided the requested profile, or declines creation | The setup continues its existing conversation or stops; no instruction files are replaced before confirmation. |
| Existing instructions | Runs setup where either common or Claude instructions already exist | Existing custom rules are read and reconciled; originals are backed up before changes. A fresh generic profile does not replace the existing personal context. Existing memory and local skill files remain byte-identical; missing ancillary files are created only if shown in the confirmed preview. |
| Host entry | Starts a supported fresh Claude Code or Codex session in the updated vault | Both instruction entries lead to the same complete common rules; host-specific shortcuts and unverified loading conditions are clearly distinguished. |
| Current local vault | Applies this confirmed cleanup | Existing naming, quality, valid personal rules and video-delivery expectations remain; obsolete wiki/news routing, obsolete skill names and the retired daily-news shortcut no longer appear as active instructions. |
| Existing output | Opens an old wiki page, news digest, story note or other existing note | Its content and location remain unchanged; no note migration is performed. |
| Re-entry | Runs setup or the same local cleanup again | Existing compatible files are reused; valid custom content remains and common policies are not duplicated. Existing memory and local skill files are not reset or rewritten. |
| Backup, read or conflict failure | A required original cannot be read, backed up safely or reconciled with concurrent changes | The affected file and original tool error are reported, completion is not claimed, and existing content is preserved; retry begins by rereading current files after the condition is resolved. |
| Restore | Needs the pre-update instruction files or retired shortcut back | Private byte-identical originals and the recorded restore mapping are available; later user edits must be checked before restoring anything over them. |
| Delivery boundary | Receives the plugin PR and local change summary | The PR contains generic templates and checks; actual personal instructions and backups remain local. Tests describe what was executed rather than claiming all host sessions were refreshed. |

In-progress behavior uses the host's existing tool/task feedback; no new progress interface, CLI command or exit-code contract is added. Native tool errors retain their actual wording. No automatic change to global Claude/Codex settings or installed plugin caches is performed by this change.

## Confirmed refinement and evidence continuity

On 2026-11-15, after the planning-only request and continuation, the user replied "OK" to the displayed combined simplification, including task-scoped context reads, removal of duplicated manuals/catalogs, mandatory skill use and separately preserved local requirements. The six intent Acceptance lines, shared-file strategy, privacy, backup and data-preservation guarantees remain unchanged. This is a continuation of the same change, not a new task or review-budget reset: the first completed review digest remains Round 1, and the refined functional content will be Round 2. Existing suite/inventory evidence remains relevant to unchanged distribution; old acceptance and attestation describe the earlier content and must be replaced for changed outputs and contextual behavior. No implementation-task failure or retry counter is reset. The prior workspace-state concurrency limitation remains retained evidence, not a failed task reclassified as success.
