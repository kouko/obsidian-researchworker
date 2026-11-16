# Search the local Obsidian vault from other projects — plan
intent: 2026-11-15-search-vault-from-other-projects@2d77d90
spec: docs/loom/2026-11-15-search-vault-from-other-projects/spec.md@bb2161f
charter: 1.1

## Task DAG

Wave 1 — locator first; hook and skill consume it.

**W1-01 Vault locator script**  after: none  acceptance: 1, 3
- Files: obsidian/skills/obsidian-vault-search/scripts/find_vaults.py, `obsidian/tests/test_vault_search.py`
- Test: A1 positive: registry_lists_existing_vault; negative: missing_registry_prints_nothing. A3 positive: env_override_replaces_registry; boundary: registry_entry_with_deleted_path_skipped.
- Risk: stdlib only; macOS + Linux registry paths, Windows unsupported; OBSIDIAN_VAULT replaces registry (spec Design decision, REQ-1, REQ-3). agent-decided.

**W1-02 SessionStart pointer hook (boundary test)**  after: W1-01  acceptance: 2
- Files: obsidian/hooks/hooks.json, obsidian/hooks/vault_pointer.py, `obsidian/tests/test_vault_search.py`
- Test: A2 positive: hook_emits_one_line_with_vault_paths; negative: hook_silent_and_exit0_without_vault.
- Risk: plugin hook output reaches every session; keep one line, never error (spec Review fixes, REQ-2). Verified host: Claude Code only. agent-decided.

**W1-03 obsidian-vault-search skill**  after: W1-01  acceptance: 4, 5, 6, 9, 10
- Files: obsidian/skills/obsidian-vault-search/SKILL.md, `obsidian/tests/test_vault_search.py`
- Test: A4 positive: skill_declares_read_only; negative: skill_has_no_write_tools. A5 positive: skill_marks_note_excerpt_block; boundary: skill_says_notes_never_instructions. A6 positive: skill_proposes_rule_with_consent; negative: skill_forbids_additional_directories. A9 positive: skill_has_subagent_paragraph; boundary: paragraph_labels_note_vs_web. A10 positive: skill_states_3_notes_30kb_threshold; boundary: skill_caps_subagent_at_10.
- Risk: behaviour is instruction text, so static tests check contract wording; live behaviour proven in acceptance testing (REQ-4..6, 9, 10). agent-decided.

**W1-04 Plugin wiring and docs**  after: W1-02, W1-03  acceptance: 3, 8
- Files: obsidian/tests/test_skill_inventory.py, obsidian/skills/using-obsidian/SKILL.md, obsidian/.claude-plugin/plugin.json, obsidian/README.md, obsidian/README.ja.md, obsidian/README.zh-TW.md, obsidian/CHANGELOG.md, .claude-plugin/marketplace.json
- Test: A8 positive: inventory_includes_vault_search; negative: routing_table_lists_vault_search. A3 positive: shipped_files_have_no_personal_vault_path; boundary: shipped_files_have_no_user_folder_names.
- Risk: existing test `obsidian/tests/test_skill_inventory.py` RETAINED set widened by one skill; coverage preserved. Version 4.1.0. agent-decided.

Wave 2 — evidence.

**W2-01 Retrieval check on real questions**  after: W1-03  acceptance: 7
- Files: docs/loom/2026-11-15-search-vault-from-other-projects/retrieval-check.md
- Test: docs only — exempt from Test pairs.
- Risk: run read-only against the user's vault from a non-vault cwd; record found/not-found per question, no note bodies copied. agent-decided.

**W2-02 Graduate hostile-registry probe**  after: W1-01  acceptance: 3
- Files: `obsidian/tests/test_find_vaults_hostile_registry.py`, docs/loom/2026-11-15-search-vault-from-other-projects/evidence/probes/test_find_vaults_hostile_registry.py
- Test: A3 positive: test_find_vaults_newline_in_path_never_splits_line; boundary: test_find_vaults_relative_registry_path_not_reported.
- Risk: probe caught two defects (fixed f0de4a6); move unchanged into package suite per review.probe-graduation. agent-decided.

Wave 3 — Python-free search fix-round (2026-11-15, after A6 FAIL: host CC 2.1.325 has no Grep/Glob tools; user-decided CLI-primary + macOS built-ins over Python).

