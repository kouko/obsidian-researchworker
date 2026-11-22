# Optional earnings-call evidence — spec
intent: 2026-11-22-equity-earnings-call-evidence@8f26dab
confirmed-behavior: 2026-11-22 @8cc8594
pre-build-review: not-required — scoped guidance for existing analysis notes and source registration with no interface or data migration

## Requirements

REQ-1 — Trace the claim
  WHEN a relevant transcript is available, the research skill shall cite the issuer and fiscal quarter, the source, and the speaker with a section or timecode, and distinguish management guidance, analyst questions and realized results → Acceptance #1

REQ-2 — Continue through gaps
  WHEN only an excerpt, summary or no eligible call evidence is available, the research skill shall label the coverage or gap and continue work supported independently → Acceptance #2

REQ-3 — Honor the cutoff
  WHEN researching a historical quarter, the research skill shall distinguish the call time from the cited material's verified public availability and exclude information whose availability by the cutoff cannot be established → Acceptance #3

REQ-4 — Prefer formal financial figures
  IF a transcript figure conflicts with a cutoff-eligible formal financial statement or SEC document for the same period, metric and basis, THEN the research skill shall cite the formal figure and flag the discrepancy, labeling call-only figures as management commentary or guidance with their verification status → Acceptance #4

## Design decision

- Agent-decided — Use the existing optional source registration and already supported text payload. Record provenance and coverage in the existing fields and relevant analysis. Keep call evidence out of mandatory asset source lists.
- Agent-decided — When an analysis explicitly relies on a call source, use the existing dependency checks before reusing that analysis. Other work can continue.
- Agent-decided — Keep the same analysis entry point and output set. Place lookup details in the bundled reference and the numeric evidence rule where the research skill applies it.

## Alternatives considered

- Automatic collection and a mandatory transcript for every quarter would create a hard dependency on inconsistent availability.
- A standalone call report would duplicate evidence and expand the agreed deliverable.

## Current state evidence

- Forward: `obsidian-finance/skills/equity-research/SKILL.md`, acquisition and analysis section.
- Reverse: `obsidian-finance/skills/equity-research/templates/source-registration.md`, existing registration template.
- Error: `obsidian-finance/scripts/work_assessment.py`, checks consumed dependencies and eligible source revisions.
- Data: `docs/loom/research/2026-11-22-earnings-call-qualitative-evidence.md`, optional source publication and historical cutoff probe.
- Boundary: `docs/loom/research/2026-11-22-earnings-call-source-feasibility.md`, free access examples and limits.

## UI flows

| Case | User request | Observed outcome |
| --- | --- | --- |
| Relevant call evidence | Ask to research a company quarter. | The relevant analysis cites the eligible call by speaker and location. |
| Partial or missing evidence | Ask to research a quarter with limited call coverage. | The analysis labels the limit and independently supported work proceeds. |
| Historical assessment | Ask to research as of an earlier date. | The analysis excludes call-related content without verified availability by that date. |
| Conflicting numbers | Ask to research a quarter with conflicting transcript and formal financial figures. | The analysis uses the eligible formal figure for realized results, flags the discrepancy and labels call-only figures separately. |
