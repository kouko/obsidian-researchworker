# Actual fresh-host sessions — public isolated validation

## Scope and identity

W3-01 uses the existing `/Users/kouko/.local/bin/codex`, version 0.169.0,
with existing ChatGPT authentication. No model/provider override, global
installation, trust mutation, formal vault write or additional paid API/provider
obligation was selected. Public Apple fiscal 2024Q2/Q3 material is a validation
case; the generic helper and source skill have no Apple-specific behavior.

The fixture root is `/private/tmp/finance-host-public-20261116`. It contains
copied public quarter-packs and retained valuation/forecast/competition notes,
plus an uninstalled copy of the package source. Skill execution is explicitly
**source-invoked**, not proof of installed-plugin discovery. Public source
content and local authorship dates must still be distinguished.

Preflight repeated the allowlisted model/effort/provider selectors and presence
booleans only: selected model `gpt-6.1-sol`, effort `low`, no explicit
`model_provider`, no selected-provider override, and no nonempty
`OPENAI_BASE_URL`, `OPENAI_API_BASE`, `OPENAI_API_KEY`, `CODEX_HOME`,
`CODEX_MODEL_PROVIDER` or `SEC_USER_AGENT`. Login reported
`Logged in using ChatGPT`; this alone was not actual routing proof.

## First failures and request proof

The first normal outer-sandbox invocation exited 1 before a model request:

```text
WARNING: proceeding, even though we could not create PATH aliases: Operation not permitted (os error 1)
Error: failed to initialize in-process app-server client: Operation not permitted (os error 1)
```

The identical host command was then allowed through the outer execution
approval mechanism; the host retained its normal read-only sandbox and guards.
No dangerous sandbox/hook bypass, `--trust`, `--ignore-rules`, alternate
provider or config override was used. This is a permitted process launch, not
an application-level guard bypass.

```sh
/Users/kouko/.local/bin/codex exec \
  --cd /private/tmp/finance-host-public-20261116 --sandbox read-only \
  --ephemeral --skip-git-repo-check --color never \
  --output-last-message /private/tmp/finance-host-public-20261116/probe-escalated-last.txt \
  - < /private/tmp/finance-host-public-20261116/probe-prompt.txt
```

The native header reports provider `openai`, model `gpt-6.1-sol`, effort `low`,
session `01a1e20f-7954-7d90-8a15-596f70f1a2cb`. The actual response was
`HOST_REQUEST_OK` and exit status 0. This establishes a successful request to
the selected host/runtime, not a claim about universal quota or future cost.

## Behavioral evidence

Separate direct checks by the W3 implementer recompute numbers and read exact
saved bytes independently of the CLI author's self-check. They are not a
fresh-context independent research/acceptance review or a closing attestation.

Each invocation uses `codex exec` directly, with `--sandbox workspace-write`,
`--ephemeral`, `--skip-git-repo-check`, no resume/fork/model override, the same
public `--cd`, its own prompt on stdin and separate transcript/last-message
paths. Outer process-launch approval is retained; normal host guards apply.

| Run | Native session ID | Observed behavior | Result |
|---|---|---|---|
| 01 | `01a1e210-932f-7c92-9b54-926933d9f6a6` | Discovered Q2/Q3 originals, actually opened selected original SEC passages, computed Q3 growth/counterevidence and fiscal identity, saved partial checkpoint | Exit 0; Q3 growth/identity reusable; investment-case pending |
| 02 | `01a1e214-0db5-7571-a802-ab011278fcb2` | Fresh discovery detects local method v1→v2, recomputes Q3 revenue/gross margin while reusing exact independent identity output/check | Exit 0; managed predecessor and all 28 pre-run managed paths preserved |
| 03 | `01a1e21d-ba5c-71f1-a551-30ac424d942d` | Fixed-helper discovery retains unreviewed Q2; actual Q2 source-page check; Q2 bounded research plus linked Q3 v3 growth recomputation; Q3 identity preserved | Exit 0; four units reusable across Q2/Q3, both investment-case questions pending; all 44 pre-run managed paths preserved |
| 04 | `01a1e222-7894-7962-9874-22578d7fbe9b` | Fresh unchanged-local check of Q3 completed growth/identity | Exit 0; all 78 managed files byte-identical, no additions/deletions/duplicate reviews; full root still has both required investment-case questions pending |
| 05 | `01a1e226-6e0e-7111-82b7-2e1b147b39ab` | Two isolated clean/useredit copies; substantive unfinished MD&A progress note; deliberate save-worker exit 75 at final review creation | Exit 0 for host; both worker exits 75, journals/drafts/outputs present, final review absent, predecessor view preserved; no recovery in this session |
| 06 | `01a1e229-8a0b-7731-ae04-388f8245de9a` | Fresh discovery of both interrupted cases; normal clean resume then rollback; normal edited-case resume and rollback conflicts | Exit 0; clean predecessor view restored with all new/old reports retained; both edited-case operations refused without changing user text, draft, journal or any case file |
| 07 | `01a1e22c-e025-71c3-9b81-7080e6ad8870` | Separate initially bounded quarterly-study scope: Q2 baseline preserved, actual Q3 original-source arrival discovered, source indexes/pages checked and Q3 recomputed | Exit 0; normal complete publication only for required growth/identity, four Q2/Q3 units reusable with zero bounded gaps; all 27 prior managed files unchanged |
| 08 | `01a1e23b-5819-7de3-b47e-fcc5799cbbbe` | Fresh actual continuation of the initially bounded now-complete Q2/Q3 study | Exit 0; both quarters no_analysis_update, four reusable units, zero bounded gaps, no publish/duplicate; all 46 managed files identical. Whole-root additions audit FAILED due to two W3-added external measurement files; see below |

