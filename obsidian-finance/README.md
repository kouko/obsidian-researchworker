# Obsidian Finance

Optional `obsidian-finance` 0.1.0 provides `sec-data` for public SEC filing
metadata/financial observations and `finance-research` for agent-led research
continuation from a designated folder. It runs independently of the general-note
`obsidian` plugin and the original Monkey Skills project.

Claude and Codex manifests register this separate package in the repository's
local marketplace. Isolated Codex installation and fresh-session operation were
verified. Global plugin refresh and OpenCode support remain unverified, and no
finance loader is shipped for OpenCode.

The [actual host-session evidence](../docs/loom/2026-11-16-finance-research-continuation/evidence/host-sessions.md)
records source-invoked Codex CLI tests using public isolated fixtures. The
[contact acceptance evidence](../docs/loom/2026-11-18-sec-contact-setup/evidence/acceptance-test-evidence.md)
covers isolated installed Codex conversations and distinguishes offline tests
from live SEC access. Partial checkpoints retain unresolved research.

## Skill guides

Use [sec-data](skills/sec-data/README.md) for a public issuer’s filings and
reported financial observations. Choose the fiscal-quarter selector if the
issuer’s fiscal calendar matters, or use the observation-end date range when
you already know the dates. Use [finance-research](skills/finance-research/README.md)
to continue analysis in an existing managed research folder.

## Run directly

Python 3.11 or later is the only runtime requirement; all runtime imports use
the standard library. Live acquisition uses the operator or organization name
and contact email saved in the private local file
`~/.config/obsidian-finance/sec-contact.json`. The SEC skill asks for these
values in the current conversation on first use. The bundled script accepts
`--setup-contact` with a separate non-echoing stdin JSON payload containing
the `name` and `email` fields. See the [SEC skill](skills/sec-data/SKILL.md)
for setup and failure handling. Requests send the contact and public issuer
request to SEC. Local analysis and reuse checks do not require a contact.

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
metrics or twenty-year analysis. The acquisition operation provides no quarterly
arithmetic, narrative analysis, investment recommendations or automatic note
updates.

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

## Folder-grounded agent research

The [finance-research skill](skills/finance-research/SKILL.md) guides the host
agent through scoped discovery, applicable source checks, actual affected
analysis and append-only publication/recovery using the APIs below. It is
separate from download-only `sec-data`; no command wrapper, scheduler or general
workflow engine is added. The persisted asset questions define the research
scope; the caller supplies the root, mode and assessment cutoff rather than a
new hand-written work list each time. Unsupported old notes are preserved.
The current saved-folder adapter manages equities; ETF, commodity and FX
continuation have not been validated as supported asset workflows.

Its [research method](skills/finance-research/references/research-method.md)
requires source-bound reasoning, opposing evidence, explicit analysis horizons
and actual original-section reading coverage with unread exclusions. Retaining
filing HTML or checking selected numbers does not establish complete SEC reading
or a full investment case. Independent completed questions can be saved in a
managed partial checkpoint while required missing work remains pending. Generic
methods stay in the skill; private assumptions and applied-version manifests
remain local. Local no-work findings leave external freshness unverified.

[Isolated behavioral evidence](../docs/loom/2026-11-16-finance-research-continuation/evidence/skill-eval/iteration-1/review.md)
compares synthetic fresh-context trials and retains failures and a schema-guidance
repair. The skill and helpers provide instructions and bounded local mechanics;
those trials do not prove installed-host execution, live source coverage,
calibrated returns or completion of the broader financial research program.
Real fresh-host continuation remains a separate verification requirement.

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

## Read-only saved-folder discovery (metadata v1)

`scripts/research_store.py` provides `discover(root, mode, cutoff) -> dict`.
The root is an explicitly selected local research folder containing the managed
`investing/` subtree. Mode and timezone-aware assessment cutoff are explicit;
the result keeps the accepted assessor's supplied-local-evidence scope and
unverified external freshness. Discovery does not acquire sources, write notes,
publish completion, or certify the substance of investment analysis. Existing
`assess_work.py` and `work_assessment.py` interfaces remain unchanged.

