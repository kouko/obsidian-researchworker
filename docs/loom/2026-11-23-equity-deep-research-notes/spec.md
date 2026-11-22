# Deep quarterly equity research notes — spec
intent: 2026-11-23-equity-deep-research-notes@6a1b95e
confirmed-behavior: 2026-11-23 @fdd04fc
pre-build-review: required — Changes to the published note contract must preserve cutoff-aware verification and safe continuation.

## Requirements

REQ-1 — Readable research notes
  WHEN the workflow writes a Markdown report or registration, it shall provide concise flat Obsidian properties, a visible purpose, a supported conclusion or evidence description, traceable references and material limitations → Acceptance #1

REQ-2 — Analysis depth and evidence gaps
  WHEN the workflow prepares a quarterly analysis, it shall apply the minimum checks for that analysis role and present their outcomes, or disclose the missing input, the unfinished check and the affected judgment → Acceptance #2

REQ-3 — Compact overview and evidence presentation
  WHEN a quarter is saved, the workflow shall show material changes, report links and evidence gaps in the overview, use tables for relevant comparisons and Mermaid only where relationships benefit from a diagram, and store materially fewer repeated observations than the existing overview on the same evidence → Acceptance #3

REQ-4 — Continuation and integrity
  WHEN a researcher updates or resumes a quarter, the workflow shall preserve eligible evidence and report paths, honor the requested cutoff, preserve manual edits and support recovery from interrupted saves → Acceptance #4

## Design decision

- User-confirmed scope: every generated Markdown note is reader-facing, including source and method registrations. Retain existing fiscal naming, source integrity and note update protections.
- Agent-decided: retain only atomic properties at the top. Give reports a clear question, findings, evidence and limitations. Give registrations a purpose, applicability, evidence or method steps and limitations. Keep data-native source payloads in their original format.
- Agent-decided: keep the source version binding and selected evidence exact. Replace repeated full projections with references to the quarter-local captured records, validating the resolved evidence before reuse and portable verification. Review the reduction against the actual Fastenal baseline.
- Agent-decided: keep existing published files in place. Exercise the compact format in an isolated copy, with existing saved data readable where current behavior depends on it.

## Alternatives considered

- Formatting alone leaves duplicated observations and insufficient role guidance.
- Deleting the structured record would remove portable evidence and continuation checks.
- Moving repeated YAML to another location would leave total duplication intact.

## Current state evidence

- Forward: `obsidian-finance/skills/equity-research-us/SKILL.md` chooses role instructions and publishes quarterly reports.
- Reverse: `obsidian-finance/scripts/research_store.py`, `_fixed_record` and `_verify_quarter_evidence`, reads the overview and verifies source bindings.
- Error: `obsidian-finance/scripts/research_store.py`, `recover_quarterly`, scopes interrupted update recovery.
- Data: `obsidian-finance/scripts/research_store.py`, `_capture_quarter`, captures the consumed evidence for portable verification.
- Boundary: the isolated Fastenal Q2 baseline has 3,739 lines in the overview record and 12 consumed projections with two unique payloads.

## UI flows

Open overview → See the reason for the study, material changes since the prior quarter, links to analyses and the priority gaps.

Open report → See the question and conclusion first, then the evidence, calculations or reasoning, counterevidence and limits. Compare periods or scenarios in tables. Use a diagram where a causal or dependency relationship needs explanation.

Open source or method registration → See why it was used, the supporting document or applied method and its limitations. Follow its links to retained evidence or related notes.

Continue research → Reopen the same report paths. Adopt verified eligible prior results and show how they support the new work. Keep dated material revisions as part of the affected note.

Open a report with insufficient data → See the completed portion, the missing evidence, the pending check and the conclusion it prevents. Do not produce a numeric estimate without support.

Request history or encounter a conflicted save → See cutoff-eligible results or a specific evidence gap. Preserve edits and report any interrupted publication that needs recovery.

### Minimum analysis outputs

| Role | Visible result |
| --- | --- |
| Financial | Comparable statements and period definitions, a material earnings-to-cash or balance-sheet reconciliation, and liquidity or financing implications. |
| Operating | Business-specific operating drivers, quantitative and qualitative evidence classified separately, and a test of whether change can persist. |
| Industry and competition | Market boundary, company exposure, independent comparisons where available and rival explanations for changes. |
| Forward forecast | Prior assumptions and outcomes where eligible, management guidance distinct from analyst scenarios, drivers, triggers and limitations. |
| Valuation and risk | Model choice and dated inputs, supported range and sensitivity when possible, and a risk mechanism with observable triggers. |
| Technical | Dated price and volume basis, adjustments, trend and levels where verifiable, and limits on comparison against value. |
| Synthesis | Decision-relevant changes, thesis and counterevidence, separate horizons, conditions and ranked gaps. |
