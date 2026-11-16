# Folder-grounded investment research continuation — acceptance test evidence

Tried on 2026-11-16, in a clean copy of the project at 64dd4c0.

Initial run on 2026-11-16 tested `2e135990987f320d0ea391e48b7e55b3fdc2a2e9` and was committed in `933710c174b55eb5c3df5ec7a565d7f3c51a7b27`. Its original observations, failures and native evidence remain below, followed by the dated re-run section. Statements about the initial new host refer to that first run, not a newly launched re-run host.

## Environment, setup and evidence boundaries

- Tested exact HEAD: `2e135990987f320d0ea391e48b7e55b3fdc2a2e9`.
- Independent witness did not implement or repair product code. First attempted `git worktree add --detach /private/tmp/finance-acceptance-clean <HEAD>` failed because that path already existed. A different new worktree path failed because the shared Git metadata was outside writable roots. Neither failed directory was accepted as the test environment.
- Started clean instead with `git clone --no-hardlinks /private/tmp/finance-research-continuation /private/tmp/finance-acceptance-witness-2e13599`, then `git checkout --detach 2e135990987f320d0ea391e48b7e55b3fdc2a2e9`. Checkout reported `HEAD is now at 2e13599 test(finance): retain post-sync adversarial evidence`; initial and final `git status --porcelain=v1` were empty. No preexisting working artefacts were copied into the clone.
- Followed root README and `obsidian-finance/README.md`: Python 3.11+, standard-library runtime, existing pytest/Node for checks, source invocation rather than global installation. Existing `/private/tmp/finance-validation-env/bin/python --version` returned `Python 3.15.0`; `node --version` returned `v26.12.0`. Loaded the shipped `research_store.py` Python API; no nonexistent CLI was invented. The new actual host read skill, method reference and README and used that exact helper.
- Ran only the criterion-focused command below, not the entire package suite:

```sh
/private/tmp/finance-validation-env/bin/python -m pytest \
  obsidian-finance/tests/test_research_store.py \
  obsidian-finance/tests/test_research_publication.py \
  obsidian-finance/tests/test_research_continuation.py \
  -q -p no:cacheprovider
```

Captured result: `........................................................... [100%]` and `59 passed in 2.00s`, exit 0. The automated test suite, which runs before the change is accepted and blocks it on failure, remains the separate finalize-review check. Its command is `python3 -m pytest obsidian/tests obsidian-finance/tests -q -p no:cacheprovider`; this witness did not run or claim its result.

- Local direct probe: `/private/tmp/finance-acceptance-probe.py`; captured JSONL: `/private/tmp/finance-acceptance-probe-output.jsonl`. These are witness-only temporary artefacts, not executable committed evidence. Public fixtures were copied exclusively from the clean clone's `docs/finance/pilots/apple-2024q2-q3/host-continuation/` into new temporary directories. Discovery never used conversation-supplied work statuses.
- Prior actual runtime evidence is retained in `docs/loom/2026-11-16-finance-research-continuation/evidence/host-sessions.md` and the pilot's `host-continuation/run-01` through `run-08` transcripts, prompts, source-checks, reviews, before/after hashes and recovery calls. Independently opened all eight native headers and terminal results. Their session IDs differ and their headers report `provider: openai`, `model: gpt-6.1-sol`, `reasoning effort: low`. These are prior actual executions, not new acceptance executions or native-reviewer substitutes.
- Verified `git diff b4ee26d76b1c6f5fb49b111e40ca54395e57e29b 2e135990987f320d0ea391e48b7e55b3fdc2a2e9 -- obsidian-finance/scripts/research_store.py obsidian-finance/skills/finance-research` is empty. Current helper SHA256 is `fd0cede6aae38590bc09a07bc7935e87bd5986e1350f2c64fe35e7db6aba8526`, matching retained fixed-runtime evidence. Thus the later real sessions use the same functional helper/skill, while run-01's original discovery failure remains explicitly preserved. This does not claim all original transitions were newly replayed during this witness run.

## New actual host request on 2026-11-16