**W3-01 Bundled sh script `scripts/vault.sh`**  after: none  acceptance: 1, 3, 6
- Files: obsidian/skills/obsidian-knowledge/scripts/vault.sh (locate + search), `obsidian/tests/test_vault_search.py` locator/search sections rewritten against vault.sh, `obsidian/tests/test_find_vaults_hostile_registry.py` ported from find_vaults.py to vault.sh locate (find_vaults.py is deleted later, in the skill-dir rename).
- Test: A1 locate via OBSIDIAN_VAULT override; negative: no vault → empty. A3 boundary: relative/control-char paths rejected (hostile probes ported). A6: script has no write verbs.
- Risk: macOS registry read via plutil is untested on other registries; keep output contract one path per line, exit 0. agent-decided.

**W3-02 Hook rewrite to `vault_pointer.sh`**  after: W3-01  acceptance: 2
- Files: obsidian/hooks/hooks.json, obsidian/hooks/vault_pointer.sh (python removed), tests.
- Test: A2 positive: hook_emits_one_line_with_vault_paths; negative: hook_silent_and_exit0_without_vault.
- Risk: hook runs every session; silent failure, exit 0, no python dependency. agent-decided.

**W3-03 Skill rewrite to `obsidian-knowledge`**  after: W3-01  acceptance: 4, 5, 9, 10, 8
- Files: obsidian/skills/obsidian-knowledge/SKILL.md (renamed; Step 2 calls `vault.sh search`; no Grep/Glob mentions; subagent paragraph updated), obsidian/tests/test_skill_inventory.py (RETAINED entry renamed — the rename itself breaks that set, so it must land in this commit, not a later one), tests.
- Test: A4/A5/A9/A10 wording assertions updated for the new name and search step. A8 positive: inventory RETAINED lists `obsidian-knowledge`.
- Risk: instruction-text contract; static wording tests + live acceptance testing. agent-decided.

**W3-04 Wiring: docs + version**  after: W3-02, W3-03  acceptance: 8
- Files: obsidian/skills/using-obsidian/SKILL.md, obsidian/.claude-plugin/plugin.json, obsidian/README*.md, obsidian/CHANGELOG.md, .claude-plugin/marketplace.json.
- Test: A8 routing name `obsidian-knowledge`; version 4.2.0; no personal vault path in shipped files.
- Risk: rename misses a doc → stale routing; sweep all shipped text for the old name. agent-decided.

## Simplicity check
- Skill only, no hook — declined: skill descriptions are dropped from the listing on the user's machine (spec Alternatives).
- Locator logic inline in skill text instead of script — declined: hook needs the same logic; one script avoids two copies.
- Two locators (sh for macOS, Python for Linux) — declined: one POSIX `sh` file with a platform branch (`plutil` on macOS, `python3` best-effort on Linux) keeps a single source.
- Paste-ready subagent prompt in the skill instead of a new agents file — taken
- Merge W1-02 into W1-01 — declined: mixes hook boundary risk into locator commit (plan reviewer note).

## Questions asked
① — what — 預設允許查詢哪些資料夾？
① — what — 為什麼現在做？這次會讓哪項原本要做的工作延後？
① — what — 要加這條驗收（A）嗎？（子 agent 研究時同時查網路與筆記庫）
② — behaviour — 這樣對嗎？（你下 ___ 會看到 ___ 行為表）
② — what — 筆記多時是直接讀筆記原文？還是派 subagent？（A/B/C/D）
② — what — 回傳路徑要哪一種？（相對／完整／obsidian://）
② — behaviour — 審查修正後的行為，這樣可以嗎？

## Risks
1. Hook runs in every session of every project; failure must be silent. Risk: description; boundary test W1-02 covers no-vault path.
2. Note text sent to the model provider; accepted by user at ① (intent Constraints, spec Design decision).
3. Global settings write only on explicit yes; never automated by code in this change.
4. Linux unverified, Windows unsupported; README must say so (PRINCIPLES #3).
- user-decided — second-vendor selection-confirmed: codex (direct request 「可以用 codex 做一次獨立 review 嗎」, target: change 2026-11-15-search-vault-from-other-projects, PR #5).
