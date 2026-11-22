import importlib.util
import json
from datetime import datetime
from pathlib import Path


def load_acquisition():
    path = Path(__file__).resolve().parents[1] / "skills/tw-equity-research/scripts/acquire.py"
    spec = importlib.util.spec_from_file_location("tw_acquire", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def response(result=None, code=200, message="查詢成功"):
    return json.dumps({"code": code, "message": message, "result": result}).encode()


def transport(*, result="body", monthly=None):
    rows = [
        ["1611", "中電", "114/07/02", "10:00:00", "本季公告",
         {"apiName": "t05st01_detail", "parameters": {"serialNumber": "1",
          "companyId": "1611", "marketKind": "sii", "enterDate": "1140702"}}],
        ["1611", "中電", "114/10/30", "10:00:00", "下一季公告",
         {"apiName": "t05st01_detail", "parameters": {"serialNumber": "2",
          "companyId": "1611", "marketKind": "sii", "enterDate": "1141030"}}],
    ]

    def fetch(url, body=None):
        if url.endswith("/t05st01"):
            data = {"companyId": "1611", "marketName": "上市公司", "data": rows}
            if result == "empty":
                return response(code=406, message="查無相符資料")
            if result == "failed":
                return response(code=500, message="無法查詢")
            return response(data)
        if url.endswith("/t05st01_detail"):
            day = "114/07/02" if body["serialNumber"] == "1" else "114/10/30"
            return response({"companyId": "1611", "data": [
                [body["serialNumber"], day, "10:00:00", "", "", "", "", "", "", "本文" if result == "body" else ""]
            ]})
        if url.endswith("/t05st10_ifrs"):
            month = int(body["month"])
            return response({"marketKindName": "上市公司", "yymm": f"114{month:02}",
                             "data": [["本月", "90,240" if monthly is None else monthly]]})
        if "step=1" in url:
            return ('<table><tr><td>1611</td><td>114</td><td></td><td></td>'
                    '<td></td><td>IFRSs合併財報</td><td></td>'
                    '<td><a href=\'javascript:readfile2("A","1611","202503_1611_AI1.pdf");\'>財報</a></td>'
                    '<td>1,000</td><td>114/11/11 13:24:58</td><td></td>'
                    '</tr></table>').encode()
        if "step=9" in url:
            return b'<a href="/pdf/202503_1611_AI1_20261122_220738.pdf">download</a>'
        if "/pdf/" in url:
            return b"%PDF-1.4 fixture"
        raise AssertionError(url)

    return fetch


def run(tmp_path, *, cutoff="2025-11-30T00:00:00+08:00", fetch=None, history=()):
    return load_acquisition().acquire(
        "1611", "2025Q3", cutoff, tmp_path, fetch=fetch or transport(),
        observed_at=datetime.fromisoformat("2026-11-22T22:00:00+08:00"),
        monthly_history=history,
    )


def test_historical_month_requires_publication_evidence_and_excludes_future_revision(tmp_path):
    history = [
        {"month": "2025-07", "ticker": "1611", "amount_ntd_thousands": 90240,
         "available_at": "2025-08-08T15:00:00+08:00", "url": "https://example.com/original",
         "payload": "Original July release"},
        {"month": "2025-07", "ticker": "1611", "amount_ntd_thousands": 90250,
         "available_at": "2025-12-01T15:00:00+08:00", "url": "https://example.com/correction",
         "payload": "Corrected July release"},
    ]
    result = run(tmp_path, history=history)
    july, august, _ = result["monthly_revenue"]
    assert july["amount_ntd_thousands"] == 90240
    assert (tmp_path / july["path"]).read_text() == "Original July release"
    assert august["status"] == "publication_unverified"


def test_filing_and_disclosure_text_have_provenance(tmp_path):
    result = run(tmp_path)
    assert result["quarterly_filing"]["status"] == "available"
    assert result["quarterly_filing"]["available_at"] == "2025-11-11T13:24:58+08:00"
    assert "step=9" in result["quarterly_filing"]["url"]
    assert (tmp_path / result["quarterly_filing"]["path"]).read_bytes().startswith(b"%PDF")
    disclosures = result["material_disclosures"]
    assert disclosures["status"] == "available"
    assert disclosures["entries"][0]["body"] == "本文"
    assert disclosures["entries"][1]["status"] == "needs_quarter_relevance_review"


def test_empty_failed_and_missing_body_are_distinct(tmp_path):
    for state, expected in [("empty", "none_found"), ("failed", "retrieval_failed"),
                            ("missing", "missing_body")]:
        result = run(tmp_path, fetch=transport(result=state))
        assert result["material_disclosures"]["status"] == expected


def test_pre_filing_cutoff_excludes_quarterly_filing_and_future_disclosures(tmp_path):
    result = run(tmp_path, cutoff="2025-10-01T09:00:00+08:00")
    assert result["quarterly_filing"]["status"] == "not_available_at_cutoff"
    assert len(result["material_disclosures"]["entries"]) == 1


def test_latest_observation_does_not_backdate_monthly_revenue(tmp_path):
    result = run(tmp_path, cutoff=None)
    assert all(month["status"] == "observed" for month in result["monthly_revenue"])
    assert all(month["observed_at"] == result["cutoff"] for month in result["monthly_revenue"])
    assert all("available_at" not in month for month in result["monthly_revenue"])


def test_flagged_quarterly_filing_uses_independently_dated_versions(tmp_path):
    acquisition = load_acquisition()
    original_fetch = transport()

    def fetch(url, body=None):
        raw = original_fetch(url, body)
        return raw.replace(b"<td></td></tr>", "<td>更正</td></tr>".encode()) if "step=1" in url else raw

    versions = []
    for name, day in (("original", 11), ("corrected", 26)):
        pdf = tmp_path / f"{name}.pdf"
        pdf.write_bytes(f"%PDF-1.4 {name}".encode())
        versions.append({"ticker": "1611", "quarter": "2025Q3",
                         "available_at": f"2025-11-{day}T13:24:58+08:00",
                         "url": f"https://example.com/{name}.pdf",
                         "publication_url": f"https://example.com/{name}-release",
                         "publication_evidence": f"Archive identifies {name} PDF and publication timestamp.",
                         "pdf": pdf})

    out = tmp_path / "output"
    for day, expected in ((10, None), (20, "original"), (30, "corrected")):
        report = acquisition.acquire("1611", "2025Q3", f"2025-11-{day}T23:00:00+08:00",
                                     out, fetch=fetch, filing_history=versions)
        filing = report["quarterly_filing"]
        if expected is None:
            assert filing["status"] == "not_available_at_cutoff"
        else:
            assert filing["status"] == "available"
            assert filing["url"] == f"https://example.com/{expected}.pdf"
            assert (out / filing["path"]).read_bytes() == f"%PDF-1.4 {expected}".encode()
            assert expected in (out / filing["publication_path"]).read_text()