Copied the initially bounded `quarter-check-scope` public fixture to `/private/tmp/finance-acceptance-host-study`. Supplied `/private/tmp/finance-acceptance-host-prompt.txt`, explicitly requesting source invocation, persisted-scope discovery, independent Decimal calculations, source/method checks, conditional horizons and no publication unless needed. No new paid provider/API, private data transfer, install, real-vault write, external message or provider configuration was authorized or performed.

```sh
/Users/kouko/.local/bin/codex exec \
  --cd /private/tmp/finance-acceptance-host-study --sandbox workspace-write \
  --ephemeral --skip-git-repo-check --color never \
  --output-last-message /private/tmp/finance-acceptance-host-last.txt \
  - < /private/tmp/finance-acceptance-host-prompt.txt
```

Initial normal outer-sandbox launch exited 1 before a request: `failed to initialize in-process app-server client: Operation not permitted (os error 1)`. The same command with ordinary process-launch approval ran with the host's normal sandbox and guards; no dangerous bypass, trust mutation or allowlist edit occurred. Exit 0. Native header:

```text
OpenAI Codex v0.169.0
model: gpt-6.1-sol
provider: openai
approval: never
sandbox: workspace-write [workdir, /tmp, $TMPDIR]
reasoning effort: low
session id: 01a1e258-950a-7d03-bade-691c18bf2dec
```

The host independently discovered two `no_analysis_update` decisions, four reusable growth/identity units, `gaps=[]`, `excluded=[]`, and `external_freshness=unverified`. It read notes, checks, source metadata, method metadata and retained numerical originals, recalculated both quarters and reported all investment horizons as insufficient. It did not access external sources, advance attempts/success, publish a review, or change managed/imported evidence.

It correctly disclosed that the witness prompt's requested cutoff `2024-08-02T23:59:59-04:00` is four hours later than persisted `2024-08-02T23:59:59+00:00`; latest mode permits the earlier saved reviews. No external coverage for the extra hours was inferred. Current method/skill hashes agree with saved checks; README hash differs, so the host did not claim all generic hashes agreed. Current README SHA256 `ea573de4769864e7aa693936f60a842b72d16abe6cf5a2c5a2f37fe0b5e5e387`; saved method-check README hash `d1acb354b02ca6cf40fd431afbbe8d66b3dd9493592f1d08dff5d289e8597967`. Same local applied method and equations were verified; exact old README reconstruction was not claimed. No metadata was refreshed to conceal the difference.

One long shell write was blocked by the host's existing PreToolUse guard: `BLOCKED by dcg`; reason `Embedded shell command blocked: command contains too many substitutions for bounded static analysis (line 7 of heredoc)`. The command was not executed. The host used the dedicated patch tool to create its report and reran read-only verification. It did not follow the guard's suggested allowlist/allow-once alternatives. Final output: `PASS: repeated discovery identical; investing/imports hashes unchanged across final verification; both deliverables exist.`

Independently compared the finished host copy with clean committed originals: `managed_count=46`, `identical=true`, `added=[]`, `deleted=[]`, `changed=[]`, `import_original_preserved=True`. This comparison included all managed files, not only old paths, and imports. The only new root result files were the two requested witness outputs; the earlier run-08 concurrent-audit failure remains a separate preserved event.

Native reported `tokens used: 60,641`. This is a raw host counter, not billable/cached breakdown or monetary cost. Exact individual wall duration and billing remain unknown. Native transcript contains UTC event `2026-11-16T03:15:34.201658Z`; no fabricated start/end timing is supplied.

Original acceptance request artefacts remain locally accessible:

| Artefact | SHA256 |
|---|---|
| `/private/tmp/finance-acceptance-host-transcript-approved.txt` | `fa0805ceaa2030bcd9132b551d23b2f5f29571215712a257ceb05a3b9c3f765f` |
| `/private/tmp/finance-acceptance-host-study/acceptance-host-result.md` | `620e6845c526d0f359b635c54c00dfad5885545faaee38bf71ff37e5b3ff86d3` |
| `/private/tmp/finance-acceptance-host-study/acceptance-host-discovery.json` | `52985308a0f19d40a397e46875aba6530fbbfecaaef5f75cfec0931d2dcce471` |

