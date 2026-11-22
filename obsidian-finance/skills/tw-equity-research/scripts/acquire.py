"""Retrieve Taiwan-listed issuer evidence from public TWSE services."""

import argparse
import hashlib
import json
import re
from datetime import date, datetime, timedelta
from html import unescape
from pathlib import Path
from tempfile import NamedTemporaryFile
from urllib.parse import urlencode, urlsplit
from urllib.request import HTTPRedirectHandler, Request, build_opener
from zoneinfo import ZoneInfo


MOPS = "https://mops.twse.com.tw/mops/api/"
DOC_HOST = "https://doc.twse.com.tw"
DOC = DOC_HOST + "/server-java/t57sb01"
TAIPEI = ZoneInfo("Asia/Taipei")
MAX_BYTES = 64 * 1024 * 1024


class AcquisitionError(ValueError):
    pass


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, request, handle, code, reason, headers, new_url):
        raise AcquisitionError("Unexpected redirect from TWSE source")


def fetch_public(url, body=None):
    headers = {"User-Agent": "Mozilla/5.0", "Accept": "*/*"}
    data = None
    if body is not None:
        headers["Content-Type"] = "application/json"
        data = json.dumps(body).encode()
    with build_opener(NoRedirect()).open(Request(url, data=data, headers=headers), timeout=30) as response:
        payload = response.read(MAX_BYTES + 1)
    if len(payload) > MAX_BYTES:
        raise AcquisitionError("TWSE response exceeds size limit")
    return payload


def _instant(value):
    timestamp = datetime.fromisoformat(value) if isinstance(value, str) else value
    if timestamp.tzinfo is None or timestamp.utcoffset() is None:
        raise ValueError("Supply a timezone-aware timestamp")
    return timestamp.astimezone(TAIPEI)


def _roc_timestamp(value):
    year, month, remainder = value.split("/", 2)
    return _instant(f"{int(year) + 1911:04d}-{month}-{remainder}+08:00")


def _retain(output, payload, suffix):
    digest = hashlib.sha256(payload).hexdigest()
    path = output / f"{digest}.{suffix}"
    with NamedTemporaryFile(dir=output) as stream:
        stream.write(payload)
        stream.flush()
        try:
            path.hardlink_to(stream.name)
        except FileExistsError:
            if path.is_symlink() or path.read_bytes() != payload:
                raise AcquisitionError(f"Evidence file does not match its hash: {path.name}")
    return {"path": path.name, "sha256": digest}


def _mops(fetch, endpoint, parameters):
    raw = fetch(MOPS + endpoint, parameters)
    envelope = json.loads(raw)
    if envelope.get("code") == 406 and "查無" in envelope.get("message", ""):
        return None, raw
    if envelope.get("code") != 200 or not isinstance(envelope.get("result"), dict):
        raise AcquisitionError(f"MOPS {endpoint}: {envelope.get('message', 'invalid response')}")
    return envelope["result"], raw


def _history_revenue(output, history, ticker, period, cutoff):
    selected = None
    for row in history:
        if row.get("ticker") != ticker or row.get("month") != period:
            continue
        available = _instant(row["available_at"])
        if available > cutoff:
            continue
        url = urlsplit(row["url"])
        amount = row["amount_ntd_thousands"]
        if (url.scheme != "https" or not url.hostname or type(amount) is not int
                or not isinstance(row["payload"], str) or not row["payload"].strip()):
            raise AcquisitionError(f"Invalid dated evidence for {period}")
        if selected is None or available > selected[0]:
            selected = available, row
        elif available == selected[0] and selected[1] != row:
            raise AcquisitionError(f"Conflicting monthly versions for {period}")
    if selected is None:
        return None
    available, row = selected
    return {"status": "available", "available_at": available.isoformat(), "url": row["url"],
            "amount_ntd_thousands": row["amount_ntd_thousands"], "scope": row.get("scope"),
            "provenance": "supplied_dated_source",
            **_retain(output, row["payload"].encode(), "txt")}


def _monthly(fetch, output, ticker, year, month, clock, cutoff, history):
    period = f"{year}-{month:02d}"
    bound = cutoff if cutoff is not None else clock()
    if date(year, month, 1) > bound.date():
        return {"month": period, "status": "not_available_at_cutoff"}
    dated = _history_revenue(output, history, ticker, period, bound)
    if dated is not None:
        return {"month": period, **dated}
    parameters = {"companyId": ticker, "dataType": "2", "year": str(year - 1911),
                  "month": str(month), "subsidiaryCompanyId": ""}
    result, raw = _mops(fetch, "t05st10_ifrs", parameters)
    if result is None:
        return {"month": period, "status": "none_found"}
    if result.get("marketKindName") != "上市公司" or result.get("yymm") != f"{year - 1911}{month:02d}":
        raise AcquisitionError("MOPS monthly result does not match the listed issuer and period")
    amount = int(dict(result["data"])["本月"].replace(",", ""))
    evidence = {"month": period, "url": MOPS + "t05st10_ifrs", "parameters": parameters,
                "observed_at": clock().isoformat()}
    if cutoff is not None:
        return evidence | {"status": "publication_unverified"}
    return evidence | {"status": "observed", "amount_ntd_thousands": amount,
                       "provenance": "current_observation_no_publication_time",
                       **_retain(output, raw, "json")}


