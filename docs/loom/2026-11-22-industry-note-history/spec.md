# Continue research from editable industry notes — spec
intent: 2026-11-22-industry-note-history@228e415
confirmed-behavior: 2026-11-22 @bde0c75
pre-build-review: required — changes the persistent note reader and the eligibility of saved historical records

## Requirements

REQ-1 — Read existing histories
  WHEN resuming from the tested prototype or released pre-rename note format, the industry-research skill shall return usable saved records without rewriting the notes → Acceptance #1

REQ-2 — Resume after prose edits
  WHEN a user edits the prose in an industry note and its research history remains complete, the industry-research skill shall read the history and allow the next quarter to be researched → Acceptance #2

REQ-3 — Report unusable history
  IF a history record is unreadable, incomplete or belongs to a different study or quarter, THEN the industry-research skill shall report the affected gap and exclude the record from verified carry-forward while allowing independent, eligible work → Acceptance #3

REQ-4 — Retain cutoff eligibility
  WHEN asked to cite a historical claim, the industry-research skill shall restrict evidence to original sources available at the specified cutoff → Acceptance #4

## Design decision

- User-decided: remove read-time note fingerprints and record the convention in the repository.
- Agent-decided: read existing history formats in place and check record fields and attribution because note edits and format upgrades must not require migration.
- Agent-decided: retain the existing write-time conflict protection because concurrent edits can otherwise be lost.

## Alternatives considered

- Retain a prose fingerprint. It would keep rejecting legitimate edits.
- Drop history validation entirely. Unreadable or misattributed data could be carried into later quarters.

## Current state evidence

- Forward: `obsidian-finance/skills/industry-research/SKILL.md` — calls resume and cite.
- Reverse: `obsidian-finance/scripts/market_research.py` — resume, cite, and carry-forward consult saved quarter records.
- Error: `docs/skill-dogfood/2026-11-22-industry-research/report.md` — the prototype history failed validation but the agent carried it forward directly.
- Data: `obsidian-finance/scripts/market_research.py` — note history stores structured data alongside visible Markdown.
- Boundary: `obsidian-finance/scripts/industry_update.py` — detects intervening edits at publication.

## UI flows

- Ask to resume a prototype or released study → The assistant reads available research without altering the original notes.
- Edit the note prose and ask to continue → The assistant uses the complete saved history to continue the next quarter.
- Ask to continue with a missing or mismatched history record → The assistant identifies the gap and continues independent work using eligible evidence.
- Ask for a claim at a historical cutoff → The assistant returns the eligible claim and source or identifies the missing evidence.
