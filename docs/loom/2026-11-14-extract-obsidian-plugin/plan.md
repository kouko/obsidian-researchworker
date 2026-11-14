# Extract Obsidian plugin — plan
intent: 2026-11-14-extract-obsidian-plugin@5f9d4e7
spec: docs/loom/2026-11-14-extract-obsidian-plugin/spec.md@655b205
charter: 1.1

## Task DAG

**W1-01 Transfer independently usable plugin baseline** after: none  acceptance: 1,4
- Files: obsidian/, LICENSE, ATTRIBUTION.md, .github/workflows/test-obsidian.yml, tests/
- Test: A1 positive: source_tree_and_licenses; negative: missing_attribution_detected. A4 positive: upstream_unchanged; boundary: historic_tests_retained.
- Risk: REQ-1/REQ-4; agent-decided retain source tree and existing tests while replacing repository-coupled fixtures with equivalent evidence.

**W2-01 Publish independent installation metadata** after: W1-01  acceptance: 1,4
- Files: .claude-plugin/marketplace.json, obsidian/.claude-plugin/plugin.json, obsidian/.codex-plugin/plugin.json, obsidian/package.json, obsidian/.opencode-plugin/index.js, obsidian/README.md, tests/
- Test: A1 positive: independent_marketplace_resolves; negative: missing_plugin_detected. A4 positive: original_marketplace_unchanged; boundary: duplicate_install_documented.
- Risk: REQ-1/REQ-4; agent-decided keep plugin namespace pending host verification; never alter existing installations without a validated transition.

**W2-02 Deliver roadmap and transition documentation** after: W1-01  acceptance: 3,4
- Files: ROADMAP.md, README.md, docs/migration.md
- Test: A3 positive: roadmap_covers_all_tracks; negative: future_work_not_claimed_complete. A4 positive: existing_wiki_preserved; boundary: old_entry_retained.
- Risk: REQ-3/REQ-4; agent-decided defer wiki replacement, source-tool integration and long research to separately scoped changes.

**W3-01 Validate independent installation in a fixture** after: W2-01,W2-02  acceptance: 1,2,4
- Files: tests/, docs/verification.md
- Test: A1 positive: suite_passes; negative: broken_source_detected. A2 positive: codex_fixture_note; negative: missing_host_is_unmet. A4 positive: isolated_vault_only; boundary: no_existing_plugin_mutation.
- Risk: REQ-1/REQ-2/REQ-4; agent-decided use temporary Codex home and fixture vault, recording each host or network limitation.

## Simplicity check

- none found

## Questions asked

1 — what — 這樣的拆分範圍和驗收目標，符合你的意思嗎？

## Risks

1. Public installation identifiers and caches may behave differently across hosts; only claim a host when real installation and use are observed.
2. Upstream tests depend on historical files and root attribution; preserve their intent and isolate any adaptation from upstream state.
3. Independent review, remote repository creation, and the package suite can be blocked by host or network state; report evidence and preserve remaining work.