The supported layout is deliberately versioned; arbitrary older Markdown is
preserved, never interpreted or migrated. Missing configuration, unsupported
metadata, escaping references, symlinks and ambiguous source identities raise
`ValueError` with recovery context. No input files change. Configure once:

```text
investing/research.json
investing/assets/equities/{asset-id}/asset.json
investing/assets/equities/{asset-id}/data/sources/{source-revision}.json
investing/assets/equities/{asset-id}/data/analysis/{analysis-id}.json
investing/assets/equities/{asset-id}/data/{original-file}
investing/assets/equities/{asset-id}/cycles/{YYYYQn}/{cutoff}-{review}/review.json
```

Every metadata object has integer `version: 1` (booleans are rejected).
Duplicate JSON keys and non-finite numbers are invalid. Asset, question, review
and logical source IDs contain only ASCII letters, digits, `_` and `-`.
Filenames do not supply fiscal identity. References are root-relative and must
stay beneath `investing/`; all directory components and regular-file reads use
no-follow descriptors, including root ancestors. Document instructions and
unknown fields remain inert data. No selectors or document commands execute.

- `research.json`: `{version: 1, assets: ["aapl"]}` enumerates asset scope.
- `asset.json`: `{version: 1, id: "aapl", issuer: "AAPL", questions: [...]}`.
  Each required question has `id`, `required_sources` (logical source IDs) and
  optional `required_analysis` (local method/assumption IDs) and `depends_on`
  (question IDs in this asset). These durable research
  requirements are configuration, not per-invocation work statuses. Empty
  requirements and unknown question dependencies are rejected. A source ID may
  use the single literal template `{fiscal}` (for example,
  `financial-{fiscal}` becomes `financial-2024Q2` for that record); no arbitrary
  selectors execute and future quarter IDs need no manual question-list edit.
  Every question's expanded required source IDs must appear in that unit's
  frozen consumed identities. Expansion uses the saved record's fiscal quarter,
  including for prices without financial fiscal metadata. An absent source or
  omitted consumed identity invalidates the question and dependent synthesis,
  including legacy reviews without frozen requirements; independent completed
  questions remain reusable.
- Source revision JSON: `version: 1`, stable logical `id`, matching `issuer`,
  `kind`, economic `identity`, `available_at`, relevant typed `projection`,
  `raw_ref`, `raw_digest` and `raw_format` (`json` or `text`). The digest is
  SHA256 of the exact original bytes. JSON originals are strictly parsed;
  text originals require the full decoded original in `projection.raw_text`
  so unverifiable prose changes cannot be dismissed as formatting. Projection
  values retain units and JSON types, including booleans. The full original
  hash supplies provenance; semantic comparison uses identity and projection.
  Relevant-field selection is a recorded author responsibility, not proof of
  authenticity or relevance. Preserve each economic revision and its original
  file instead of replacing historical metadata. Duplicate `(id, identity)`
  pairs and tied latest publication times are rejected. The latest eligible
  publication of each logical source is selected at cutoff; future and unknown
  publication revisions remain visible as exclusions/gaps, never replacements
  for an eligible original. Excluded competing revisions use an `@` plus
  identity SHA256 suffix in result IDs. Selected source IDs are namespaced
  `{asset-id}:{source-id}`. Missing identity/projection/availability remains
  incomplete evidence under the accepted assessment contract.
- Financial-original sources additionally carry source-declared
  `fiscal: {year, period, period_end, original_accession}` as documented above.
  A stable financial source ID binds one fiscal identity; new quarters use new
  IDs, while revisions of the same quarter retain its ID. Cross-quarter reuse
  of one financial source ID is rejected. Price dates never create financial
  quarters. Shared economic studies belong among the applicable source
  dependencies; local methods and assumptions use the separate analysis-input
  contract below. A 2026-authored reconstruction method is not a 2024 economic
  publication and must never acquire a fabricated historical availability date.
