# Remove wiki and daily-news mechanisms — acceptance test evidence

Tried on 2026-11-14, in a clean copy of the project at 36ba53c.

Full tested HEAD: `36ba53c1baa3cc3447b339ec35c9c41010a8c2a5`.
Base: `5c34004d6b2b4524e97ea7d4d77add7919ddb9f3`.
Clean copy: `/private/tmp/removal-acceptance-36ba53c`.
Active report destination: `/private/tmp/obsidian-remove-wiki-news-20261114`.
No network, installed-cache, real-vault or other-repository writes occurred.
This is source-level execution with a synthetic registration context, not live host execution.

## Setup and shared captured commands

Read root README and plugin README before execution. Root README requires Python and pytest already available; used the existing interpreter without installing dependencies. The plugin README explicitly leaves live host installation unverified and documents external dependencies; those services were not used.

```sh
git archive 36ba53c1baa3cc3447b339ec35c9c41010a8c2a5 -o /private/tmp/removal-acceptance.tar
mkdir /private/tmp/removal-acceptance-36ba53c
tar -xf /private/tmp/removal-acceptance.tar -C /private/tmp/removal-acceptance-36ba53c
```
All three exited 0. No pre-existing working files were copied.

From the clean copy's obsidian directory:
```sh
PYTHONDONTWRITEBYTECODE=1 /Users/kouko/.conda/envs/dbt-redshift/bin/python3 -m pytest -q -p no:cacheprovider tests/test_skill_inventory.py tests/test_validate_canvas.py tests/test_obsidian_markdown_viz_guide.py
```
Captured output: `14 passed in 0.43s`, exit 0. These are criterion tests, not the full package suite.

From the clean root, executed the real OpenCode source loader:
```sh
node --input-type=module -e 'import plugin from "./obsidian/.opencode-plugin/index.js"; const skills=[]; await plugin.setup({skill:{transform:async fn=>fn({add:s=>skills.push(s)})}}); console.log("Registered",skills.length,"skills"); for(const s of skills) {if(!s.content||!s.description) throw Error(s.id); console.log(s.id)} if(skills.length!==14||skills.some(s=>/:(wiki-|daily-news)/.test(s.id)))throw Error("inventory");'
```
Captured output (exit 0):
```text
Registered 14 skills
obsidian-researchworker:dashboard-design
obsidian-researchworker:defuddle
obsidian-researchworker:obsidian-bases
obsidian-researchworker:obsidian-canvas
obsidian-researchworker:obsidian-cli
obsidian-researchworker:obsidian-daily
obsidian-researchworker:obsidian-excalidraw-diagram
obsidian-researchworker:obsidian-file-intel
obsidian-researchworker:obsidian-markdown
obsidian-researchworker:obsidian-mermaid-visualizer
obsidian-researchworker:obsidian-research
obsidian-researchworker:obsidian-tldr
obsidian-researchworker:obsidian-vault-setup
obsidian-researchworker:using-obsidian
```

## 1. 新版本不再提供目前建立、萃取、查詢、連結、合併、檢查、自動研究與維護 wiki 的能力。
- How I tried it: ran `test_shipped_skill_inventory`, `test_retained_skills_have_no_retired_dependencies` and the real loader command above.
- What came back: both tests passed; none of the eight wiki skill directories or registrations remained. The dependency test also verified removed shared helpers and wiki-ingest test directory absent.
- Evidence: `obsidian/tests/test_skill_inventory.py`; loader output above.

## 2. 新版本不再提供目前的每日新聞彙整、跨日期新聞回顧、新聞故事追蹤與其專用維護能力。
- How I tried it: same inventory and dependency tests; inspected deleted paths with `git diff --name-only 5c34004d6b2b4524e97ea7d4d77add7919ddb9f3 36ba53c1baa3cc3447b339ec35c9c41010a8c2a5`.
- What came back: daily-news-digest absent from registration and disk; deleted paths included arc-tracking, collect_history.py, collect_sources.py and dedicated validation support.
- Evidence: the two passing inventory tests and loader output.

