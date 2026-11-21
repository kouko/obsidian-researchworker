"""Publish and recover versioned quarterly market research in Obsidian."""

import argparse
import hashlib
import json
import math
import os
import re
import sys
from datetime import datetime, time, timezone
from pathlib import Path

from market_evidence import _parse_time, claim_is_eligible, compare_forecast


_NOTE_NAMES = ("analysis.md", "sources.md", "outlook.md")
_RECORD_START = "\n```market-research-record\n"
_RECORD_END = "\n```\n"


def _quarter_number(quarter):
    if not isinstance(quarter, str) or not re.fullmatch(r"[0-9]{4}Q[1-4]", quarter):
        raise ValueError("Expected a calendar quarter in YYYYQn format")
    return int(quarter[-1])


def _scope(root, market, quarter):
    if not isinstance(market, str) or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", market):
        raise ValueError("Expected a lowercase market slug")
    _quarter_number(quarter)
    market_dir = Path(root).resolve() / market
    quarter_dir = market_dir / quarter
    for directory in (market_dir, quarter_dir):
        if directory.is_symlink():
            raise ValueError(f"Research scope cannot be a symlink: {directory}")
    return quarter_dir


def _boundary(value):
    parsed = _parse_time(value)
    if isinstance(parsed, datetime):
        return parsed
    return datetime.combine(parsed, time.max, tzinfo=timezone.utc)


def _canonical_json(value):
    return json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False)


def _validate(record, market, quarter, revision):
    if record.get("market") != market or record.get("quarter") != quarter:
        raise ValueError("Snapshot identity does not match its location")
    if type(revision) is not int or revision < 1 or record.get("revision") != revision:
        raise ValueError("Expected a positive integer snapshot revision")
    if type(record["revision"]) is not int:
        raise ValueError("Snapshot revision must be an integer")
    _boundary(record.get("cutoff"))
    for field in ("overview", "analysis", "outlook"):
        if not isinstance(record.get(field), str) or not record[field].strip():
            raise ValueError(f"Expected Markdown text for {field}")
    if not isinstance(record.get("pending"), list) or not all(
        isinstance(item, str) and item.strip() for item in record["pending"]
    ):
        raise ValueError("Expected a list of pending research items")
    for field in ("sources", "claims"):
        if not isinstance(record.get(field), dict) or not all(
            isinstance(key, str) and key.strip() and isinstance(value, dict)
            for key, value in record[field].items()
        ):
            raise ValueError(f"Expected a mapping of {field} by identifier")
    for claim_id, claim in record["claims"].items():
        text = claim.get("text")
        ids = claim.get("source_ids")
        if not isinstance(text, str) or not text.strip() or not isinstance(ids, list) or not ids:
            raise ValueError(f"Expected claim text and source versions for {claim_id}")
        if any(not isinstance(key, str) or key not in record["sources"] for key in ids):
            raise ValueError(f"Unknown source version for {claim_id}")
    for field in ("forecasts", "actuals", "comparisons"):
        if field in record and not isinstance(record[field], list):
            raise ValueError(f"Expected a list of {field}")


def _read_bytes(path):
    if path.is_symlink() or not path.is_file():
        raise ValueError(f"Missing or invalid {path.name}")
    return path.read_bytes()


def _digest(data):
    return hashlib.sha256(data).hexdigest()


def _read_record(path, market, quarter, revision):
    _, marker, tail = _read_bytes(path).decode().partition(_RECORD_START)
    encoded, footer, trailing = tail.partition(_RECORD_END)
    if not marker or not footer or trailing:
        raise ValueError("Missing or malformed snapshot record")
    manifest = json.loads(encoded)
    if not isinstance(manifest, dict) or manifest.get("schema") != 1:
        raise ValueError("Unsupported snapshot schema")
    record, files = manifest.get("record"), manifest.get("files")
    if not isinstance(record, dict) or not isinstance(files, dict) or set(files) != set(_NOTE_NAMES):
        raise ValueError("Incomplete snapshot manifest")
    _validate(record, market, quarter, revision)
    for name in _NOTE_NAMES:
        if _digest(_read_bytes(path.with_name(name))) != files[name]:
            raise ValueError(f"Content changed in {name}")
    return record