The raw host report is Traditional Chinese because it is host-produced user output; this witness evidence and probe descriptions are English. Temporary paths are retained locally, not a promise of archival availability on another computer.

## 1. Saved assets, fiscal quarters, completion and work discovery

- How tried: direct `discover(public_copy, 'latest', '2024-08-02T23:59:59-04:00')`, then independent new-host discovery from persisted configuration. Also ran `test_folder_discovers_cycles`, `test_source_declared_new_quarters_without_saved_conversation`, and all parametrizations of `test_individually_unreviewed_quarters_remain_visible`.
- Observed: bounded Q2/Q3 growth and identity are four reusable units, two no-work decisions, no bounded gaps. A separate direct discovery of the original full-scope root returns `status=partial`, two `resume_incomplete_work` decisions for `investment-case`, and four independent reusable units.
- Evidence: captured JSONL probes `test_folder_saved_scope_discovered` and `test_folder_full_scope_pending_not_completed`; new native discovery file above; named tests passed in the 59-test criterion run. No hand-written current work list was provided.

## 2. New-quarter, changed-evidence, interruption and incremental reuse

- How tried: criterion tests `test_new_quarter_and_changed_source`, `test_local_analysis_dependencies_preserve_actual_authorship`, `test_transitive_input_change_rejects_old_units`, `test_interrupted_publication_recovers`, `test_equal_local_source_ids_invalidate_only_own_issuer`; inspected native run-02/03/05/06/07 terminal outcomes, saved outputs and frozen dependencies.
- Observed: eligible new quarters are discovered separately, future evidence is excluded; economic/method/assumption changes invalidate affected work and dependent synthesis; independent results remain reusable. New actual run independently recalculated saved eligible results without regenerating them.
- Prior actual evidence: run-02 linked partial review recomputes growth and preserves identity; run-03 fixes observed older-quarter omission and saves both quarters with pending investment-case; run-05 interrupts the save worker; run-06 performs ordinary resume and rollback; run-07 saves Q3 after controlled historical original-source arrival. This is bounded research, not newly published 2026 SEC evidence or a complete company case.

## 3. Unchanged, formatting-only and mtime-only requests

- How tried: `test_unchanged_no_work[False]`, `[True]`; repeated direct discovery; actual new ephemeral host independently checked saved scope/calculations before deciding no-work.
- Observed: identical discovery; no publication; all 46 managed files and imports remain exact, with no added/deleted managed file. External freshness remains unverified. The full original scope still has pending investment-case work, so bounded no-work never became global no-work.

## 4. Sources, dates, assumptions, horizons and history

- How tried: `test_completed_unit_reused_and_linked_provenance`, `test_incomplete_envelope_rejected`, local-authorship and public-pilot cutoff tests; new actual host read both saved reviews, source/method records, outputs/checks and recomputed arithmetic.
- Observed: fiscal originals Q2 accession `0000320193-24-000069` and Q3 `0000320193-24-000081`, period ends `2024-03-30`/`2024-06-29`, and publication dates `2024-05-03`/`2024-08-02` remain separate from 2026 actual method authorship. Original source URLs remain in research; original HTML is not retained in this bounded copy and was not newly verified.
- Recomputed from saved USD originals with Decimal: Q2 revenue YoY `-4.305327090978%`, Q3 `4.865704121178%`; Q3 margins `46.257155181459%` / `44.516302553883%`, change `1.740852627576` percentage points. Q2 margins `46.578074554009%` / `44.261672782488%`. Category changes and Greater China weakness remain counterevidence rather than universal-recovery claims.
- Short/medium/long advisory conclusions remain `insufficient_evidence`; Q3 explicitly preserves `(0,3]`, `(3,12]`, `(12,60]` months as pilot convention, not the user's holding period. Full forecasts, valuation, governance, narrative and competitive diligence remain incomplete. Wrong v1/v2 exact authorship declarations and their correction remain historical evidence, not verified original timestamps.

## 5. Unknown freshness, missing evidence, user edits and failure protection

