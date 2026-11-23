# 讓 Mermaid 圖表技能符合新版 Obsidian 的繪圖引擎
originator: kouko
kind: product
needs-design: yes — 技能產出的圖表語法與寫作規則會改變，現有規格只涵蓋舊版引擎
evidence: ["/Users/kouko/kouko-obsidian-vault/research/2026-11-23 Obsidian 新版 Mermaid 與 Pele：功能變化、折線標籤與 K 線支援.md"]
status: confirmed 2026-11-23
intent_confirmed_sha: f5c3a05
publication: automatic — authorized 2026-11-23 by kouko

## Problem

新版 Obsidian（1.15 起）換掉了原本的 Mermaid 繪圖程式，改用自家的新引擎。現在的圖表技能仍照舊版規則寫圖：

- 一部分避坑規則已不需要，讓圖寫得比必要更繞；
- 另一部分舊問題仍在，加上新引擎自己的新限制（例如主題設定被忽略、圖示顯示成空框、圖內連結不進反向連結），技能沒有提醒；
- 新引擎支援的多種新圖表類型，技能完全不會用；
- 技能附帶的自我檢查用的是舊版繪圖程式，檢查通過的圖在 Obsidian 裡仍可能壞掉，反之亦然。

結果是使用者在筆記裡請 Claude 畫圖時，可能拿到在 Obsidian 顯示錯誤、或錯過更合適圖表類型的結果，只能自己手動修。

## Proposed outcome

圖表技能以新版 Obsidian 實際行為為準：保留仍有效的避坑規則、移除已失效的、補上新引擎特有的限制，能選用新支援的圖表類型，且附帶的自我檢查與 Obsidian 實際顯示結果一致。

## Acceptance

1. 本次研究在 Obsidian 實機或新引擎上確認「仍會出錯」的每一種寫法，技能都會指示避開；確認「已修好」的寫法，技能不再當成禁止事項。
2. 技能說明的支援版本與限制，與新版 Obsidian（1.15）一致，不再宣稱以舊版 Mermaid 為準。
3. 對研究中確認可正常顯示的新圖表類型，技能至少能產出一張可在 Obsidian 正確顯示的範例。
4. 技能的自我檢查對一組「新引擎會報錯」與「新引擎可正常顯示」的樣本，判定結果與新引擎一致。
5. 其他引用這個技能的技能、說明文件與測試仍一致可用，套件測試全數通過。

## Constraints

- 以 Obsidian 1.15 內建的新引擎行為為準；與官方 Mermaid 不同時，以 Obsidian 為準。
- 保留技能名稱與入口，現有使用方式不變（AGENTS.md 規則 4）。
- 不改動使用者 Vault 內既有筆記。

## Value case

- 受益者：在 Obsidian 筆記中請 Claude 畫圖的使用者（kouko）。
- 急迫性：Obsidian 1.15 已於 2026-11-02 發布，使用者已在 1.15.1。
- 現有替代：手動修圖，或照舊規則寫保守的圖。
- 排擠的工作：無明顯排擠。
- GO — 新引擎已上線，舊規則與實際行為的落差已實測確認。

## Out of scope

- 舊版 Obsidian（1.14 以前）的相容寫法。
- 其他 Mermaid 顯示環境（GitHub、網頁等）的專屬調整。
- 為 Obsidian 補上新引擎缺少的功能（如圖示來源、數學式）。
- K 線圖等新引擎本身不支援的圖表。

## Open questions
- none
