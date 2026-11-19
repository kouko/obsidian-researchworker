# Start and update a research project — acceptance test evidence

Tried on 2026-11-19 at `0fa6447ef59f3baedf34355899c088a9f7cf717a`. The source checkout was clean at the beginning of acceptance. The isolated Codex marketplace loaded `obsidian@obsidian-researchworker` at 4.2.0. Compared 94 tracked skill and Codex manifest files with the installed cache and found zero differences. Native session inputs were disposable vaults and local synthetic library notices.

Native runs used `CODEX_HOME=<isolated-profile> codex exec --skip-git-repo-check --sandbox workspace-write --json -C <case-dir> '<request>'`. Separate confirmation or refusal used `codex exec --sandbox workspace-write --json resume --skip-git-repo-check <thread-id> '<reply>'` in the case directory. The case names below refer to captured JSONL in the disposable run directory. Vault comparisons record sorted paths, types, and SHA-256 digests of regular files.

Focused automated tests used the installed dbt-redshift Python from the plugin directory:

```sh
python -m pytest -q -p no:cacheprovider \
  tests/test_research_transaction.py::test_create_first_round_then_resume \
  tests/test_research_transaction.py::test_create_rejects_unsafe_target_without_changes \
  tests/test_research_transaction.py::test_interrupted_first_round_is_preserved_but_cannot_resume \
  tests/test_research_transaction.py::test_replay_does_not_write \
  tests/test_first_round_integrity.py
```

Result: `8 passed in 0.52s`. The full package test command is `python3 -m pytest -q -p no:cacheprovider` from `obsidian/`. Final review runs the full suite and blocks acceptance on failure.

## 1. 從零啟動研究後，可在主題資料夾找到本輪問題、結論、證據與待查事項。

- How I tried it: Asked for the first round of the library project, using the original November schedule in an empty synthetic vault. Confirmed the proposed scope, target, and outputs in a separate message.
- What came back: The topic entry provides the question, monthly total, weekly total and a link to the completed first report. The report links the archived original and identifies actual operations and dates outside November as unresolved by the supplied evidence.
- Evidence: `project.first.jsonl`, `project.response.jsonl`. First-round entry records 30 scheduled days, seven per complete week, and one in each partial week. The round links `sources/raw/original.md` and says the actual number of open days was not recorded.

## 2. 另一個對話能接續第一輪。新證據造成改判時，仍可回查舊結論採用的證據。重送相同來源不增加筆記或版本。

- How I tried it: Started a fresh conversation on the first round's vault, supplied a corrected library notice and approved the proposed update in a later message. Compared the before-update copy with the saved project and started a new replay conversation with the same correction.
- What came back: The conclusion changed from 30 to 25 scheduled days in November, or from seven to six in a complete week. The original report and archived source were byte-identical. The new report links both and adds the corrected notice. Replay result is recorded in row 14.
- Evidence: `project.update.jsonl`, `project.update-approved.jsonl` and `project-created-before-update`. Comparing the before/after trees showed a changed entry, one new report and one new raw source.

## 3. 已存在的同名研究內容受到保留。建立第一輪時，只新增當輪實際需要的筆記。

- How I tried it: Compared the confirmed first round with the empty baseline. Requested a new project at an existing topic folder that contained one private note, and stopped at the response.
- What came back: The first round contained three files: one entry, one completed report and one archival source. The same-name request produced an alternate proposal and waited. The existing vault snapshot matched the initial snapshot byte-for-byte.
- Evidence: `project.response.jsonl`, `project-created-before-update`, `existing.first.jsonl`, `existing.before.json`. The focused existing-folder rejection preserved the existing file.

## 4. 單篇研究維持產出獨立研究筆記的行為。

- How I tried it: Requested one detailed standalone note comparing initial scheduling, subsequent corrections, and records of actual operation, using the local original notice only.
- What came back: One Markdown note under `research/`; its response linked that note and the vault gained no topic folder or history.
- Evidence: `deep-note.first.jsonl`. Output: `research/2026-11-19 河岸分館的排定與實際開館口徑.md`.

## 5. Project proposal

