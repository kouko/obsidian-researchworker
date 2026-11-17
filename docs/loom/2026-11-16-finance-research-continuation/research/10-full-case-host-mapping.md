# Fresh full-case host mapping

Date: 2026-11-17. Owning task: W3-01; no software or skill change.
Status: mapping prepared; isolated full-case study **not initialized**; no host/provider execution or publication.

## Decision and retained boundaries

Use a fresh study at `/private/tmp/finance-fullcase-v9-20261117`, rather than
repairing the old host root or retroactively attaching a predecessor. The old
root's Q2/Q3 reviews both use August 2 UTC. The accepted research instead uses
Q2 `2024-05-03T23:59:59-04:00` and Q3 `2024-08-02T23:59:59-04:00`.
Neither changing their labels nor run07/08's growth/identity no-work demonstrates
the full investment case. Preserve those reports, failures and counters.

The FINAL acceptance section of
`/private/tmp/finance-program-studies/docs/finance/research/apple-stage-c-v9-economic-acceptance.txt`
accepts the finite conditional economic research; it explicitly withholds whole
Stage C behavior acceptance. Reuse that work. Do not restart valuation, require
unobservable future actual values, or force a rating. Actual fair value remains
unidentified; that is a researched conclusion, not an infinite missing task.
The original software terminal/finalizer evidence, scope-specific host failures,
whitespace failure and whole-root additions audit failure remain historical facts.
This mapping changes none of them or the current review/cap accounting.

## Files inspected and bounded integrity check

Research checkout: `/private/tmp/finance-program-studies`, HEAD
`6dc54ecee0547572e9f65c25577b2c441e27654f` (read-only).
Read v9 economic acceptance including original whole-C limits, both v9 quarterly
syntheses, economic decision, both v9 manifests, and selected dependency records:
connected-equity-v2, correction-materiality, governance-risk-v1/v2, competition,
risk-baseline, equity-risk-basis, ERP reference and price evidence. Read current
skill/method, README version-1 contracts, intent/spec/plan, old SCOPE and asset/
filing metadata. Reading selected records is not recursive primary diligence.

Computed SHA-256 for all 6 direct dependencies of
`synthesis-v9/economic-decision-evidence.json` and all 43 unique direct dependency
paths across cases in `synthesis-v9/evidence.json`: all matched their recorded
digests. This is **only direct bytes verification**, not recursive provenance,
original publication authentication, full reading, or new economic acceptance.
The economic decision manifest includes the acceptance report itself; do not
treat this dependency cycle as independent evidence of correctness.

Two supplied original HTML files were read as bytes and checked for declaration
markers; this did not amount to substantive rereading of every filing section:

| Original | Bytes | SHA-256 |
|---|---:|---|
| `/private/tmp/apple-stage-a-q2/sec-run-xm9kia6b/raw/primary-0000320193-24-000069.html` | 884950 | `7a327c99c4a2c29341682d2ab5bb2465cb4e899341374ddaf565012e0d480991` |
| `/private/tmp/apple-stage-a-q3/sec-run-05erqm5p/raw/primary-0000320193-24-000081.html` | 889240 | `953b1e0d484cabbcb8308b0f362bb0304c14f06b3604b7770f7f0f9ea1f0e931` |

## Exact initialization proposal

All referenced files must be immutable regular in-root files beneath `investing/`;
no symlinks to either old checkout. Copy retained public research preserving its
relative directory layout under `investing/imports/finance-program-studies/`.
Retain the old full host root there only as an immutable historical import, never
as current managed reviews. No copied `cycles/` is placed in the active asset.
Verify each copied file against its actual original digest; import provenance
does not create historical economic availability.

Active files:

```json
// investing/research.json (JSON object only; omit this comment)
{"version":1,"assets":["aapl"]}
// investing/assets/equities/aapl/asset.json
{"version":1,"id":"aapl","issuer":"AAPL","questions":[
 {"id":"growth","required_sources":["filing-{fiscal}"],"required_analysis":["fullcase-method"],"depends_on":[]},
 {"id":"identity","required_sources":["filing-{fiscal}"],"depends_on":[]},
 {"id":"investment-case","required_sources":["filing-{fiscal}"],"required_analysis":["fullcase-method","case-assumptions-2024Q2","case-assumptions-2024Q3"],"depends_on":["growth","identity"]}
]}
```

