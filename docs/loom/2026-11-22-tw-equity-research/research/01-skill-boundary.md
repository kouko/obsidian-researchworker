---
title: "Should Taiwan and US quarterly equity research share a skill?"
type: loom-research
status: concluded
created: 2026-11-22
updated: 2026-11-22
change: 2026-11-22-tw-equity-research
tags: [loom/research]
---

# Should Taiwan and US quarterly equity research share a skill?

## Question and scope

Choose a user-facing entry for quarterly issuer research in Obsidian. The first Taiwan release covers TWSE-listed companies. Preserve existing US research and the agreed Taiwan source and completion requirements.

## Method and rationale

Compare the repository's saved research workflow and Taiwan evidence requirements against the same criteria: ease of invoking the right workflow, isolation of market-specific rules, and duplication of shared rules. Reuse prior source and transcription checks for feasibility context.

## Findings

- The existing skill shares quarterly note templates, evidence dates and revisions, retained-forecast comparison, downstream reassessment, and review criteria. It also explicitly invokes SEC acquisition, and generic-looking asset identifiers and quarter fields still need compatibility checks.
- Taiwan needs its own issuer identity, MOPS/TWSE acquisition, published monthly revenue before quarterly close, and market-specific completion criteria. Annual reports, PDF pages and investor-call materials have their own publication dates and evidence roles.
- One public skill with separate market instructions preserves one entry and limits which market rules the agent loads. Putting both markets inline exposes every run to irrelevant acquisition and completion rules. Two public skills can also share the store and methods, but require distinct triggering and a way to keep any repeated requirements aligned.

## Evidence

- [Equity research skill](../../../../obsidian-finance/skills/equity-research/SKILL.md), especially source acquisition, templates, cutoff checks and forecast comparison.
- [Research store](../../../../obsidian-finance/scripts/research_store.py), for existing asset and quarter record boundaries.
- [Taiwan intent draft](../../intent/2026-11-22-tw-equity-research.md), for monthly updates, disclosure requirements, source priorities and the first-release market.

## Decision impact

Revised recommendation: use one public equity-research entry that resolves market identity, then hands off to a complete market workflow. Keep issuer analysis, interpretation of evidence, forecasts and completion criteria market-owned. Share storage, source traceability and mechanical checks where the contracts genuinely match. Preserve known US identifiers and notes. The user expects analytical differences across markets; their extent is unverified. This narrows the earlier recommendation to share the quarterly workflow. Validate the boundary with a Taiwan monthly continuation, an ambiguous issuer request, and an existing US review.

The user subsequently preferred an independent Taiwan skill so the Taiwan instruction set can be maintained in Traditional Chinese. Recommend separate public entries under that maintenance preference. Reuse language-neutral code and data contracts where they already match. The earlier single-entry recommendation optimized invocation and remains technically viable.

## Limitations and open questions

The design has no matched implementation or triggering test. Independent invocation and continued US note compatibility still need verification. The intent remains open.
