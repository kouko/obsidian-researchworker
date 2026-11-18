# Obsidian identity and commands in OpenCode — spec
intent: 2026-11-15-opencode-obsidian-name@fe0f8f6
confirmed-behavior: 2026-11-15 @d24cccf
pre-build-review: required — changes externally visible plugin and skill identifiers and command behavior

## Requirements
REQ-1 — Obsidian identity
  WHEN the user views the installed plugin and its skills in OpenCode, the plugin shall be identified as `obsidian` and its skills by `obsidian:<skill>` → Acceptance #1

REQ-2 — Existing skills remain usable
  WHEN a new OpenCode session loads the plugin, the existing 14 skills shall remain available for their existing purposes → Acceptance #2

REQ-3 — Other distribution identities
  The source repository shall remain `obsidian-researchworker`, and Claude and Codex plugin identities shall remain unchanged → Acceptance #3

REQ-4 — Existing data
  The change shall preserve existing notes and plugin data → Acceptance #4

REQ-5 — Slash invocation
  WHEN the user opens the OpenCode slash command list, each currently shipped user-invocable Obsidian skill shall appear as `/obsidian:<skill>` and selecting it shall invoke the corresponding skill with the user's text → Acceptance #5

## Design decision
- agent-decided — Register commands for the 14 existing skills, which do not declare themselves unavailable to users; keep skill and command identifiers aligned.
- agent-decided — Leave repository identity and other hosts' manifests unchanged to preserve their existing installations.
- agent-decided — Preserve the existing vault and plugin data, and report the old OpenCode skill identifiers as changed rather than silently claiming compatibility.

## Alternatives considered
- Keep the existing identifiers and add commands only — declined because the user explicitly requested the `obsidian` identity.
- Rename the repository — declined because its name is a separate, already established identity.

## Current state evidence
- Forward: `obsidian/.opencode-plugin/index.js:209` exposes the current OpenCode plugin ID.
- Reverse: `obsidian/package.json:5` exports the OpenCode loader.
- Error: `obsidian/.opencode-plugin/index.js:263` logs failed skill registration.
- Data: `obsidian/.opencode-plugin/index.js:246` gives skill IDs the repository prefix.
- Boundary: `.claude-plugin/marketplace.json` and `obsidian/.codex-plugin/plugin.json` retain their existing identities.

## UI flows
- Open the Plugins list → the OpenCode plugin appears as `obsidian`.
- Type `/obsidian:` → the list offers the 14 existing user-invocable skills.
- Select `/obsidian:using-obsidian` and enter a task → OpenCode submits the task with the corresponding skill instructions.
- Enter `@obsidian` → the skills appear with `obsidian:` IDs.
- If the plugin fails to load → its commands are absent; OpenCode's existing error reporting and plugin controls remain in effect.
- Return to or close the list without choosing → no task is submitted and existing data stays unchanged.
