---
title: "Historical replay of chart pattern tools"
type: loom-research
status: complete
created: 2026-11-23
updated: 2026-11-23
change: 2026-11-23-technical-analysis-source-fallback
tags:
  - loom/research
---

# Historical replay of chart pattern tools

## Question and scope

Compare the four candidates in [the source study](01-chart-pattern-tools.md) on matched daily price and volume. Measure signal coverage, what was knowable on each bar date, and whether the detector distinguishes a candidate from confirmation and invalidation. Detection accuracy and predictive power require a labeled test set and are outside this pilot.

## Method and rationale

Use two Yahoo Finance adjusted daily snapshots, AAPL and MSFT. Both contain 501 bars with no missing completed sessions in the fetch metadata. The pilot takes the last 250 bars per ticker (2025-11-24 to 2026-11-20), and tests the last 126 cutoff dates per ticker (2026-05-26 to 2026-11-20). Every daily run sees only the prefix from the same start date. Use default detector parameters and compare date-indexed outputs with a one-pass run on the 250 bars where the API emits historical labels. Test the Stock-Pattern predicates at controlled prices before and after the relevant price levels.

The snapshots were captured on 2026-11-22, at 17:01:57.991391 UTC for AAPL and 17:32:55.194127 UTC for MSFT. Truncation tests rule dependence on later bars within this exact data version. It cannot establish the historical availability of this adjusted data version.

## Findings

| Tool | AAPL | MSFT | Interpretation |
|---|---:|---:|---|
| Stock-Pattern | 0 candidate dates | 0 candidate dates | Neither direction triggered on the 252 cutoffs with default settings. Controlled top and bottom candidates return true, then return false after either confirmation or invalidation. The detector does not emit those two outcomes separately. |
| chart_patterns, bottoms mode | 4 batch and 4 cutoff dates, 0 disagreements | 4 batch and 4 cutoff dates, 4 disagreements | MSFT shows how aggregate counts hide changed dates. Batch-only labels on Aug 10–11, replay-only labels on Oct 8–9. Both detect Oct 6–7. |
| chart_patterns, tops and both modes | 0 dates | 0 dates | Both mode missed all eight bottom labels found by the explicit bottoms runs. |
| PatternPy | 35 batch labels, 0 on the cutoff bar | 35 batch labels, 0 on the cutoff bar | Every historical label was unavailable on its own bar date. The implementation explicitly needs the next bar. An adapter could date availability later, but the label still describes a local three-bar shape. |
| TA-Lib | 102 dates with at least one candlestick signal | 96 dates with at least one candlestick signal | All 15,372 per-function date comparisons matched between batch and prefix across both symbols. These are candlestick patterns. The tested function inventory has no double-top or double-bottom detector. |

For example, the MSFT run labels Aug 10 as a double bottom when the full series is present. Its final local turning point is dated Aug 10 itself. The pivot routine requires three bars to its right, so that particular evidence cannot be available as of Aug 10. The Aug 10 prefix did not emit that label.

PatternPy failed with pandas 3.1.1 because it assigns text into a floating-point result column. The comparison completed in the isolated environment with pandas 2.2.2. The chart_patterns repository requires its expected package name in nested imports. The harness provided the namespace without modifying upstream source. The test calls the detectors directly and does not exercise their graphical, CLI, or output packaging workflows.

## Evidence

- Upstream pins: [Stock-Pattern](https://github.com/BennyThadikaran/stock-pattern/tree/85c710daa5809f8f85c9e6f3f98ceea200317566), [chart_patterns](https://github.com/zeta-zetra/chart_patterns/tree/44f8baa3b15dfa6b9d54b51d2307c85a255d3a40), [PatternPy](https://github.com/keithorange/PatternPy/tree/2b1f29b17986acafffeb32c83e772417d540c100). TA-Lib Python 0.8.3, Python 3.12.11, pandas 2.2.2.
- Raw runs, output and checks are in the isolated directory `/private/tmp/chart-pattern-pilot-20261123`. Run `PYTHONWARNINGS=ignore env/bin/python replay.py /private/tmp/ta-dogfood.hB2xBT/direct-live.json msft.json > results.json` followed by `env/bin/python audit.py` from that directory.
- `results.json` contains each of the 252 daily results with batch and prefix outcomes. `audit.py` independently compares all 61 TA-Lib candlestick outputs and verifies the Stock-Pattern predicate boundaries.

## Decision impact

Use Stock-Pattern as a candidate reference, not as the shipped detector based on this evidence. For the initial double-top/bottom scope, prototype the report's needed candidate, confirmation, and invalidation rules over the existing swing points and compare with pinned Stock-Pattern on independently labeled cases. This keeps cutoff tests and evidence dates under the same snapshot validation and avoids adding pandas to the local report path for an unproven gain. If candlestick patterns become a separate requirement, TA-Lib is a viable candidate for a dedicated evaluation.

## Limitations and open questions

Two stocks over one period do not establish true positives or false negatives. Zero Stock-Pattern candidates may reflect history, detector selection rules, or both. PatternPy's 70 retrospective labels do not establish its accuracy. A reliability study requires independently labeled positive and negative shapes, dates for the earliest knowable confirmation, gap cases, and a holdout across more instruments and periods. Investment or forward-return performance was not measured. No skill or implementation-plan files were edited for this experiment.
