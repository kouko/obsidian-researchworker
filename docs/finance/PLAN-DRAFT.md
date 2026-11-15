# Obsidian Finance — research and implementation planning draft

Status: proposal; planning only. Created 2026-11-15.
This document does not authorize implementation, installation, vault changes,
paid services, background execution, publication, or merge. It is not a confirmed
Loom intent, ratified specification, or executable station plan.

## 1. Outcome and confirmed requirements

Provide repeatable, source-traceable investment research in Obsidian. Preserve
historical analyses and update them by quarter, with separate short-, medium-
and long-horizon recommendations. Recommendations are conditional research
judgments, not automatic transactions or mandatory portfolio allocations.

Confirmed by the user:

- Start with US equities, with Apple as the primary historical case.
- Cover at least twenty historical years; a quarter is the smallest analysis unit.
- Do not infer a twenty-year holding period. Holding period remains unspecified.
- Validate the skill across different industries, not just Apple or big technology.
- Eventually cover companies, ETFs, commodities and currencies.
- Retain dimension-specific notes and a period-specific integrated assessment.
- Put reusable methods and quality rules in skills, not duplicated vault policy.
- Transplant any reused Monkey Skills tooling here before using or modifying it.
- Treat Monkey Skills as read-only and eliminate runtime dependencies on its paths.

Candidate direction, not a confirmed requirement: a sibling optional plugin named
`obsidian-finance` in this repository, separate from the existing `obsidian` plugin.

## 2. Scope and alternatives

| Choice | Benefit | Cost / limitation | Proposed handling |
|---|---|---|---|
| Add finance to obsidian | One distribution surface | Couples ordinary notes to finance dependencies | Not preferred for this scope |
| Sibling optional plugin | Independent installation, dependencies and release | More manifests and host verification | Preferred, validate before implementation |
| Separate repository | Independent ownership | More coordination, no demonstrated need | Exclude for now |
| Research documents only | Small, reversible learning step | No runnable capability | Current authorized work |

Use a small equity implementation to learn, while retaining the full historical
and cross-asset objective. Do not silently redefine success as two quarters or
shorten twenty years to match a convenient API. Cross-asset delivery follows
equity evidence, not a universal template assumed in advance.

## 3. Ownership and packaging

| Owner | Responsibility | Must not own |
|---|---|---|
| Finance plugin | Acquisition, financial computation, research methods, longitudinal records, synthesis | User-specific risk limits embedded as global defaults |
| Existing obsidian plugin | General note, diagram and vault capabilities | Finance-specific acquisition dependencies |
| Vault | Personal investment settings, sources, datasets and actual research | A copied, separately maintained generic research manual |
| Repository docs | Design decisions, research evidence, provenance and validation | Private portfolio contents or credentials |

Proposed source root: `obsidian-finance/`, with skill instructions, bundled method
references, executable scripts, tests, licenses/provenance and host metadata.
Exact internal layout and public skill names are design outputs, not fixed here.
Do not mirror the toolkit's complete skill count or three-layer directory tree
merely to preserve its appearance.

Default design target: finance must be usable without undocumented cross-plugin
calls or Monkey Skills/domain-teams installation. Choose a minimal standalone
Markdown output path; optional obsidian assistance must have explicit availability
checks. Avoid a shared runtime package until concrete duplication warrants it.
Skill availability, source registration, installation and actual fresh-session
execution are separate validation claims.

## 4. Research program: bounded questions, not an up-front encyclopedia

| Study | Consequential question | Output / exit evidence |
|---|---|---|
| Data coverage | Which periods, statements and narratives can actually be acquired? | Per-company coverage matrix with gaps, source dates, costs and rights |
| Equity methods | What must every company analysis cover, and where do industries differ? | Common core plus justified industry-specific additions |
| Report design | Which separate notes improve judgment rather than duplicate it? | Example dimension notes, synthesis and cross-period review |
| Recommendation horizons | What do short/medium/long mean for quarterly research? | Explicit durations, benchmarks, assumptions and validity conditions |
| Historical reconstruction | What was public at each decision date? | Historical cutoff and revision policy demonstrated on real filings |
| Prior art | Which existing systems solve these exact problems? | Source-inspected reuse findings, including limitations |

