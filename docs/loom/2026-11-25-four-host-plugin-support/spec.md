# Four-host plugin support — spec
intent: 2026-11-25-four-host-plugin-support@74b5c0f
confirmed-behavior: 2026-11-25 @eaffa24
pre-build-review: required — changes a public invocation contract and adds a distribution target across hosts

## Requirements
REQ-1 — Consistent releases
  WHEN users inspect either package, the marketplace and platform package metadata shall agree on its release version and advertise the actual 15 Obsidian or 4 Finance skills, including Taiwan equity research and excluding File Intel → Acceptance #1

REQ-2 — Installation across hosts
  WHEN users follow the installation guide for Claude Code, Codex, Antigravity or OpenCode, both packages shall install and expose their complete skill inventories → Acceptance #2

REQ-3 — Native OpenCode selection
  WHEN users mention a registered OpenCode skill by its exact namespaced ID with @ or the model selects it with the native skill tool, OpenCode shall load the corresponding skill from its own package, with its supporting files available and no package-generated slash commands → Acceptance #3

REQ-4 — Accurate guidance and preserved data
  WHEN users install or update either package following its guide, the documented supported and verified behaviors shall match the observed results, the package test suite shall pass, and existing vault notes and settings shall be preserved → Acceptance #4

## Design decision
- Agent-decided: align the marketplace and all distribution metadata to Obsidian 5.0.0 and Finance 0.2.0 respectively; Obsidian retires a public OpenCode command surface and File Intel, while Finance adds Taiwan equity research and a new host entry.
- User-decided: retire the OpenCode custom slash commands, use native @ mentions and automatic model selection, retain exact existing Obsidian skill IDs and use a distinct Finance namespace.
- Agent-decided: retain the existing skill registration content contract and remove the command registration branch. Reuse its behavior in Finance with independently installable package contents; avoid a shared runtime dependency between the optional plugins.
- Agent-decided: test Antigravity's existing Claude-plugin conversion before adding any additional manifest; add native metadata only if necessary to satisfy the supported installation guide.
- Agent-decided: verify each supported host against isolated candidate packages and preserve the user's current installations and vault during development; report any verified installation or model-selection limitations.

## Alternatives considered
- Retain custom OpenCode slash commands alongside @ mentions — redundant user-facing entry points and additional prompt forwarding logic.
- Install Finance by manually copying its skills to an OpenCode skill directory — loses the documented independently updateable package.
- Publish a shared external loader package — adds an installation dependency for two small independent packages without a demonstrated need.

## Current state evidence
- Forward: `.claude-plugin/marketplace.json` already lists both packages; each has Claude and Codex manifests.
- Reverse: `obsidian/.opencode-plugin/index.js` exposes both skill and command transforms, while `obsidian/tests/test_opencode_loader.py` currently requires both.
- Error: `obsidian-finance/README.md` documents the absent OpenCode loader; Antigravity's local validator reports Claude conversion required for both packages.
- Data: `obsidian/skills/` has 15 skill definitions and `obsidian-finance/skills/` has 4 including `tw-equity-research`.
- Boundary: `PRINCIPLES.md` requires preservation of vault data and accurate capability claims; skill methods and note formats remain outside this change.

## UI flows
- Install either plugin in Claude Code or Codex → its skill inventory shows all 15 or 4 skills at the new release version.
- Install either plugin in Antigravity using the documented supported route → its plugin and skill inventory shows the corresponding full package.
- Install both OpenCode packages → the registry shows 19 skills under the two distinct plugin IDs.
- Enter `@obsidian:obsidian-research` or `@obsidian-finance:tw-equity-research` in OpenCode → the respective skill is selected using OpenCode's native mechanism.
- Ask for a matching task without naming a skill → OpenCode advertises the relevant skill to the model according to its normal discovery mechanics.
- Open OpenCode's slash-command menu → the two plugins' generated skill commands are absent; built-in and other plugins' commands remain.
- Follow the documented update route → new release contents are available, including Taiwan equity research, with the retired File Intel entry absent and existing vault files and settings preserved.
