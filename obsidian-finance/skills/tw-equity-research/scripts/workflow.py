#!/usr/bin/env python3
"""Summarize Taiwan quarter source readiness and reconcile reported revenue."""

import argparse
import json
import re
from pathlib import Path


SCOPES = ("consolidated", "individual", "parent-only")


def assess(acquired, *, filed_ntd_thousands=None, filed_scope=None,
           reviewed_post_quarter=(), excluded_post_quarter=None, annual=False):
    period = re.fullmatch(r"([0-9]{4})Q([1-4])", acquired["quarter"])
    if period is None:
        raise ValueError("Expected a quarter in YYYYQn form")
    first = 3 * (int(period[2]) - 1) + 1
    expected_months = [f"{period[1]}-{month:02d}" for month in range(first, first + 3)]
    months = {row["month"]: row for row in acquired["monthly_revenue"]}
    if len(months) != len(acquired["monthly_revenue"]) or set(months) != set(expected_months):
        raise ValueError("Monthly source rows must match the three quarter months")
    if filed_ntd_thousands is not None and type(filed_ntd_thousands) is not int:
        raise ValueError("Filed revenue requires an integer amount in thousands of NTD")
    filing = acquired["quarterly_filing"]
    if filed_ntd_thousands is not None and filing["status"] != "available":
        raise ValueError("Filed revenue requires an available quarterly filing")
    if filed_scope is not None and filed_scope not in SCOPES:
        raise ValueError("Unrecognized filed revenue scope")

    gaps = []
    amounts, monthly_urls = [], []
    monthly_scopes = set()
    for month in expected_months:
        row = months[month]
        eligible = row["status"] == "available" or (
            acquired.get("mode") == "latest" and row["status"] == "observed"
        )
        if (eligible and type(row.get("amount_ntd_thousands")) is int
                and row.get("currency", "TWD") in ("NTD", "TWD")):
            amounts.append(row["amount_ntd_thousands"])
            monthly_urls.append(row["url"])
            scope = row.get("scope")
            monthly_scopes.add(scope if scope in SCOPES else None)
        else:
            gaps.append("monthly_revenue:" + month)
    monthly_scope = None
    monthly_total = None
    if len(amounts) == len(expected_months) and len(monthly_scopes) == 1:
        monthly_scope = next(iter(monthly_scopes))
        if monthly_scope is not None:
            monthly_total = sum(amounts)
    if filing["status"] != "available":
        gaps.append("quarterly_filing")

    disclosures = acquired["material_disclosures"]
    entries = disclosures["entries"]
    exclusions = excluded_post_quarter or {}
    for index, reason in exclusions.items():
        if (type(index) is not int or not 0 <= index < len(entries)
                or entries[index].get("relevance") != "post_quarter"
                or not isinstance(reason, str) or not reason.strip()):
            raise ValueError("Each post-quarter exclusion requires a valid index and reason")
    missing_entries = [index for index, item in enumerate(entries) if item.get("status") == "missing_body"]
    resolved_body_failures = (disclosures["status"] == "missing_body" and missing_entries
                              and all(index in exclusions for index in missing_entries))
    if disclosures["status"] != ("available" if entries else "none_found") and not resolved_body_failures:
        gaps.append("material_disclosures")
    expected_status = {"quarter": "available", "post_quarter": "needs_quarter_relevance_review"}
    for index, item in enumerate(entries):
        if index in exclusions:
            continue
        relevance = item.get("relevance")
        body = item.get("body")
        if (relevance not in expected_status or item.get("status") != expected_status[relevance]
                or not isinstance(body, str) or not body.strip()):
            gaps.append(f"material_disclosure:{index}")
        elif relevance == "post_quarter" and index not in reviewed_post_quarter:
            gaps.append(f"post_quarter_disclosure:{index}")
    quarterly_source_gate = not gaps
    annual_source_gate = None
    if annual:
        annual_source_gate = acquired.get("annual_report", {}).get("status") == "available"
        if not annual_source_gate:
            gaps.append("annual_report")

    difference = None
    if (filed_ntd_thousands is not None and monthly_total is not None
            and filed_scope == monthly_scope):
        difference = filed_ntd_thousands - monthly_total
    return {
        "quarterly_source_gate": quarterly_source_gate,
        "annual_source_gate": annual_source_gate,
        "gaps": gaps,
        "excluded_post_quarter": exclusions,
        "revenue": {
            "monthly_total_ntd_thousands": monthly_total,
            "monthly_scope": monthly_scope,
            "monthly_urls": monthly_urls,
            "filed_ntd_thousands": filed_ntd_thousands,
            "filed_scope": filed_scope,
            "filing_url": filing.get("url"),
            "filed_minus_monthly_ntd_thousands": difference,
        },
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--filed-ntd-thousands", type=int)
    parser.add_argument("--filed-scope", choices=SCOPES)
    parser.add_argument("--reviewed-post-quarter", type=int, action="append", default=[])
    parser.add_argument("--exclude-post-quarter", nargs=2, metavar=("INDEX", "REASON"),
                        action="append", default=[])
    parser.add_argument("--annual", action="store_true")
    args = parser.parse_args()
    try:
        acquired = json.loads(args.manifest.read_text(encoding="utf-8"))
        result = assess(
            acquired, filed_ntd_thousands=args.filed_ntd_thousands,
            filed_scope=args.filed_scope,
            reviewed_post_quarter=args.reviewed_post_quarter, annual=args.annual,
            excluded_post_quarter={int(index): reason for index, reason in args.exclude_post_quarter},
        )
    except (OSError, ValueError, KeyError, TypeError) as error:
        parser.error(str(error))
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
