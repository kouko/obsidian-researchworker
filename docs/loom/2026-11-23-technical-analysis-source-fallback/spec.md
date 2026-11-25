# Stock technical analysis data availability — spec
intent: 2026-11-23-technical-analysis-source-fallback@9bb6541
confirmed-behavior: 2026-11-23 @b8ab1f4
pre-build-review: required — cutoff-sensitive pattern decisions and third-party evidence affect the skill's public analysis contract

## Requirements

REQ-1 — Reproducible current analysis
  WHEN current acquisition succeeds, the skill shall report short-, medium-, and long-term results with values, dates, and conclusions reproducible from the same identified snapshot used for the report → Acceptance #1

REQ-2 — Eligible local data
  WHEN current acquisition is unavailable and an eligible local snapshot is available, the skill shall report the results supported by that snapshot and identify its version and the analysis cutoff → Acceptance #2

REQ-3 — Explicit lack of evidence
  WHEN no eligible snapshot is available, the skill shall state the observable reason, mark all three horizons as having insufficient data, and leave unsupported values and directions unset → Acceptance #3

REQ-4 — Separately attributed external perspectives
  WHEN computed analysis is available and a verifiable relevant external technical perspective exists, the skill shall place that attributed perspective after the computed results, with its applicable date or period, without changing computed metrics, directions, revision conditions, or evidence gaps, and with historical commentary restricted to publications verifiably available by the requested cutoff → Acceptance #4

REQ-5 — Reproducible chart patterns
  WHEN a horizon has eligible price and volume history, the skill shall evaluate double tops and bottoms, head-and-shoulders tops and bottoms, rectangular ranges, and ascending, descending, and symmetrical triangles, showing dated price anchors and confirmation or invalidation conditions for identified patterns and distinguishing no match from insufficient evidence → Acceptance #5

## Design decision

- agent-decided — Keep one snapshot and the existing report calculation path for every supported conclusion because the captured version, cutoff, price adjustment, and calculation must be reproducible together.
- agent-decided — Use the existing eligibility rules for local data and keep the requested historical cutoff intact because a newer snapshot does not establish what was available then.
- agent-decided — Tie a failure explanation to the actual acquisition or input evidence because the clean-session dogfood claimed a write restriction without attempting acquisition.
- user-decided — Complete the analysis from its eligible snapshot first, then attach a clearly attributed external perspective. Treat differences as commentary. The perspective cannot supply missing values, alter a direction, confirm a computed pattern, or change a revision condition.
- agent-decided — Track whether dated pattern anchors and a subsequent qualifying close are known by the cutoff because retrospective labeling can assign a signal before its last turning point is confirmed. Preserve distinct candidate, confirmed, invalidated, no-match, and insufficient-data results as applicable.
- agent-decided — Evaluate the agreed families against common historical fixtures before choosing a detector. Do not infer confirmation from an upstream candidate label.

## Alternatives considered

- Assemble a result from individual web quotes and published averages. Their source versions, adjustment basis, and observation dates may differ.
- Stop after a download failure even when the user has a usable local snapshot. This would discard supported conclusions that the existing report path can reproduce.

## Current state evidence

- Forward: obsidian-finance/skills/technical-analysis/SKILL.md, Choose the data, starts latest and local analysis.
- Reverse: docs/skill-dogfood/2026-11-23-technical-analysis/report.md, Finding 1, shows fresh Codex loading the installed skill from a plain AAPL request.
- Error: docs/skill-dogfood/2026-11-23-technical-analysis/report.md, Finding 1, records cache and network failures and the substitute web-based response.
- Data: obsidian-finance/skills/technical-analysis/SKILL.md, Choose the data, documents snapshot metadata, exact cutoff, and completed bars.
- Boundary: docs/loom/intent/2026-11-23-technical-analysis-source-fallback.md, Out of scope, excludes holiday-week analysis and routing changes.
- Pattern evidence: research/02-chart-pattern-historical-replay.md, Findings, demonstrates retrospective labels with evidence unavailable on the labeled date.

## UI flows

| Case | What the user does | What they see |
|---|---|---|
| Current data available | Ask for short-, medium-, and long-term AAPL technical analysis | Three outlooks tied to one identified snapshot and cutoff. The observation dates and forecast dates are shown separately. |
| Current data unavailable, local snapshot eligible | Ask for analysis and supply an eligible local snapshot | The reply says it used local data, gives the snapshot version and cutoff, and marks any horizon that the available data cannot support. |
| Data unavailable | Ask for analysis when there is no eligible snapshot | The reply gives the observed reason, marks each horizon as having insufficient data, and says the user can supply an eligible local snapshot or retry acquisition. |
| Retry with new evidence | Supply a local snapshot or retry the request after an acquisition failure | The supplied or newly acquired data is validated against the requested cutoff before any supported result is shown. |
| Chart pattern present | Ask for a supported horizon with an identifiable pattern | The report names the pattern, shows the dates and prices that define it, and states whether the evidence supports only a candidate, a confirmed break, or an invalidated formation. |
| Chart pattern absent or unassessable | Ask for a horizon with sufficient history but no match, or history that cannot support detection | The report says no supported pattern matched or explains why the available data cannot determine the result. |
| External perspective available | Receive computed results with relevant, verifiable external commentary | The commentary follows the computed report and identifies its source and dates. A disagreement is attributed to the source and does not change the computed result. |
| External perspective unavailable | Receive computed results with no verifiable relevant commentary | The computed report is delivered on its own. A historical request excludes later or undated commentary. |

There is no new interface or progress display for acquisition. Existing conversation and optional note behavior applies where a report can be produced.
