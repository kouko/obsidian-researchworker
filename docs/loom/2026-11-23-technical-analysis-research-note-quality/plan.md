# Technical analysis research note — plan
intent: 2026-11-23-technical-analysis-research-note-quality@d803142
spec: docs/loom/2026-11-23-technical-analysis-research-note-quality/spec.md@f678a8e
charter: 1.1

## Task DAG

### Wave 1 — Saved research notes

**W1-01 Guide the saved report from question to evidence**  after: none  acceptance: 1, 2, 3
- Files: obsidian-finance/skills/technical-analysis/SKILL.md
- Test: A1 positive: conclusion-first-note; boundary: insufficient-horizon. A2 positive: extrema-and-attributed-warning; boundary: late-source. A3 positive: matched-replay-and-links; negative: note-collision. Reuse technical report publication tests.
- Risk: REQ-1–3. agent-decided — Keep existing publication and calculations. Use the same prompt and inputs in fresh sessions to expose format drift.

#### Verification for W1-01

- Capture the installed baseline and candidate in isolated fresh Codex sessions. Match model, exact request, quote snapshot, cutoff, and relevant source fixtures. Avoid naming the desired output structure in the prompt.
- Check properties, research question, conclusion, cutoff and revision conditions near the start. Verify contents resolve and the note explains range-extrema support and resistance while preserving material dates and values. Compare computed and external thresholds only on evidence eligible for the request.
- Compare snapshot attachments to the original and replay the report. Check chart and sources resolve. Exercise a limited-data note and reuse tests for collisions and recording provenance.
- Run `python3 -m pytest obsidian/tests obsidian-finance/tests -q -p no:cacheprovider`. Record actual baseline/candidate outputs and limitations without altering the user's vault.

## Simplicity check

- none found

## Questions asked

① — what — 這個樣稿的方向符合你要的研究筆記水準嗎？
② — behaviour — 你確認這就是要的預設存檔行為嗎？

## Risks

1. The same model can render different content across sessions. Preserve the raw matched runs and evaluate the user-visible result.
2. A compact summary may conceal date, provenance or pattern information. Retain detailed evidence in the saved note.
3. Historical source versions can drift. Preserve the original cutoff and avoid rebuilding the comparison from undated pages.