All substantive native runtime headers report provider `openai`, model `gpt-6.1-sol`,
reasoning effort `low`. This is observed host routing, not model self-report.
Run 01 independently read Q3 cover/selected MD&A and Q2 selected MD&A through
web open/find. It does **not** claim complete raw HTML, same-context XBRL
validation, filing-index publication/amendment coverage or whole-case freshness.
SEC acquisition was not run without genuine local `SEC_USER_AGENT`.

Run 01 computes revenue YoY 4.865704%, compared with Q2 -4.305327%, and
reconciles category changes to +3,980 USD million. Run 02 adds current/prior
gross margin 46.257155%/44.516303%, +1.740853 percentage points. It preserves
identity output digest `75a9bcdf75a5600ead172f1640031bfe8861e7f19d686edc83bd938e026c11fa`
and check digest `c226637441de859800b328549e89a927a50ff47571d35d1ddb17c6298293b0a0`
with their original paths. No new external attempt/success is claimed in run 02;
`last_success` remains absent and the earlier attempt observation is retained.
The original v1/v2 declarations remain separate from 2024 economic evidence,
but their exact claimed authorship times were subsequently found erroneous;
see the correction below.

### Fixture author-time correction

The W3 fixture preparer supplied v1 midnight and v2 02:10 UTC as exact local
method author timestamps without exact-time evidence. The latter was even in
the future relative to the execution clock when discovered. These are preserved
original fixture declarations, not verified actual authorship. This evidence
error belongs to fixture preparation, not the helper. At the real current UTC
time `2026-11-16T02:08:46.931664+00:00`, the method text/metadata was revised
as `v3-authorship-corrected`. A new host must reverify/recompute affected growth;
it cannot attach the new identity to the old output. Old reports and wrong
values remain available with `AUTHORSHIP-CORRECTION.md`; no 2026 value supplies
2024 economic availability. Subsequent results must cite the actual revision.

### Preserved failures and limitations

Initial code at `c56676d94d353d1306d7ccb97c89abb9c5c0331f` has a discovery
defect: after Q3 is saved, the still-unreviewed eligible Q2 source disappears
from the missing-quarter decisions because the asset already has a cycle.
Before/after discovery and run-01-report preserve this. Q2 was never marked
complete; the defect was reported to the owning implementer and no helper was
edited by W3. The owning implementer repaired this at
`b4ee26d76b1c6f5fb49b111e40ca54395e57e29b`. Only the copied helper was
updated before run 03: SHA256 changed from
`4a4bbe04a6b01848be9d61f531bcbd5d8e5b12fd86642150f27149a215422c0e` to
`fd0cede6aae38590bc09a07bc7935e87bd5986e1350f2c64fe35e7db6aba8526`;
`runtime-source-v2.json` records this source boundary. The genuine new run 03
then observed Q2 missing, Q3 growth invalidated and Q3 identity reusable,
performed affected work, and retained both quarter records after publication.
This supersedes the defect as a current behavior claim without deleting its
original evidence.

