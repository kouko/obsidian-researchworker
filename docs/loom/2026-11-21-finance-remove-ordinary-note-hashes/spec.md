# Ordinary research note edits — spec
intent: 2026-11-21-finance-remove-ordinary-note-hashes@b2b2b75
confirmed-behavior: 2026-11-21 @cff7120
pre-build-review: required — saved evidence records are a compatibility contract and ordinary note edits interact with publication conflicts

## Requirements

REQ-1 — Continue after routine note edits
  WHEN an ordinary research note is edited, the system shall allow reuse and a follow-up save when the adopted claim and eligible evidence still support the analysis → Acceptance #1

REQ-2 — Check adopted claims
  WHEN an adopted claim changes, disappears, or lacks eligible original evidence, the agent shall identify the affected analysis and distinguish it from independently reusable work → Acceptance #2

REQ-3 — Accept old and new research records
  WHEN a quarter is read or saved, the system shall accept old ordinary-note hash fields as legacy metadata and shall save new ordinary-note citations without requiring or writing a hash → Acceptance #3

REQ-4 — Protect publication and the original evidence
  WHEN a competing save advances a quarter's valid predecessor or an independently copied quarter is verified, the system shall reject the competing save or verify the bound SEC originals and cutoff, respectively → Acceptance #4

## Design decision

- agent-decided — Ordinary research notes do not provide economic evidence by themselves. Store the attributed claim, note path and independently eligible source identity. Recheck the meaning of adopted claims in the live skill so harmless edits do not invalidate work by byte comparison.
- agent-decided — Exclude only ordinary candidate note bytes from publication conflict detection. Preserve protection for authoritative records, analysis outputs and source or method files. Distinguish managed note roles from ordinary notes.
- agent-decided — Ignore legacy ordinary-note digests on read and strip them from newly saved citations. Leave prior files in place. Standalone verification can check the saved claim's bound evidence without access to the current ordinary note.

## Alternatives considered

- Retain note digests as invalidation signals. Byte changes would continue to conflate editorial and evidence changes.
- Remove all hashes. This would also remove exact SEC evidence and managed output verification outside the requested scope.

## Current state evidence

- Forward: `obsidian-finance/skills/finance-research/SKILL.md:49` calls candidate-aware discovery before deciding which work to reuse.
- Reverse: `obsidian-finance/scripts/research_store.py:335` checks claims, note bytes and independent source bindings.
- Error: `obsidian-finance/scripts/research_store.py:850` checks changed filesystem snapshot entries at publication.
- Data: `obsidian-finance/tests/test_research_continuation.py:375` exercises editing an ordinary note cited by an older record.
- Boundary: `obsidian-finance/scripts/research_store.py:1193` represents the portable verification path. Preserve the primary evidence and cutoff contract.

## UI flows

- Fix a typo or adjust formatting in a cited ordinary note, then continue research → the unchanged claim and valid analysis remain usable and a follow-up save is allowed.
- Remove or change an adopted claim, then continue → the agent identifies what needs reconsideration and states the evidence gap.
- Continue a previously saved quarter → old note digests require no migration. New ordinary-note citations retain attribution without retaining note hashes.
- Save from a predecessor already advanced by someone else → the competing save is refused. Move an existing quarter and verify an SEC original → the agent can check its retained original and cutoff.