Start with prior local research and recheck its original citations. In particular,
do not repeat the July prior-art survey's universal absence or leadership claims
without current source inspection. Research official methodologies, real analyst
reports and original project implementations; distinguish financial standards,
issuer disclosures, vendor claims and local design inferences.

Each study retains question, conditions, sources, conclusion, limits and the
decision it changes. Stop when enough evidence supports that decision. New
research is triggered by a concrete gap, contradiction or failing case, not by a
quota. Methods, report structure and industry extensions remain revisable.

## 5. Case selection

| Company | Reason for inclusion | Initial depth |
|---|---|---|
| Apple | Primary long-history and product/business transition case | At least twenty complete fiscal years, quarterly coverage tracked |
| Microsoft | Subscription/cloud transitions and segment changes | Selected comparable quarters and transition cases |
| JPMorgan Chase | Bank accounting, credit and capital require different methods | Normal and stress-period cases |
| ExxonMobil | Commodity cycles and capital-intensive operations | High/low-cycle cases |
| Costco | Membership retail and operating efficiency | Selected comparable quarters |

These are proposed validation cases, not investment recommendations or a claim
of full industry coverage. The smaller first contrast set is Apple, JPMorgan and
ExxonMobil; Microsoft and Costco extend it before a broad cross-industry claim.
Do not require twenty years of all five companies to validate a first workflow.
Add a failed, acquired or delisted case before claiming broad historical validity;
successful survivors alone do not test failure handling.

## 6. Historical data and time semantics

Track independently: fiscal period start/end, source publication date/time,
retrieval time, research cutoff and analysis completion time. Keep fiscal years
distinct from calendar years, and handle 52/53-week accounting calendars.

Two outputs have different information rules:

1. Historical decision reconstruction uses only information public by its cutoff.
2. Retrospective review may use later outcomes, clearly labeled as hindsight.

A quarter-end cutoff cannot use financial results published afterward. A
post-earnings review may use that filing but must declare its later cutoff and
contemporaneous price. Comparing outcomes must not start a hypothetical trade
before the recommendation could have existed.

Retain original statements and amendments as separate versions. Never overwrite
past judgments with later knowledge. Mark corrected, derived and unavailable
values explicitly; missing is not zero. Preserve currency, units, consolidation
basis, concept changes, share splits and price-adjustment settings.

Pin the historical window at run start: at least twenty complete fiscal years
ending in the latest eligible completed year, plus any subsequent eligible
quarters if needed. Report every required quarter as complete, partial or missing;
do not call an annual comparative figure a complete quarterly record. Extend
farther back if required to obtain the requested full window.

Price histories need explicit split/dividend and total-return conventions.
Historical macro releases need historical publication versions, not simply today's
revised series. Original filing text, operational indicators and competitor
evidence need coverage checks separate from three-statement coverage.

## 7. Tool transplant plan

Reference revision and bounded probe: [tooling assessment](../loom/research/2026-11-15-investment-tooling-reuse.md).

| Candidate | Reuse purpose | Dependency / evidence required before acceptance |
|---|---|---|
| SEC adapter and cache | Filing identifiers, downloads and raw source retention | SEC identity configuration, rate limits, failures, paging and isolated cache |
| Quarterly series helpers | Stitch statements and derive discrete quarters | Acquisition dependencies, period classification, arithmetic and partial-result semantics |
| KPI/version store | Preserve source-linked observations and revisions | Schema, filesystem helpers, locking, date semantics and cutoff queries |
| Yahoo adapter | Price history | Adjustment behavior, requested span, missing data and source-use conditions |
| FRED adapter | Macro observations | Historical vintage support; existing latest-series adapter alone is insufficient |
| DCF / comparable valuation | Deterministic calculations | Input assumptions, industry suitability and numerical checks |
| Report/method references | Workflow and document precedents | Remove hidden domain-team/runtime dependencies; revalidate source claims |

