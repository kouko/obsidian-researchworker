# Apple valuation diagnostic v1

Status: completed bounded diagnostic, not a calibrated valuation or full Stage C.
The user authorized Q2 first, then Q3 comparison after Stage A. Work order:
verify dated prices; reconstruct reported earnings; separate assumptions; compute
Q2; apply unchanged method to Q3; challenge temporal/model claims; save evidence.

## Method decision and formulas

Agent-decided: use a five-year earnings/exit-multiple sensitivity diagnostic before
a DCF. A cash-flow valuation needs a justified operating forecast, reinvestment,
discount rate and enterprise/equity bridge. Those inputs are not established.
CFO minus capex is not automatically FCFF or FCFE. Skipping that bridge would
produce false precision. This diagnostic fills prices and reported-earnings
coverage but does not close the operating-forecast or calibrated-valuation gaps.

All money is nominal USD. Let NI be reported net income, S dated cover shares,
P the dated close, g an illustrative annual earnings growth rate and M an
illustrative fifth-year price/earnings multiple:

```
TTM NI = FY2023 NI + FY2024 current YTD NI - FY2023 comparable YTD NI
TTM revenue = FY2023 revenue + current YTD revenue - prior comparable YTD revenue
earnings-per-dated-share proxy = TTM NI / S
market-cap proxy = P * S
market-cap / TTM NI = P * S / TTM NI
NI in model year t = TTM NI * (1 + g)^t, t = 1..5
year-5 scenario price = NI in model year 5 / S * M
annualized price return = (year-5 scenario price / P)^(1/5) - 1
required g for price-return hurdle h = (1+h) * (current multiple / M)^(1/5) - 1
```

The model years begin on each assessment date, not the fiscal-year start. The
reported TTM scale is lagged; no stub-period earnings forecast is implied.
NI and revenue are additive; EPS and weighted-average shares are not subtracted.
FY2023 had 53 weeks, FY2024 has 52; the bridge retains reported-period week
differences rather than pretending to be a precise 365-day measure.
Fixed shares deliberately exclude future buybacks, dilution and share-count
forecasting. No cash is added to this equity earnings model; no debt is deducted.
Net income already reflects financing. This is not a cash-flow DCF.

The -2%, 2%, 6%, 10% growth and 20x/25x/30x multiples are agent-decided stress
coordinates, not empirical estimates, analyst consensus or a professional
standard. Their endpoints are not bounds on possible outcomes. There are no
probabilities, expected-value price, fair value, margin-of-safety claim or target.
The 8% price-return hurdle is an illustrative parameter, not user policy or a
benchmark forecast. A five-year endpoint cannot become a twelve-month target.
Damodaran's primary method reference associates equity multiples with growth,
payout and risk; it does not endorse these numeric assumptions:
[fundamental determinants](https://pages.stern.nyu.edu/~adamodar/New_Home_Page/littlebook/controldifferences.htm).

## Source register and temporal separation

Financial rows in reported-inputs.json retain concept, unit, accession, reported
period and filing date. They were selected from the already retrieved SEC
companyfacts payload, with accession equality rather than a latest-value search.
The current payload is not a preserved 2024 feed snapshot. The original filing
tables were independently inspected through public SEC pages for annual/YTD
income, revenue and dated cover shares:

- [FY2023 original 10-K](https://www.sec.gov/Archives/edgar/data/320193/000032019323000106/aapl-20230930.htm), filed 2023-11-03: annual income statement.
- [2024Q2 original 10-Q](https://www.sec.gov/Archives/edgar/data/320193/000032019324000069/aapl-20240330.htm), filed 2024-05-03: cover and six-month income statement.
- [2024Q3 original 10-Q](https://www.sec.gov/Archives/edgar/data/320193/000032019324000081/aapl-20240629.htm), filed 2024-08-02: cover and nine-month income statement.

Price-evidence.json records the exact vendor URL, field, raw float, two-decimal
value used, observation timestamp, retrieval date and raw-payload SHA256.
Yahoo quote.close is used, not adjclose. Both fields were returned and differed:
May 3 close 183.38 vs retrieved adjclose about 181.2647; August 2 close 219.86
vs adjclose about 217.6187. Adjustment histories were not reconstructed; do not
claim all vendor close series are invariant to splits or corporate actions.
Today's quote metadata (including regularMarketPrice) was explicitly excluded.
This is retrospective vendor retrieval, not direct-exchange or historical-vintage
certification. No later dividends or realized outcomes enter the scenarios.

Public structured-note filings corroborate the same historical close levels:
[May 3](https://www.sec.gov/Archives/edgar/data/1666268/000183988224014818/ms2040_424b2-08861.htm)
and [August 2](https://www.sec.gov/Archives/edgar/data/1666268/000183988224025028/ms3186_424b2-14889.htm).
Only search-index excerpts were accessible in this continuation. Their complete
bodies/filing timestamps were not verified, so they are corroboration candidates,
not eligible cutoff-bound forecast inputs or primary exchange proof. The Q2
level also appears in a contemporaneous [AP market report](https://apnews.com/article/3da3918af2387f4921b212194559d610).

Apple IR history returned HTTP 403 to the public fetch; Nasdaq's page exposed no
historical table. Browser-host access was unavailable. Those paths did not
verify prices; the successful Yahoo retrieval is separate evidence. No paid or
authenticated service was used and no access restriction was bypassed.

Method references accessed in 2026 supply research technique, not economic
information supposedly known in 2024. Scenario assumptions were chosen in 2026;
this is an illustrative reconstruction, not a blind point-in-time backtest.
Q3 is a distinct later assessment. Q3 inputs are absent from Q2 calculations.

## Benchmark, recommendation and next evidence

Agent-decided pilot convention: USD S&P 500 Total Return for future performance
evaluation. A total-return index includes reinvested distributions:
[index-provider explanation](https://www.spglobal.com/spdji/en/research-insights/index-literacy/methodology-matters/).
No benchmark values, performance or outperformance are calculated. Price-only
scenario returns cannot be compared directly with benchmark total returns.
Existing pilot horizons (0,3], (3,12], (12,60] months remain proposed conventions,
not global skill defaults. Both assessments retain insufficient_evidence ratings.

Next bounded research: justify revenue by business/geography, margins, buyback
and dilution paths with cutoff-eligible evidence; obtain contemporaneous peer
and expectations inputs; then select/calibrate a valuation method. Full DCF,
short-term catalysts, scenario probabilities and benchmark return data remain
missing. No automatic update/resume skill, twenty-year history, cross-industry
validation, real-vault deployment or production recommendation gate is complete.

## Reproduction and verification

reported-inputs.json, assumptions.json, price-evidence.json and calculations.json
are the compact durable record. Recompute using the formulas above; all 24 grid
cells and six reverse-growth thresholds were independently checked with a
separate verifier. validation.json records checks and exclusions. Large raw
payloads remain temporary, as in Stage A, so hashes identify the fetched bytes
but do not guarantee their future availability. Markdown was checked statically;
actual Obsidian reading-view rendering and host invocation remain unverified.
