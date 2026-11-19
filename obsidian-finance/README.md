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

## Read-only local work assessment (prototype v1)

This separate operation explains research work from explicitly supplied local
evidence. It does not acquire sources, execute research, resume an agent,
automatically recover work, or maintain notes in an installed host. External
freshness is always `unverified`; even `no_analysis_update` applies only to the
supplied evidence. It never scans a vault or parses the draft pilot
`research-state.json` directly. Adapt those records explicitly first.

```sh
python3 obsidian-finance/scripts/assess_work.py \
  --root /private/tmp/finance-assessment-example \
  --snapshot snapshot.json --mode historical \
  --cutoff 2024-05-03T23:59:59-04:00
```

All four arguments are required. `--mode` is `historical` or `latest`;
`--cutoff` is an ISO timestamp with timezone. Historical cutoff must match
every supplied saved record cutoff. Latest uses the requested cutoff without
changing saved records. stdout contains one JSON result on success; diagnostics
and recovery instructions use stderr. Exit 0 means a completed local assessment
(possibly listing unfinished research), 2 means partial/uncertain evidence,
1 means invalid/unreadable snapshot, and 64 means invalid invocation. An
interrupted process has no persisted job; retry revalidates all inputs.

The Python entry is `run(root, snapshot, mode, cutoff, *, stdout=None,
stderr=None) -> int`; streams default to the process streams. `main(argv=None)`
implements the CLI. Neither entry writes files. The pure core
`work_assessment.assess(snapshot, mode, cutoff)` consumes normalized data rather
than reading paths; the adapter supplies file content to that core.

The exact adapter input is a JSON object with integer `version: 1`, `sources`
and `records` arrays (empty arrays produce evidence gaps). Duplicate JSON keys,
duplicate IDs, non-finite numbers and invalid field types are rejected.

- Each source has nonempty `id`, `issuer`, `kind`; `version` and `available_at`
  are strings or absent/null when unknown. `available_at` is a date or an ISO
  timestamp with timezone; dates become end of day in the assessment timezone.
  Missing/unverified availability is excluded and reported. Supply relevant
  values including units in `projection`, or use `projection_ref` to a JSON
  file; these two fields cannot coexist. Optional `consumers` lists work IDs.
  Financial originals use `kind: financial_original` and source-declared
  `fiscal: {year, period, period_end, original_accession}`; `year` is an integer,
  `period` is Q1–Q4 and `period_end` is an ISO date. Missing fiscal evidence
  produces a gap rather than an inferred quarter.
- Each record has unique `id`, `issuer`, saved timezone-aware `cutoff`,
  `required_sources` (source IDs), `work` array and its saved `fiscal` identity.
  Optional `execution_state`, `last_attempt`, `last_success` remain observations;
  assessment never advances or clears them.
- Each work item has unique `id`, `status` (`complete` or `missing`), optional
  `depends_on` work IDs and `consumed` mapping from source ID to exactly
  `{version, projection}`. Completed work requires `output: {path, digest}`
  and `completion_evidence`, a path to nonempty local verification text.
  `digest` is SHA256 of the output's decoded UTF-8 text encoded as UTF-8
  (universal newline normalization applies). Output text is read and its digest
  checked; a filename or inline `content` never proves completion. Missing or
  mismatched completion evidence prevents reuse. Referenced unreadable files
  invalidate the input; absent completion fields instead produce work gaps.

Use stable logical source IDs across updates, such as `aapl-price`. Change
the source's `version`, `available_at` and relevant `projection` when evidence
changes, retaining the old identity/projection under saved `consumed`. A fresh
source ID alone does not express replacement of an old consumed dependency.
Projection comparison is structured equality; no arbitrary selectors run.
File mtime and unrelated metadata do not establish analytical change. A version
is supplied identity, not a raw-file hash or proof of external authenticity.

`--snapshot`, `projection_ref`, output `path` and `completion_evidence` are
relative to the explicit root. Absolute paths, `..`, and all symlinks (including
in-root symlinks) are rejected before reading targets. Only regular UTF-8 local
files are read. URLs, commands and note instructions remain inert data; unknown
metadata is ignored, never interpreted as a file reference or executable code.
Root-relative reads also use no-follow file descriptors to prevent a swapped
symlink from escaping the boundary.

Result v1 contains `scope: supplied_local_evidence`, `external_freshness:
unverified`, mode, cutoff, status, and stable arrays `decisions`, `gaps`,
`excluded`, `reusable`, `observations`. Decisions identify record, action, work,
evidence, reason and affected dimensions; gaps identify evidence and recovery.
Repeated unchanged inputs return the same result. No live source-discovery or
investment-completion claim follows from this result.

### Isolated Apple example

Run this from the repository root to create a new isolated sample using the
committed Apple Q2 reported evidence. This explicit adaptation retains the
source data and declares forecast work missing; it makes no claim that the
existing pilot's saved dependencies or outputs have been independently verified.
The setup writes only its new temporary directory; the assessor reads it.

```sh
python3 - <<'PY'
import json
from pathlib import Path
import tempfile

pilot = Path("docs/finance/pilots/apple-2024q2-q3/forecast-v1")
root = Path(tempfile.mkdtemp(prefix="finance-assessment-", dir="/private/tmp"))
reported = json.loads((pilot / "reported-inputs.json").read_text())
row = next(row for row in reported["fact_rows"] if row["id"] == "q2.opex")
projection = {"concept": row["concept"], "value": row["val"], "unit": row["unit"],
              "start": row["start"], "end": row["end"]}
(root / "projection.json").write_text(json.dumps(projection))
fiscal = dict(year=row["fy"], period=row["fp"], period_end=row["end"],
              original_accession=row["accn"])
source = dict(id="q2-opex", issuer="AAPL", kind="financial_original",
              version=row["accn"], available_at=row["filed"], fiscal=fiscal,
              projection_ref="projection.json", consumers=["forecast"])
record = dict(id="aapl-2024q2", issuer="AAPL", fiscal=fiscal,
              cutoff=reported["known_as_of"], required_sources=["q2-opex"],
              work=[dict(id="forecast", status="missing", depends_on=[],
                  consumed={"q2-opex": dict(version=row["accn"], projection=projection)})])
(root / "snapshot.json").write_text(json.dumps(dict(version=1, sources=[source], records=[record])))
print(root)
PY
# Use the printed directory as ROOT, then:
python3 obsidian-finance/scripts/assess_work.py \
  --root "$ROOT" --snapshot snapshot.json --mode historical \
  --cutoff 2024-05-03T23:59:59-04:00
```

Set `ROOT` to the printed path before the second command. Expected result:
exit 0 with `resume_incomplete_work` for forecast and unverified external
freshness. The example supplies one relevant financial observation, not a full
financial-analysis dataset. Existing acquisition remains the separate operation
documented above.
