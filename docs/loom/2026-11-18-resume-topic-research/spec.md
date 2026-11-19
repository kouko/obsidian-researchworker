# Resume topic research — spec
intent: 2026-11-18-resume-topic-research@5b2b206
confirmed-behavior: 2026-11-18 @ca8d1d3
pre-build-review: required — multi-file history and partial updates can compromise evidence traceability

## Requirements

REQ-1 — Resume from saved research
  WHEN the user requests another round by topic or by explicit folder, the skill shall resolve the folder (default: `<vault-root>/research/{topic}`) and find the latest saved research state from the entry note, recover the question and unresolved work, and show the scope and measurement basis of the new evidence → Acceptance #1

REQ-2 — Revise affected judgments
  WHEN new evidence overturns a shared judgment, the skill shall revise it, record why, and update both dependent topic notes in the acceptance case with the effect on each → Acceptance #2

REQ-3 — Read prior conclusions and evidence
  WHEN the skill updates research, the skill shall preserve the ability to open the exact judgment and source versions used by earlier reports → Acceptance #3

REQ-4 — Preserve supported judgments
  WHEN evidence only qualifies the judgment or is insufficient to revise it, the skill shall preserve the supported judgment, reuse existing notes for useful qualifications, update the entry only for new follow-up work, and create no additional notes or historical versions when replaying the same evidence → Acceptance #4

## Design decision

- agent-decided — Use the entry note, source notes, topic notes, and dated history established in the pilot. Keep shared judgments with topic notes and give them a distinct note only when reused.
- agent-decided — Save a change record for material judgment changes and reuse existing fixed local Markdown versions and retained source artifacts for historical references. Link current work to the latest judgment and dated reports to the version they used. Flag unavailable original source material rather than asserting exact traceability.
- agent-decided — Keep the latest saved research state reachable from the entry note. For useful qualifications, reuse existing notes and add a source note only for distinct evidence worth citing. For insufficient or duplicate evidence, report the result in chat and add only genuinely new follow-up work to the entry. Keep at most one temporary recovery record for unfinished work and clear it after recovery or completion.
- user-decided — Default to `<vault-root>/research/{topic}` for a named topic. An explicit folder within the selected vault takes precedence.
- user-decided — Create `sources/raw/` only when a source file such as a PDF or CSV needs to be retained. Keep one copy of each retained version and link to it from the source note. Keep versions needed by earlier reports addressable after a replacement is received. For CSV evidence, record the relevant period, units, and fields in the source note when available.
- user-decided — Name notes by purpose. Keep the entry and current topic or shared-judgment filenames stable, with creation and update dates in note properties. Identify sources by a stable ID and short title; record publication date, retrieval date, and version when available. Prefix dated round records and frozen historical notes with `YYYY-MM-DD` and the round ID to distinguish same-day runs. The prefix is the date of the research round represented by the note; record the evidence cutoff separately.
- agent-decided — Only write within the designated research folder. Preserve existing inputs before edits. When the folder is ambiguous, locate it with user input before writing. Validate traversal from the entry to the new round and from the old report to its prior evidence.
- agent-decided — Use an isolated Codex session for initial acceptance because the prior manual tests exercised the document workflow there. Wider host support requires its own evidence.

- agent-decided — Before modifying a current note, trace affected historical links transitively. If an old report links to a mutable target, preserve the exact prior target and repair only its historical link, preserving the report text and original file version. If the prior target cannot be established, leave active notes unchanged and identify the affected report. A pre-existing missing original is reported as missing; a substitute does not establish exact traceability.
- agent-decided — Save a recoverable record of the planned writes and prior content before applying changes across files. On resume after an interruption, detect incomplete writes and complete or restore the update before interpreting current notes. Verify with an interruption after changing the judgment but before updating dependent notes.
- agent-decided — Resolve the selected vault and all paths, including symlinks. Reject destinations outside the vault or updates outside the designated research folder before any writes. If there is no valid entry or completed round to resume, report that fact and leave the folder untouched. A summary-only request does not update research.

### Shared writing guide

Use the vault's conventions for language and note properties. These examples show the minimum useful content for each note type. Create a note only when the existing research notes cannot carry the new content clearly. Add optional sections only when the evidence or question calls for them. Link to evidence or prior versions instead of repeating their contents.

