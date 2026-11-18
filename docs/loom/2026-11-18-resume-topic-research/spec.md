# Resume topic research — spec
intent: 2026-11-18-resume-topic-research@5b2b206
confirmed-behavior: 2026-11-18 @caa6356
pre-build-review: required — multi-file history and partial updates can compromise evidence traceability

## Requirements

REQ-1 — Resume from saved research
  WHEN the user requests another round by topic or by explicit folder, the skill shall resolve the folder (default: `<vault-root>/research/{topic}`) and find the latest completed round from the entry note, recover the question and unresolved work, and show the scope and measurement basis of the new evidence → Acceptance #1

REQ-2 — Revise affected judgments
  WHEN new evidence overturns a shared judgment, the skill shall revise it, record why, and update both dependent topic notes in the acceptance case with the effect on each → Acceptance #2

REQ-3 — Read prior conclusions and evidence
  WHEN the skill updates research, the skill shall preserve the ability to open the exact judgment and source versions used by earlier reports → Acceptance #3

REQ-4 — Preserve supported judgments
  WHEN evidence only qualifies the judgment or is insufficient to revise it, the skill shall preserve the supported judgment and record the qualification or evidence gap in the new round accessible from the entry note → Acceptance #4

## Design decision

- agent-decided — Use the entry note, source notes, topic notes, and dated history established in the pilot. Keep shared judgments with topic notes and give them a distinct note only when reused.
- agent-decided — Use fixed local Markdown versions and retained source artifacts for historical references. Link current work to the latest judgment and dated reports to the version they used. Flag unavailable original source material rather than asserting exact traceability.
- agent-decided — Present the latest completed round from the entry note, including a completed round with no change in judgment. Record interrupted work separately so the entry continues to identify the last completed round.
- user-decided — Default to `<vault-root>/research/{topic}` for a named topic. An explicit folder within the selected vault takes precedence.
- user-decided — Name notes by purpose. Keep the entry and current topic or shared-judgment filenames stable, with creation and update dates in note properties. Identify sources by a stable ID and short title; record publication date, retrieval date, and version when available. Prefix dated round records and frozen historical notes with `YYYY-MM-DD` and the round ID to distinguish same-day runs. The prefix is the date of the research round represented by the note; record the evidence cutoff separately.
- agent-decided — Only write within the designated research folder. Preserve existing inputs before edits. When the folder is ambiguous, locate it with user input before writing. Validate traversal from the entry to the new round and from the old report to its prior evidence.
- agent-decided — Use an isolated Codex session for initial acceptance because the prior manual tests exercised the document workflow there. Wider host support requires its own evidence.

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
| Qualification or insufficient evidence | Supply evidence with a limited or mismatched scope | The supported judgment remains. The new round explains the qualification or evidence gap and is reachable from the entry. |
| Browse research notes | Open the topic folder | Current notes have stable names. Historical notes show the research date and round, with the evidence cutoff recorded separately. |
| Review history | Open an earlier report | Its links open the exact judgment and source versions used then. Missing originals are disclosed explicitly. |
| Ambiguous target or interrupted round | Give an ambiguous vault or folder reference or resume after an interrupted update | The skill asks which vault or folder to use before writing, or identifies the last completed round and any saved unfinished work. |
| Irreversible action | N/A | The approved flow retains prior versions within the selected research folder. |
