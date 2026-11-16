# Obsidian Finance — research and implementation planning draft

Status: Stage A definition/evidence pilot completed locally; acquisition slice
separately accepted locally. Wider research implementation remains proposed.
Created 2026-11-15; Stage A completion recorded 2026-11-15.
This program document alone does not authorize implementation, installation,
vault changes, paid services, background execution, publication, or merge.
The separately confirmed acquisition intent/spec govern that slice; the wider
program remains a proposal, not an executable station plan.

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

Selected for the confirmed acquisition slice: a sibling optional plugin named
`obsidian-finance`, separate from the existing `obsidian` plugin. This selection
does not ratify the wider research architecture or authorize host installation.

## 2. Scope and alternatives

| Choice | Benefit | Cost / limitation | Proposed handling |
|---|---|---|---|
| Add finance to obsidian | One distribution surface | Couples ordinary notes to finance dependencies | Not preferred for this scope |
| Sibling optional plugin | Independent installation, dependencies and release | More manifests and host verification | Selected and implemented for the acquisition slice |
| Separate repository | Independent ownership | More coordination, no demonstrated need | Exclude for now |
| Research documents only | Small, reversible learning step | No runnable capability | Earlier boundary; confirmed acquisition implementation now exists |

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

Implemented acquisition root: `obsidian-finance/`, with one `sec-data` skill,
executable scripts, tests, licenses/provenance and Claude/Codex host metadata.
Additional research methods and layout remain future design outputs.
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

User clarification, 2026-11-15: use company fiscal quarter YYYYQq as the primary
research key, independently of issuer release schedules. The normal review is
a retrospective snapshot of the selected quarter; a historical decision
reconstruction has a separately declared information cutoff. Keep the actual
fiscal period, calendar-period mapping, release dates and revisions as metadata.
No calendar-month or current-year-end guessing for historical fiscal periods.
Quarter keys do not imply complete single-quarter statements or Q4 arithmetic.

Further user clarification, 2026-11-15: fiscal quarter selects the financial
reporting period, not a universal update frequency or a universal information
cutoff. A research assessment has its own as-of timestamp. Financials, prices,
market conditions, macro releases and material company events each retain
observation periods, public-release timestamps and source versions. All inputs
to one recommendation must have been available by that assessment's cutoff;
they need not share an observation period or release date. Financial analysis
may need prior quarters/years as comparisons, not only the selected quarter.

Preserve a release-time historical assessment separately from later current
assessments using the same financial quarter plus newer eligible market/event
evidence. Never overwrite the original judgment or use later market data in
its historical reconstruction. A later financial filing can be a new baseline;
do not describe the old selected quarter as the latest financial information
when newer eligible financial disclosures exist. Cadences below are design
candidates, not a shipped scheduler: financial filings per quarter/revision,
market/prices per assessment or trading day, macro per release, material
business/competitive events when relevant evidence changes. Only affected
research dimensions need updating; refresh synthesis when their conclusions
or recommendation inputs change. SEC acquisition alone does not implement
market/macro ingestion, valuations or investment recommendations.


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
| investing/assets/equities/{stable-id}/cycles/{fiscal-quarter}/{cutoff}-{review}/ | One review's progress, dimension notes and integrated assessment |
| investing/assets/equities/{stable-id}/events/ | Material changes between formal reviews |
| investing/assets/equities/{stable-id}/data/ | Durable source manifests, needed snapshots and calculations |
| investing/portfolio/ | Optional portfolio-level research, outside the first equity slice |

Other asset subfolders appear only when implemented; do not create empty trees
or nonexistent-note links. Quarter research notes use `{fiscal-quarter} {asset-id} {topic}.md` within their review directory; event notes retain `YYYY-MM-DD {asset-id} {topic}.md`. Multiple dated reviews of one quarter remain separate.
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
| Plugin name and installation scope | obsidian-finance selected for acquisition; host choice remains explicit before installation/testing |
| Short/medium/long boundaries and benchmark | Decide from method research before report acceptance; not universal constants |

