# Retire Obsidian File Intel — plan
intent: 2026-11-24-remove-obsidian-file-intel@4bff87f
spec: docs/loom/2026-11-24-remove-obsidian-file-intel/spec.md@b9a6527
charter: 1.1

## Task DAG

### Wave 1

**W1-01 Retire the packaged skill** after: none acceptance: 1, 2, 3
- Files: obsidian/skills/, obsidian/README*.md, obsidian/.claude-plugin/plugin.json, obsidian/.codex-plugin/plugin.json, obsidian/tests/test_skill_inventory.py, ATTRIBUTION.md
- Test: A1 positive: inventory; negative: retired-references. A2 positive: package-suite; boundary: loader-inventory. A3 positive: upstream-attribution; boundary: package-only-diff.
- Risk: REQ-1–3; agent-decided reuse the existing inventory guard in obsidian/tests/test_skill_inventory.py, preserving other retirement checks and adding this skill to the retired set.

## Simplicity check
- Remove the entry directly and reuse inventory tests — taken

## Questions asked
① — what — 這就是你要的移除範圍嗎？
② — behaviour — 請確認新版就照上述方式運作

## Risks
1. Keep historical records and upstream attribution; verify active metadata and retained guidance independently of historical references.
