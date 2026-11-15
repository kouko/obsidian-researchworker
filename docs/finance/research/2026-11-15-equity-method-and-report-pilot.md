# Equity research methods and report pilot — Stage A

Research date: 2026-11-15. Scope: method selection, source coverage and report
examples for Apple fiscal 2024Q2/Q3. This is a research design, not a released
analysis skill, legal compliance determination or a historical performance test.

## Evidence and its effect on the design

| Primary reference | Observed guidance | Local design decision |
|---|---|---|
| [CFA financial-analysis framework](https://www.cfainstitute.org/insights/professional-learning/refresher-readings/2026/integration-financial-statement-analysis-techniques) | Begins with purpose, separates data preparation from interpretation, and includes follow-up | State the question and data boundary before drafting; keep numerical evidence separate from judgments and record update dependencies |
| [CFA Research Challenge report guidelines](https://www.cfainstitute.org/sites/default/files/-/media/documents/support/research-challenge/challenge/rc-written-report-guidelines.pdf) | Includes business, industry/competition, financials, valuation, risks and ESG; prices are dated | Cover those questions across a small set of notes, rather than treating financial ratios alone as investment research |
| [SEC financial-statement guide](https://www.sec.gov/about/reports-publications/beginners-guide-financial-statements) | Explains related statements with different period/stock meanings | Preserve instant balances and duration flows; do not treat profit and cash generation as interchangeable |
| [FINRA 2241(c)(1)–(2)](https://www.finra.org/rules-guidance/rulebooks/finra-rules/2241) | Member-firm reports explain the basis and risks of ratings and define rating horizons/benchmarks | Use explicit horizon/benchmark fields and an insufficient-evidence result. This is a design reference, not a claim that the personal pilot is a FINRA member report |

A [broker-hosted 2014 Morningstar guide with an Apple analyst-report sample](https://www.schwab.wallst.com/client/Content/Documents/MstarEquityAnalystReportGuide.pdf)
provides a professional-format contrast: it separates the thesis, bullish and
bearish arguments, valuation and uncertainty, and describes daily rating updates.
This supports separating a reporting-quarter financial baseline from a more
frequently reassessed price-dependent judgment. It does not establish current
provider policy, investment performance or a universal reporting schedule. We
inspect its structure only; no report pages, ratings or proprietary model are
redistributed. The [Japanese provider page](https://ibbotson.co.jp/information-products/research/equity-research/)
was also checked for source provenance, not used to purchase research. A current
Morningstar help page returned 403 and is not counted as inspected evidence.

The CFA competition is an educational industry-style report reference, not proof
that all professional analysts use one format. The 2026 curriculum informs a
method chosen now; it is not evidence the method or model ran in 2024. There is
no universal professional definition of short/medium/long established here.

## Minimal common core and note boundaries

| Note | Questions answered | Body shape | Evidence / update trigger |
|---|---|---|---|
| Financials | Growth, margins, cash conversion, balance sheet and capital allocation | Reported/derived metric table, explanations, contrary evidence | New filing, correction, accounting or calculation change |
| Business and competition | Product/region drivers, economic exposure and competitive claims | Driver evidence, alternative explanations, independent-data gaps | Material operating/competitive disclosure |
| Market and valuation | What market conditions and price/assumptions make the security attractive? | Dated market context, valuation inputs, scenarios and missing evidence | New price/assumption/macro release; recheck before a new recommendation |
| Synthesis | What changed, how strong is the case, and what would invalidate it? | Thesis/counter-thesis, three horizon judgments, dependencies and next questions | Material change to an input note or scheduled reassessment |

This four-note pilot merges related dimensions to avoid empty files. Risks,
governance/capital allocation and ESG coverage remain explicit sections; an
unassessed issue is marked unknown. Split a dimension only after the pilot shows
a distinct question or update cadence, not to imitate another toolkit's count.
Reusable rules would later belong in the finance skill; these repository research
documents are evidence for that future decision, not a policy manual copied into
the user's vault. Private objectives, tax, sizing and risk limits remain unset.

## Three distinct time meanings

- Financial identity: issuer fiscal year/quarter and literal reported periods.
- Source availability: publication date/time and accession/version for each input.
- Assessment: an explicit information cutoff, separate from creation/retrieval time.

The examples use end-of-day New York cutoffs on 2024-05-03 and 2024-08-02,
after their original SEC filings. Earnings releases were public one day earlier;
the SEC-based sample does not claim that filing date is the earliest time the
market knew the figures. No intraday eligibility, executable signal or trade
return is demonstrated. A later current assessment may reuse the quarter's
financials with newer eligible market evidence, retaining a new version; it must
also disclose if newer financial filings are available. Old judgments stay intact.

## Proposed horizon and benchmark convention

Local, reversible **pilot convention**, not a user-ratified global policy:

| Horizon | Explicit interval from assessment | Main question | Needed evidence |
|---|---|---|---|
| Short | More than 0 through 3 months | Catalyst and price expectations | Verified price, upcoming events and expectations |
| Medium | More than 3 through 12 months | Earnings/valuation revision | Forecast bridge, price and scenarios |
| Long | More than 12 through 60 months | Durable economics and capital allocation | Competitive evidence, reinvestment and valuation range |

The intervals are mutually exclusive and configurable. The user's twenty-year
requirement concerns research history, not a twenty-year holding period. Proposed
primary comparison is a US broad-equity **total-return** benchmark, with a
technology/growth comparison as optional secondary context; the actual index,
currency, dividend reinvestment and cost convention must be fixed before a
performance claim. No benchmark return is calculated in this pilot.

Separate fundamental stance from security recommendation. `insufficient_evidence`
is not `hold`, an assumed neutral return, or a zero target. An attractive business
can be an unattractive security at a given price. This pilot does not invent a
price target, personal allocation or a buy/sell decision when valuation inputs
are incomplete.

## Numerical preparation demonstrated

Use the original accession and exact start/end for each metric, not companyfacts
`fy/fp` as a comparative-period identity. USD values and USD/share EPS stay
distinct. Product/region cells are taken from the original 10-Q MD&A tables,
where the standard consolidated API lacks dimensional detail.

Only additive cash-flow items are differenced across compatible current-year
YTD statements. Q2 needs Q1 as a supporting input; Q3 needs Q2. Both inputs must
share issuer, consolidated scope, currency, fiscal-year start and compatible
accounting definitions, with their source vintages visible. This finite example
is not a general restatement-safe normalization engine. EPS, weighted-average
shares, margins and instant balances are never obtained by this subtraction.
The local FCF proxy is CFO less PP&E cash purchases; it is a named calculation,
not an issuer-reported or universally defined financial measure.

## Prior art rechecked at original sources

| Source inspected | What is actually visible | Useful reference / limit |
|---|---|---|
| [n8n stock-analysis template](https://n8n.io/workflows/2209-ai-powered-automated-stock-analysis/) | A documented planning/writing/editing workflow using SEC 10-K questions and a Google Docs output | Reference for work decomposition; listing/marketing is not proof of source accuracy, historical cutoffs, persistent revisions or automated investment quality |
| [n8n Q&A companion](https://n8n.io/workflows/2183-ai-crew-to-automate-fundamental-stock-analysis-qanda-workflow/) | Annual-report PDF ingestion and a retrieval/Q&A back end are documented separately from the front-end analysts | Separate acquisition/retrieval from analysis; no template was purchased, installed or executed |
| [FinRobot Equity README](https://github.com/AI4Finance-Foundation/FinRobot/blob/master/finrobot_equity/README.md) and [published example](https://ai4finance-foundation.github.io/FinRobot/finrobot_equity/core/output/NVDA_Equity_Research_Report.html) | A public report artifact and a documented data/computation/narrative/rendering pipeline with provider keys | Reference for section responsibility and number provenance. Documentation/example inspection plus the bounded source check below; no pinned whole-project audit, runtime or forecast/valuation validation |

A bounded static read of FinRobot's [report renderer](https://raw.githubusercontent.com/AI4Finance-Foundation/FinRobot/master/finrobot_equity/core/src/create_equity_report.py)
(`generate_major_takeaways`, observed 2026-11-15) found improvement-oriented
phrases and affirmative fallback statements without a corresponding directional
comparison in that helper. This is a concrete reason to verify claims against
numbers rather than accepting polished prose or role separation as validation.
It is a mutable-master source observation, not a pinned whole-project audit or
an executed failure; no code was copied into the plugin or run.

No universal absence, superiority or profitability claim follows. Do not import
those projects, providers or execution dependencies on the strength of a report
example. Monkey Skills remains a read-only provenance/reference source; this
phase reuses only already transplanted acquisition code.

## Deliberate limits and later design decisions

Verified historical price/adjustment conventions, peer valuations, forecast
assumptions, independent competitive metrics and broader ESG evidence are still
needed for an actionable security recommendation. The two-quarter examples are
allowed to conclude insufficient evidence; missing is never zero. Full host
operation, automatic task discovery/resumption, general quarterly normalization,
cross-industry behavior and twenty-year backfill are later acceptance gates.
