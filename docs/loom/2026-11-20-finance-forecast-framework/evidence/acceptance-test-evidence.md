# Forward forecast framework — acceptance test evidence

Tried on 2026-11-20, in a clean copy of the project at ce7df9cfdcb51867ef65aca6e10b2d4f090bd34c. The initial four-row exercise ran on a61d02b111b77060fb0af52082681b54aca78f7a. For this re-run, cloned locally and checked exact HEAD and empty `git status --porcelain` before testing. Followed the README's folder-grounded entry by loading the checked-out skill directly and applying it to fictional excerpts. This is a source-loaded agent exercise with an offline fixture. No installed-host invocation, live vault, external source access, or real company conclusion was involved.

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

## Re-run on 2026-11-20, at ce7df9cfdcb51867ef65aca6e10b2d4f090bd34c

- 1: carried over. The fix adds retention instructions and does not alter the method or supported scenario rules. Compared the complete reference diff.
- 2: re-tested. Re-applied the release, authorship, metric, driver and gap cases above. Separately ran the following reproducible harness from the clean clone to exercise the actual version-1 publication helper twice. The harness uses a distinct synthetic calendar (2024Q2 reviews target 2024Q3) matching the existing generic issuer fixture. Each synthetic audit file is written before the corresponding call and represents an authorized pre-existing audit of the exact text, with a simulated timestamp. The audit input models the evidence reviewed by the agent; it does not authenticate real historical times.
- The first complete publication wrote v1, the second wrote v2 with v1 as predecessor, and v1 review, output and accompanying JSON remained byte-identical. Historical selection at the exact v1 cutoff returned v1 and latest selection returned v2. The acceptance harness followed the scoring guidance against a synthetic first comparable release reporting $112m, selected the $108m v2 over the $105m v1, and calculated +$4m. The equivalent reconciliation is +0.4m units at the same $10 price. Evidence available only at the first live release, evidence with different bytes and absent evidence were ineligible. The earlier-cutoff/post-release-authorship exercise remains independently ineligible. Scoring is an agent procedure in the guidance; the publication helper persists receipt bytes through its existing accompanying-file contract.
- 3: carried over. The fix does not change the forecast consumer contract or price-only and forecast revision instructions.
- 4: carried over. The fix does not change eligibility, expectations labeling or version-1 storage code. Repeated the focused storage command at this HEAD as well: `14 passed, 30 deselected in 0.51s`.

Run the probe below from the clean checkout with:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=obsidian-finance/tests python3.12 /private/tmp/test_forecast_versions_publish_and_reconcile.py
```

```text
v1 published status=complete predecessor=None output_sha256=535a7743f497f1db5fe54c8078b6ceca3b2e7afa957019a7b89ffa77a4d7df88
v2 published status=complete predecessor=v1 output_sha256=5c1192a48e83a5ae665bda3ab7e98399ddd1caa4c97feddfa138cff125669afd
v1 review/output/receipt bytes preserved; historical=v1; latest=v2; selected=v2; realized error=+4 USD million
missing audit, mismatched audited output, and evidence at first public release: ineligible
```

```python
"""Publish two exact forecast versions and reconcile solely eligible content."""

from copy import deepcopy
from datetime import datetime
from hashlib import sha256
import json
from pathlib import Path
from shutil import rmtree
from tempfile import TemporaryDirectory

from test_research_publication import proposal
from test_research_store import load, put


def read(path):
    return json.loads(path.read_bytes())


def digest(content):
    return sha256(content).hexdigest()