Run 07's first final audit also raised `AssertionError` because it wrongly
required `observations` to be empty. The actual observation was the legitimate
`last_attempt`, with no gap or unfinished publication. Its corrected audit
checks observation type; the initial error and traceback remain, and no managed
file was changed or republished. The existing
[README saved-folder contract](../../../../obsidian-finance/README.md#read-only-saved-folder-discovery-metadata-v1)
(lines 398–399 in this tree) explicitly retains optional `execution_state`,
`last_attempt` and `last_success` as unmodified observations; the
[publication/recovery contract](../../../../obsidian-finance/README.md#protected-local-publication-and-recovery)
(lines 518 onward) places unfinished publications in discovery gaps.
The actual nonempty observation is `last_attempt` for
`aapl/2024Q3/run-07-q3` at `2026-11-16T02:34:37.927015+00:00`.
Status, gaps, decisions and each observation's meaning—not blanket emptiness—
are the correct checks. No helper or skill change was made to silence this
one-off audit assumption.

Run 02's broad self-check initially raised `AssertionError` because it included
the actively growing transcript in its whole-root inventory. Diagnosis retained
the exact failure and identified that transcript as the sole difference; the
final validation qualifies this. Independent managed-only verification confirms
all 28 pre-run `investing/` paths still match. Transcript growth is not a lost
research report and does not invalidate the saved output/hash reuse proof.

Neither native subagents nor Python test results count as new-host execution.
Exact public prompts/transcripts, managed records and before/after hashes are
retained under pilot `host-continuation/` after inspection. The initial eight
managed inputs are also retained byte-identically in `fixture-initial/`, checked
against every before-run-01 digest; this reconstruction never alters live data.


### Controlled interruption and input protection

Run 05 workers use an explicitly retained in-memory fault hook to exit 75 at
final `review.json` creation after durable journals/drafts and proposed outputs
exist. The package source is unchanged. This is a deliberately interrupted save
process driven by the actual CLI host, not an assertion of an unexpected host
crash. No pytest/native-subagent result is counted in its place.

Between actual invocations the fixture preparer appended explicit user-edit
simulation text to only the `useredit` proposed MD&A note. `run-06-user-edit.json`
records exact before/after hashes and the unchanged original draft. In actual
new run 06, normal `recover(..., action="resume")` returned `checkpoint` for
`clean`, then `action="rollback"` returned `rolled_back`. The original
`run-03-q3` view is visible again, while recovered report, note, draft and
withdrawal remain. Both normal operations on `useredit` returned:

```text
Publication conflict: user edited investing/assets/equities/aapl/cycles/2024Q3/2024-08-02-run-05-useredit-q3/investment-case-progress.md
```

Exact calls/results/tracebacks are in `run-06-helper-calls.json`. Direct
independent hash checks confirm the user edit and original draft remain exact,
the conflicting target has no completed/withdrawn marker, the clean withdrawn
review still exists, and all 78 original main managed paths remain identical.
No precondition refresh, journal rewriting, deletion or forced recovery occurred.
The conflicting unfinished run intentionally remains pending for explicit human
resolution; it is not labeled recovered or complete.

### Independent bounded scope and actual source arrival

`quarter-check-scope/SCOPE.md` defines its initial required questions as only
quarterly growth/gross-margin arithmetic and bounded fiscal identity. It never
claims complete company investment research. The original main root keeps all
three questions, including required `investment-case`, unchanged.

The retained `SETUP.py` uses normal publication to adopt the already actual,
substantive and verified run-03 Q2 units into a **new** bounded baseline. The
original full-scope review/requirements and every original Q2 file are retained
byte-identically under `imports/original-q2-review/`; none is edited to remove a
question. New asset configuration, scope and normal review are distinct files.
Direct checks verify the two original question definitions/source identities,
all output/check bytes and method-v3 identity. The baseline normal publish is
`complete` only within the new two-question study; baseline discovery has zero
gaps and `no_analysis_update`. This initialization is fixture preparation using
prior actual research, not another actual CLI session.

Only after retaining `arrival-before.json` does the constructor add the two
real Q3 original input files; every old baseline path/hash remains unchanged.
The adjacent source-bound original accessions have different fiscal endpoints
and publication dates. `arrival-added.json` names this controlled historical
source arrival, not a newly published 2026 filing. The actual new run 07 then
observes Q2 reusable and Q3 unfinished, performs affected work, checks original
SEC filing indexes/dates and the Q3 document, and preserves completed Q2.
Actual new run 08 independently read saved analysis, citations, counterevidence,
method/source identities and recalculated both quarters, then reported genuine
`no_analysis_update` for both. It called no publication and all 46 managed
paths/bytes remain identical, with no duplicate review. External freshness and
attempt/success observations were not advanced. This cannot erase the full
main-root investment-case gaps or reduce Stages C–G.

Run 08's **whole-root additions audit failed**: while it was auditing, the W3
preparer concurrently added `after-run-08.json` and
`independent-run-08-check.json` outside `investing/`. The exact AssertionError,
two additions and attribution remain in the transcript/verification/report.
This was measurement interference by the W3 preparer. It is not an error-free
whole-root run, and the narrower managed-46-file equality check does not prove
zero additions throughout the root. The actual host did not publish or alter
research because of these files. No repeat run, data edit or scoring change
was used to hide the failure.

## Observed operational metrics

The native CLI reports these raw `tokens used` counters. They are not inferred
billing/cached-token categories or dollars. Scopes differ, so this is not an
A/B benchmark, and no 84-quarter cost is extrapolated. In particular, the
unchanged-local run 04 still reports 49,187 tokens; no-work is not zero host
cost. Actual individual start/end timestamps and wall duration were not logged
and remain unknown. These counters do not supply missing native-trial metrics.

| Actual invocation | CLI reported tokens used |
|---|---|
| probe-escalated | 15,789 |
| run-01 | 71,272 |
| run-02 | 56,406 |
| run-03 | 87,405 |
| run-04 | 49,187 |
| run-05 | 69,723 |
| run-06 | 57,240 |
| run-07 | 87,144 |
| run-08 | 64,762 |

## Acceptance boundary

A completed bounded growth/identity question is not a completed investment case.
The fixture deliberately retains investment-case, market-price, narrative and
full competition/valuation gaps. Unknown external freshness must stay unknown;
last attempted source access and last successful verification remain distinct.
The wider A–G program, 84 historical quarter candidates and additional asset
methods are separate obligations and remain incompletely delivered.
