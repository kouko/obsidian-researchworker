# Quarterly industry and market research — spec
intent: 2026-11-21-finance-industry-market-research@57f464b
confirmed-behavior: 2026-11-21 @3ef4b7c
pre-build-review: required — the replacement vault layout, preservation of user edits, and historical evidence eligibility affect a persistent public contract

## Requirements

REQ-1 — Quarterly market analysis
  WHEN asked to study adjacent smartphone market quarters, the skill shall create standard Obsidian research notes with comparable shipment and share observations, scope, definitions, explanations and evidence limits → Acceptance #1

REQ-2 — Resume saved research
  WHEN a new conversation resumes a market, the skill shall recover its verified progress, source versions and open work from saved Markdown and continue the requested quarter → Acceptance #2

REQ-3 — Cite eligible market findings
  WHEN Apple research cites a market finding, the skill shall expose its original source, version, observation quarter and availability and exclude evidence later than the issuer cutoff → Acceptance #3

REQ-4 — Review outlook across markets and quarters
  WHEN updating either of at least two verified markets to the next quarter, the skill shall compare earlier outlooks with eligible results for the corresponding target period, preserve unresolved forecasts and update its assumptions and outlook → Acceptance #4

REQ-5 — Update the same quarter notes
  WHEN a quarter is updated, the skill shall retain the note paths, link available substudies from the quarter overview and record material changes alongside their earlier values, judgments, forecasts and applicable source versions and dates in the affected notes → Acceptance #5

REQ-6 — Default to the vault investment research area
  WHEN a user starts a study in a resolved Obsidian vault without specifying another location, the skill shall create the study and quarter notes under the vault's investing/industries directory → Acceptance #6

REQ-7 — Identify quarterly notes in Obsidian
  The skill shall use the same quarter-first prefix for a quarter's related filenames and supply consistent flat properties for filtering by market, quarter and status → Acceptance #7

## Design decision

User-decided: keep one directory per market and one per calendar quarter. Use
`<vault>/investing/industries/<study-id>/<YYYYQn>/` by default. Resolve an
explicit, unambiguous vault-local destination when supplied. Use a stable
market identifier for storage and a full human-readable market name in notes.
Fix the naming language and market display name once for the study. Use a
shared `<quarter> <market name>-<topic>.md` prefix, with filenames and first
headings matching except for the extension. In Traditional Chinese, the
standard topic suffixes are 總覽, 規模與市佔率, 供應鏈, and 指引與展望.
A company observation uses the same prefix and adds the company to the
supply-chain topic. It is created when independent tracking adds value.

Agent-decided: use flat Obsidian properties with stable types. Proposed core
quarter properties are `type` (text role), `market` (text study identifier),
`quarter` (text calendar quarter), `status` (text progress), `as_of`
(text ISO date or offset-bearing timestamp), and `updated` (date).
Use `company` (text stable company identifier) on company observations.
Use title text in the filename and H1. Link to existing substudies and show
missing evidence or pending sections in the overview. The project overview
holds cross-quarter definitions and enduring roles. The quarterly supply-chain
study documents material changes and substantiated dependencies, and labels
unverified relationships. Preserve exact definitions used by earlier notes.

Agent-decided: use the prior clean revised result as the basis of a same-note
update. Preserve prior materially different evidence, claims and forecasts
with stable references and the historical cutoff. Separate source release time,
research cutoff and note write time. Retain comparable-target and all-source
eligibility rules in research/07-spec-review-criteria.md where applicable.
Save the current text without discarding user edits, use recoverable writes,
and never select an incomplete batch as the authoritative quarter. A conflict
surfaces the affected note and preserves user text. Keep earlier rN records
readable where supported. Do not automatically migrate, remove or rewrite
existing legacy files.

## Alternatives considered

- One physical note for an entire quarter impedes independent supply-chain
  and company research.
- One full set of files for every revision obscures the current notes in the
  vault file list and duplicates unaffected material.
- Updating only the latest prose would discard historical evidence needed for
  cutoff-bound citations and forecast review.

## Current state evidence

- Forward: obsidian-finance/skills/market-research/SKILL.md, Establish the study.
- Reverse: obsidian-finance/skills/finance-research/references/industry-and-competition.md, Adopt quarterly market evidence.
- Error: research/03-smartphone-quarterly-pilot.md, Forecast carry-forward, records an unreconciled change to Q2 growth.
- Data: obsidian-finance/skills/market-research/references/record.md currently documents rN note groups; research/08-runtime-replay.md verifies that old behavior.
- Boundary: obsidian/skills/obsidian-research-project/SKILL.md, Apply or recover an update, provides the continuity reference. Existing vault notes stay in place.

## UI flows

| Case | What the user does | What they see |
|---|---|---|
| First quarter | Ask to research a quarter in a chosen vault | A project under investing/industries by default and a quarter overview linking its substudies. Related notes share the quarter and full market name. |
| Missing evidence | Ask for a study whose inputs are incomplete | The overview identifies the partial studies, missing evidence and what to resume. |
| Resume | Ask a new conversation to continue | It finds the quarter overview and notes, reads pending questions and source versions, and reports any conflict or interrupted update. |
| Same-quarter update | Supply corrected data for the same quarter | The affected notes retain their paths. Current analysis is updated and the material prior claim or outlook remains available in the note. |
| Next quarter | Ask for the next quarter | A new quarter group links to the prior outlook and compares eligible matching actuals. Unreported targets remain pending. |
| Company citation | Ask Apple research to cite a market claim at its cutoff | The eligible version, original source and market observation quarter are shown separately from the fiscal quarter and issuer cutoff. Later evidence is excluded. |
| Obsidian browsing | Search by filename or filter note properties | Sibling notes group by their common prefix and the properties distinguish roles, quarters, markets and progress. |