The confirmed acquisition slice implements the sibling package with standard-library
runtime and structured JSON data output. Wider proposals include no new shared
framework, standalone research Markdown, Apple depth plus contrast cases, and
manual initiation before scheduling; they are not user-ratified wider architecture.

## 13. Next authorized boundary

The original deliverable was this planning draft. Do not transplant or implement
the wider program from it automatically. On implementation authorization, start capture-intent,
confirm outcome/scope, write the behavioral specification, then the concrete
file/task/test plan, build, review and acceptance. Research continues whenever
a consequential unresolved question could change those artifacts. Publication
and merge permissions are not granted by this document.

## 14. Cross-session progress and continuation

This document is the durable program plan. Research records contain evidence;
session handoffs contain operational restart state. Do not duplicate the entire
plan into each handoff or mark planned work as completed research.

Historical snapshot, superseded by the continuation below: 2026-11-15, first
acquisition-slice intent and behavior confirmed.
Independent spec and plan reviews completed; SEC acquisition transplant is
committed at 5a7c2bd, cutoff/output at 624c30d, and packaging at 0b7030f.
The combined suite passed 55 tests before independent adversarial/acceptance
review. No live new-tool acquisition, host installation or full research is verified.

| Stage | Current status | Existing evidence / immediate next action |
|---|---|---|
| A: definition and evidence | Completed locally within the bounded research gate | Method/report research, Apple two-quarter examples, source/coverage and unknowns recorded in pilots/apple-2024q2-q3/STAGE-A-COMPLETION.md; horizons remain labeled pilot conventions |
| B: minimal transplant | Accepted locally in the conversation | Accepted acquisition HEAD 08f65d9: 99 package tests and independent review; genuine-contact/fresh-host limits remain explicit |
| C: small equity case | In progress: actual Q2/Q3 research remains partial | Retained financial, valuation/forecast and competition evidence plus folder discovery/publication helpers and a source skill exist. Two-quarter analytical completeness, price/narrative evidence and independent research acceptance remain open; software passes do not close them |
| D: industry contrasts | In progress: four source-bound bank/energy method cases | JPM 2020Q1/2024Q2 and XOM 2020Q2/2024Q2 originals inspected; model refusals and cash-flow definition arithmetic retained. Full statements, valuation and independent research acceptance remain pending |
| E: historical expansion | Input inventory and partial early drafts only; zero completed historical-batch quarters | FY2006–FY2026 has 84 original filing candidates. Candidate count is not fiscal/source coverage verification or substantive quarterly research |
| F: ongoing research | Bounded actual host scenarios observed; full ongoing investment research incomplete | Eight new source-invoked Codex sessions demonstrate discovery, affected research/reuse, separate bounded complete-scope no-work and controlled save recovery/conflict. Failures and high token counts are retained; installed-plugin execution and global refresh remain unverified |
| G: assets / automation | Bounded ETF/commodity/FX method preparation and cases; full support incomplete | Method applicability and refusal boundaries do not establish full asset research workflows. No scheduler, trading, paid service or background execution authorization |

Earlier next-session guidance, superseded by the active-Build continuation:
Stage A should examine the original
sources behind the existing long-horizon study, produce an equity-method and
report-format comparison, and identify data coverage gaps for Apple plus industry
contrasts. This is research, not permission to transplant or execute source tools.
If the user instead directs implementation, use Section 13's intent/specification
boundary first. Do not repeat the entire requirements interview when the answers
are already recorded here.

Continuation update: the initial revalidation and acquisition-scope study now
exists. The intent in `docs/loom/intent/2026-11-15-finance-sec-baseline.md` was
confirmed after the automatic-update clarification; its behavior and task plan
were subsequently confirmed/reviewed. Continue the active Build, not the intent
interview or the completed initial study.
This first intake may prepare the data-only slice while unresolved method studies
continue; it does not waive the full Stage A exit conditions for advisory-report
implementation. The earlier handoff is a historical snapshot predating this work.

