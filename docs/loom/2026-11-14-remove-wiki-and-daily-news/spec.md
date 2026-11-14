# Remove wiki and daily-news skills — spec
intent: 2026-11-14-remove-wiki-and-daily-news@2e7d40a31d5f4e926666e7794f30282134a8b5d4
confirmed-behavior: 2026-11-14 @a9402c3
pre-build-review: required — removal changes the publicly exposed skill contract

## Requirements

REQ-1 — Remove wiki capabilities
  The released plugin shall no longer expose wiki-setup, wiki-ingest, wiki-query, wiki-cross-linker, wiki-merge, wiki-lint, wiki-auto-research, or wiki-update, including their dedicated helpers and maintenance support → Acceptance #1

REQ-2 — Remove news capabilities
  The released plugin shall no longer expose daily-news-digest, including daily aggregation, cross-date history, story tracking, and dedicated helpers → Acceptance #2

REQ-3 — Preserve the remaining skills
  The plugin shall expose the other 14 skills without requiring the removed components, preserving general daily notes, topic research, web/video extraction, note writing, and diagrams, with relevant regression checks and representative basic operations passing → Acceptance #3

REQ-4 — Describe the current offering
  The plugin's current entry points, descriptions, routing instructions, and operating documentation shall offer the retained skills without directing users to the nine removed skills → Acceptance #4

REQ-5 — Preserve existing data and unrelated work
  The removal shall leave existing vault notes, wiki pages, news digests, story-tracking notes and settings, the original Monkey project, installed plugin caches, and unrelated work including the pre-existing roadmap draft untouched → Acceptance #5

REQ-6 — Preserve traceability
  The repository shall retain Git history, required licensing and attribution, and historical records, distinguishing historical wiki/news capabilities from the current offering → Acceptance #6

## Design decision

- agent-decided — Delete the nine skill directories and their exclusively owned supporting code, tests, and references; retaining dormant implementations would leave the requested mechanisms in the project.
- agent-decided — Remove only obsolete CI checks and shared distribution support whose consumers are all removed; preserve meaningful checks for retained functionality.
- agent-decided — Clean current cross-references in retained skills without redesigning their unrelated behavior; preserve ordinary wikilink syntax.
- agent-decided — Release metadata must consistently identify the changed offering; installed caches and host settings are outside this source change.
- user-decided — Existing user data is preserved, as pinned by intent Constraints and PRINCIPLES.md non-negotiable 1; no migration or deletion command is introduced.
- agent-decided — Historical changelog and provenance remain historical evidence; current descriptions are updated instead of rewriting historical claims.

## Alternatives considered

- Disable routing but keep the nine directories: rejected because hosts can still discover installed skill directories.
- Remove every mention of wiki or daily: rejected because this would damage ordinary internal links, daily notes, and historical attribution.
- Delete existing vault output: rejected because it violates the confirmed data-preservation constraint.
- Replace removed capabilities with another workflow: rejected as outside the confirmed scope.

## Current state evidence

- Forward: obsidian/.codex-plugin/plugin.json, interface.defaultPrompt, currently offers wiki ingestion.
- Reverse: obsidian/skills/using-obsidian/SKILL.md, Wiki layer table and Quick Start, routes users to wiki skills; obsidian/skills/obsidian-research/SKILL.md, Related skills, references removed siblings.
- Error: obsidian/skills/daily-news-digest/scripts/validate.sh, exit-status contract, reports validation failures for news diagrams; this dedicated command disappears with its owning skill.
- Data: obsidian/skills/daily-news-digest/SKILL.md, daily output under news/daily-news and story books under news/store-arcs, describes user-owned output that this change must not touch.
- Boundary: .github/workflows/test-obsidian.yml, SSOT drift and skill-script pytest steps, includes dedicated checks requiring reassessment; PRINCIPLES.md, Non-negotiables, preserves user data and bounded scope.

## UI flows

| Case | What the user does | What they see |
|---|---|---|
| Current offering | Reads the new version's skill listing or current usage documentation | Fourteen retained skills; the eight wiki skills and daily-news-digest are absent from offered operations. |
| Retained operation | Requests general daily notes, topic research, web extraction, note writing, or diagrams | The corresponding retained skill remains available with its existing workflow. |
| Removed operation | Attempts to select one of the nine removed skills in the new version | The plugin does not provide or route to that skill; missing-skill wording and presentation remain host-controlled. |
| Existing output | Opens a pre-existing wiki page, news digest, or story-tracking note | The existing file remains unchanged; this removal adds no migration or deletion step. |
| Historical documentation | Reads old changelog or provenance records | Past capabilities remain traceable as history, separate from the current offering. |

Empty, progress, and error variants: no new interactive operation is added. Listing, loading, and missing-skill errors remain host-owned; this change promises no new host messages, exit codes, progress indicators, or recovery controls. Source changes alone do not refresh an already installed plugin or the active session's catalog.