Sequence: select a dependency-complete subset; preserve source revision and
licenses; transplant source and useful behavior tests; run only the transplanted
copy in an isolated project environment; then adapt and evaluate. Do not copy
personal cache, data stores, keys or installed plugin state. No original-repo
absolute imports, subprocess paths or dependency on an installed source plugin.

Directly verify transfer provenance and discard migration-only machinery. Retain
tests for enduring behavior such as dates, arithmetic, revisions and failure
handling. Do not run setup scripts or adopt the entire market/provider stack by
default. Package/environment selection belongs to the technical plan.

## 8. Vault layout and document responsibilities

Preserve existing `investing/memos/`, old investing notes, external references
and automated reading-list output. New content uses a separate bounded subtree;
no bulk migration is needed to validate it.

| Proposed vault-relative path | Content |
|---|---|
| investing/投資研究總覽.md | Watchlist, latest completed reports, research in progress |
| investing/投資設定.md | Optional personal currency, objectives and constraints |
| investing/shared/macro/ | Dated shared macro analyses |
| investing/shared/industries/ | Dated industry/comparable-company analyses |
| investing/shared/themes/ | Dated cross-industry themes |
| investing/assets/equities/{stable-id}/ | One company's overview and history |
| investing/assets/equities/{stable-id}/cycles/{cutoff}-{review}/ | One review's progress, dimension notes and integrated assessment |
| investing/assets/equities/{stable-id}/events/ | Material changes between formal reviews |
| investing/assets/equities/{stable-id}/data/ | Durable source manifests, needed snapshots and calculations |
| investing/portfolio/ | Optional portfolio-level research, outside the first equity slice |

Other asset subfolders appear only when implemented; do not create empty trees
or nonexistent-note links. New dated notes follow `YYYY-MM-DD {asset-id} {topic}.md`.
The durable identifier must disambiguate listing/entity and survive renames;
ticker and issuer filing identifier are separate metadata, not interchangeable.

Dimension notes share an envelope: asset identity, fiscal coverage, cutoff,
status, method version, source links and predecessor. Their bodies differ by
question. Start with financials, business operations, industry/competition,
valuation/scenarios and synthesis, merging short overlapping dimensions.
Governance, capital allocation and risks must have explicit coverage even if not
separate files. A linked shared study must also be a version eligible at cutoff.

The integrated report records thesis, price/date, horizon-specific recommendation,
supporting and contradictory evidence, scenario assumptions, risks, invalidation
conditions, missing evidence, prior-period changes and next review triggers.
It does not average arbitrary dimension scores into a recommendation.

Completed reports are preserved; corrections and new judgments are linked new
versions. Each cycle's progress record tracks unfinished questions and next work.
Mark completion explicitly and update overview pointers; modification time is
not a reliable indicator of the latest completed report.

Raw large datasets may use a project-owned durable data directory with paths,
hashes and source manifests in the vault. Decide portable backup behavior before
adopting external storage; temporary cache is never the only evidence copy.

## 9. Research flow and interruption

| Activity | Persisted result | Required failure behavior |
|---|---|---|
| Establish scope/cutoff | Cycle identity, eligible sources and budget | Missing scope cannot become implicit personal advice |
| Acquire and validate | Source manifests, coverage and normalized facts | Partial fetch stays partial; preserve usable evidence |
| Analyze dimensions | Cited findings, assumptions and unknowns | Conflicts stay visible; no invented numbers |
| Synthesize and challenge | Conditional horizon judgments and counterevidence | Permit insufficient-evidence result |
| Publish locally after validation | Completed report and overview pointer | Interrupted write must not advertise an incomplete report as complete |
| Resume / compare | Pending work and linked comparison | Do not restart all completed work or reuse ineligible later evidence |