Current continuation, 2026-11-15: the earlier 74-test closing review preceded a
live after-hours filing failure and does not certify the fiscal-quarter amendment.
W6-01 (`f1408de`) repairs that false exclusion; W6-02 (`61b79c9`) adds
source-declared quarter selection. Scoped runtime tests passed 71 cases. A real
payload replay and one live CLI run both resolved AAPL 2024Q3 to 2024-06-29
and returned 125 eligible observations and 124 historical inventory filings at
cutoff 2024-08-15. The 124 filings are not 124 reports for this quarter.
The [recorded evidence](../loom/2026-11-15-finance-sec-baseline/evidence/quarter-replay.md)
separates synthetic tests, offline replays, live transport and unverified host
invocation. The live call used an explicitly authorized non-real test identity;
normal operation still requires the operator's genuine contact. New full-suite,
adversarial, closing-review and acceptance results remain pending. Continue that
existing Build/review episode without resetting earlier counts or publishing.

### Decision register

| Topic | Status | Basis / remaining action |
|---|---|---|
| Apple, at least twenty historical years, quarter minimum | User-confirmed | Holding period is not fixed; short/medium/long recommendations required |
| Cross-industry validation | User-confirmed | Exact case set and periods remain proposed |
| Transplant before reuse/modification | User-confirmed | Source repository stays read-only; no original-path runtime dependencies |
| Methods in skills, private conditions in vault | Planning agreement | No duplicated generic policy manual in vault |
| Sibling plugin / obsidian-finance name | Selected for confirmed acquisition slice | Package implemented; global installation and fresh-host invocation remain unverified |
| Company fiscal quarter as primary research key | User-confirmed 2026-11-15; acquisition implemented | DEI-bound quarter entry at 61b79c9; release dates remain source/version/cutoff metadata, not a universal analysis cutoff |
| Short/medium/long durations | Unresolved | Method research must justify proposed definitions |
| Hosts, providers, paid budgets | Unresolved | Determine before related execution or spending |
| Vault layout and individual note templates | Proposed | Validate against real examples before standardizing |
| Agent discovers necessary analysis updates from vault/source state | Confirmed continuation intent/spec; implementation and bounded actual host trials | Core Stage C/F requirement; modification time is only a hint. Per-quarter discovery, dependency-aware checkpoint reuse and protected recovery have retained source/host evidence; full research and installed-host acceptance remain separate |

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
- [Fiscal-quarter replay and live CLI evidence](../loom/2026-11-15-finance-sec-baseline/evidence/quarter-replay.md).

Session-specific restart instructions are saved separately under
`.claude/handoffs/`; consult the explicitly provided latest handoff path rather
than assuming a prior handoff describes the current repository state.


### Stage A completion, 2026-11-15

The user authorized the Apple adjacent-quarter pilot and then requested automatic
completion of the previously planned first stage. The active interpretation was
stated as Stage A: scope/time semantics, method research, coverage and report
examples. Public-source research and project-only fixtures proceeded without
another interview. This authorization did not include new runtime features,
actual-vault changes, paid providers, installation, publication or merge.

See [the Stage A completion record](pilots/apple-2024q2-q3/STAGE-A-COMPLETION.md),
[method research](research/2026-11-15-equity-method-and-report-pilot.md) and
[pilot index](pilots/apple-2024q2-q3/INDEX.md). This continuation supersedes older
pending Stage A/B status snapshots above; their historical measurements remain.
The accepted acquisition branch/attestation was not modified. Sample notes stay
draft/partial with insufficient valuation evidence; Stage A completion is not
Stage C completion or a reduction of the twenty-year/cross-industry objective.

### Valuation research continuation, 2026-11-15

The user authorized Q2 first and then Q3 comparison. A separate
[earnings/exit-multiple diagnostic](pilots/apple-2024q2-q3/valuation-v1/METHOD.md)
now supplies dated price fields, accession-bound TTM inputs, explicit five-year
stress assumptions, reverse-growth thresholds and a same-method comparison.
Original Stage A notes are preserved. This closes a bounded price/earnings
evidence task; it does not close calibrated forecast/valuation evidence or Stage C.
Next: connect operating forecasts and peer/expectations evidence before claiming
actionable valuation or implementing the report/update skill. Acquisition code,
accepted runtime review and the broader twenty-year/multi-industry goal remain.

