# Open-vault check portability — acceptance test evidence

Tried on 2026-11-16, in a clean copy of the project at 13b5a5c (13b5a5cb9a65fbed13ffc1cc1e59981d31a37381).

Setup: the clean copy was produced with `git archive --format=tar HEAD | tar -x` into a fresh
directory under /tmp, so nothing from the change worktree or any stale artefact was present. The
project README says to run `cd obsidian && python3 -m pytest -q -p no:cacheprovider`; the intent's
reuse command is `python3 -m pytest obsidian/tests -q -p no:cacheprovider`, run from the repository
root, which collects the same suite. Every command below was run in that clean copy unless it says
otherwise. No fixture read or wrote the user's real vault, real Obsidian config, or running app.

## 1. 在無 plutil 的環境（CI 的 ubuntu 條件）重跑 `python3 -m pytest obsidian/tests -q -p no:cacheprovider`：73 項全數通過，三個 CLI 分支測試不再失敗。

- How I tried it: built a shadow directory of symlinks to every file in /usr/bin except `plutil`,
  then set PATH to the real PATH with only the /usr/bin entry swapped for that shadow dir (keeps
  node and the conda python3 the minimal PATH was dropping). Confirmed inside that environment that
  `plutil` is genuinely absent while python3/node/grep remain. Ran the full suite there.
- What came back:
  - `plutil -> (not found)`; `python3 -> /Users/kouko/.conda/envs/dbt-redshift/bin/python3`;
    `node -> /opt/homebrew/bin/node`; `grep/sh/sort/awk` all resolved.
  - Full suite: `75 passed in 4.55s`, exit 0.
  - The three CLI-branch tests alone (`-k 'leave_vault_unchanged or relative_output or
    encodes_each_word_as_quoted_phrase'`): `3 passed, 40 deselected`, exit 0, under the same
    plutil-free PATH.
- Evidence: `/tmp/final_a1_run.py` (the runner); output captured above. Note on count: the intent
  says 73; the suite now holds 75 because this change adds two tests of its own. All 75 pass; the
  three CLI-branch tests named in the intent are among them and no longer fail.

## 2. macOS 行為不變：有 plutil 時同一套件 73 項通過；registry 標記 open 時 CLI 分支照舊被採用，app 關閉或 vault 不符時照舊走 grep 後備。

- How I tried it: (a) ran the same full suite in the clean copy under the normal PATH (plutil
  present); (b) functional routing probes against temporary fixtures under /tmp — a fake vault with
  two notes, a fake Obsidian CLI that prints relative paths, and a throwaway registry JSON — with
  HOME/OBSIDIAN_CONFIG_DIR pointed at the temp config and OBSIDIAN_CLI_BIN at the fake CLI.
- What came back:
  - (a) Full suite under normal PATH: `75 passed in 4.51s`, exit 0.
  - (b) Probe a — registry `open: true` + fake CLI printing relative paths: output
    `['.../vault/sub/beta.md', '.../vault/alpha.md']`, exit 0 — the CLI branch was taken (the fake
    CLI's output came back, vault-prefixed).
  - Probe b — registry with no `open` entry + fake CLI that touches a marker file and prints
    `should-not-run`: output `['.../vault/alpha.md']` (grep's answer), exit 0, and the marker file
    was never created — the CLI was not invoked.
  - Probe c — registry `open: true` but `path` value ending in `\n`: output
    `['.../vault/alpha.md']` (grep's answer), exit 0, and the fake CLI's args-file was never
    created — the CLI branch was not taken.
- Evidence: `/tmp/a2_probes.py` (the probe script) and its verbatim output above; the three probes
  assert the hit set and CLI invocation, and the script prints `ALL A2 FUNCTIONAL PROBES PASSED`.

## 3. 修復範圍最小且可稽：只改 `vault.sh` 的 open 判定（含 reviewer-b 指出的同一行 lossy `$( )` 讀取）與對應測試；PR #5 其餘已審查功能內容逐檔不變。

- How I tried it: `git diff 2a689ad..HEAD --stat` in the change worktree (2a689ad is the tip of PR
  #5's branch, the merge base); then extracted each named function's body from both revisions with
  `git show <rev>:path` and compared byte-for-byte; then confirmed the diff inside vault.sh is
  exactly the open-vault read block plus the new helper.
- What came back:
  - `git diff 2a689ad..HEAD --stat` shows 4 files: the two loom docs (plan, intent) and exactly two
    code files — `obsidian/skills/obsidian-knowledge/scripts/vault.sh` (35 lines changed) and
    `obsidian/tests/test_vault_search.py` (89 lines added).
  - The vault.sh diff has exactly two hunks: (1) a new helper
    `python_registry_open_vault` (a best-effort python3 read of the registry's `open` vault);
    (2) the open-vault read block in `do_search` changed from a single plutil-gated loop to a
    plutil/python3 branch — the plutil path is byte-identical to the old loop, and the `$( )`
    lossy capture of `vaults.$id.open` is replaced by `plutil_raw` inside the plutil branch.
  - Byte-identical across the diff: `plutil_raw`, `plutil_vaults`, `python_registry_vaults`,
    `emit_vault`, `do_locate`, and `do_search`'s query construction and accept gate
    (`open_vault == vault`) tail. `python_registry_open_vault` is new (absent in 2a689ad).
  - `git diff d87f7d5..HEAD` (PR #5's base..tip) confirms PR #5's feature content is carried
    unchanged; `2a689ad..HEAD` adds no file PR #5 did not already have.
- Evidence: the two `git diff` outputs above; `/tmp/verify_funcs.py` (the byte-identity checker)
  and its output `IDENTICAL` for each named function.

## 4. 新 PR 的 required CI 全綠；PR #5 關閉並留下被取代的說明；main 不出現紅燈。

- How I tried it: not testable on this machine. CI runs on GitHub's ubuntu runners; PR #5's close
  and main's status are repository events after publication. I did not run `gh` (forbidden) and
  did not claim any of it.
- What came back: nothing — no evidence exists yet.
- Evidence: none. What will be observed and where, when it is observable: the required `pytest`
  check on the new PR's runs page (all jobs green, no `3 failed / 70 passed` repeat); PR #5's page
  showing it closed with a comment noting it is superseded by the new PR; main's commits page / CI
  badge showing no red run between this change's merge and now.

## Re-run on 2026-11-16, at 13b5a5c

- First and only run; no re-run was needed. No step was skipped and no line was carried over.
