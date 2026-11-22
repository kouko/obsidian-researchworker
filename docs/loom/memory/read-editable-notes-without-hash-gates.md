---
name: read-editable-notes-without-hash-gates
description: Read user-editable Obsidian prose as it exists now. Validate the research fields a claim depends on and detect conflicting edits during the current write.
type: practice
sources:
  - resource: "docs/loom/2026-11-22-industry-note-history/research/01-obsidian-edit-and-history.md"
  - resource: "docs/skill-dogfood/2026-11-22-industry-research/report.md"
---

# Read editable notes without hash gates

**Trigger.** A skill resumes research from Obsidian notes that readers can edit between sessions.

**Correct path.** Read the current note without requiring its prose to match a persisted fingerprint. Validate the saved research fields needed for the operation, including record ownership, required evidence, and source availability at the cutoff. Report gaps for the affected records. Before overwriting a note, detect changes since the current operation read it and preserve intervening edits.

**Why.** An ordinary Markdown edit or a change in digest format can break an exact fingerprint while leaving the research record usable. A current-write comparison addresses a different failure: overwriting edits made after the current operation read the file.

**Limits.** The convention applies to editable notes. Immutable source artifacts and interrupted-write recovery may have separate integrity requirements.
