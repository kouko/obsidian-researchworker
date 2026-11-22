# Stable equity quarterly notes — spec
intent: 2026-11-22-equity-quarterly-notes@7824c3c
confirmed-behavior: 2026-11-22 @5560a0d
pre-build-review: required — Updating multiple existing notes in place requires interrupted-write recovery and edit-conflict handling.

## Requirements

REQ-1 — Stable quarterly notes
  WHEN a company fiscal quarter is researched or continued, the equity research workflow shall use one stable path for each saved report role in that quarter and link the existing reports from the quarterly overview → Acceptance #1

REQ-2 — Stable English filenames
  WHEN a quarterly report is created, the workflow shall name it using the fiscal quarter, ticker, company display name and numbered English report label, and retain that path across changes in writing language or display name → Acceptance #2

REQ-3 — Traceable revisions
  WHEN newer eligible evidence materially changes a saved conclusion, the workflow shall retain the previous conclusion, its source references and cutoff, and the reason for the change in the same report → Acceptance #3

REQ-4 — Cutoff-aware continuation
  WHEN a historical or later-quarter study reads existing research, the workflow shall distinguish current and dated prior conclusions, reuse only evidence eligible at the requested cutoff, and report any gap that prevents reconstruction → Acceptance #3

REQ-5 — Safe updates
  IF publication is interrupted or an affected note has changed since the workflow read it, the workflow shall preserve existing edits and make any incomplete publication detectable without presenting it as complete → Acceptance #4

## Design decision

- user-decided — Use one fixed set per company fiscal quarter and retain important revisions inside the affected report. Old-format compatibility is outside this change.
- user-decided — Use fixed English report labels and localizable titles and bodies. The filename pattern is `YYYYQq <TICKER> <Company> - <NN> <English Label>.md`.
- agent-decided — Place the overview and reports directly in `cycles/<YYYYQq>/`. Use the overview for links and saved progress. Keep evidence under that quarter's `data/` and retain consumed source versions.
- agent-decided — Reuse the existing quarter's saved paths for its report roles to preserve links. On creation, sanitize filesystem-unsafe filename components and refuse ambiguous paths or occupied destinations. Identify notes by fiscal quarter, asset ID and role in their Markdown properties.
- agent-decided — Preserve unowned and old-format files in place. Do not treat them as completed new-format research. Historical requests that cannot be answered from available dated evidence must report the gap.
- agent-decided — Protect editable notes by checking for changes since reading them. Assess recovery requirements against the industry workflow before choosing which existing mechanisms to reuse. Keep the SEC acquisition entry and the analytical dependencies intact.

## Alternatives considered

- Keep timestamped report sets and rename their files. Duplicate quarterly reports and changing links would remain.
- Use localized filenames. A fixed English label avoids a separate filename vocabulary for each language.
- Migrate or maintain a legacy reader. The user excluded compatibility and data migration from the scope.

## Current state evidence

- Forward: `obsidian-finance/scripts/research_store.py`, `_target` and `_publish_markdown`, place reports under dated run directories and restrict filenames.
- Reverse: `obsidian-finance/skills/equity-research/SKILL.md`, Isolated Markdown pilot and Quarter-owned evidence, document fixed review files and the current source layout.
- Error: `obsidian-finance/scripts/research_store.py`, `_publish_markdown`, checks staged files and publication collisions.
- Data: `obsidian-finance/skills/equity-research/templates/` defines the existing typed Markdown roles.
- Boundary: `docs/loom/2026-11-21-finance-industry-market-research/acceptance-test-report.md`, Acceptance 5, documents verified same-quarter in-place revisions in industry research.

## UI flows

Open or continue a quarter → See one quarterly overview and up to seven analysis notes using fixed filenames. For Apple FY2024Q3 the ordered filenames use the prefix `2024Q3 AAPL Apple - ` and these suffixes:

| Number | English label |
| --- | --- |
| 00 | Research Overview |
| 01 | Financial Analysis |
| 02 | Operating Analysis |
| 03 | Industry and Competition |
| 04 | Forward Forecast |
| 05 | Valuation and Risk |
| 06 | Technical Analysis |
| 99 | Investment Synthesis |

Continue the same quarter in another language → Existing note paths are reused. Note titles and prose can use the chosen language.

Update a material finding → Open the same report to see the latest finding and the dated revision history.

Request an earlier cutoff → See conclusions supported by evidence available at that time, or an explicit gap when the saved evidence is insufficient.

Continue into the next fiscal quarter → See a separate set of notes and quarter-owned evidence.

Encounter a conflicting edit or interrupted save → See the affected work flagged, with the existing edits and recoverable research preserved.
