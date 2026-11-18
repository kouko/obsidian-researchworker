# 讓「目前開著的筆記庫」判定在無 plutil 平台可用 — 我試了什麼、結果如何

Tried on 2026-11-16, in a clean copy of the project at 102e908 (102e908ed2cb1724325a8335c481756220681b73). How I tried each line and what came back: `docs/loom/2026-11-16-open-vault-check-portability/evidence/acceptance-test-evidence.md`.

## What you asked for, one line at a time

| # | What you asked for | Verdict | What happened | Re-run |
|---|---|---|---|---|
| 1 | 在無 plutil 的環境（CI 的 ubuntu 條件）重跑 `python3 -m pytest obsidian/tests -q -p no:cacheprovider`：73 項全數通過，三個 CLI 分支測試不再失敗。 | works | 我把 plutil 從可執行路徑裡拿掉（確認它真的找不到，其餘工具都在），整套測試全數通過：75 項、零失敗，那三個依賴 CLI 分支的測試也在裡面且通過。 | — |
| 2 | macOS 行為不變：有 plutil 時同一套件 73 項通過；registry 標記 open 時 CLI 分支照舊被採用，app 關閉或 vault 不符時照舊走 grep 後備。 | works | 有 plutil 時整套測試同樣全數通過（75 項）；用暫存筆記庫與假 CLI 實測三種情況都照舊：筆記庫標成開著就走 CLI、沒有開著標記就走 grep 且 CLI 沒被叫、開著但路徑值含換行就退回 grep 且 CLI 沒被叫。 | — |
| 3 | 修復範圍最小且可稽：只改 `vault.sh` 的 open 判定（含 reviewer-b 指出的同一行 lossy `$( )` 讀取）與對應測試；PR #5 其餘已審查功能內容逐檔不變。 | works | 與 PR #5 相比只動了兩支程式檔（腳本與測試）；腳本裡只有「開著的筆記庫怎麼讀」那一段和新加的一個小幫手，其餘函式與搜尋的接受閘逐字相同；PR #5 的功能內容原樣帶過來。 | — |
| 4 | 新 PR 的 required CI 全綠；PR #5 關閉並留下被取代的說明；main 不出現紅燈。 | not verified | 這要在發布之後才看得到：CI 在 GitHub 的機器上跑、PR #5 的關閉與 main 的燈號都是發布後的事件，這台機器上無從驗證。我沒有宣稱它們成立，也不知道現在是不是綠的。 | — |

## 對你既有的資料做了什麼 (what this did to data you already had)

Nothing — it only touched files this change created. 這次只動了一支唯讀的搜尋腳本和它的測試；所有測試都用暫存資料夾裡自己造的假筆記庫與假設定檔，沒有讀或寫你真正的筆記庫、真正的 Obsidian 設定，也沒有碰執行中的 Obsidian。這個修復本身不新增任何寫入動作。

## I decided for you

- **怎麼模擬「沒有 plutil 的機器」** — 我沒有用最精簡的 PATH，而是拿你平常的 PATH、只把 `/usr/bin` 那一格換成一個少了 plutil 的替代資料夾，因為最精簡的 PATH 會連 node 和你的 python 一起弄丟，測出來的紅燈會是「工具不見」而不是「plutil 不見」。改天要在真正的 Linux 上驗證，還是得靠 CI 那一輪。
- **「73 項」與實際 75 項的落差** — 我照你驗收條件裡的指令跑，沒有改動期望值；套件現在是 75 項，因為這次修復自己加了兩個測試。我說的是「全數通過」（75 項），不是「恰好 73 項」；如果你要的是字面上 73 這個數字，那是驗收條件寫定時套件還只有 73 項，不是有測試被漏掉。

## Steps you told me to skip

Nothing — no step was skipped.

## Things I am not sure you want

- 第 4 條（CI 全綠、PR #5 關閉、main 不紅）是真的只能等發布後才看得到；要不要在發布後補一輪，把 CI 的執行結果與 PR #5 的關閉說明貼回這份報告，讓它從「未能驗證」變成「已確認」？
- 驗收條件寫的是 73 項，實際是 75 項（多的兩個是這次為防回歸而加的測試）。這只是筆數對不上，不是有東西沒過；要維持文字原樣，還是把驗收條件的數字更新成 75？
