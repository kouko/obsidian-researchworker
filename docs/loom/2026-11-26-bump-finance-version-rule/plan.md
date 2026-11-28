# Bump obsidian-finance to 0.2.1 and add version-bump rule — plan
intent: 2026-11-26-bump-finance-version-rule@0e7cc67
charter: 1.1

## Current State Evidence
- Forward: `obsidian-finance/.claude-plugin/plugin.json:3` reads 0.2.0 although #42 changed shipped skill text.
- Reverse: `.claude-plugin/marketplace.json:12`, `obsidian-finance/.codex-plugin/plugin.json:3`, `obsidian-finance/package.json:3` also read 0.2.0.
- Error: `/plugin` update reports "already at the latest version (0.2.0)"; installed cache stays at 4d6d53d.
- Data: prose mentions 0.2.0 at `README.md:4`, `README.md:55`, `docs/migration.md:4`, `obsidian-finance/README.md:3`.
- Boundary: `obsidian/tests/test_opencode_loader.py:78` checks names across the four metadata files but not versions.

## Task DAG

**W1-01 Bump finance version and pin metadata version sync**  after: none  acceptance: 1, 3
- Files: obsidian-finance/.claude-plugin/plugin.json, obsidian-finance/.codex-plugin/plugin.json, obsidian-finance/package.json, .claude-plugin/marketplace.json, obsidian-finance/README.md, README.md, docs/migration.md, obsidian/tests/test_opencode_loader.py
- Test: A1 positive: test_package_identity_keeps_repository_and_other_hosts; negative: test_package_identity_keeps_repository_and_other_hosts. A3 positive: full package suite; negative: full package suite.
- Risk: agent-decided — widens test_opencode_loader.py identity test with version equality; obsidian stays 5.0.0.

**W1-02 Add version-bump rule to AGENTS.md**  after: W1-01  acceptance: 2
- Files: AGENTS.md
- Test: A2 positive: agents_md_rule6_present (reviewer read-back); boundary: agents_md_rules_1_to_5_unchanged (git diff).
- Risk: agent-decided — appends rule 6; existing rules unchanged.

## Simplicity check
- Separate version-sync script or CI job — declined: out of scope; one extra assertion in the existing identity test suffices.

## Questions asked
① — consequence — 確認修改目標（finance 升到 0.2.1、AGENTS.md 加升版規則、驗收、範圍）並授權通過審查後自動開 PR、合併另由使用者決定

## Risks
1. The rule relies on agents following AGENTS.md; no enforcement (out of scope per intent).