- How I tried it: Described research needing a future correction round without directing Codex to create a project. Separately requested a new project and declined the confirmation.
- What came back: Codex proposed a sensible topic and asked for approval, but it opened the original source before proposing the round and acknowledged the early read. In the explicit request, it read only the skill and listed paths before asking. The refusal produced no tool calls and preserved the vault snapshot.
- Evidence: `proposal.first.jsonl` records the completed shell call `cat <cached-project-skill>; rg --files ...; cat original.md` and the final acknowledgement of the premature read. This violates the spec's confirmed requirement to perform only target checks before agreement. The explicit decline control is in `decline.first.jsonl`, `decline.response.jsonl` and `decline.before.json`.

## 6. First round

- How I tried it: Requested a new project in an identified vault and then sent separate explicit consent.
- What came back: The first turn listed paths and read the installed skill, then asked for approval. It neither read the source contents nor called a writer in that turn. The consent turn wrote a completed first round with its archived source.
- Evidence: `project.first.jsonl` and `project.response.jsonl`; see row 1 for the saved result.

## 7. Missing target

- How I tried it: Requested a project without naming a topic.
- What came back: Codex asked for the topic and proposed a default vault location. It listed paths and did not write.
- Evidence: `missing-target.first.jsonl`; the shared decline-case vault still matched `decline.before.json`.

## 8. Existing target

- How I tried it: Requested a start at the same name as a folder containing a private note.
- What came back: Codex identified that content, offered an alternate folder and asked for approval. The response did not explicitly offer to resume this folder, which had no completed research round.
- Evidence: `existing.first.jsonl`. The directory and retained note matched `existing.before.json`.

## 9. Update

- How I tried it: After creating the first round, opened a fresh Codex conversation and requested an update using only `correction.md` as new evidence. Agreed to the proposed update after reading the proposal.
- What came back: The first turn read the skill and listed files, then asked for a later reply. Following approval Codex saved the correction and reported the changed judgment. The first round and its archived evidence were byte-identical before and after.
- Evidence: `project.update.jsonl` and `project.update-approved.jsonl`. The second report links `history/2026-11-19-r01.md`, `sources/raw/original.md` and `sources/raw/correction.md`. Additional evidence within the same confirmed round was not separately tried.

## 10. Missing saved round

- How I tried it: Requested an update of a topic with an entry pointing to missing `history/R01.md`. Confirmed the proposed round separately.
- What came back: The response identified the missing report and stopped project writes. The vault snapshot stayed identical. The approval turn also compared the supplied local notices even though the topic could not be resumed.
- Evidence: `incomplete.first.jsonl`, `incomplete.response.jsonl`, `incomplete.before.json`.

## 11. Interrupted first save

- How I tried it: Ran the focused test `test_interrupted_first_round_is_preserved_but_cannot_resume`, which stops the process after saving evidence and before publishing the topic entry, then invokes inspection.
- What came back: The incomplete-first-round diagnostic was returned, and the existing files stayed unchanged. `test_create_concurrentedit_stayspending` also passed.
- Evidence: `obsidian/tests/test_research_transaction.py::test_interrupted_first_round_is_preserved_but_cannot_resume` and `obsidian/tests/test_first_round_integrity.py::test_create_concurrentedit_stayspending`. Native conversation for this exact interruption was not exercised.

## 12. Destination appeared while researching

- How I tried it: In a disposable vault asserted the topic target was absent, prepared a valid three-file create plan, then created the destination with one external note before invoking `research_transaction.py create <vault> <target>`.
- What came back: The command failed with `research transaction: project destination already exists`. The external note was the only file after rejection and its contents were unchanged.
- Evidence: CLI diagnostic and independent postcondition. Native conversation offering alternatives after this late collision was not exercised.

## 13. Unsafe destination

- How I tried it: Requested a native project targeting `vault/../outside-project`, then exercised traversal and symlink variants with the transaction tests.
- What came back: Codex identified the path as outside the vault, offered a safe alternate location and waited. The native command list contains skill and directory reads only. Both transaction variants rejected the proposed path without changes.
- Evidence: `unsafe-target.first.jsonl` and `test_create_rejects_unsafe_target_without_changes` parameterized cases `symlink` and `traversal`.

## 14. Replay

- How I tried it: Started a fresh conversation requesting a replay of the byte-identical correction against the updated project. Sent consent separately, then compared the vault's research directory against the copy taken after the second round.
- What came back: Codex recognized that the original bytes and current conclusion already matched the supplied correction, and reported no new round. The before/after directory comparison found no differences.
- Evidence: `project.replay.jsonl`, `project.replay-approved.jsonl`, `diff -qr <project-updated-before-replay> <project/vault/research>` exit 0 with no output. Focused `test_replay_does_not_write` passed.

