# Finance analysis frameworks — acceptance test evidence

Tried on 2026-11-20 in a fresh local clone at `36ff45ed842949b1fe37d008db09d2a957f4ea08`. `git status --porcelain` returned no changes before testing. Used the README's folder-grounded research entry and Python 3.12 for its documented local helper. The fresh acceptance agent read the checked-out skill directly. No installed-host invocation, external request, credential access, or real vault was used.

## 1. 財務、營運、產業與競爭、估值與風險、技術分析、綜合分析各有獨立指引，說明研究問題、證據要求、比較或計算口徑與完成條件。

- How I tried it: Opened `obsidian-finance/skills/finance-research/SKILL.md` and resolved the six links under “Select the analysis framework” relative to the source skill. Opened each distinct target when doing its respective full-quarter task below.
- What came back: `financial-analysis.md`, `operating-analysis.md`, `industry-and-competition.md`, `valuation-and-risk.md`, `technical-analysis.md`, `synthesis.md` each opened and had distinct Research questions, Evidence, Analysis and Completion sections. Each linked back to the same `research-method.md`.

## 2. 驗證代理按工作需求載入對應指引。單面向更新不需讀完六份，綜合分析可沿用仍有效的面向成果。

- How I tried it: Followed the skill with the prompt “Review the fictional issuer's full Q2 as of 2024-08-08 16:15 New York time, using only the retained evidence and giving conditional short, medium and long conclusions. Then handle each subsequent update separately from the same initial case.” This is a bounded offline source-loaded task. The synthetic excerpts and resulting analysis are recorded below. For each prompt the listed dimension references are the ones that supplied the instructions; the shared method was also applied.
- Fixture: Original Q2 filing released August 5, income statement rows 4–6: revenue 120, operating profit 18 in millions USD, versus comparable 100 and 12 in the retained Q1 original; cash flow rows 3–6: CFO 24, capex 6 versus 18 and 5. MD&A paragraph 2 reports comparable unit volume up 12%, with a favorable mix and one large shipment. August 6 peer original, business paragraph 3, comparable volume +8% in the same region, with a different customer mix. Dated model worksheet August 7: normalized distributable cash 12–14 USD/share, required yield 10%, and scenario value under a quote-consuming capital-weight variant at a 12% yield. Fictional exchange session rows (USD/share, unadjusted, no corporate action): August 7 close 110; August 8 close 121, both available 16:05 New York time following 16:00 sessions. Same-window benchmark goes from 100 to 104, with same frequency/basis.
- What came back, full quarter: Began with financial, operating and industry references. Financial: operating margin 15% versus 12%, up 3 percentage points; cash after capex 18 versus 13 million, with working capital composition unverified. Operating: stronger volume and favorable mix are supported, durability limited by shipment timing. Industry: volume outgrew the comparable peer by 4 percentage points, with no market share inference from a single peer of different mix. Continued with valuation/risk: conditional capitalization range 120–140 USD/share at 10%; holding cash constant, the price-sensitive 12% calculation yields 100–116.67. The competing hypothesis is that the one-off shipment made normalized cash too high. Technical: close-to-close return +10%, 6 percentage points above benchmark's +4%; the 121 close sits inside the fixed-yield 120–140 range and above the separately labeled price-sensitive range. Two sessions cannot establish a durable trend. Synthesis: short horizon (0–3 months anchored August 8) records the price-sensitive result with reversal at a close below 110; medium (3–12 months) records conditional operating improvement, challenged by one-off shipment timing and invalidated if comparable unit growth normalizes below the peer; long (12–60 months) remains insufficient for an investment judgment pending further cash conversion and competitive evidence. These are analysis windows, separate from a holding preference.
- What came back, cases using the same baseline:
  - **Market-only, no benchmark** — prompt “Update the two-session issuer return only.” Used the technical reference alone among dimensions. Reported +10% from the two eligible closes with no benchmark-relative return and no unrelated dimension reopened.
  - **Quote-only with dependent analysis** — prompt “Replace only the August 8 quote with the eligible correction to 132 and update affected work.” Used valuation/risk, technical and synthesis. A separately supplied worksheet maps the changed quote to a 12.5% required yield, so the quote-dependent range becomes 96–112. The fixed-yield 120–140 remains valid. Price return becomes +20%, the benchmark-relative gap becomes 16 percentage points, and 132 remains within the fixed-yield range and above the price-dependent range. Financial, operating and competitive outputs were reused.
  - **Valuation-only** — prompt “Adopt only the revised comparable 100–115 valuation range with a verified new model input.” Used valuation/risk, technical and synthesis. Kept the baseline +10% and +6 percentage point spread and reused the three fundamental results. Reclassified baseline close 121 as above 100–115 and updated the price-sensitive synthesis.
  - **Standalone technical observation with missing valuation** — prompt “Keep the baseline quotes, but omit the required comparable valuation range.” Used the technical reference; attempted the comparison against the supplied inventory, marked the comparison pending, and retained both supported price signals. An investment judgment remains pending where it depends on the comparison.