Persist after meaningful units. Rerunning the same source/cycle must not duplicate
records. Distinguish retryable transport failure, missing disclosure, invalid
data and analytical uncertainty. Avoid silent fallback to an unrelated company,
provider, annual period or current-data substitute. The first implementation is
user-triggered; background scheduling and notifications are separate capabilities.

### 9.1 Automatic update assessment when an agent runs

User clarification, 2026-11-15: after the folder structure is established, later
agents should inspect its files and changes, decide whether existing analysis
needs updating or a new period needs analysis, and perform the relevant work
with relatively little manual direction. This is a core longitudinal behavior,
not merely an optional scheduler enhancement. No always-running host is implied.

Proposed operation: when invoked for investment work in this vault, read the
watchlist/asset overviews and in-progress cycle records, inspect eligible new
disclosures when connectivity and permissions allow, classify necessary work,
and execute only that work within the established scope and budget. The user
should not need to choose every outdated note or manually create every quarter.
Exact invocation/automatic skill-trigger surfaces require the behavioral spec;
do not scan or launch investment work on unrelated vault requests.

Folder paths and filesystem modification times help discovery, but modification
time alone is insufficient: formatting changes, sync/restore, copied files and
unchanged local files despite new external disclosures can mislead the decision.
Use completed-period status, the information cutoff, source accession/revision,
the source versions actually consumed and actual content changes as authoritative
inputs. A recently edited report may still be analytically out of date.

| Observed condition | Proposed action | Completion evidence |
|---|---|---|
| New disclosed quarter with no completed cycle | Start that quarter's analysis | New cycle with eligible source versions and integrated report |
| Existing cycle interrupted or incomplete | Resume missing work | Completed work reused; outstanding work explicitly resolved |
| New eligible source or amendment affects an existing conclusion | Reanalyze affected dimensions and synthesis | Linked new analysis version; old completed report preserved |
| Shared input analysis changes substantively | Recheck dependent conclusions | Impact identified from recorded input versions; no blind whole-vault rewrite |
| Only formatting, link display or sync timestamps change | Do not regenerate financial analysis | Explain why no analytical update was needed |
| No new relevant evidence, cycle complete and review not due | No analysis generation | Recorded checked state and a short no-work explanation |
| Review due but no new relevant evidence | Revalidate; retain conclusion if supported | Record review without fabricating changed financial facts |
| External sources cannot be checked | Report freshness unknown | Keep last successful check distinct from last attempt; no false up-to-date claim |
| User edited a managed report | Preserve and reconcile or report conflict | User edits retained; no silent overwrite |

Store only the minimal durable state needed for these decisions, preferably
existing note properties and source manifests; do not add a global database,
file watcher or extra dependency engine without demonstrated need. A last-checked
date is not a substitute for the data cutoff or the source version used. Repeated
invocation with unchanged inputs must not create duplicate cycles or new advice.

Stage C must demonstrate this decision behavior on a small interrupted/new-quarter
case, and Stage F must demonstrate it across real fresh host sessions. These gates
must precede any claim of automatic ongoing maintenance. Stage G adds background
initiation only if separately requested. The initial acquisition slice supplies
source identity/dates and honest failures; it does not yet perform this maintenance.

## 10. Staged delivery and stopping gates

| Stage | Deliverable | Evidence required to advance |
|---|---|---|
| A: definition and evidence | Confirmed scope, method studies, source coverage, report examples | Historical semantics and first report behavior are defined; unknowns recorded |
| B: minimal transplant | Independent finance package with selected tools | Operates without Monkey Skills or personal cache; retained behavior tests pass |
| C: complete small equity case | Two adjacent Apple quarters with dimension and synthesis notes | Source traceability, cutoff exclusion, cross-period changes, automatic work selection and interruption/resume demonstrated |
| D: industry contrasts | Bank, energy and other proposed contrast cases | Industry-specific methods and unsuitable-model refusals demonstrated before large historical generation |
| E: historical expansion | At least twenty-year Apple coverage ledger and period research | Every expected quarter accounted for; complete target reached or explicitly remains unmet |
| F: agent-assessed ongoing research | New-quarter/update/no-work decisions in selected real hosts | Fresh-session discovery, source checks, incremental updates, isolated vault operation and rollback evidence |
| G: additional assets / automation | Separately scoped ETF, commodity, FX or scheduler changes | Asset-specific methods, instruments, providers, failure handling and acceptance |