## 15. Standalone

- How I tried it: Used the detailed standalone prompt in row 4, which included a future correction scenario while asking for one independent note.
- What came back: Codex saved one standalone note without proposing a project or asking for project confirmation.
- Evidence: `deep-note.first.jsonl` and final vault paths.

## Re-run on 2026-11-19, at `0fa6447`

The earlier explicit-start conversation proceeded from its initial request into project creation. A separate initial decline-case conversation also read the evidence before consent. The revised skill requires a later confirmation turn and prohibits substantive evidence reads, research and writes before that confirmation. The explicit start, decline and update turns honored the gate on this run. The implicit proposal still read the source early. Re-tested preservation on interrupted and conflicting writes because the fix range also changed first-round publication checks.

## Re-run on 2026-11-19, at `26a54d4`

The fix changes only the skill description, skill procedure, and vault router. It leaves the transaction helper and standalone skill documents unchanged. Retained the earlier evidence above so the failed implicit proposal remains visible.

- Setup: Compared 94 tracked runtime files at `26a54d4` with the fresh native Codex cache. Zero differences.
- 1, 3, 6: re-tested — `r3/project.first.jsonl` loaded the skill by itself, listed target/source paths, then asked for confirmation. After separate approval, `r3/project.response.jsonl` saved exactly three files in the selected vault: entry, completed R01, and the archived original. The entry states the question, 30 scheduled days, seven per full week, links R01, and records actual operation and cross-month totals as unresolved. R01 links the archived original.
- 2, 9: update re-tested — `r3/project.update.jsonl` ended with a separate approval request after reading the skill and checking paths. The approved turn saved R02 with 25 scheduled days and six per full week. Comparing the created and updated trees found one modified entry, the new R02, and the new archived correction. R01 and the archived original matched byte-for-byte. R02 links both.
- 4, 15: re-tested — the exact natural-language deep-note prompt from the prior run selected knowledge and Markdown skills rather than standalone research. It produced a single file in the workspace's `research/`, beside the selected vault; the vault was unchanged. A separate request expressly invoking the standalone skill loaded `obsidian-research` and saved one note under the selected vault's `research/`. A further natural prompt run from inside the vault selected Markdown and saved one note in the correct vault. See `r3/deep-note.first.jsonl`, `r3/direct-note.first.jsonl` and `r3/normal-note.first.jsonl`.
- 5: re-tested — `r3/proposal.first.jsonl` records the skill loaded by itself, followed by `pwd -P` and `ls -ld original.md <topic>`. The assistant proposed a workspace, one dated round and retained evidence for next month's correction. It stopped for a separate reply without reading the source body. That prompt located the vault under the workspace, but metadata checks examined the workspace instead of the child vault. A second implicit proposal explicitly selected the child vault and checked it correctly, also with no evidence reads. See `r3/proposal-explicit-vault.first.jsonl`.
- 6 control: `r3/decline.first.jsonl` only loaded the skill and checked metadata before asking. Separate refusal left the vault unchanged.
- 8: re-tested — `r3/existing.first.jsonl` loaded the skill and listed paths; it kept the old folder and proposed an alternate location because the fixture contained one standalone note and no completed round. `r3/project.complete-collision.jsonl` requested a start at an existing complete project; it offered both an alternate folder and resuming that same project, then waited. Neither proposal issued a write call.
- 10: re-tested — `r3/incomplete.first.jsonl` loaded only the skill before asking for confirmation. The approved turn said the saved R01 was missing, and the vault matched its original snapshot.
- Focused automated coverage re-run at this revision, adding `tests/test_skill_inventory.py` to the above selection: `10 passed in 0.51s`.

## Re-run on 2026-11-19, at `39205fa063797616bc3e4a083b3043d04adf91a2`

This candidate changes only the project, standalone, and vault-router skill instructions. The latest changes make the project proposal resolve the selected vault by its `.obsidian/` directory and route one-off notes from supplied local sources to the standalone research skill. The transaction helper is byte-identical to R3. Runtime captures for this revision were recorded under `/tmp/obsidian-project-acceptance-r4/`; the earlier sections preserve the previous failures.

