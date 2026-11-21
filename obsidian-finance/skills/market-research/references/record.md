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
Each source records its verified `published_at` date or timestamp,
original `url`, `locator` within the source and `observation_period`.
Label the source's status, such as preliminary, in the notes. The mapping
key identifies that exact source version. Each claim gives its `text` and
a `source_ids` list with all of its economic
inputs. Save unavailable inputs as pending work. A claim, forecast or actual
cannot use a source released after the saved snapshot cutoff. A citation also
needs a URL, locator and observation period for each source version.
Avoid using a date-only same-day release for an intraday claim.

Save reusable structured observations and forecasts in `actuals` and
`forecasts` where appropriate. Give each observation its `version`,
`scope`, `metric`, `unit`, `target_period`, numeric `value`, and a
`source_ids` list. Retain exact earlier forecast and actual versions and the
comparison result in `comparisons`. A pending outcome remains open until
a matching release is eligible. The `compare` command reads `forecast`,
optional `actual`, and `sources` from standard input.

A minimal publication example:

```json
{
  "market": "smartphones",
  "quarter": "2024Q3",
  "cutoff": "2024-10-14",
  "revision": 1,
  "overview": "# Smartphones",
  "analysis": "Worldwide shipments totaled 316.1 million units (preliminary).",
  "outlook": "Check later releases for revisions.",
  "sources": {
    "idc-2024q3-preliminary": {
      "published_at": "2024-10-14",
      "url": "https://www.idc.com/resource-center/press-releases/worldwide-smartphone-market-grows-4-with-316-1-million-units-shipped-in-the-third-quarter-of-2024-according-to-idc/",
      "locator": "Worldwide Smartphone Shipments table, all vendors",
      "observation_period": "2024Q3"
    }
  },
  "claims": {
    "market-total": {
      "text": "Worldwide smartphone shipments totaled 316.1 million units (preliminary).",
      "source_ids": ["idc-2024q3-preliminary"]
    }
  },
  "pending": ["Check later releases for revisions."]
}
```

The market directory holds a user-editable `overview.md`, created if
absent and preserved on later publications. Each quarter has revision
subdirectories with their own `overview.md`, `analysis.md`, `sources.md`,
`outlook.md` and `review.md`. The review links to the notes saved for
that revision and is the authoritative published record. For an older
record without its own overview, a missing or changed shared overview
is reported as a recovery issue. A resume lookup returns the selected record and any
issues found. Keep any occupied revision directory intact, including an
interrupted one. Publish the next attempt under a free revision number and
use the prior valid record as the starting point where available.

A citation returns the matched claim and source records, or null when there
is no eligible match. Its `cutoff` is the requested issuer assessment cutoff,
and `snapshot_cutoff` is the selected market review's cutoff. If
`retrospective` is true, the market review uses a later cutoff. Describe the
citation as a reconstruction using original evidence eligible at the issuer
cutoff. The source's `published_at` field gives its own availability date
or timestamp.

For monthly aggregation, send an object with `observations` and `sources`.
Each row gives an ISO `month`, `scope`, `metric`, `unit`, `definition` and its
`source_ids`. For totals supply `value`. For `--ratio`, supply
`numerator` and `denominator` to obtain a fraction. The helper returns
source IDs for the components and identifies missing months when coverage
is partial. Confirm that each row represents a discrete observation.
A rolling monthly average cannot be added as if it were a monthly total.
