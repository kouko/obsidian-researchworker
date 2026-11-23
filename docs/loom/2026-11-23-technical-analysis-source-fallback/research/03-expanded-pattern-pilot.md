---
title: "Expanded daily chart pattern pilot"
type: loom-research
status: complete
created: 2026-11-23
updated: 2026-11-23
change: 2026-11-23-technical-analysis-source-fallback
tags:
  - loom/research
---

# Expanded daily chart pattern pilot

## Question and scope

Assess whether tools considered in the [prior historical replay](02-chart-pattern-historical-replay.md) cover the agreed first set of chart patterns, with interpretable dated points and cutoff-safe candidate or confirmation outcomes.

## Method and rationale

Reuse the fixed source revisions and AAPL/MSFT daily bars from the prior pilot. Sample every tenth session across the previous 126 cutoff dates and include the last date, giving 14 cutoffs per ticker. Compare Stock-Pattern's direct head-and-shoulders and triangle detectors, chart_patterns batch and prefix labels, and PatternPy's head, triangle and channel labels. Flag channel labels separately because the detector tests rising and falling channels.

Obtain separate Yahoo unadjusted daily downloads for three published chart examples. Compare raw pivots or detector results to the author's description. This is an exploratory cross-check against independent illustrative annotations. It does not estimate population accuracy or demonstrate historical availability of today's file versions.

## Findings

| Source-annotated example | Observed replay or check |
|---|---|
| Ford double top (1998–1999) | Stock-Pattern returned no double-top candidate on the available trading days from April through June 1999. The independent example describes a December 1998 peak, a second peak in 1999 and a later support break. This is a disagreement with the default scanner, not an estimate of its miss rate. [ChartSchool](https://chartschool.stockcharts.com/table-of-contents/chart-analysis/chart-patterns/double-top-reversal) |
| AT&T inverse head and shoulders (1998) | Stock-Pattern labeled 12 cutoff days between Aug 18 and Sep 8, all with the same five points. Its left shoulder was Apr 27 and head May 15. The published example places the left shoulder after late June, so these hits cannot be counted as reproducing the annotated shape. [ChartSchool](https://chartschool.stockcharts.com/table-of-contents/chart-analysis/chart-patterns/head-and-shoulders-bottom) |
| Micron rectangle (1999–2000) | The published near-30/40 range has multiple matching pivot dates. Within one dollar of 30, the lows were Oct 19 (30.03125), Dec 10 (29.25) and Jan 31 (29.125). Within one dollar of 40, highs were Nov 10 (39.96875) and Jan 14 (39.1875). After Feb 15 the first close above 40 was Feb 29 at 48, with 45,132,000 volume. This verifies the criterion against published levels, not automated box search. [ChartSchool](https://chartschool.stockcharts.com/table-of-contents/chart-analysis/chart-patterns/rectangle) |
| Triangle | The source defines dated converging boundaries and a separate confirming break. An independently annotated triangle matched to row-level historical data was not run in this pilot. [ChartSchool](https://chartschool.stockcharts.com/table-of-contents/chart-analysis/chart-patterns/symmetrical-triangle) |

Across the 28 AAPL/MSFT cutoffs, Stock-Pattern returned no head-and-shoulders or triangle hits. PatternPy returned zero head-and-shoulders labels and 11 triangle labels. Its 11 rising or falling channel labels do not count as rectangles. The completed chart_patterns head and triangle modes returned zero labels at those cutoffs. Its MSFT symmetrical triangle batch aborted when assigning an array into a table cell (`ValueError: Must have equal len keys and value when setting with an iterable`), so that mode has no MSFT coverage result.

## Evidence

- Pilot directory: `/private/tmp/chart-pattern-pilot-20261123`. `expanded.py` runs the 28 sampled cutoffs from the two snapshots. `F-reference.csv`, `MU-reference.csv`, and `T-reference.csv` preserve the downloaded daily data.
- Run `PYTHONWARNINGS=ignore env/bin/python expanded.py /private/tmp/ta-dogfood.hB2xBT/direct-live.json msft.json > expanded-results.json` in that directory. The environment used pandas 2.2.2 and SciPy 1.18.1. The JSON distinguishes a completed zero-label run from an exception.
- Reproduce the case checks with the pinned Stock-Pattern revision in the [prior replay](02-chart-pattern-historical-replay.md). Call `get_max_min` on each prefix and `find_double_top` for Ford (1999-04-01 through 1999-06-30) or `find_reverse_hns` for AT&T (1998-08-01 through 1999-01-31). For Micron, compute pivots from 1999-09-01 to 2000-02-15 and scan later closes against the published resistance.

## Decision impact

The stock-pattern candidates can inform comparison, but the published examples demonstrate why a date-level label must be compared by its anchor points. Retain all agreed families in the specification. Use the same dated evidence and close-confirmation contract for all of them. Keep oscillator-like K-line detectors and rising/falling channel labels out of rectangle acceptance. Require independent annotated examples for the chosen detector before adoption, including each triangle subtype.

## Limitations and open questions

The published examples are illustrative and selected after the event. Cutoff-safe approximation tests cannot reconstruct the original publisher's data version, and fixed support/resistance supplied from the article do not prove automatic detection. Detection accuracy, breakout performance, and a larger holdout remain unmeasured.
