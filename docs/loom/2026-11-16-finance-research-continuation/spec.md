# Folder-grounded investment research continuation — spec
intent: 2026-11-16-finance-research-continuation@718b8df
confirmed-behavior: 2026-11-16 @85c40e3
pre-build-review: required — research writes, user-edit protection, source cutoffs and cross-session completion can otherwise turn stale or partial evidence into misleading advice or lost data

## Requirements

REQ-1 — Discover saved research
  WHEN the user requests investment research continuation for a designated research folder, the agent shall identify its assets, fiscal quarters, completion evidence and outstanding research from the retained files without requiring the current conversation or a manually prepared work list, using file modification times only as discovery hints → Acceptance #1

REQ-2 — Continue the necessary work
  WHEN an eligible new disclosure, relevant evidence change or incomplete research is found, the agent shall acquire or verify the applicable evidence and execute the affected research while reusing completed work whose dependencies remain valid, preserving company fiscal-quarter identity and using publication dates to determine eligibility at the assessment cutoff → Acceptance #2

REQ-3 — Avoid unnecessary regeneration
  WHEN eligible relevant evidence is unchanged or changes affect only formatting or modification times, the agent shall preserve completed analytical outputs without duplicate quarters or unsupported new recommendations and explain the no-work result within the evidence actually checked → Acceptance #3

REQ-4 — Retain analytical and historical evidence
  WHEN the agent saves research, the saved result shall retain original sources, fiscal coverage, cutoff, method and conditional assumptions, short-, medium- and long-horizon judgments including insufficient evidence, predecessor versions and cross-quarter changes, with market and other faster-changing inputs assessed at their own observation and publication times → Acceptance #4

REQ-5 — Preserve data under uncertainty and failure
  IF source freshness cannot be established, evidence is missing, user edits conflict or execution is interrupted, THEN the agent shall preserve existing research and user edits, identify the affected uncertainty and recovery action and refrain from advertising incomplete or unverified research as complete or current → Acceptance #5

REQ-6 — Demonstrate genuine cross-session operation
  WHEN the capability is verified in an isolated research vault, the selected actual host shall demonstrate new-quarter, changed-evidence, interrupted-continuation and no-work behavior in fresh sessions with observable incremental writes, input protection and recovery evidence, rather than treating subprocess assessment or a fresh reviewer context as that demonstration → Acceptance #6

## Design decision

- agent-decided — Add a finance research skill that guides the host agent through
  discovery, evidence checking, analysis and bounded publication. Reuse existing
  SEC acquisition and pure work assessment; add only the file discovery and
  publication support required for this outcome. A deterministic helper validates
  identity and file integrity, not the truth or quality of the agent's research.
- agent-decided — Keep the existing normalized-input assessment API intact. A
  bounded folder reader derives that input from persisted local records and
  source/output references. Users no longer prepare a work list per invocation;
  an overview/watchlist and initial asset scope are configuration, not a task list.
- agent-decided — Use the program plan's `investing/` layout, stable asset IDs,
  `cycles/{fiscal-quarter}/{cutoff}-{review}/`, separate events and durable data.
  Only initialize the designated new subtree or an explicitly authorized isolated
  copy. Do not reinterpret or migrate arbitrary old Markdown. Existing unsupported
  notes are preserved and reported with the minimal missing metadata needed.
- agent-decided — Use small versioned local progress/source records, with explicit
  required questions and source/output references, beside human-readable notes.
  The reader enumerates assets/cycles and derives missing outputs and dependency
  differences. Do not introduce a global database, always-running daemon or a
  second scheduler. The plan must specify the exact bounded format and reader
  behavior; no arbitrary executable selectors or commands in notes are accepted.
- agent-decided — Treat note bodies, remote documents and links as untrusted data.
  Confine reads/writes to the explicitly selected research root and authorized
  managed subtree, reject escaping/symlink references and never execute document
  instructions. Public-source requests send only the configured public issuer/
  query and legitimate identifying header where required, not private vault notes.
- agent-decided — Default scope comes from persisted asset configuration. If root,
  asset identity, mode or cutoff cannot be established unambiguously, state the
  missing scope and do not fabricate it. Historical mode freezes its cutoff;
  latest mode may create a new review with the requested/current assessment time
  explicitly recorded, never silently rewrite a historical judgment.
- agent-decided — Discover new financial quarters only from source-declared fiscal
  identity and original filing evidence. Price, industry, macro and other inputs
  may change within the same financial quarter and cause a same-quarter/event
  review. A price date never creates a new financial quarter. Missing publication
  time is a gap, not permission to use current information historically.