def _html(raw):
    try:
        return raw.decode("utf-8")
    except UnicodeDecodeError:
        return raw.decode("cp950")


def _filing(fetch, output, ticker, year, number, cutoff):
    kind = "A" if number else "F"
    index_year = year if number else year + 1
    query = urlencode({"step": 1, "colorchg": 1, "co_id": ticker, "year": index_year - 1911,
                       "seamon": "", "mtype": kind})
    index = DOC + "?" + query
    html = _html(fetch(index))
    candidates = []
    for row in re.findall(r"<tr\b[^>]*>(.*?)</tr>", html, flags=re.I | re.S):
        cells = re.findall(r"<td\b[^>]*>(.*?)</td>", row, flags=re.I | re.S)
        if len(cells) < 10:
            continue
        name = re.search(r'readfile2\("' + kind + r'","' + ticker + r'","([0-9A-Za-z_]+\.pdf)"\)', cells[7])
        if name is None:
            continue
        filename = name[1]
        if number and filename != f"{year}{number:02d}_{ticker}_AI1.pdf":
            continue
        if not number and not re.fullmatch(rf"{year}_{ticker}_\d{{8}}F(?:04|11)\.pdf", filename):
            continue
        available = _roc_timestamp(cells[9].strip())
        correction = unescape(re.sub(r"<[^>]+>", "", cells[10])).strip() if len(cells) > 10 else ""
        candidates.append((available, filename, correction))
    eligible = [candidate for candidate in candidates if candidate[0] <= cutoff]
    if not eligible:
        state = "not_available_at_cutoff" if candidates else "not_found_in_index"
        return {"status": state, "index_url": index}
    available, filename, correction = max(eligible)
    # A correction flag can mean that the bytes behind the initial filename
    # have changed. Until an independently dated copy is found, avoid
    # backdating those bytes to the timestamp of the original upload.
    if number and correction not in {"", "無"}:
        return {"status": "revision_unverified", "index_url": index, "correction": correction}
    url = DOC + "?" + urlencode({"step": 9, "colorchg": 1, "kind": kind,
                                 "co_id": ticker, "filename": filename})
    landing = _html(fetch(url))
    prefix = re.escape(filename.removesuffix(".pdf"))
    href = re.search(rf"""href=['"](/pdf/{prefix}(?:_[0-9_]+)?\.pdf)['"]""", landing, re.I)
    if href is None:
        raise AcquisitionError(f"No download link for {filename}")
    pdf = fetch(DOC_HOST + href[1])
    if not pdf.startswith(b"%PDF-"):
        raise AcquisitionError(f"Invalid PDF response for {filename}")
    return {"status": "available", "available_at": available.isoformat(), "url": url,
            "index_url": index, "filename": filename, **_retain(output, pdf, "pdf")}


def _detail(fetch, output, ticker, timestamp, row):
    metadata = row[5]
    parameters = metadata["parameters"]
    if (metadata["apiName"] != "t05st01_detail" or parameters["companyId"] != ticker
            or parameters["marketKind"] != "sii"
            or not re.fullmatch(r"[0-9]{7}", parameters["enterDate"])
            or not re.fullmatch(r"[0-9]+", parameters["serialNumber"])):
        raise AcquisitionError("Invalid disclosure details reference")
    result, raw = _mops(fetch, "t05st01_detail", parameters)
    if result is None or result.get("companyId") != ticker or len(result["data"]) != 1:
        raise AcquisitionError("Disclosure details do not identify the requested issuer and event")
    body = result["data"][0]
    if (body[0] != parameters["serialNumber"]
            or _roc_timestamp(f"{body[1]} {body[2]}") != timestamp or not body[9].strip()):
        raise AcquisitionError("Missing or mismatched disclosure body")
    return {"url": MOPS + "t05st01_detail", "parameters": parameters,
            "body": body[9], **_retain(output, raw, "json")}


