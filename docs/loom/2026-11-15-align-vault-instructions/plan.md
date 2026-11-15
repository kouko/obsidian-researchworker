# Shared vault instructions — plan
intent: 2026-11-15-align-vault-instructions@a87ecbd6c765539bd375eb6816a0e2532ab4b9fb
spec: docs/loom/2026-11-15-align-vault-instructions/spec.md@cda9a4a0d75f3c0b5ab7bc04a135dde4b1fcc560
charter: 1.1

## Task DAG

### Wave 1 — Public initializer contract and release

**W1-01 Update shared instruction generation and safe re-entry** after: none acceptance: 1, 2, 3, 4, 6
- Files: `obsidian/skills/obsidian-vault-setup/`, `obsidian/README*.md`, `obsidian/CHANGELOG.md`, `obsidian/.claude-plugin/plugin.json`, `obsidian/.codex-plugin/plugin.json`, `.claude-plugin/marketplace.json`, `obsidian/package.json`, `README.md`
- Test: A1 positive: personalized; boundary: preview-declined. A2 positive: current-routing; boundary: dangling-links. A3 positive: shared-body; boundary: host-unverified. A4 positive: preserved-customization; boundary: ancillary-preserved. A6 positive: fixture-evidence; boundary: private-excluded.
- Risk: agent-decided — REQ-1/2/3/4/6: retain description triggering and role customization; short inline policy, no generator or prose-mirror tests. Three synthetic old/new cases expose generated-file defects; existing Canvas/Markdown tests retain coverage. Minor release reflects the changed output contract.

### Wave 2 — Private local application

**W2-01 Apply preserved local rules and retire obsolete shortcut** after: W1-01 acceptance: 3, 4, 5, 6
- Files: External vault only: `AGENTS.md`, `CLAUDE.md`, `.claude/commands/daily-news.md`, `.agent-instruction-backups/`; private target supplied at dispatch, no repository edits
- Test: A3 positive: import-resolves; boundary: conflicting-bodies-absent. A4 positive: originals-restorable; boundary: concurrent-edit-preserved. A5 positive: shortcut-retired; boundary: notes-unchanged. A6 positive: private-evidence; boundary: repository-clean.
- Risk: agent-decided — REQ-3/4/5/6: apply only approved local targets after snapshots; preserve valid unique requirements and existing uncommitted changes. Store backups as non-discoverable data with restore mapping. No vault Git commit, remote transfer, global settings or ancillary writes.

## Simplicity check

- none found

## Questions asked

① — what — 以上範圍符合你的意思嗎？
② — behaviour — 以上使用結果正確嗎？
② — behaviour — 這個使用結果正確嗎？

## Risks

1. agent-decided — Existing instruction sources differ; merge semantic requirements rather than choosing one wholesale. Preserve original transcript-delivery expectations locally while removing unavailable tool advertisements, not adding a new integration.
2. agent-decided — Public artifacts use synthetic personas and fixtures. Real instruction bodies, backups and detailed local evidence remain outside the plugin repository; public acceptance evidence reports only bounded outcomes.
3. agent-decided — Use the skill-authoring quick evaluation path because this is a bounded template-policy refresh with confirmed criteria; retain the existing structure and description. Compare the old skill before edits; new, existing and refused/conflicting cases cover the contract.
4. agent-decided — Runtime discovery can be suppressed by host settings or overriding instruction files. Validate the common body/import separately and disclose any unexecuted host behavior; do not change global host settings to force a pass.
5. agent-decided — Existing memory and local skills stay unchanged, including on setup re-entry. Missing ancillary creations must appear in the confirmed setup preview; the one-time private cleanup invokes no ancillary or application-opening branches.