## 3. 保留的技能可在不含 wiki 與每日新聞元件的環境載入，與本次移除相關的既有功能檢查及代表性基本操作通過。
- How I tried it: executed loader and targeted tests above; ran the packaged validator directly on a packaged Canvas template:
```sh
/Users/kouko/.conda/envs/dbt-redshift/bin/python3 obsidian/skills/obsidian-canvas/scripts/validate_canvas.py obsidian/skills/obsidian-canvas/assets/template-mindmap-simple.canvas
```
- What came back: validator exit 0, empty output. Targeted tests: 14 passed; includes nine Canvas cases and three Markdown guide checks, plus two inventory checks.
- Basic user operation: read `obsidian/skills/obsidian-markdown/SKILL.md` (workflow, Properties, Internal Links and Callouts); created `Existing.md` and `Acceptance-note.md` only in the disposable copy with the edit tool. Confirmed target existed before emitting its wikilink. Wrote a journal frontmatter, `[[Existing]]`, and note callout, then read them back:
```sh
/Users/kouko/.conda/envs/dbt-redshift/bin/python3 -c 'from pathlib import Path; p=Path("Acceptance-note.md"); s=p.read_text(); assert Path("Existing.md").is_file(); assert "[[Existing]]" in s and "> [!note]" in s and s.startswith("---\n"); print(p.read_text()); print("Basic Markdown fixture: existing target, frontmatter, wikilink and callout preserved.")'
```
Captured output (exit 0):
```text
---
type: journal
status: draft
---
# Acceptance note

[[Existing]] remains an ordinary internal link.

> [!note]
> General daily note writing remains available.

Basic Markdown fixture: existing target, frontmatter, wikilink and callout preserved.
```
- Full suite command, deliberately not run by this tester: from `obsidian`, `/Users/kouko/.conda/envs/dbt-redshift/bin/python3 -m pytest -q -p no:cacheprovider`. Package-tests is not skipped; finalize-review will execute the automated test suite and block acceptance on failure. Prior Build results are not this tester's evidence.

## 4. 插件入口、功能說明與現行操作文件不再引導使用者執行已移除的 wiki 或每日新聞功能。
- How I tried it: read README, plugin README, manifests, router and research skill; searched the current English/Japanese/Traditional Chinese guides:
```sh
rg -n 'wiki-|daily-news|store-arcs|collect_history' README.md ROADMAP.md docs/migration.md obsidian/README* obsidian/skills/README.md obsidian/.codex-plugin/plugin.json obsidian/.claude-plugin/plugin.json obsidian/skills/using-obsidian/SKILL.md obsidian/skills/obsidian-research/SKILL.md
```
- What came back: only explicit retirement statements in root README:4, ROADMAP:3/15/17, migration:5, plugin README:31, Japanese README:30 and Traditional Chinese README:29. No removed invocation in router, research skill, manifest or skill attribution table. Loader showed fourteen current skills.

## 5. 使用者既有 vault 筆記、新聞摘要、故事追蹤筆記與設定、原 Monkey 專案及其他未授權工作不因本次移除被刪除或改寫。
- How I tried it: inspected the committed base-to-tested-HEAD path list and deletion scope; read migration and spec constraints. No migration/deletion command targets user output. All executed commands were read-only outside the fresh copy and report destination.
```sh
shasum -a 256 /Users/kouko/GitHub/obsidian-researchworker/ROADMAP-DRAFT.md
```
- What came back: `ffb3b44f03b09109080cbc3f5cba11352b80d436e43c340e9a1e382d213945fd`, matching supplied original hash.
- Limitation: no real vault or Monkey checkout was opened, deleted or rewritten. This is bounded committed-diff and execution-scope evidence, not an exhaustive before/after audit of external machines.

