# Forward forecast framework — acceptance test evidence

Tried on 2026-11-20, in a clean copy of the project at a61d02b111b77060fb0af52082681b54aca78f7a. Cloned locally and checked exact HEAD and empty `git status --porcelain` before testing. Followed the README's folder-grounded entry by loading the checked-out skill directly and applying it to fictional excerpts. This is a source-loaded agent exercise with an offline fixture. No installed-host invocation, live vault, external source access, or real company conclusion was involved.

## 1. 前瞻預測有獨立指引，說明從前三類基本面證據選擇驅動因素、模型、期間與情境的方法，列出可核對的假設、來源與資料缺口。每季檢視樂觀、基準、悲觀三條路徑；證據足夠才量化，否則保留方向與驗證條件，或明列證據缺口。

- How I tried it: Opened the framework link at `obsidian-finance/skills/finance-research/SKILL.md:128`, then applied it to “Forecast fictional Alder's Q3 and review all three paths using the information available on 2025-08-14 at 16:00 New York time.” Fictional retained originals: Q2 issuer filing Aug 5 16:10, income statement row 4 shows USD 100m from 10m units at $10; MD&A paragraph 2 shows the dominant operating driver is orders converting to shipments, with spare capacity up to 12m units. Aug 7 industry study table 1 shows unchanged pricing and 5% regional growth but gives no company share denominator. Aug 13 issuer operating update paragraph 3 shows additional confirmed orders covering a base of 10.5m units, with conditional shipments supporting 11–11.5m.
- What came back: Bottom-up revenue (units × price) is the simplest model with supported inputs. $105m base at $10 and 10.5m units, with stable prices and order conversion as the checks. The bull gives $110m–$115m if conditional orders convert while utilization stays within capacity. Bear direction is below base if cancellations or delivery slippage rise, with a weekly cancellations/shipment check and a missing downside-volume floor. Spare capacity does not guarantee conversion. Industry growth is a cross-check and does not establish company share or justify an independent top-down estimate. The Q2 result anchors the scale, and the comparable Q3 baseline and beyond-Q3 inputs are gaps. Recorded source passages, timestamp, fiscal period, units and assumptions. No unsupported probabilities.

## 2. 每季保存一版當時可得的預測及資訊截止時間；遇到重要修訂保留舊版。下一季用實績核對上季同口徑預測，說明差異與新假設。

- How I tried it: Applied “Keep the August versions and reconcile Q3 at its first public release.” Simulated a version ledger with unchanged retained snapshots: v1 authored and published Aug 14 at 16:05 after the 16:00 cutoff, $105m base; v2 authored and published Aug 21 at 16:05 after its 16:00 cutoff, $108m base, from a dated confirmed order update supporting 10.8m units; timestamped fixture publication records identify the exact v1 and v2 contents. Q3 actual first release Nov 4 at 16:05, same basis and fiscal period, $112m at 11.2m units and $10. Added a Nov 5 reconstruction with Aug 14 cutoff and $112m base, and a nominal Aug 22 version whose only retention information was a file modification time.
- What came back: Kept v1 and v2 independently associated with their original cutoffs and retained the revision rationale. Adopted v2 as the latest verified pre-release version. Error was +$4m, with 0.4m more units than the v2 base at the same price; subsequent planning updates the conversion baseline, while the persistence of this difference remains open. A hypothetical saved $107m–$109m range comparison yields $3m above its upper bound. Nov 5 actual-matching reconstruction was ineligible for realized scoring despite its early cutoff; the Aug 22 version was also ineligible because retention was unverifiable. Kept the Nov 4 release in the scoring analysis. A currency/basis mismatch without conversion evidence would leave scoring pending. See `forward-forecast.md` under “Save and reconcile forecast versions” and `synthesis.md:28`.

## 3. 估值可引用實際採用的預測版本；只有行情改變時沿用仍有效的營運預測，預測假設改變時重評相依的估值與綜合判斷。

- How I tried it: Applied `valuation-and-risk.md` and the price-only and forecast-revision instructions in `SKILL.md:147` to a valuation snapshot binding v1 explicitly. Fictional worksheet converts supported $105m quarterly revenue to $10.50/share in this illustrative model (assumed 10% margin, four comparable quarters independently supported, 10% capitalization rate and 40m shares). Quote moves from $10 to $12. Then adopt the separately retained v2 snapshot at $108m with the same other inputs.
- What came back: Quote-only case reused v1 and the $10.50 intrinsic estimate, updating the quote-to-value comparison and price-dependent synthesis. For the v2 adoption, retained v1 binding and snapshot, selected the v2 record explicitly, recomputed $10.80 intrinsic value, and updated the price-to-value comparison and dependent synthesis. Price-only market signals are independently reusable during the forecast revision. A quote-dependent valuation assumption, where present, is re-evaluated on quote changes. The focused local dependency tests below independently verified invalidation of valuation and dependent synthesis when input version, authorship, projection, content, or presence changes, while unrelated work survived.

## 4. 歷史重建排除當時未公開的資料，並區分公司指引、市場共識與自己的模型。缺資料時保留缺口，沿用既有季度儲存契約。

- How I tried it: Reconstructed Aug 14 using a distinct issuer management release Aug 12, Q3 revenue guidance $102m–$110m on the same basis, a consensus snapshot first published Aug 15, and the Nov 4 actual and subsequent amendment. These dates are fictional New York publication dates and the reconstruction was authored Nov 5.
- What came back: Kept issuer guidance distinct from the analyst's $105m model; left Aug 14 point-in-time consensus unavailable, excluded the Aug 15 snapshot, actual and subsequent amendment from forecast inputs, and labeled actual authorship Nov 5. Placed the scoped forecast under the existing quarter review and output convention. Bound retained eligible economic inputs separately from the locally authored assumptions, projections, and adopted forecast version. No migration or requirement for additional standalone notes emerged.
- Evidence: Ran the focused existing version-1 storage tests below. They exercise retention of unsupported existing folder data, exclusion of future-only saved quarters from historical results, and local analysis input provenance and dependency invalidation. The default Python executable lacks pytest, so the same selection ran with the already available Python 3.12. The automated package suite is reserved for finalization, which blocks acceptance if it fails.

```sh
PYTHONDONTWRITEBYTECODE=1 python3.12 -m pytest obsidian-finance/tests/test_research_store.py -q -p no:cacheprovider -k 'local_analysis_dependencies or earlier_cutoff or unsupported_folder'
```

```text
..............                                                           [100%]
14 passed, 30 deselected in 0.78s
```

Package-suite command documented by README: `python3 -m pytest obsidian/tests obsidian-finance/tests -q -p no:cacheprovider`.
