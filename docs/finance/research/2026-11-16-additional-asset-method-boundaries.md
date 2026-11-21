# Additional asset method boundaries

Status: preparatory primary-source research, 2026-11-16. This does not complete
Stage G, add supported runtime asset layouts, select a personal portfolio or
authorize scheduling. C/F integration remains the current implementation task.

## ETF: distinguish fund economics from an operating company

The SEC's [ETF investor bulletin](https://www.investor.gov/introduction-investing/general-resources/news-alerts/alerts-bulletins/investor-bulletins-24)
distinguishes the exchange trading price from net asset value (NAV), explains
the creation/redemption role of authorized participants, and identifies
premiums/discounts, bid-ask spreads and fees as separate investor concerns.
Importantly, its stated scope excludes commodity exchange-traded products and
exchange-traded notes that are not registered under the Investment Company Act.
The body was inspected, including its scope statement and risks sections.

Agent-decided research requirements: identify legal vehicle and benchmark
first; inspect mandate, holdings/concentration, replication, fees, distributions,
tracking difference and liquidity. Compare NAV and market-price returns with
matching timestamps and distribution treatment. A discount alone does not
establish undervaluation, and a tight spread does not establish NAV alignment.
Do not apply corporate earnings or free-cash-flow valuation directly to a fund.
Do not assume a gold trust shares every equity ETF disclosure requirement.

## Commodity: specify the exposure before calculating a return

CME's [precious-metals term-structure lesson](https://www.cmegroup.com/education/courses/introduction-to-precious-metals/what-is-contango-and-backwardation)
defines contango and backwardation by futures relative to spot prices, discusses
storage, financing and insurance costs, and explains convenience yield and
convergence. The complete short text body was inspected; no video was viewed.

Agent-decided research requirements: distinguish physical/spot exposure, a
specific futures contract, a rolling futures strategy and an exchange-traded
vehicle. Record contract month, settlement convention, unit, currency, expiry,
delivery and roll rule. Analyze inventory/supply/demand and financing alongside
the curve. An upward-sloping curve alone is not evidence of a positive expected
investor return; rolling exposure needs actual contract prices and costs.
Missing historical curves or a licensed-price restriction remains a gap, not
permission to substitute spot returns for futures-strategy performance.

## FX: separate the traded pair from an effective-rate index

The BOJ's [effective exchange rate explanation](https://www.boj.or.jp/en/statistics/outline/exp/exrate02.htm)
describes nominal effective rates as weighted bilateral-rate measures and real
rates as incorporating relative inflation. It states a monthly release cadence
and explicitly warns that updated trade weights revise historical series.
The April 2026 methodology and usage-warning sections were inspected. This
current explanation is method evidence, not a vintage snapshot of older values.

Agent-decided research requirements: declare pair direction and units, e.g.
JPY per USD, observation time and quote source; separate spot-price changes
from deposit/carry, forward or leveraged-position returns. Keep monetary-policy
releases, inflation, external balances and positioning on their own availability
dates. Do not treat a real effective-rate index as a directly tradable pair,
an unchanged historical vintage or an automatic equilibrium fair value.

## Bounded FX numerical case

The [Fed H.10 release dated July 1, 2024](https://www.federalreserve.gov/releases/h10/20240701/)
reports June 24–28 observations, explicitly in currency units per USD except
asterisked currencies. Its yen row rises from 159.7100 to 160.8800 JPY/USD.
Decimal calculation gives USD appreciation in JPY of 0.7326%, but JPY
depreciation in USD of -0.7273%; reciprocal returns are not exact arithmetic
negatives. These are reference-price changes, not funded trading returns.

The [retained selected evidence](../pilots/additional-assets-v1/fx-reference-evidence.json)
also rejects this July 1 document as an input to a June 28 reconstruction,
despite its earlier observation dates, and accepts it at a July 2 cutoff.
`ND` remains missing rather than zero or an implicit forward fill. Corporate
P/E and cash-flow valuation are refused for this currency pair. The release
header, units, yen row and missing-value legend were read; raw HTML was not
retained. Macro evidence, instrument costs, horizon conclusions and independent
research review remain pending; this does not complete the FX investment case.

## Bounded commodity delivery case

The [EIA article actually dated April 27, 2020](https://www.eia.gov/TodayinEnergy/detail.php?id=43495)
supports an April 28 reconstruction of negative May-contract prices and delivery
constraints. Its tank inventory/capacity figures imply 76% occupancy after
rounding; unused physical space is not necessarily uncommitted storage. The
[selected evidence](../pilots/additional-assets-v1/wti-delivery-evidence.json)
separately excludes a November CFTC audit and distinguishes intraday low from
settlement. Negative values are retained; log returns and a prospective purchase
of an expired contract are refused. This is not a verified rolling strategy.

## Bounded ETF tracking case

SPY's [original annual report](https://www.sec.gov/Archives/edgar/data/884394/000119312524266771/d814670dn30d.htm)
reports 36.15% NAV total return versus 36.35% benchmark return, a -0.20
percentage-point difference. This is not tracking-error volatility or executable
market-price return. The [filing index](https://www.sec.gov/Archives/edgar/data/884394/000119312524266771/0001193125-24-266771-index.html)
dates publication to November 27, after the September 30 report endpoint.
[Selected evidence](../pilots/additional-assets-v1/etf-tracking-evidence.json)
therefore excludes this document at September 30. Mandate, holdings, liquidity
and complete investment analysis remain pending; no current fee or return claim
is inferred from the historical report.

## Required next evidence before Stage G can pass

For each asset class, select one identified instrument and fixed information
cutoff, acquire its actual eligible data/documents, calculate an independently
checkable example, demonstrate an unsuitable-model refusal and source failure,
and produce conditional short/medium/long analysis with counterevidence.
Preserve source reading coverage and historical revisions. This document alone
proves neither acquisition support nor a completed investment case.
