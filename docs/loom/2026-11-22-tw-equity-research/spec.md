# Taiwan quarterly equity research — spec
intent: 2026-11-22-tw-equity-research@5fe05ea
confirmed-behavior: 2026-11-22 @a71eddb
pre-build-review: required — new public skill and external disclosure inputs

## Requirements

REQ-1 — Quarterly continuity
  WHEN the user starts or resumes research on a TWSE-listed issuer, the skill shall maintain one editable set of numbered Traditional Chinese notes per quarter, with acceptance covering three issuers across three consecutive quarters each and both transitions per issuer → Acceptance #1

REQ-2 — Monthly updates
  WHEN monthly revenue is public before the filing, the skill shall show available months and compare matching periods with the eligible original prior-quarter forecast while preserving the forecast and its publication time → Acceptance #2

REQ-3 — Sources and completeness
  WHEN research is saved, the overview shall show the cutoff, eligible filing versions and gaps, with quarterly completion requiring the quarterly filing, three months of revenue and checked material disclosures and annual completion requiring the annual report → Acceptance #3

REQ-4 — Conference evidence
  WHEN conference evidence is checked, the skill shall show the status and links for slides, transcripts and recordings, record search attempts for missing items and produce a timestamped machine transcript when only accessible media is available → Acceptance #4

REQ-5 — Traceable claims
  WHEN a report cites evidence, the skill shall prefer original quantitative disclosures for actuals, cite the PDF pages and flag unreadable content, and attribute management outlook and strategies to the source with numerical guidance labeled as expectations → Acceptance #5

REQ-6 — US continuity
  WHEN the US skill resumes an existing quarter, it shall retain its existing issuer identity, notes and source references → Acceptance #6

## Design decision

- User-decided — provide an independent skill in Taiwan Traditional Chinese, with acquisition code bundled behind the research entry.
- User-decided — use `YYYYQq <ticker> <company> - <number> <report name>.md` with 00 季度研究總覽, 01 財務分析, 02 營運分析, 03 產業與競爭, 04 預測, 05 估值與風險, 06 技術分析 and 99 投資綜合結論.
- Agent-decided — use stable quarterly paths and dated revision history, following the current equity format. Preserve concurrent user edits and record conflicts for retry.
- Agent-decided — compare evidence availability against the requested cutoff and distinguish retrieval failures from a successful search that found no disclosure. Search MOPS and issuer IR for supplementary materials. Missing supplementary sources leave dependent claims pending.
- Agent-decided — prefer published transcripts and available captions. Use timestamped machine transcription as fallback. Read original needed PDF pages including their visual content, checking material values against the original units and columns.
- Agent-decided — select nine issuer-quarter cases in the plan using source coverage and variation in conference material availability.

## Alternatives considered

- Combined US and Taiwan entry — separate entries preserve independent analytical instructions and their authoring languages.
- Separate download skill — one research entry covers the agreed use.
- Version folders for every update — stable quarterly paths support continued editing and dated history.

## Current state evidence

- Forward — [US equity skill](../../../obsidian-finance/skills/equity-research/SKILL.md#quarterly-equity-research).
- Reverse — [finance package guide](../../../obsidian-finance/README.md) describes quarterly publication.
- Error — [quarterly notes spec](../2026-11-22-equity-quarterly-notes/spec.md) describes update and recovery.
- Data — [research store](../../../obsidian-finance/scripts/research_store.py) defines report roles and stable names.
- Boundary — [confirmed intent](../intent/2026-11-22-tw-equity-research.md#out-of-scope).

## UI flows

- Start with an issuer and quarter → see the selected company, quarter and cutoff, then a quarterly overview and available numbered reports.
- Resume before the filing is public → see published months, comparable prior forecast and outstanding sources. While acquiring evidence, see which sources are being checked.
- Resume after the filing is public → see the same notes updated with dated revisions and the latest status.
- Inspect conference evidence → see source status and links, including a timestamped transcript when only accessible media is available.
- Enter an ambiguous issuer → see which company identity is required. Clarify it to resume.
- Encounter unavailable evidence → see the affected source and pending findings. Resume when the source is available or supplied.
- Encounter a conflicting edit → see which note changed. Resolve the conflict before retrying, retaining the currently saved note.
- Resume US research → see the saved scope and reports through the existing US entry.
