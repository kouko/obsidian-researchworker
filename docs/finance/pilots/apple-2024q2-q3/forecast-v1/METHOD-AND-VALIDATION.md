# Q2 operating forecast and update examples

Status: bounded research fixture. User authorized a Q2 operating-evidence
supplement, update-decision fields/examples, and an applicability conclusion.
No runtime feature, general schema, actual vault write, publication or merge.
Original Stage A and valuation-v1 notes remain unchanged.

## Work and acceptance

1. Inspect cutoff-eligible reported product/region/margin evidence and dated
   management-outlook reports; separate primary, secondary and local assumptions.
2. Use an original prior-year June filing as the seasonal base, not a future
   filing's comparative column; calculate conditional next-quarter results.
3. Reconcile product, region, margin and earnings assumptions, without inventing
   standalone product forecasts or a long-horizon growth forecast.
4. Save dependency/completeness/work-state fields and explicit update examples
   for historical and latest modes, including missing sources and interruption.
5. Independently recompute arithmetic and verify provenance, cutoff and document
   links; distinguish checked examples from an implemented update engine.

## Sources and limits

sources.json records URLs, publication dates, roles and inspected locations.
Q2 original 10-Q was inspected via its public SEC page and the cached raw HTML.
The raw SHA256 identifies fetched bytes; no archived 2024 vendor snapshot is
claimed. The prior June base uses the original 2023Q3 filing, accession
0000320193-23-000077, filed 2023-08-04. Products and regions were manually
transcribed from the original SEC page and reconciled to companyfacts totals.
No 2024Q3 result or later product outcome enters this forecast.

The May 2 management outlook is a secondary report of the call, not a directly
verified issuer transcript/audio. Dated MacDailyNews live notes supplied the
qualitative revenue directions and gross-margin range; Axios corroborated the
revenue direction. Current HTML does not establish an immutable 2024 snapshot.
MarketBeat returned 403; it was not used as a read source. Apple's own release
confirms the call date and short replay window, buyback authorization and
dividend, but not the entire numeric outlook. No paid/authenticated transcript,
LSEG feed, analyst-consensus or proprietary forecast was acquired.

Date-only sources are used for an EOD cutoff; intraday publication availability
is not certified. Retrieval and authorship occurred in 2026. This is a
retrospective illustrative reconstruction, not a blind point-in-time backtest.
The word 'guidance' here refers only to attributed management outlook. It does
not turn qualitative phrases into precise endpoints or local numeric choices.

## Formula register

All financial calculations below use USD millions and unrounded ratios.

```
revenue = prior June revenue * (1 + selected total growth)
services = prior June services * (1 + selected service growth)
iPad = prior June iPad * (1 + selected iPad growth)
other categories required = revenue - services - iPad
other category growth = other categories required / prior other categories - 1
gross profit = revenue * selected total gross margin
operating income = gross profit - Q2 reported operating expenses
conditional NI = (operating income + assumed other income of zero)
                 * (1 - Q2 reported tax / Q2 reported pretax income)
required product gross margin = (gross profit - services * assumed service GM)
                                / (revenue - services)
China revenue = prior June China * (1 + selected China growth)
other regions required = revenue - China revenue
other region growth = other regions required / prior June other regions - 1
next TTM NI = Q2 TTM NI - prior June NI + conditional June NI
next TTM change = next TTM NI / Q2 TTM NI - 1
```

Top-line scenarios use 2/3/4% growth, selected points rather than a definition or
full range of management's low-single-digit phrase. Double-digit category growth
does not specify a distribution; 10/14/18% services and 10/15/25% iPad are local
coordinates. China -10/-5/0% is an uncalibrated risk check, not company guidance.
The middle coordinate is not 'base case'. No scenario probabilities are given.
These three scenarios do not bound possible loss, revenue or earnings outcomes.

Operating expenses and effective tax are deliberately simple carry-forwards,
not validated forecasts; other income is a zero assumption, not missing data
silently coerced to zero. No cash-flow model, net-cash adjustment, repurchase
execution, diluted share forecast, EPS forecast or target price is produced.
Tax, operating expenses and financing are material unresolved sensitivities.

## Applicability decision

Repeatable now as an authoring method: retain exact financial periods and
original sources; separate observations/outlook/assumptions; reconcile alternative
views of the same revenue; preserve dependencies and insufficiency by dimension.
These can inform a later skill design but are not installed production policy.

Requires further analysis: product and geography demand, unit/price evidence,
peer selection, competitive changes, margin sustainability, reinvestment and
market expectations. A one-quarter conditional forecast cannot calibrate
five-year earnings growth or a terminal multiple. Short, medium and long
recommendation statuses remain insufficient_evidence.

Update examples resolve an important distinction: a frozen historical cutoff
rejects later information, while latest-mode assessments may advance their
cutoff and append a same-quarter market revision until a source-declared new
financial quarter exists. Missing evidence creates work without implying a new
quarter. Methods are dependencies too. Mtime is only a discovery hint.

research-state.json is an example inventory, not a stable public schema or an
implemented planner. The related dependency projection digests exclude transport
timestamps and irrelevant raw metadata. A raw-byte digest is retained separately
for provenance. Actual execution needs atomic publication, claim/lease handling,
idempotency, checkpoint validation, retry policy and host dogfood in a separately
specified software change. update-examples.json is an expected-outcome catalog;
no runtime planner or interruption test ran in this batch.

## Verification

See validation.json for the current read-back and independent Decimal arithmetic
checks, temporal exclusions, dependency-digest checks and static Markdown links.
No plugin code changed, so no runtime package-suite result is claimed for this
research batch. Actual Obsidian rendering, scheduler, skill triggering and
cross-session automatic execution remain unverified.

Next bounded research: apply the same evidence separation to Q3 if the method is
retained, and investigate contemporary peer/expectations plus a multi-quarter
operating path before elevating a valuation or recommendation. The twenty-year
history and cross-industry program scope are unchanged.
