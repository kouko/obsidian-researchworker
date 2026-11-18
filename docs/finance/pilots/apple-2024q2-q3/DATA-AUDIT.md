# Apple two-quarter source and numerical audit

Research date: 2026-11-15. Data source: public SEC responses and original primary
filings, acquired with the unchanged accepted runtime at `08f65d9`. Requests used
the previously authorized visibly non-real test contact. Success establishes
public transport for these samples, not genuine-contact validation or a claim
that SEC never checks identities. No private settings were read.

## Scope actually observed

| Fiscal period | Purpose | Reporting endpoint | Official filing / sample cutoff | Eligible observations |
|---|---|---|---|---:|
| 2024Q1 | Supporting YTD input only | 2023-12-30 | 2024-02-02 | 98 |
| 2024Q2 | First research sample | 2024-03-30 | 2024-05-03 | 124 |
| 2024Q3 | Second research sample | 2024-06-29 | 2024-08-02 | 125 |

All three acquisitions returned complete/exit 0 and no source errors. That status
means the acquisition's required endpoints and selected observations succeeded;
it does **not** certify complete statements, analytical quality or all quarters.
Source manifests, original accessions, retrieval timestamps and hashes are in
[source-manifests.json](data/source-manifests.json). Raw latest API payloads are
unfiltered evidence, not immutable historical API snapshots. The primary filing
and exact accession-bound rows are retained as the figures' review basis.

## Durable evidence and temporary material

- [financial-observations.json](data/financial-observations.json) stores selected
  reported current/comparative rows with concept, unit, dates, value and source.
- [quarter-packs.json](data/quarter-packs.json) stores literal MD&A cells and
  prepared values. Their dollar tables use millions; the JSON metrics use USD.
- [calculations.json](data/calculations.json) stores input identifiers, formulas,
  derived values and assumptions for cash-flow differences and the FCF proxy.
- Full raw runs remain at the explicitly labeled local paths in the manifest;
  they may be removed by temporary cleanup. The committed compact evidence and
  primary URLs allow review without treating that cache as the only record.
- The one-off extraction/validation programs are temporary research aids, not
  shipped plugin features. No generic normalization or update engine was added.

## Coverage by research dimension

| Dimension | Verified input | Missing / limitation | Consequence |
|---|---|---|---|
| Income and balance sheet | Selected exact accession/period facts; accounting equation checked | Not every line/footnote was modeled | Limited financial analysis, not statement completeness |
| Cash flow | Same-year YTD CFO, capex, repurchases and dividends with Q1/Q2 supports | Cross-filing comparability requires analyst review; not a universal amendment handler | Derived rows explicitly marked and inputs preserved |
| Product and geography | Original 10-Q MD&A product and Greater China rows | Units sold, prices, independent market share and segment full economics absent | Drivers are hypotheses, not demonstrated volume/market-share changes |
| Capital allocation/governance | Cash-flow repurchases/dividends, share counts and public authorization | Cash-flow, equity-table and management repurchase measures differ | Do not mix measures or equate an authorization with cash spent |
| Market/macro | Dated FOMC statements at each assessment | Verified historical stock price, adjustment basis and return benchmark absent | No numeric target, valuation multiple or security rating |
| Competition/ESG | Bounded issuer risk evidence and dated DOJ allegation | Independent peer dataset and substantive ESG review absent | Explicit unknowns, not a favorable default assessment |
| Twenty-year objective | Two notes plus one supporting period | No twenty-year inventory/coverage or analyses | At least 80 quarter obligations remain a later coverage target, not this result |

## Data preparation controls

Product revenues sum to total revenue in each quarter. Assets equal liabilities
plus equity at both endpoints. Current and prior-year direct income rows are
selected from the same original filing; YoY compares their actual periods.
Q2 and Q3 are not interchangeable calendar-quarter labels. Each current/prior-year
Q2/Q3 income comparison spans 91 inclusive days. The supporting Q1 packet also
retains its original comparative dates, whose prior-year first quarter spans
98 days rather than 91; no Q1 growth claim is used in the two sample reports.

Cash-flow example, USD millions:

| Measure | Q1 YTD | Q2 YTD | Derived Q2 | Q3 YTD | Derived Q3 |
|---|---:|---:|---:|---:|---:|
| Operating cash flow | 39,895 | 62,585 | 22,690 | 91,443 | 28,858 |
| PP&E cash purchases | 2,392 | 4,388 | 1,996 | 6,539 | 2,151 |
| Local FCF proxy | Not used | Not used | 20,694 | Not used | 26,707 |

Q2 subtracts Q1; Q3 subtracts Q2. Values share consolidated USD and fiscal start
2023-10-01. The originals were reviewed for the same cash-flow labels. A future
restatement, classification or consolidation change requires reconciliation,
not automatic subtraction. EPS and shares retain direct three-month values.

## Cross-industry source reconnaissance, not validation

| Proposed contrast | Primary source inspected | Additional questions identified | State |
|---|---|---|---|
| JPMorgan Chase | [2024 10-K](https://www.sec.gov/Archives/edgar/data/19617/000001961725000270/jpm-20241231.htm) | Net interest economics, credit losses and regulatory capital need a bank-specific path | Source-level reconnaissance only; no acquisition or bank report test |
| ExxonMobil | [2024 10-K](https://www.sec.gov/Archives/edgar/data/34088/000003408825000010/xom-20241231.htm) | Production/reserves, commodity prices and downstream economics need distinct evidence | Source-level reconnaissance only; no acquisition or energy report test |

The 2025-filed contrast reports inform method design today and are **not** inputs
to either 2024 Apple assessment. A large JPMorgan PDF could not be opened by the
web reader; the SEC HTML alternative was inspected. One corporate Exxon report
landing page was inaccessible; the original SEC filing was used instead. No
unavailable source was silently counted as read.

## Unresolved before a full Stage C case

Choose and verify historical market/benchmark data and price conventions; define
valuation and forecast inputs; add independent competitors and material risks;
exercise source revisions, user edits and interrupted/new-period work selection.
The examples below demonstrate report content and temporal boundaries, not those
unimplemented automatic behaviors. Portfolio constraints and sizing remain unset.
