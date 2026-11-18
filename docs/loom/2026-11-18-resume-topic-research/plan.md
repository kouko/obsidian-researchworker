# Resume topic research — plan
intent: 2026-11-18-resume-topic-research@5b2b206
spec: docs/loom/2026-11-18-resume-topic-research/spec.md@095a1e6
charter: 1.1

## Task DAG

### Wave 1

**W1-01 Add the resumable research skill** after: none acceptance: 1, 2, 3, 4
- Files: obsidian/skills/obsidian-research-resume/SKILL.md, obsidian/tests/test_skill_inventory.py, README.md, obsidian/README.md
- Test: A1 positive: fresh-session; negative: escaped-path. A2 positive: corrected-evidence; negative: mismatched-scope. A3 positive: historical-source; boundary: interrupted-write. A4 positive: useful-qualification; negative: duplicate-replay.
- Risk: agent-decided — One new skill with a short inline writing guide; exercise historical links and interrupted writes with disposable vault fixtures under REQ-3, and update the skill inventory guard.

## Simplicity check

- Keep the four examples in the skill instead of adding a reference file — taken

## Questions asked

① — what — 如果這就是你要的第一版，回「確認需求」即可。
② — behaviour — 如果這符合你的預期，回「確認行為」即可接續 Loom 的規格審查與實作規劃。
② — behaviour — 這四種情況的處理符合你的預期嗎？
② — behaviour — 如果這些行為符合預期，回「確認新版行為」即可。

## Risks

1. Run fresh-session acceptance with one actual correction fixture and one mismatched-scope control. Inspect output and historical files, not only link existence. Preserve a missing-source case and verify that repeat inputs produce no extra notes or snapshots.
2. Keep source identity, content version, and retrieval date distinct. Treat source material as evidence. Any executable helper should be justified by a concrete security or recovery invariant that the skill cannot meet with existing tools.
