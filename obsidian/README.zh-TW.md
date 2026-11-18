# obsidian

[English](README.md) | [日本語](README.ja.md) | **繁體中文**

> Obsidian vault workflow — daily note、markdown、Bases、圖表、Canvas、file intel、vault 管理、dashboard 設計，封裝為 Claude Code plugin。

## ⚠️ Cowork 相容性

本 plugin 大部分 skill 都與 Cowork 相容，唯獨 `defuddle` skill 例外 ——
它透過 subprocess 呼叫 [Defuddle CLI](https://github.com/kepano/defuddle)
抓取與清理外部 URL，會被 Cowork 的 sandbox URL allowlist 阻擋。
請在 Claude Code CLI 使用 `defuddle`。這些是上游的相容性說明；
獨立版本的 Claude/Cowork 相容性尚未驗證。[驗證紀錄](../docs/verification.md)
僅記載過去 Codex 本機來源安裝成功，實際使用仍未達成。

下表列出獨立版本的驗證狀態；上述 `defuddle` 限制來自上游，並非本版本的實測結果。

| Skill | Cowork | Claude Code CLI |
|---|---|---|
| `defuddle` | 未驗證；上游記載 URL 抓取受阻 | 未驗證 |
| 其他 obsidian skill | 未驗證 | 依個別 skill 證據；尚無全套驗證 |

## Version

4.2.0 — 參見 [`.claude-plugin/plugin.json`](.claude-plugin/plugin.json)。

初始化會預覽個人化的命名、筆記品質與現行 skill 規範，完整內容放在
`AGENTS.md`；`CLAUDE.md` 僅含 `@AGENTS.md` 與結尾換行。
既有規範會從兩份目前檔案合併，替換前先建立可還原的私人備份。
既有 memory 與本機 skill 保持原始位元組；缺少的附屬檔案須列入預覽並確認後
才建立。個人規範與備份只留本機。Codex 探索與 Claude 匯入是相容策略，
新工作階段的實際載入仍未驗證；不自動變更全域設定或安裝快取。
獨立版號的 OpenCode package 為 0.2.0。

## 獨立發行

從 [Monkey Skills](https://github.com/kouko/monkey-skills) 移轉至
[Obsidian ResearchWorker](../README.md) 獨立維護，保留 plugin 名稱 `obsidian`。
4.0.0 保留 14 個 skill，移除八個 wiki skill 與 daily-news-digest。
一般每日筆記、單題研究、Defuddle 擷取與雙括號內部連結仍保留；既有 vault
產出與設定不變。切換安裝前請先閱讀[過渡說明](../docs/migration.md)；
[驗證紀錄](../docs/verification.md)所載版本已在隔離環境完成 Codex 本機來源安裝，
但 skill 執行與筆記建立仍未達成；其他 host 與遠端安裝尚未驗證。
4.2.0 改名為 `obsidian-knowledge`，改用隨附的唯讀 shell script 搜尋（不再需要編輯器的 Grep/Glob；skill 數仍為 15）。

## 背景

Obsidian 是 local-first 的 markdown 知識庫。日常 vault 工作充滿小而重複的任務：
打開今天的 daily note、整理 inbox、撰寫合法的 Bases YAML、在 note 內畫
Mermaid 圖、把一整個 PDF 資料夾匯入成摘要 note，以及在 session 結束時
保存對話摘要。

本 plugin 把這些任務封裝為 skill，讓 Claude Code 依 intent dispatch。
Original skill 涵蓋 daily workflow、file intel、dashboard 設計、vault setup、
對話摘要。Imported skill 則涵蓋 Obsidian 專屬 markdown、Bases、Obsidian CLI、
Defuddle 網頁萃取、Canvas 建立、Excalidraw 圖與 Mermaid 圖。

## Router 與 agent

### Router

`using-obsidian` 是入口 skill，依使用者意圖（daily note、vault setup、
file processing、圖表、清理 vault）將請求 routing 至正確的 skill。

用 `/using-obsidian` 呼叫即可。

### Agent

`obsidian-vault-organizer` 是 vault 維運 agent，負責週期性的 hygiene 任務
（整理 `inbox/`、修復壞掉的 wikilink、正規化 frontmatter、標示重複候選、
統一 tag 命名）。**絕不刪檔** —— 僅 move 或 edit；目的地不明時會先確認。

## Skills

### Original skill（this project）

| Skill | 用途 |
|---|---|
| `using-obsidian` | Router —— 把 vault workflow 意圖 routing 至正確的 skill |
| `obsidian-daily` | 讀取或建立今日 daily note，整理 `inbox/`，列出今日 top 3 priority |
| `obsidian-vault-setup` | 互動式 vault 首次設定 —— 從自由文字回答推測 role 與 scope |
| `obsidian-tldr` | 把對話摘要寫入 vault，並更新 `memory.md` |
| `obsidian-research` | 上網研究指定主題（英文＋日文，主題有特定語言時再加該語言並以它為主），在 `research/` 產出附目錄的研究筆記 |
| `obsidian-knowledge` | 從任何 project 搜尋本機 vault（唯讀）；SessionStart hook 會告訴每個 session vault 在哪裡；不需 Grep/Glob |
| `obsidian-file-intel` | 透過 Gemini 從 PDF / PPTX / XLSX / DOCX / CSV / JSON 萃取內容並產出 Obsidian-ready 摘要 |
| `dashboard-design` | 依日本數位廳 dashboard 設計指引，從需求釐清引導到 layout |

### 引入自 kepano（Steph Ango）

Upstream：[`kepano/obsidian-skills`](https://github.com/kepano/obsidian-skills)
—— MIT, Copyright (c) 2026 Steph Ango。

| Skill | 用途 |
|---|---|
| `obsidian-markdown` | 撰寫 Obsidian Flavored Markdown —— wikilink、embed、callout、properties、註解 |
| `obsidian-bases` | 建立與編輯 `.base` 檔，含 view、filter、formula、summary |
| `obsidian-cli` | 透過官方 CLI 操作運行中的 Obsidian instance —— read / create / search / plugin 與 theme 開發 |
| `defuddle` | 透過 Defuddle CLI 擷取網頁內容與 YouTube 逐字稿 |

### 引入自 axtonliu（Axton Liu）

Upstream：[`axtonliu/axton-obsidian-visual-skills`](https://github.com/axtonliu/axton-obsidian-visual-skills)
—— MIT, Copyright (c) 2025 Axton Liu。

| Skill | 用途 |
|---|---|
| `obsidian-canvas` | 建立 Obsidian Canvas 檔，支援 MindMap 或 freeform layout，另提供四種社群版型（看板／儀表板（首頁）／研究地圖／moodboard）與範本、`.canvas` 輸出驗證腳本，以及零外掛的進階應用（巢狀畫布／研究雙畫布／資料管線文件化／稽核・事故檢討・onboarding 畫布／教師班級畫布／世界觀建構／Bases-in-canvas 1.9+／canvas-only／2D MOC）（整合 kepano 的 json-canvas） |
| `obsidian-excalidraw-diagram` | 產生 Excalidraw 圖（Obsidian / Standard / Animated 三種格式） |
| `obsidian-mermaid-visualizer` | 17 種 Mermaid 圖（flow / data-viz / structural / time）—— 為 Obsidian 11.4.1 優化，可移植到 GitHub / Notion / HackMD |

## Install

獨立版本的安裝實績僅有[驗證紀錄](../docs/verification.md)所載的過去隔離 Codex
本機來源安裝。遠端安裝、Claude/Cowork 相容性與實際使用尚未驗證。
變更既有安裝前請先閱讀[過渡說明](../docs/migration.md)。

`defuddle` skill 需要 Defuddle CLI：

```bash
npm install -g defuddle
```

`obsidian-cli` skill 需要官方 Obsidian CLI 與運行中的 Obsidian instance ——
參見 [help.obsidian.md/cli](https://help.obsidian.md/cli)。

`obsidian-file-intel` skill 需要 vault 內外部提供的相容腳本
`scripts/process_files_with_gemini.py` 與設定好的 Gemini API key。
本發行版未附帶該腳本，也未提供取得或設定程序。沒有既有相容腳本時無法使用
檔案處理；獨立版本的設定與執行仍未驗證。

`obsidian-knowledge` skill 從其他 project 讀取 vault。SessionStart hook
（`hooks/hooks.json`）在 session 開始時輸出 vault 路徑。搜尋使用隨附的 `skills/obsidian-knowledge/scripts/vault.sh`（POSIX sh；Obsidian 開著時用 CLI，否則用 BSD grep）——macOS 上不需要 Python，也不需要 Grep/Glob。若讀取 vault 跳出權限確認，
可在 `~/.claude/settings.json` → `permissions.allow` 加一行讀取規則
（例：`Read(~/Documents/MyVault/**)`）；skill 會顯示確切那一行，經你同意才加入。
隱私：skill 讀到的筆記內容會傳送給模型供應商。支援範圍：Claude Code 於 macOS
已驗證；Linux 未驗證；Windows 不支援。

## Usage

開始一天：

```
> Start my day
```

`using-obsidian` 會 routing 到 `obsidian-daily`，讀取或建立
`daily/YYYY-MM-DD.md`、列出 `inbox/` 內容，並提示 top 3 priority。

session 結束時保存對話摘要：

```
> Save a TLDR of this conversation
```

`using-obsidian` 會 routing 到 `obsidian-tldr`，把 markdown 摘要寫入
相關資料夾並更新 `memory.md`。

在 note 內畫圖：

```
> 幫我畫 OAuth device flow 的 Mermaid sequence diagram
```

`using-obsidian` 會 routing 到 `obsidian-mermaid-visualizer`，挑選
sequence diagram type、套用 Obsidian 11.4.1 的 quirk，輸出
` ```mermaid ` 區塊。

## Repository 結構

```
obsidian/
├── .claude-plugin/
│   └── plugin.json              # plugin metadata，version 4.2.0
├── agents/
│   └── obsidian-vault-organizer.md  # vault 維運 agent
├── hooks/                       # SessionStart vault pointer
├── skills/
│   ├── README.md                # 各 skill attribution 表
│   ├── using-obsidian/          # router（original）
│   ├── obsidian-daily/          # daily workflow（original）
│   ├── obsidian-vault-setup/    # vault 設定（original）
│   ├── obsidian-tldr/           # 對話摘要（original）
│   ├── obsidian-research/       # 單題研究 → vault 筆記（original）
│   ├── obsidian-knowledge/      # 唯讀 vault 搜尋（original）
│   ├── obsidian-file-intel/     # 檔案 → Obsidian 摘要（original）
│   ├── dashboard-design/        # dashboard 設計（original）
│   ├── obsidian-markdown/       # 引入自 kepano
│   ├── obsidian-bases/          # 引入自 kepano
│   ├── obsidian-cli/            # 引入自 kepano
│   ├── defuddle/                # 引入自 kepano
│   ├── obsidian-canvas/ # 引入自 axtonliu
│   ├── obsidian-excalidraw-diagram/ # 引入自 axtonliu
│   └── obsidian-mermaid-visualizer/ # 引入自 axtonliu
├── README.md
├── README.ja.md
└── README.zh-TW.md
```

各 skill 的 attribution 詳見 [`skills/README.md`](skills/README.md)；
整個 repo 的 attribution 詳見 [`../ATTRIBUTION.md`](../ATTRIBUTION.md)。

## 貢獻

- Bug 回報與功能建議：請至
  [github.com/kouko/obsidian-researchworker/issues](https://github.com/kouko/obsidian-researchworker/issues)
  開 issue。
- 歡迎 PR。請維持既有 skill 結構（frontmatter + workflow + reference 檔），
  並使用 Conventional Commits。
- 引入自上游的 skill：kepano / axtonliu 上游變更會持續流入；如修正屬於
  上游性質，建議同步開 upstream PR。

## License

MIT — 詳見 repository root 的 [LICENSE](../LICENSE)。

引入的 skill 在各 skill 的 `LICENSE` 檔保留原著作權聲明：

- `defuddle`、`obsidian-bases`、`obsidian-cli`、`obsidian-markdown` —— MIT,
  Copyright (c) 2026 Steph Ango。詳見各 skill 內的 `LICENSE`。
- `obsidian-canvas`、`obsidian-excalidraw-diagram`、
  `obsidian-mermaid-visualizer` —— MIT, Copyright (c) 2025 Axton Liu。
  詳見各 skill 內的 `LICENSE`。（`obsidian-canvas` 同時包含 kepano
  的 json-canvas integration。）

整個專案的 license 詳見 [LICENSE](../LICENSE)，
完整 third-party 元件對照表詳見 [ATTRIBUTION.md](../ATTRIBUTION.md)。
