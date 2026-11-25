# Mermaid skill for the new Obsidian engine — plan
intent: 2026-11-23-mermaid-skill-for-new-obsidian-engine@a2448ab
spec: docs/loom/2026-11-23-mermaid-skill-for-new-obsidian-engine/spec.md@9e32c3e
charter: 1.1

## Task DAG

Wave 1

**W1-01 Pele-based validator**  after: none  acceptance: 4
- Files: obsidian/skills/obsidian-mermaid-visualizer/scripts/validate.mjs, scripts/package.json, scripts/validate.sh, scripts/validate.test.sh, obsidian/tests/test_mermaid_validator.py
- Test: A4 positive: renders-ok-samples-pass; negative: pele-rejected-samples-fail (unquoted parens, timeline 9:00, CJK gitGraph branch).
- Risk: Pin pele to Obsidian 1.15 bundled version; validate.sh becomes thin wrapper so existing callers keep working. agent-decided per spec Design decision; tests skip when node unavailable.

**W1-02 Rewrite compatibility and quirks**  after: none  acceptance: 1, 2
- Files: obsidian/skills/obsidian-mermaid-visualizer/SKILL.md, obsidian-compatibility.md, obsidian-common-quirks.md, obsidian/tests/test_mermaid_skill_content.py
- Test: A1 positive: still-broken-patterns-listed; negative: fixed-patterns-not-prohibited. A2 positive: states-obsidian-1-15; negative: no-11-4-baseline-claim.
- Risk: Content sourced only from the evidence note's verified table; unverified items marked unverified. agent-decided, spec REQ-1/REQ-2.

Wave 2

**W2-01 Update and add diagram type files**  after: W1-01, W1-02  acceptance: 3
- Files: obsidian/skills/obsidian-mermaid-visualizer/flow/*.md, data-viz/*.md, structural/*.md, time/*.md, SKILL.md
- Test: A3 positive: every-type-example-passes-validator (13 new types); negative: excluded-types-absent (eventmodeling, cynefin, candlestick).
- Risk: Examples checked by W1-01 validator; one real-device spot check in Obsidian. agent-decided, spec REQ-3.

**W2-02 Sync dependents**  after: W1-02, W2-01  acceptance: 5
- Files: obsidian/README.md, obsidian/README.ja.md, obsidian/README.zh-TW.md, obsidian/skills/README*.md, obsidian/CHANGELOG.md, obsidian/skills/obsidian-markdown/references/mermaid-quirks.md, obsidian/skills/obsidian-markdown/references/viz-decision-guide.md, obsidian/tests/test_obsidian_markdown_viz_guide.py
- Test: A5 positive: package-suite-passes; boundary: no-stale-11-4-references-outside-changelog.
- Risk: Preserves existing inventory and viz-guide test coverage; may widen assertions, never narrows. agent-decided, spec REQ-5.

Wave 3

**W3-01 Graduate adversarial probes into package suite**  after: W2-01, W2-02  acceptance: 4
- Files: obsidian/tests/test_mermaid_validator_fence_forms.py, obsidian/tests/test_mermaid_skill_examples_render.py, docs/loom/2026-11-23-mermaid-skill-for-new-obsidian-engine/evidence/probes/
- Test: A4 positive: fence-forms-detected (tilde, callout); negative: unclosed-fence-fails.
- Risk: Probes caught defects, so they move into the every-change suite per review.probe-graduation; preserves their cases unchanged. agent-decided.

## Simplicity check
- Single validator replacing mermaid-cli instead of two validators — taken
- Validator-only example checks with one device spot check — taken

## Questions asked
① — what — 當前規劃會有全新的圖表嗎？
① — consequence — 新圖表全做或只做常用幾種 → "OK 那就都做吧"
② — behaviour — 六種情況的行為表與五項完成結果「這樣對嗎？」 → "對"

## Risks
1. Pele releases near-daily; behaviour may drift from pinned version. Validator records pinned version; skill states verification date.
2. Node/npm may be absent in test environments; validator tests skip with explicit reason rather than pass silently.