- Local analysis metadata under `data/analysis/{analysis-id}.json` contains
  `version: 1`, matching `id`, `kind: method` or `assumption`, actual
  timezone-aware `authored_at`, method/assumption `identity`, typed `projection`,
  `content_ref` and SHA256 `content_digest` of the exact local file bytes.
  It must not contain `available_at`, `fiscal` or `raw_ref`; economic facts and
  prices remain economic sources, never reclassified to bypass cutoff checks.
  Method/assumption kinds are rejected in economic source metadata. Local
  inputs are not screened against the economic cutoff: their actual authorship
  remains visible in each unit's frozen identity, including a 2026 method used
  to reconstruct a 2024 judgment. This does not permit future economic data.
  A method's content file may be a compact applied-version manifest rather
  than a copied generic manual. Generic methodology stays in the skill; the
  calling research agent verifies its selected bundled method's content/version
  before discovery and refreshes this local applied-version manifest when it
  changes. The read-only helper checks only in-root files; it cannot detect or
  certify changes to an external plugin skill without that refresh. Assumptions
  and their content remain local.
- `review.json`: `version: 1`, asset-local review `id`, fiscal identity,
  timezone-aware saved `cutoff`, optional `predecessor` (review ID in the same
  asset and quarter), and `units` mapping question IDs to saved results.
  Fiscal identity must match the quarter directory. Optional `execution_state`,
  `last_attempt` and `last_success` remain unmodified observations. Per quarter,
  discovery selects the sole eligible leaf of the predecessor chain. Latest
  mode includes saved cutoffs at or before the request; historical mode requires
  an exact saved cutoff. Future children never hide eligible predecessors.
  Missing target reviews, dangling or cyclic predecessors, conflicting fiscal
  identities and competing leaves produce explicit review gaps. Every retained
  quarter is considered independently; old reports remain immutable inputs.
  Every eligible source-declared quarter without a usable saved review derives
  its own `/new` record and configured missing questions, even when an older or
  newer quarter is already saved. Empty, interrupted or wholly withdrawn
  quarters cannot hide missing research; existing review/publication gaps remain
  visible. Reviewed quarters do not receive duplicate candidates. Without an
  eligible original the helper does not invent a fiscal quarter.
- A unit contains `consumed: {source-id: {version, projection}}`, freezing
  actual economic identity and relevant projection, `output: {path, digest}`,
  and `verification` (a root-relative JSON reference). Local inputs separately
  use `analysis_inputs: {analysis-id: {kind, version, authored_at, projection,
  content_ref, content_digest}}`, with `version` freezing metadata `identity`.
  Required and previously consumed local inputs are checked, so removing an
  input from configuration cannot silently remove a saved dependency. Missing
  files, changed content, versions, typed projections or authorship invalidate
  the unit and its dependent synthesis transitively; independent work remains
  reusable. Output digests use the
  exact UTF-8 bytes decoded and re-encoded without newline normalization.
  Missing required questions, missing outputs or verification, mismatched
  output content, and changed dependencies prevent reuse. Question dependency
  changes propagate through the existing assessor. Saved units cannot remove
  required questions or introduce unknown questions.
- Verification JSON contains `version: 1`, the same `output_digest`,
  `checks: {sources: true, citations: true, calculations: true,
  counterevidence: true}` and `unresolved: []`. These are recorded author
  self-checks tied to the output, not independent review or proof of analytical
  truth. A required unresolved question stays pending. Existence, nonempty text
  and hashes alone cannot establish completion.

Repeated unchanged discovery is deterministic and read-only. JSON whitespace
and file modification times alone do not trigger analytical work. A no-work
decision applies only to the locally checked scope; it establishes neither
current external coverage nor advisory sufficiency. Folder mechanics and
recorded checks do not replace the agent's substantive research and review.

## Protected local publication and recovery

The same module exposes Python APIs only; it has no publication CLI. These
operations are for an explicitly authorized managed subtree or isolated copy.
They do not acquire evidence, perform analysis, certify investment quality or
establish external freshness. Persist acquired evidence as immutable inputs,
then capture the preconditions **before** analysis/publication:

