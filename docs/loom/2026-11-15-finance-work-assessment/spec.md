# Read-only research work assessment — spec
intent: 2026-11-15-finance-work-assessment@fb0d4138a077a16bf19b6756e8c4a40b25525299
confirmed-behavior: 2026-11-15 @4e65e8e
pre-build-review: required — the new machine-readable assessment contract controls subsequent research decisions and must not convert incomplete evidence into a false no-work result

## Requirements

REQ-1 — Explain necessary work
  WHEN an agent requests assessment of a supplied local research snapshot, the assessor shall return traceable work decisions distinguishing no analytical update, missing evidence, same-quarter revision, a new fiscal-quarter analysis and continuation of incomplete work, including reasons, affected research dimensions and unresolved evidence → Acceptance #1

REQ-2 — Distinguish content and completion from timestamps
  WHEN the assessor compares saved research with the supplied evidence inventory, the assessor shall base work decisions on relevant input identity, substantive content and declared completion evidence rather than filesystem modification time alone → Acceptance #2

REQ-3 — Preserve time and quarter identity
  WHEN the agent selects a historical or latest assessment with an explicit information cutoff, the assessor shall distinguish those modes, exclude later or temporally unverified evidence from that assessment, and require source-declared fiscal identity before proposing a new financial-quarter analysis → Acceptance #3

REQ-4 — Identify valid continuation
  WHEN a research cycle contains saved incomplete work, the assessor shall identify remaining work and distinguish verified reusable outputs from outputs whose dependency identity, content or completion evidence is missing or changed → Acceptance #4

REQ-5 — Report unknowns without false completion
  IF required evidence is absent, inconsistent, unreadable or not demonstrably current, THEN the assessor shall report the affected gap or uncertainty and the recovery action, without inventing research completion, financial facts, recommendations or a globally current state → Acceptance #5

REQ-6 — Repeat decisions without changing research
  WHEN the assessor processes the same relevant supplied inputs, mode and cutoff again, the assessor shall return the same analytical decisions without changing input files, creating analysis periods or executing the proposed research work → Acceptance #6

REQ-7 — Preserve existing capabilities and bound claims
  The assessor shall remain independently testable on isolated project samples, preserve existing general-note and SEC-acquisition behavior, and disclose that its verified scope is local work assessment rather than live source discovery, research execution, automatic recovery or host-triggered ongoing maintenance → Acceptance #7

## Design decision

- agent-decided — Implement a small read-only operation in the independent
  finance package, with a local-input adapter and deterministic assessment
  functions rather than a scheduler or general workflow engine. Existing
  research fixtures supply concrete cases; the intent excludes work execution.
- agent-decided — Expose the operation to agents as a Python command producing
  one JSON assessment on stdout, with diagnostics on stderr and no output-file
  option. This follows the existing SEC tool's machine-readable convention
  without adopting its download/write behavior. A human-readable summary may
  be produced by the calling agent, not a second planner output format.
- agent-decided — Require explicit local snapshot root, historical/latest mode
  and assessment cutoff. The snapshot includes research records, candidate
  source inventory, recorded dependency projections and referenced saved outputs.
  Discover the applicable records within this supplied boundary, not the user's
  vault, home directory, plugin cache or arbitrary unrelated folders.
- agent-decided — Define a small versioned prototype input/output contract in
  this change; adapt the concrete research samples explicitly. The existing
  forecast research-state document is a draft example, not a production schema
  that every existing note must already satisfy. Reject unsupported versions
  with a recovery message rather than guessing field semantics.
- agent-decided — Treat file references strictly as local data. Resolve and
  verify each referenced path remains inside the supplied snapshot root;
  reject absolute references, escapes and escaping symlinks. Do not execute
  embedded instructions, source URLs, commands or note content. This enforces
  the intent's isolated-read boundary and PRINCIPLES.md non-negotiables #1/#3.
