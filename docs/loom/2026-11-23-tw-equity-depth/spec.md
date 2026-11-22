# Taiwan equity research depth — spec
intent: 2026-11-23-tw-equity-depth@dcc22e22ae30a8fe41a0a484ff84e39e3d599e30
pre-build-review: required — The persisted quarter format is a compatibility contract for portable verification, continuation, and conflict protection.
confirmed-behavior: 2026-11-23 @b38ac20

## Requirements

REQ-1 — Readable quarter and supporting notes
  WHEN a Taiwan quarter is saved, the skill shall provide a readable Obsidian overview with the cutoff, main conclusions, material gaps and report links, give every emitted Markdown research note readable properties and prose, and retain machine records in separately traceable non-Markdown research data → Acceptance #1

REQ-2 — Analysis depth
  WHEN a Taiwan report section is written, the skill shall answer its research question using traceable point-in-time sources, calculations or reasoning, limitations and evidence that would change the conclusion where applicable → Acceptance #2

REQ-3 — Installed replay
  WHEN the finished skill is validated, the project shall check the TSMC Q3 reading sample and independently replay two consecutive quarters for each of Hon Hai, TSMC and Delta, verifying all six reports, three transitions and Obsidian reading behavior → Acceptance #3

REQ-4 — Traceable continuation
  WHEN a researcher opens or updates a quarter, the skill shall preserve access to prior sources, forecast and correction versions, protect simultaneous edits, and keep existing Taiwan and US quarterly research readable and resumable → Acceptance #4

## Design decision

- agent-decided — Keep the visible Taiwan note roles and put machine records under quarterly data with a versioned reader. This gives users stable note paths and limits the format change to Taiwan. Read legacy inline records without bulk conversion.
- agent-decided — Keep source and method identity, date, and revision records, and have analysis reference the applicable versions instead of expanding them in the overview. A transaction may check for concurrent edits without making a formerly verified content hash a prerequisite for reading ordinary prose.
- agent-decided — Provide one Traditional Chinese analysis framework per role or a shared reference with clear role sections. Financial analysis connects the three statements and reconciles monthly versus filing amounts. Operating analysis examines business drivers and tests management statements. Industry analysis distinguishes direct peers and supply-chain signals. Forecasts identify comparable versions, assumptions and sensitivities. Valuation explains model inputs and downside. Technical analysis shows price and volume windows and limits. Synthesis weighs evidence by horizon and identifies update triggers.
- agent-decided — Assess substantive claims and evidence rather than a line quota. Where a source is missing, identify the affected conclusion and state what follow-up would resolve it. Keep contemporaneous guidance distinct from retrospective analysis.

## Alternatives considered

- Collapse the existing machine block. It would still be part of the note source and would leave the duplicate payload and research depth unchanged.
- Remove the machine record. It would discard bindings needed for verification, forecasts and corrections.
- Reuse US guidance verbatim. The analytical questions overlap, but the Taiwan workflows need local source timing, accounting and filing conventions and Traditional Chinese instructions.

## Current state evidence

- Forward: `obsidian-finance/skills/tw-equity-research/SKILL.md` sets extensive acquisition and cutoff rules with a short general analysis instruction.
- Reverse: `obsidian-finance/scripts/research_store.py` reads fixed quarterly overviews for discovery and verifies their associated evidence.
- Error: `obsidian-finance/tests/test_research_continuation.py` exercises quarterly publication, recovery and conflicting edits.
- Data: The isolated TSMC Q3 overview contained 3,476 lines with the machine record inline. Its reading sample at `/private/tmp/tsmc-q3-analysis-pilot/研究筆記` has eight Markdown notes and separate research data. Static properties, targets and rendering were checked.
- Boundary: The new Taiwan format changes generated outputs. Existing vaults and the US note format remain outside bulk migration.

## UI flows

| Case | What the researcher does | What they see |
| --- | --- | --- |
| Open the quarter | Open the overview in Obsidian | Conclusions, cutoff, gaps and navigation to the seven analyses |
| Review evidence | Follow links from an analysis or its evidence note | The source version and locator, which facts are supported, and the limits of the interpretation |
| Continue the research | Open an earlier quarter or update a quarter with new evidence | Date-appropriate prior findings and revisions at stable paths, with conflicts surfaced before any overwrite |
