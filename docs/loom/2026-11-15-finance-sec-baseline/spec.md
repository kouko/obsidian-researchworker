# Independent US financial-data acquisition — spec
intent: 2026-11-15-finance-sec-baseline@b5c4dcd
confirmed-behavior: 2026-11-15 @a2d1032
pre-build-review: required — adds an independently distributed plugin and a public data-artifact/command contract, with historical-eligibility semantics

## Requirements

REQ-1 — Optional independent finance capability
  The finance plugin shall be selectable separately from the existing general-note plugin and execute its data operation with the original Monkey Skills checkout and installed plugins unavailable → Acceptance #1

REQ-2 — Traceable Apple acquisition
  WHEN the user requests an Apple financial-data sample, the finance capability shall return acquired public filing metadata and structured financial observations with issuer identity, source identifiers/URLs, reporting dates, publication dates and retrieval timestamps → Acceptance #2

REQ-3 — Honest coverage and failure
  WHEN acquisition finishes or cannot finish, the capability shall identify acquired, partial, empty and failed results and observed coverage without claiming annual/comparative observations are complete quarterly statements or twenty-year analysis → Acceptance #3

REQ-4 — Historical date eligibility
  WHEN the user supplies a historical information cutoff, the capability shall separate eligible observations and filings from later or undated information, preserving their publication evidence and making no claim of knowledge before that evidence → Acceptance #4

REQ-5 — Repeatable, non-destructive output
  WHEN acquisition is repeated or encounters input, identity, network or data errors, the capability shall preserve existing research/output, return a reproducible source-linked result or an explicit actionable error, and never present failure as success → Acceptance #5

REQ-6 — Provenance and bounded compatibility
  The change shall retain required source attribution and useful acquired behavior checks, preserve the original source project and existing general-note functionality, and distinguish package registration, installation and actually observed host execution → Acceptance #6

## Design decision

