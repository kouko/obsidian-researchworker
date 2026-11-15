# Retrieval check: direct vault search (W2-01, Acceptance 7)

Date: 2026-11-15

## Method

- Vault located with `obsidian/skills/obsidian-knowledge/scripts/vault.sh locate`; searched read-only via `vault.sh search`.
- Questions derived from recent note titles in `research/` and `projects/`, and from `ROADMAP.md` (YTSS/RLSS integration). Three questions are phrased in a different language or wording than the target note title; two target topics believed absent from the vault.
- Search as the skill prescribes: Obsidian CLI `search` when the app is running (primary, relevance-ranked), falling back to BSD `grep -rliF` (fixed strings, not regex) over `*.md` excluding `.obsidian/` and `.trash/`, keywords in zh/ja/en. "Hits" = number of matching files. "Found" = a clearly relevant note is identifiable in the hits (yes / partial / no). Paths are absolute; no note bodies copied.

## Results

| # | Question | Keywords used | Hits | Found | Top note | Note on miss / noise |
|---|---|---|---|---|---|---|
| 1 | How does loom handoff compare to ctx-handoff? | `ctx-handoff` | 2 | yes | `research/2026-10-15 ctx-handoff-mod 研究——長 session 自動交接與 loom handoff 對比.md` | — |
| 2 | What did I find about Claude Code mods and forms? | `Claude Code Mods`, `mods … 表單/form` | 18 | yes | `research/2026-10-12 Claude Code Mods 深度研究——實作、Desktop 與 CLI 差異、表單與帳密安全.md` | watch-later clips also match; research note is identifiable |
| 3 | How does pstack decide a task is complete? | `pstack` | 4 | yes | `research/2026-10-27 pstack 深度研究——架構、完成判定機制與貼文說法查證.md` | — |
| 4 | What is a "software factory" and which frameworks exist? | `軟體工廠`, `software factor`, `ソフトウェアファクトリー` | 75 | yes | `research/2026-10-13 軟體工廠深度研究——概念、運作架構、業界態度與實作框架評估.md` | high noise; title-in-filename made it findable |
| 5 | (en wording) What do vendors say about conflicting instructions in prompts? | en only: `conflicting instruction`, `contradictory instruction` | 0 | no | — | **language**: note is zh (`矛盾`); succeeded only after adding zh keyword (14 hits, `research/2026-09-16 提示詞指示的矛盾、重複與過強語氣….md`) |
| 6 | (en wording) What inclusion criteria should a knowledge base use? | en only: `inclusion criteria` | 0 | no | — | **language + synonym**: note uses `收料` / `判準`; zh keyword `收料` finds `research/2026-09-22 知識庫該收什麼料….md` (4 hits) |
| 7 | (ja wording) テーブルの書き方のルールは? | `テーブルの書き方`, `表の書き方`, `table writing`, `表格.*(慣例\|規則)` | 13 | yes | `research/2026-09-16 表格在軟體／設計／商業產業中的使用慣例與寫作規則.md` | found only via the zh pattern; ja phrasing alone does not match |
| 8 | What do I have on YTSS / RLSS (ROADMAP §2)? | `YTSS`, `RLSS`, then `reading.?list` | 32 / 674 | partial | `projects/reading-list-summarize-scraper/2026-03-29 Chrome Reading List LevelDB 直讀技術實作筆記.md` | **concept not literal**: acronyms appear incidentally; expansion `reading list` floods with the `reading_list/` folder (674) |
| 9 | (absent) Kubernetes HPA autoscaling tuning | `Kubernetes`, `HPA autoscal`, `オートスケール` | 91 | no (correct) | — | **false-positive noise**: passing mentions in unrelated notes; no relevant note exists |
| 10 | (absent) Sourdough starter maintenance | `sourdough`, `酸種`, `天然酵母` | 2 | no (correct) | — | incidental matches (pizza video, image generator) |

Supplementary: "how to resume an interrupted long session" (`長 session`, `長いセッション`, `context exhaustion`) → 11 hits, Q1's note found (synonym bridged only because the zh title literally contains `長 session`).

## Summary counts

- Answerable questions (1-8): found 4 on first keyword set (1, 2, 3, 4) + 1 via mixed-language pattern (7) = 5 yes; 1 partial (8); 2 missed on the stated wording (5, 6), each recovered only by adding a zh keyword.
- Absent topics (9, 10): correctly no relevant note, but with 91 and 2 noisy hits.
- Totals: found 5, partial 1, missed 2 (+2 correct negatives).

## Observed failure classes

1. **Language mismatch** — notes are mostly Traditional Chinese; en/ja wording misses unless the searcher translates keywords (Q5, Q6, Q7).
2. **Synonym / vocabulary** — the note's own term (`收料`, `判準`) differs from natural query terms (Q6).
3. **Concept not literal** — project acronyms (YTSS/RLSS) are not used in note text; expansions collide with a folder name (Q8).
4. **Noise on common terms** — broad terms match passing mentions in many notes; ranking relies on filename titles (Q4, Q9).

## Conclusion

Direct search suffices when the question shares a literal, distinctive term with the note (tool or product names, and topics whose title is in the query language): 5 of 8 answerable questions succeeded, and both absent topics were correctly not found. The recurring gap is cross-language and synonym retrieval: questions phrased in English or Japanese against Chinese notes missed until the searcher supplied the Chinese term. That gap, not raw recall on literal names, is what would justify a later semantic or multilingual index; the skill's existing instruction to search zh/ja/en keywords mitigates it only when the searcher guesses the note's vocabulary.