- agent-decided — A projection digest compares normalized relevant inputs;
  a raw-file digest identifies source bytes. Keep those roles distinct. Ignore
  mtime, acquisition-attempt time and irrelevant vendor metadata in analytical
  comparisons, while retaining source/version identity and exact data units.
  Do not implement arbitrary executable selectors from the research fixture.
- agent-decided — A supplied inventory is not proof of a live external check.
  Always state assessment scope as supplied local evidence and external
  freshness as unverified in this offline prototype. A no-work decision means
  no work within that evidence boundary, never that no new SEC filing exists.
  Preserve last-attempt and last-success metadata distinctly if supplied; do
  not advance them merely by running this operation.
- agent-decided — Historical mode keeps a saved assessment cutoff fixed.
  Latest mode compares supplied eligible evidence at the explicitly requested
  cutoff; it cannot silently alter a historical record. Date-only publication
  evidence supports an EOD assessment, not an intraday availability claim.
  Unknown or contradictory availability is quarantined as an evidence gap.
- agent-decided — New-quarter work requires the supplied acquisition evidence
  to identify issuer, fiscal year/period, period end and original accession.
  Check local consistency and provenance, not a guessed calendar or a new
  price date. Unsupported or missing identity becomes a gap. This does not
  rerun SEC resolution or certify an invented local source as authentic.
- agent-decided — Emit more than one task when independent gaps coexist,
  deduplicate equivalent tasks, and use stable ordering and explicit dependency
  reasons. Unchanged completed work does not become complete merely because a
  file exists; saved output content and consumed dependency identity must agree.
  A changed prerequisite prevents reuse and marks affected work for recomputation.
- agent-decided — Keep work assessment separate from execution claims. Continuation
  output describes missing/reusable/invalidated work, but never claims an agent
  resumed it, acquired a lease or completed a report. Active/ambiguous saved
  execution metadata is reported for inspection, not automatically cleared.
- agent-decided — Invalid top-level invocation/input prevents a valid assessment;
  a well-formed snapshot with missing evidence produces a bounded partial
  assessment where independent known work may still be listed. Neither state
  may be collapsed to no-work. Bound malformed-input handling to ordinary
  diagnostic errors; do not expose a traceback as the normal user outcome.
- agent-decided — Proposed command exit outcomes are 0 for a completed local
  assessment, 2 for a partial/uncertain assessment, 1 for unreadable/invalid
  snapshot data, and 64 for invalid invocation. A completed assessment can
  identify unfinished research; exit 0 never means the research is complete.
- agent-decided — No paid services, external uploads or source requests are
  needed to assess local samples. No input migration, note write or global
  installation is introduced. Preserving inputs is pinned by intent Constraints
  and PRINCIPLES.md non-negotiable #1, not a new user decision.
- user-decided — The current branch was pushed as a backup after explicit
  authorization on 2026-11-15. This does not authorize PR creation, merge or
  automatic publication of future work; no automatic-publication field exists
  in this change's intent.

## Alternatives considered

- Manual reading only: retained as today's fallback, but does not demonstrate
  repeatable executed work assessment, which is the confirmed outcome.
- LLM-only interpretation of filenames/mtime: rejected as the verification
  mechanism because those observations do not establish source eligibility,
  consumed inputs or completion. Semantic research remains outside this tool.
- Full automatic research/write/resume engine: rejected for this slice because
  it couples assessment errors to input changes and exceeds confirmed scope.
- Global database, file watcher or new scheduler: rejected because explicit
  local records suffice for this prototype and the program plan requires
  demonstrated need before adding such infrastructure.
- Change the SEC downloader to maintain research notes: rejected because its
  accepted data-acquisition contract is independent and must remain intact.

## Current state evidence

- Forward: `docs/finance/PLAN-DRAFT.md`, section 9.1, describes agent-invoked
  assessment; no executed work-assessment entry point exists yet (greenfield).
