# Taiwan quarterly equity research acceptance progress

## Source acquisition

The planned cohort is TSMC (2330), Hon Hai (2317) and China Electric (1611), 2025 Q1–Q3. The initial acquisition preflight obtained all nine original quarterly PDFs. It did not establish quarterly completion.

- TSMC: nine monthly observations were bound to dated issuer releases in the [TSMC newsroom archive](https://pr.tsmc.com/chinese/news-archives). The first preflight returned disclosure records, while later cutoff replays returned a disconnected MOPS query. These results must not be treated as equivalent to a successful search with no relevant announcements.
- Hon Hai: nine monthly observations were bound to dated [issuer releases](https://www.foxconn.com/zh-tw/investor-relations/financial-information/reports?category=monthly&year=2025). The June 15 replay for Q2 admitted April and May, with June and the quarterly filing excluded. Later runs retained all three filed PDFs; the material-disclosure query failed.
- China Electric: the [issuer monthly table](https://www.chinaelectric.com.tw/investor.php) shows the amounts but did not establish original publication dates or versions. The TWSE monthly table showed later generation dates. A later capture therefore cannot act as contemporaneous evidence in the 2025 replay.
- China Electric annual correction: the TWSE filing index returned the original FY2024 annual report on May 7, 2025 at 16:21:54 Taipei time and the corrected one on August 8, 2025 at 13:39:57. This is actual source evidence for a future before/after note comparison.

## Conference recording

The [TWSE China Electric recording](https://www.youtube.com/watch?v=bMWy8nvERVY) was acquired through the conference tool at a November 30, 2025 research cutoff. No usable captions were found. Local Whisper produced 190 timestamped segments from 581 seconds of audio. The tool retained the recording URL, source date, normalized audio hash and derived SRT hash. This verifies acquisition and fallback, rather than an entire quarterly report.

## Isolated notebook publication

An isolated vault was used to follow the Taiwan skill instructions and call the normal quarterly publication helper on TSMC 2025 Q1, Q2 before filing, Q2 after filing, and Q3. All four saved revenue-evidence units passed portable verification and were rediscovered as reusable. The second Q2 save used the same report paths and retained the dated prior report. The two quarter transitions retained prior-quarter links. The official quarterly PDF revenue was NT$839,253,664 thousand, NT$933,791,869 thousand and NT$989,918,318 thousand respectively (appendix pages 30, 31 and 31). There was no independently authored prior forecast in this test. The MOPS query disconnected, so all reports remained partial.

A separate Hon Hai vault followed the same four checkpoints. All four passed portable verification and rediscovery. Q2 reused the same paths and retained its dated changes, and Q2 and Q3 retained prior-quarter links. Filed revenue was NT$1,644,315,563 thousand, NT$1,793,468,046 thousand and NT$2,058,949,127 thousand (PDF pages 7, 8 and 7). The quarters were partial because material-disclosure and full analytical work were outstanding.

China Electric ran in a separate Codex CLI 0.171.0 profile with the local marketplace and obsidian-finance installed. The fresh session selected the installed Taiwan skill. Its cached entry, acquisition, conference, workflow and store files matched commit `20d21cb` byte for byte. The session saved three partial checkpoints (June 3, August 31 and November 30, 2025 Taipei cutoff days), each verified with the portable helper and rediscovered. Preliminary forecast conditions written during replay can exercise continuation but do not establish that an analyst published those conditions in 2025. This host check preceded the mixed-scope repair.

## Unverified

Nine complete quarterly research cases and six end-to-end continuations using the final packaged skill remain unverified. All nine quarters have partial publications across the isolated runs. Full-period disclosure retrieval and dated monthly source versions for China Electric remain open. A repeat request to the official disclosure endpoint returned RemoteDisconnected. Controlled tests cannot substitute for completed issuer-quarter acceptance.

## Automated verification

Commit `337fb19`: the full package suite passed (479 tests). The independent mixed-scope probe failed on both cases before the repair and passed both after the repair. The repair suppresses a monthly total when scopes are mixed or unknown and a filed-versus-monthly difference when scopes do not match.
