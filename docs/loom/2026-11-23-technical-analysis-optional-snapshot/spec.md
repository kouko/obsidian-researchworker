# On-demand technical analysis snapshots — spec
intent: 2026-11-23-technical-analysis-optional-snapshot@aa4378d
confirmed-behavior: 2026-11-23 @d717f6d
pre-build-review: required — changes the public saved-note attachment contract

## Requirements

REQ-1 — Routine saved note
  WHEN the user saves a technical analysis without requesting snapshot retention, the skill shall save a note with the market-data source, capture time, analysis cutoff, price basis and a chart when eligible daily bars exist, with neither a snapshot attachment nor a snapshot link → Acceptance #1

REQ-2 — Saved note with replay data
  WHEN the user requests retention of the complete snapshot while saving a technical analysis, the skill shall link to the saved analysis input so that it opens and reproduces the computed results under the same cutoff and calculation rules → Acceptance #2

## Design decision

- agent-decided — Use an explicit retention choice in the existing save workflow so a natural-language request can select either output without persistent settings.
- agent-decided — Preserve existing direct command behavior unless its caller selects the new save mode, because existing scripts may expect an attachment.
- agent-decided — Keep the existing publish and recovery boundary so each note and its selected attachments are saved together.
- agent-decided — The existing limit on publishing when no eligible snapshot exists still applies. Existing notes and attachments remain untouched.

## Alternatives considered

- Always attach the snapshot — adds an attachment to routine notes with no exact replay requirement.
- Eliminate attachment support — removes exact replay from notes explicitly saved for that purpose.

## Current state evidence

- Forward: `obsidian-finance/skills/technical-analysis/SKILL.md`, saved research note instructions.
- Reverse: `obsidian-finance/skills/technical-analysis/scripts/report.py`, `main` calls `save_report` for normal publication.
- Error: `obsidian-finance/skills/technical-analysis/scripts/report.py`, `_attachment_links` checks prepared links and `_publish` stages the output.
- Data: `obsidian-finance/skills/technical-analysis/SKILL.md`, local input snapshot schema.
- Boundary: `obsidian-finance/skills/technical-analysis/scripts/report.py`, `save_report` chooses the files to publish.

## UI flows

| What the user asks | What they see |
| --- | --- |
| Save the technical analysis as an Obsidian note. | A note with its source details and a chart when supported. No snapshot file or snapshot link is created. The note alone cannot reproduce the exact historical calculation. |
| Save the note and keep the original market-data snapshot. | The same note and chart, with an additional link to the exact snapshot used in the calculation. |
| Save an analysis when no eligible daily data can be acquired. | The existing response explains the missing data and how to supply an eligible snapshot or retry. |
