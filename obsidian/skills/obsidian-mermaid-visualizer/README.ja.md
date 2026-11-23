# Mermaid Visualizer

[English](README.md) | **日本語** | [繁體中文](README.zh-TW.md)

テキストコンテンツを **30 種類**の Mermaid 図に変換します — 主に Obsidian 1.15 のネイティブ render（Pele エンジン、Mermaid 12.1.0 syntax）向けに最適化していますが、出力は標準 Mermaid syntax なので他の renderer（GitHub、GitLab、Mermaid Live Editor、Notion、Confluence、HackMD、Docusaurus、MkDocs 等）でも使えます。

## Why Obsidian-first?

この skill は Obsidian ノート向けに設計されています。Obsidian 1.15 以降、Mermaid ブロックは Mermaid.js ではなく Obsidian 自社製の **Pele** エンジンで render されます。syntax と quirk は Pele 1.13.0（Obsidian 1.15.1 同梱）に合わせて調整しており、回避策のないエンジン制約（theme、icon、HTML ラベル、数式）は一覧化して、無理に回避せずユーザーに伝えます。1.15 より前の Obsidian はターゲット外です。

## What this skill does

Obsidian 1.15 で正しく render される Mermaid 図を生成し、以下をカバーします：

- **Flow & conceptual**（11）: flowchart / circular flow / comparison / mindmap / sequence / state / swimlane / kanban / user journey / ishikawa / use case
- **Data visualization**（7）: xychart / pie / quadrant / radar / sankey / treemap / venn
- **Structural**（10）: architecture / block / class / ER / C4 / gitgraph / tree view / wardley map / packet / requirement
- **Time**（2）: gantt / timeline

各タイプには `flow/`、`data-viz/`、`structural/`、`time/` 配下に専用 reference ファイルがあり、canonical syntax、設定オプション、Obsidian 1.15 互換性ノート、実例、タイプ別エラー予防策が含まれます。

## Obsidian 1.15 compatibility

- タイプ別の状態とエンジン制約: [`obsidian-compatibility.md`](obsidian-compatibility.md)
- タイプ横断の quirk（旧 renderer では壊れたが Pele では render される書き方 — `1. ` ラベル、引用符なし CJK ラベル、`\n` 改行 — を含む）: [`obsidian-common-quirks.md`](obsidian-common-quirks.md)

## Validation

```bash
scripts/validate.sh path/to/note.md
```

ノート内の各 ` ```mermaid ` ブロックを Pele 1.13.0 で render し、ブロックごとに `PASS` / `FAIL` を報告します。`node` が必要で、初回実行時に固定バージョンの Pele を `~/.cache/obsidian-mermaid-visualizer/pele-1.13.0` にインストールします。

## Directory structure

```
obsidian-mermaid-visualizer/
├── SKILL.md                          # Router + Selection Tree + know-how
├── obsidian-common-quirks.md         # タイプ横断ルール（まだ壊れる書き方と修正済みの書き方）
├── obsidian-compatibility.md         # 30 タイプ互換マトリクス + エンジン制約
├── flow/                             # 11 個の flow/conceptual タイプファイル
├── data-viz/                         # 7 個の data-viz タイプファイル
├── structural/                       # 10 個の structural タイプファイル
├── time/                             # 2 個の time-viz タイプファイル
├── scripts/                          # validate.sh（Pele validator）
├── README.md
└── LICENSE
```

この構造は他の `obsidian/skills/*` で採用されている `references/` の慣例から**意図的に逸脱**しています。理由: 30 個のタイプ別ファイルは補助 reference ではなく、この skill のメインの route 対象コンテンツだからです。Anthropic の「reference は one level deep に保つ」ガイドラインに従い、単層 router（SKILL.md → タイプファイル）を採用。

## Original Source

- **Author**: [axtonliu](https://github.com/axtonliu)
- **Repository**: [axtonliu/axton-obsidian-visual-skills](https://github.com/axtonliu/axton-obsidian-visual-skills)
- **Plugin**: `obsidian-visual-skills`
- **Marketplace**: `axton-obsidian-visual-skills`

## Version history

- **v3.0.0**（2026-11-23）— Obsidian 1.15（Pele エンジン）をターゲットに変更。13 タイプ（swimlane、kanban、journey、ishikawa、use case、radar、sankey、treemap、venn、tree view、wardley、packet、requirement）を追加し計 30 タイプ。検証を mermaid-cli から `scripts/validate.sh`（Pele 1.13.0）に変更。
- **v2.0.0**（2026-04-20）— 6 タイプから 17 タイプの図に拡張。data-viz（xychart / pie / quadrant）、structural（architecture / block / class / ER / C4 / gitgraph）、time-viz（gantt / timeline）の各カテゴリを追加。タイプ別ファイル + 単層 router 構造に再構成。Architecture-icon fallback policy をドキュメント化。すべての syntax を Mermaid 11.4.1（Obsidian バンドル版）に校正。Named-line syntax が xychart 折れ線グラフで正しく render されることをユーザー検証済み。
- **v1.x** — axtonliu によるオリジナル 6 タイプ版
