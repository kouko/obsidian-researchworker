# Obsidian Finance

Optional `obsidian-finance` 0.1.0 provides one `sec-data` skill for public SEC
filing metadata and financial observations. It runs independently of the
general-note `obsidian` plugin and the original Monkey Skills project.

Claude and Codex manifests register this separate package in the repository's
local marketplace. Registration is not installation or evidence of fresh-session
skill execution. No global plugin refresh or host installation is performed;
OpenCode support is unverified and no finance loader is shipped for that host.

## Run directly

Python 3.11 or later is the only runtime requirement; all runtime imports use
the standard library. Configure `SEC_USER_AGENT` locally with the operator's
genuine identifying name and contact email before running. Do not reuse an
example identity or commit contact details. Requests send this identity and
the public issuer request to SEC; private vault content is not used.

From the repository root:

```sh
python3 obsidian-finance/skills/sec-data/scripts/acquire.py \
  --ticker AAPL \
  --fiscal-quarter 2024Q3 \
  --output-dir /private/tmp/sec-data-sample
```

`YYYYQq` selects the company's fiscal quarter. Without `--as-of`, the data
cutoff is the UTC acquisition date and `mode` is `retrospective`; add
`--as-of 2024-08-15` for an explicit `historical` data snapshot. Both summary
and manifest record `effective_cutoff` and the source-bound `resolution`.
These are data-acquisition dates, not investment-assessment dates. Market,
macro and other research dimensions may need different observation periods
and their own assessment cutoff; this operation does not acquire them.

The compatible observation-end range entry still requires all three dates:

```sh
python3 obsidian-finance/skills/sec-data/scripts/acquire.py \
  --ticker AAPL \
  --period-start 2024-01-01 \
  --period-end 2024-12-31 \
  --as-of 2024-12-31 \
  --output-dir /private/tmp/sec-data-sample
```

The explicitly requested output root may be created when its direct parent
already exists. Each invocation creates a new `sec-run-*` directory; existing
research and previous runs remain unchanged. stdout is one JSON summary;
stderr carries progress. Missing identity or invalid input returns exit 64
before any request.
Quarter and date-range selectors cannot be mixed.

## Fiscal-period evidence

Companyfacts `fy/fp` labels only nominate original 10-Q/10-K primary documents
whose accession and observation endpoint match submissions `reportDate`.
Quarter identity requires the primary document's same-context inline-XBRL
DEI declarations for fiscal year, fiscal period, period endpoint and issuer CIK.
The resolution retains original accession/filing date, literal period end,
declarations/context references and source URL/hash/retrieval time. It does not
guess a quarter start, use calendar months or today's fiscal-year end.

Supported period-end formats are ISO `YYYY-MM-DD` and the inline transformation
`date-monthname-day-year-en` (for example, `June 29, 2024`). Unsupported
transforms, missing or contradictory declarations, ambiguous originals and
unavailable eligible primary documents return `FISCAL_PERIOD_UNRESOLVED` /
exit 1, with raw diagnostics but no eligible dataset or completion marker.
Declaration context matching checks `contextRef` agreement, not full XBRL
context semantics. Primary-document basenames accept only letters, digits,
underscores and hyphens followed by `.htm` or `.html`.

Quarter mode selects observations with exactly the resolved end date while
preserving their original start dates and versions. Q4 binds an original 10-K's
`FY` endpoint; annual/YTD values remain annual/YTD, without Q4 subtraction.

## Data and status

Each finalized usable run contains:

- `manifest.json`: request, issuer, per-source URLs, retrieval timestamps,
  raw payload hashes, errors, limitations and output paths.
- `raw/tickers.json`, `raw/submissions.json`, `raw/companyfacts.json` and
  `raw/archives/`: acquired responses saved verbatim when available. Quarter
  requests also retain candidate `raw/primary-<accession>.html` documents.
- `eligible-facts.json`: observation rows with taxonomy, concept, unit, value,
  duration/instant dates, accession, filed date and source evidence.
- `filings.json`: 10-K, 10-Q and amendments published on or before cutoff,
  without a lower publication bound.
- `coverage.json`: observed spans, exclusion counts and inventory limitations.
- `completion.json`: actual status of a fully written usable run.

Required-source failures take precedence over empty results. `complete` / exit
0 means eligible facts and all required sources; `partial` / exit 2 means a
required source or archive failed; `empty` / exit 3 means no eligible facts
with all required sources valid, even if filings exist. `failed` / exit 1 means
no trustworthy issuer or usable financial endpoint section, or an output error.
Unresolved fiscal-period identity also forces failed / exit 1 before other statuses.
Source-failed runs may retain a diagnostic manifest and raw evidence but have
no eligible dataset or
completion marker. Output errors may leave unfinished files without that marker;
do not use them as completed data. Retry into a new run.

Observation end dates are filtered inclusively by the requested period; filed
dates are filtered inclusively by cutoff. Missing or invalid publication dates
are excluded; conflicting accession or acceptance-date evidence is quarantined.
Acceptance before the official filing date is valid; preserve both and use the
official filing date for cutoff eligibility. Malformed acceptance timestamps or
acceptance dates after the official filing date remain conflicts.
Unknown inventory accessions retain their filed date and reconstructable SEC
URL with an explicit inventory-absence label. Distinct reported versions remain
distinct; duration start dates preserve annual, year-to-date and shorter facts.

Raw responses are unfiltered latest endpoint evidence, not historical
snapshots. A day cutoff does not establish intraday trading availability.
Observed spans do not establish complete quarterly statements, custom segment
metrics or twenty-year analysis. No quarterly arithmetic, narrative analysis,
investment recommendations or automatic note updates are provided.

## Development and provenance

With pytest already available, run from the repository root:

```sh
python3 -m pytest obsidian/tests obsidian-finance/tests -q -p no:cacheprovider
```

pytest is a development-only dependency. Use an isolated project environment
if setup is needed; do not install into conda base. Offline synthetic-response
tests exercise the pipeline; they do not establish live SEC access or host
execution. See [PROVENANCE.md](PROVENANCE.md) and [LICENSE](LICENSE) for the
attributed narrow extraction and retained source license.

The [quarter replay evidence](../docs/loom/2026-11-15-finance-sec-baseline/evidence/quarter-replay.md)
separately records a real-payload offline replay and one live CLI acquisition.
Neither establishes installed-host skill execution or complete financial research.
