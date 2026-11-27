# Sync official Obsidian skills and add headless, knap — plan
intent: 2026-11-27-sync-official-obsidian-skills@8b8cbf9
charter: 1.1

## Current State Evidence
- Forward: `obsidian/skills/obsidian-cli/SKILL.md` "Vault targeting" says most-recently-focused vault; example uses nonexistent `silent` flag.
- Reverse: `obsidian/tests/test_skill_inventory.py` RETAINED set pins the 15 shipped skill names; adding skills must update it.
- Error: upstream `obsidian-cli/SKILL.md` "Before using the CLI" documents exit status 0 on failure; local copy lacks it.
- Data: upstream source obsidianmd/obsidian-skills commit 9c9560a (v1.2.3), cloned to session scratchpad `official/plugins/obsidian/skills/`.
- Boundary: `obsidian/skills/README.md` attribution table and `ATTRIBUTION.md` list per-skill upstream and LICENSE; counts appear in README, plugin.json files.

## Task DAG

### Wave 1

**W1-01 Merge upstream fixes into obsidian-cli**  after: none  acceptance: 1
- Files: obsidian/skills/obsidian-cli/SKILL.md, obsidian/tests/test_official_skill_sync.py
- Test: A1 positive: cli_has_upstream_cautions_and_vault_listing; negative: cli_has_no_silent_flag.
- Risk: agent-decided — take upstream text wholesale, keep repo's multiline description style; add repo-only `obsidian vaults verbose` and same-name-by-path rule in Vault targeting.

**W1-02 Merge upstream fixes into obsidian-bases**  after: none  acceptance: 2
- Files: obsidian/skills/obsidian-bases/SKILL.md, obsidian/tests/test_official_skill_sync.py
- Test: A2 positive: bases_has_kanban_and_note_prefix; boundary: bases_body_matches_upstream_except_frontmatter.
- Risk: agent-decided — repo had no bases extensions, so adopt upstream body verbatim; keep local frontmatter description only.

**W1-03 Merge upstream fixes into defuddle**  after: none  acceptance: 3
- Files: obsidian/skills/defuddle/SKILL.md, obsidian/tests/test_official_skill_sync.py
- Test: A3 positive: defuddle_has_untrusted_content_rule; negative: defuddle_keeps_youtube_and_version_floor.
- Risk: agent-decided — keep repo YouTube, 0.19.0 floor, quoted URLs; add upstream data-not-instructions rule and availability check wording.

**W1-04 Add obsidian-headless and knap skills**  after: none  acceptance: 4
- Files: obsidian/skills/obsidian-headless/, obsidian/skills/knap/, obsidian/tests/test_skill_inventory.py, obsidian/tests/test_official_skill_sync.py
- Test: A4 positive: new_skills_match_upstream_with_license; negative: shipped_skill_inventory.
- Risk: agent-decided — copy SKILL.md verbatim plus upstream LICENSE per skill, README.md guide matching sibling pattern.

### Wave 2

**W2-01 Update plugin metadata and docs**  after: W1-01, W1-02, W1-03, W1-04  acceptance: 5
- Files: obsidian/.claude-plugin/plugin.json, obsidian/.codex-plugin/plugin.json, obsidian/README*.md, obsidian/skills/README*.md, README.md, ATTRIBUTION.md, obsidian/skills/using-obsidian/SKILL.md, obsidian/CHANGELOG.md
- Test: A5 positive: package_tests_pass; boundary: skill_count_text_matches_inventory.
- Risk: agent-decided — skill count 15→17 everywhere; version bump 5.0.0→5.1.0 (new skills, minor); upstream credited as obsidianmd/obsidian-skills.

## Simplicity check
- One shared test file for all sync assertions instead of per-skill files — taken
- Skip version bump — declined: new skills change shipped inventory; repo bumps version per release.

## Questions asked
① — what — 照 A 做，headless 跟 knap 也一起加
① — what — obsidian-cli 是否加入 `obsidian vaults verbose` 找 vault 規則 → A
① — done — 需求確認是否正確（含自動開 PR 授權）→ 對

## Risks
1. Upstream text may conflict with repo cross-references (obsidian-knowledge pointer in cli README); keep README links intact.
2. user-decided — option A: merge upstream fixes, keep repo extensions, add headless and knap; add vault-listing rule to obsidian-cli.