Coverage-ledger generation is not twenty years of completed analysis. Historical
expansion can run in bounded batches, but completion requires both the requested
coverage and substantive period outputs. Measure real cost/time on the small case
before estimating the whole history; no unsupported token, API or calendar budget.
Set user-approved spending limits before paid work. Do not bypass unavailable
data or quota failures by silently substituting weaker results.

## 11. Acceptance evidence

- Twenty-year quarterly coverage: expected fiscal periods reconcile against
  actual sources; missing dimensions/periods are visible and do not count as complete.
- Numerical quality: representative values and derived quarters reconcile to
  original filings, units and calculation inputs, including negative/boundary cases.
- Historical integrity: a later amendment or release cannot enter an earlier
  reconstruction; hindsight review remains separately labeled.
- Cross-period reasoning: changed recommendations identify changed facts,
  assumptions, prices or methods; contradictions and errors remain reviewable.
- Recommendation integrity: short/medium/long judgments have explicit horizons,
  conditions and limitations; unknown personal constraints do not become sizing advice.
- Resumption: a fresh session continues an intentionally interrupted case;
  rerunning completed acquisition does not duplicate durable records.
- Update assessment: a fresh session identifies a new quarter, affected older
  analysis and unfinished work from durable records and source changes; formatting
  or sync-only timestamp changes do not trigger full reanalysis. Unchanged inputs
  produce no duplicate cycle, and unavailable source checks remain unknown.
- Industry transfer: finance/energy cases do not receive inappropriate generic
  industrial-company models; absent data is explicit.
- Vault integrity: no unauthorized old-note changes; links resolve; incomplete
  cycles never appear as latest completed reports.
- Package independence: source repository and original plugins are unavailable
  during the independent test; no hidden cross-plugin path remains.
- Host validation: label each host as untested, installed, invoked or full-case
  verified, rather than claiming support from manifests alone.

Research quality is not established by passing software tests. Review actual
reports against original source material and adversarial examples separately.
Investment performance claims require a separate point-in-time evaluation with
benchmarks, costs, outcome windows and selection-bias treatment; none are claimed here.

## 12. Risks and decisions still needed

| Risk / open item | Current handling |
|---|---|
| Older unstructured filings / incomplete narrative history | Research acquisition options; do not infer completeness from companyfacts |
| Hidden dependency closure in transplanted tools | Trace imports, subprocess targets and environment/config before copying |
| Financial model and citation errors | Deterministic calculations plus source-level review and explicit uncertainty |
| Oversized per-quarter file count | Split only meaningful dimensions; reference unchanged eligible work |
| Automation cost growth | Measure bounded batches; explicit budgets and stops |
| Generic plugin versus personal finance settings | Methods bundled; private choices/data remain local |
| Plugin name and installation scope | obsidian-finance is provisional; host choice must be explicit before host testing |
| Short/medium/long boundaries and benchmark | Decide from method research before report acceptance; not universal constants |

Agent-decided proposals: sibling package, no external runtime dependency, no new
shared framework, standalone basic Markdown output, Apple depth plus contrast
cases, and manual initiation before scheduling. These are reasoned proposals,
not user-ratified architecture.

## 13. Next authorized boundary

The current deliverable is this planning draft. Do not transplant or implement
from it automatically. On implementation authorization, start capture-intent,
confirm outcome/scope, write the behavioral specification, then the concrete
file/task/test plan, build, review and acceptance. Research continues whenever
a consequential unresolved question could change those artifacts. Publication
and merge permissions are not granted by this document.