The helper only expands `{fiscal}` in source requirements. Use two literal local input IDs
`case-assumptions-2024Q2` and `case-assumptions-2024Q3`, each containing only its
authored conditions and no economic observations. Both are authored in 2026 and
may be present at both reconstruction cutoffs; changing either would conservatively
invalidate both investment-case units. This avoids inventing a selector or
modifying runtime. The minimal required filing dependency does not imply a filing
alone answers the investment case: the completed unit must additionally freeze
each actual material consumed economic input below. The research self-check owns
that substantive sufficiency judgment, as the existing contract requires.

The financial source metadata must use these exact identities (not price dates):

| ID | Fiscal year/period/end/accession | Known filing availability |
|---|---|---|
| `filing-2024Q2` | 2024 / Q2 / 2024-03-30 / 0000320193-24-000069 | 2024-05-03 |
| `filing-2024Q3` | 2024 / Q3 / 2024-06-29 / 0000320193-24-000081 | 2024-08-02 |

Each retains original HTML with `raw_format: text` and complete decoded
`projection.raw_text`; relevant typed numeric projections additionally retain
periods/units and declared identities. Date-only filing availability is sufficient
for these end-of-day cutoffs; no intraday acceptance/tradability claim follows.
Do not use transformed packs as if they were raw filings.

Use individual material source IDs for the remaining inputs below; never give
unrelated inputs one bundle publication date. Quarter-specific projections and
optional excluded evidence preserve their own provenance. Configuration can be
initialized before all analysis is finished; there are no completed units yet.

## Required classification and source mapping

| Material retained dependency | Correct classification / availability / case filter |
|---|---|
| v9 syntheses, decision, prior v4/v8, model outputs and readbacks | Authored 2026 research/output imports, not original 2024 disclosures and not generic methods. Preserve conflicting old partial labels; new managed analysis explains FINAL acceptance precedence without rewriting imports. |
| Bundled research-method.md | Generic method stays in skill. Local `fullcase-method` is only digest/version identity plus selected convention (0–3, 3–12, 12–60 months), with actual timezone-aware authorship at initialization. |
| Product 3%, services 10%, R&D 14%, SG&A 5%, stable 2%, five-year neutrality, SBC treatment, conditional delta/U | Applied, explicitly authored 2026 assumptions; preserve why selected, counterexample and non-prediction limits. Historical anchors remain separately dated economic inputs. Five years is not issuer guidance. |
| Q2/Q3 original, earlier same-season originals, annual notes, FY2023 annual risk/lease/debt baseline | Individual economic records; current Q2/Q3 dates above, FY2023 10-K 2023-11-03. Earlier originals must be individually inventoried, not inferred from later comparative rows. Annual risk record says full raw annual HTML not retained. |
| Proxy, vote, ownership amendments | Proxy available 2024-01-11, table observation 2024-01-02 with older institution footnotes; vote 8-K 2024-02-28; Vanguard 2024-02-13; Berkshire 2024-02-14. Selected passage evidence retained; governance manifests say full raw files absent. Do not certify original byte identity. |
| DOJ complaint / EC original release | 2024-03-21 / 2024-06-24. Q2 excludes June EC release; updated 2025 web bodies only corroboration, not vintage originals. Record selected complaint pages 76–77 and EC two-page scope. |
| IDC releases / Samsung | 2024-04-15 08:30 -04:00 and 2024-04-30 eligible both; 2024-07-15 08:30 -04:00 and 2024-07-31 Q3 only. Units and fiscal/calendar mismatch retained. IDC distribution copies are attributed research, not issuer revenue. |
| Fed / BLS | Q2 2024-05-01 / 2024-05-03; Q3 2024-07-31 / 2024-08-02. Original initial-release vintages, not later revisions; preserved excerpts require their own actual byte/provenance mapping. No new requests. |
| Reuters/LSEG expectations, ROIC transcript | Reuters 2024-05-02 June-quarter expectation is Q2 eligible; Q3 target differs, no substitute September consensus invented. ROIC call label 2024-05-02 is not proven first publication; raw HTML/audio unretained. Keep attribution/unknown publication qualifications. |
| Yahoo close reference | Observations 2024-05-03 / 2024-08-02, retrieved 2026-11-15; 183.38 / 219.86 USD, unadjusted. Original 2024 vendor publication bytes not authenticated. No current meta/adjusted close or timestamp-as-close-time. |
| ERP monthly workbook / betas23 / Apple2024.xlsx | Individual external economic/model inputs, not generic method. ERP May/Aug rows are observation dates, publicationTimestampVerified=false; beta archive year is not proof of vintage. Published model is an attributed dated external reference, not issuer fair value. Preserve unknown availability rather than invent May/Aug publication. |
| Capital allocation, cash-debt, forecast-v2, connected-equity-v1/v2 and materiality evidence | Mixed authored calculations plus historical inputs. Split case-specific conditions, historical source rows and excluded later economics; never classify the whole JSON as a method. Preserve explicit once-only cost/tax/principal comparisons and no-total-valuation-bound limits. |