def _snapshots(quarter_dir):
    valid = []
    issues = []
    if not quarter_dir.is_dir():
        return valid, issues
    for directory in sorted(quarter_dir.iterdir()):
        match = re.fullmatch(r"r([1-9][0-9]*)", directory.name)
        if not match:
            continue
        if directory.is_symlink() or not directory.is_dir():
            issues.append(f"{directory.name}: invalid snapshot directory")
            continue
        path = directory / "review.md"
        try:
            record = _read_record(
                path, quarter_dir.parent.name, quarter_dir.name, int(match[1]),
            )
        except (ValueError, OSError, OverflowError) as error:
            issues.append(f"{directory.name}: {error}")
            continue
        valid.append((record, path))
    valid.sort(key=lambda item: (_boundary(item[0]["cutoff"]), item[0]["revision"]), reverse=True)
    return valid, issues


def _overview_file(path, text):
    try:
        with path.open("x", encoding="utf-8") as handle:
            handle.write(text.rstrip() + "\n")
    except FileExistsError:
        # The entry may be a note maintained by the user.
        pass


def publish(root, record):
    """Save one revision. The atomic appearance of review.md publishes it."""
    market, quarter = record.get("market"), record.get("quarter")
    revision = record.get("revision")
    quarter_dir = _scope(root, market, quarter)
    _validate(record, market, quarter, revision)
    snapshot_dir = quarter_dir / f"r{revision}"
    history, _ = _snapshots(quarter_dir)
    earlier = [
        path for old, path in history
        if old["revision"] < revision and _boundary(old["cutoff"]) <= _boundary(record["cutoff"])
    ]
    notes = {
        "analysis.md": record["analysis"],
        "sources.md": "# Source versions\n\n```json\n" + _canonical_json(record["sources"]) + "\n```",
        "outlook.md": record["outlook"],
    }
    notes = {name: (body.rstrip() + "\n").encode() for name, body in notes.items()}
    manifest = {
        "schema": 1, "record": record,
        "files": {name: _digest(data) for name, data in notes.items()},
    }
    label = "Partial" if record["pending"] else "Complete"
    links = "\n".join(f"- [{name.removesuffix('.md').title()}]({name})" for name in _NOTE_NAMES)
    predecessor = f"\n[Previous snapshot](../{earlier[0].parent.name}/review.md)\n" if earlier else ""
    review = (
        f"# {market} {quarter} r{revision}\n\n{label} at {record['cutoff']}\n\n"
        f"[Market overview](../../overview.md)\n\n{links}\n{predecessor}"
        f"{_RECORD_START}{_canonical_json(manifest)}{_RECORD_END}"
    )
    snapshot_dir.mkdir(parents=True, exist_ok=False)
    _overview_file(quarter_dir.parent / "overview.md", record["overview"])
    for name, data in notes.items():
        with (snapshot_dir / name).open("xb") as handle:
            handle.write(data)
    staging = snapshot_dir / ".review.tmp"
    with staging.open("x", encoding="utf-8") as handle:
        handle.write(review)
    path = snapshot_dir / "review.md"
    os.link(staging, path)
    staging.unlink()
    return path


def resume(root, market, quarter, cutoff=None):
    """Return the newest valid snapshot within the selected research scope."""
    boundary = _boundary(cutoff) if cutoff is not None else None
    snapshots, issues = _snapshots(_scope(root, market, quarter))
    for record, path in snapshots:
        if boundary is None or _boundary(record["cutoff"]) <= boundary:
            return {"record": record, "review": str(path), "issues": issues}
    return {"record": None, "review": None, "issues": issues}


def cite(root, market, quarter, claim_id, cutoff):
    """Look up a claim whose material source versions are eligible at cutoff."""
    boundary = _boundary(cutoff)
    snapshots, _ = _snapshots(_scope(root, market, quarter))
    for record, path in snapshots:
        claim = record["claims"].get(claim_id)
        if claim is not None and claim_is_eligible(claim, record["sources"], cutoff):
            return {
                "claim": claim,
                "sources": {key: record["sources"][key] for key in claim["source_ids"]},
                "review": str(path), "quarter": quarter, "market": market,
                "cutoff": cutoff, "snapshot_cutoff": record["cutoff"],
                "retrospective": _boundary(record["cutoff"]) > boundary,
            }
    return None


