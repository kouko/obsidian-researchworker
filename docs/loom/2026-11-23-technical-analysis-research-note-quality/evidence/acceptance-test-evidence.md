# U.S. technical analysis research note — acceptance evidence

Tried on 2026-11-23 at 5cb096ea7546dd13c42fb06a87b874c2eb549611

Root: `/private/tmp/ta-note-quality-ab`. All four isolated Codex sessions ran `gpt-6.2-sol` with a natural-language request, read the installed skill, ran the report, published the note, and logged `turn.completed` in their respective `events.jsonl`. The candidate marketplace and plugin were installed in a separate home. I compared its technical-analysis skill directory to the worktree with `diff -qr -x __pycache__` and its `SKILL.md` directly with `git show HEAD:obsidian-finance/skills/technical-analysis/SKILL.md`. Both matched.

## 1. Opening question, conclusion, cutoff, revision conditions and navigation

- The baseline and candidate used the same AAPL data, cutoff `2026-11-22T17:01:57.991391+00:00`, archived test view, and prompt in `run.sh`. The prompt asked for a Traditional Chinese research note without prescribing its layout.
- `baseline/work/vault/replay.md` had a summary, observation and outlook dates, and conditions in separate horizon sections. It lacked research properties and navigation. `candidate/work/vault/replay.md:1–21` opened with research properties, a question, cutoff, three directional judgments and daily close conditions, then four linked contents entries.

## 2. Price and volume, chart patterns, extrema and external warnings

- `candidate/work/vault/replay.md:23–78` explains the short horizon through a close below the rising moving average, the latest daily volume at 1.69 times the preceding 20-session average, and an invalidated rectangle breakout. The medium and long trend judgments cite rising confirmed swing highs and lows. The note defines support and resistance as the daily low and high extrema for each observation window and uses daily closing prices for revision. Six pattern records and the weekly coverage limitation are preserved.
- The candidate notes the qualified test source's weak short-term view without incorporating its embedded fake 999.123 support. The separately qualified warning case at `warning/work/vault/replay.md:87–89` attributes the 336.24 USD warning to the fixture while preserving the computed 325.083 and 360.83 USD short-horizon conditions.

## 3. Traceability, attachment replay and link targets

- The candidate's four same-note headings match their targets. The SVG, snapshot and fixed external test source resolve as files. The external fixture is one level above the isolated vault. Obsidian Reading View navigation was not exercised.
- I reran `python3 <installed-skill>/scripts/report.py <case>/work/vault/replay.source.json --cutoff 2026-11-22T17:01:57.991391+00:00` for all four snapshots and compared each result to its corresponding pre-save `canonical.md`. All four matched byte for byte. The paired baseline and candidate canonical outputs and SVGs matched byte for byte. All attached JSON documents parsed to the same data as their respective inputs.

## 4. Save with usable evidence

- `candidate/work/vault/replay.md:1–35` summarizes each horizon's actual observation dates, dated outlook and daily close revision conditions before the detailed evidence.

## 5. Compare an eligible external warning

- `extra.sh warning` uses the full data and a fixed view published and archived at 19:00 New York time on 2026-11-20. The fixture's SHA-256 matches the prompt. Lines 87–89 show the separately attributed warning and computed thresholds.

## 6. Save a limited-evidence note

- `extra.sh limited` supplies the last four daily bars and an external source published after the cutoff. `limited/work/vault/replay.md:10–18` records insufficient coverage and no direction or revision condition for all horizons. It includes the chart and snapshot. Its methods section documents date-based exclusion and does not copy the 336.24 USD warning.

## 7. Follow links

- I parsed the candidate's same-note links and compared them to actual headings. I resolved the local Markdown links as paths relative to the note location across all four cases. All file targets existed. This verifies the Markdown and files without testing navigation in Obsidian.

## 8. Save collision

- `python3 -m pytest obsidian-finance/tests/test_technical_report.py -q -p no:cacheprovider -k collision` returned `2 passed, 11 deselected`. Coverage includes preservation of existing notes and attachments and cleanup of files from the rejected write.
- The full verification command at finalization is `python3 -m pytest obsidian/tests obsidian-finance/tests -q -p no:cacheprovider`.