This table is a mapping for inspected families, not a completed recursive source
inventory. Unknown original availability remains unknown/excluded. If a conditional
scenario reuses a numerical coordinate from an unauthenticated historical series,
name it as a chosen coordinate and retain its separate excluded economic provenance;
do not present it as a known-at-cutoff economic fact or silently reclassify the
series as an assumption. Required unknown inputs would keep a question pending.
The accepted finite non-identification conclusion may omit such a factual claim;
that requires explicit case-level reasoning, not merely changing metadata.

## Remaining bounded work and actual next step

No `discover` call was made: no prepared study exists, so there is no initial
discovery observation to report. No newly identified missing economic calculation
blocks the accepted finite conclusion. The concrete missing preparation is the
active source/analysis metadata and the case-specific claim projection, not
recursive certification of every original. In particular, v9 Q2 financial and
macro claims can use the retained Q2 original and saved May Fed/BLS observations;
Q3 must use its own original and July/August observations. Shared research records
must be projected by named case instead of copying later Q3 observations into Q2.

The minimum offline preparation is: copy the immutable public imports and two
HTML originals; write the exact root/asset configuration above; write a compact
applied-method identity and two actual-authorship assumption manifests; then
create one individual source record per material saved economic observation
actually used (filings, macro, competition, governance, price and expectations).
A saved excerpt/observation is admissible retained evidence with a hash of its
actual local bytes and explicit capture/provenance qualifications; it must not be
called an authenticated full original. Known original publication dates remain
distinct from capture dates. Source unknowns such as first-published ERP vintage
remain excluded from factual-at-cutoff claims, while the accepted model may retain
explicit numeric reference conditions and the final non-identification decision.
This adapts provenance without recomputing the accepted economic model. It does
not require network recovery, a new provider call or unavailable primary bytes.
The subsequent host's substantive work is to bind those saved claims/conditions
and final economic acceptance into new checked managed outputs, not to repeat
old accepted research or predeclare their completion here.

Then import the **actual** helper with Python 3.11+ and call
`research_store.discover(root, "latest", "2024-05-03T23:59:59-04:00")` read-only.
Latest mode here selects eligible saved Q2 at later requests; historical mode
requires exact saved cutoff and would not demonstrate reuse across May/Aug.
With no active reviews it must identify Q2's three questions as pending and
exclude Q3, never report completion. Do not prepublish checks or reviews.

Parent's later authenticated source-host preflight precedes any host run:
first fresh host performs the May Q2 full case from preserved accepted research;
second at August detects Q3 and reuses Q2 with its original May cutoff; third
unchanged request demonstrates full-case no-work without another publication.
All three questions remain required. Full case includes business, financials,
competition, governance, valuation, risk and all three horizons. A new managed
answer must reconcile stale v9 partial/pending language against final economic
acceptance and retain actual evidence limitations. No fabricated current-SEC
freshness or `last_success` advance. Source/method change and interrupted recovery
have only their original bounded evidence until targeted full-scope trials run.

No network, credentials/config, installation, provider/model invocation, formal
vault write, outbound message, commit, push or merge occurred in this task.

## Actual offline setup — 2026-11-17 (supersedes proposal status above)

Parent authorized the concrete offline initialization after reviewing this mapping.
Created `/private/tmp/finance-fullcase-v9-20261117` with 305 byte-verified public
copies (303 pilot/research imports, 2 original HTML files), active configuration,
22 economic metadata records, 6 explicitly excluded provenance metadata records,
3 local analysis inputs, and no reviews/checks/completed units. Full source/copy
mapping and evolving preparation evidence live outside that root at
`/private/tmp/finance-fullcase-v9-preparation-evidence/`. No old root was edited.

**Corrected local dependency proposal:** do not require both quarter assumption
IDs in both investment-case units as proposed above. Actual configuration requires
only `fullcase-method` for investment-case. Each actual published unit must freeze
its own `case-assumptions-2024Q2` or Q3 additionally in `analysis_inputs`.
`research_store.py:_analysis_valid` validates the union of required and consumed
IDs; normal `_validate_proposal` calls `_snapshot`, which calls that validator.
Read-only frozen-input validation confirmed all 3 local records load. This avoids
inventing cross-quarter dependencies or requiring unsupported analysis templates.
Actual local authorship is `2026-11-17T02:56:00.143610+00:00`; these are preparation
manifests incorporating explicitly attributed 2026 research, not 2024 predictions.

