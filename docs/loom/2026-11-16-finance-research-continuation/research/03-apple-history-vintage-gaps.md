---
title: Apple cached facts cannot establish twenty-year original-vintage research
type: loom-research
status: concluded
created: 2026-11-16
updated: 2026-11-16
tags: [loom/research]
change: 2026-11-16-finance-research-continuation
---

# Apple history input coverage and vintage gaps

## Question and scope

Does the existing Apple companyfacts cache establish the original financial
inputs needed for at least twenty years of historical quarterly research?
This is a bounded cache audit, not a complete SEC/archive inventory or Stage E
completion. No new network request, permanent data tool or research generation
was executed. The existing twenty-year outcome remains unchanged.

## Method and rationale

Inspect exact row endpoints, filing dates and accession provenance from three
relevant USD concepts in the already acquired raw cache. A comparative period
reported in a later filing cannot prove availability at the earlier cutoff.
Count cached observations only as observations, not complete fiscal quarters.

## Findings

| Concept | Cached USD rows | Earliest period end | Earliest filing date | Latest period end |
|---|---:|---|---|---|
| NetIncomeLoss | 341 | 2007-09-29 | 2009-07-22 | 2026-09-26 |
| SalesRevenueNet | 210 | 2007-09-29 | 2009-07-22 | 2018-06-30 |
| RevenueFromContractWithCustomerExcludingAssessedTax | 120 | 2017-09-30 | 2019-01-30 | 2026-09-26 |

The earliest-filing NetIncomeLoss and SalesRevenueNet examples inspected have
2008-06-28 endpoints but accession `0001193125-09-153165`, filed 2009-07-22.
The newer revenue concept's earliest-filing example has 2017-12-30 endpoint but
accession `0000320193-19-000010`, filed 2019-01-30. Such rows may be useful
comparison evidence for the later assessment, not original eligible inputs for
the earlier historical judgment. A single current revenue tag also does not
span all old accounting/reporting definitions.

## Evidence

Inspected cache:
`/private/tmp/apple-stage-a-q3/sec-run-05erqm5p/raw/companyfacts.json`.
Issuer metadata: CIK 320193, Apple Inc. SHA256:
`f085735b4d08fb116ade18d24247ffabe11df8eb52eae6556b165831f15ef1ad`.

The local Python audit selected each concept's `units.USD` array, printed its
length, min/max `end`, min `filed`, then the first two rows sorted by
`(filed,end)` with `start,end,accn,form,filed`. The retained table/examples above
are the compact observed output; no value was inferred from `fy/fp` alone.
The cache is a previously acquired current inventory, not a historical snapshot
certified at every old date. Its full contents include later observations.

## Decision impact

Agent-decided — do not bulk-fill old quarterly notes from these comparative
rows or one revenue tag. Obtain the original period's filing/release and exact
original tables, preserving accounting definitions and source publication.
Before fixing the exact twenty-year endpoint, verify the latest complete
company-declared fiscal year and enumerate all expected quarters; a proposed
twenty-year range is not an availability or completion claim.

Older documents may require different extraction from current inline-XBRL;
that capability is not established by this cache. Manual original-source
research is a viable bounded alternative to adding a generalized parser.
Choose new maintained extraction work only for a demonstrated repeated gap,
through its owning software station. Keep quarterly dates source-declared and
do not assume fixed calendar months or subtract EPS/average shares.

## Limitations and open questions

No original old filing was acquired or fully read in this audit. No conclusion
about the entire SEC archive, all tags, all annual/quarterly dates or uniform
historical availability follows. The table establishes a concrete insufficiency
of the selected cached inputs, not a universal absence of usable old records.
Stage E still needs original sources and substantive period analysis for every
expected quarter; a cache, ledger or successful downloader is insufficient.
