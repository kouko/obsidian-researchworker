# 美股研究入口改名
originator: kouko
kind: engineering
needs-design: no — 入口改名及 Python 執行指引沿用現有研究行為
status: confirmed 2026-11-23
intent_confirmed_sha: 3bbb5fd

## Problem

美股研究入口的名稱沒有顯示適用市場。技能指引也未寫明優先使用的 Python 執行工具。

## Proposed outcome

將美股研究入口定名為 equity-research-us，補充 uv 和 uvx 執行指引。

## Acceptance

1. 隔離安裝可找到新入口，SEC 擷取程式可從新路徑啟動。
2. 套件、其他技能、文件與測試使用新名稱。

## Constraints

- 既有研究筆記原地保留。

## Out of scope

- 修改 SEC 擷取、分析或季度研究儲存行為。

## Open questions

- none