**Retained initialization correction:** the first discover had 28 active sources,
including 7 unknown-publication records. The assessor raises issuer-wide gaps for
all active unknown sources, even if no question consumes them. Six records were
then classified outside active sources for a substantive reason: two retrospective
price references, two monthly ERP coordinates, one industry beta reference and
one third-party net-neutral direction are only attributed conditional reference
inputs in this study, not established known-at-cutoff facts. They retain original
metadata, `available_at: null`, hashes, raw observations and qualifications under
`data/excluded-observations/`; actual SCOPE explains each claim and limitation.
This is an explicit initialization choice, not an unchanged-history claim.

An intermediate 21-active/7-excluded discover is also retained. On further
claim-level review, Q3 expectations was restored as active unknown: v9 adopts its
September guidance attribution as an economic premise, not merely a numerical
coordinate. Thus final discovery honestly retains that precise unresolved gap.
No unknown was backdated or silently converted to method. BLS availability was
conservatively simplified from a scheduled-time coordinate to its known release
date, sufficient for end-of-day cutoffs; original initial metadata bytes were
reconstructed, digest-matched against the first snapshot, and retained outside
the root. Initial, intermediate and final observations/hashes remain separate.

Actual read-only latest-mode results:

| Exact cutoff | Pending work | Reusable | Exclusions / extra availability gap |
|---|---|---|---|
| May 3, 23:59:59 -04:00 | Q2 growth, identity, investment-case | none | Q3 filing/macro, July competition, June EC excluded; Q3 expectation unknown excluded and issuer-wide gap retained |
| August 2, 23:59:59 -04:00 | Both quarters' three questions | none | Q3 expectation unknown excluded, issuer-wide gap retained for both quarters |

Both statuses are partial and external_freshness is unverified. There is no
last_success or accepted/reusable quarter. Each discover's before/after complete
file hash map was identical. No provider/host run occurred. Root `SCOPE.md`,
input inventory and owning `evidence/full-case-preparation.md` identify exact
source IDs/dates and the unresolved premise. Actual host entry is not authorized
by preparation; parent first evaluates whether the unknown-timezone expectation
can be established by cutoff or whether final finite reasoning can omit that
premise without weakening scope. No new economic model is required by this issue.

## Q3 expectation eligibility qualification — subsequent bounded update

Parent authorized an independent mathematical/contract check, not a timezone
guess. Recomputed from retained original strings: publication August 1 16:33,
update August 2 01:20, display timezone null. For any civil offset o with |o| <24h,
UTC = local−o < local+24h. The update therefore has strict conservative UTC upper
bound `2024-08-03T01:20:00+00:00`, 9599 seconds before the actual Q3 cutoff
`2024-08-03T03:59:59+00:00`. Independently enumerated all 2879 minute offsets
−1439 through +1439; the inequality itself covers every continuous offset too.
The earlier publication has an earlier bound. Assumptions: displayed timestamps
are normal civil dates and selected attributed content belongs to that dated
report/update rather than undated later additions. Mathematical qualification
does not independently authenticate either assumption or the historical page.

README requires an ISO availability field, identity, relevant typed projection,
original raw reference/digest and visible qualifications; the loader/assessor
uses availability only as the eligibility boundary here. It does not require an
exact first-publication instant for this sole revision. The bound is therefore
represented conservatively, with explicit top-level `available_at_semantics` and
full `availability_bound` inside the frozen projection. It is not a general
claim that bound timestamps can order overlapping competing source revisions.
No runtime/skill contract or code was changed.

The source remains active, its identity version changes to bind this substantive
qualification, and the exact pre-change metadata is preserved in external audit
`qualification-history/expectations-2024Q3-pre-bound-metadata.json`. Its raw
observation and imported original record are byte-unchanged. Exact timezone and
actual publication instant remain unknown, historical-vintage certification
remains false, and September consensus remains null. Root SCOPE and a digest-bound
qualification sidecar carry these conditions; no first-published UTC was invented.

New read-only discovery preserves all previous outputs in qualification-history:
May has Q2's three pending questions, excluding this later bound and Q3 originals;
August has both quarters' six pending questions and no time-unknown gap. Both
remain partial solely for unpublished question work, with zero reusable units,
no accepted-quarter/last_success advance and external freshness unverified.
Full root hash maps were unchanged by discovery; all 305 source/copy pairs remain
unchanged. No publication, model/provider CLI, network, skill/runtime edit or
commit occurred. This resolves the narrow eligibility premise conditionally,
not the pending full-case host behavior acceptance.
