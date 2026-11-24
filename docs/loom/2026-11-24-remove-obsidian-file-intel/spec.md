# Retire Obsidian File Intel — spec
intent: 2026-11-24-remove-obsidian-file-intel@4bff87f
confirmed-behavior: 2026-11-24 @ca8196c
pre-build-review: not-required — removal of one optional entry point with no vault data changes or replacement workflow

## Requirements
REQ-1 — Remove the public entry point
  WHEN users browse the updated plugin, consult its current guides, or finish vault setup, the plugin shall no longer offer or recommend File Intel → Acceptance #1

REQ-2 — Preserve the other skills
  WHEN the updated packages are checked, their suites shall pass and the remaining skills shall still be available → Acceptance #2

REQ-3 — Preserve vault data and provenance
  WHEN the plugin is updated, the change shall leave existing vault files and settings intact and preserve attribution to earlyaidopters/second-brain → Acceptance #3

## Design decision
Remove the packaged skill and active references. Retain historical attribution and keep vault setup's remaining behavior. Agent-decided because setup only recommends the skill in its post-setup guidance.

## Alternatives considered
- Retain the entry point as a general-purpose batch summarizer. This would retain a public workflow outside the confirmed scope.

## Current state evidence
- Forward: `obsidian/skills/obsidian-file-intel/SKILL.md` invokes an external vault script.
- Reverse: `obsidian/skills/using-obsidian/SKILL.md` and `obsidian/skills/obsidian-vault-setup/SKILL.md` recommend the skill.
- Error: `obsidian/README.md` documents the missing bundled script and its prerequisite.
- Data: The script and its outputs are external to the package.
- Boundary: `ATTRIBUTION.md` records the transfer through Monkey Skills, and the dotfiles import records the original upstream.

## UI flows
Open the updated skill list → File Intel is absent.
Complete vault setup → The usual setup output appears without the File Intel recommendation.
