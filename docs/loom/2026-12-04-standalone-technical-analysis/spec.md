# Standalone stock technical analysis — spec
intent: 2026-12-04-standalone-technical-analysis@ebd3301
confirmed-behavior: 2026-12-04 @f494be6
pre-build-review: required — a new skill, a network data source, and a persisted research format cross package and vault boundaries

## Requirements

REQ-1 — Single-stock price and volume analysis
  WHEN the user requests a single U.S. stock analysis, the skill shall use automatically fetched completed daily bars or supplied local data to report period return, moving averages, volume changes, and rule-based trend observations → Acceptance #1

REQ-2 — Reproducible evidence
  The skill shall identify the input snapshot, analysis cutoff, trading timezone, observed date range, price adjustment basis, and analytical settings so that reusing the same inputs reproduces the numeric results and rule classifications → Acceptance #2

REQ-3 — Data eligibility
  IF a bar is incomplete, available only after the cutoff, or unverifiable for a historical cutoff, THEN the skill shall exclude it from supported findings and identify any conclusions limited by the resulting coverage → Acceptance #3

REQ-4 — Conversation and note
  WHEN the user requests the analysis, the skill shall present the result in conversation and shall save it as a separate Obsidian note on request → Acceptance #4

REQ-5 — Three dated outlooks
  The skill shall report separate short-, medium-, and long-term technical evidence and conclusions, each with its stated length, actual observed start and end dates, explicit forward outlook start and end dates, and an evidence-gap explanation where a conclusion is unsupported → Acceptance #5

## Design decision

- agent-decided — Resolve the completed exchange sessions and validate source metadata at the acquisition boundary. Run indicators and chart rules offline on eligible bars. This permits local replay and isolates provider dependencies.
- agent-decided — Evaluate TA-Lib against the existing monkey-skills fixtures before selecting it for standard indicators. Fix the supported formulas and settings and keep pattern confirmation rules explicit so results can be inspected without relying on narrative generation.
- agent-decided — Default to outlook lengths of three calendar weeks, three calendar months, and one calendar year, within the previously discussed scales. Start each window the calendar day after the cutoff in the listing timezone and include dates through the cutoff date plus its duration, clamping month-end dates when necessary. Calendar dates keep forecast coverage legible across weekends and holidays. State actual historical evidence ranges separately, including when coverage is shorter.
- agent-decided — Use completed daily bars and aggregate complete exchange weeks for long-term structure where coverage supports it. Allow extra history for indicator calculation beyond the observation window and report the range actually used.
- agent-decided — Present scenario evidence and revision conditions per horizon, with a marked price and volume chart when saving the supported analysis. Explicitly disclose missing data without inventing price targets or conflating conditional outlooks with predicted outcomes.
- agent-decided — Keep existing vault notes outside this change and create a separate note at the user's requested destination. A conflicting destination needs a new available filename or an explicit user choice.

## Alternatives considered

- Offline-only release — leaves routine single-ticker use dependent on manual exports.
- One overall score — hides disagreements between the three horizons.
- Treat every latest download as usable for historical replay — collection after the cutoff cannot establish what was available then.

## Current state evidence

- Forward: obsidian-finance/skills/equity-research/SKILL.md, Establish the boundary, starts analysis in an identified quarterly research context.
- Reverse: obsidian-finance/skills/equity-research/SKILL.md, analytical framework table, links price analysis from quarterly research.
- Error: obsidian-finance/skills/equity-research/references/technical-analysis.md, Completion, keeps insufficient-input work pending.
- Data: obsidian-finance/skills/equity-research/templates/technical-analysis.md, frontmatter, binds the existing note to a fiscal quarter and review identifier.
- Boundary: PRINCIPLES.md, Non-negotiables, preserves existing user data and limits advertised capability to supported behavior.

## UI flows

| Case | What the user does | What they see |
|---|---|---|
| Latest analysis | Request technical analysis for a single U.S. ticker | A report based on completed daily sessions, with key technical evidence and dated outlooks for all three horizons |
| Historical or local analysis | Supply a local snapshot, and a historical cutoff when applicable | The same report format using eligible data, with the observed period and forward dates shown separately |
| Missing inputs | Request a horizon with incomplete coverage, or fetch when the provider or dependency is unavailable | A clear gap on affected results, with local data or isolated setup instructions offered as applicable |
| Save | Ask to save the analysis to Obsidian | A separate note with the three dated conclusions, evidence, and chart when data supports it |
| Typical edge case | Use a cutoff during a session or during an incomplete trading week | The report uses completed periods, identifies the last included period, and retains any affected horizon with an explicit limitation |