## 6. 專案 Git 歷史、必要授權與既有歷史紀錄仍可追溯，並能區分歷史功能與目前提供的功能。
- How I tried it: read changelog and provenance; verified original base remains an ancestor, archive reference and all provenance mapping destinations:
```sh
git show-ref | rg 'archive/obsidian'
/Users/kouko/.conda/envs/dbt-redshift/bin/python3 -c 'import json,subprocess; from pathlib import Path; tip="3c95872cb266a54af38f5a43485da4b9aa0c06fd"; mapping=json.loads(Path("docs/provenance-commits.json").read_text()); [subprocess.run(["git","merge-base","--is-ancestor",s,tip],check=True) for s in mapping.values()]; print(f"{len(mapping)} mapped commits reachable from archive tip"); print("Protected licensing/mapping diff:"); subprocess.run(["git","diff","--exit-code","5c34004d6b2b4524e97ea7d4d77add7919ddb9f3","36ba53c1baa3cc3447b339ec35c9c41010a8c2a5","--","LICENSE","ATTRIBUTION.md","docs/provenance-commits.json"],check=True); print("unchanged"); subprocess.run(["git","merge-base","--is-ancestor","5c34004d6b2b4524e97ea7d4d77add7919ddb9f3","36ba53c1baa3cc3447b339ec35c9c41010a8c2a5"],check=True); print("base remains ancestor of tested HEAD")'
```
Captured output:
```text
3c95872cb266a54af38f5a43485da4b9aa0c06fd refs/remotes/origin/archive/obsidian-3.27.0-history
131 mapped commits reachable from archive tip
Protected licensing/mapping diff:
unchanged
base remains ancestor of tested HEAD
```
- Initial lookup incorrectly guessed `refs/remotes/archive/main` and returned unknown revision; corrected using actual `git show-ref` inventory above. This was a tester lookup error, not a product failure.
- Historical changelog entries remain below the new 4.0.0 retirement entry; provenance explicitly distinguishes current offering from imported 3.27.0 history.

## 7. UI flow — Current offering
- How I tried it: read the current multilingual listing, then executed the source loader (shared commands).
- What came back: fourteen named retained skills; no offered removed skill. Source-level result only.

## 8. UI flow — Retained operation
- How I tried it: selected the daily, research, defuddle, Markdown and diagram entries from actual registered output; inspected router routes and retained workflows; performed Markdown fixture write/read and direct Canvas validation in row 3.
- What came back: each corresponding entry loaded with nonempty description and instructions; basic note and Canvas operations passed. External web/research services and live host dispatch were not executed.

## 9. UI flow — Removed operation
- How I tried it: attempted lookup through actual source registration list and verified all nine names absent with inventory tests.
- What came back: none of the nine entries can be selected from that list. Host-owned missing-skill wording was not tested or promised.

## 10. UI flow — Existing output
- How I tried it: opened existing-style Markdown in the disposable copy; inspected complete source-change scope and preservation policy, as row 5.
- What came back: existing Markdown remains directly readable; no migration/deletion step is introduced. Real pre-existing wiki/news/story files were deliberately not touched. This verdict is about the removal's source effect, not a live vault rendering claim.

## 11. UI flow — Historical documentation
- How I tried it: read new and old changelog sections, provenance and archive mapping; executed row 6 reachability checks.
- What came back: prior functionality remains readable as historical text; current offering explicitly says removed; all 131 mapped imported commits remain reachable.

## Findings and close-out metadata

- No product findings from these bounded checks. No important-or-worse dismissed findings were supplied.
- No user-instructed skips; plan and intent contain no skipped-by-instruction records.
- Source version decisions: plugin 4.0.0, separate OpenCode package 0.1.0. Installed refresh, merge and live host validation are outside this run.
- Git-memory classification: routine witness-report commit; no new non-obvious product decision, surprising constraint or durable gotcha. No memory trailers earned.
- Privacy gate: exact final commit message is scanned before commit; it contains no private-party identifiers, so the conditional semantic judge is not required.
