---
title: "Existing tools for daily chart pattern detection"
type: loom-research
status: complete
created: 2026-11-23
updated: 2026-11-23
change: 2026-11-23-technical-analysis-source-fallback
tags:
  - loom/research
---

# Existing tools for daily chart pattern detection

## Question and scope

Identify existing double-top and double-bottom detectors and determine whether they can provide dated price anchors, distinguish a candidate from a confirmed break, and fit the skill's local, cutoff-aware analysis.

## Method and rationale

Compared upstream function inventories, the executable detection rules for the strongest candidates, and the project's current swing detection. Source inspection can establish what the implementations return and when. Installation and detection quality need a fixture experiment if dependency adoption is proposed.

## Findings

| Tool | Evidence and implications |
|---|---|
| Stock-Pattern | The CLI uses pandas and NumPy for detection. Both double-pattern paths produce dated pivot prices and check volume at the two extrema. Its rules require the latest close to remain between the second extremum and the intermediate level, so the returned match is a pre-breakout candidate. The project is GPL-3.0. [Rule predicates](https://github.com/BennyThadikaran/stock-pattern/blob/main/src/utils.py#L208-L263) · [Double top output](https://github.com/BennyThadikaran/stock-pattern/blob/main/src/utils.py#L821-L904) · [Double bottom output](https://github.com/BennyThadikaran/stock-pattern/blob/main/src/utils.py#L795-L817) · [Project and license](https://github.com/BennyThadikaran/stock-pattern) |
| chart_patterns | The detector records indices and prices for a five-pivot sequence. The bottom branch is an `elif` after a branch that also accepts `both`, so `both` reaches only the top branch. Pivots require bars on their right. Any historical integration would need cutoff-aligned input and a test of when a pivot first becomes knowable. [Double-pattern detector](https://github.com/zeta-zetra/chart_patterns/blob/main/chart_patterns/doubles.py#L45-L81) · [Pivot implementation](https://github.com/zeta-zetra/chart_patterns/blob/main/chart_patterns/pivot_points.py#L13-L52) |
| PatternPy | Its double-pattern function labels a three-bar local shape using adjacent highs/lows and each surrounding bar's range. It has no separate dated neckline-break result and does not check that the two extrema are close to each other. This is a weaker match to the required report. [Detector source](https://github.com/keithorange/PatternPy/blob/main/tradingpatterns/tradingpatterns.py) |
| TA-Lib | Its official pattern inventory covers candlestick patterns and includes no double-top or double-bottom detector. It remains an option for candlestick analysis if that scope is added. [Function inventory](https://ta-lib.org/functions/) · [Candlestick outputs](https://ta-lib.org/api/candlestick-outputs/) |

## Evidence

Upstream source references use the inspected main branches, with commit SHAs unpinned. Local baseline is `d1987f1`. The skill already derives dated swing highs and lows from eligible data and exposes the resulting points. [Current analyzer](../../../../obsidian-finance/skills/technical-analysis/scripts/analyze.py) · [Skill interface](../../../../obsidian-finance/skills/technical-analysis/SKILL.md) · [Project license](../../../../LICENSE)

## Decision impact

Use Stock-Pattern as the first reference scanner for a bounded comparison. Its dated evidence and volume checks match much of the intended workflow. Adopting the scanner directly would still require snapshot conversion, cutoff-safe replay, a post-breakout confirmation layer, and a distribution license review. If initial scope stays at two shapes, compare it with the current swing extraction plus a minimal rule for candidate, confirmation, and invalidation. A larger set of required shapes would make adopting a library more attractive if its output and distribution terms fit.

Use the same fixtures for both candidates. Include real historical prefixes and labeled boundary cases covering candidate, confirmation, invalidation, insufficient history, and a break only after the requested cutoff. Keep third-party market commentary separate from all computed pattern results.

## Limitations and open questions

The packages were researched through source and documentation. They were not installed or run against fixtures. Runtime fit, miss/over-detection rates, and distribution terms for a chosen integration remain unverified. This record does not select a dependency or change the confirmed skill behavior.