- Setup: Compared 94 tracked skill and Codex manifest paths at this commit to the isolated installed 4.2.0 cache. Zero differences.
- Focused automated coverage re-run at this revision: `10 passed in 0.53s` using the R3 selection.
- 1, 3, 6: re-tested — `r4/project.first.jsonl` loaded the skill separately, verified the selected vault and checked the target path. The proposed scope used only the original notice and named the entry and report as outputs. Following separate approval in `r4/project.response.jsonl`, the vault contains only the entry, completed R01 and original archive. The index states the research question, 30 scheduled days, the report and archive links, and actual operation and December as open. The first report identifies how to count partial weeks. `r4/decline.response.jsonl` confirmed the refusal and the unchanged vault snapshot.
- 4, 15: re-tested — `r4/deep-note.first.jsonl` used the same natural-language request as R2 and R3. It loaded `obsidian-research` and Markdown, identified the selected child vault, and saved and linked one standalone research note within it. The only added vault path is `research/2026-11-19 河岸分館排定與實際開館口徑.md`. The note separates scheduled from actual opening days and uses the supplied local source.
- 5: re-tested — the identical natural request that exposed the earlier premature read and vault mismatch loaded only the project skill, checked the child vault and path metadata, and proposed `vault/research/河岸分館開館天數/`. The response asked for another message before doing evidence work. No source body or writer call appears in `r4/proposal.first.jsonl`.
- 7: re-tested — `r4/missing-target.first.jsonl` identified the child vault through its marker, then asked for the study topic before doing research or creating files.
- 8: re-tested — `r4/existing.first.jsonl` offered an alternate path and preserved the legacy note. With a completed project present, `r4/project.complete-collision.jsonl` checked only location metadata, then offered to create elsewhere or resume the completed project. No writer ran while awaiting the choice.
- 2, 9: update re-tested — `r4/project.update.jsonl` was a new conversation. Before asking for consent it only loaded the project skill and listed paths. After consent, the helper safely rejected a duplicated relative vault name and a plan that referenced the new R02 as the prior round. The assistant corrected both in that same turn. The report then recorded 30 → 25 scheduled days and seven → six per full week, and linked the unchanged R01 and original archive. The post-update diff found one modified index and two additions, R02 and the archived correction. An independent path and byte check found that all nine saved Markdown links resolve within the topic, both archived notices match their supplied bytes, and R01 is unchanged. See `r4/project.update-approved.jsonl`. Mid-round additional input remained outside the tested sequence.
- 10: re-tested — `r4/incomplete.first.jsonl` checked the vault marker and identified saved-file paths before proposing an update. After approval, `r4/incomplete.response.jsonl` reported the missing completed round and stopped before comparing the supplied notice. The vault still matched the pre-test snapshot.
- 11, 12: transaction behavior carried over — the transaction helper is unchanged, and the focused interruption and destination-rejection tests passed again. Native conversation after these precise fault injections remains unverified.
- 13: re-tested — `r4/unsafe-target.first.jsonl` resolved the supplied traversal path outside the verified vault, proposed a contained location, and stopped for consent. The only calls loaded the skill or printed path metadata.
- 2, 14: replay re-tested — `r4/project.replay.jsonl` asked for separate consent and `r4/project.replay-approved.jsonl` completed after consent. It reported a byte-identical source and an unchanged result of 25 scheduled days, with no new round. `diff -qr <project-updated-before-replay> <project/vault/research>` exited 0 and printed nothing. Separate SHA-256 path snapshots also confirmed that the decline, existing-only and incomplete vaults matched their respective baselines.

## Re-run on 2026-11-19, at `7201eb8dd30c38a9bbd8d75ba0772f13dd48f9cf`

The repair changes the first-save implementation and describes absolute vault/project arguments to the assistant. It leaves standalone research and router instructions unchanged. The native captures are in `/tmp/obsidian-project-acceptance-r5/`. Its `run.py` drives Codex sessions in separate disposable vaults and checks file names and SHA-256 digests before and after confirmation, refusal, update, and replay.