## 3. 資訊截止、來源引用、缺資料處理與跨季沿用仍遵守共用規則。僅行情變動時，由受影響的分析決定重做範圍。

- How I tried it: Applied the historical cutoff from case 2 to two additional candidates: an August 8 session quote of 150 first published at 16:20 New York time, and a September 3 amendment containing a rewritten Q1 comparative. Also tested a quote-missing variant and advanced only the authored method version.
- What came back: Excluded both later releases, even though their observation periods were within the cutoff. Q1 used the retained Q1 original and the operating comparison retained the peer source and its different mix. The quote-missing variant kept the independent intrinsic range and left price return and price-relative valuation pending. A method authored in 2026 was recorded with actual authored date, with the 2024 economic cutoff unchanged. For all variants, eligible/reused observations kept their own dates and the passages above; missing series/market-value inputs did not replace existing quarterly results. The quote-only and valuation-only results in section 2 record the specific changes and preserved analyses.
- Evidence: Relevant instruction points are “Evidence and time identities”, “Original reading coverage” and “Completion and continuation” in `research-method.md`; the calculations and dispositions above are the direct acceptance-agent output. The existing cold multi-quarter and public adjacent-quarter tests below separately exercise saved version-1 evidence, including exclusion of future sources.

## 4. 既有季度筆記可繼續沿用，季度輸出可按內容分合。

- How I tried it: Ran these focused compatibility cases from the clean clone.

```sh
python3.12 -m pytest \
  obsidian-finance/tests/test_research_continuation.py::test_cold_multi_issuer_calendars_repeat_and_amendment \
  obsidian-finance/tests/test_research_continuation.py::test_public_pilot_adjacent_quarters_and_competition_cutoffs \
  obsidian-finance/tests/test_research_store.py::test_unsupported_folder_preserved \
  obsidian-finance/tests/test_research_store.py::test_local_analysis_dependencies_preserve_actual_authorship \
  obsidian-finance/tests/test_research_publication.py::test_completed_unit_reused_and_linked_provenance \
  -q -p no:cacheprovider
```

```text
...............                                                          [100%]
15 passed in 0.66s
```

- The tested checkpoint publishes and reuses an independent completed unit while its added synthesis question remains pending. The legacy-format case asserts every preexisting byte is preserved through publication.
- Also ran `PYTHONPATH=obsidian-finance/tests python3.12 <probe-path>` with the temporary probe below. The initial attempt used the default macOS temp location via the symlinked `/var` ancestor and the store rejected it as unsafe. Retried with the README's physical `/private/tmp` location.

```text
grouped=True output_count=1 publication=complete reused=['market', 'valuation'] original_bytes_unchanged=True
grouped=False output_count=2 publication=complete reused=['market', 'valuation'] original_bytes_unchanged=True
```