- How tried: missing/unsupported/source/output/verification cases, publication interruption and all edit/symlink preservation parametrizations in the criterion tests. Copied the committed actual `cases/useredit` fixture and called normal recovery for its real run ID, both actions.
- Initial witness-only error: used shortened `run-05-useredit`, yielding `FileNotFoundError`; did not count this as a product conflict result. A first convenience replay of the entire probe prefix also hit `FileExistsError` on an already created temporary copy and did not run the intended recovery calls. Inspected persisted run directories, then invoked correct `run-05-useredit-interrupt` directly without recreating the fixture.
- Correct captured output for both `resume` and `rollback`: `ValueError Publication conflict: user edited investing/assets/equities/aapl/cycles/2024Q3/2024-08-02-run-05-useredit-q3/investment-case-progress.md`. Full before/after byte map matched: `all_case_bytes_preserved True`.
- New host made zero external requests and zero newly opened original pages. Prior source-reading declarations remain prior evidence, not new source verification. `last_attempt` is retained and no `last_success` is invented. The native guard rejection and safe report-tool fallback above are preserved separately from product recovery.

## 6. Genuine fresh-host continuation and recovery

- How tried: independently read all eight retained CLI headers and final outcomes and checked functional helper/skill equality with tested HEAD; newly launched ephemeral native session `01a1e258-950a-7d03-bade-691c18bf2dec` with its own isolated public copy and direct source invocation.
- Actual prior sessions: run-02 `01a1e214-0db5-7571-a802-ab011278fcb2` (changed method); run-03 `01a1e21d-ba5c-71f1-a551-30ac424d942d` (fixed two-quarter continuation); run-05 `01a1e226-6e0e-7111-82b7-2e1b147b39ab` (controlled worker interruption); run-06 `01a1e229-8a0b-7731-ae04-388f8245de9a` (normal recovery/rollback and edited conflicts); run-07 `01a1e22c-e025-71c3-9b81-7080e6ad8870` (new-quarter arrival); run-08 `01a1e23b-5819-7de3-b47e-fcc5799cbbbe` (bounded no-work).
- Observed: new request repeats bounded no-work and independent arithmetic without modifying research. Prior native evidence supplies the other actual transitions; criterion tests are only additional mechanical verification. Source invocation is not installed-plugin discovery. Controlled save-worker exit 75 is not a claim of unexpected host process death. The retained run-08 whole-root additions audit failure caused by two concurrent measurement files is not erased by the managed-only pass or this clean new run.

## 7. Start flow

- How tried: new actual host source-invoked skill, read SCOPE/config/asset questions and called the shipped helper.
- Observed: identified AAPL, both fiscal quarters, requested/latest cutoff, required growth/identity scope and advisory insufficiency; no per-note todo supplied. Native report/discovery above.

## 8. Empty or unsupported folder flow

- How tried: direct discovery on a newly created root containing only `user.md`; also ran all `test_unsupported_folder_preserved` cases.
- Observed: `ValueError: Cannot discover version-1 investing research: [Errno 2] No such file or directory: 'investing'; supply missing metadata or repair the reference and retry`; `test_folder_unsupported_user_note_preserved: true`. This is the actual helper's refusal and recovery information; no fresh-host conversational rendering of this error was separately claimed.

## 9. In-progress flow

- How tried: direct full-root discovery and checkpoint/publication criterion tests; inspected retained native partial-checkpoint and interruption reports.
- Observed: four independently complete units remain reusable while both required investment-case questions stay pending. Meaningful saved progress exists; no background service or full-case success asserted.

## 10. New financial quarter flow

- How tried: `test_new_quarter_and_changed_source`, `test_source_declared_new_quarters_without_saved_conversation`, multi-issuer/cold/public-pilot tests and retained actual run-07 source-arrival output.
- Observed: eligible source-declared Q3 generates work, source after cutoff is excluded, Q2 remains preserved. New quarter is not inferred from a price observation or filename. Actual run-07 wrote bounded growth/identity with the preceding Q2 baseline intact.

## 11. Changed evidence flow

- How tried: changed source, local method/assumption and transitive-dependency criterion cases, plus run-02/03 actual saved results.
- Observed: affected growth recomputed; independent fiscal identity reused with exact output/check digests. Method v3 correction remains honestly 2026-authored. No stale output merely receives a new dependency identity.