- agent-decided — Reuse the existing dedicated `finese-research` branch: its uncommitted work and user-selected worktree have exclusively carried this finance program, and its base contains no unrelated in-flight implementation. No branch reset or source worktree mutation is needed.
- agent-decided — Use `obsidian-finance` as the initial sibling plugin identifier, matching the user's candidate and optional installation outcome; no separate repository, proxy plugin or general-purpose shared framework.
- agent-decided — Deliver one data acquisition skill and a narrow command under its own plugin root. Extract only dependency-complete SEC acquisition functions and necessary enduring behavior tests after confirmation, retaining provenance; do not copy the 6,197-line adapter and unrelated provider/model entrypoints wholesale.
- user-decided — Source tools must be transplanted here before reuse or modification; no runtime import, subprocess or cache dependency on Monkey Skills. Preserve source repository and existing vault.
- agent-decided — Use the public SEC submissions/companyfacts endpoints, not paid providers, to validate the first slice. Follow archived submissions pages for the requested filing interval; explicitly report archive retrieval failures. No filing-document narrative parsing, three-statement stitching or quarterly arithmetic in this slice.
- agent-decided — A successful manifest registers only currently shipped finance data behavior, not research recommendations. Register separate Claude/Codex plugin metadata; any OpenCode metadata/loader must be tested independently before declaring that host usable. No user/global plugin refresh is performed by this change. Validate executable data behavior directly in isolated output first; disclose fresh-session skill invocation limitations separately.
- agent-decided — A single operation accepts `--ticker`, `--period-start`, `--period-end`, `--as-of` and `--output-dir`. All dates are ISO dates; start/end filter observation end dates, not guessed fiscal quarter names. Endpoints are public and no API key is required. `SEC_USER_AGENT` supplies a user-provided identifying contact string and is never copied from a private config, inferred from a source default, committed or logged in full. Missing identity is an actionable pre-network error. Avoid treating an arbitrary default address as a genuine operator identity.
- agent-decided — Output is a structured data artifact, not a Markdown investment report. The CLI's machine-readable stdout is one summary object; progress is stderr only. The skill translates that summary into concise Traditional Chinese when used in this conversation's language.
- agent-decided — Write a new immutable run subdirectory under the explicitly requested output directory, refusing file collisions and avoiding existing content. Missing parent directories may be created only beneath that requested root. The user chooses a test/output location; the program does not discover or write the actual vault or global config.
- agent-decided — Store a source manifest, complete acquired raw endpoint responses, eligible fact rows, a filing inventory and exclusion/coverage counts. Raw latest API responses may contain information later than cutoff and are explicitly labeled unfiltered evidence; only eligible rows/inventory are analytical inputs. If all acquisition fails, write no success dataset. A finalized failed manifest may be retained in the new run directory for diagnostics. An interrupted/unfinished directory has no completion marker and cannot be mistaken for an eligible completed run.
- agent-decided — Observation identity retains taxonomy, concept, unit, duration/instant dates, value, accession and filed date; preserve multiple reported versions without selecting a single latest value across historical time. This slice filters eligibility, not harmonizes concepts or produces canonical accounting lines. A file containing year-to-date cash flow is not silently relabeled as a discrete quarter.
- agent-decided — `--as-of` is an inclusive publication date, not an intraday timestamp. Exclude fact rows with missing/invalid publication dates; label the limitation. Match accession metadata/acceptance time where available; if evidence conflicts, quarantine the row rather than resolving the conflict through guesswork. A supplied cutoff in the future or invalid input is rejected. A day cutoff is not evidence a fact was available before a specific trading session that day.
- agent-decided — Period-start is inclusive, period-end inclusive, and start must not exceed end. Keep duration start dates to distinguish annual, year-to-date and shorter observations. The filing inventory can include filings after the selected observation period but no later than cutoff because those can contain relevant comparative periods. Publication timing and fiscal period coverage remain separate filters.
- agent-decided — Coverage reports observed concept/unit/period spans and counts by eligibility, not completeness against an invented canonical set of quarters. The intended twenty-year objective remains unmet until later coverage and analysis stages validate it. Standard-taxonomy companyfacts does not claim complete custom segment/operating metrics.
- agent-decided — Retain source payload hashes and acquisition timestamps for replay/audit, while treating network responses as variable across runs. Reruns can produce separate evidence snapshots but must not overwrite existing data or claim immutable latest-API contents. No persistent KPI service or silent cross-run content merge.
- agent-decided — Missing acquisition sections make a partial result; empty eligible facts are a no-results result, not proof that the issuer published no information. HTTP denial/rate limiting, malformed data, issuer mismatch and archive-page failures remain distinguishable errors. No silent fallback to another issuer, provider or current-data replacement.
- agent-decided — Package/runtime dependencies use an isolated project environment; no setup in conda base, credentials migration or changes to global host settings. Exact dependency pins, command filename and public schema details belong to the technical plan with tests, within these visible semantics.
- agent-decided — No investment analysis, automatic update assessment, price history, total-return computation, FRED vintage retrieval, task scheduler or recommendations are included. Data identity/date evidence is useful input to those later capabilities, not evidence they work now.

## Alternatives considered

- Copy the entire original adapter and pack runner: imports narrative/reconstruction/provider responsibilities not needed for finite public fact acquisition and increases dependency ownership.
- Reimplement SEC acquisition from scratch: discards existing behavior and fixes without establishing a missing capability; prefer an attributed narrow extraction with explicit adaptations.
- Run the original checkout through a wrapper: violates transplant-first and independent execution requirements.
- Normalize quarterly statements now: increases semantic risk before raw coverage and date provenance are established.
- Store only endpoint extrema as "coverage": cannot distinguish repeated observations, annual comparatives or missing quarterly values, so observed spans must be labeled and never marketed as complete research.
- Use filesystem modification time or a cache age as historical eligibility: neither proves publication before a research cutoff.
- Overwrite a fixed output filename or merge into the user's vault: unnecessary risk to existing user data; new run directories satisfy this slice.

## Current state evidence