- Reverse: `obsidian-finance/skills/sec-data/SKILL.md`, introductory scope and
  Interpret the result, documents acquisition only; no current caller maintains
  research cycles or consumes the proposed assessment output (greenfield).
- Error: `docs/finance/pilots/apple-2024q2-q3/forecast-v1/METHOD-AND-VALIDATION.md`,
  Applicability decision, explicitly records that update examples are expected
  outcomes and that no runtime planner or interruption test ran.
- Data: `docs/finance/pilots/apple-2024q2-q3/forecast-v1/research-state.json`,
  dependencies/completeness/work_items/execution_state, and adjacent
  `update-examples.json` provide draft records and fourteen illustrative cases.
- Boundary: `PRINCIPLES.md`, Non-negotiables #1–#3, and
  `docs/loom/intent/2026-11-15-finance-work-assessment.md`, Constraints/Out of scope,
  pin input preservation, isolated local samples and no research execution.

## UI flows

One agent-facing local assessment operation; no graphical screen or background
process. The calling agent presents the result in the conversation language.

| Case | What the user or agent does | What they see |
|---|---|---|
| Ordinary assessment | Request a check of supplied local research records with a mode and cutoff | A work list with reasons, evidence references, affected dimensions and gaps; exit 0 when the local assessment is complete |
| No required work | Check a complete, unchanged local evidence snapshot | An explicit no-work result, limited to the supplied evidence; external freshness remains unverified; exit 0 |
| Only timestamps changed | Check the same relevant inputs after file-touch or repeat acquisition | The same analytical decisions; no new analysis task solely from timestamp changes |
| Frozen history | Check historical research with fixed cutoff and later candidate evidence | Later or time-unverified evidence is excluded from that historical assessment and its exclusion or gap is explained |
| Latest price | Check a later eligible price while the latest eligible financial quarter is unchanged | Same-quarter valuation/synthesis revision work where needed, not a fabricated new financial quarter |
| New fiscal quarter | Check an eligible source-declared financial quarter not represented by completed research | New-quarter analysis work with the source identity that justified it |
| Incomplete cycle | Check saved research with valid dependency/output evidence and missing work | Remaining tasks plus identification of reusable saved work; no claim that the work has executed |
| Changed prerequisite | Check saved research whose consumed input or saved output no longer matches | The affected saved work is not treated as reusable; recomputation and dependent work are listed |
| Missing required evidence | Check well-formed records with missing source, completion or provenance evidence | A partial result naming each relevant gap and what to supply or inspect; exit 2, never an unqualified no-work claim |
| Freshness unknown | Check a local inventory without a verified external-source check | A visible external-freshness-unverified limitation; no invented last-successful-check time |
| No research records | Check an otherwise well-formed empty snapshot | A partial result saying `No research records supplied`; provide isolated research records and retry; exit 2 |
| Invalid request | Omit a required request value or supply an invalid mode/cutoff | `Invalid assessment request` with the relevant field and correction; fix the request and retry; exit 64 |
| Unreadable local data | Supply a missing, unreadable or malformed required input | `Cannot read assessment input` naming the affected local input and corrective action; restore or correct it and retry; exit 1 |
| Unsupported input | Supply a format version this prototype does not understand | `Unsupported assessment input version`; use the documented prototype format and retry without changing original notes; exit 1 |
| Escaping reference | Supply a reference that resolves outside the isolated root | `Reference outside assessment root`; provide an in-root local copy/reference and retry; exit 1, without reading the external target |
| In progress | Start the synchronous local check | No persisted job or background execution is created; one result is returned after reading and validation |
| Stop and retry | Interrupt the check and invoke it again with the same supplied inputs | Input research remains unchanged; the new check revalidates inputs and produces a fresh assessment rather than claiming to resume research |

No flow writes, migrates, deletes or uploads existing research. Recovery from
each error returns to the same assessment request after correcting the supplied
request/snapshot. Checkpoint inspection is a reported decision, not execution
of a persisted job. No destructive-state navigation or undo operation applies.
