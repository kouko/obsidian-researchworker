# Mermaid skill for the new Obsidian engine — spec
intent: 2026-11-23-mermaid-skill-for-new-obsidian-engine@a2448ab
confirmed-behavior: 2026-11-23 @61e5068
pre-build-review: not-required — skill instructions and a local validator only; no security, irreversible data, external contract or cross-system change; skill name and entry point stay fixed

## Requirements
REQ-1 — Rules match verified engine behaviour
  The skill shall instruct avoidance of every authoring pattern the research verified as still failing on the Obsidian 1.15 engine, and shall not prohibit any pattern the research verified as fixed → Acceptance #1
REQ-2 — Stated target is Obsidian 1.15
  The skill shall state Obsidian 1.15 (its built-in engine) as its target and its known limits, and shall not claim Mermaid 11.4.x as the compatibility baseline → Acceptance #2
REQ-3 — New diagram types usable
  For each diagram type the research verified as rendering (venn, treemap, radar, sankey, kanban, journey, ishikawa, treeView, swimlane, wardley, usecase, packet, requirement), the skill shall provide guidance and at least one example that renders without error in Obsidian 1.15 → Acceptance #3
REQ-4 — Self-check agrees with the engine
  WHEN the skill's self-check runs on a sample set of diagrams the engine rejects and diagrams the engine renders, the self-check shall report each sample's pass/fail identically to the engine → Acceptance #4
REQ-5 — Dependents stay consistent
  The skills, documentation and tests that reference this skill shall remain consistent with it, and the package test command shall pass → Acceptance #5

## Design decision
- Rewrite `obsidian-compatibility.md` and `obsidian-common-quirks.md` around the Pele engine behaviour recorded in the evidence note; update affected type files (xychart, architecture, block, timeline, gitgraph, state, flowchart); add one type file per new type under the existing category folders. agent-decided — keeps the skill's existing progressive-disclosure layout.
- Replace the mermaid-cli validator with a Node script that renders each block with the `pele` npm package pinned to the version bundled in the user's Obsidian (record the version in the script). agent-decided — mermaid-cli disagrees with Pele on several verified cases, so it cannot satisfy REQ-4.
- Keep a shell entry wrapper only if tests reference it; otherwise update tests to the new script. agent-decided — avoid two validators.
- Excluded: eventmodeling and cynefin (syntax not resolved); candlestick (unsupported). agent-decided — REQ-3 limited to verified types.
- Obsidian-specific behaviours (theme ignored, icons empty, links not indexed, CJK wrapping) documented as warnings, not workarounds. agent-decided — intent Out of scope excludes adding engine features.

## Alternatives considered
- Keep mermaid-cli and add a Pele-differences list — rejected: still mis-judges samples, fails REQ-4.
- Rewrite SKILL.md as a single file — rejected: loses per-type lazy loading and breaks existing references.
- Validate via the live Obsidian CLI — rejected: requires a running app and enabled CLI; not reproducible in tests.

## Current state evidence
- Forward: obsidian/skills/obsidian-mermaid-visualizer/SKILL.md:9 (claims Obsidian 11.4.1 target)
- Reverse: obsidian/skills/obsidian-research/SKILL.md, obsidian/tests/test_skill_inventory.py, obsidian/tests/test_obsidian_markdown_viz_guide.py, obsidian/README*.md
- Error: obsidian/skills/obsidian-mermaid-visualizer/scripts/validate.sh:20 (`MERMAID_VER="11.4.2"`, judges by old renderer)
- Data: obsidian/skills/obsidian-mermaid-visualizer/obsidian-compatibility.md (17-type matrix for 11.4.1)
- Boundary: skill folder plus its referrers; user vault notes untouched

## UI flows
Surface: a user asks Claude, in an Obsidian note context, to draw a diagram.

| case | what the user does | what they see |
|---|---|---|
| Existing type | asks for a flowchart / gantt / timeline etc. | a diagram that renders in Obsidian 1.15 without error, written without obsolete workarounds |
| New type | asks for e.g. a venn, sankey, radar or kanban | a diagram of that type that renders in Obsidian 1.15 |
| Pattern still broken | content needs a pattern known to fail (e.g. parentheses in a label, time like `9:00` in a timeline) | Claude writes the safe form; the diagram renders |
| Engine limit | asks for a theme, an icon, or links counted as backlinks | Claude says the engine ignores / does not support it, and draws without it |
| Unsupported type | asks for a candlestick chart | Claude says Obsidian's engine cannot draw it and offers the closest supported chart |
| Self-check | Claude checks a note's diagrams | each diagram is reported pass or fail, matching what Obsidian shows |

Empty: a note with no diagrams → self-check reports "no mermaid diagrams found" and passes. In progress: N/A — instant. Error: a failing diagram → self-check names the block and the engine's error message; the way out is to fix that block and rerun.