- Forward: `.claude-plugin/marketplace.json` currently lists only `obsidian`; finance data entry is greenfield in this repo.
- Reverse: `obsidian/.codex-plugin/plugin.json` advertises general note/research skills, not a finance-specific acquisition consumer; future finance consumers are not implemented.
- Error: `docs/loom/research/2026-11-15-investment-tooling-reuse.md`, probe section, preserves initial DNS failure and subsequent independent public download; no existing destination finance error contract.
- Data: `docs/loom/research/2026-11-15-investment-tooling-reuse.md`, observed concept table, shows repeated observations and different period/publication dates; source originals remain outside the destination runtime.
- Boundary: `docs/finance/PLAN-DRAFT.md`, Sections 7, 9.1 and 10, separates minimal acquisition from quarterly reports, automatic work selection and twenty-year historical expansion.

## UI flows

### Finance acquisition operation

The user requests public filing/fact data for Apple, specifies an observation
date range, a historical information cutoff and a new output location. They see
a data package and summary; this operation does not present investment advice.

| Case | What the user does | What they see / recovery |
|---|---|---|
| Cold start / independent selection | Select only the finance plugin and request data | The data operation is available without the original project or general-note plugin; unsupported/unverified hosts are identified rather than implied supported |
| In progress | Start a valid acquisition request | Progress names the public source and stage on stderr, while stdout remains machine-readable; no completed result appears before validation |
| Success | Request Apple data with a valid date range/cutoff, identity and destination | Exit 0, summary `status: complete`, new run path, source/period/publication/retrieval evidence, eligible counts and coverage limitations |
| Partial source acquisition | A required source section or archive cannot be acquired but another section is valid | Exit 2, summary `status: partial`, named missing sections and retry guidance; preserved usable evidence is not called complete |
| Empty eligible data | Supply a valid request with no eligible observations or filings | Exit 3, summary `status: empty`, exclusion counts/reasons and guidance to review dates or disclosure coverage; no invented analysis |
| No contact identity | Start without the required supplied contact identity | Exit 64, `SEC_IDENTITY_REQUIRED`; explain how to configure the contact string before retrying; no network request |
| Invalid input | Supply an invalid ticker/date, reversed interval, future cutoff or invalid destination | Exit 64, `INVALID_INPUT` or `OUTPUT_UNAVAILABLE`, affected input and correction guidance; preserve existing files |
| Unknown issuer | Supply a ticker not resolved by the registry | Exit 1, `ISSUER_NOT_FOUND`, no substituted issuer and guidance to verify identifier |
| Source identity mismatch | Returned issuer identity disagrees with requested identity | Exit 1, `ISSUER_MISMATCH`, no eligible dataset from that response; verify source/identifier before retry |
| Source failure | Network/HTTP denial/rate limit or malformed response prevents usable acquisition | Exit 1, `SOURCE_UNAVAILABLE` or `INVALID_SOURCE_DATA`, source/stage and bounded retry guidance; never suggest a successful refresh |
| Output error | Destination cannot be written or a reserved file collides | Exit 1, `OUTPUT_WRITE_FAILED`, preserved existing contents and a different-location/retry instruction; no completed marker |
| Historical exclusion | Acquired facts include later or undated disclosures | Eligible inputs omit them; raw evidence is clearly unfiltered, and counts explain exclusions; same-day timing limitations remain visible |
| Repeat request | Run the same request again | A separate run preserves previous outputs; no existing report is edited and no claim that counts must remain identical across source revisions |
| Abandon / interrupt | Stop while fetching or writing | Prior completed runs remain valid; unfinished output is not marked complete; rerun starts a new bounded acquisition rather than assuming a partial run succeeded |

### Existing research and downstream use

Read a completed data summary → see source evidence and limitations, not buy/sell
advice or a claim that a new quarter was analyzed.

Return after an interrupted run → see the earlier run as unfinished and can retry
to a fresh output; cross-session analysis resumption belongs to a later slice.

Ask for automatic note updates or twenty-year analysis → the skill explains this
slice's available data operation and the missing later capabilities without
advertising unimplemented behavior or modifying existing notes.

All errors preserve existing research; no operation rewrites, deletes or sends
private vault content. Public requests disclose the requested public issuer and
the explicitly configured SEC contact identity to SEC. No paid provider or
account subscription is introduced.
