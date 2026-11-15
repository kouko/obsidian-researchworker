# OpenCode Obsidian identity and commands — plan
intent: 2026-11-15-opencode-obsidian-name@fe0f8f6
spec: docs/loom/2026-11-15-opencode-obsidian-name/spec.md@26ebfdc
charter: 1.1

## Task DAG

**W1-01 Register Obsidian identity and commands** after: none acceptance: 1, 2, 3, 4, 5
- Files: obsidian/.opencode-plugin/index.js, obsidian/package.json, obsidian/tests/test_opencode_loader.py, README.md, docs/migration.md
- Test: A1 positive: obsidian-id; negative: old-id. A2 positive: fourteen-skills; boundary: missing-description. A3 positive: other-host-identity; negative: repo-rename. A4 positive: no-data-writes; boundary: repeated-setup. A5 positive: command-prompt; negative: missing-command.
- Risk: REQ-1–5; agent-decided reuse loaded skills for commands; verify registration and execution path in isolated OpenCode as well as automated loader cases.

## Simplicity check

- none found

## Questions asked

① — what — OpenCode 那邊名稱應該是 obsidian ， marketplace 名稱才是 obsidian-researchworker
② — behaviour — 對

## Risks

1. Existing `obsidian-researchworker:*` references change; the repository and other host identities remain unchanged.
