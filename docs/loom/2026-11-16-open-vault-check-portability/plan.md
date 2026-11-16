# Portable open-vault check — plan
intent: 2026-11-16-open-vault-check-portability@b6bce62
charter: 1.1

## Current State Evidence
- Forward: `obsidian/skills/obsidian-knowledge/scripts/vault.sh:155` — `do_search` reads the open vault only when `command -v plutil` succeeds; otherwise `open_vault` stays empty.
- Reverse: `vault.sh:115` — `do_locate` already picks between `plutil_vaults` and `python_registry_vaults`; the portable registry reader lives at `vault.sh:63`.
- Error: `vault.sh:163` — the CLI branch needs `open_vault` to equal the requested vault; an empty value sends every search to grep. CI run 43803700885: 3 failed / 70 passed.
- Data: `vault.sh:31` `plutil_raw` reads one key losslessly (exit 2 absent, exit 1 line-spanning); `vault.sh:158` still reads `open` through a lossy `$( )`.
- Boundary: `obsidian/tests/test_vault_search.py:204` pins the line-spanning registry path falling back to grep; the CLI tests at `:85`, `:188`, `:262` fail without plutil.

## Task DAG
Wave 1 — the fix; nothing else consumes it.

**W1-01 Portable open-vault read in `vault.sh`**  after: none  acceptance: 1, 2, 3
- Files: obsidian/skills/obsidian-knowledge/scripts/vault.sh
- Test: A1 positive: cli_branch_reachable_without_plutil; negative: closed_vault_falls_back_to_grep. A2 positive: cli_branch_accepts_relative_output; boundary: open_vault_registry_newline_falls_back_to_grep. A3 positive: search_and_locate_leave_vault_unchanged; boundary: grep_skips_hidden_directories.
- Risk: preserves `obsidian/tests/test_vault_search.py` coverage unchanged — no case added, dropped or weakened; the `open` read moves to `plutil_raw`. Python branch stays best-effort, unverified. agent-decided.

Wave 2 — delivery evidence (A4 is observable only after ship).

**W2-01 Publication evidence record**  after: W1-01  acceptance: 4
- Files: docs/loom/2026-11-16-open-vault-check-portability/publication-evidence.md
- Test: docs only — exempt; records the CI run URL, the new PR number and the PR #5 supersede note.
- Risk: written after ship observes the required check; the note states PR #5's content carried forward file-by-file. agent-decided.

## Simplicity check
- W2-01 reproduction transcript — declined: the CI run itself is the no-plutil evidence; a local transcript adds no Acceptance coverage.

## Questions asked
① — consequence — 「紅燈的 PR #5 要怎麼處理？」選項 A 新變更承接全部內容＋修復、另開 PR、PR #5 關閉註明被取代；B 直接關閉不修；C 其他。你選「A 新變更修好再 land（建議）」。
① — what — 「這樣理解對嗎？」intent 的問題陳述與四條驗收條件；你回「開始做吧」。

## Risks
1. user-decided — 你原話「A 新變更修好再 land（建議）」：新變更承接 PR #5 全部內容再加修復，PR #5 關閉並註明被取代，不以紅燈合併。
2. Without plutil the registry is read by python3; where python3 is also absent the CLI branch stays unreachable and the existing grep fallback answers — no wider behaviour change.
3. A4's green CI and the PR #5 closure are observable only after ship; this change delivers the locally reproducible ubuntu condition, not a live-Linux claim.
4. The diff touches only `do_search`'s open read; engine choice, accept gate and hit set stay as reviewed, and macOS keeps the plutil path verbatim.