def test_forecast_versions_publish_and_reconcile():
    with TemporaryDirectory(dir="/private/tmp") as tmp:
        root = Path(tmp)
        base, legacy_review, template = proposal(root)
        # Reuse generic project/issuer fixture setup, but make both forecast
        # versions fresh publications through the store rather than seed one.
        rmtree(root / legacy_review)
        metadata_path = base + "/asset.json"
        metadata = read(root / metadata_path)
        metadata["questions"] = [
            dict(id="forecast", required_sources=["price"], depends_on=[])
        ]
        put(root, metadata_path, metadata)
        module = load()
        metric = dict(name="revenue", fiscal_period="2024Q3", unit="USD million", scope="consolidated")
        saved_versions = []

        for name, predecessor, cutoff, authored, retained, revenue in (
            ("v1", None, "2024-05-10T16:00:00+00:00", "2024-05-10T16:04:00+00:00", "2024-05-10T16:05:00+00:00", 105),
            ("v2", "v1", "2024-05-17T16:00:00+00:00", "2024-05-17T16:04:00+00:00", "2024-05-17T16:05:00+00:00", 108),
        ):
            version = deepcopy(template)
            version.update(id=name, cutoff=cutoff)
            version.pop("predecessor")
            if predecessor:
                version["predecessor"] = predecessor
            path = f"{base}/cycles/2024Q2/{cutoff[:10]}-{name}"
            snapshot = dict(version=name, cutoff=cutoff, authored_at=authored, metric=metric, forecast=revenue)
            report = json.dumps(snapshot, sort_keys=True)
            output_digest = digest(report.encode())
            unit = version["units"].pop("valuation")
            unit.update(output=dict(path=path + "/forecast.md", digest=output_digest),
                        verification=path + "/check.json")
            version["units"]["forecast"] = unit
            files = {"forecast.md": report,
                     "check.json": json.dumps(dict(version=1, output_digest=output_digest,
                         checks={k: True for k in ("sources", "citations", "calculations", "counterevidence")},
                         unresolved=[]))}
            audit_ref = f"audit/{name}.json"
            # The fixture simulates an authorized audit of exact bytes before
            # review publication; the dates are test input, not host timestamps.
            put(root, audit_ref, dict(retained_at=retained, snapshot=report))
            receipt = dict(forecast_version=name, output_path=unit["output"]["path"],
                           output_digest=output_digest, retained_at=retained,
                           evidence_ref=audit_ref)
            files["forecast-retention.json"] = json.dumps(receipt)
            result = module.publish(root, "aapl", version, files, module.publication_snapshot(root), "save-" + name)
            assert result["status"] == "complete"
            review = root / result["review"]
            output = root / unit["output"]["path"]
            assert read(review).get("predecessor") == predecessor
            assert digest(output.read_bytes()) == output_digest
            receipt_path = review.parent / "forecast-retention.json"
            assert read(receipt_path) == receipt
            saved_versions.append((review, review.read_bytes(), output, output.read_bytes(), receipt_path, receipt_path.read_bytes()))
            print(f"{name} published status={result['status']} predecessor={predecessor} output_sha256={output_digest}")

        for review, original_review, output, original_output, receipt_path, original_receipt in saved_versions:
            assert review.read_bytes() == original_review
            assert output.read_bytes() == original_output
            assert receipt_path.read_bytes() == original_receipt
        historical = module.discover(root, "historical", "2024-05-10T16:00:00+00:00")
        latest = module.discover(root, "latest", "2024-05-18T16:00:00+00:00")
        assert historical["reusable"] == [dict(record="aapl/2024Q2/v1", work="forecast")]
        assert latest["reusable"] == [dict(record="aapl/2024Q2/v2", work="forecast")]
        actual = dict(metric=metric, value=112, published_at="2024-08-02T16:05:00+00:00")
        compare_time = datetime.fromisoformat
        release = compare_time(actual["published_at"])
        def check(review, output, receipt, audit):
            forecast = read(output)
            frozen = review["units"]["forecast"]["output"]
            if (receipt and audit
                    and receipt["forecast_version"] == forecast["version"] == review["id"]
                    and receipt["output_path"] == frozen["path"] == str(output.relative_to(root))
                    and receipt["output_digest"] == frozen["digest"]
                    == digest(output.read_bytes()) == digest(audit["snapshot"].encode())
                    and receipt["retained_at"] == audit["retained_at"]
                    and forecast["metric"] == actual["metric"]
                    and all(compare_time(t) < release for t in
                            (forecast["cutoff"], forecast["authored_at"], audit["retained_at"]))):
                return forecast
            return None

        matched = []
        for review, _, output, _, receipt_path, _ in saved_versions:
            receipt = read(receipt_path)
            audit = read(root / receipt["evidence_ref"])
            matched.append(check(read(review), output, receipt, audit))
            assert matched[-1] is not None
            assert check(read(review), output, receipt, None) is None
            assert check(read(review), output, receipt, dict(audit, snapshot="changed bytes")) is None
            late = actual["published_at"]
            assert check(read(review), output, dict(receipt, retained_at=late), dict(audit, retained_at=late)) is None
        chosen = max(matched, key=lambda row: row["cutoff"])
        assert chosen["version"] == "v2"
        assert actual["value"] - chosen["forecast"] == 4
        print("v1 review/output/receipt bytes preserved; historical=v1; latest=v2; selected=v2; realized error=+4 USD million")
        print("missing audit, mismatched audited output, and evidence at first public release: ineligible")


if __name__ == "__main__":
    test_forecast_versions_publish_and_reconcile()
```
