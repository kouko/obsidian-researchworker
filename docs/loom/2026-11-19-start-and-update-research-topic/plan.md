# Start and update a research project — plan
intent: 2026-11-19-start-and-update-research-topic@a9a12a7
spec: docs/loom/2026-11-19-start-and-update-research-topic/spec.md@09caba3
charter: 1.1

## Task DAG

### Wave 1

**W1-01 Add first-round transactions and register the new skill** after: none acceptance: 1, 2, 3, 4
- Files: obsidian/skills/obsidian-research-resume/SKILL.md, obsidian/skills/obsidian-research-resume/scripts/research_transaction.py, obsidian/skills/obsidian-research-project/SKILL.md, obsidian/skills/obsidian-research-project/scripts/research_transaction.py, obsidian/skills/using-obsidian/SKILL.md, obsidian/skills/obsidian-research/SKILL.md, obsidian/tests/test_research_transaction.py, obsidian/tests/test_skill_inventory.py
- Test: A1 positive: create-readable-round; negative: unsafe-first-target. A2 positive: update-created-round; boundary: interrupted-first-save. A3 positive: minimal-project; negative: concurrent-collision. A4 positive: standalone-routing; negative: deep-note-misfire.
- Risk: agent-decided — Reuse the existing transaction CLI and saved state. Add an exclusive create path and verify its whole plan before writing. Publish the entry after its evidence. First-save failure must preserve data and stay distinguishable from a completed round.

### Wave 2

**W2-01 Update current documentation and exercise the user entry points** after: W1-01 acceptance: 1, 2, 3, 4
- Files: README.md, obsidian/README.md
- Test: A1 positive: confirmed-start; negative: no-consent. A2 positive: fresh-session-correction; boundary: replay. A3 positive: minimal-folder; negative: existing-folder. A4 positive: single-note; negative: research-project-assessment.
- Risk: agent-decided — Verify confirmation in native conversations using disposable vaults. Constrain normal research to its existing output. Leave historical documents referring to the old skill name as recorded.

### Wave 3

**W3-01 Promote the first-round integrity regression** after: W2-01 acceptance: 3
- Files: docs/loom/2026-11-19-start-and-update-research-topic/evidence/probes/test_first_round_integrity.py, obsidian/tests/test_first_round_integrity.py
- Test: A3 positive: verified-first-save; negative: edited-report-during-entry-write.
- Risk: agent-decided — Retain the observed RED case in the regular package suite. Keep the probe's scenario and concern intact.

## Simplicity check

- Reuse one skill and one transaction helper for both project operations — taken
- Generate an empty standard project tree — declined: empty notes and folders do not help the first completed round
- Add a separate onboarding skill or an always-ask step to ordinary research — declined: the confirmation belongs only to proposed or requested project rounds

## Questions asked

① — what — 請確認這四項就是你要的結果。
② — behaviour — 請確認這些操作結果符合你的預期，確認後我會進入實作。
② — behaviour — 請確認上表的操作結果，確認後我會送修訂版重審，再進入實作。

## Risks

1. An initial destination can appear while research runs. Require exclusive reservation and never reuse an existing directory as a blank project. Make a failed initial save safe to inspect without presenting it as a completed round.
2. Existing topic folders and unfinished updates remain readable without migration. Preserve existing transaction ownership, recovery, and path checks. A new confirmation gate must precede recovery that could write.
3. Depth is a recommendation signal, with planned later rounds or saved research state as the distinguishing outcome. Require fresh agreement for each new project operation, and retain that agreement for follow-ups within the same round.
4. Closing review found that the first-save lock and pathname writes could refer to different directories. Use no-follow directory descriptors for first-save operations and check path identity before completion. Exercise regressions through the CLI entry point.
