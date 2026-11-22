# Taiwan equity research depth — plan
intent: 2026-11-23-tw-equity-depth@dcc22e2
spec: docs/loom/2026-11-23-tw-equity-depth/spec.md@fb0d521
charter: 1.1

## Task DAG

**W1-01 Readable Taiwan notes with portable evidence** after: none acceptance: 1, 4
- Files: obsidian-finance/scripts/research_markdown.py, obsidian-finance/scripts/research_store.py, obsidian-finance/tests/test_research_continuation.py
- Test: A1 positive: readable-overview-and-evidence; boundary: missing-or-invalid-machine-record. A4 positive: Taiwan-portable-and-US-legacy; boundary: changed-prose-and-concurrent-write.
- Risk: REQ-1/4 — agent-decided: stage immutable evidence before making the overview reference visible, retain legacy readers, and validate that reference during recovery.

**W1-02 Taiwan role frameworks** after: none acceptance: 2
- Files: obsidian-finance/skills/tw-equity-research/SKILL.md, obsidian-finance/skills/tw-equity-research/references/analysis-framework.md
- Test: A2 positive: compare the seven bodies against role-specific analytical obligations; boundary: incomplete evidence leaves a named conclusion open.
- Risk: REQ-2 — agent-decided: define the question, evidence, reasoning and failure conditions per role without requiring irrelevant metrics or imputing missing history.

**W2-01 Installed package replay** after: W1-01, W1-02 acceptance: 1, 2, 3, 4
- Files: obsidian-finance/README.md, docs/loom/2026-11-23-tw-equity-depth/acceptance-test-report.md
- Test: A1 positive: eight readable notes; boundary: support records. A2 positive: grounded role findings; boundary: source limitations. A3 positive: six isolated quarter runs; boundary: three continuations. A4 positive: original versions resolve; boundary: legacy and edited prose.
- Risk: REQ-1–4 — agent-decided: run the installed artifact against frozen source cutoffs, starting with TSMC Q3 reading and reporting explicit limits per issuer.

## Simplicity check

- Keep fixed quarterly filenames and shared storage APIs — taken
- Move machine records to a sidecar and leave required plain properties in notes — taken
- Reuse immutable quarter evidence preparation for the companion record and commit its overview link through the existing note transaction — taken
- Make existing US and Taiwan notes use a new format before they can be read — declined: the dual reader preserves existing data and limits conversion to new Taiwan publication.

## Questions asked

① — what — 你確認依這四條進入規格與實作嗎？
② — behaviour — 你確認這就是預期的閱讀與更新方式嗎？
② — behaviour — 這兩個補上的處理方式符合你的預期嗎？

## Risks

1. A copied quarter needs all referenced evidence; exercise portable verification with missing, mutated and cross-company record fixtures.
2. A shallow report may satisfy storage checks; independently assess evidence and inference for every role, recording material limitations and all three version-linked transitions.

## Review obligations

- For W1-01, keep the human-readable note available when companion evidence is missing, malformed or belongs to another quarter. Discovery must show an explicit gap and block only affected reuse. Verify interrupted publication through the real recovery entry point with a companion record and intervening edits. Recover a coherent pair or preserve existing files for inspection.
- For W1-02 and W2-01, audit all seven roles against the saved evidence. Each role needs a question, a supported finding or an explicitly pending finding, a material limitation and the evidence that would change the assessment. A required unresolved conclusion cannot count as verified just because a note was saved. Include a controlled insufficient-evidence case.