```python
import copy
import json
from pathlib import Path
from tempfile import TemporaryDirectory

from test_research_publication import proposal
from test_research_store import CUTOFF, load, put


def test_quarter_outputs_grouped_or_split_reusable():
    """Publish and rediscover both output layouts with a version-1 predecessor."""
    for grouped in (True, False):
        with TemporaryDirectory(dir="/private/tmp") as directory:
            root = Path(directory)
            base, old, review = proposal(root)
            asset = json.loads((root / base / "asset.json").read_text())
            asset["questions"].append(dict(id="market", required_sources=[], depends_on=[]))
            put(root, base + "/asset.json", asset)
            market = copy.deepcopy(review["units"]["valuation"])
            market["consumed"] = {}
            if not grouped:
                for unit, field in ((market["output"], "path"), (market, "verification")):
                    new_path = old + "/market-" + Path(unit[field]).name
                    (root / new_path).write_bytes((root / unit[field]).read_bytes())
                    unit[field] = new_path
            review["units"]["market"] = market
            before = {p: p.read_bytes() for p in root.rglob("*") if p.is_file()}
            store = load()
            saved = store.publish(root, "aapl", review, {}, store.publication_snapshot(root), "acceptance")
            discovered = store.discover(root, "latest", CUTOFF)
            reused = sorted(row["work"] for row in discovered["reusable"])
            paths = {unit["output"]["path"] for unit in review["units"].values()}
            assert saved["status"] == "complete"
            assert reused == ["market", "valuation"]
            assert len(paths) == (1 if grouped else 2)
            assert all(p.read_bytes() == original for p, original in before.items())
            print(f"grouped={grouped} output_count={len(paths)} publication={saved['status']} reused={reused} original_bytes_unchanged=True")


if __name__ == "__main__":
    test_quarter_outputs_grouped_or_split_reusable()
```

- Package-suite check documented by README: `python3 -m pytest obsidian/tests obsidian-finance/tests -q -p no:cacheprovider`. The full suite is reserved for finalization and blocks acceptance on failure.

## Re-run on 2026-11-20, at 8299c735e76f8c1435bee15dac8340df5c08d958

Clean local clone, exact HEAD verified and blank `git status --porcelain`. Used the same local README and source-loaded workflow, with no installed host, real vault, or network. Reviewed `git diff fb2b4a0..8299c73`.

- 1: re-tested — opened and verified all six links and each reference's four sections and shared method link. The changed Technical Analysis Completion section now covers a revised quote against a reused range and a revised range against the still-eligible quote.
- 2: re-tested — applied the same full and partial prompts in section 2. The full sequence produced margins 15% versus 12%, operating volume +12% against a comparable peer's +8%, 120–140 fixed-yield and 100–116.67 quote-dependent value ranges, +10% two-session return and +6 percentage point benchmark spread, followed by three horizon judgments. Market-only used technical alone. The 132 correction scenario refreshed the quote-dependent value to 96–112, kept 120–140, and recomputed benchmark-relative return to +16 percentage points and dependent synthesis. Valuation-only used the eligible 121 close against the revised 100–115 range while preserving +10% and +6 percentage points. Missing valuation retained those two market signals and left comparison pending.
- 3: re-tested — again quarantined the 16:20 quote and September amendment at the historical 16:15 cutoff, cited the retained Q1 original for comparisons, kept the 2026 method identity separate, and left return and comparison pending where the eligible quote was missing. Added the prompt “The same fictional issuer's exchange corrected the August 8 close at 16:10 to 145 USD/share. The August 7 fixed-yield worksheet still gives 120–140 on the same currency and share basis and is the only adopted valuation. Update the price-sensitive short conclusion.” Used technical and synthesis; checked the eligible saved valuation's binding and reused that range without rerunning its model. The 121 baseline was inside 120–140. The 145 correction was above the unchanged upper bound by 3.5714%, with a two-session return of +31.8182% (prior close 110) and a +27.8182 percentage point spread over the +4% benchmark. The short judgment now records trading above the supported range despite positive relative performance, with a return to 140 or lower as its observable reversal; medium and long conclusions retain their earlier operating evidence and limitations. The unchanged fundamentals and valuation are reused.
- 4: carried over — the fix diff changes source instructions for selecting and applying valuation and technical analyses. It changes neither the instruction about combined or split notes nor the store, quarter metadata, publication and rediscovery paths or tests. The previous focused and grouped/split checks remain applicable.