## 12. Interrupted work flow

- How tried: interruption resume/rollback criterion cases and independently opened actual run-05/06 results.
- Observed: incomplete publication leaves predecessor visible and a gap; clean resume validates staged data and yields a checkpoint; required investment-case work is still pending. Tests did not stand in for the original host invocations.

## 13. No necessary work flow

- How tried: actual new session and repeated direct/format-only discovery.
- Observed: two `no_analysis_update` decisions, four reusable units, zero bounded gaps and no duplicate review. Explicit external freshness limitation and incomplete broader scope are in actual host output.

## 14. Historical review flow

- How tried: `test_folder_discovers_cycles` saved exact historical cutoff and `test_unchanged_no_work` future-source exclusions; directly requested historical `2024-05-03T23:59:59+00:00`-equivalent saved-test scope and the public bounded root at `2024-05-03T23:59:59-04:00`.
- Observed: saved exact cutoff selected in the criterion test; the public bounded root lacks that exact review, reports partial/missing-cutoff gaps and excludes Q3 as `after_cutoff`. It did not silently reinterpret a later review as a historical completion or mutate history. No fresh-host conversational error rendering is claimed for this boundary.

## 15. Missing data flow

- How tried: direct original full-root discovery, missing source/output/verification and required-economic-input criterion cases.
- Observed: two investment-case questions remain incomplete with recovery instructions, while four independent units are reusable. Missing required dependency identities cannot be dropped to force completion.

## 16. Source-check unavailable flow

- How tried: actual new request explicitly limited to local public inputs; checked its returned freshness, observation and no-success state, alongside incomplete-envelope last-success criterion.
- Observed: no credentials fabricated, SEC acquisition not invoked without genuine operator identification, no network request or freshness advancement. Local support remains usable but external freshness is `unverified`; a local publication cannot advance successful external checking. A new live remote failure was not induced.

## 17. Invalid or escaping input flow

- How tried: unsupported-folder `escape`, `symlink`, `duplicate`, ambiguous and incomplete cases; publication's symlink and race preservation cases.
- Observed: invalid references/identities rejected, unchanged-byte assertions passed, no external read/write or execution of document instructions established by these inputs. These are executed boundary checks, not a claim that a conversational host rephrased every error.

## 18. User-edit conflict flow

- How tried: correct-run normal resume and rollback on actual retained useredit fixture copy, plus ten publication preservation cases.
- Observed: exact file-specific conflict for both calls; every case-file byte preserved. User text, staged draft and journal were not overwritten, deleted, refreshed or forced into success.

## 19. Publication interrupted flow

- How tried: `test_interrupted_publication_recovers` for both finish paths, generic multi-issuer interruption cases, shared-target/run-identity tests; inspected native run-05 worker exit 75 and retained incomplete state.
- Observed: draft/journal/proposed output precede review completion; predecessor remains visible and a different run cannot conceal the failed run. Recovery is not falsely complete because some output exists.

## 20. Repeated request flow

- How tried: direct repeated discovery, formatting/mtime variants and independent actual new-host invocation.
- Observed: deterministic decisions and no publication; 46 managed files and imports identical. Native invocation itself still consumed tokens; no zero-cost or global no-work inference.

## 21. Success flow

- How tried: normal complete/linked-provenance criterion test, retained actual bounded run-07 publication and new native checks of saved review/source/assumption/horizon fields.
- Observed: completed review points to prior evidence and preserves original full-scope imports. Only the initially configured bounded questions are complete; full investment-case, 84 historical quarter candidates and A–G obligations remain incomplete. Self-check flags and hashes alone are not analytical truth or advisory sufficiency.

## 22. Recovery or rollback flow

- How tried: clean normal recovery/rollback criterion tests, retained actual run-06 clean recovery and direct edited-fixture attempts on the exact tested helper.
- Observed: clean recovery succeeds and withdrawal restores eligible predecessor while retaining all new/old reports; edited case refuses both actions with no byte changes. Rollback does not delete arbitrary user files or fabricate a historical predecessor at a different cutoff.

