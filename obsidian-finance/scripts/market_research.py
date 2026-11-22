"""Publish and recover versioned quarterly market research in Obsidian."""

import argparse
import hashlib
import json
import math
import os
import re
import sys
from datetime import date, datetime, time, timezone
from pathlib import Path
from urllib.parse import urlsplit

import industry_notes as notes
import industry_update as update

from market_evidence import _parse_time, claim_is_eligible, compare_forecast


_LEGACY_NOTE_NAMES = ("analysis.md", "sources.md", "outlook.md")
_NOTE_NAMES = ("overview.md", *_LEGACY_NOTE_NAMES)
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


def _provenance_available(source):
    for key in ("url", "locator", "observation_period"):
        value = source.get(key)
        if not isinstance(value, str) or not value.strip():
            return False
    try:
        original = urlsplit(source["url"])
    except ValueError:
        return False
    return original.scheme in ("https", "http") and bool(original.hostname)


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
        if not claim_is_eligible(claim, record["sources"], record["cutoff"]):
            raise ValueError(f"Ineligible source version at snapshot cutoff for {claim_id}")
    for field in ("forecasts", "actuals", "comparisons"):
        if field in record and not isinstance(record[field], list):
            raise ValueError(f"Expected a list of {field}")
    for field in ("forecasts", "actuals"):
        for observation in record.get(field, []):
            if not isinstance(observation, dict) or not claim_is_eligible(
                observation, record["sources"], record["cutoff"],
            ):
                raise ValueError(f"Ineligible source version at snapshot cutoff in {field}")


def _read_bytes(path):
    if path.is_symlink() or not path.is_file():
        raise ValueError(f"Missing or invalid {path.name}")
    return path.read_bytes()


def _digest(data):
    return hashlib.sha256(data).hexdigest()


def _note_bytes(text):
    return (text.rstrip() + "\n").encode("utf-8")


def _read_record(path, market, quarter, revision):
    _, marker, tail = _read_bytes(path).decode().partition(_RECORD_START)
    encoded, footer, trailing = tail.partition(_RECORD_END)
    if not marker or not footer or trailing:
        raise ValueError("Missing or malformed snapshot record")
    manifest = json.loads(encoded)
    if not isinstance(manifest, dict) or type(manifest.get("schema")) is not int:
        raise ValueError("Unsupported snapshot schema")
    schema = manifest["schema"]
    if schema not in (1, 2):
        raise ValueError("Unsupported snapshot schema")
    note_names = _LEGACY_NOTE_NAMES if schema == 1 else _NOTE_NAMES
    record, files = manifest.get("record"), manifest.get("files")
    if not isinstance(record, dict) or not isinstance(files, dict) or set(files) != set(note_names):
        raise ValueError("Incomplete snapshot manifest")
    _validate(record, market, quarter, revision)
    for name in note_names:
        if _digest(_read_bytes(path.with_name(name))) != files[name]:
            raise ValueError(f"Content changed in {name}")
    if schema == 1:
        overview = path.parents[2] / "overview.md"
        if _digest(_read_bytes(overview)) != _digest(_note_bytes(record["overview"])):
            raise ValueError("Legacy shared overview.md differs from the saved snapshot")
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


