# Four-host plugin support — plan
intent: 2026-11-25-four-host-plugin-support@74b5c0f
spec: docs/loom/2026-11-25-four-host-plugin-support/spec.md@e2218e6
charter: 1.1

## Task DAG

### Wave 1

**W1-01 Register native OpenCode skills in both independent packages** after: none acceptance: 2, 3
- Files: obsidian/.opencode-plugin/, obsidian-finance/.opencode-plugin/, obsidian-finance/package.json, obsidian/tests/test_opencode_loader.py, obsidian/tests/test_command_registration_failure.py
- Test: A2 positive: both-inventories; boundary: standalone-package. A3 positive: skill-registration-content; negative: no-command-transform.
- Risk: REQ-2–3; agent-decided preserve existing loader parsing and registration failure isolation; update existing command-specific tests to cover native-only registration.

### Wave 2

**W2-01 Align releases and document installation** after: W1-01 acceptance: 1, 4
- Files: .claude-plugin/marketplace.json, obsidian/.claude-plugin/, obsidian/.codex-plugin/, obsidian/package.json, obsidian-finance/.claude-plugin/, obsidian-finance/.codex-plugin/, obsidian/tests/test_vault_search.py, README.md
- Test: A1 positive: version-and-inventory; negative: retired-skill. A4 positive: package-suite; boundary: no-vault-changes.
- Risk: REQ-1,4; agent-decided align versions and retain existing inventory tests; update historical version assertion for current metadata.

**W2-02 Verify host installation and consolidate guides** after: W2-01 acceptance: 2, 4
- Files: obsidian/README*.md, obsidian-finance/README.md, docs/migration.md, docs/loom/2026-11-25-four-host-plugin-support/evidence/
- Test: A2 positive: eight-install-inventories; boundary: isolated-config. A4 positive: documented-routes; boundary: unsupported-or-unverified-disclosed.
- Risk: REQ-2,4; agent-decided use disposable host configurations, document actual verified behavior and keep existing global settings.

## Simplicity check
- Remove custom slash handler and retain native registration — taken
- Use existing Claude conversion rather than additional Antigravity metadata if verified — taken

## Questions asked
① — what — 確認這個範圍後，我會繼續設計與實作。
② — behaviour — 請確認新版行為符合預期。

## Risks
1. Isolated host installs must preserve supporting scripts and references; native mention and automatic selection require runtime evidence.
2. Existing OpenCode generated command invocations are retired; preserve namespaced skill IDs.