- **Entry (`index.md`)** — Keep the question and scope, current progress, open work and navigation together. Example: “Why did global smartphone shipments fall in 2022? Scope: worldwide, calendar year 2022. Latest change: [Supply exception]. Next: obtain comparable retail data.”
- **Source (`sources/`)** — Record the publisher, date, version, evidence location, and what the source supports or leaves open. Link any retained original. Example: “Canalys, 2023-01-31, first paragraph. The annual decline refers to shipments into distribution; retail purchases use a different measure.” For CSV evidence, add data period, units and columns used when available.
- **Topic or shared judgment (`topics/`)** — State the question, current answer, supporting evidence and reasoning, and any unresolved points. Example: “Can we estimate inventory reduction from these releases? The measures have different coverage and bases, so their percentage difference does not quantify inventory reduction. Comparable channel flows are still needed.”
- **Material change record (`history/`)** — Record the research date and round, the substantive change and why, affected notes, and links to the prior judgment and source versions. Example: “R02 revised the branch's scheduled opening from seven to six days based on the corrected schedule for the same period. Updated visit planning and weekend access; see the prior report and original schedule.” Label illustrative data as such if it is used in a published example.

## Alternatives considered

- Copy the entire folder for every round. Rejected because it duplicates the evidence library and obscures the current working notes.
- Require a standalone note for every judgment. Rejected because only shared judgments required independent reuse in the pilot.
- Keep a mutable report plus a summary of changes. Rejected because a summary cannot recover the exact prior evidence.
- Schedule unattended updates. Deferred under the confirmed scope.

## Current state evidence

- Forward: docs/loom/intent/2026-11-18-resume-topic-research.md, Proposed outcome. No formal entry point exists for this capability.
- Reverse: obsidian/skills/obsidian-research/SKILL.md, description. Existing research skill describes writing a standalone research note.
- Error: docs/skill-dogfood/2026-11-18-resume-topic-research/report.md, Findings. Manual draft runs exposed missing entry-to-report navigation and missing raw source versions.
- Data: docs/research-pilots/2026-11-18-shared-claim/rules.md, citation and revision rules. Pilot uses Markdown and fixed prior claim notes.
- Boundary: docs/loom/intent/2026-11-18-resume-topic-research.md, Out of scope.

## UI flows

| Case | User action | Visible result |
|---|---|---|
| Resume | Ask to continue a named topic or specify a folder in a fresh conversation | The skill uses `research/{topic}` in the selected vault by default and identifies the last completed round, the question, outstanding work, and the scope of any new evidence. |
| Reversal | Supply evidence that overturns a shared judgment | The current judgment and dependent notes reflect the change. The new round shows why and which notes changed. The entry links to it. |
| Qualification or insufficient evidence | Supply evidence with a limited or mismatched scope | The supported judgment remains. Useful qualifications go into existing notes. Evidence gaps are reported in chat and only new follow-up work is added to the entry. Replaying the same evidence creates no notes or versions. |
| Retain an original source | Supply a PDF or CSV whose original is needed as evidence | The source note links to the retained version in `sources/raw/`. The folder appears when first needed, and repeated use of the same version reuses that file. |
| Browse research notes | Open the topic folder | Current notes have stable names. Historical notes show the research date and round, with the evidence cutoff recorded separately. |
| Review history | Open an earlier report | Its links open the exact judgment and source versions used then. Missing originals are disclosed explicitly. |
| Ambiguous target or interrupted round | Give an ambiguous vault or folder reference or resume after an interrupted update | The skill asks which vault or folder to use before writing, or identifies the last completed round and any saved unfinished work. |
| Missing or unsafe destination | Ask to resume a folder with no resumable round, or give a path outside the selected vault | The skill explains the problem and leaves the files untouched. |
| Incomplete update or untraceable prior version | Resume after an interruption, or provide evidence for a judgment whose prior version cannot be established | The skill recovers an interrupted update before relying on the current notes. If an earlier judgment cannot be recovered, it explains which report is affected and leaves the current judgment unchanged. |
| Summary only | Ask for a source summary without requesting a research update | The source summary is returned without changing the research folder. |
| Irreversible action | N/A | The approved flow retains prior versions within the selected research folder. |
