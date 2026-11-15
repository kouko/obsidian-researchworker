# Shared vault instructions — plan
intent: 2026-11-15-align-vault-instructions@a87ecbd6c765539bd375eb6816a0e2532ab4b9fb
spec: docs/loom/2026-11-15-align-vault-instructions/spec.md@3af0ada33a47abca7e1ace5d50667d9174d8321b
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

### Wave 3 — Confirmed instruction refinement

**W3-01 Reduce duplicated generated instructions and narrow context triggers** after: W1-01 acceptance: 1, 2, 3, 4, 6
- Files: `obsidian/skills/obsidian-vault-setup/`, `obsidian/README*.md`, `obsidian/CHANGELOG.md`, `README.md`
- Test: A1 positive: compact-personalized; boundary: no-unrelated-daily-read. A2 positive: required-skill-routing; boundary: unavailable-skill-reported. A3 positive: exact-import; boundary: host-unverified. A4 positive: custom-rules-preserved; boundary: ancillary-unchanged. A6 positive: synthetic-comparison; boundary: private-excluded.
- Risk: agent-decided — REQ-1/2/3/4/6: keep existing structure/description and release versions; reuse three manual eval cases plus task-scoped context cases. Baseline 56 lines; reduction is measured, not a quota. No new framework; inventory/Canvas tests retain unchanged coverage.

**W4-01 Apply the approved reduction to local rules without losing unique requirements** after: W3-01, W2-01 acceptance: 3, 4, 5, 6
- Files: External vault only: `AGENTS.md`, `CLAUDE.md`, `.agent-instruction-backups/`; private target supplied at dispatch, no repository edits
- Test: A3 positive: import-resolves; boundary: host-unverified. A4 positive: private-requirements-retained; boundary: concurrent-change-stops. A5 positive: retired-entry-remains-absent; boundary: protected-content-unchanged. A6 positive: private-local-evidence; boundary: public-excluded.
- Risk: agent-decided — REQ-3/4/5/6: preserve local exceptions and video-delivery rules while removing only duplicate catalogs/manuals and broad triggers. Back up current bytes anew; preserve earlier originals, memory, local skills and concurrent workspace state. No vault Git commit or shortcut rewrite.

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
6. user-decided — Approved combined simplification with "OK" on 2026-11-15; continue six Acceptance obligations and the existing review episode. Round 2 replaces invalidated output/context evidence; the old attestation is not current and no failure/retry budget is reset.
