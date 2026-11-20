# 延伸研究：Agent 如何接續已保存的研究

整理日期：2026-11-20。這份筆記彙整已查閱的公開來源，對照專案研究 skill，並記錄後續行為測試的由來。

## 問題

當 Agent 為既有專案納入新資料，哪些做法能讓研究持續累積，並讓使用者查回判斷的依據？

## 來源與適用性

| 來源 | 原文觀點 | 對本專案的推論 |
|---|---|---|
| Nick Milo 的 Obsidian 影片 | 建立新筆記前先搜尋既有筆記，有相關內容時可接著補寫。 [原影片 5:57](https://www.youtube.com/watch?v=WB-yLc_ALZw&t=357s) | 更新前先找原先的判斷與來源，確認新增內容實際補充了什麼。 |
| Obsidian 社群 | 使用入口筆記組織相關內容。Vaultkeeper AI 的論壇討論另記錄使用者要求查閱和還原 Agent 的修改，開發者回報了檔案歷史功能。 [入口筆記討論](https://forum.obsidian.md/t/on-the-process-of-making-mocs/1060) · [編輯歷史討論](https://forum.obsidian.md/t/new-plugin-vaultkeeper-ai-claude-gemini-openai-mistal-and-local/115940) | 入口頁可指向目前答案。歷史報告需要連到當時採用的證據版本，讓讀者能重建判斷。 |
| 個人知識管理 | Andy Matuschak 描述可持續修訂的常青筆記，以概念累積內容，靠回讀與連結釐清想法之間的關係。 [Evergreen notes](https://notes.andymatuschak.org/z5E5QawiXCMbtNtupvxeoEX?stackedNotes=zF8xCU4BwXwbmSyp7tmff9i&stackedNotes=zNUaiGAXp21eorsER1Jm9yU) | 研究連結應指出新資料影響哪條主張，以及它提供的是佐證、適用條件或反證。 |
| 學術研究方法 | Cochrane 手冊區分新增資料對結論無影響、提高既有結論的確定程度，以及改變結論。更新後的報告應整合全體證據。 [更新手冊](https://www.cochrane.org/authors/handbooks-and-manuals/handbook/current/chapter-iv) | 結論維持原樣時，仍要辨認新資料是否真的提高信心，並交代新舊資料的可比性。 |
| 研究中使用 AI | Cochrane 等四個研究組織的聯合聲明要求人類監督，並透明報告 AI 所做或建議的判斷。 [聯合聲明](https://journals.sagepub.com/doi/10.1002/cl2.70074) | 確認每輪範圍之後，輸出還需要讓使用者查到 Agent 據以調整判斷的具體段落或圖表。 |

## 與現行 skill 的關係

現行 skill 允許首輪只保留入口與有日期的報告。後續先核對來源版本與既有判斷，再決定補充、改寫或略過，也要求讓歷史報告可追到採用過的來源版本。 [專案研究 skill](../../../obsidian/skills/obsidian-research-project/SKILL.md)

最值得測的情境是「核心答案相同，證據強度不同」。同一批資料被另一篇文章轉述時，來源數雖然增加，證據仍來自同一批資料。另一批資料可能提供額外支持，支持程度取決於它回答的問題、樣本和指標。兩次隔離測試觀察到 Agent 有辨別這兩種情況，複核也發現 B 漏引較直接的圖表，且在沒有新增後續工作的情況下改了入口。信心提高時應如何記錄日期與理由，仍待釐清。 [行為測試與限制](report.md)

這些來源提供設計依據。社群貼文反映個別實踐，Cochrane 規範適用於證據綜合，兩案的執行結果限於本次測試設定。