## 14. Cross-session progress and continuation

This document is the durable program plan. Research records contain evidence;
session handoffs contain operational restart state. Do not duplicate the entire
plan into each handoff or mark planned work as completed research.

Snapshot: 2026-11-15, Stage A research has started on user direction. The first
acquisition-slice intent was confirmed; its behavioral specification is next.
No runtime has been transplanted or implemented.

| Stage | Current status | Existing evidence / immediate next action |
|---|---|---|
| A: definition and evidence | In progress | Initial primary-source revalidation and minimum acquisition scope recorded; full cross-industry coverage, report examples and horizons remain pending |
| B: minimal transplant | Not started | Select dependency-complete subset after package and scope decisions |
| C: small equity case | Not started | Depends on transplanted tools and researched report methods |
| D: industry contrasts | Not started | Candidate companies proposed; selected periods not yet chosen |
| E: historical expansion | Not started | Twenty-year target remains; complete quarterly availability unproven |
| F: ongoing research | Not started | No host chosen or finance plugin installed |
| G: assets / automation | Not started | Long-term scope only; no scheduling or trading authorization |

Next session's first substantive work should be Stage A: examine the original
sources behind the existing long-horizon study, produce an equity-method and
report-format comparison, and identify data coverage gaps for Apple plus industry
contrasts. This is research, not permission to transplant or execute source tools.
If the user instead directs implementation, use Section 13's intent/specification
boundary first. Do not repeat the entire requirements interview when the answers
are already recorded here.

Continuation update: the initial revalidation and acquisition-scope study now
exists. The intent in `docs/loom/intent/2026-11-15-finance-sec-baseline.md` was
confirmed after the automatic-update clarification; continue its specification,
not the intent interview or the completed initial study.
This first intake may prepare the data-only slice while unresolved method studies
continue; it does not waive the full Stage A exit conditions for advisory-report
implementation. The earlier handoff is a historical snapshot predating this work.

### Decision register

| Topic | Status | Basis / remaining action |
|---|---|---|
| Apple, at least twenty historical years, quarter minimum | User-confirmed | Holding period is not fixed; short/medium/long recommendations required |
| Cross-industry validation | User-confirmed | Exact case set and periods remain proposed |
| Transplant before reuse/modification | User-confirmed | Source repository stays read-only; no original-path runtime dependencies |
| Methods in skills, private conditions in vault | Planning agreement | No duplicated generic policy manual in vault |
| Sibling plugin / obsidian-finance name | Agent recommendation, provisional | Confirm product boundary and name before implementation |
| Short/medium/long durations | Unresolved | Method research must justify proposed definitions |
| Hosts, providers, paid budgets | Unresolved | Determine before related execution or spending |
| Vault layout and individual note templates | Proposed | Validate against real examples before standardizing |
| Agent discovers necessary analysis updates from vault/source state | User-stated desired behavior | Core Stage C/F requirement; modification time is a hint, not sufficient evidence; exact behavior remains to specify |

### Updating this record

After each session, update the stage table only against observed deliverables;
link new research and validation evidence; record changed decisions with reasons;
retain failed evidence and limitations; and state the next bounded action.
Separate planned, implemented, tested, installed and accepted states. Changes to
an accepted behavioral requirement need explicit reconfirmation; routine research
findings and technical choices need a reason, not a new approval ritual.

Research index:

- [Existing tool assessment and bounded Apple probe](../loom/research/2026-11-15-investment-tooling-reuse.md).
- [Primary-source revalidation and first-slice scope](../loom/research/2026-11-15-finance-first-slice-scope.md).
- [Confirmed acquisition-slice intent](../loom/intent/2026-11-15-finance-sec-baseline.md).

Session-specific restart instructions are saved separately under
`.claude/handoffs/`; consult the explicitly provided latest handoff path rather
than assuming a prior handoff describes the current repository state.
