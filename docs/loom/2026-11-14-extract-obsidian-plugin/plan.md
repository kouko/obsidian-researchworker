# Extract Obsidian plugin — plan
intent: 2026-11-14-extract-obsidian-plugin@37fe7d3
spec: docs/loom/2026-11-14-extract-obsidian-plugin/spec.md@43957f9
charter: 1.1

## Task DAG

**W0-01 Preserve plugin history and predecessor paths** after: none  acceptance: 1,4
- Files: obsidian/, docs/provenance.md, tests/
- Test: A1 positive: history_inventory_verified; negative: missing_predecessor_rejected. A4 positive: original_ancestry_preserved; boundary: uncommitted_snapshot_restored_and_compared.
- Risk: REQ-1/REQ-4; agent-decided retain only Obsidian-related history; publish source-to-import ID mapping and any coverage limitations. Do not claim completeness if predecessor discovery or verification is inconclusive.

**W1-01 Transfer independently usable plugin baseline** after: W0-01  acceptance: 1,4
- Files: obsidian/, LICENSE, ATTRIBUTION.md, .github/workflows/test-obsidian.yml, tests/
- Test: A1 positive: source_tree_and_licenses; negative: missing_attribution_detected. A4 positive: upstream_unchanged; boundary: historic_tests_retained.
- Risk: REQ-1/REQ-4; agent-decided retain source tree and useful upstream tests; use one-time direct evidence rather than permanent migration fixtures.

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

## History verification

Discover relevant source paths through moves and renames and pin an expected source commit inventory. Compare each mapped commit's authors, dates, messages, relevant trees and ancestry. A missing pre-split commit or mapping must fail coverage. Before an isolated import, inventory and snapshot tracked changes and all untracked files including ROADMAP-DRAFT.md; restore and compare every preserved file before W1 resumes.

## W1/W2 offline implementation evidence — 2026-11-14

- W1-01: retained the plugin tree, MIT notices, attribution and useful upstream
  tests. Removed only the requested untracked migration test; removed its now
  empty root-suite CI invocation. Subsequently removed the added Canvas migration
  history tests and their two fixtures; retained unrelated upstream doc tests.
- W2-01: added a local marketplace resolving `./obsidian`; updated Claude/Codex
  repository URLs and independent OpenCode package/loader identity. Kept the
  `obsidian` plugin namespace and documented duplicate-registration uncertainty.
- W2-02: added root README, ROADMAP, migration guide and durable provenance with
  131 retained commit mappings and 67 invalidated signatures disclosed. Preserved
  ROADMAP-DRAFT.md and marked wiki removal, YTSS/RLSS and long research as future.
- Direct comparison against the cached upstream plugin: 153 identical files,
  no missing files, eight expected differences (three READMEs, two manifests,
  package metadata, loader identifiers and the prior Canvas test adaptation).
  A separate fixture hash inventory had no missing non-cache baseline files.
- All 131 mapped imported commits are ancestors of current HEAD. The marketplace
  source resolves locally. No network or remote freshness check was performed.
- Existing suite: `PYTHONDONTWRITEBYTECODE=1
  /Users/kouko/.conda/envs/dbt-redshift/bin/python3 -m pytest -q -p no:cacheprovider`
  from `obsidian/`: 155 passed. Default Homebrew Python lacks pytest; no package
  was installed. Drift check and Node syntax check passed; `git diff --check`
  passed for tracked edits. Direct comparisons also inspect the untracked plugin.
- W3 installation, actual note creation, live providers, host compatibility,
  rollback and closing review remain unverified. This implementer pass does not
  provide an attestation or claim overall acceptance. No readiness invocation.
- Changes remain uncommitted: this session exposes `.git` as read-only. No
  mutation of the original Monkey repository, actual vault or installed plugins
  was attempted.

## Simplicity check

- none found

## Questions asked

1 — what — 這樣的拆分範圍和驗收目標，符合你的意思嗎？
1 — what — 新 repo 目前只複製檔案；你希望也保留 Obsidian plugin 在 Monkey Skills 裡的 Git 提交歷史嗎？
1 — consequence — 保留歷史有兩種方式：只帶 Obsidian 相關提交會保留內容與作者，但提交編號會改變；完整帶入 Monkey Skills 歷史則保留原編號，也會帶入其他 plugins 的歷史。你偏好哪一種？

## Risks

User clarification, 2026-11-14: this one-time transfer adds no permanent migration
tests or verification infrastructure. Remove only the untracked
`tests/test_extraction_baseline.py`; retain useful upstream tests and existing
tests without the added migration-only history checks or fixtures. Use direct
offline comparison and existing tests. This
narrows verification machinery without resetting the active change or evidence.
W1/W2 exclude W3 host installation, network access and readiness invocation.
Agent-decided: retain plugin namespace `obsidian`, separate marketplace/package
identity, preserve the roadmap draft and publish retained-commit mappings only.

1. Public installation identifiers and caches may behave differently across hosts; only claim a host when real installation and use are observed.
2. Upstream tests depend on historical files and root attribution; preserve their intent and isolate any adaptation from upstream state.
3. The user added history preservation after W1 began; uncommitted W1 work is snapshotted and verified while W0 verifies original and predecessor history.
4. Independent review, remote repository creation, and the package suite can be blocked by host or network state; report evidence and preserve remaining work.