- agent-decided — Separate financial originals, economic source revisions, local
  method versions, assumptions and authored analysis dates. Record relevant
  projections for semantic invalidation and full raw hashes for provenance.
  Preserve JSON types and units. Formatting-only changes to structured evidence
  do not change meaning; unverifiable free-text meaning must not be automatically
  dismissed as formatting. Locally authored 2026 assumptions are not falsely
  represented as 2024 publications.
- agent-decided — Track the complete declared dependency set for a work unit,
  including shared studies and method/assumption versions. Changed dependencies
  invalidate affected work and synthesis transitively; independent completed
  questions stay reusable. Do not infer semantic completeness from nonempty text,
  an output hash, a successful command or existence alone. The agent records a
  source/citation/calculation/counterevidence check before publishing completion.
- agent-decided — Protect old completed reports as immutable analysis versions.
  New or corrected judgments append linked reviews. Record managed output hashes
  and recheck immediately before publication. Any unexpected edit is a conflict:
  preserve it and the proposed draft, identify the file and do not replace it.
  Updates to managed overview/progress pointers require the same precondition.
- agent-decided — Stage outputs separately and publish completion/pointers last.
  Record enough identity to detect an interrupted publication. Resume revalidates
  sources, output content and dependency identity before adopting a saved unit.
  Recovery never deletes a user-modified file; rollback concerns only the files
  created by the recorded isolated run. An unsuccessful run cannot advance the
  latest-completed pointer or last-successful external check.
- agent-decided — Report last external attempt and successful verification
  separately. Public local snapshots can support bounded continuation while
  external freshness stays unknown. No-work is conditional on the checked sources
  and scope, not a global freshness assertion. A failed market input need not
  block independent financial work, but must qualify affected recommendations.
- agent-decided — Separate factual coverage, analytical completeness and advisory
  sufficiency. A review may document an unresolved question honestly; a required
  unresolved analytical task remains pending. `insufficient_evidence` is not hold
  or a neutral expected return. Never make completion true by dropping missing
  questions, substituting a later vintage or copying a generic thesis.
- agent-decided — Research includes business/competition, financial condition,
  capital allocation/governance, valuation/scenarios and risks, with synthesis
  and changes. Existing industry-method evidence controls applicability; an
  unsuitable model is refused with a reason, not filled with invented numbers.
  No fixed number of files forces duplicated prose across short dimensions.
- agent-decided — Preserve the user's unspecified holding period. Each report
  states its analysis horizons, price/benchmark/currency assumptions when used,
  evidence and invalidation triggers. A quarterly earnings bridge cannot justify
  a multi-year terminal growth or multiple without independent support. Do not
  silently mix the earlier pilot's 0–3/3–12/12–60-month convention with the later
  exploratory 1-quarter/1–3-year/5+-year note; reconcile and disclose in methodology.
- agent-decided — Verify the actual currently available host in a bounded isolated
  vault without global installation, unapproved paid calls or private-data upload.
  Record session identity, task input, discovered files, source check, actual
  outputs and recovery. If a real fresh-session facility is unavailable under
  existing authorization, report Acceptance #6 as unverified and continue the
  authorized work; do not relabel a unit test or reviewer as a host session.
- user-decided — Intent confirmed on 2026-11-16. Paid usage, real-vault changes,
  global installation and publication remain outside the existing authorization.
  This change does not settle or shrink program Stages D, E or G.

## Alternatives considered

- Keep only the supplied-snapshot CLI: useful independently, but leaves the
  confirmed discovery and actual research continuation gap unresolved.
- A general autonomous workflow engine: rejected because a host agent plus
  bounded evidence/publication helpers supplies the required behavior without
  creating a new runtime, service or scheduler to maintain.
- Infer all state from filenames and mtime: rejected because copied/synced and
  user-edited files do not establish source identity, meaning or completion.
- Replace the pure assessment core: rejected because its accepted bounded
  contract is reusable and a new reader/executor must not erase its evidence.
- Rewrite old reports in place: rejected by the confirmed history/user-edit
  protection requirements and PRINCIPLES.md non-negotiable #1.
- Generate twenty years before testing continuation: rejected because it grows
  research volume without demonstrating reliable cross-session maintenance.

## Current state evidence

- Forward: `docs/finance/PLAN-DRAFT.md` §9.1 describes agent-invoked ongoing
  work; `obsidian-finance/scripts/assess_work.py`, `run`, currently requires a
  supplied normalized snapshot and returns only decisions.