## Findings, decisions and skipped steps

- No new fatal/important product defect was reproduced. No important/fatal dismissal was supplied by the closing-review owner.
- This is first independent acceptance for the post-sync target; no row is carried from an earlier acceptance report. Prior native execution is explicitly identified as retained source evidence, not a claimed new replay.
- No `skipped-by-instruction` record was present in intent Constraints or plan Risks. No package-test or finalize-review skip was supplied. The full suite remains owned by finalize-review, not omitted from the workflow.
- The report's resolved choices summarize the retained spec's bounded configuration/adapter, local method/source separation, dependency/fiscal semantics, append-only protection, completion/advice distinction and source-invoked validation. No new product design decision was implemented by this witness.
- Git-memory classification for this report-only commit: routine acceptance evidence capture, no new reopened design decision, newly undisclosed product constraint or product gotcha; no memory trailers required. Exact commit message must pass the deterministic privacy scan. Only report and evidence are to be committed.

## Re-run on 2026-11-16, at 64dd4c0

### Fresh setup and inspected fix scope

- Exact new tested HEAD: `64dd4c0119aa10dd7ef677608878cfcae5249469`. Created a genuinely new clone at `/private/tmp/finance-acceptance-witness-64dd4c0` using `git clone --no-hardlinks /private/tmp/finance-research-continuation /private/tmp/finance-acceptance-witness-64dd4c0`, then detached checkout of that exact SHA. Checkout confirmed `64dd4c0 docs(finance): reconcile live package-capability descriptions`; status was clean before and after verification.
- Re-read the new root README, finance source setup contract, edited JSON interfaces and marketplace, PLAN-DRAFT ownership summary, retained plan delta, `research/07-package-capability-descriptions.md` and `/private/tmp/finance-round1-prose.yaml`. The earlier important inconsistency was fixed, not dismissed: discovery surfaces had incorrectly denied research continuation and made SEC contact identity appear necessary for local reuse. No new fatal/important finding was reproduced.
- Inspected the complete `933710c..64dd4c0` diff: six paths only. Four live description surfaces changed (`README.md`, `obsidian-finance/.codex-plugin/plugin.json`, `.claude-plugin/marketplace.json`, `docs/finance/PLAN-DRAFT.md`), plus the existing plan and new class-sweep research record. No new requirements, runtime change, method change, analysis change or fixture change.
- Independently ran `git diff --name-only 2e135990987f320d0ea391e48b7e55b3fdc2a2e9 64dd4c0119aa10dd7ef677608878cfcae5249469 -- obsidian-finance/scripts obsidian-finance/skills obsidian-finance/tests obsidian-finance/README.md docs/finance/pilots/apple-2024q2-q3/host-continuation`; captured output was empty. This is the exact equality ground for carried behavior, retained actual session transcripts and all earlier criterion tests, not an assumption from the fix title.
- Followed README setup again with the existing Python environment, loaded the shipped helper in the new clean clone and executed both bounded and full-scope discovery with `SEC_USER_AGENT` explicitly absent. No global installation, fresh provider/API obligation, native host relaunch, source fetch or full suite was needed to validate this description-only fix. Earlier actual-host observations remain earlier actual-host observations, with unchanged functional source and inputs.

### Executed re-run checks and captured outputs

Executed via `env -u SEC_USER_AGENT /private/tmp/finance-validation-env/bin/python -c`, with this actual inline body (line breaks added for readability):

```python
import sys,json,hashlib
from pathlib import Path
sys.path.insert(0,"obsidian-finance/scripts")
import research_store as m
r=Path("docs/finance/pilots/apple-2024q2-q3/host-continuation/quarter-check-scope")
before={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in r.rglob("*") if p.is_file()}
x=m.discover(r,"latest","2024-08-02T23:59:59+00:00")
assert len(x["reusable"])==4 and not x["gaps"] and all(d["action"]=="no_analysis_update" for d in x["decisions"])
assert x["external_freshness"]=="unverified"
assert before=={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in r.rglob("*") if p.is_file()}
print(json.dumps({"setup":"source API loaded with SEC_USER_AGENT absent","status":x["status"],"decisions":x["decisions"],"reusable_count":len(x["reusable"]),"gaps":x["gaps"],"external_freshness":x["external_freshness"],"all_fixture_files_unchanged":True},sort_keys=True))
plugin=json.loads(Path("obsidian-finance/.codex-plugin/plugin.json").read_text())
market=json.loads(Path(".claude-plugin/marketplace.json").read_text())
assert any(p["name"]==plugin["name"] for p in market["plugins"])
assert all((Path("obsidian-finance/skills")/s/"SKILL.md").is_file() for s in ("sec-data","finance-research"))
print("PASS: both edited JSON parse and both advertised source skills exist")
```

