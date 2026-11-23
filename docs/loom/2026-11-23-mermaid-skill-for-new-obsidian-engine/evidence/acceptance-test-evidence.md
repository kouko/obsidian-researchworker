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

## Re-run on 2026-11-24, at df521e1
Fix range a3a92f1..df521e1: CJK identifier quoting guidance in `obsidian-common-quirks.md` Quirk 5 / quoting section / checklist, `obsidian-markdown/references/mermaid-quirks.md`, `structural/gitgraph.md` (new quoted-CJK example), `flow/usecase.md`, `structural/wardley.md`, `structural/requirement.md`, `flow/swimlane.md`; `scripts/validate.mjs` exits 2 when pele cannot load; tests. Clean worktree: `git worktree add --detach <scratch>/acc3/wt df521e1`. Engine: pele 1.13.0 from `~/.cache/obsidian-mermaid-visualizer/pele-1.13.0`. Device check skipped (no vault note created).
- Setup: `validate.test.sh` -> `7 passed, 0 failed`. `PELE_DIR=/nonexistent node validate.mjs validate.mjs` -> `cannot load pele from /nonexistent (...)`, `exit=2`.
- 1: re-tested — probe note `cjk.md` (scratch), validator output:
  - gitGraph `branch 開發` FAIL (`Lexical error ... branch 開發`); skill's quoted example (`branch "開發"`/`checkout`/`merge`) PASS.
  - usecase `actor 使用者` FAIL (`Expecting ... IDENTIFIER | PLAIN_STRING`); `actor "使用者"` + `"使用者" --> Login` PASS.
  - wardley bare `anchor 業務` FAIL (lexical); quoted anchor/component/edge PASS.
  - venn bare `set 前端` FAIL (lexical); quoted sets + union PASS.
  - requirement bare `requirement 登入 {` FAIL (lexical); quoted names PASS (`req.md` R1; my first quoted sample used `type: test`, a keyword -> `got 'VERIFY_TEST'`, my sample's error).
  - architecture `service "伺服器"(server)` FAIL (`Expecting token of type 'ID'`); `service api(server)[伺服器]` PASS.
  - radar `axis "速度"` FAIL (`Expecting token of type 'ID'`); `axis speed["速度"]` PASS.
  - unquoted CJK in classDiagram, stateDiagram-v2, erDiagram, flowchart (node + subgraph ID), mindmap, kanban: all PASS.
  All 20 results match the skill's claims.
- 2: carried over — no added line in the fix diff mentions `11.4` or `1.15` outside the loom report itself.
- 3: carried over — fix diff changes no type file's first example; the added gitgraph quoted-CJK example PASSes the engine (block 2 above) but was not opened in the app.
- 4: re-tested — validator over every `.md` under `obsidian-mermaid-visualizer/` and `obsidian-markdown/references/mermaid-quirks.md`: no FAIL. Probe results above agree with the skill text.
- 5: re-tested — `python3 -m pytest obsidian/tests/test_mermaid_skill_content.py obsidian/tests/test_mermaid_skill_examples_render.py obsidian/tests/test_mermaid_type_files.py obsidian/tests/test_mermaid_validator_fence_forms.py obsidian/tests/test_mermaid_validator.py obsidian/tests/test_obsidian_markdown_viz_guide.py -q -p no:cacheprovider` -> `31 passed in 5.45s`. Full suite left to finalize-review: `python3 -m pytest obsidian/tests obsidian-finance/tests -q -p no:cacheprovider`.

## Re-run on 2026-11-24, at 299ff69
Fix range df521e1..299ff69: `flow/flowchart.md` (CJK paragraph + error-prevention row: unquoted CJK renders, quote for parentheses/shape chars; link to `obsidian-common-quirks.md` "Quote positions" replaces the dangling "Quirk 4.5"), `flow/mindmap.md` (canonical-syntax line + bare-CJK paragraph), `SKILL.md` checklist quote list (adds venn sets, requirement/element names), `test_mermaid_skill_content.py`. Clean worktree: `git worktree add --detach <scratch>/acc4/wt 299ff69`. Engine: pele 1.13.0 from `~/.cache/obsidian-mermaid-visualizer/pele-1.13.0` (`engine: pele 1.13.0 (Obsidian 1.15.1 bundle)`). No vault note created; app not opened.
- Setup: `validate.test.sh` -> `ok - cold cache -> exit 0`, `7 passed, 0 failed`.
- 1: re-tested — probe note `acc4/p.md`, `validate.sh` output:
  - block 1 `A[開始] --> B(處理中) --> C{判斷}` PASS (flowchart.md claim: unquoted CJK renders).
  - block 2 `A[開始 (現在)]` FAIL (`Expecting 'SQE', 'UNICODE_TEXT', 'TEXT', 'TAGSTART', got 'PS'`); block 3 `A["開始 (現在)"]` PASS (claim: quote required for parentheses).
  - block 4 mindmap bare `可擴展性` / `效能` PASS (mindmap.md claim: bare CJK renders).
  - block 5 mindmap `Scale["可擴展性 (規模)"]` PASS.
  - block 6 mindmap bare `可擴展性 (規模)` PASS at parse level, but the engine reads `(規模)` as a rounded-shape label, so the text `可擴展性` is dropped silently — consistent with mindmap.md saying the wrapper is needed for parentheses (a silent problem the validator cannot flag).
  - SKILL.md:181 quote list now names venn sets and requirement/element names, matching the df521e1 probes (bare FAIL / quoted PASS). flowchart.md link resolves to `obsidian-common-quirks.md:146` `## Quote positions`.
- 2: carried over — the only added lines mentioning `1.15` are the two new flowchart/mindmap sentences, both stating Obsidian 1.15 / Pele 1.13.0; no `11.4`.
- 3: carried over — fix diff changes no example block in any type file (prose and a table row only).
- 4: re-tested — validator over every `.md` under `obsidian-mermaid-visualizer/` and `obsidian-markdown/references/mermaid-quirks.md`: no FAIL. Probe verdicts above match the skill text.
- 5: re-tested — the six mermaid/viz-guide test files (same command as above) -> `32 passed in 5.95s`. Full suite left to finalize-review: `python3 -m pytest obsidian/tests obsidian-finance/tests -q -p no:cacheprovider`.
