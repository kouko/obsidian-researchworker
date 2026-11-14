# Extract Obsidian plugin — acceptance test evidence

Tried on 2026-11-14, in a clean copy of the project at f9ffeff.

Exact tested HEAD: `f9ffeff2e859a3d9ed9af624f752788f8ad83ca3`.
Fresh clone: `/private/tmp/researchworker-review-3swgw120/acceptance-final`.
Executed `git clone /private/tmp/researchworker-review-3swgw120/repo /private/tmp/researchworker-review-3swgw120/acceptance-final`, exit 0; `git rev-parse HEAD` returned the exact HEAD above. Read agent/template, confirmed intent, spec, plan, root/plugin documentation, provenance, migration, verification, roadmap and archive research before writing.

This is final-content verification, not a failed-test retry. Preliminary Round 2 report/evidence at `/private/tmp/researchworker-review-3swgw120/acceptance-round2/docs/loom/2026-11-14-extract-obsidian-plugin/` describe 700652a and are historical only. Current `git diff 700652a..HEAD` restores exactly one intent Out-of-scope line to its original “合併任何 PR。”; later conditional merge authorization remains separately in plan Risks. An executed inline Python assertion checked `git diff --name-only 700652a..HEAD` equals only that intent path. All other tracked content is byte unchanged.

No network, credential, model, real vault, original Monkey working tree, installed plugin or other-vendor access occurred. The pinned source Git snapshot was read-only. No permanent tests/scripts/infrastructure or source-build edits; no commit. No important finding was dismissed.

## 1. Independent source, history, licenses, documentation and traceability

### test_documentation_repaired_claims_consistent

Read all three plugin READMEs in full, root README, file-intel SKILL, attribution, provenance, migration and history research. All translations replace old marketplace installation instructions with honest independent-install status and verification/transition links. Root and plugin READMEs identify isolated installation as historical and real skill/note use as unmet. All three README dependency paragraphs and SKILL Step 2 disclose the missing external Gemini vault script and unavailable acquisition/setup. File processing is unavailable without it. All three trees omit nonexistent commands and unsupported standalone /obsidian example; version is 3.27.0. Attribution labels unrelated inventory as upstream historical context and retains transferred license notices.

Executed inline Python stdlib probe with pathlib/re: parsed Markdown link targets in root README, ATTRIBUTION, provenance, three plugin READMEs, file-intel SKILL, Mermaid compatibility and history research; skipped schemes and anchor-only targets, resolved file targets relative to documents and asserted each exists. Asserted old marketplace command, standalone /obsidian line, commands/ tree and 3.25.0 absent in all three READMEs. Exit 0:
```text
9 documentation surfaces: 80 local file links resolve; stale install, command and version absent
```
This checks local file targets, not network links or heading anchors.

### test_history_archive_mapped_commits_reachable

The same executed inline Python probe loaded docs/provenance-commits.json, asserted 131 mappings and each imported value within `git rev-list 3c95872cb266a54af38f5a43485da4b9aa0c06fd`. For each pair it compared exact bytes from `git show -s --format=%an%x00%ae%x00%aI%x00%cn%x00%ce%x00%cI%x00%B <commit>` between this clone and read-only `/private/tmp/obsidian-researchworker-monkey-source`. Exit 0:
```text
131 mapped metadata pairs match; all 131 reachable from imported tip; remote not queried
Only confirmed-intent record changed from 700652a; all other tracked content byte unchanged
```
Remote archive creation/existence is the parent's recorded observation in research, not this agent's remote reading. Read provenance/research: archive is at imported tip; squash does not make imported commits main ancestors; preserve archive until verified replacement. Original discovery/scoped-tree/ancestry audit, 67 removed signatures and semantic-history limitations remain disclosed. Historical original tester's source inventory was 161 blobs, 153 identical, eight deviations and zero missing; no new exhaustive blob/discovery audit claimed.

### test_existing_checks_repaired_docs_pass

From obsidian/ executed:
```sh
PYTHONDONTWRITEBYTECODE=1 /Users/kouko/.conda/envs/dbt-redshift/bin/python3 -m pytest -q -p no:cacheprovider scripts/test_verify_drift.py tests/test_canvas_plugin_docs.py
```
Exit 0: `6 passed in 0.34s`.
From root executed `python3 obsidian/scripts/verify-drift.py`, exit 0:
`OK: all 4 functional copies match canonical + SSOT header.`
Executed `git diff --check`, no output.
Setup follows README's existing Python/pytest checks using an already available environment; no package installation. The final setup limitation is recorded in row 2 instead of inventing successful real-host use.

Full package suite deliberately not run by this acceptance tester. Expected automatic blocking check from obsidian/:
`PYTHONDONTWRITEBYTECODE=1 /Users/kouko/.conda/envs/dbt-redshift/bin/python3 -m pytest -q -p no:cacheprovider`.
Finalization executes the suite and blocks on failure; this is a check description, not a future pass claim. Parent reports historical 152 passed and six abuse probes at 700652a; no new final-HEAD full-suite execution claimed here. Honest partly/unmet coverage can be recorded without turning row 2 into works; this report neither forbids nor promises finalization or merge.

## 2. Installation and basic use

Carried over after exact-delta check: no runtime behavior or runtime evidence changed. Verdict partly; criterion remains unmet. Read docs/verification.md: historical isolated Codex 0.169.0 local-source installation succeeded at 5df7f6ce3c34098ca9c45590ce943967a199409b. Real model/skill execution and representative note creation did not succeed; DNS and authentication unavailable, fixture had no note. Other hosts/remote installation unverified. This run does not retry installation, credentials, network or model invocation. The amended plan records “幫我修正文件 通過測試沒問題後合併” as conditional baseline merge authorization, not AC2 waiver. Closure requires isolated successful real-host skill/model execution and note creation with revision/host/output evidence.

## 3. Roadmap

Re-tested by reading ROADMAP.md in full: baseline then wiki retirement/reconsideration, YTSS/RLSS integration, resumable multi-note research; every stage has Exit/Open criteria, proposed status and no future-implementation authority. Exact-delta check also confirms unchanged from 700652a. No new feature behavior claimed.

## 4. Existing data and transition

Re-tested every delivered entry: root README, all three plugin README installation/independent-distribution paragraphs and full docs/migration.md. They link the transition guide, preserve existing install until isolated replacement works, warn against shared-namespace duplicate registration, require separately authorized host-specific switch, retain old settings and restore registration for rollback without deleting vault data. Existing wiki retained. No actual switch or rollback exercise claimed. Writes confined to new temporary clone/report; no existing user data or original Monkey working checkout accessed. No changes to runtime/transition guide across final delta.

## Final-content run on 2026-11-14, at f9ffeff

- 1: re-tested — current docs, 80 local links, 131 history mappings/reachability, six retained tests and drift; passed within disclosed bounds.
- 2: carried over — final delta only restores immutable original authorization line and creates no runtime evidence.
- 3: re-tested — full roadmap read; stages/Exit/Open and proposed status present.
- 4: re-tested — all transition entry surfaces and full guide walked; no existing-data operations.
