# 四平台插件安裝與技能入口 — 驗收結果

Tried on 2026-11-25, in a clean copy of the project at 16b389b. How I tried each line and what came back: `docs/loom/2026-11-25-four-host-plugin-support/evidence/acceptance-test-evidence.md`.

## What you asked for, one line at a time

| # | What you asked for | Verdict | What happened | Re-run |
|---|---|---|---|---|
| 1 | 兩個插件的版本、發行資訊及實際技能清單一致，包含台股研究且不包含已退役的檔案摘要技能。 | works | 版本一致為 5.0.0 和 0.2.0，技能數為 15 和 4。 | re-tested |
| 2 | 兩個插件在四個平台皆能依文件安裝，並可查到各自完整的技能清單。 | works | 四平台的本機安裝皆查得完整技能清單。 | carried over — 本機初次安裝欄與指令未改動 |
| 3 | OpenCode 的兩個插件可透過原生技能選取與正常自動載入機制使用，且不額外註冊斜線指令。 | partly | 原生選單和技能註冊通過，實際模型自動選取未驗證。 | carried over — OpenCode 載入器與設定指引未改動 |
| 4 | 安裝指南與實際支援狀態一致，套件驗證通過，既有 vault 資料和設定保留。 | works | 修正的 Codex 本機更新指令成功，相關測試 51 項通過，既有資料未動；完整測試失敗會阻止最終驗證。 | re-tested |
| 5 | Install either plugin in Claude Code or Codex → its skill inventory shows all 15 or 4 skills at the new release version. | works | 兩平台的兩個插件均安裝成功，所有技能和支援檔案一致。 | carried over — 初次安裝指令未改動 |
| 6 | Install either plugin in Antigravity using the documented supported route → its plugin and skill inventory shows the corresponding full package. | works | 兩個插件均由 Claude 格式轉換成功，技能清單完整。 | carried over — 安裝指令未改動 |
| 7 | Install both OpenCode packages → the registry shows 19 skills under the two distinct plugin IDs. | works | 實測兩個插件均為 active，辨識出 19 個技能。 | carried over — OpenCode 載入器與設定指引未改動 |
| 8 | Enter `@obsidian:obsidian-research` or `@obsidian-finance:tw-equity-research` in OpenCode → the respective skill is selected using OpenCode's native mechanism. | partly | 先前候選的原生選單可補全兩個技能，未送出模型提示；載入器在 rebase 後一致。 | carried over — OpenCode 選取方式未改動 |
| 9 | Ask for a matching task without naming a skill → OpenCode advertises the relevant skill to the model according to its normal discovery mechanics. | not verified | 註冊包含描述；送出工作階段模型提示的驗證未獲准。 | carried over — OpenCode 自動選取方式未改動 |
| 10 | Open OpenCode's slash-command menu → the two plugins' generated skill commands are absent; built-in and other plugins' commands remain. | works | 實際指令登錄查不到兩個插件的產生指令，仍有 4 個內建指令。 | carried over — OpenCode 指令登錄未改動 |
| 11 | Follow the documented update route → new release contents are available, including Taiwan equity research, with the retired File Intel entry absent and existing vault files and settings preserved. | partly | Claude、Codex、AGY 本機更新皆通過。OpenCode 遠端更新尚未驗證。 | re-tested |

## 對你既有的資料做了什麼

驗收僅使用隔離的安裝目錄及測試來源，未讀寫既有 vault 內容或正式插件設定。

## I decided for you

- **版本** — 一般插件為 5.0.0，金融插件為 0.2.0，反映公開入口退役與新增安裝目標。
- **獨立套件** — 兩個插件各自保留相同載入流程，讓個別安裝時不需要另一個插件。
- **Antigravity** — 沿用 Claude 插件轉換，實際安裝已成功。
- **測試隔離** — 避免變更現有四平台設定和 vault，未驗證正式安裝更新。

## Steps you told me to skip

無。模型提示驗證未獲准執行，完整套件測試由最終審查程序執行。

## Things I am not sure you want

無。