```python
expected = research_store.publication_snapshot(root)
result = research_store.publish(
    root, "aapl", review, files, expected, "unique-run-id", complete=True,
)
# Revalidate an interrupted recorded run, or restore its predecessor view:
result = research_store.recover(root, "unique-run-id", action="resume")
result = research_store.recover(root, "unique-run-id", action="rollback")
```

`publication_snapshot(root) -> dict[path, sha256]` captures exact regular-file
bytes beneath `investing/`, excluding the helper's `.research-runs/` journals.
The returned map is mandatory and must remain the original pre-analysis map;
refreshing it to suppress a conflict defeats user-edit protection. Changed,
added or missing managed files cause a conflict. Publication and recovery check
these preconditions before work and immediately before the commit point. This
is conservative: even an unrelated managed edit requires reassessment. All
directory traversal and writes use anchored no-follow descriptors; new files
use exclusive creation. Existing files are never overwritten or deleted.
If source acquisition adds files after initial discovery, first verify every
previously captured discovery path still has its original digest; then capture
the publication baseline including only those known new evidence files. An
unexpected edit or addition requires inspection, not an automatic refresh.

`publish(root, asset, review, files, expected, run_id, *, complete=True) -> dict`
accepts the saved-review contract above. `asset` must be configured; `run_id`
is a new stable ASCII ID. The review directory is derived as
`investing/assets/equities/{asset}/cycles/{YYYYQn}/{cutoff-date}-{review-id}`.
An existing quarter requires the current eligible leaf as `predecessor`;
a first review has no predecessor. `files` maps plain filenames ending in
`.md` or `.json` to UTF-8 text, without subdirectories or reserved marker names.
New unit output and verification references use their final root-relative
paths in that directory. An unchanged unit may retain its predecessor's
output/check references and complete frozen dependency identity. Changing its
dependencies or verification while keeping that output is rejected; changed
economic evidence, methods, assumptions or required question dependencies need
recomputation, including dependent synthesis. Legacy reviews without frozen
question requirements retain the existing discovery contract; new publications
freeze all question definitions under `requirements` for subsequent checking.

Each proposed review also supplies `research` with `method` (nonempty applied
method description/version string), `assumptions` (list), `changes` (nonempty
cross-quarter or review change string, not a list), `gaps` (list), and `horizons`.
The latter has exactly `short`, `medium` and `long`, each containing `judgment`,
`evidence` (reference list) and
`invalidation_triggers` (list). Record `insufficient_evidence` honestly where
appropriate; the research agent supplies the actual horizon durations and
conditional reasoning. Structural checks do not judge that reasoning. The
publisher embeds source/local-analysis metadata under `provenance`, retaining
original references/hashes, fiscal identities, economic publication times and
separate actual method/assumption authorship. Original evidence files remain
immutable. The recorded semantic author self-checks remain distinct from an
independent review of research quality.

With `complete=True`, every configured question must be reusable under the
existing discovery/assessment rules and declared research gaps must be empty.
Use `complete=False` to commit a meaningful partial checkpoint: verified units
remain reusable and missing or unresolved required questions remain pending.
Saving review metadata never itself establishes analytical completeness. The
local helper preserves the predecessor's `last_success`; it rejects advancing
the last successful external verification from a local publication. An actual
external attempt can be recorded separately as `last_attempt`, while external
freshness remains unverified by these APIs.

The immutable request, its integrity journal, drafts and staged completion live
under `investing/.research-runs/{run_id}/`. Outputs and a hash-bound
`pending.json` precede `review.json`. The commit point creates a no-overwrite,
same-filesystem hard link to the fully flushed staged completion file;
unsupported filesystem behavior fails without replacing research. A digest
mismatch or incomplete metadata is a named conflict, not a completed review.
Discovery reports unfinished journals/publications even when an older review is
still usable. A review or rollback marker resolves only its matching immutable
run, with journal and published-byte validation. A different run targeting the
same review cannot conceal an earlier failed attempt; recovery of that earlier
run reports a conflict and preserves the other run and both drafts.
It does not present an interrupted attempt as an unchanged no-work
result without that gap. No mutable overview/latest pointer is maintained:
the eligible predecessor-chain leaf defines the saved view.