The inline probe imported `obsidian-finance/scripts/research_store.py` by its actual path. It read the clean clone's committed `host-continuation/quarter-check-scope`, captured all fixture paths and exact SHA256 bytes before discovery, called the public `discover` API, asserted four reusable units, no gaps, two no-work decisions and unverified external freshness, then compared the full fixture map. No manually constructed work list or mocked output was supplied. Captured output:

```json
{"all_fixture_files_unchanged":true,"external_freshness":"unverified","gaps":[],"reusable_count":4,"setup":"source API loaded with SEC_USER_AGENT absent","status":"complete"}
```

The returned decisions were `aapl/2024Q2/bounded-baseline-q2` and `aapl/2024Q3/run-07-q3`, both `no_analysis_update`, preserving the existing publication-attempt observation. Edited JSON parsed successfully; marketplace finance name matches plugin name and both advertised `skills/sec-data/SKILL.md` and `skills/finance-research/SKILL.md` exist. Captured: `PASS: both edited JSON parse and both advertised source skills exist`.

A separate real full-root discovery, again under `env -u SEC_USER_AGENT`, returned `status=partial`, four reusable units, exactly two `resume_incomplete_work` decisions for `investment-case`, and `external_freshness=unverified`. Captured: `PASS: full-scope discovery keeps four reusable units, two pending investment-case questions, partial status and unverified freshness`.

Re-read the whole four changed paragraphs/interfaces rather than relying on matching a word: root README separates acquisition from agent-led research; plugin description/interface and default prompt identify designated managed equities folder, scope/cutoff, protected edits and gaps; marketplace exposes both skills and unverified installation; current program ownership summary includes both while retaining incomplete broader research. Old acquisition-only intake/history remains historical. No scheduler, trading, global install, completed investment case or installed-host proof was advertised. Verified all four local links from the complete root finance section resolve:

```text
PASS: all four root finance-section links resolve
obsidian-finance/README.md
obsidian-finance/skills/sec-data/SKILL.md
obsidian-finance/skills/finance-research/SKILL.md
docs/loom/2026-11-16-finance-research-continuation/evidence/host-sessions.md
PASS: scope/cutoff prompt and acquisition-only contact requirement are explicit
```

Ran only focused criteria, not a full package suite:

```sh
/private/tmp/finance-validation-env/bin/python -m pytest \
  obsidian-finance/tests/test_research_store.py::test_folder_discovers_cycles \
  obsidian-finance/tests/test_research_store.py::test_unchanged_no_work \
  obsidian-finance/tests/test_research_continuation.py::test_source_declared_new_quarters_without_saved_conversation \
  -q -p no:cacheprovider
```

Captured `.... [100%]` and `4 passed in 0.09s`, exit 0. No substitute tests for the four new wording paragraphs were created. Full suite remains `python3 -m pytest obsidian/tests obsidian-finance/tests -q -p no:cacheprovider`, owned by finalize-review and blocking acceptance on failure; this witness does not assert the owner's supplied full-suite result as its own run.

### Per-row re-run decision, checked against the entire fix diff