### Q2 operating evidence and update examples, 2026-11-15

The user authorized the next bounded research batch. The [Q2 supplement and
applicability record](pilots/apple-2024q2-q3/forecast-v1/METHOD-AND-VALIDATION.md)
now separate reported financials, secondary management outlook and local numeric
assumptions; reconcile next-quarter revenue/margins/earnings; and retain a draft
dependency inventory with frozen-history/latest-mode update examples. Original
2023Q3 values provide the seasonal base, not later 2024Q3 comparative columns.
These are research fixtures, not a production forecast or implemented updater.
Short/medium/long ratings remain insufficient_evidence. Stage C runtime,
cross-session recovery, long-horizon calibration and cross-industry validation
remain pending; no accepted acquisition attestation or existing note is replaced.

### Goal continuation and Q3 operating evidence, 2026-11-16

The user's active Goal preserves the complete A-G outcome; it is not satisfied
by the already accepted read-only assessor or this research batch. Work continues
on isolated branch `docs/2026-11-16-finance-stage-c-pilot` from accepted 0462b01.
The [Q3 continuation record](pilots/apple-2024q2-q3/continuation-pilot/RUN.md)
and linked inputs/results retain actual partial before/after/repeat assessments.
Twenty-eight self-check assertions passed; all three assessors returned exit 2.
The completed operating supplement is reusable under supplied evidence, while
valuation and consensus work stay pending. No fresh agent or host session ran.

Agent-decided research choices:

- Derive the seasonal FY2023 Q4 base from original annual less original nine
  months. Reject later comparative rows and subtraction of EPS or average shares;
  retain original accession/duration rows in reported-inputs.json.