def _number(value):
    return type(value) is int or (type(value) is float and math.isfinite(value))


def aggregate_quarter(quarter, observations, cutoff, *, sources, ratio=False):
    """Aggregate three eligible comparable months, or identify why incomplete."""
    start = 1 + 3 * (_quarter_number(quarter) - 1)
    _boundary(cutoff)
    expected = [f"{quarter[:4]}-{month:02}" for month in range(start, start + 3)]
    components = {}
    issues = []
    for observation in observations:
        month = observation.get("month")
        if month not in expected:
            issues.append(f"Outside-quarter observation: {month}")
        elif claim_is_eligible(observation, sources, cutoff):
            previous = components.get(month)
            if previous is not None and previous != observation:
                issues.append(f"Conflicting observations for {month}")
            else:
                components[month] = observation
    missing = [month for month in expected if month not in components]
    rows = [components[month] for month in expected if month in components]
    source_ids = list(dict.fromkeys(key for row in rows for key in row["source_ids"]))
    for key in ("scope", "metric", "unit"):
        descriptors = [row.get(key) for row in rows]
        if any(not isinstance(value, str) or not value.strip() for value in descriptors):
            issues.append(f"Missing component {key}")
        elif len(set(descriptors)) > 1:
            issues.append(f"Incompatible component {key}")
    fields = ("numerator", "denominator") if ratio else ("value",)
    if any(not _number(row.get(field)) for row in rows for field in fields):
        issues.append("Invalid component value")
    if ratio and not issues and any(
        row["numerator"] < 0 or row["denominator"] < row["numerator"]
        for row in rows
    ):
        issues.append("Invalid share components")
    partial = {"status": "partial", "issues": issues, "missing_months": missing, "source_ids": source_ids}
    if missing or issues:
        return partial
    if ratio:
        denominator = sum(row["denominator"] for row in rows)
        if not denominator:
            return {**partial, "issues": ["Quarter denominator is zero"]}
        numerator = sum(row["numerator"] for row in rows)
        return {
            "status": "complete", "value": numerator / denominator, "source_ids": source_ids,
            "numerator": numerator, "denominator": denominator,
        }
    return {"status": "complete", "value": sum(row["value"] for row in rows), "source_ids": source_ids}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("publish").add_argument("root")
    for name in ("resume", "cite"):
        command = commands.add_parser(name)
        command.add_argument("root")
        command.add_argument("market")
        command.add_argument("quarter")
        if name == "resume":
            command.add_argument("--cutoff")
        else:
            command.add_argument("claim_id")
            command.add_argument("cutoff")
    aggregate = commands.add_parser("aggregate")
    aggregate.add_argument("quarter")
    aggregate.add_argument("cutoff")
    aggregate.add_argument("--ratio", action="store_true")
    commands.add_parser("compare").add_argument("cutoff")

    args = parser.parse_args(argv)
    try:
        if args.command == "publish":
            result = {"review": str(publish(args.root, json.load(sys.stdin)))}
        elif args.command == "resume":
            result = resume(args.root, args.market, args.quarter, args.cutoff)
        elif args.command == "cite":
            result = cite(args.root, args.market, args.quarter, args.claim_id, args.cutoff)
        elif args.command == "aggregate":
            data = json.load(sys.stdin)
            result = aggregate_quarter(
                args.quarter, data["observations"], args.cutoff,
                sources=data["sources"], ratio=args.ratio,
            )
        else:
            data = json.load(sys.stdin)
            result = compare_forecast(data["forecast"], data.get("actual"), data["sources"], args.cutoff)
        print(_canonical_json(result))
    except (ValueError, OSError, KeyError, TypeError, AttributeError, OverflowError) as error:
        parser.exit(1, f"{parser.prog}: {error}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
