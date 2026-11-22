# Stock technical analysis data availability — spec
intent: 2026-11-23-technical-analysis-source-fallback@ecd1d87
confirmed-behavior: 2026-11-23 @f0c5833
pre-build-review: required — the installed skill's public analysis contract governs support for financial conclusions when acquisition fails

## Requirements

REQ-1 — Reproducible current analysis
  WHEN current acquisition succeeds, the skill shall report short-, medium-, and long-term results with values, dates, and conclusions reproducible from the same identified snapshot used for the report → Acceptance #1

REQ-2 — Eligible local data
  WHEN current acquisition is unavailable and an eligible local snapshot is available, the skill shall report the results supported by that snapshot and identify its version and the analysis cutoff → Acceptance #2

REQ-3 — Explicit lack of evidence
  WHEN no eligible snapshot is available, the skill shall state the observable reason, mark all three horizons as having insufficient data, and leave unsupported values and directions unset → Acceptance #3

## Design decision

- agent-decided — Keep one snapshot and the existing report calculation path for every supported conclusion because the captured version, cutoff, price adjustment, and calculation must be reproducible together.
- agent-decided — Use the existing eligibility rules for local data and keep the requested historical cutoff intact because a newer snapshot does not establish what was available then.
- agent-decided — Tie a failure explanation to the actual acquisition or input evidence because the clean-session dogfood claimed a write restriction without attempting acquisition.

## Alternatives considered

- Assemble a result from individual web quotes and published averages. Their source versions, adjustment basis, and observation dates may differ.
- Stop after a download failure even when the user has a usable local snapshot. This would discard supported conclusions that the existing report path can reproduce.

## Current state evidence

- Forward: obsidian-finance/skills/technical-analysis/SKILL.md, Choose the data, starts latest and local analysis.
- Reverse: docs/skill-dogfood/2026-11-23-technical-analysis/report.md, Finding 1, shows fresh Codex loading the installed skill from a plain AAPL request.
- Error: docs/skill-dogfood/2026-11-23-technical-analysis/report.md, Finding 1, records cache and network failures and the substitute web-based response.
- Data: obsidian-finance/skills/technical-analysis/SKILL.md, Choose the data, documents snapshot metadata, exact cutoff, and completed bars.
- Boundary: docs/loom/intent/2026-11-23-technical-analysis-source-fallback.md, Out of scope, excludes holiday-week analysis and routing changes.

## UI flows

| Case | What the user does | What they see |
|---|---|---|
| Current data available | Ask for short-, medium-, and long-term AAPL technical analysis | Three outlooks tied to one identified snapshot and cutoff. The observation dates and forecast dates are shown separately. |
| Current data unavailable, local snapshot eligible | Ask for analysis and supply an eligible local snapshot | The reply says it used local data, gives the snapshot version and cutoff, and marks any horizon that the available data cannot support. |
| Data unavailable | Ask for analysis when there is no eligible snapshot | The reply gives the observed reason, marks each horizon as having insufficient data, and says the user can supply an eligible local snapshot or retry acquisition. |
| Retry with new evidence | Supply a local snapshot or retry the request after an acquisition failure | The supplied or newly acquired data is validated against the requested cutoff before any supported result is shown. |

There is no new interface or progress display for acquisition. Existing conversation and optional note behavior applies where a report can be produced.