- 1: re-tested — read all four live discovery surfaces, followed every root finance link and source setup in the fresh clone, ran bounded and full-root discovery without SEC identity; identified two fiscal quarters, four reusable units and two unresolved full-scope questions without a supplied task list.
- 2: carried over — the entire script/skill/method/test/public-fixture trees are byte-identical; the fix changes no new-quarter, economic/local-method dependency, interruption or reuse behavior, so prior complete criterion and native incremental evidence remains applicable.
- 3: carried over — no no-work, typed-projection, formatting/mtime or publication code/input changed; earlier formatting/mtime and actual-host no-duplicate evidence remains applicable. Setup's incidental no-work result is additional evidence, not a substituted new native replay.
- 4: carried over — research envelopes, original sources, cutoffs, method/assumption identities, horizon rules, outputs and historical records are unchanged; description prose does not revise their meaning or advisory status.
- 5: carried over — no freshness/state/validation/publication/recovery helper, protection rule or failure fixture changed; exact prior useredit and interruption checks remain valid over all named failure surfaces.
- 6: re-tested — checked all four changed discovery descriptions now expose continuation while preserving source-invoked versus installed-host limits; loaded the exact new source successfully; verified complete functional source/fixture equality and retained actual native evidence for new-quarter/change/resume/no-work plus the prior independent ephemeral request. Did not launch a redundant host or label a subprocess/test as a new host.
- 7: re-tested — followed root package/skill/evidence links; parsed the actual Codex interface and marketplace; inspected the new defaultPrompt for designated folder and cutoff; loaded source helper and discovered both persisted scopes without acquisition credentials. Installation itself remains unverified.
- 8: carried over — empty/unsupported-folder validation and recovery text in the helper/skill are unchanged; no changed manifest/default prompt bypasses missing-scope refusal.
- 9: carried over — progress reporting instruction, checkpoint publication, pending-question configuration and saved partial research are unchanged; the description now correctly exposes existing behavior without changing it.
- 10: carried over — fiscal-source identity, quarter discovery, original arrival fixture and append-only research are unchanged; description edits do not alter the source-declared quarter boundary.
- 11: carried over — economic/local-method/assumption dependency tracking, transitive synthesis, independent reuse and old-review links are unchanged, including all prior actual changed-method source inputs.
- 12: carried over — interrupted-work detection, reusable-unit validation, pending work and normal resume are unchanged; no process/session continuation mechanism was edited.
- 13: carried over — local no-work reporting, freshness qualification and publication avoidance instruction/code/fixtures are unchanged; retained actual native no-work and exact-byte preservation remain applicable.
- 14: carried over — historical exact-cutoff selection, future-source exclusion, missing-review gaps and preserved research are unchanged; the new default prompt still requires an explicit assessment cutoff.
- 15: carried over — missing-input/question semantics, recovery information and independent work are unchanged; no required investment-case question or original scope was removed by the wording fix.
- 16: re-tested — inspected all four changed surfaces for acquisition-only SEC contact requirements and preserved freshness/installation limits; actual local bounded and full discovery ran without SEC_USER_AGENT and returned external freshness unverified. Original attempt/success records remain unchanged; no external request/success was invented.
- 17: carried over — no root/path/symlink/identifier validation, anchored I/O or instruction-inertness rule changed; prior executed invalid/escape cases remain valid over the complete named boundary.
- 18: carried over — no snapshot, output/draft/hash protection or resume/rollback conflict path changed; the exact retained edited-case inputs and earlier all-bytes preservation evidence are unchanged.
- 19: carried over — staging, journal/run identity, final completion point and interrupted-publication observations are unchanged; prior real worker interruption and mechanical recovery evidence remain applicable.
- 20: carried over — stable discovery/reuse and no-duplicate publication behavior plus inputs are unchanged; no repeated invocation or scheduler was introduced by the new description/default prompt.
- 21: carried over — completion conditions, source/provenance/assumptions/horizons/gap envelopes and saved links are unchanged; the four descriptions explicitly retain incomplete full investment research rather than broadening success.
- 22: carried over — normal recovery/withdrawal, user-edit conflict, preserved drafts/history and predecessor rules are unchanged over all previously exercised clean/edited cases.

No instructed skip, no dismissed important/fatal finding, no new product fix and no native-host cost occurred in this re-run. A–G, complete investment-case diligence, external freshness and installed-plugin loading remain outside what these bounded passing results establish. The initial 59-test result, first native request/counter, raw artefact hashes, failed launches, witness probe mistakes and retained original host audit failures above are preserved, not reset.