def _publish_legacy(root, record):
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
        "overview.md": record["overview"],
        "analysis.md": record["analysis"],
        "sources.md": "# Source versions\n\n```json\n" + _canonical_json(record["sources"]) + "\n```",
        "outlook.md": record["outlook"],
    }
    notes = {name: _note_bytes(body) for name, body in notes.items()}
    manifest = {
        "schema": 2, "record": record,
        "files": {name: _digest(data) for name, data in notes.items()},
    }
    label = "Partial" if record["pending"] else "Complete"
    links = "\n".join(
        f"- [{name.removesuffix('.md').title()}]({name})" for name in _LEGACY_NOTE_NAMES
    )
    predecessor = f"\n[Previous snapshot](../{earlier[0].parent.name}/review.md)\n" if earlier else ""
    review = (
        f"# {market} {quarter} r{revision}\n\n{label} at {record['cutoff']}\n\n"
        f"[Market overview](overview.md)\n\n{links}\n{predecessor}"
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


def _resume_legacy(root, market, quarter, cutoff=None):
    """Return the newest valid snapshot within the selected research scope."""
    boundary = _boundary(cutoff) if cutoff is not None else None
    snapshots, issues = _snapshots(_scope(root, market, quarter))
    for record, path in snapshots:
        if boundary is None or _boundary(record["cutoff"]) <= boundary:
            return {"record": record, "review": str(path), "issues": issues}
    return {"record": None, "review": None, "issues": issues}


def _cite_legacy(root, market, quarter, claim_id, cutoff):
    """Look up a claim whose material source versions are eligible at cutoff."""
    boundary = _boundary(cutoff)
    snapshots, _ = _snapshots(_scope(root, market, quarter))
    for record, path in snapshots:
        claim = record["claims"].get(claim_id)
        if (
            claim is not None
            and claim_is_eligible(claim, record["sources"], cutoff)
            and all(_provenance_available(record["sources"][key]) for key in claim["source_ids"])
        ):
            return {
                "claim": claim,
                "sources": {key: record["sources"][key] for key in claim["source_ids"]},
                "review": str(path), "quarter": quarter, "market": market,
                "cutoff": cutoff, "snapshot_cutoff": record["cutoff"],
                "retrospective": _boundary(record["cutoff"]) > boundary,
            }
    return None


_HISTORY_START = "\n```industry-research-data\n"
_HISTORY_END = "\n```"
_ROLES = ("size-share", "outlook", "supply-chain")
_DISPLAYS = {
    "en": ("Substudies", "Pending", "Important changes", "Sources", "Earlier revision", "Updated"),
    "ja": ("関連調査", "未確認事項", "重要な修正", "出典", "以前の版", "更新日"),
    "zh-TW": ("子研究", "待查事項", "重要修訂", "來源", "先前版本", "更新日"),
}
_ROLE_FIELDS = {
    "size-share": ("analysis", "sources", "claims"),
    "outlook": ("outlook", "forecasts", "actuals", "comparisons"),
    "supply-chain": ("supply_chain",),
    "company": ("body",),
}


def _in_vault(root, destination, record=None):
    marker = Path(root) / ".obsidian"
    return destination is not None or marker.exists() or marker.is_symlink() or (
        record is not None and "market_name" in record
    )


def _relative(study, path):
    return path.relative_to(study.vault).as_posix()


def _key(data):
    return hashlib.sha256(json.dumps(data, ensure_ascii=False, sort_keys=True,
                                   separators=(",", ":"), allow_nan=False).encode()).hexdigest()


def _history_scope(study, quarter, role, company=None):
    return [study.identifier, quarter, role, company]


def _history(text, scope):
    _, marker, trailing = notes.managed_body(text).partition(_HISTORY_START)
    encoded, end, after = trailing.partition(_HISTORY_END)
    if not marker or not end or (after and not after.startswith("\n")) or _HISTORY_START in trailing:
        raise ValueError("Missing or ambiguous industry note history")
    envelope = json.loads(encoded)
    if not isinstance(envelope, dict) or set(envelope) not in (
        {"scope", "data"}, {"hash", "data"},
    ):
        raise ValueError("Invalid industry note history")
    # Legacy envelopes have no explicit scope. Their note path, properties,
    # and linked revisions still have to agree with the requested study.
    if "scope" in envelope and envelope["scope"] != scope:
        raise ValueError("Industry note history belongs to a different study or note")
    return envelope["data"]


def _pack_history(visible, data, scope):
    visible = visible.rstrip()
    if _HISTORY_START in visible:
        raise ValueError("Unexpected history marker in research text")
    envelope = {"scope": scope, "data": data}
    return visible + _HISTORY_START + _canonical_json(envelope) + _HISTORY_END


def _read_note(study, path):
    data = update.inspect(study.vault, [_relative(study, path)])[_relative(study, path)]
    return data.decode("utf-8") if data is not None else None


def _note_for(study, quarter, role, company=None, name=None):
    return notes.note_path(study, role, quarter=quarter, company=company, company_name=name)


def _decode_parts(study, quarter, version, loaded):
    for ref in version["parts"]:
        role, company = ref["role"], ref.get("company")
        identity = role, company
        if identity in loaded:
            continue
        path = _note_for(study, quarter, role, company)
        text = _read_note(study, path)
        if text is None:
            raise ValueError(f"Missing linked industry note: {path}")
        scope = _history_scope(study, quarter, role, company)
        items = _history(text, scope)
        if not isinstance(items, dict):
            raise ValueError(f"Invalid material history in {path}")
        loaded[identity] = items, text


def _record_from_version(study, quarter, version, loaded):
    if not isinstance(version, dict):
        raise ValueError("Invalid industry quarter index")
    record = {key: version[key] for key in ("revision", "cutoff", "updated", "overview", "pending")}
    record.update(market=study.identifier, quarter=quarter)
    companies = []
    roles = set()
    for ref in version["parts"]:
        role, company = ref["role"], ref.get("company")
        identity = role, company
        if identity in roles:
            raise ValueError("Duplicate linked industry note")
        roles.add(identity)
        item = loaded[identity][0][ref["version"]]
        if role == "company":
            companies.append({"company": company, "name": ref["name"], "body": item["body"]})
        else:
            if role not in _ROLES or set(item) - set(_ROLE_FIELDS[role]):
                raise ValueError("Invalid industry note role content")
            record.update(item)
    if companies:
        record["companies"] = companies
    _validate(record, study.identifier, quarter, version["revision"])
    _validate_industry_outlook(record)
    return record


def _quarter_history(study, quarter, *, issues=None):
    overview = _note_for(study, quarter, "overview")
    text = _read_note(study, overview)
    if text is None:
        return overview, text, [], {}, []
    index = _history(text, _history_scope(study, quarter, "overview"))
    if not isinstance(index, list) or not index:
        raise ValueError("Invalid industry quarter index")
    loaded, records = {}, []
    for revision, entry in enumerate(index, 1):
        try:
            if not isinstance(entry, dict) or entry.get("revision") != revision:
                raise ValueError("Industry quarter revisions must be contiguous")
            _decode_parts(study, quarter, entry, loaded)
            records.append(_record_from_version(study, quarter, entry, loaded))
        except (ValueError, OSError, AttributeError, KeyError, TypeError) as error:
            if issues is None:
                raise
            issues.append(f"r{revision}: {error}")
    return overview, text, index, loaded, records


def _split_parts(record):
    parts = {}
    for role in _ROLES:
        item = {field: record[field] for field in _ROLE_FIELDS[role] if field in record}
        if item:
            parts[(role, None)] = item, None
    for entry in record.get("companies", []):
        identity = ("company", entry["company"])
        if identity in parts or not isinstance(entry["body"], str) or not entry["body"].strip():
            raise ValueError("Invalid or duplicate company research note")
        parts[identity] = {"body": entry["body"]}, entry.get("name", entry["company"])
    return parts


def _material_text(role, item, sources_heading):
    text = item[_ROLE_FIELDS[role][0]]
    if role == "size-share":
        claims = "\n".join(f"- {claim['text']}" for claim in item["claims"].values())
        sources = "\n".join(
            f"- {key}: {source.get('url', '')} — {source.get('locator', '')} "
            f"({source.get('published_at', '')})" for key, source in item["sources"].items()
        )
        return f"{text}\n\n{claims}\n\n## {sources_heading}\n\n{sources}"
    if role == "outlook":
        forecasts = "\n".join(
            f"- {forecast.get('version')}: {forecast.get('value')} {forecast.get('unit')} "
            f"({forecast.get('target_period')})" for forecast in item.get("forecasts", [])
        )
        return f"{text}\n\n{forecasts}"
    return text


def _part_body(study, role, current, history, earlier, scope):
    _, _, revisions, sources, prior, edited = _DISPLAYS[study.language]
    sections = [_material_text(role, current, sources)]
    if earlier:
        sections.append(f"## {revisions}")
        for key, revision, cutoff, updated in earlier:
            sections.append(f"### {prior} {revision} · {cutoff} · {edited} {updated}\n\n"
                            + _material_text(role, history[key], sources))
    return _pack_history("\n\n".join(sections), history, scope)


_OBSERVATION_SERIES = ("scope", "metric", "unit", "target_period")


def _observation_identity(row):
    return (row.get("version"), *(row.get(key) for key in _OBSERVATION_SERIES))


def _observations_by_identity(record, field):
    observations = {}
    for item in record.get(field, []):
        version = item.get("version")
        if not isinstance(version, str) or not version.strip():
            raise ValueError(f"Each {field} observation needs an exact version")
        if any(not isinstance(item.get(key), str) or not item[key].strip()
               for key in _OBSERVATION_SERIES) or not _number(item.get("value")):
            raise ValueError(f"Invalid {field} measurement or target: {version}")
        identity = _observation_identity(item)
        if identity in observations:
            raise ValueError(f"Duplicate {field} identity: {identity}")
        observations[identity] = item
    return observations


def _validate_industry_outlook(record):
    forecasts = _observations_by_identity(record, "forecasts")
    actuals = _observations_by_identity(record, "actuals")
    sources, cutoff = record["sources"], record["cutoff"]
    pairs = set()
    for submitted in record.get("comparisons", []):
        if not isinstance(submitted, dict):
            raise ValueError("Expected an exact forecast comparison")
        forecast_id = submitted.get("forecast_version")
        matches = [key for key in forecasts if key[0] == forecast_id]
        if len(matches) != 1:
            raise ValueError(f"Comparison forecast is unknown or ambiguous: {forecast_id}")
        key, = matches
        forecast = forecasts[key]
        if submitted.get("status") == "compared":
            actual_id = submitted.get("actual_version")
            actual = actuals.get((actual_id, *key[1:]))
            if actual is None or not _number(submitted.get("error")):
                raise ValueError(f"Comparison requires an exact actual and numeric error: {actual_id}")
            outcomes = [compare_forecast(forecast, actual, sources, cutoff)]
        else:
            actual_id = None
            outcomes = []
            if not any(actual_key[1:] == key[1:] for actual_key in actuals):
                outcomes.append(compare_forecast(forecast, None, sources, cutoff))
                if actuals:
                    mismatched = next(iter(actuals.values()))
                    outcomes.append(compare_forecast(forecast, mismatched, sources, cutoff))
        pair = forecast_id, actual_id
        if pair in pairs or submitted not in outcomes:
            raise ValueError(f"Comparison does not match its exact inputs: {forecast_id}")
        pairs.add(pair)


def _check_version_identity(record, history):
    for old in history:
        for key, source in record["sources"].items():
            if key in old["sources"] and old["sources"][key] != source:
                raise ValueError(f"Source version was rebound: {key}")
        for field in ("forecasts", "actuals"):
            old_items = {_observation_identity(item): item for item in old.get(field, [])}
            for item in record.get(field, []):
                key = _observation_identity(item)
                if key in old_items and item != old_items[key]:
                    raise ValueError(f"{field} version was rebound: {key}")


def _previous_quarter(quarter):
    number = _quarter_number(quarter)
    if number > 1:
        return f"{quarter[:4]}Q{number - 1}"
    year = int(quarter[:4])
    return f"{year - 1:04d}Q4" if year else None


def _saved_overview_cutoff(study, quarter):
    try:
        text = _read_note(study, _note_for(study, quarter, "overview"))
        if text is not None:
            return _boundary(notes.parse_note(text).get("as_of"))
    except (ValueError, OSError):
        return None


def _check_carry_forward(study, record, destination):
    compared_ids = {comparison["forecast_version"] for comparison in record.get("comparisons", [])}
    previous = _previous_quarter(record["quarter"])
    if not compared_ids or previous is None:
        return
    cutoff = _boundary(record["cutoff"])
    history, issues = _available_records(study.vault, study.identifier, previous, destination)
    prior = {}
    for old, _ in history:
        if _boundary(old["cutoff"]) <= cutoff:
            for forecast in old.get("forecasts", []):
                version = forecast.get("version")
                if version in compared_ids:
                    prior.setdefault(version, []).append((forecast, old["sources"]))
    prior_cutoff = _saved_overview_cutoff(study, previous) if issues else None
    for forecast in record.get("forecasts", []):
        version = forecast["version"]
        if issues and version in compared_ids and version not in prior:
            # Releases strictly newer than the saved overview could not
            # have been sources for a forecast in that overview.
            sources = [record["sources"][key] for key in forecast["source_ids"]]
            if prior_cutoff is None or not all(
                _provenance_available(source) and _boundary(source["published_at"]) > prior_cutoff
                for source in sources
            ):
                raise ValueError(f"Cannot verify prior forecast {version} for {previous}: {issues[0]}")
        if version in prior and not any(
            earlier == forecast and all(
                sources.get(source_id) == record["sources"].get(source_id)
                for source_id in forecast["source_ids"]
            )
            for earlier, sources in prior[version]
        ):
            raise ValueError(f"Comparison changed a carried-forward forecast or release: {version}")


def _plan_industry_publication(study, record):
    quarter = record["quarter"]
    overview, previous, index, histories, records = _quarter_history(study, quarter)
    if record["revision"] != len(index) + 1:
        raise ValueError(f"Expected industry quarter revision {len(index) + 1}")
    if records and _boundary(record["cutoff"]) < _boundary(records[-1]["cutoff"]):
        raise ValueError("An in-place update cannot move the quarter cutoff backwards")
    _check_version_identity(record, records)
    changes = {}
    paths = []
    references = []
    parts = _split_parts(record)
    if index:
        for ref in index[-1]["parts"]:
            identity = ref["role"], ref.get("company")
            if identity not in parts:
                parts[identity] = histories[identity][0][ref["version"]], ref.get("name")
    props = {"quarter": quarter, "status": "partial" if record["pending"] else "complete",
             "as_of": record["cutoff"], "updated": record.get("updated", date.today().isoformat())}
    for (role, company), (item, name) in parts.items():
        path = _note_for(study, quarter, role, company, name)
        paths.append(path)
        scope = _history_scope(study, quarter, role, company)
        ref = {"role": role, "version": _key([scope, item])}
        if company:
            ref.update(company=company, name=name)
        references.append(ref)
        history, verified_text = histories.get((role, company), ({}, None))
        old_text = _read_note(study, path)
        if old_text != verified_text and (
            old_text is None or verified_text is None
            or notes.managed_body(old_text) != notes.managed_body(verified_text)
        ):
            raise ValueError(f"Linked industry note changed during publication: {path}")
        key = ref["version"]
        prior_refs = [
            (entry["version"], version["revision"], version["cutoff"], version["updated"])
            for version in index for entry in version["parts"]
            if entry["role"] == role and entry.get("company") == company
            and entry["version"] != key
        ]
        earlier = list({entry[0]: entry for entry in reversed(prior_refs)}.values())
        history = {**history, key: item}
        updated = notes.render_note(study, role, _part_body(study, role, item, history, earlier, scope),
                                    company=company, company_name=name, existing=old_text, **props)
        changes[path] = old_text, updated

    project = notes.note_path(study, "project")
    if _read_note(study, project) is None:
        changes[project] = None, notes.render_note(
            study, "project", record.get("project_overview", record["overview"]),
        )
    summaries, pending, revisions, _, prior, edited = _DISPLAYS[study.language]
    planned = (*paths, project)
    body = [record["overview"], f"## {summaries}",
            f"- {notes.note_link(study, project, planned=planned)}"]
    body.extend(f"- {notes.note_link(study, path, planned=planned)}" for path in paths)
    if record["pending"]:
        body.extend((f"## {pending}", "\n".join(f"- {item}" for item in record["pending"])))
    changes_to_overview = [
        f"### {prior} {entry['revision']} · {entry['cutoff']} · {edited} {entry['updated']}\n\n"
        f"{entry['overview']}"
        for entry in index if entry["overview"] != record["overview"]
    ]
    if changes_to_overview:
        body.extend((f"## {revisions}", *changes_to_overview))
    index = [*index, {key: record[key] for key in ("revision", "cutoff", "overview", "pending")}]
    index[-1].update(parts=references, updated=props["updated"])
    rendered = notes.render_note(study, "overview", _pack_history("\n\n".join(body), index,
                                               _history_scope(study, quarter, "overview")),
                                 existing=previous, **props)
    changes[overview] = previous, rendered
    return overview, changes


def publish(root, record, *, destination=None):
    """Publish same-path Obsidian notes, or keep the older explicit-root API."""
    if not _in_vault(root, destination, record):
        return _publish_legacy(root, record)
    _validate(record, record.get("market"), record.get("quarter"), record.get("revision"))
    _validate_industry_outlook(record)
    vault = Path(root).resolve()
    with update.read_barrier(vault):
        study = notes.identify_study(vault, record["market"], name=record.get("market_name"),
                                     language=record.get("language"), destination=destination)
        _check_carry_forward(study, record, destination)
        overview, changes = _plan_industry_publication(study, record)
    expected = {_relative(study, path): before.encode() if before is not None else None
                for path, (before, _) in changes.items()}
    intended = {_relative(study, path): after.encode() for path, (_, after) in changes.items()}
    def check_scope():
        current = notes.identify_study(vault, study.identifier, name=study.name,
                                       language=study.language, destination=destination)
        if current != study:
            raise update.UpdateConflict(f"Study identity changed before publication: {study.path}")

    update.apply(vault, expected, intended, check_scope=check_scope)
    return overview


def _available_records(root, market, quarter, destination):
    vault = Path(root).resolve()
    path = notes.resolve_study(vault, market, destination=destination)
    _quarter_number(quarter)
    legacy, issues = _snapshots(notes._inside(vault, path / quarter, directory=True))
    if destination is None:
        older, older_issues = _snapshots(_scope(vault, market, quarter))
        legacy.extend(older)
        issues.extend(older_issues)
    if not path.exists():
        return legacy, issues
    try:
        if not list(notes._notes(path, "project")):
            if not legacy and any(path.iterdir()):
                issues.append(f"Existing destination has no matching industry study: {path}")
            return legacy, issues
        study = notes.identify_study(vault, market, destination=destination)
        overview, _, _, _, records = _quarter_history(study, quarter, issues=issues)
    except (ValueError, OSError, AttributeError, KeyError, TypeError) as error:
        return legacy, [*issues, str(error)]
    candidates = [(record, overview) for record in reversed(records)] + legacy
    candidates.sort(key=lambda item: (_boundary(item[0]["cutoff"]), item[0]["revision"]), reverse=True)
    return candidates, issues


def resume(root, market, quarter, cutoff=None, *, destination=None):
    if not _in_vault(root, destination):
        return _resume_legacy(root, market, quarter, cutoff)
    boundary = _boundary(cutoff) if cutoff is not None else None
    with update.read_barrier(Path(root).resolve()):
        candidates, issues = _available_records(root, market, quarter, destination)
        for record, path in candidates:
            if boundary is None or _boundary(record["cutoff"]) <= boundary:
                return {"record": record, "review": str(path), "issues": issues}
    return {"record": None, "review": None, "issues": issues}


def cite(root, market, quarter, claim_id, cutoff, *, destination=None):
    if not _in_vault(root, destination):
        return _cite_legacy(root, market, quarter, claim_id, cutoff)
    boundary = _boundary(cutoff)
    with update.read_barrier(Path(root).resolve()):
        candidates, _ = _available_records(root, market, quarter, destination)
        # Committed views made at or before the cutoff are preferred. A later
        # reconstruction can still supply a claim if all releases were available.
        candidates.sort(key=lambda item: _boundary(item[0]["cutoff"]) > boundary)
        for record, path in candidates:
            claim = record["claims"].get(claim_id)
            if claim is None or not claim_is_eligible(claim, record["sources"], cutoff):
                continue
            sources = {key: record["sources"][key] for key in claim["source_ids"]}
            if not all(_provenance_available(source) for source in sources.values()):
                continue
            return {"claim": claim, "sources": sources, "review": str(path),
                    "market": market, "quarter": quarter, "cutoff": cutoff,
                    "snapshot_cutoff": record["cutoff"],
                    "claim_version": _key([market, quarter, claim_id, claim, sources]),
                    "retrospective": _boundary(record["cutoff"]) > boundary}
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
    for key in ("scope", "metric", "unit", "definition"):
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
    publish_command = commands.add_parser("publish")
    publish_command.add_argument("root")
    publish_command.add_argument("--destination")
    commands.add_parser("recover").add_argument("root")
    for name in ("resume", "cite"):
        command = commands.add_parser(name)
        command.add_argument("root")
        command.add_argument("market")
        command.add_argument("quarter")
        command.add_argument("--destination")
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
            result = {"review": str(publish(args.root, json.load(sys.stdin), destination=args.destination))}
        elif args.command == "resume":
            result = resume(args.root, args.market, args.quarter, args.cutoff, destination=args.destination)
        elif args.command == "cite":
            result = cite(args.root, args.market, args.quarter, args.claim_id, args.cutoff,
                          destination=args.destination)
        elif args.command == "recover":
            result = {"recovered": update.recover(notes._vault_root(args.root))}
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
