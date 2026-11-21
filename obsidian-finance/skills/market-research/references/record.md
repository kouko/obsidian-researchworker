# Quarterly market research records

Use Python 3.11 or later. Run these commands with the absolute script and
research-root paths selected for the current host. The command options below
assume the working directory is the finance plugin root.

```sh
python3 scripts/market_research.py resume /path/to/research smartphones 2024Q2 --cutoff 2024-07-15
python3 scripts/market_research.py publish /path/to/research < /path/to/draft.json
python3 scripts/market_research.py cite /path/to/research smartphones 2024Q3 market-total 2024-10-31
python3 scripts/market_research.py compare 2024-10-31 < /path/to/comparison.json
python3 scripts/market_research.py aggregate 2024Q3 2024-10-31 --ratio < /path/to/months.json
```

The input and output of the helper are JSON for tool interchange. The vault
receives Markdown. Use a temporary input file outside the managed research
root, or pass the equivalent JSON on standard input.

A publication record identifies `market` (a stable slug), `quarter` (such
as `2024Q3`), `cutoff` (ISO date or timezone-aware ISO date-time) and
positive integer `revision`. Supply `overview`, `analysis` and `outlook`
as Markdown strings. Supply `sources` as a mapping from unique exact
release identifiers to source records, `claims` as a mapping from stable
claim IDs to claim records, and `pending` as a list of unresolved work.
Each source records its verified `published_at` date or timestamp, URL,
locator, observation period and classification, such as preliminary. The
mapping key identifies that exact source version.
Each claim gives its text and a `source_ids` list with all of its economic
inputs. Save unavailable inputs as pending work. A claim, forecast or actual
cannot use a source released after the saved snapshot cutoff. A citation also
needs a URL, locator and observation period for each source version.
Avoid using a date-only same-day release for an intraday claim.

Save reusable structured observations and forecasts in `actuals` and
`forecasts` where appropriate. Give each observation its `version`,
`scope`, `metric`, `unit`, `target_period`, numeric `value`, and source
identifiers. Retain exact earlier forecast and actual versions and the
comparison result in `comparisons`. A pending outcome remains open until
a matching release is eligible. The `compare` command reads `forecast`,
optional `actual`, and `sources` from standard input.

The market directory holds `overview.md`. Each dated observation quarter
has revision subdirectories with `analysis.md`, `sources.md`,
`outlook.md` and `review.md`. The linked review is the authoritative
published record. A resume lookup returns the selected record and any
issues found. A citation returns the matched claim and source records,
or null when there is no eligible match.

For monthly aggregation, send an object with `observations` and `sources`.
Each row gives an ISO `month`, `scope`, `metric`, `unit`, `definition` and its
`source_ids`. For totals supply `value`. For `--ratio`, supply
`numerator` and `denominator` to obtain a fraction. The helper returns
source IDs for the components and identifies missing months when coverage
is partial. Confirm that each row represents a discrete observation.
A rolling monthly average cannot be added as if it were a monthly total.