- Use the August 1 call's September outlook rather than copying May guidance.
  The inspected [contemporaneous call report](https://www.macrumors.com/2024/08/01/apple-3q-2024-earnings/)
  at 2:23 pm provides 45.5-46.5% margin, $14.2-14.4bn expenses and about 16.5%
  tax. It remains secondary evidence, not an issuer transcript.
- Choose local 3/5/7% revenue and 12/14/16% services sensitivity coordinates
  around that qualitative outlook; reject presenting them as company guidance,
  calibrated probabilities or a five-year earnings path.
- Retain the June 14 [Rakuten analyst article](https://media.rakuten-sec.net/articles/-/45520)
  only as a dated individual expectation eligible for Q3. It is too late for
  Q2 and cannot substitute for broad independent consensus.
- Keep local 2026-authored assumptions as analysis metadata rather than inventing
  2024 publication dates. The assessor currently covers declared source/output
  identity only; manual file hashes do not imply recursive dependency tracking.

Remaining Stage C work: independent semantic challenge of the integrated two-
quarter case; explicit unresolved valuation/model evidence; and the authorized
software station for actual folder discovery and research continuation rather
than just a hand-prepared normalized snapshot. Stage F additionally requires
real new-host sessions, source freshness, user-edit protection and rollback.
The existing two-attestation branch attribution ambiguity remains unconfirmed;
accepted evidence is preserved. Stages D-G are not claimed complete.

### Industry contrast evidence, 2026-11-16

The [first bank/energy cases](pilots/industry-contrasts-v1/INDEX.md) compare
JPMorgan 2020Q1/2024Q2 and ExxonMobil 2020Q2/2024Q2 using original dated issuer
releases and a primary financial-service-method reference. Agent-decided:
choose the 2020 stress periods to challenge profitable-survivor assumptions;
use the 2024 periods as contemporary-reporting contrasts, not claims of normal
cycle conditions or representative industry averages. Each historical case has
its own publication cutoff; the 2026 comparison cannot enter a 2020 judgment.

Observed consequences for method design: bank credit provisions/regulatory
capital require separate analysis from industrial CFO/capex; one-off Visa
earnings cannot be directly annualized; a loss-making energy quarter does not
support positive trailing P/E; acquisition-inclusive production is not wholly
organic growth. Exxon 2024Q2's original FCF reconciliation gives $4,937m versus
$4,325m for a simple CFO-minus-PP&E proxy, a $612m definition difference.
Keep both named measures instead of treating matching field names as equivalent.

Arithmetic and source-date/link self-checks are recorded in the pilot; no
independent semantic review or full Stage D acceptance is claimed. Original
accession-bound statements, sector-specific drivers, prices/expectations and
valuation remain; so do the proposed broader contrasts and failure-case work.

### Extended method cases and remaining history inputs, 2026-11-16

Additional [cloud/member-retail](pilots/industry-contrasts-v1/雲端與會員零售案例.md)
and [bank-receivership](pilots/industry-contrasts-v1/銀行接管事件案例.md) cases
retain original MSFT 2024Q4/COST 2024Q3 releases and separate March 10/March 12
2023 agency cutoffs. Agent-decided: use them to challenge cloud/AI investment
attribution, membership-fee profit attribution, 12-week annualization and
deposit-protection/equity-value conflation. Six arithmetic checks passed; these
are bounded method examples, not complete company valuations or Stage D.

The user asked whether full SEC originals are read. Current acquisition retains
original HTML and research checks selected original passages, but neither the
current spec nor software proves complete chapter reading. Do not count file
download or numeric reconciliation as full MD&A, risk, notes or legal review.
The forthcoming skill must disclose actual reading coverage rather than
advertising full-document review without evidence; no claim of a newly
confirmed mandatory word-for-word full-reading requirement is made.

The [history-input audit](../loom/2026-11-16-finance-research-continuation/research/03-apple-history-vintage-gaps.md)
found cached old comparison rows filed years after their observation periods.
Agent-decided: do not fill twenty-year historical reports from later comparison
rows or one modern revenue tag. Obtain period-original evidence and verify the
latest complete company fiscal year before fixing the exact twenty-year range.
The audit is input research, not completed Stage E quarters.

Agent-decided history window, 2026-11-16: use FY2006–FY2026 (84 expected
quarters), extending the preliminary twenty-fiscal-year window by one year to
avoid a literal twenty-calendar-year boundary ambiguity. The original issuer
FY2006 Q1 declaration and SEC filing bind the first endpoint, while the FY2026
annual header binds the last. The retained SEC indexes yield 84 unique original
filing candidates; each fiscal identity, required supporting filing, cutoff and
substantive analysis still requires verification. See the
[history inventory and limits](history/apple-fy2006-fy2026/INDEX.md).
No historical-batch quarter is accepted complete by this source count.

The [delivery attribution investigation](../loom/2026-11-16-finance-research-continuation/research/02-stacked-delivery-attribution.md)
traced the live command's unconfirmed result to accepted prerequisite
attestations in the whole trunk delta. Preserve them; no installed-checker
patch, trunk-ref rewrite, publication or merge was performed. An explicit-base
diagnostic confirmed the cause but is not an ordinary delivery pass.


### Actual continuation host evidence, 2026-11-16

The [actual host record](../loom/2026-11-16-finance-research-continuation/evidence/host-sessions.md)
supersedes earlier not-started/source-only status snapshots for this bounded
continuation capability; their original measurements remain retained. Eight
separate source-invoked Codex sessions used isolated public Apple originals,
with observed provider openai/model gpt-6.1-sol. They exposed and revalidated a
per-quarter discovery repair, executed bounded Q2/Q3 research and changed-method
recomputation, preserved independent work, and demonstrated controlled save-
worker interruption/resume/rollback plus refusal of user-edit conflicts.

A separately initialized growth/fiscal-identity study establishes genuine local
no-work after its required questions finish. The original full research root
retains required investment-case work for both quarters. Neither scope implies
current external coverage, installed-plugin behavior, complete two-quarter
investment analysis, Stage E historical-batch completion or wider asset support.
The run08 whole-root additions audit failed due to two W3-added measurement
files; only the narrower managed 46-file equality and no-publication claim pass.
Raw CLI token counters and all first failures are retained, without dollar/cache
or 84-quarter cost estimates. Stage A/B acceptance stands; C/D remain partial,
E has 84 candidates and zero completed historical-batch quarters, and G's bounded
ETF/commodity/FX methods/cases are not full asset research or automation.
