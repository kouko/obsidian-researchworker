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

### Wave 2

**W2-01 Serialize research writes and recovery** after: W1-01 acceptance: 1, 3, 4
- Files: obsidian/skills/obsidian-research-resume/SKILL.md, obsidian/skills/obsidian-research-resume/scripts/research_transaction.py, obsidian/tests/test_research_transaction.py
- Test: A1 positive: locked-inspection; negative: escaped-path. A3 positive: interrupted-recovery; boundary: concurrent-writer. A4 positive: first-apply; negative: stale-or-replay.
- Risk: agent-decided — A process-held directory lock protects REQ-3 during recovery and writes. A prose-only instruction cannot enforce ownership. The helper handles files while the skill decides which evidence changes a judgment.

## Simplicity check

- Keep the four examples in the skill instead of adding a reference file — taken
- One helper for locked inspection, recovery, and applying changes — taken

## Questions asked

① — what — 如果這就是你要的第一版，回「確認需求」即可。
② — behaviour — 如果這符合你的預期，回「確認行為」即可接續 Loom 的規格審查與實作規劃。
② — behaviour — 這四種情況的處理符合你的預期嗎？
② — behaviour — 如果這些行為符合預期，回「確認新版行為」即可。

## Risks

The independent review of `d2277cc` reproduced an edit accepted as the
baseline after initial snapshot validation. Reuse the validated entries to
check every captured baseline and every returned inspection read. Recheck the
folder before journaling, since checking only planned destinations misses
unplanned changes. Use exclusive creation for absent targets. Existing-file
replacement has no portable compare-and-swap operation for non-cooperating
editors, so the runtime instructions request that editing and sync wait for
apply or recovery to finish.

Installed-plugin trials at `7336cd1` pinned the old report's link but
overwrote its exact prior bytes. Preserve those bytes under a separate dated
path before any link repair. A verified byte-for-byte archive keeps the
original version while the repaired report remains the reader's link target.
Test this against both default and explicitly selected folders.

1. Run fresh-session acceptance with one actual correction fixture and one mismatched-scope control. Inspect output and historical files, not only link existence. Preserve a missing-source case and verify that repeat inputs produce no extra notes or snapshots.
2. Keep source identity and content version distinct. Treat source material as evidence. Exercise overlapping processes and require busy callers to leave files unchanged.
