# Technical analysis research note — spec
intent: 2026-11-23-technical-analysis-research-note-quality@a587bc5
confirmed-behavior: 2026-11-23 @a4ca3b1
pre-build-review: required — this changes the public structure and evidence links of saved research notes

## Requirements

REQ-1 — Readable entry
  WHEN the user asks to save a technical analysis as a research note, the note shall open with the research question, supported conclusion, cutoff, and per-horizon revision conditions, and provide navigation to methods, detailed evidence and sources → Acceptance #1

REQ-2 — Explain the evidence
  WHEN the note presents a supported analysis, the note shall explain how the key price, volume and pattern evidence informs the outlook, describe the range-extrema calculation, and distinguish computed revision rules, eligible outside commentary, and known limits → Acceptance #2

REQ-3 — Retain reproducible evidence
  WHEN the skill saves the note, the note shall make its material claims traceable and provide working navigation and links to the original snapshot and any supported chart so the same calculation can be replayed → Acceptance #3

## Design decision

- agent-decided — Use flat research properties and put the substantive result ahead of acquisition metadata to match the readability conventions identified in the vault examples.
- agent-decided — Explain support and resistance as observed range extrema and compare an external threshold only if its source, scope and timing meet existing eligibility rules. The AAPL pilot contains a clearly labeled retrospective comparison, whose exact publication version could not be independently verified at the historical cutoff. It demonstrates presentation without relaxing the skill's historical evidence rule.
- agent-decided — Attribute the trend to the computed report's actual rule inputs. Identify volume and pattern readings as contextual evidence unless they directly drive the reported calculation. Identify any interpretive inference and its limits.
- agent-decided — Retain detailed pattern anchors and calculation provenance in the note. Save a chart when eligible observed bars exist, including when there is insufficient evidence for an outlook. This follows the existing publisher.

## Alternatives considered

- Add only research properties and a contents list. These aid navigation but leave the explanation and revision conditions dispersed.
- Reuse the AAPL sample as literal note text. Its inputs and outside evidence are specific to one snapshot.

## Current state evidence

- Forward: obsidian-finance/skills/technical-analysis/SKILL.md, Present, defines report contents and ordinary note saving.
- Reverse: obsidian-finance/skills/technical-analysis/scripts/report.py, save_report, publishes prepared note content and its original snapshot.
- Error: docs/loom/intent/2026-11-23-technical-analysis-research-note-quality.md, Problem, records the readability gap found in a fresh installed replay.
- Data: obsidian-finance/skills/technical-analysis/scripts/analyze.py, _level and _horizon, computes dated extrema from each observation window.
- Boundary: docs/loom/intent/2026-11-23-technical-analysis-research-note-quality.md, Out of scope and Deferred research, preserves analysis rules and existing vault data.

## UI flows

| Case | What the user does | What they see |
|---|---|---|
| Save with usable evidence | Ask to save an AAPL technical analysis as a research note | A note starting with the question, key conclusion and what would change each outlook, followed by the reasoning. A contents list leads to the method, dated details and sources. |
| Compare an eligible external threshold | Read a note that includes a dated external warning from an eligible source | The outside warning is attributed and distinguished from the independent level used to revise the computed outlook. |
| Partial evidence | Save a report where an eligible snapshot supports only some horizons | The note identifies the missing evidence and leaves unsupported judgments open. An ineligible or unavailable third-party perspective is omitted. |
| Review the saved note | Follow its evidence and attachment links | Navigation reaches the relevant sections and the attached original snapshot and chart, where the chart is supported. |
| Save error | Ask to save at an existing note path | The existing save protection reports the conflict and the user can choose a new path. |

The save follows the existing analysis and publication workflow. No new progress display is introduced.