`recover(root, run_id, *, action="resume") -> dict` rechecks the original
preconditions, journal integrity, saved draft/output bytes and current source,
method and assumption dependencies before adopting unfinished work. Repeating
a successful resume returns the same saved result if its files and original
preconditions still match. `action="rollback"` appends a validated
`withdrawn.json` for a committed review, or `abandoned.json` for unfinished
publication; the prior eligible view becomes visible while all reports,
drafts and failure evidence stay on disk. Rollback refuses edits, unexpected
files or later dependent reviews rather than hiding or deleting them. Altered
withdrawal metadata also produces a conflict. Historical discovery still obeys
the requested exact cutoff; withdrawal never fabricates a predecessor at a
different cutoff. Rollback is limited to this recorded run, not arbitrary files.

Results contain `status` (`complete`, `checkpoint` or `rolled_back`), `review`
(root-relative metadata path) and `run`. Validation/conflict errors raise
`ValueError`; filesystem interruption can raise `OSError`. Preserve the named
files and draft, inspect the conflict and reassess before starting a new run.
Do not edit run journals or completion files to force a success. These are
local mechanics; actual agent continuation and fresh-host research behavior
require separate verification.

## Markdown research continuation

Use this format for new skill-managed research. Python needs PyYAML for
Markdown metadata; existing JSON runs remain readable without it. The helper's
legacy write interface remains available to older callers.

- `investing/index.md` with role `research-overview` supplies the tracked assets.
  An ordinary unmarked overview leaves the legacy watchlist in effect.
- Register research inputs under `data/sources/<revision>.md` and authored
  methods under `data/analysis/<method-id>.md`. Use the bundled templates with
  a matching source or method identity and version. The fenced YAML record
  uses the same version-1 field names as the legacy reader. Keep evidence bytes
  in their original format. Distinct source versions may coexist.

- An optional marked asset note in the asset directory uses a flat Obsidian
  property header and a fenced asset-entry record. Its identity must match
  any existing legacy asset metadata. Duplicate or malformed marked entries
  fail.
- Pass a selected asset and quarter through the candidate-discovery argument.
  Read relevant returned notes and check their claims against the original
  evidence. Frozen notes record the exact claim, note hash, source version,
  and proven availability. Edited notes invalidate dependent work.
- The existing publication helper accepts Markdown mode for the
  seven analysis roles. It renders a versioned review note, embeds verification,
  retains old outputs, and writes no management JSON for new pilot runs.
- The final review appears after its output is written and verified. An
  interruption or conflicting publisher leaves a draft for inspection.
  Re-run discovery and prepare a fresh publication; legacy recovery remains
  a separate operation.


### Copy and verify a quarter

A portable Markdown review keeps its bound inputs under
`cycles/{YYYYQn}/data/`. Source registrations and method registrations are
Markdown. Raw evidence keeps its original format and bytes. A source
registration can bind both the reviewed extraction (`raw_ref` and
`raw_digest`) and the original filing (`original_ref` and
`original_digest`). Register both when citing an extraction whose original
filing is distinct. Comparison sources keep their real fiscal identity.
They do not create cycles in the destination.

Copy the whole quarter folder, then call
`verify_quarter(quarter_root, "run-directory/review.md")`. Operational
references are quarter-relative. Verification checks the captured
configuration, rendered outputs and local evidence, including their hashes
and historical cutoff. A missing local file fails verification even if the
original vault is accessible. Cross-quarter links describe provenance, and
previous research notes stay in their original folders. Save a cited prior
conclusion with `excerpt`, `origin`, and `revision` in
`research.adopted_conclusions`. The verifier does not judge the financial
conclusions.
