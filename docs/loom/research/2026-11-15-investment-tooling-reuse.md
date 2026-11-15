---
title: Investment tooling reuse and bounded Apple data probe
type: loom-research
status: concluded
created: 2026-11-15
updated: 2026-11-15
tags: [loom/research]
---

# Question and conditions

Can existing Monkey Skills tooling support quarterly investment research covering at least twenty historical years? The first target is Apple; eventual recommendations cover short, medium and long horizons. Other companies will test industry differences. No holding period has been fixed.

User constraint: any reused or modified Monkey Skills tool must first be transplanted into this repository. The source repository remains read-only; no runtime dependency on its absolute paths is acceptable. A separate optional plugin, provisionally named obsidian-finance, is under consideration, not approved or implemented.

# Method and rationale

Inspected connected local source paths and selected test definitions at Monkey Skills revision c66424d387584c8ddb8c9dd109d15bfbd08b6802. Performed one bounded public-data probe, not an end-to-end pipeline test. Did not install packages or run setup. Existing source comments and historical research are leads, not independently reproduced measurements.

# Evidence

Source root: /Users/kouko/GitHub/monkey-skills/investing-toolkit/skills/.

- data-markets/scripts/pack_us.py:2460 defines quarterly-series orchestration: filing enumeration, acquisition, stitching, discrete-quarter derivation and projection. Its years parameter caps a span; it is not a historical knowledge cutoff.
- data-markets/scripts/sec_edgar_client.py:700 enumerates historical 10-K/10-Q filings, following archived submissions. summarize_concept retains start/end, accession and filed dates.
- analysis-kpi/scripts/kpi_store.py supports append-only observations and point-in-time queries. This does not prove the entire quarterly pipeline respects a requested historical cutoff.
- data-markets/scripts/fred_client.py:180 requests observations without historical-vintage parameters. Historical macro availability is unverified.
- analysis-kpi/SKILL.md documents companyfacts history limitations. Its shorthand about a 2009 floor must distinguish publication dates from earlier comparative periods.
- Existing long-horizon methods research: /Users/kouko/GitHub/monkey-skills/docs/loom/evidence/research/2026-07-19-longhorizon-equity-analysis-process-and-deliverables.md. Its citations and claims have not been revalidated here.

Probe artifacts: /private/tmp/apple-research-probe-20261115/ (temporary, not durable project evidence). First attempted Python requests access failed DNS. That attempt imported the original client's pure parsing definitions before the user stated the transplant-first constraint; no source mutation occurred. A subsequent curl request independently downloaded https://data.sec.gov/api/xbrl/companyfacts/CIK0000320193.json with HTTP success (curl exit 0), and Python standard-library JSON inspection produced coverage-summary.json. The original pipeline was not executed. Requests emitted a dependency-version warning in the existing interpreter; its pinned script environment was not validated.

Observed USD concept coverage (ranges are extrema, not proof of continuous quarterly coverage):

| Concept | Observations | Earliest period end | Latest period end | Earliest filing date |
|---|---:|---|---|---|
| SalesRevenueNet | 210 | 2007-09-29 | 2018-06-30 | 2009-07-22 |
| RevenueFromContractWithCustomerExcludingAssessedTax | 120 | 2017-09-30 | 2026-09-26 | 2019-01-30 |
| NetIncomeLoss | 341 | 2007-09-29 | 2026-09-26 | 2009-07-22 |
| Assets | 148 | 2008-09-27 | 2026-09-26 | 2009-07-22 |

SalesRevenueNet and NetIncomeLoss include start dates from 2006-10-01; those are period starts, not evidence of a report publicly available then. Counts include repeated reporting observations, not distinct quarters.

# Findings and decision impact

Reuse candidates exist for acquisition, quarter derivation, provenance and historical versions. Prefer a bounded dependency-complete transplant over rebuilding these or copying the whole toolkit. Selection and destination remain open pending plugin-boundary evaluation. Preserve attribution/licenses and useful behavior tests when transplanting; do not add permanent one-time migration machinery.

The probe does not establish twenty years of complete quarterly statements or contemporary knowledge reconstruction. Historical filings and missing-period acquisition must be evaluated separately. Do not reduce the user's twenty-year requirement to fit existing tooling.

Packaging alternatives: add finance to the current plugin (less packaging, coupled dependencies), introduce a sibling optional plugin (separate install/version/dependencies, more metadata and host verification), or defer packaging while finishing scope evaluation (no premature migration). A separate repository is not required merely to create a separate plugin.

# Limitations and open decisions

No quarterly acquisition/stitching execution, full suite, investment report, host install, vault write, migration or publication was performed. Only selected concepts were inspected; no continuous-quarter completeness, historical-vintage integration, price-adjustment semantics or older narrative extraction was verified. No claim about investment performance is supported. Plugin naming and boundaries remain proposals.
