---
title: Earnings calls as supplemental equity research evidence
type: loom-research
status: concluded
created: 2026-11-22
updated: 2026-11-22
tags:
  - loom/research
---

# Earnings calls as supplemental equity research evidence

Question: Can the current quarterly research structure retain and use call transcripts, recordings, and reports as optional qualitative evidence without a new report or a new storage schema?

## Findings

- The [existing source registration](../../../obsidian-finance/skills/equity-research/templates/source-registration.md) supports a dated text or JSON payload. The [store](../../../obsidian-finance/scripts/research_store.py) captures the exact sources consumed by each work unit in the quarter, including optional sources. Use text for a transcript or permitted excerpt. A permitted original recording can be linked separately as an original artifact. The helper does not transcribe it.
- [Operating analysis](../../../obsidian-finance/skills/equity-research/references/operating-analysis.md) can use management explanations of sales mix, demand and costs, with independent checks. [Forward forecasts](../../../obsidian-finance/skills/equity-research/references/forward-forecast.md) already separate management guidance from the researcher's models. Risk and synthesis should cite material changes through the affected work rather than repeat the call. Keep filed actuals distinct from forward guidance, and an analyst question distinct from management's response.
- [Microsoft FY2024 Q3](https://www.microsoft.com/en-us/investor/events/fy-2024/earnings-fy-2024-q3) contains management's expectation of higher FY2025 capital expenditure contingent on demand and service adoption. The analyst raised a speculative investment amount. This supports a conditional assumption for forecast and valuation, not an observed expenditure or a management-confirmed amount.
- Record source format and coverage (full, excerpt, or summary), fiscal quarter, event time, verified public availability, and speaker plus section or timestamp. Preserve transcript creation or retrieval time separately when reconstructing a historical call. Compare material numeric claims against the filing, release, or recording as appropriate. The source acquisition trade-off is in [the companion study](2026-11-22-earnings-call-source-feasibility.md).

## Mechanical probe

A disposable fixture on revision 40da2c9 used a paraphrased Microsoft excerpt, a fixture fiscal identifier, the normal Markdown publication API, and a forecast work unit with no mandatory sources. The test registered the text, bound it as a consumed optional source, published a partial checkpoint, rediscovered the forecast as reusable, copied the quarter, and verified it standalone. A test-only later source version was excluded at the historical cutoff and invalidated the earlier forecast for latest mode. The fixture simulates source availability and a revision. It does not verify Microsoft's historical publication timestamp or represent a production research result.

The [assessment implementation](../../../obsidian-finance/scripts/work_assessment.py) tracks revisions of consumed inputs. Discovery does not automatically designate a previously unconsumed call as an input. The skill or analyst must discover and select it during research.

## Decision

Start by documenting how to select and cite optional call evidence in the existing method, operating and forecast guides. Keep the seven analysis outputs and source schema. Missing call material can be noted without making it a required input for every quarter. A missing source already relied upon must be addressed before reusing that analysis. No automatic collection, installed skill change, or new required data source was implemented.