- Reverse: `obsidian-finance/skills/sec-data/SKILL.md`, scope and result
  interpretation, exposes acquisition; no current finance research skill calls
  an end-to-end folder reader and publisher (new capability).
- Error: `docs/finance/pilots/apple-2024q2-q3/continuation-pilot/RUN.md`, Observed
  continuation, records actual exit-2 partial results and explicitly excludes
  fresh-agent/host proof, recursive tracking and full-case completion.
- Data: `docs/finance/pilots/apple-2024q2-q3/continuation-pilot/state/after.json`,
  sources/records/work, freezes declared inputs and the completed output digest;
  `AUTHORING-EVIDENCE.md` explains manual metadata and remaining semantic gaps.
- Boundary: `PRINCIPLES.md`, Non-negotiables #1–#3; confirmed intent Constraints;
  `docs/finance/PLAN-DRAFT.md` §§8–11 pin isolated data protection, honest maturity,
  quarterly identity, history, substantive research and original stage gates.

## UI flows

The user invokes investment research in the existing conversation with a
designated research folder. There is no new graphical screen. Messages are
localized to the conversation language; notes follow the user's vault language.
These are conversation outcomes, not a promise of new public CLI commands.

| Case | What the user does | What they see |
|---|---|---|
| Start | Ask the agent to continue investment research in a designated folder | The identified assets, research scope and cutoff, then the necessary work with reasons; no per-note task list is required |
| Empty or unsupported folder | Request continuation where no usable asset/research configuration exists | “Research scope is missing” with the missing asset/root/cutoff information; existing files are preserved and the user can provide the missing scope and retry |
| In progress | Start eligible research work | A concise current-work update and durable progress after meaningful completed units; no background service is implied |
| New financial quarter | Continue after an eligible company-declared quarter appears | New-quarter research with the source identity, dimensions and synthesis; earlier quarters remain available |
| Changed evidence | Continue after relevant eligible price, macro, industry, filing or shared research changes | Only affected research and its synthesis are updated in a linked review, with the reason and previous judgment visible; a market date alone does not create a financial quarter |
| Interrupted work | Ask to continue the same research after interruption | Verified completed units are reused; missing or invalidated units are resumed; the agent identifies what remains and why |
| No necessary work | Continue complete research with unchanged relevant checked evidence, including formatting/mtime-only changes | An explicit “No analytical update needed” with checked scope and source freshness limitations; no duplicate reports or new advice |
| Historical review | Ask for research at a saved historical cutoff | Only evidence eligible at that cutoff is used; later information is listed as excluded and historical reports are preserved |
| Missing data | Continue with absent or conflicting evidence | “Evidence incomplete” naming the affected question and recovery; independent work can proceed while affected recommendations remain qualified |
| Source check unavailable | Continue while an external check fails or cannot run | “External freshness unverified” with the failed attempt and last successful check if known; no false up-to-date claim; retry can continue saved work |
| Invalid/escaping input | Designate an invalid root or a reference outside it | “Research input cannot be used” identifying the problem and asking for an in-root valid reference; no external file is read or modified |
| User-edit conflict | Continue after changing a managed report or pointer | “User edits preserved” naming the conflicting file and proposed draft; resolve the conflict explicitly and retry, with no silent overwrite |
| Publication interrupted | Stop while a new review is being saved | On retry the agent identifies incomplete publication, preserves old completed reports/pointers, validates staged outputs and reports/resumes remaining work rather than advertising success |
| Repeated request | Repeat continuation with unchanged saved evidence | The same applicable conclusions and work status; no duplicate cycle or previously completed work regenerated merely because it ran again |
| Success | Complete the eligible research questions and verification | Links to the new completed review and predecessor, source/cutoff/assumptions, horizon judgments, gaps and next triggers; incomplete questions are not hidden as success |
| Recovery/rollback | Request recovery of the recorded isolated run | The agent identifies its created files and restores the prior managed completed view where safe; user-modified files are preserved and conflicts named rather than deleted |

Cold start lands at scope discovery; corrected scope/input returns to that same
request. Retry after evidence recovery rechecks eligibility and dependencies;
retry after a user edit rechecks the file precondition. Abandoning a run preserves
the last completed view and saved unfinished work. A fresh session follows the
same discovery path using files, not conversation memory. Piped/narrow output is
plain text with local links; no layout-dependent control is required.

Existing completed reports are not rewritten or deleted. Only explicitly
managed progress/overview pointers are updated after verified new outputs, with
precondition checks and a recoverable prior version. All actual verification in
this change uses isolated copies; the original vault remains outside execution
authorization. Public-source checks do not transmit private notes.