- Setup: Matched 94 tracked skill and Codex manifest files against the isolated installed 4.2.0 cache, with zero differences. The R3 focused pytest selection was re-run against the repaired code and returned `10 passed in 0.56s`.
- 1, 3, 6: re-tested — `project.first.jsonl` shows that the assistant read the installed skill and checked paths, then asked for a separate reply before research. The vault snapshot stayed empty apart from its original directories. After consent `project.response.jsonl` ran the installed create helper. Exactly three files appeared: the entry, R01, and the original notice. The first conclusion was 30 scheduled days, seven per full week, with the dated report and evidence linked and the actual count and December left open.
- 2, 9: update re-tested — the fresh conversation used only file location checks before asking for later consent. During the approved turn the helper rejected a first plan using R02 as the prior round. The assistant corrected the plan and saved R02, archived the correction, and updated the index. The new conclusion is 25 scheduled days and six per full week, with R01 and the original evidence preserved byte-for-byte. See `project.update.jsonl` and `project.update-approved.jsonl`.
- 4, 15: re-tested — `deep-note.first.jsonl` assigned the same natural deep-note request to standalone research. It returned a link to exactly one Markdown note under the chosen vault's research directory.
- 5: re-tested — `decline.first.jsonl` inferred an ongoing tracking need, proposed a path in the selected vault, and asked for approval. The commands loaded only the skill and checked paths. `decline.response.jsonl` accepted the refusal and the vault remained unchanged.
- 8: re-tested for a legacy-only folder — `existing.first.jsonl` found its private note and offered another location, with no vault changes. The completed-project choice from R4 carries over because the patch does not affect the proposal decision or target inspection.
- 10: re-tested — `incomplete.first.jsonl` proposed an update and waited. The consent turn diagnosed a missing R01 and stopped without evidence comparison or vault changes.
- 11, 12: storage re-tested — the focused interruption and concurrent edit tests passed using the repaired writer. They verify that failed publication preserves the pending state and original concurrent revision. The CLI late-target probe described under row 12 was also repeated against this revision: diagnostic `project destination already exists`, and the external note remained the only file with the same bytes. The exact interruption and collision dialogs remain unverified.
- 7, 13: native results carried over — the fix leaves pre-consent missing-target and path-containment instructions unchanged. The focused existing, symlink, traversal, and missing-evidence rejection cases passed against this revision.
- 2, 14: replay re-tested — the fresh replay first loaded the skill and listed paths, then requested separate consent. After approval, it confirmed the archive matched the correction and retained the 25-day conclusion without creating or changing notes. The harness exited 0, with all five case groups passing and identical pre/post replay path and SHA-256 snapshots. See `project.replay.jsonl` and `project.replay-approved.jsonl`.

## Re-run on 2026-11-19, at `14cccd367a8ec0e02c3512eefbc8199c9bf0ee4a`

The revised first save builds and verifies its files in an isolated staging directory, then publishes the completed project without replacing a destination. This run uses native captures in `/tmp/obsidian-project-acceptance-r6/`. The installed Codex cache matches 94 tracked runtime paths from this commit byte-for-byte.

- 1, 3, 6: re-tested — the explicit start proposed the child vault, topic, scope and outputs. It waited for a separate reply. After consent, `project.response.jsonl` used the installed helper and created exactly the index, completed R01 and archived original in the selected vault, with no staging directory left. The initial source supported 30 scheduled days, seven per full week. The entry/report retained the research question, evidence and unresolved actual-operation and later-schedule questions.
- 4, 15: re-tested — the natural deep request loaded the standalone research and Markdown skills, found the selected child vault, and saved and linked exactly one note under its research directory. It cited the original notice and differentiated scheduled from actual openings. The tool trace also shows the model examined the other local fixture while gathering context. See `deep-note.first.jsonl`.
- 2, 9, 14: native re-tested — fresh update and replay turns each asked for separate consent before reading evidence. The update saved R02 and the correction archive and updated the index from 30 to 25 scheduled days, or seven to six per full week. Independent inspection verified all nine saved links resolve, the original and correction archives match supplied bytes, and R01 is unchanged. Replay left path and SHA-256 snapshots identical. The harness exited 0 with all five standard-path groups passing. Mid-round additional input remains untested. See `project.update*.jsonl` and `project.replay*.jsonl`.
- 5, 8, 10: re-tested — the implicit proposal selected the child vault and waited; the refusal yielded no vault changes. The legacy-only collision offered another path. After consent, the incomplete-project reply identified the missing R01 and stopped without modifying the vault. The complete-existing-project choice from R4 carries over because the existing-target proposal rules are unchanged. See `decline.*.jsonl`, `existing.first.jsonl` and `incomplete.*.jsonl`.
- 11, 12: storage re-tested — the exact-revision focused tests returned `10 passed in 0.59s`; the new `test_create_preserves_directory_that_appears_before_publication` separately returned `1 passed in 0.17s`. That test adds an empty destination immediately before publication and checks its original directory identity and empty contents. The staged note and pending marker remain available for inspection. The interruption test stops before the entry write and checks that the intended project is absent and the preserved staging folder is recognized as incomplete. Native dialogs for those precise faults remain unverified.
- 7, 13: R4 native evidence carries over for missing-target and unsafe-path proposals because the pre-consent target selection is unchanged. The exact-revision focused symlink and traversal rejection cases passed.
- The closing station recorded `103 passed` for the package suite and `1 passed` for the promoted integrity probe at this exact revision. Filesystem behavior was exercised on macOS; the Linux publication path was not locally tested.
- Compatibility failure outside the standard-path harness: an existing complete project at `research/.research-first-round-library`, with an entry linked to R01 and no pending marker, was readable under the R4 helper (`inspect --read index.md --read R01.md`, exit 0). The exact same command and test data under R6 returned exit 1 with `incomplete first round staging; preserved for inspection`. Both original note files retained their bytes. The prefix filter in `require_project_location` rejects a valid legacy path based solely on its spelling.

