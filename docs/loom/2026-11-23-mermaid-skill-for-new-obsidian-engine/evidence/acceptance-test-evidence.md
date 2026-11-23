# Mermaid skill for the new Obsidian engine — acceptance test evidence

Tried on 2026-11-23, in a clean copy of the project at 4b9cd8f (`git worktree add --detach <scratch>/at 4b9cd8f`).

Setup: the skill ships as plain markdown inside the `obsidian` plugin; the only runnable part is
`scripts/validate.sh`, which needs `node` and installs pinned `pele` 1.13.0 into
`~/.cache/obsidian-mermaid-visualizer/pele-1.13.0` on first use. The cache was already present on this
machine, so the first-run install path was not exercised here. `validate.test.sh`: `6 passed, 0 failed`.

## 1. 本次研究在 Obsidian 實機或新引擎上確認「仍會出錯」的每一種寫法，技能都會指示避開；確認「已修好」的寫法，技能不再當成禁止事項。
- How I tried it: read `obsidian-common-quirks.md` (Quirks 1-6 "Still broken/required"; section "Fixed in Obsidian 1.15 — do not avoid any more"), then rendered one sample per pattern with the validator (`samples.md` in scratch).
- What came back:
  - still-broken, skill says avoid -> engine FAIL: unquoted parens label (`got 'PS'`), timeline `9:00 :` (`got 'INVALID'`), bare subgraph name (`got 'NODE_STRING'`), architecture edge without sides (`Expecting token of type ':'`). Comma `style A,B` PASSes (silent orphan node — the skill documents it as a silent problem, correct).
  - fixed, skill says no longer avoid -> engine PASS: `A[1. Perception]`, unquoted CJK label, `<br/>` label, `stateDiagram` v1, `---` edge.
- Evidence: validator output above; quirks file lines 15-139.

## 2. 技能說明的支援版本與限制，與新版 Obsidian（1.15）一致，不再宣稱以舊版 Mermaid 為準。
- How I tried it: `grep -n '11.4|1.15|Pele'` over SKILL.md and obsidian-compatibility.md; `grep -rl '11.4'` over both plugins.
- What came back: SKILL.md:9, :39, :172, :229 and compatibility.md:5-11 target Obsidian 1.15 / Pele 1.13.0 (Mermaid 12.1.0 syntax). Remaining `11.4` hits are only the dated v2.0.0 changelog line in the three READMEs, CHANGELOG.md, and tests asserting its absence elsewhere.
- Evidence: `test_obsidian_markdown_viz_guide.py` (stale-claim guard) passed.

## 3. 對研究中確認可正常顯示的新圖表類型，技能至少能產出一張可在 Obsidian 正確顯示的範例。
- How I tried it: extracted the first ```mermaid block of each of the 13 new type files (venn, treemap, radar, sankey, kanban, journey, ishikawa, treeview, swimlane, wardley, usecase, packet, requirement) plus 7 updated types (xychart, architecture, block, timeline, gitgraph, state, flowchart) into the temp note `_loom-acceptance-mermaid-2026-11-23.md` at the vault root. Opened it in the running Obsidian (`obsidian version` -> `1.15.1 (installer 1.15.0)`) in reading mode via `dev:cdp Runtime.evaluate`, scrolled through, and for each `h2` read the following block's `svg:not(.svg-icon)` and any error element/text.
- What came back: 20/20 sections have an `svg.pele.pele-<type>` (pele-venn … pele-requirement, pele-xychart … pele-flowchart), 0 error elements. Validator on the same note: 20 PASS. Screenshot taken (`dev:screenshot`, scratch only). Temp note then closed and deleted; `Pele-測試-2026-11-23.md` untouched.
- Evidence: probe output in this session; per-type class list above.

## 4. 技能的自我檢查對一組「新引擎會報錯」與「新引擎可正常顯示」的樣本，判定結果與新引擎一致。
- How I tried it: validator on the 9-sample set (see #1) and on the 20-example note (see #3).
- What came back: renders-in-app side: 20/20 agree with the live app. Errors side: the 4 broken patterns FAIL with the same parse errors the research recorded (quirks file Quirk 3 quotes the identical message); I did not re-render the broken set in the app (one temp note allowed). A ninth sample I wrote myself (venn guess syntax) failed — my sample, not the skill's.
- Evidence: tests `test_mermaid_validator.py`, `test_mermaid_validator_fence_forms.py` passed.

## 5. 其他引用這個技能的技能、說明文件與測試仍一致可用，套件測試全數通過。
- How I tried it: `python3 -m pytest obsidian/tests/test_mermaid_skill_content.py obsidian/tests/test_mermaid_skill_examples_render.py obsidian/tests/test_mermaid_type_files.py obsidian/tests/test_mermaid_validator_fence_forms.py obsidian/tests/test_mermaid_validator.py obsidian/tests/test_obsidian_markdown_viz_guide.py -q -p no:cacheprovider`
- What came back: `27 passed in 5.34s`.
- Full suite (not run here; finalize-review runs it and blocks on failure): `python3 -m pytest obsidian/tests obsidian-finance/tests -q -p no:cacheprovider`.

## Re-run on 2026-11-23, at a3a92f1
Fix range 4b9cd8f..a3a92f1: `obsidian-markdown/references/mermaid-quirks.md` (`()` row -> "Quote the label (Rule 5)"), `flow/flowchart.md` Example 5 (`"1. Perception"` … labels, ①②③④ note removed), `validate.test.sh` cold-cache case, `test_obsidian_markdown_viz_guide.py`. Clean worktree at a3a92f1.
- Setup: `validate.test.sh` -> `ok - cold cache -> exit 0`, `7 passed, 0 failed`.
- 1: re-tested — same 9 samples plus quoted `A["Start (now)"]`: blocks 1-4 FAIL with the same parse errors as before, 5-8 PASS, quoted-parens PASS (block 10); block 9 is my own bad venn sample, as before. `mermaid-quirks.md:70` and `:94` now say quote labels with `()`, consistent with `obsidian-common-quirks.md` Quirk 2; `flowchart.md` no longer prescribes ①②③④, matching the "Fixed" table.
- 2: carried over — fix diff touches no version/limit text (`grep '11.4|1.15'` over the diff: none).
- 3: carried over — no new-type file in the fix diff; the only changed example (flowchart Example 5) re-validated under 1/4.
- 4: re-tested — validator over every `.md` under `obsidian-mermaid-visualizer/*/` and `mermaid-quirks.md`: no file FAILs; `flowchart.md` 11/11 blocks PASS (incl. Example 5). Broken/fixed samples as in 1. App not re-opened.
- 5: re-tested — the six mermaid/viz-guide test files: `28 passed in 5.99s`. Full suite left to finalize-review (same command).
