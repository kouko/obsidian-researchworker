# Mermaid Visualizer

[English](README.md) | [日本語](README.ja.md) | **繁體中文**

將文字內容轉換為 **30 種類型**的 Mermaid 圖表 — 主要針對 Obsidian 1.15 原生渲染（Pele 引擎，Mermaid 12.1.0 語法）最佳化，輸出為標準 Mermaid 語法，亦可用於其他渲染器（GitHub、GitLab、Mermaid Live Editor、Notion、Confluence、HackMD、Docusaurus、MkDocs 等）。

## Why Obsidian-first?

本 skill 為 Obsidian 筆記設計。自 Obsidian 1.15 起，Mermaid 區塊改由 Obsidian 自製的 **Pele** 引擎渲染，不再使用 Mermaid.js。所有 syntax 與 quirk 皆以 Pele 1.13.0（Obsidian 1.15.1 內建）校準；無法繞過的引擎限制（theme、icon、HTML 標籤、數學式）皆已列出，skill 會提醒使用者而不是硬繞。不再支援 1.15 之前的 Obsidian。

## What this skill does

產生可在 Obsidian 1.15 正確渲染的 Mermaid 圖表，涵蓋：

- **Flow & conceptual**（11）：flowchart / circular flow / comparison / mindmap / sequence / state / swimlane / kanban / user journey / ishikawa / use case
- **Data visualization**（7）：xychart / pie / quadrant / radar / sankey / treemap / venn
- **Structural**（10）：architecture / block / class / ER / C4 / gitgraph / tree view / wardley map / packet / requirement
- **Time**（2）：gantt / timeline

每種類型在 `flow/`、`data-viz/`、`structural/`、`time/` 下皆有專屬參考檔，內含 canonical syntax、設定選項、Obsidian 1.15 相容性註記、實作範例與每類型的錯誤防範。

## Obsidian 1.15 compatibility

- 各類型狀態與引擎限制：[`obsidian-compatibility.md`](obsidian-compatibility.md)
- 跨類型 quirk，包含舊渲染器會壞、Pele 已能正常渲染的寫法（`1. ` 標籤、未加引號的 CJK 標籤、`\n` 換行）：[`obsidian-common-quirks.md`](obsidian-common-quirks.md)

## Validation

```bash
scripts/validate.sh path/to/note.md
```

以 Pele 1.13.0 渲染筆記中每個 ` ```mermaid ` 區塊，逐塊回報 `PASS` / `FAIL`。需要 `node`；首次執行會把固定版本的 Pele 安裝到 `~/.cache/obsidian-mermaid-visualizer/pele-1.13.0`。

## Directory structure

```
obsidian-mermaid-visualizer/
├── SKILL.md                          # Router + Selection Tree + know-how
├── obsidian-common-quirks.md         # 跨類型規則（仍會壞的與已修好的寫法）
├── obsidian-compatibility.md         # 30 類型相容性矩陣 + 引擎限制
├── flow/                             # 11 個 flow/conceptual 類型檔
├── data-viz/                         # 7 個 data-viz 類型檔
├── structural/                       # 10 個 structural 類型檔
├── time/                             # 2 個 time-viz 類型檔
├── scripts/                          # validate.sh（Pele 驗證器）
├── README.md
└── LICENSE
```

此結構**刻意偏離**其他 `obsidian/skills/*` 使用的 `references/` 慣例。理由：30 個 per-type 檔案是本 skill 主要的 routed 內容，而非輔助參考資料。依 Anthropic「references 保持一層深度」的指引採單層 router（SKILL.md → 類型檔）。

## Original Source

- **Author**：[axtonliu](https://github.com/axtonliu)
- **Repository**：[axtonliu/axton-obsidian-visual-skills](https://github.com/axtonliu/axton-obsidian-visual-skills)
- **Plugin**：`obsidian-visual-skills`
- **Marketplace**：`axton-obsidian-visual-skills`

## Version history

- **v3.0.0**（2026-11-23）— 改以 Obsidian 1.15（Pele 引擎）為目標。新增 13 種類型（swimlane、kanban、journey、ishikawa、use case、radar、sankey、treemap、venn、tree view、wardley、packet、requirement），共 30 種。驗證由 mermaid-cli 改為 `scripts/validate.sh`（Pele 1.13.0）。
- **v2.0.0**（2026-04-20）— 從 6 種擴充至 17 種圖表類型。新增 data-viz（xychart / pie / quadrant）、structural（architecture / block / class / ER / C4 / gitgraph）與 time-viz（gantt / timeline）類別。重構為 per-type 檔案配單層 router。Architecture-icon fallback policy 已記錄。所有 syntax 校準至 Mermaid 11.4.1（Obsidian 內建版本）。經使用者驗證 named-line syntax 在 xychart 折線圖可正確渲染。
- **v1.x** — 由 axtonliu 製作的原始 6 類型版本