## Re-run on 2026-11-19, at `cc32114dac027a55e4a18d3741d59d8489599280`

The confirmed scope now covers continuation of projects created by this version and preservation of existing folders. Compatibility and migration for folders from the previous resume skill are outside scope. The original R6 observation above is retained.

The isolated host used the plugin installed from `33b856b` before syncing trunk. `git diff --exit-code 33b856b..HEAD -- obsidian` returned 0 with no output. An independent comparison of the 94 tracked skill and Codex manifest paths at `cc32114` against the same installed cache found no differences. Native captures and the path/SHA-256 comparison harness are under `/tmp/obsidian-project-acceptance-r7/`.

- 1, 3, 6: re-tested — before approval, the explicit start used read-only path checks. After approval, the assistant saved the index, R01, and the archived original in the selected vault. The hidden project identity marker contained exactly `obsidian-research-project-v1\n`. The first report documents 30 scheduled days, seven per full week, the original evidence, and unresolved actual operation.
- 4, 15: re-tested — the deep one-off prompt loaded the standalone skill and saved one note under the selected vault, with no project folder or history.
- 5: re-tested — the implicit project prompt received a proposal and separate approval request. The assistant checked paths, and a subsequent refusal left the vault snapshot identical.
- 7, 13: carried over the R4 native missing-topic and unsafe-target proposals. Their pre-consent selection rules are unchanged; current helper tests rechecked path rejection.
- 8: re-tested with a legacy folder containing a complete index and R01. With the creation marker absent, the assistant offered a new location without opening the notes or changing any vault paths or bytes. A separate copy of the completed new-version project also entered the same-name flow. The assistant checked the identity marker and paths only, then offered to create at a separate location or resume the existing project and waited. Recursive diff of the copied vault against the original found no changes. See `existing.first.jsonl` and `complete-collision.first.jsonl`.
- 9: fresh update re-tested — the pre-consent turn checked only location and identity metadata. The confirmed turn archived the new notice and corrected 30 to 25 scheduled days, leaving the first report and original notice byte-identical. Mid-round extra input remains untested.
- 2, 14: replay re-tested — the follow-up in a new session first requested separate consent. The approved turn matched the correction to the archived notice and retained the 25-day conclusion. The harness compared pre/post replay names and digests, including the creation marker, and all were identical. See `project.replay*.jsonl`. The harness exited 0 with all six groups passing their path and digest assertions.
- 10: re-tested a folder with an index pointing to a missing report and no version marker. Both the request and later confirmation left it unchanged, and the assistant described the missing material. A marked project with a missing report was not independently exercised in native chat.
- 11, 12: storage re-tested on macOS. The interruption test preserved the unpublished partial save. The collision test retained the destination that appeared just before publication. The exact native interruption and collision dialogs are unverified, as is Linux publication.
- 16: re-tested unsupported-folder update separately. The folder had a complete legacy index and R01, but no version marker. The assistant listed paths without reaching the transaction helper or opening evidence, declined the update, and all paths and file bytes remained identical. The assistant suggested a standalone note instead of offering the specified choices to select a supported project or start one elsewhere. See `legacy-update.first.jsonl`. Scoped regression tests also checked that `inspect` and `apply` reject a legacy folder with a valid prior recovery record without modifying or recovering it.
- Mechanical checks: `13 passed in 0.84s` in scoped local tests at `cc32114`. The closing station recorded `183 passed` for the full `obsidian/tests obsidian-finance/tests` suite at `cc32114`, and `1 passed` for the promoted integrity probe at the byte-identical pre-sync plugin revision.
