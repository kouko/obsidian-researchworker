# Quarterly industry and market research — spec
intent: 2026-11-21-finance-industry-market-research@25ddff0
confirmed-behavior: 2026-11-21 @1573ed2
pre-build-review: required — persistent note layout and historical evidence eligibility form a public contract

## Requirements

REQ-1 — Quarterly market analysis
  WHEN asked to study adjacent smartphone market quarters, the skill shall create standard Obsidian research notes with comparable shipment and share observations, scope, definitions, explanations and evidence limits → Acceptance #1

REQ-2 — Resume saved research
  WHEN a new conversation resumes a market, the skill shall recover its verified progress, source versions and open work from saved Markdown and continue the requested quarter → Acceptance #2

REQ-3 — Cite eligible market findings
  WHEN Apple research cites a market finding, the skill shall expose its original source, version, observation quarter and availability and exclude evidence later than the issuer cutoff → Acceptance #3

REQ-4 — Review outlook across markets and quarters
  WHEN updating either of at least two verified markets to the next quarter, the skill shall compare earlier outlooks with eligible results for the corresponding target period, preserve unresolved forecasts and update its assumptions and outlook → Acceptance #4

## Design decision

Agent-decided: use a market overview and a consistent set of quarterly Markdown note roles for market analysis, evidence and outlook, with versioned review records linking them. This keeps the material readable in Obsidian and gives continuation an explicit record to check. Source-native evidence can stay in its original format. Use one market-specific scope and metric dictionary per market, since published shipments, revenue and registrations require different units and aggregation. Use distinct observation, publication and forecast target dates, since the pilots include late releases and annual forecasts reviewed mid-year.

Agent-decided: retain prior reviewed snapshots and link revisions, with incomplete work clearly labeled and isolated verification fixtures. A historical replay keeps its cutoff fixed. Missing observations are explicitly pending. An Apple citation names the exact market claim, source version and cutoff eligibility. No migration or rewrite of existing vault notes is needed, consistent with PRINCIPLES.md.

## Alternatives considered

- A single rolling market note makes prior forecasts and evidence revisions difficult to recover.
- One fixed set of metrics would require unsupported values for at least one of the tested markets.
- A full second storage system would duplicate the Markdown continuation conventions already explored by the issuer and project workflows.

## Current state evidence

- Forward: obsidian-finance/skills/finance-research/SKILL.md, Select the analysis framework.
- Reverse: obsidian-finance/skills/finance-research/references/industry-and-competition.md, Completion.
- Error: research/03-smartphone-quarterly-pilot.md, Forecast carry-forward, records an unreconciled change to Q2 growth.
- Data: research/05-semiconductor-forecast-review.md and research/06-eu-car-quarter-aggregation.md distinguish observation, aggregation and availability.
- Boundary: obsidian/skills/obsidian-research-project/SKILL.md, Find the last completed state and Apply or recover an update, supply reference behavior for continuity.

## UI flows

| Case | What the user does | What they see |
|---|---|---|
| First quarter | Ask to research a market quarter | A market overview and a consistently named quarter folder with linked analysis, sources and outlook notes. |
| Missing evidence | Ask for a quarter whose material inputs are incomplete | A partial result that names what is missing and what can be resumed. |
| Resume | In a new conversation, ask to continue a market | The last valid saved progress, its source versions and the work still pending. |
| Next quarter | Ask to update the market to the next quarter | Comparable changes, a review of earlier outlook against eligible results and an updated outlook. Forecasts whose target has not been reported remain pending. |
| Revision | Ask to refresh the same quarter after a source correction | A new dated version linked to its predecessor, with affected conclusions identified. |
| Company citation | Ask Apple research to cite the market result at a cutoff | The cited market quarter, original source and version. Later data are excluded. |
