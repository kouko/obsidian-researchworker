---
title: "Official Anthropic and OpenAI skills relevant to industry research"
type: loom-research
status: concluded
created: 2026-11-21
updated: 2026-11-21
tags: [loom/research]
change: 2026-11-21-finance-industry-market-research
---

# Official Anthropic and OpenAI skills relevant to industry research

## Question and scope

Identify first-party workflows that could inform the proposed independent,
repeatable market study. This supplements
[the public methods comparison](01-industry-market-research-methods.md).
The review inspected official public instructions and inventories without
installation or execution.

## Evidence and findings

- Anthropic's [Market Researcher agent](https://github.com/anthropics/financial-services/blob/main/plugins/agent-plugins/market-researcher/agents/market-researcher.md)
  orchestrates a sector or thematic primer, competitive landscape, trading
  comparables and an ideas shortlist. Its stock-investment path calls for
  CapIQ or FactSet for comparable multiples and human review at two points.
  [Sector Overview](https://github.com/anthropics/financial-services/blob/main/plugins/agent-plugins/market-researcher/skills/sector-overview/SKILL.md)
  covers scope, sizing, segmentation, value chain, entry barriers, drivers,
  competitive positioning, valuation and implications.
  [Competitive Analysis](https://github.com/anthropics/financial-services/blob/main/plugins/agent-plugins/market-researcher/skills/competitive-analysis/SKILL.md)
  starts with a consistently applied set of industry-specific metrics.
- OpenAI's [Market Sizing](https://github.com/openai/plugins/blob/main/plugins/data-analytics/skills/market-sizing/SKILL.md)
  defines scope and units, selects aggregate or unit-based estimation, traces
  inputs and formulas, separates facts from assumptions and states ranges,
  sensitivity and validation priorities. This is a directly relevant skill for
  an estimate with incomplete observed data.
- OpenAI's [Public Equity Investing inventory](https://github.com/openai/plugins/blob/main/plugins/public-equity-investing/README.md)
  documents an internal sector context playbook for KPIs, source hierarchy and
  modeling conventions. Listed-equity workflows use that context within
  their own deliverables. This inventory did not show a standalone,
  recurring market study equivalent to the proposed Markdown workflow.

## Decision impact

Use Anthropic's scope, market structure and competitive questions as
the analytical reference. Use OpenAI's market-sizing procedure when the
research needs to estimate a missing quantity. When a comparable observed
series exists, record and validate it directly. Keep stock screening and
valuation conditional on the research question. For cross-session updating and
issuer citations, retain the existing project standard for cutoff eligibility,
versioned evidence, saved Markdown progress and unresolved questions.

## Limitations

This compares written first-party workflows, not runtime output quality.
It does not establish absence across private or enterprise-only catalogs,
nor validate vendor data entitlements. The analyzed references do not
document the combination of historical source-version selection and
Obsidian continuation required here.