def _disclosures(fetch, output, ticker, start, end, cutoff):
    entries, queries, errors = [], [], []
    for year in range(start.year, cutoff.year + 1):
        parameters = {"companyId": ticker, "year": str(year - 1911),
                      "month": "all", "firstDay": "", "lastDay": ""}
        query = {"url": MOPS + "t05st01", "parameters": parameters}
        try:
            result, raw = _mops(fetch, "t05st01", parameters)
            if result is not None and (result.get("marketName") != "上市公司"
                                       or result.get("companyId") != ticker):
                raise AcquisitionError("MOPS disclosure result does not match listed issuer")
            queries.append(query | {"status": "searched", **_retain(output, raw, "json")})
            for row in [] if result is None else result["data"]:
                timestamp = _roc_timestamp(f"{row[2]} {row[3]}")
                if row[0] != ticker:
                    raise AcquisitionError("Unexpected issuer in disclosure rows")
                if not start <= timestamp.date() or timestamp > cutoff:
                    continue
                relevance = "quarter" if timestamp.date() <= end else "post_quarter"
                entry = {"available_at": timestamp.isoformat(), "title": row[4], "relevance": relevance}
                try:
                    entry.update(_detail(fetch, output, ticker, timestamp, row))
                    entry["status"] = "available" if relevance == "quarter" else "needs_quarter_relevance_review"
                except (OSError, ValueError, IndexError, KeyError, TypeError) as error:
                    entry.update(status="missing_body", error=str(error), url=MOPS + "t05st01_detail",
                                 detail_reference=row[5] if len(row) > 5 else None)
                entries.append(entry)
        except (OSError, ValueError, IndexError, KeyError, TypeError) as error:
            errors.append(query | {"error": str(error)})
    if errors:
        state = "retrieval_failed"
    elif any(entry["status"] == "missing_body" for entry in entries):
        state = "missing_body"
    else:
        state = "available" if entries else "none_found"
    return {"status": state, "entries": entries, "queries": queries, "errors": errors}


def _status(operation, *args):
    try:
        return operation(*args)
    except (OSError, ValueError, KeyError, TypeError, IndexError) as error:
        return {"status": "retrieval_failed", "error": str(error)}


def acquire(ticker, quarter, cutoff, output, *, annual_year=None, monthly_history=(),
            fetch=fetch_public, observed_at=None):
    if not re.fullmatch(r"[0-9]{4}", ticker):
        raise ValueError("Supply a four-digit TWSE-listed company code")
    period = re.fullmatch(r"(\d{4})Q([1-4])", quarter)
    if period is None or int(period[1]) < 1912:
        raise ValueError("Supply the corporate fiscal quarter as YYYYQ1 through YYYYQ4")
    year, number = map(int, period.groups())
    historical_cutoff = _instant(cutoff) if cutoff is not None else None
    fixed_observation = _instant(observed_at) if observed_at is not None else None

    def clock():
        return fixed_observation if fixed_observation is not None else datetime.now(TAIPEI)

    output = Path(output)
    output.mkdir(parents=True, exist_ok=True)
    first = (number - 1) * 3 + 1
    start = date(year, first, 1)
    end = (date(year, first + 3, 1) if number < 4 else date(year + 1, 1, 1)) - timedelta(days=1)
    if (historical_cutoff or clock()).date() < start:
        raise ValueError("The cutoff precedes the selected quarter")
    months = [
        {"month": f"{year}-{month:02d}",
         **_status(_monthly, fetch, output, ticker, year, month, clock, historical_cutoff, monthly_history)}
        for month in range(first, first + 3)
    ]
    observed_at = clock()
    cutoff = historical_cutoff or observed_at
    result = {"issuer": f"twse-{ticker}", "quarter": quarter, "cutoff": cutoff.isoformat(),
              "mode": "historical" if historical_cutoff is not None else "latest",
              "observed_at": observed_at.isoformat(), "monthly_revenue": months,
              "quarterly_filing": _status(_filing, fetch, output, ticker, year, number, cutoff),
              "material_disclosures": _disclosures(fetch, output, ticker, start, end, cutoff)}
    if annual_year is not None:
        result["annual_report"] = _status(_filing, fetch, output, ticker, annual_year, None, cutoff)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("ticker")
    parser.add_argument("quarter")
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--cutoff", help="Historical assessment cutoff with timezone")
    mode.add_argument("--latest", action="store_true", help="Include current observations without publication times")
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--annual-year", type=int)
    parser.add_argument("--monthly-history", type=Path, help="Verified dated original releases, as JSON")
    args = parser.parse_args()
    history = [] if args.monthly_history is None else json.loads(args.monthly_history.read_text())
    report = acquire(args.ticker, args.quarter, args.cutoff, args.output,
                     annual_year=args.annual_year, monthly_history=history)
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
