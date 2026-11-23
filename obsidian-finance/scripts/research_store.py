"""Bounded investing discovery and append publication; see README's v1 contract."""

from contextlib import contextmanager
import fcntl
import importlib.util
import json
import os
from pathlib import Path
import re
from hashlib import sha256
import stat
from tempfile import TemporaryDirectory
from urllib.parse import quote
from datetime import date, datetime, time

_spec = importlib.util.spec_from_file_location("assess_work", Path(__file__).with_name("assess_work.py"))
_adapter = importlib.util.module_from_spec(_spec)
exec(compile(_spec.loader.get_source("assess_work"), _spec.origin, "exec"), _adapter.__dict__)


_markdown_spec = importlib.util.spec_from_file_location("research_markdown", Path(__file__).with_name("research_markdown.py"))
_markdown = importlib.util.module_from_spec(_markdown_spec)
_markdown_spec.loader.exec_module(_markdown)

_update_spec = importlib.util.spec_from_file_location("industry_update", Path(__file__).with_name("industry_update.py"))
_update = importlib.util.module_from_spec(_update_spec)
_update_spec.loader.exec_module(_update)

_REPORT_LABELS = {
    "quarter-overview": "00 Research Overview",
    "financial-analysis": "01 Financial Analysis",
    "operating-analysis": "02 Operating Analysis",
    "industry-and-competition": "03 Industry and Competition",
    "forward-forecast": "04 Forward Forecast",
    "valuation-and-risk": "05 Valuation and Risk",
    "technical-analysis": "06 Technical Analysis",
    "synthesis": "99 Investment Synthesis",
}


def _require(value, message):
    if not value:
        raise ValueError(message)


def _id(value):
    _require(isinstance(value, str) and re.fullmatch(r"[a-zA-Z0-9_-]+", value), "ambiguous identity")
    return value


def _open(root, reference, directory=False, *, quarter_relative=False):
    path = Path(reference)
    _require(not path.is_absolute() and path.parts and ".." not in path.parts
             and (quarter_relative or path.parts[0] == "investing"), "escaping reference")
    fd = os.open("/", os.O_RDONLY | os.O_DIRECTORY)
    try:
        for part in Path(root).absolute().parts[1:]:
            child = os.open(part, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=fd)
            os.close(fd)
            fd = child
        for index, part in enumerate(path.parts):
            flags = os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK
            if directory or index < len(path.parts) - 1:
                flags |= os.O_DIRECTORY
            child = os.open(part, flags, dir_fd=fd)
            os.close(fd)
            fd = child
        return fd
    except BaseException:
        os.close(fd)
        raise


def _bytes(root, reference, *, quarter_relative=False):
    with os.fdopen(_open(root, reference, quarter_relative=quarter_relative), "rb") as stream:
        _require(stat.S_ISREG(os.fstat(stream.fileno()).st_mode), "regular local file required")
        return stream.read()


def _names(root, reference, *, quarter_relative=False):
    fd = _open(root, reference, True, quarter_relative=quarter_relative)
    try:
        return sorted(os.listdir(fd))
    finally:
        os.close(fd)


def _object(root, reference):
    data = _adapter._json(_bytes(root, reference).decode("utf-8"))
    _require(isinstance(data, dict) and type(data.get("version")) is int and data["version"] == 1,
             "unsupported metadata: supply version-1 investing metadata; existing notes remain unchanged")
    return data


def _registered_metadata(root, reference):
    if reference.endswith(".json"):
        return _object(root, reference)
    path = Path(reference)
    _require(path.suffix == ".md" and path.parent.name in ("sources", "analysis"),
             "unsupported research registration")
    asset = path.parts[3]
    kind = "source" if path.parent.name == "sources" else "method"
    payload = _bytes(root, reference)
    if len(path.parts) == 9 and path.parts[4] == "cycles" and re.fullmatch(r"[0-9a-f]{64}", path.stem):
        _require(sha256(payload).hexdigest() == path.stem, "quarter registration digest mismatch")
    props, record = _markdown.record(payload.decode("utf-8"), kind + "-registration", asset_id=asset)
    _require(type(record.get("version")) is int and record["version"] == 1
             and props.get(kind + "_id") == record.get("id")
             and props.get(kind + "_version") == record.get("identity"),
             "Markdown research registration identity mismatch")
    if kind == "source" and "available_at" in props:
        _require(props["available_at"] == record.get("available_at"), "Markdown source availability mismatch")
    if len(path.parts) == 9 and path.parts[4] == "cycles":
        cycle = "/".join(path.parts[:6])
        fields = ("raw_ref", "original_ref") if kind == "source" else ("content_ref",)
        for field in fields:
            if field in record:
                ref = Path(record[field])
                _require(not ref.is_absolute() and ref.parts and ref.parts[0] == "data"
                         and ".." not in ref.parts, "quarter registration requires local evidence")
                record[field] = cycle + "/" + record[field]
    return record


def _research_config(root):
    try:
        note = _bytes(root, "investing/index.md").decode("utf-8")
    except FileNotFoundError:
        return _object(root, "investing/research.json")
    if not _markdown.declares_role(note, "research-overview"):
        return _object(root, "investing/research.json")
    _, record = _markdown.record(note, "research-overview")
    _require(type(record.get("version")) is int and record["version"] == 1,
             "unsupported Markdown research configuration")
    return record


def _managed_directories(root, path):
    """Skip regular notes while preserving unsafe paths and legacy diagnostics."""
    entries = []
    fd = _open(root, path, True)
    try:
        for name in sorted(os.listdir(fd)):
            if name.endswith(".md") or name == "data":
                mode = os.stat(name, dir_fd=fd, follow_symlinks=False).st_mode
                if (name.endswith(".md") and stat.S_ISREG(mode)) or (name == "data" and stat.S_ISDIR(mode)):
                    continue
            entries.append(name)
    finally:
        os.close(fd)
    return entries


def _asset_metadata(root, base):
    marked = []
    for name in _names(root, base):
        if name.endswith(".md"):
            note = _bytes(root, base + "/" + name).decode("utf-8")
            if _markdown.declares_role(note, "asset-entry"):
                marked.append(note)
    _require(len(marked) <= 1, "duplicate Markdown asset entries")
    if not marked:
        return _object(root, base + "/asset.json")
    asset = base.rsplit("/", 1)[1]
    _, record = _markdown.record(marked[0], "asset-entry", asset_id=asset)
    _require(type(record.get("version")) is int and record["version"] == 1
             and record.get("id") == asset and _adapter._text(record.get("issuer")),
             "Markdown asset identity mismatch")
    try:
        legacy = _object(root, base + "/asset.json")
    except FileNotFoundError:
        return record
    _require(legacy.get("id") == asset and legacy.get("issuer") == record["issuer"],
             "Markdown and legacy asset identities differ")
    return record


def _verification(root, unit):
    value = unit["verification"]
    if isinstance(value, dict):
        _require(type(value.get("version")) is int and value["version"] == 1, "invalid inline verification version")
        return value
    return _object(root, value)


def _unique(items, key="id"):
    result = {}
    for item in items:
        identity = _id(item[key])
        _require(identity not in result, "duplicate identity " + identity)
        result[identity] = item
    return result


def _available(value, cutoff):
    try:
        return (datetime.combine(date.fromisoformat(value), time(23, 59, 59), cutoff.tzinfo)
                if len(value) == 10 else _adapter._core._instant(value))
    except (ValueError, TypeError, AttributeError):
        return None


def _source_versions(local, cutoff):
    groups = {}
    seen = set()
    for source in local:
        sid = _id(source["id"])
        identity = (sid, source["version"])
        _require(identity not in seen, "duplicate source revision")
        seen.add(identity)
        if source.get("kind") == "financial_original":
            _require(all(previous.get("fiscal") == source.get("fiscal") for previous in groups.get(sid, [])), "financial source identity crosses fiscal quarters")
        groups.setdefault(sid, []).append(source)
    result = []
    for sid, revisions in groups.items():
        eligible = [(stamp, source) for source in revisions
                    if (stamp := _available(source.get("available_at"), cutoff)) is not None and stamp <= cutoff]
        if eligible:
            latest = max(stamp for stamp, _ in eligible)
            selected = [s for stamp, s in eligible if stamp == latest]
            _require(len(selected) == 1, "ambiguous source publication order: " + sid)
            result.extend(selected)
        for source in revisions:
            stamp = _available(source.get("available_at"), cutoff)
            if stamp is None or stamp > cutoff:
                # Keep excluded or unverifiable revisions visible without replacing
                # the stable identity of an eligible historical original.
                if len(revisions) > 1:
                    source["id"] = sid + "@" + sha256(str(source["version"]).encode()).hexdigest()
                result.append(source)
    return result


def _required(question, quarter):
    return [_id(sid.replace("{fiscal}", quarter)) for sid in question["required_sources"]]


def _required_all(questions, asset, quarter):
    return sorted({asset + ":" + sid for q in questions.values() for sid in _required(q, quarter)})


_ANALYSIS_FIELDS = {"kind", "version", "authored_at", "projection", "content_ref", "content_digest"}


def _analysis_identity(frozen):
    _require(isinstance(frozen, dict) and set(frozen) == _ANALYSIS_FIELDS, "frozen analysis identity")
    _require(frozen["kind"] in ("method", "assumption"), "local analysis identity/kind")
    _adapter._timestamp(frozen["authored_at"])
    _require(all(_adapter._text(frozen[key]) for key in ("version", "content_ref", "content_digest")),
             "frozen analysis content/version")


def _completion_valid(check, output_digest):
    checks = check.get("checks", {})
    return (output_digest is not None and isinstance(checks, dict)
            and set(checks) == {"sources", "citations", "calculations", "counterevidence"}
            and all(value is True for value in checks.values()) and check.get("unresolved") == []
            and output_digest == check.get("output_digest"))


def _current_method(root, base, quarter, identity, gaps):
    """Choose the newest authored version, coalescing equivalent located copies."""
    reference = base + "/data/analysis/" + identity
    candidates = []
    for extension in (".md", ".json"):
        try:
            candidates.append((False, _registered_metadata(root, reference + extension)))
        except FileNotFoundError:
            continue
        break
    for path in _metadata_paths(root, base + "/cycles/" + quarter + "/data/analysis"):
        try:
            metadata = _registered_metadata(root, path)
            _id(metadata["id"])
            _adapter._timestamp(metadata["authored_at"])
        except (OSError, ValueError, KeyError, TypeError) as error:
            gap = dict(record=path, evidence="quarter-method",
                       reason="Invalid quarter method: " + str(error),
                       recovery="Preserve damaged bytes and reverify the exact local version")
            if gap not in gaps:
                gaps.append(gap)
            continue
        if metadata.get("id") == identity:
            candidates.append((True, metadata))
    if not candidates:
        raise FileNotFoundError(reference)

    authored = [(_adapter._core._instant(record["authored_at"]), localized, record)
                for localized, record in candidates]
    newest = max(timestamp for timestamp, _, _ in authored)
    versions = [(localized, record) for timestamp, localized, record in authored if timestamp == newest]
    localized, selected = versions[0]
    if len(versions) > 1:
        location_fields = {"content_ref", "origin_reference"}
        selected_metadata = {key: val for key, val in selected.items() if key not in location_fields}
        for _, record in versions:
            comparable = {key: val for key, val in record.items() if key not in location_fields}
            _require(_adapter._core._same_json(comparable, selected_metadata)
                     and sha256(_bytes(root, record["content_ref"])).hexdigest() == record["content_digest"],
                     "ambiguous quarter method version: " + identity)
    return localized, selected


def _analysis_valid(root, base, quarter, required, consumed, record, gaps):
    """Local analysis authorship is not economic publication eligibility."""
    fields = _ANALYSIS_FIELDS
    _require(isinstance(consumed, dict), "analysis_inputs object")
    valid = True
    for identity in sorted(set(required) | consumed.keys()):
        _id(identity)
        frozen = consumed.get(identity)
        if frozen is not None:
            _analysis_identity(frozen)
        try:
            localized, metadata = _current_method(root, base, quarter, identity, gaps)
            _require(metadata.get("id") == identity and metadata.get("kind") in ("method", "assumption"), "local analysis identity/kind")
            _require(not {"available_at", "fiscal", "raw_ref"} & metadata.keys(), "economic evidence cannot be a local analysis input")
            _adapter._timestamp(metadata["authored_at"])
            _require(_adapter._text(metadata.get("identity")), "local analysis version")
            current = {key: metadata[key] for key in fields - {"version"}}
            current["version"] = metadata["identity"]
            content = _bytes(root, metadata["content_ref"])
            if localized and frozen is not None:
                # A captured method copy has a new location and the same frozen bytes.
                current["content_ref"] = frozen["content_ref"]
            matches = (sha256(content).hexdigest() == metadata["content_digest"]
                       and frozen is not None and _adapter._core._same_json(frozen, current))
        except FileNotFoundError:
            matches = False
        if not matches:
            valid = False
            gaps.append(dict(record=record, evidence="analysis:" + identity,
                reason="Local analysis input is missing, changed or not bound to this unit",
                recovery="Review the actual authored method/assumption and recompute dependent analysis; never backdate economic availability"))
    return valid


_LEGACY_REVIEW_MARKERS = frozenset({"review.json", "pending.json", "withdrawn.json", "abandoned.json"})
_QUARTER_NOTE = re.compile(r"investing/assets/equities/[^/]+/cycles/[0-9]{4}Q[1-4]/(?!index\.md$)[^/]+\.md")
_CITATION_FIELDS = ("path", "claim", "source_id", "source_version", "source_available_at")
_ROLE_MARKER = re.compile(
    r"(?:^|[,{])[ \t]*" + _markdown._SCALAR_STRING_TAG + r"""['"]?finance_role['"]?[ \t]*:[ \t]*"""
    + _markdown._SCALAR_STRING_TAG + r"""['"]?([a-z-]+)(?![\w-])""", re.M)


def _ordinary_quarter_note(path, payload):
    if not _QUARTER_NOTE.fullmatch(path):
        return False
    text = payload.decode("utf-8", errors="replace").lstrip("\ufeff")
    if not text.startswith(("---\n", "---\r\n")):
        return True
    header = re.split(r"\r?\n---(?:\r?\n|$)", text[3:], maxsplit=1)[0]
    try:
        properties = _markdown._mapping(header)
    except ValueError:
        pass
    else:
        if "finance_role" not in properties:
            return True
        role = properties["finance_role"]
        if isinstance(role, str) and role in _markdown._ROLE_FIELDS:
            return False
    # Keep recognizable declarations protected even if their YAML is truncated.
    return not any(match[1] in _markdown._ROLE_FIELDS for match in _ROLE_MARKER.finditer(header))


def _note_references(root, base, quarter):
    path = base + "/cycles/" + quarter
    try:
        fd = _open(root, path, True)
    except FileNotFoundError:
        return []
    try:
        return [path + "/" + name for name in sorted(os.listdir(fd))
                if _QUARTER_NOTE.fullmatch(path + "/" + name)
                and stat.S_ISREG(os.stat(name, dir_fd=fd, follow_symlinks=False).st_mode)
                and _ordinary_quarter_note(path + "/" + name, _bytes(root, path + "/" + name))]
    finally:
        os.close(fd)


def _candidate_citations(unit):
    references = unit.get("candidate_notes", [])
    _require(isinstance(references, list), "candidate notes must be a list")
    for citation in references:
        _require(isinstance(citation, dict) and all(_adapter._text(citation.get(key)) for key in _CITATION_FIELDS),
                 "incomplete candidate note evidence")
    return references


def _without_candidate_digests(unit):
    _require(isinstance(unit, dict), "saved unit object")
    if "candidate_notes" not in unit:
        return unit
    citations = [{key: value for key, value in citation.items() if key != "digest"}
                 for citation in _candidate_citations(unit)]
    return dict(unit, candidate_notes=citations)


def _dependent_work(questions, work):
    affected = {work}
    while True:
        downstream = {qid for qid, question in questions.items()
                      if affected.intersection(question.get("depends_on", []))}
        if downstream <= affected:
            return sorted(affected - {work})
        affected.update(downstream)


def _candidate_sources_valid(base, quarter, cutoff, unit, sources):
    cycle = base + "/cycles/" + quarter + "/"
    for citation in _candidate_citations(unit):
        source_id = _id(citation["source_id"])
        source = sources.get(source_id, {})
        fiscal = source.get("fiscal", {})
        published = _available(source.get("available_at"), cutoff)
        bound = unit.get("consumed", {}).get(source_id, {})
        if (not citation["path"].startswith(cycle) or not _QUARTER_NOTE.fullmatch(citation["path"])
                or not published or published > cutoff
                or f"{fiscal.get('year', '')}{fiscal.get('period', '')}" != quarter
                or citation["source_available_at"] != source["available_at"]
                or citation["source_version"] != source.get("version")
                or bound.get("version") != source.get("version")
                or not _adapter._core._same_json(bound.get("projection"), source.get("projection"))):
            return False
    return True


def _fixed_notes(root, cycle, asset, quarter):
    notes = {}
    try:
        names = _names(root, cycle)
    except FileNotFoundError:
        return notes
    for name in names:
        if not name.endswith(".md"):
            continue
        path = cycle + "/" + name
        raw = _bytes(root, path)
        text = raw.decode("utf-8", errors="replace")
        for role, label in _REPORT_LABELS.items():
            if not _markdown.declares_role(text, role):
                continue
            props, _ = _markdown.parse_note(text, role, asset_id=asset, fiscal_quarter=quarter)
            _require(role not in notes, "duplicate quarterly note role: " + role)
            suffix = " - " + label + ".md"
            _require(name.startswith(quarter + " ") and name.endswith(suffix),
                     "invalid fixed quarterly filename: " + name)
            notes[role] = (path, raw, props)
    return notes


def _fixed_record(notes):
    _require("quarter-overview" in notes, "missing fixed quarterly overview")
    path, raw, props = notes["quarter-overview"]
    _, review = _markdown.record(raw.decode("utf-8"), "quarter-overview")
    for field in ("publication", "reports", "research", "requirements", "units", "quarter_evidence"):
        _require(isinstance(review.get(field), dict), "quarterly overview requires a mapping for " + field)
    _require(all(isinstance(question, dict) for question in review["requirements"].values()),
             "invalid quarterly overview requirement")
    bindings = review["quarter_evidence"].get("units")
    _require(isinstance(bindings, dict) and bindings.keys() == review["units"].keys(),
             "invalid quarterly overview evidence mappings")
    paths = set()
    for qid, unit in review["units"].items():
        _require(isinstance(unit, dict) and isinstance(unit.get("analysis_inputs", {}), dict)
                 and isinstance(unit.get("consumed", {}), dict), "invalid quarterly overview unit: " + qid)
        _candidate_citations(unit)
        _require(isinstance(bindings[qid], dict) and isinstance(bindings[qid].get("methods"), dict),
                 "invalid quarterly overview method bindings: " + qid)
        for method in unit.get("analysis_inputs", {}).values():
            _analysis_identity(method)
        if "output" in unit:
            output = unit["output"]
            _require(isinstance(output, dict) and _adapter._text(output.get("path")),
                     "invalid quarterly overview output: " + qid)
            paths.add(output["path"])
    reports = {role: Path(note[0]).name for role, note in notes.items() if role != "quarter-overview"}
    _require(type(review.get("version")) is int and review["version"] == 1
             and review["id"] == props["review_id"] and review["cutoff"] == props["as_of"]
             and type(review["publication"]["complete"]) is bool
             and props["status"] == ("complete" if review["publication"]["complete"] else "partial")
             and review["reports"] == reports, "quarterly overview and reports disagree")
    prefix = Path(path).name.removesuffix(" - 00 Research Overview.md")
    for role, name in reports.items():
        report_props = notes[role][2]
        _require(name == f"{prefix} - {_REPORT_LABELS[role]}.md" and report_props["status"] != "draft"
                 and _adapter._core._instant(report_props["as_of"]) <= _adapter._core._instant(review["cutoff"]),
                 "invalid report identity or cutoff: " + name)
    _require(paths <= set(reports.values()), "quarterly overview refers to an unowned output")
    return path, review


def _fixed_reviews(root, base, quarter, cutoff, mode, gaps, proposed, invalid_units):
    if proposed is not None:
        return [proposed]
    asset = base.rsplit("/", 1)[1]
    cycle = base + "/cycles/" + quarter
    try:
        notes = _fixed_notes(root, cycle, asset, quarter)
        if not notes:
            return []
        path, review = _fixed_record(notes)
        instant = _adapter._core._instant(review["cutoff"])
        if instant > cutoff or (mode == "historical" and instant != cutoff):
            gaps.append(dict(record=path, evidence="historical review",
                reason="No complete saved report state for the requested earlier cutoff",
                recovery="Inspect the dated report revisions and rebuild only from eligible local sources"))
            return []
        damaged = {}
        _verify_fixed_evidence(Path(root) / cycle, asset, quarter, review, damaged=damaged)
        if invalid_units is not None:
            invalid_units[path] = damaged
        for qid, error in damaged.items():
            gaps.append(dict(record=path, evidence="quarter-unit:" + qid,
                reason=str(error), recovery="Recheck the affected report or its exact quarter data"))
        return [(path, _rebase_review(review, cycle, portable=False))]
    except (OSError, ValueError, KeyError, TypeError) as error:
        gaps.append(dict(record=cycle, evidence="quarterly overview", reason=str(error),
            recovery="Preserve existing notes and resolve the missing or inconsistent quarterly record"))
        return []


def _reviews(root, base, quarter, cutoff, mode, gaps, proposed=None, *,
             invalid_units=None, repairable_gaps=None, quarterly=False):
    if quarterly:
        return _fixed_reviews(root, base, quarter, cutoff, mode, gaps, proposed, invalid_units)
    gaps_start = len(gaps)
    saved = {}
    withdrawn = set()
    unusable = set()
    try:
        directories = _managed_directories(root, base + "/cycles/" + quarter)
    except FileNotFoundError:
        _require(proposed is not None, "missing quarter directory")
        directories = []
    for directory in directories:
        _id(directory)
        path = base + "/cycles/" + quarter + "/" + directory
        try:
            markdown = _bytes(root, path + "/review.md")
        except FileNotFoundError:
            pass
        except (OSError, ValueError) as error:
            gaps.append(dict(record=path + "/review.md", evidence="reviews", reason="Invalid Markdown review: " + str(error),
                recovery="Preserve the damaged marker and inspect the prior valid record"))
            continue
        else:
            try:
                asset = base.rsplit("/", 1)[1]
                props, review = _markdown.record(markdown.decode("utf-8"), "review",
                                                 asset_id=asset, fiscal_quarter=quarter)
                rid = _id(review["id"])
                complete = review.get("publication", {}).get("complete")
                _require(type(review.get("version")) is int and review["version"] == 1
                         and type(complete) is bool
                         and props.get("status") == ("complete" if complete else "partial")
                         and props.get("predecessor") == review.get("predecessor")
                         and props.get("review_id") == rid and props.get("as_of") == review["cutoff"]
                         and _target(asset, review)[1] == path, "Markdown review identity mismatch")
                _require(not _LEGACY_REVIEW_MARKERS &
                         set(_names(root, path)), "conflicting Markdown and legacy review")
            except (OSError, ValueError, KeyError, TypeError) as error:
                gaps.append(dict(record=path + "/review.md", evidence="reviews", reason="Invalid Markdown review: " + str(error),
                    recovery="Preserve the damaged marker and inspect the prior valid record"))
                continue

            # A valid envelope still establishes ancestry when its payload is damaged.
            _require(rid not in saved, "duplicate review identity")
            saved[rid] = (path, review)
            if invalid_units is not None:
                invalid_units[path] = {}
            try:
                if "quarter_evidence" in review:
                    cycle = base + "/cycles/" + quarter
                    damaged = {}
                    replay = _verify_quarter_evidence(Path(root) / cycle, asset, quarter, review, damaged=damaged)
                    review = _rebase_review(review, cycle, portable=False)
                    if damaged and not replay["reusable"]:
                        unusable.add(rid)
                    if invalid_units is not None:
                        invalid_units[path] = damaged
                    for qid, error in damaged.items():
                        gaps.append(dict(record=path, evidence="quarter-unit:" + qid,
                            reason=str(error), recovery="Restore the exact local evidence or recompute the affected unit"))
                else:
                    for unit in review["units"].values():
                        output = unit.get("output", {})
                        if output.get("path", "").startswith(path + "/"):
                            _require(sha256(_bytes(root, output["path"])).hexdigest() == output.get("digest")
                                     and _completion_valid(_verification(root, unit), output["digest"]),
                                     "published Markdown output is changed, incomplete or unverified")
            except (OSError, ValueError, KeyError, TypeError) as error:
                unusable.add(rid)
                gaps.append(dict(record=path, evidence="reviews", reason="Invalid Markdown review payload: " + str(error),
                    recovery="Preserve affected files and resume from an intact review"))
            else:
                saved[rid] = (path, review)
            continue
        try:
            pending = _object(root, path + "/pending.json")
        except FileNotFoundError:
            pending = None
        try:
            if pending is not None:
                actual = sha256(_bytes(root, path + "/review.json")).hexdigest()
                if actual != pending.get("review_digest"):
                    gaps.append(dict(record=path, evidence="publication:" + _id(pending["run"]),
                        reason="Publication metadata changed or incomplete; prior view retained",
                        recovery="Preserve conflicting bytes and draft; inspect the recorded run before retry"))
                    continue
            review = _object(root, path + "/review.json")
            rid = _id(review["id"])
            _adapter._timestamp(review["cutoff"])
            fiscal = review.get("fiscal")
            _require(_adapter._core._fiscal(fiscal)
                     and f"{fiscal['year']}{fiscal['period']}" == quarter
                     and isinstance(review.get("units"), dict), "invalid legacy review envelope")
        except FileNotFoundError:
            try:
                abandoned = _object(root, path + "/abandoned.json")
            except FileNotFoundError:
                abandoned = None
            if abandoned is not None and _rollback_valid(root, path, abandoned):
                continue
            gaps.append(dict(record=path, evidence="publication:" + _id(pending["run"]) if pending is not None else "publication",
                reason="Interrupted publication; prior research remains available",
                recovery="Use recover(root, run_id) to revalidate/resume or action='rollback' to abandon; preserve drafts"))
            continue
        except (OSError, ValueError, KeyError, TypeError) as error:
            gaps.append(dict(record=path + "/review.json", evidence="reviews", reason="Invalid legacy review: " + str(error),
                recovery="Preserve the damaged marker and inspect the prior valid record"))
            continue
        _require(rid not in saved, "duplicate review identity")
        saved[rid] = (path, review)
        try:
            marker = _object(root, path + "/withdrawn.json")
        except FileNotFoundError:
            marker = None
        if marker is not None:
            if _rollback_valid(root, path, marker):
                withdrawn.add(rid)
            else:
                gaps.append(dict(record=path, evidence="rollback", reason="Withdrawn research has user edits",
                    recovery="Preserve edited files and resolve the withdrawal conflict explicitly"))
    if proposed is not None:
        path, review = proposed
        _require(review["id"] not in saved, "duplicate review identity")
        saved[review["id"]] = (path, review)
    try:
        for rid, (_, review) in saved.items():
            trail = {rid}
            current = review
            while current.get("predecessor") is not None:
                previous = _id(current["predecessor"])
                _require(previous in saved and previous not in trail, "dangling or cyclic predecessor")
                trail.add(previous)
                parent = saved[previous][1]
                _require(parent["fiscal"] == review["fiscal"], "cross-quarter predecessor")
                _require(_adapter._core._instant(parent["cutoff"]) <= _adapter._core._instant(current["cutoff"]), "predecessor cutoff order")
                current = parent
        eligible = {rid: pair for rid, pair in saved.items() if rid not in withdrawn
                    and (_adapter._core._instant(pair[1]["cutoff"]) == cutoff if mode == "historical"
                        else _adapter._core._instant(pair[1]["cutoff"]) <= cutoff)}
        if (saved and not withdrawn and not eligible
                and len(gaps) == gaps_start
                and all(_adapter._core._instant(pair[1]["cutoff"]) > cutoff for pair in saved.values())):
            for _, review in saved.values():
                fiscal = review.get("fiscal")
                _require(_adapter._core._fiscal(fiscal)
                         and f"{fiscal['year']}{fiscal['period']}" == quarter, "fiscal directory mismatch")
                _require(isinstance(review.get("units"), dict)
                         and all(isinstance(unit, dict) for unit in review["units"].values()), "saved unit object")
                for unit in review["units"].values():
                    _require(isinstance(unit.get("consumed", {}), dict), "consumed identities")
                    for sid, identity in unit.get("consumed", {}).items():
                        _id(sid)
                        _require(isinstance(identity, dict) and set(identity) == {"version", "projection"}
                                 and _adapter._text(identity["version"]), "consumed identity")
                    _require(isinstance(unit.get("analysis_inputs", {}), dict), "analysis_inputs object")
                    for identity, frozen in unit.get("analysis_inputs", {}).items():
                        _id(identity)
                        _analysis_identity(frozen)
                    if "output" in unit:
                        output = unit["output"]
                        _require(isinstance(output, dict), "saved output object")
                        _require(sha256(_bytes(root, output["path"])).hexdigest() == output.get("digest"),
                                 "Future review output changed or incomplete")
                        _require("verification" in unit, "Future review completion evidence missing")
                        check = _verification(root, unit)
                        _require(_completion_valid(check, output["digest"]),
                                 "Future review completion evidence invalid or unbound")
            parents = {pair[1].get("predecessor") for pair in saved.values()}
            _require(sum(rid not in parents for rid in saved) == 1, "ambiguous competing future reviews")
            return []
        parents = {pair[1].get("predecessor") for pair in eligible.values()}
        leaves = [rid for rid in eligible if rid not in parents]
        _require(len(leaves) == 1, "missing cutoff review or ambiguous competing reviews")
        tip = leaves[0]
        while tip in unusable:
            tip = saved[tip][1].get("predecessor")
        if repairable_gaps is not None and tip == leaves[0]:
            ancestor = tip
            while ancestor is not None:
                path, older = saved[ancestor]
                for qid, error in invalid_units.get(path, {}).items():
                    if isinstance(error, _QuarterInputError):
                        units = older["units"]
                        affected = [qid, *_dependent_work(older["requirements"], qid)]
                        repairable_gaps[path, "quarter-unit:" + qid] = {
                            units[work]["output"]["path"] for work in affected
                            if work in units and "output" in units[work]
                        }
                ancestor = older.get("predecessor")
        return [eligible[tip]] if tip in eligible else []
    except (ValueError, FileNotFoundError) as error:
        gaps.append(dict(record=base + "/cycles/" + quarter, evidence="reviews", reason=str(error), recovery="Repair review metadata or provide the requested cutoff review; preserve existing research"))
        return []


def _metadata_paths(root, directory):
    try:
        return [directory + "/" + name for name in _names(root, directory)]
    except FileNotFoundError:
        return []


def _verify_source_payload(source, raw):
    _require(sha256(raw).hexdigest() == source["raw_digest"], "source raw digest mismatch")
    _require(source.get("raw_format") in ("json", "text"), "source raw_format")
    if source["raw_format"] == "json":
        _adapter._json(raw.decode("utf-8"))
    else:
        _require(isinstance(source.get("projection"), dict)
                 and source["projection"].get("raw_text") == raw.decode("utf-8"),
                 "free-text projection must retain full raw_text")


def _source_registration(root, path, issuer):
    source = _registered_metadata(root, path)
    _id(source["id"])
    _require(source.get("issuer") == issuer, "source issuer mismatch")
    _require(_adapter._text(source.get("kind")), "source kind")
    _require(source["kind"] not in ("method", "assumption"), "local analysis inputs must not be economic sources")
    _require("fiscal" not in source or isinstance(source["fiscal"], dict), "source fiscal")
    _require(source.get("identity") is None or _adapter._text(source["identity"]), "source identity")
    _require(source.get("available_at") is None or _adapter._text(source["available_at"]), "source availability")
    try:
        _verify_source_payload(source, _bytes(root, source["raw_ref"]))
    except (OSError, ValueError, TypeError) as error:
        raise ValueError(f"{source.get('raw_ref')}: {error}") from error
    if "original_ref" in source or "original_digest" in source:
        reference = source.get("original_ref")
        try:
            _require(sha256(_bytes(root, reference)).hexdigest() == source["original_digest"],
                     "source original digest mismatch")
        except (OSError, ValueError, TypeError, KeyError) as error:
            raise ValueError(f"{reference}: {error}") from error
    return source


def _source_catalog(root, base, issuer, quarters, gaps):
    """Load eligible source inputs and keep copied comparators out of cycle discovery."""
    by_key = {}
    native = set()
    company_paths = _metadata_paths(root, base + "/data/sources")
    paths = [(None, path) for path in company_paths]
    for quarter in quarters:
        paths.extend((quarter, path) for path in _metadata_paths(root, base + "/cycles/" + quarter + "/data/sources"))
    for quarter, path in paths:
        try:
            source = _source_registration(root, path, issuer)
        except (OSError, ValueError, KeyError, TypeError) as error:
            if quarter is None:
                raise
            gaps.append(dict(record=path, evidence="quarter-source",
                reason="Invalid quarter source: " + str(error),
                recovery="Preserve damaged bytes and reverify the exact local version"))
            continue
        source["version"] = source.pop("identity", None)
        key = (source["id"], source["version"])
        if key in by_key:
            _require(quarter is not None, "duplicate source revision")
            displaced = {"raw_ref", "original_ref", "origin_reference", "origin_raw_ref", "origin_original_ref"}
            _require(_adapter._core._same_json(
                {k: v for k, v in by_key[key].items() if k not in displaced},
                {k: v for k, v in source.items() if k not in displaced}), "conflicting source revision")
        else:
            by_key[key] = source
        fiscal = source.get("fiscal", {})
        if quarter is None or quarter == f"{fiscal.get('year', '')}{fiscal.get('period', '')}":
            native.add(key)
    return list(by_key.values()), native


def _snapshot(root, cutoff, mode, proposed=None, *, candidate_for=None, quarterly=False):
    config = _research_config(root)
    _require(isinstance(config.get("assets"), list) and config["assets"], "missing asset scope")
    assets = [_id(asset) for asset in config["assets"]]
    _require(len(set(assets)) == len(assets), "duplicate asset identity")
    sources, records, gaps, adopted_claims = [], [], [], []
    quarantined = set()
    for asset in assets:
        records_start = len(records)
        base = "investing/assets/equities/" + asset
        metadata = _asset_metadata(root, base)
        _require(metadata.get("id") == asset and _adapter._text(metadata.get("issuer")), "asset identity mismatch")
        issuer = metadata["issuer"]
        questions = _unique(metadata["questions"])
        _require(questions, "required questions missing")
        for question in questions.values():
            _require(_adapter._strings(question.get("required_sources")) and _adapter._strings(question.get("depends_on", [])), "question dependencies")
            _require(_adapter._strings(question.get("required_analysis", [])), "local analysis requirements")
            for identity in question.get("required_analysis", []):
                _id(identity)
            _require(set(question.get("depends_on", [])) <= questions.keys(), "unknown question dependency")
            _required(question, "2024Q1")  # Validate the sole literal template.
        try:
            quarters = _names(root, base + "/cycles")
        except FileNotFoundError:
            quarters = []
        if proposed is not None and proposed[0] == asset:
            quarters = sorted(set(quarters) | {proposed[1]})
        for quarter in quarters:
            _require(re.fullmatch(r"[0-9]{4}Q[1-4]", quarter), "invalid fiscal directory")
        local, native = _source_catalog(root, base, issuer, quarters, gaps)
        selected_sources = _source_versions(local, cutoff)
        by_source = {source["id"]: source for source in selected_sources}
        for source in selected_sources:
            sid = source["id"]
            source["id"] = asset + ":" + sid
            fiscal = source.get("fiscal", {})
            source_quarter = f"{fiscal.get('year', '')}{fiscal.get('period', '')}"
            source["consumers"] = [qid for qid, q in questions.items() if sid in _required(q, source_quarter)]
            sources.append(source)
        initial = {}
        initial_sources = {}
        ambiguous_initial = set()
        for source in selected_sources:
            available = _available(source.get("available_at"), cutoff)
            fiscal = source.get("fiscal")
            logical_id = source["id"].split(":", 1)[1]
            if ((logical_id, source["version"]) in native
                    and source["kind"] == "financial_original" and _adapter._core._fiscal(fiscal)
                    and available is not None and available <= cutoff
                    and fiscal["period_end"] <= source["available_at"][:10]):
                quarter = f"{fiscal['year']}{fiscal['period']}"
                initial_sources.setdefault(quarter, []).append(source["id"])
                if initial.setdefault(quarter, fiscal) != fiscal:
                    ambiguous_initial.add(quarter)
        for quarter in sorted(set(quarters) | initial.keys()):
            _require(re.fullmatch(r"[0-9]{4}Q[1-4]", quarter), "invalid fiscal directory")
            candidate = proposed[2:] if proposed is not None and proposed[:2] == (asset, quarter) else None
            _require(candidate is None or quarter not in ambiguous_initial, "ambiguous original filing identity")
            invalid_units = {}
            reviews = (_reviews(root, base, quarter, cutoff, mode, gaps, candidate,
                                invalid_units=invalid_units, quarterly=quarterly)
                       if quarter in quarters else [])
            if not reviews and quarter in ambiguous_initial:
                quarantined.update(initial_sources[quarter])
                for sid in initial_sources[quarter]:
                    gaps.append(dict(record=asset + "/" + quarter + "/new", evidence=sid,
                        reason="Ambiguous initial fiscal identity",
                        recovery="Reconcile the conflicting original filing identities before starting this quarter"))
            elif not reviews and quarter in initial:
                records.append(dict(id=asset + "/" + quarter + "/new", issuer=issuer, fiscal=initial[quarter],
                    cutoff=cutoff.isoformat(), required_sources=_required_all(questions, asset, quarter),
                    work=[dict(id=qid, status="missing", depends_on=q.get("depends_on", []), consumed={}) for qid, q in questions.items()]))
            for path, saved in reviews:
                fiscal = saved["fiscal"]
                _require(_adapter._core._fiscal(fiscal) and f"{fiscal['year']}Q{fiscal['period'][1:]}" == quarter, "fiscal directory mismatch")
                _id(saved["id"])
                _adapter._timestamp(saved["cutoff"])
                _require(isinstance(saved.get("units"), dict) and saved["units"].keys() <= questions.keys(), "unknown saved unit")
                work = []
                for qid, question in questions.items():
                    unit = saved["units"].get(qid, {})
                    _require(isinstance(unit, dict), "saved unit object")
                    consumed = unit.get("consumed", {})
                    _require(isinstance(consumed, dict), "consumed identities")
                    for sid, identity in consumed.items():
                        _id(sid)
                        _require(isinstance(identity, dict) and set(identity) == {"version", "projection"} and _adapter._text(identity["version"]), "consumed identity")
                    item = dict(id=qid, status="missing", depends_on=question.get("depends_on", []),
                                consumed={asset + ":" + sid: value for sid, value in consumed.items()})
                    if candidate_for == (asset, quarter):
                        for citation in _candidate_citations(unit):
                            adopted_claims.append(dict(record=asset + "/" + quarter + "/" + saved["id"], work=qid,
                                review_path=path if quarterly else path + (
                                    "/review.md" if path in invalid_units else "/review.json"),
                                dependent_work=_dependent_work(questions, qid),
                                **{key: citation[key] for key in _CITATION_FIELDS}))
                    if qid in invalid_units.get(path, {}):
                        if "output" in unit:
                            item["status"] = "complete"
                        work.append(item)
                        continue
                    if "output" in unit:
                        output = dict(unit["output"])
                        _require("content" not in output, "output content must be read from file")
                        try:
                            output["content"] = _bytes(root, output["path"]).decode("utf-8")
                        except FileNotFoundError:
                            output = {}
                        item["output"] = output
                    if "verification" in unit:
                        try:
                            check = _verification(root, unit)
                        except FileNotFoundError:
                            check = {}
                        complete = _completion_valid(check, item.get("output", {}).get("digest"))
                        if complete:
                            item.update(status="complete", completion_evidence=json.dumps(check, sort_keys=True))
                    missing_consumed = sorted(set(_required(question, quarter)) - consumed.keys())
                    if missing_consumed:
                        # Resolve against this record, including absent sources and
                        # nonfinancial inputs without source-declared fiscal data.
                        item.pop("completion_evidence", None)
                        gaps.append(dict(record=asset + "/" + quarter + "/" + saved["id"], evidence="dependencies:" + qid,
                            reason="Required economic inputs lack consumed identities: " + ", ".join(missing_consumed),
                            recovery="Verify the required sources and recompute this question and dependent synthesis"))
                    if not _analysis_valid(root, base, quarter, question.get("required_analysis", []),
                            unit.get("analysis_inputs", {}), asset + "/" + quarter + "/" + saved["id"], gaps):
                        # Preserve the saved completion claim for the assessor's
                        # invalidation action, but withdraw its reusable evidence.
                        item.pop("completion_evidence", None)
                    saved_cutoff = _adapter._core._instant(saved["cutoff"])
                    if not _candidate_sources_valid(base, quarter, saved_cutoff, unit, by_source):
                        item.pop("completion_evidence", None)
                        gaps.append(dict(record=asset + "/" + quarter + "/" + saved["id"],
                            evidence="candidate:" + qid, reason="Adopted claim lacks its bound cutoff-eligible source",
                            recovery="Check the original source and the saved claim before reusing dependent analysis"))
                    if "requirements" in saved and not _adapter._core._same_json(saved["requirements"].get(qid), question):
                        item.pop("completion_evidence", None)
                        gaps.append(dict(record=asset + "/" + quarter + "/" + saved["id"], evidence="requirements:" + qid,
                            reason="Declared question/dependency requirements changed",
                            recovery="Recompute this question and dependent synthesis against the current requirements"))
                    work.append(item)
                records.append(dict(id=asset + "/" + quarter + "/" + saved["id"], issuer=issuer, fiscal=fiscal,
                    cutoff=saved["cutoff"], required_sources=_required_all(questions, asset, quarter), work=work,
                    **{k: saved[k] for k in ("execution_state", "last_attempt", "last_success") if k in saved}))
        if not initial and len(records) == records_start:
            gaps.append(dict(record=asset, evidence="fiscal", reason="No eligible source-declared initial fiscal quarter", recovery="Supply original filing evidence and fiscal metadata; do not infer a calendar quarter"))
    return dict(version=1, sources=[s for s in sources if s["id"] not in quarantined],
                records=records), gaps, adopted_claims


def _mkdir(root, reference, *, exclusive=False):
    """Create directories through anchored descriptors, never following links."""
    parts = Path(reference).parts
    _require(parts and parts[0] == "investing" and ".." not in parts, "escaping reference")
    for index in range(1, len(parts)):
        parent = "/".join(parts[:index])
        fd = _open(root, parent, True)
        try:
            try:
                os.mkdir(parts[index], dir_fd=fd)
                os.fsync(fd)
            except FileExistsError:
                _require(not exclusive or index != len(parts) - 1, "Publication conflict: directory appeared concurrently: " + reference)
        finally:
            os.close(fd)
        child = _open(root, "/".join(parts[:index + 1]), True)
        os.close(child)


def _write_new(root, reference, data):
    parent, name = reference.rsplit("/", 1)
    if name == "review.json":
        # A same-filesystem hard link commits an already flushed complete file
        # atomically and fails if the destination exists. rename() can overwrite.
        run_id = _id(_object(root, parent + "/pending.json")["run"])
        stage = "investing/.research-runs/" + run_id
        try:
            content = _bytes(root, stage + "/completion.json")
        except FileNotFoundError:
            _write_new(root, stage + "/completion.json", data)
        else:
            _require(content == data, "Publication conflict: staged completion edited")
        source = _open(root, stage, True)
        destination = _open(root, parent, True)
        try:
            _require(_bytes(root, stage + "/completion.json") == data, "Publication conflict: staged completion edited")
            os.link("completion.json", name, src_dir_fd=source, dst_dir_fd=destination, follow_symlinks=False)
            os.fsync(destination)
        finally:
            os.close(source)
            os.close(destination)
        return
    fd = _open(root, parent, True)
    try:
        output = os.open(name, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600, dir_fd=fd)
        with os.fdopen(output, "wb") as stream:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        os.fsync(fd)
    finally:
        os.close(fd)


def _encoded(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, allow_nan=False).encode("utf-8")


def publication_snapshot(root, *, _exclude=None, _legacy_all_files=False):
    """Capture exact managed bytes before analysis; run journals are excluded."""
    result = {}
    def visit(reference):
        for name in _names(root, reference):
            path = reference + "/" + name
            if path in ("investing/.research-runs", "investing/.research-drafts", _exclude):
                continue
            fd = _open(root, path)
            try:
                kind = os.fstat(fd).st_mode
            finally:
                os.close(fd)
            if stat.S_ISDIR(kind):
                _require(_legacy_all_files or not _QUARTER_NOTE.fullmatch(path),
                         "Publication conflict: expected regular quarter note: " + path)
                visit(path)
            else:
                payload = _bytes(root, path)
                if _legacy_all_files or not _ordinary_quarter_note(path, payload):
                    result[path] = sha256(payload).hexdigest()
    try:
        visit("investing")
    except OSError as error:
        raise ValueError("Publication conflict: unsafe or unreadable managed path; preserve files and inspect: " + str(error)) from error
    return result


def _preconditions(root, expected, target=None, *, legacy_all_files=False):
    _require(isinstance(expected, dict) and expected, "publication preconditions required")
    current = publication_snapshot(root, _exclude=target, _legacy_all_files=legacy_all_files)
    changes = sorted(path for path in set(expected) | set(current) if expected.get(path) != current.get(path))
    _require(not changes, "Publication conflict; preserve user files/draft and reassess: " + ", ".join(changes))


def _target(asset, review):
    _id(asset)
    rid = _id(review["id"])
    fiscal = review["fiscal"]
    _require(_adapter._core._fiscal(fiscal), "source-declared fiscal identity required")
    _adapter._timestamp(review["cutoff"])
    quarter = str(fiscal["year"]) + fiscal["period"]
    return quarter, "investing/assets/equities/" + asset + "/cycles/" + quarter + "/" + review["cutoff"][:10] + "-" + rid


def _publication_bytes(request, target, run_id):
    review = _encoded(request["review"])
    encoded = {target + "/pending.json": _encoded(dict(version=1, run=run_id, review_digest=sha256(review).hexdigest()))}
    encoded.update({target + "/" + name: content.encode("utf-8") for name, content in request["files"].items()})
    encoded[target + "/review.json"] = review
    return encoded


def _rollback_valid(root, target, marker):
    """A withdrawal is bound to its saved run, not a freely editable hash list."""
    try:
        run_id = _id(marker["run"])
        run = "investing/.research-runs/" + run_id
        raw = _bytes(root, run + "/request.json")
        if sha256(raw).hexdigest() != _object(root, run + "/journal.json")["request_digest"]:
            return False
        request = _object(root, run + "/request.json")
        if _target(request["asset"], request["review"])[1] != target:
            return False
        encoded = _publication_bytes(request, target, run_id)
        names = set(_names(root, target)) - {"withdrawn.json", "abandoned.json"}
        expected = {target + "/" + name: sha256(encoded[target + "/" + name]).hexdigest() for name in names}
        return marker.get("files") == expected and all(sha256(_bytes(root, ref)).hexdigest() == digest for ref, digest in expected.items())
    except (OSError, ValueError, KeyError, TypeError):
        return False


def _validate_proposal(root, request, staged, *, output_suffix="", quarterly=False):
    asset, review, files = request["asset"], json.loads(json.dumps(request["review"])), request["files"]
    quarter, target = _target(asset, review)
    _require(type(review.get("version")) is int and review["version"] == 1, "review version")
    research = review.get("research", {})
    _require(isinstance(research, dict) and _adapter._text(research.get("method"))
             and isinstance(research.get("assumptions"), list) and isinstance(research.get("gaps"), list)
             and _adapter._text(research.get("changes")), "incomplete research envelope")
    horizons = research.get("horizons", {})
    _require(isinstance(horizons, dict) and set(horizons) == {"short", "medium", "long"}, "incomplete horizons")
    for judgment in horizons.values():
        _require(isinstance(judgment, dict) and _adapter._text(judgment.get("judgment"))
                 and _adapter._strings(judgment.get("evidence")) and _adapter._strings(judgment.get("invalidation_triggers")), "incomplete horizon judgment")
    base = "investing/assets/equities/" + asset
    metadata = _asset_metadata(root, base)
    questions = _unique(metadata["questions"])
    _require(isinstance(review.get("units"), dict) and review["units"].keys() <= questions.keys(), "unknown unit")
    ordinary_notes = None
    for qid, unit in review["units"].items():
        # Reused units retain all prior economic and authored dependencies.
        previous = request.get("previous", {}).get("units", {}).get(qid, {})
        if previous and unit.get("output") == previous.get("output"):
            _require(_adapter._core._same_json(_without_candidate_digests(unit), _without_candidate_digests(previous)),
                     "reused unit changes dependencies/checks without recomputing output")
            frozen = request.get("previous", {}).get("requirements")
            _require(frozen is None or _adapter._core._same_json(frozen.get(qid), questions[qid]), "reused unit changes declared dependencies")
        previous_citations = _candidate_citations(_without_candidate_digests(previous))
        for citation in _candidate_citations(_without_candidate_digests(unit)):
            if citation not in previous_citations:
                if ordinary_notes is None:
                    ordinary_notes = set(_note_references(root, base, quarter))
                _require(citation["path"] in ordinary_notes, "new claim must cite a current ordinary quarter note")
        for field in ("output", "verification"):
            ref = unit.get(field, {}).get("path") if field == "output" else unit.get(field)
            if isinstance(ref, str) and ref.startswith(target + "/"):
                name = ref[len(target) + 1:]
                _require(name in files, "missing staged output/check")
                replacement = staged + "/" + name
                if field == "output":
                    unit[field]["path"] = replacement + output_suffix
                else:
                    unit[field] = replacement
    snapshot, gaps, _ = _snapshot(root, _adapter._core._instant(review["cutoff"]), "latest",
                                   (asset, quarter, target, review), quarterly=quarterly)
    record = asset + "/" + quarter + "/" + review["id"]
    _require(not any(gap["record"] == record and gap["evidence"].startswith("candidate:") for gap in gaps),
             "candidate evidence must be independently cutoff eligible and frozen")
    result = _adapter.assess(snapshot, "latest", review["cutoff"])
    reusable = {item["work"] for item in result["reusable"] if item["record"] == record}
    _require(not request["complete"] or reusable == questions.keys(), "incomplete units or changed dependencies; save an explicit checkpoint or recompute")
    _require(not request["complete"] or not research["gaps"], "unresolved research gaps remain pending")
    return result


def _quarter_relative(cycle, reference):
    _require(isinstance(reference, str) and reference.startswith(cycle + "/"),
             "portable review requires a reference inside its selected quarter")
    return reference[len(cycle) + 1:]


def _rebase_review(review, cycle, *, portable):
    """Translate operational paths; leave saved origin references as provenance."""
    review = _adapter._json(_encoded(review).decode("utf-8"))
    for qid, unit in review["units"].items():
        def adjust(reference):
            if portable:
                return _quarter_relative(cycle, reference)
            path = Path(reference)
            _require(not path.is_absolute() and path.parts and ".." not in path.parts, "escaping quarter reference")
            return cycle + "/" + reference

        if "output" in unit:
            unit["output"]["path"] = adjust(unit["output"]["path"])
        for note in unit.get("candidate_notes", []):
            note["path"] = adjust(note["path"])
        bindings = review["quarter_evidence"]["units"][qid]["methods"]
        for identity, frozen in unit.get("analysis_inputs", {}).items():
            method = bindings[identity]
            frozen["content_ref"] = method["content_ref"] if portable else method["origin_content_ref"]
    return review


def _evidence_path(reference, folder):
    parts = Path(reference).parts
    _require(len(parts) == 3 and parts[:2] == ("data", folder)
             and parts[2] not in (".", ".."), "invalid quarter evidence reference")
    return reference


def _capture_quarter(root, asset, issuer, cycle, saved, expected, *, compact=False):
    """Build immutable registrations and raw copies for just the cited versions."""
    saved = _adapter._json(_encoded(saved).decode("utf-8"))
    base = "investing/assets/equities/" + asset
    registrations = {"sources": [], "analysis": []}
    provenance = {}
    for reference in expected:
        for folder in registrations:
            legacy = reference.startswith(base + "/data/" + folder + "/")
            local = re.fullmatch(re.escape(base) + r"/cycles/[0-9]{4}Q[1-4]/data/" + folder + r"/[^/]+\.md", reference)
            if not (legacy or local):
                continue
            try:
                metadata = (_source_registration(root, reference, issuer) if folder == "sources"
                            else _registered_metadata(root, reference))
            except (OSError, ValueError, KeyError, TypeError):
                if legacy:
                    raise
                continue
            registrations[folder].append((reference, metadata))

    files = {}
    cutoff = _adapter._core._instant(saved["cutoff"])

    def copy_payload(reference, checksum, folder):
        path = Path(reference)
        _require(not (len(path.parts) > 6 and path.parts[:3] == ("investing", "assets", "equities")
                      and path.parts[4] == "cycles" and path.parts[6] != "data"),
                 "quarter data cannot copy a previous research note")
        payload = _bytes(root, reference)
        _require(sha256(payload).hexdigest() == checksum, "quarter evidence input changed: " + reference)
        suffix = Path(reference).suffix.lower()
        if not re.fullmatch(r"\.[a-z0-9]{1,8}", suffix):
            suffix = ".bin"
        destination = f"data/{folder}/{checksum}{suffix}"
        files[destination] = payload
        return destination

    def read_narrative(role, reference):
        path = Path(reference)
        if path.suffix == ".md":
            captured = len(path.parts) == 9 and path.parts[4] == "cycles" and re.fullmatch(r"[0-9a-f]{64}", path.stem)
            return _markdown.registration_context(
                _bytes(root, reference).decode("utf-8"), role + "-registration", captured=bool(captured))
        return ()

    def bind(role, registration, origin, matches):
        narrative = read_narrative(role, origin)
        authored = registration["origin_reference"]
        if (role == "source" or not narrative) and authored != origin and any(ref == authored for ref, _ in matches):
            # Use prose only from the documented original among already checked
            # matches. The selected capture still supplies the binding metadata.
            narrative = read_narrative(role, authored) or narrative
        note = _markdown.render_registration(asset, role, registration, narrative=narrative)
        payload = note.encode("utf-8")
        digest = sha256(payload).hexdigest()
        prefix = "sources" if role == "source" else "analysis"
        reference = f"data/{prefix}/{digest}.md"
        files[reference] = payload
        return reference

    units = {}
    for qid, unit in saved["units"].items():
        links = {"sources": {}, "methods": {}}
        for sid, identity in unit.get("consumed", {}).items():
            options = [(origin, metadata) for origin, metadata in registrations["sources"]
                       if metadata["id"] == sid and metadata.get("identity") == identity["version"]
                       and _adapter._core._same_json(metadata.get("projection"), identity["projection"])]
            _require(options, "missing registered source version for quarter evidence: " + sid)
            origin, source = options[0]
            if not compact:
                provenance[source.get("origin_reference", origin)] = source
            published = _available(source.get("available_at"), cutoff)
            _require(published is not None and published <= cutoff, "source is later than cutoff: " + sid)
            _require(all(_adapter._core._same_json(
                {key: alternative.get(key) for key in ("raw_digest", "original_digest", "available_at", "fiscal")},
                {key: source.get(key) for key in ("raw_digest", "original_digest", "available_at", "fiscal")})
                for _, alternative in options), "conflicting registered quarter source: " + sid)
            record = dict(source, origin_reference=source.get("origin_reference", origin),
                          origin_raw_ref=source.get("origin_raw_ref", source["raw_ref"]),
                          raw_ref=copy_payload(source["raw_ref"], source["raw_digest"], "raw"))
            if "original_ref" in source or "original_digest" in source:
                record["origin_original_ref"] = source.get("origin_original_ref", source["original_ref"])
                record["original_ref"] = copy_payload(source["original_ref"], source["original_digest"], "raw")
            reference = bind("source", record, origin, options)
            links["sources"][sid] = reference
            if compact:
                identity["capture_digest"] = Path(reference).stem
                del identity["projection"]
        for mid, frozen in unit.get("analysis_inputs", {}).items():
            _analysis_identity(frozen)
            options = [(origin, metadata) for origin, metadata in registrations["analysis"]
                       if metadata["id"] == mid and metadata["identity"] == frozen["version"]
                       and all(_adapter._core._same_json(metadata.get(field), frozen[field])
                               for field in _ANALYSIS_FIELDS - {"version", "content_ref"})]
            _require(options, "missing registered method version for quarter evidence: " + mid)
            origin, method = options[0]
            if not compact:
                provenance[method.get("origin_reference", origin)] = method
            content_ref = copy_payload(method["content_ref"], method["content_digest"], "materials")
            method = dict(method, origin_reference=method.get("origin_reference", origin), content_ref=content_ref)
            links["methods"][mid] = dict(reference=bind("method", method, origin, options), content_ref=content_ref,
                                         origin_content_ref=frozen["content_ref"])
        if isinstance(unit.get("verification"), str):
            unit["verification"] = _verification(root, unit)
        units[qid] = links
    if compact:
        saved.pop("provenance", None)
    else:
        saved["provenance"] = provenance
    saved["quarter_evidence"] = dict(version=2 if compact else 1, issuer=issuer, units=units)
    return _rebase_review(saved, cycle, portable=True), files


class _QuarterMaterialError(ValueError):
    """A bound quarter file or completion claim failed its local checks."""


class _QuarterInputError(_QuarterMaterialError):
    """A saved input is damaged, regardless of the integrity of its output."""


def _verify_fixed_evidence(folder, asset, quarter, stored, *, damaged):
    """Restore checked observations for the existing in-memory assessment contract."""
    resolved = {}
    result = _verify_quarter_evidence(folder, asset, quarter, stored, damaged=damaged, resolved=resolved)
    if stored["quarter_evidence"]["version"] == 2:
        for qid, unit in stored["units"].items():
            if "consumed" in unit:
                unit["consumed"] = resolved.get(qid, {})
    return result


def _verify_quarter_evidence(folder, asset, quarter, stored, *, damaged=None, resolved=None):
    """Replay exact quarter-local bindings, optionally recording individual material failures."""
    manifest = stored["quarter_evidence"]
    _require(isinstance(manifest, dict) and type(manifest.get("version")) is int
             and (manifest["version"] == 1 or manifest["version"] == 2 and "reports" in stored)
             and isinstance(manifest.get("units"), dict) and isinstance(stored.get("units"), dict)
             and manifest["units"].keys() == stored["units"].keys(), "invalid quarter evidence mappings")
    conclusions = stored.get("research", {}).get("adopted_conclusions", [])
    _require(isinstance(conclusions, list)
             and all(isinstance(item, dict) and all(_adapter._text(item.get(key))
                     for key in ("excerpt", "origin", "revision")) for item in conclusions),
             "prior conclusion excerpts require origin and revision")
    questions = stored["requirements"]
    _require(isinstance(questions, dict) and stored["units"].keys() <= questions.keys(),
             "unknown portable review question")
    cutoff = _adapter._core._instant(stored["cutoff"])
    sources = {}
    work = []
    compact = manifest["version"] == 2
    source_refs = {}
    for qid, unit in stored["units"].items():
        links = manifest["units"][qid]
        _require(isinstance(unit, dict) and isinstance(links, dict), "invalid quarter evidence unit: " + qid)
        consumed = unit.get("consumed", {})
        methods = unit.get("analysis_inputs", {})
        _require(all(isinstance(value, dict) for value in (links.get("sources"), links.get("methods"), consumed, methods))
                 and links["sources"].keys() == consumed.keys() and links["methods"].keys() == methods.keys(),
                 "incomplete quarter evidence mappings: " + qid)
        for sid, ref in links["sources"].items() if not compact else ():
            _evidence_path(ref, "sources")
            binding = (ref, consumed[sid])
            accepted_ref, accepted_identity = source_refs.setdefault(sid, binding)
            _require(accepted_ref == ref and _adapter._core._same_json(accepted_identity, consumed[sid]),
                     "conflicting quarter evidence source bindings: " + sid)
        for mid, mapping in links["methods"].items():
            _analysis_identity(methods[mid])
            _evidence_path(mapping["reference"], "analysis")
            _require(mapping["content_ref"] == methods[mid]["content_ref"],
                     "quarter evidence method identity mismatch: " + mid)

    def read(path):
        return _bytes(folder, path, quarter_relative=True)

    def checked(path, checksum, *, error_type=_QuarterMaterialError):
        try:
            payload = read(path)
        except (OSError, ValueError) as error:
            raise error_type(f"cannot read quarter evidence {path}: {error}") from error
        if sha256(payload).hexdigest() != checksum:
            raise error_type("quarter evidence digest mismatch: " + path)
        return payload

    def registration(ref, folder_name, kind):
        payload = checked(_evidence_path(ref, folder_name), Path(ref).stem, error_type=_QuarterInputError)
        props, metadata = _markdown.record(payload.decode("utf-8"), kind + "-registration", asset_id=asset)
        _require(type(metadata.get("version")) is int and metadata["version"] == 1
                 and props[kind + "_id"] == metadata["id"]
                 and props[kind + "_version"] == metadata["identity"], "invalid quarter evidence registration")
        if kind == "source":
            _require(props.get("available_at") == metadata.get("available_at"),
                     "conflicting quarter source availability")
        return metadata

    for qid, question in questions.items():
        unit = stored["units"].get(qid, {})
        links = manifest["units"].get(qid, {"sources": {}, "methods": {}})
        consumed = unit.get("consumed", {})
        methods = unit.get("analysis_inputs", {})
        unit_consumed = {} if compact else consumed
        item = dict(id=qid, status="missing", depends_on=question.get("depends_on", []),
                    consumed={})
        unit_sources = {}
        try:
            if "output" in unit:
                output = unit["output"]
                parts = Path(output["path"]).parts
                _require(len(parts) == (1 if "reports" in stored else 2) and output["path"].endswith(".md"),
                         "invalid quarter analysis output path")
                payload = checked(output["path"], output["digest"])
                check = unit["verification"]
                if not isinstance(check, dict) or not _completion_valid(check, output["digest"]):
                    raise _QuarterMaterialError("quarter analysis verification missing or changed: " + output["path"])
                item.update(output=dict(output, content=payload.decode("utf-8")), status="complete",
                            completion_evidence=json.dumps(check, sort_keys=True))
                _require(set(_required(question, quarter)) <= consumed.keys()
                         and set(question.get("required_analysis", [])) <= methods.keys(),
                         "quarter analysis lacks required captured inputs: " + qid)
            for sid, ref in links["sources"].items():
                identity = consumed[sid]
                try:
                    if compact:
                        _require(isinstance(identity, dict) and set(identity) == {"version", "capture_digest"}
                                 and Path(ref).stem == identity["capture_digest"],
                                 "quarter evidence source capture mismatch")
                    record = registration(ref, "sources", "source")
                    _require(record["id"] == sid and record["identity"] == identity["version"],
                             "quarter evidence source identity mismatch: " + sid)
                    if compact:
                        _require(record.get("issuer") == manifest["issuer"], "quarter source issuer mismatch")
                    else:
                        _require(_adapter._core._same_json(record["projection"], identity["projection"]),
                                 "quarter evidence source identity mismatch: " + sid)
                    published = _available(record.get("available_at"), cutoff)
                    _require(published is not None and published <= cutoff, "quarter evidence source is later than cutoff")
                    raw = checked(_evidence_path(record["raw_ref"], "raw"), record["raw_digest"],
                                  error_type=_QuarterInputError)
                    _verify_source_payload(record, raw)
                    if "original_ref" in record or "original_digest" in record:
                        checked(_evidence_path(record["original_ref"], "raw"), record["original_digest"],
                                error_type=_QuarterInputError)
                except (OSError, ValueError, KeyError, TypeError) as error:
                    if not compact:
                        raise
                    version = identity.get("version", "unknown") if isinstance(identity, dict) else "unknown"
                    raise _QuarterInputError(f"quarter evidence source {sid} ({version}): {error}") from error
                if compact:
                    unit_consumed[sid] = dict(version=identity["version"], projection=record["projection"])
                source = dict(record, id=asset + ":" + sid, version=record["identity"])
                unit_sources[sid] = source
            for mid, method in links["methods"].items():
                frozen = methods[mid]
                record = registration(method["reference"], "analysis", "method")
                _require(record["id"] == mid and record["identity"] == frozen["version"]
                         and all(_adapter._core._same_json(record[field], frozen[field])
                                 for field in _ANALYSIS_FIELDS - {"version"}),
                         "quarter evidence method identity mismatch: " + mid)
                checked(_evidence_path(record["content_ref"], "materials"), record["content_digest"],
                        error_type=_QuarterInputError)
            for note in _candidate_citations(unit):
                path = note["path"]
                _require(_QUARTER_NOTE.fullmatch(f"investing/assets/equities/{asset}/cycles/{quarter}/{path}"),
                         "invalid quarter candidate note path")
                source = unit_sources.get(note["source_id"], {})
                fiscal = source.get("fiscal", {})
                if (note["source_version"] != source.get("version")
                        or note["source_available_at"] != source.get("available_at")
                        or f"{fiscal.get('year', '')}{fiscal.get('period', '')}" != quarter):
                    raise _QuarterMaterialError("quarter candidate note source identity mismatch: " + path)
        except _QuarterMaterialError as error:
            if damaged is None:
                raise
            damaged[qid] = error
            item.pop("completion_evidence", None)
            if "output" in unit:
                item["status"] = "complete"
        else:
            if resolved is not None:
                resolved[qid] = unit_consumed
        item["consumed"] = {asset + ":" + sid: value for sid, value in unit_consumed.items()}
        for sid, source in unit_sources.items():
            _require(sid not in sources or _adapter._core._same_json(sources[sid], source),
                     "conflicting quarter evidence source bindings: " + sid)
            sources[sid] = source
        work.append(item)

    fiscal = stored["fiscal"]
    _require(_adapter._core._fiscal(fiscal) and f"{fiscal['year']}{fiscal['period']}" == quarter,
             "invalid portable review quarter")
    issuer = manifest["issuer"]
    _require(all(source.get("issuer") == issuer for source in sources.values()),
             "quarter source issuer mismatch")
    for sid, source in sources.items():
        source["consumers"] = [qid for qid, question in questions.items() if sid in _required(question, quarter)]
    record = dict(id=f"{asset}/{quarter}/{stored['id']}", issuer=issuer, fiscal=fiscal,
                  cutoff=stored["cutoff"], required_sources=_required_all(questions, asset, quarter), work=work)
    return _adapter.assess(dict(version=1, sources=list(sources.values()), records=[record]),
                           "historical", stored["cutoff"])


def verify_quarter(folder, review):
    """Verify a copied quarter and its relative overview or dated review."""
    path = Path(review)
    if not path.is_absolute() and len(path.parts) == 1 and path.name.endswith(" - 00 Research Overview.md"):
        try:
            raw = _bytes(folder, path.name, quarter_relative=True)
            props, stored = _markdown.record(raw.decode("utf-8"), "quarter-overview")
            asset, quarter = props["asset_id"], props["fiscal_quarter"]
            prefix = path.name.removesuffix(" - 00 Research Overview.md")
            _require(prefix.startswith(quarter + " "), "fixed overview quarter mismatch")
            notes = {"quarter-overview": (path.name, raw, props)}
            _require(isinstance(stored.get("reports"), dict), "quarterly overview requires a mapping for reports")
            for role, filename in stored["reports"].items():
                _require(role in _markdown.ANALYSIS_ROLES
                         and filename == f"{prefix} - {_REPORT_LABELS[role]}.md", "invalid fixed report link")
                report_raw = _bytes(folder, filename, quarter_relative=True)
                report_props, _ = _markdown.parse_note(report_raw.decode("utf-8"), role,
                                                       asset_id=asset, fiscal_quarter=quarter)
                notes[role] = (filename, report_raw, report_props)
            _, stored = _fixed_record(notes)
            result = _verify_quarter_evidence(folder, asset, quarter, stored)
            return dict(verification=result, status="verified", reusable=result["reusable"], gaps=result["gaps"])
        except (OSError, ValueError, KeyError, TypeError) as error:
            raise ValueError("Cannot verify quarter evidence: " + str(error)) from error
    _require(not path.is_absolute() and len(path.parts) == 2 and path.name == "review.md",
             "provide the quarter-relative run/review.md")
    _id(path.parts[0])
    try:
        _require(not _LEGACY_REVIEW_MARKERS & set(_names(folder, path.parts[0], quarter_relative=True)),
                 "conflicting Markdown and legacy review")
        props, stored = _markdown.record(_bytes(folder, review, quarter_relative=True).decode("utf-8"), "review")
        asset, quarter = props["asset_id"], props["fiscal_quarter"]
        stored_quarter, target = _target(asset, stored)
        _require(stored_quarter == quarter and path.parent.name == target.rsplit("/", 1)[1]
                 and props["review_id"] == stored["id"] and props["as_of"] == stored["cutoff"]
                 and props.get("predecessor") == stored.get("predecessor"), "portable review identity mismatch")
        result = _verify_quarter_evidence(folder, asset, quarter, stored)
        return dict(verification=result, status="verified", reusable=result["reusable"], gaps=result["gaps"])
    except (OSError, ValueError, KeyError, TypeError) as error:
        raise ValueError("Cannot verify quarter evidence: " + str(error)) from error


def _validate_markdown_target(root, target, files, *, committed=False):
    try:
        names = set(_names(root, target))
        extras = names - files.keys()
        # After the marker commits, readers permit unreferenced attachments.
        _require(files.keys() <= names and (not extras or (committed and not _LEGACY_REVIEW_MARKERS & extras)),
                 "Publication conflict: unexpected files in proposed review: " + target)
        _require(all(_bytes(root, target + "/" + name) == content for name, content in files.items()),
                 "Publication conflict: proposed review files changed: " + target)
    except OSError as error:
        raise ValueError("Publication conflict: cannot verify proposed review: " + target) from error


def _publish_markdown(root, asset, review, files, expected, run_id, complete):
    _require(type(complete) is bool and isinstance(files, dict), "publication arguments")
    _require(all(isinstance(name, str) and re.fullmatch(r"[a-zA-Z0-9_-]+\.md", name)
                 and name != "review.md" and isinstance(content, str)
                 for name, content in files.items()), "Markdown analysis filenames required")
    quarter, target = _target(asset, review)
    base = "investing/assets/equities/" + asset
    _require(asset in _research_config(root)["assets"], "asset outside configured scope")
    _require(isinstance(expected, dict) and expected, "publication preconditions required")
    draft_files = {}
    for name, content in files.items():
        props, body = _markdown.parse_note(content, _markdown.ANALYSIS_ROLES, asset_id=asset,
            fiscal_quarter=quarter, as_of=review["cutoff"], review_id=review["id"])
        _require(props.get("status") in ("complete", "partial"), "invalid analysis status")
        draft_files[name] = _markdown.render_draft(props, body).encode("utf-8")

    stage = "investing/.research-drafts/" + run_id
    _mkdir(root, stage, exclusive=True)
    for name, draft in draft_files.items():
        _write_new(root, stage + "/" + name, draft)
        _write_new(root, stage + "/" + name + ".final", files[name].encode("utf-8"))

    cycle = base + "/cycles/" + quarter
    _mkdir(root, cycle)
    with _quarter_lock(root, cycle):
        _preconditions(root, expected)
        gaps = []
        entries = _managed_directories(root, cycle)
        cutoff = _adapter._core._instant(review["cutoff"])
        invalid_units, repairable_gaps = {}, {}
        leaves = (_reviews(root, base, quarter, cutoff, "latest", gaps,
                           invalid_units=invalid_units, repairable_gaps=repairable_gaps) if entries else [])
        _, draft_targets = _markdown_drafts(root)
        inherited = [gap for gap in gaps if gap["record"] not in draft_targets
                     and (gap["record"], gap["evidence"]) not in repairable_gaps]
        if entries and not leaves and not inherited:
            _require(review.get("predecessor") is None, "initial review cannot have predecessor")
        elif entries:
            _require(not inherited and len(leaves) == 1 and review.get("predecessor") == leaves[0][1]["id"],
                     "Publication conflict: predecessor changed or unfinished legacy state")
        else:
            _require(review.get("predecessor") is None, "initial review cannot have predecessor")
        previous = leaves[0][1] if leaves else {}
        try:
            legacy_runs = _names(root, "investing/.research-runs")
        except FileNotFoundError:
            legacy_runs = []
        for previous_run in legacy_runs:
            try:
                request = _object(root, "investing/.research-runs/" + _id(previous_run) + "/request.json")
            except FileNotFoundError:
                continue
            if request["asset"] == asset and _target(asset, request["review"])[0] == quarter:
                legacy_target = _target(asset, request["review"])[1]
                try:
                    legacy_names = set(_names(root, legacy_target))
                except FileNotFoundError:
                    legacy_names = set()
                _require(bool(legacy_names & {"review.json", "withdrawn.json", "abandoned.json"}),
                         "Unfinished legacy publication; preserve files for legacy recovery")
        _require(review.get("last_success") == previous.get("last_success"),
                 "local publication cannot advance last successful external verification")
        asset_metadata = _asset_metadata(root, base)
        requirements = _unique(asset_metadata["questions"])
        damaged = set(invalid_units.get(leaves[0][0], {})) if leaves else set()
        affected = damaged | {work for qid in damaged for work in _dependent_work(requirements, qid)}
        retired_outputs = set().union(*repairable_gaps.values())
        for qid, unit in review.get("units", {}).items():
            output_path = unit.get("output", {}).get("path", "")
            _require(output_path not in retired_outputs
                     and (not (qid in affected and output_path) or output_path.startswith(target + "/")),
                     "Publication conflict: recompute damaged unit or dependent output: " + qid)
            if output_path.startswith(target + "/"):
                name = output_path[len(target) + 1:]
                _require(name in files and isinstance(unit.get("verification"), dict)
                         and _completion_valid(_verification(root, unit), unit["output"].get("digest"))
                         and sha256(files[name].encode("utf-8")).hexdigest() == unit["output"]["digest"],
                         "new Markdown output lacks valid inline verification: " + qid)

        saved = dict(review, requirements=requirements, publication=dict(run=run_id, complete=complete))
        request = dict(asset=asset, review=saved, files=files, previous=previous, complete=complete)
        _validate_proposal(root, request, stage, output_suffix=".final")
        portable, evidence = _capture_quarter(root, asset, asset_metadata["issuer"], cycle, saved, expected)
        content = _markdown.render_review(asset, quarter, portable)
        _, roundtrip = _markdown.record(content, "review", asset_id=asset, fiscal_quarter=quarter)
        _require(_encoded(roundtrip) == _encoded(portable), "Markdown review does not round-trip")
        _write_new(root, stage + "/review.md", content.encode("utf-8"))
        _mkdir(root, target, exclusive=True)
        for name in files:
            staged_bytes = _bytes(root, stage + "/" + name + ".final")
            _require(staged_bytes == files[name].encode("utf-8")
                     and _bytes(root, stage + "/" + name) == draft_files[name],
                     "staged analysis changed")
            _write_new(root, target + "/" + name, staged_bytes)
        after_evidence = dict(expected)
        for reference, payload in evidence.items():
            destination = cycle + "/" + reference
            _mkdir(root, destination.rsplit("/", 1)[0])
            try:
                previous_bytes = _bytes(root, destination)
            except FileNotFoundError:
                parent, name = destination.rsplit("/", 1)
                _link_new_bytes(root, stage, parent, name, payload)
            else:
                _require(previous_bytes == payload, "quarter evidence conflicts with an existing file: " + destination)
            after_evidence[destination] = sha256(payload).hexdigest()
        _verify_quarter_evidence(Path(root) / cycle, asset, quarter, portable)
        _preconditions(root, after_evidence, target)
        final_files = {name: output.encode("utf-8") for name, output in files.items()}
        _validate_markdown_target(root, target, final_files)
        marker = content.encode("utf-8")
        try:
            _link_staged(root, stage, target, "review.md", marker)
        except FileExistsError as error:
            raise ValueError("Publication conflict: review marker appeared concurrently: " + target) from error
        _validate_markdown_target(root, target, {**final_files, "review.md": marker}, committed=True)
    return dict(status="complete" if complete else "checkpoint", review=target + "/review.md", run=run_id)


@contextmanager
def _quarter_lock(root, cycle):
    fd = _open(root, cycle, True)
    try:
        fcntl.flock(fd, fcntl.LOCK_EX)
        yield
    finally:
        os.close(fd)


def _link_staged(root, stage, target, name, payload):
    """Commit the expected marker bytes without linking the editable draft."""
    _require(_bytes(root, stage + "/" + name) == payload, "staged review changed")
    _link_new_bytes(root, stage, target, name, payload)


def _link_new_bytes(root, stage, target, name, payload):
    """Expose only flushed complete evidence and marker files."""
    commit = ".publication-marker"
    _write_new(root, stage + "/" + commit, payload)
    source = _open(root, stage, True)
    try:
        destination = _open(root, target, True)
        try:
            os.link(commit, name, src_dir_fd=source, dst_dir_fd=destination, follow_symlinks=False)
            os.fsync(destination)
            os.unlink(commit, dir_fd=source)
            os.fsync(source)
        finally:
            os.close(destination)
    finally:
        os.close(source)


def _optional_bytes(root, reference):
    try:
        return _bytes(root, reference)
    except FileNotFoundError:
        return None


def _quarter_prefix(quarter, ticker, company_name):
    _require(isinstance(ticker, str) and re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9.-]*", ticker),
             "invalid quarterly ticker")
    _require(isinstance(company_name, str), "company name required")
    company = re.sub(r'[<>:"/\\|?*#\[\]^%\x00-\x1f\x7f]', "-", company_name)
    company = " ".join(company.split()).strip(" .-")
    _require(company and len(company.encode("utf-8")) <= 120, "invalid quarterly company name")
    return f"{quarter} {ticker.upper()} {company}"


def _publish_quarterly(root, asset, review, files, expected, run_id, complete,
                       company_name, ticker, overview_title):
    _require(type(complete) is bool and isinstance(files, dict), "publication arguments")
    _require(all(re.fullmatch(r"[a-zA-Z0-9_-]+\.md", name) and isinstance(content, str)
                 for name, content in files.items()), "plain proposal filenames and UTF-8 text required")
    _require(asset in _research_config(root)["assets"], "asset outside configured scope")
    quarter, target = _target(asset, review)
    cycle = target.rsplit("/", 1)[0]
    base = cycle.rsplit("/", 2)[0]
    issuer = _asset_metadata(root, base)
    root = Path(root).absolute()
    _require(not any(path.is_symlink() for path in (root, *root.parents)), "symlink root")
    _preconditions(root, expected)
    previous_damage = {}
    previous_compact = {}
    with _update.read_barrier(root, namespace="equity"):
        notes = _fixed_notes(root, cycle, asset, quarter)
        prefix = _quarter_prefix(quarter, ticker, company_name) if not notes else None
        previous = {}
        if notes:
            overview, portable = _fixed_record(notes)
            if portable["quarter_evidence"].get("version") == 2:
                previous_compact = {qid: unit.get("consumed", {}) for qid, unit in portable["units"].items()}
                _verify_fixed_evidence(root / cycle, asset, quarter, portable, damaged=previous_damage)
            previous = _rebase_review(portable, cycle, portable=False)
            prefix = Path(overview).name.removesuffix(" - 00 Research Overview.md")
            _require(review["id"] != previous["id"]
                     and review.get("predecessor") == previous["id"]
                     and _adapter._core._instant(previous["cutoff"]) <= _adapter._core._instant(review["cutoff"])
                     and previous["fiscal"] == review["fiscal"],
                     "publication conflict: stale predecessor, fiscal identity or cutoff")
        else:
            _require(review.get("predecessor") is None, "initial quarter cannot have a predecessor")
    _require(review.get("last_success") == previous.get("last_success"),
             "local publication cannot advance last successful external verification")
    previous_units = previous.get("units", {})
    saved = _adapter._json(_encoded(review).decode("utf-8"))
    for qid, prior in previous_units.items():
        unit = saved["units"].get(qid)
        if unit is None or "output" not in prior or unit.get("output") != prior["output"]:
            continue
        _require(qid not in previous_damage, "cannot retain damaged quarterly evidence: " + qid)
        if qid in previous_compact and unit.get("consumed") == previous_compact[qid] and "consumed" in prior:
            unit["consumed"] = prior["consumed"]
    saved.update(requirements=_unique(issuer["questions"]), publication=dict(run=run_id, complete=complete))
    proposal = dict(asset=asset, review=saved, files=files, previous=previous, complete=complete)
    draft_root = "investing/.research-drafts"
    _mkdir(root, draft_root)
    with TemporaryDirectory(prefix="quarterly-", dir=root / draft_root) as temporary:
        stage = Path(temporary).relative_to(root).as_posix()
        for name, content in files.items():
            _write_new(root, stage + "/" + name, content.encode("utf-8"))
        _validate_proposal(root, proposal, stage, quarterly=True)

    reports = {role: Path(note[0]).name for role, note in notes.items() if role != "quarter-overview"}
    intended = {}
    proposed_paths = {}
    retained_outputs = []
    roles = set()
    for qid, unit in saved["units"].items():
        if "output" not in unit:
            continue
        output = unit["output"]
        path = output["path"]
        if not path.startswith(target + "/"):
            _require(unit == previous_units.get(qid), "unowned quarterly report reference")
            retained_outputs.append(output)
            continue
        name = path[len(target) + 1:]
        _require(name in files, "missing proposed analysis")
        content = files[name]
        verification = unit.get("verification")
        _require(isinstance(verification, dict)
                 and _completion_valid(verification, output["digest"])
                 and sha256(content.encode("utf-8")).hexdigest() == output["digest"],
                 "new report lacks matching inline verification")
        if name not in proposed_paths:
            props, _ = _markdown.parse_note(content, _markdown.ANALYSIS_ROLES, asset_id=asset,
                fiscal_quarter=quarter, as_of=review["cutoff"], review_id=review["id"])
            role = props["finance_role"]
            _require(role not in roles and props["status"] in ("partial", "complete"),
                     "duplicate or draft quarterly report")
            roles.add(role)
            filename = reports.setdefault(role, f"{prefix} - {_REPORT_LABELS[role]}.md")
            path = cycle + "/" + filename
            intended[path] = content.encode("utf-8")
            proposed_paths[name] = path
        path = proposed_paths[name]
        output.update(path=path, digest=sha256(intended[path]).hexdigest())
        verification["output_digest"] = output["digest"]
    _require(proposed_paths.keys() == files.keys(), "unreferenced proposed reports")
    for output in retained_outputs:
        if output["path"] in intended:
            _require(output["digest"] == sha256(intended[output["path"]]).hexdigest(),
                     "re-verify every unit retained in a changed shared report")
    saved["reports"] = reports
    portable, evidence = _capture_quarter(root, asset, issuer["issuer"], cycle, saved, expected, compact=True)
    overview = cycle + f"/{prefix} - 00 Research Overview.md"
    title = overview_title or (notes["quarter-overview"][2]["title"] if notes
                               else f"{prefix} Research Overview")
    _require(isinstance(title, str) and title.strip() and not any(c in title for c in "\r\n"),
             "invalid quarterly overview title")
    links = [(_REPORT_LABELS[role], quote(reports[role])) for role in _REPORT_LABELS if role in reports]
    overview_text = _markdown.render_quarter_overview(asset, quarter, portable, title, links)
    _markdown.record(overview_text, "quarter-overview")
    intended[overview] = overview_text.encode("utf-8")

    observed = {path: raw for path, raw, _ in notes.values()}
    for path in intended:
        if path in expected:
            _require(path in observed, "quarter report would overwrite an unowned note: " + path)

    def prepare_evidence():
        _preconditions(root, expected)
        for reference, payload in evidence.items():
            destination = cycle + "/" + reference
            _mkdir(root, destination.rsplit("/", 1)[0])
            previous_bytes = _optional_bytes(root, destination)
            if previous_bytes is None:
                _write_new(root, destination, payload)
            else:
                _require(previous_bytes == payload, "quarter evidence conflicts with an existing file: " + destination)

    _update.apply(root, {path: observed.get(path) for path in intended}, intended,
                  check_scope=prepare_evidence, namespace="equity")
    return dict(status="complete" if complete else "checkpoint", review=overview, run=run_id)


def recover_quarterly(root, asset, quarter):
    """Resume an interrupted write only for the requested asset fiscal quarter."""
    cycle = Path("investing/assets/equities") / _id(asset) / "cycles" / _id(quarter)
    _require(re.fullmatch(r"[0-9]{4}Q[1-4]", quarter), "invalid fiscal directory")
    root = Path(root).absolute()
    _require(not any(path.is_symlink() for path in (root, *root.parents)), "symlink root")

    def check_scope(changes):
        for reference, (_, intended) in changes.items():
            path = Path(reference)
            _require(path.parent == cycle, "Pending writes are outside the selected quarter")
            props, _ = _markdown.parse_note(intended.decode("utf-8"), _REPORT_LABELS.keys(),
                                           asset_id=asset, fiscal_quarter=quarter)
            _require(path.name.startswith(quarter + " ")
                     and path.name.endswith(f" - {_REPORT_LABELS[props['finance_role']]}.md"),
                     "Pending write does not match its report role")

    return _update.recover(root, namespace="equity", check_scope=check_scope)


def publish(root, asset, review, files, expected, run_id, *, complete=True, storage="legacy",
            company_name=None, ticker=None, overview_title=None):
    """Save one append-only review, completion last; recover using its run ID."""
    _id(run_id)
    _require(storage in ("legacy", "markdown", "quarterly"), "unsupported research storage")
    if isinstance(review.get("units"), dict):
        review = dict(review, units={qid: _without_candidate_digests(unit) for qid, unit in review["units"].items()})
    if storage == "markdown":
        return _publish_markdown(root, asset, review, files, expected, run_id, complete)
    if storage == "quarterly":
        return _publish_quarterly(root, asset, review, files, expected, run_id, complete,
                                  company_name, ticker, overview_title)
    _require(type(complete) is bool and isinstance(files, dict), "publication arguments")
    _require(all(isinstance(name, str) and re.fullmatch(r"[a-zA-Z0-9_-]+\.(md|json)", name)
                 and name not in ("review.json", "pending.json", "withdrawn.json", "abandoned.json")
                 and isinstance(content, str) for name, content in files.items()), "plain output filenames and UTF-8 text required")
    _preconditions(root, expected)
    quarter, target = _target(asset, review)
    base = "investing/assets/equities/" + asset
    _require(asset in _research_config(root)["assets"], "asset outside configured scope")
    cycle = base + "/cycles/" + quarter
    _mkdir(root, cycle)
    with _quarter_lock(root, cycle):
        _preconditions(root, expected)
        return _publish_legacy(root, asset, review, files, expected, run_id, complete, quarter, target)


def _publish_legacy(root, asset, review, files, expected, run_id, complete, quarter, target):
    base = "investing/assets/equities/" + asset
    try:
        entries = _managed_directories(root, base + "/cycles/" + quarter)
    except FileNotFoundError:
        entries = []
    _require(target.rsplit("/", 1)[1] not in entries, "review destination already exists; recover its recorded run")
    for entry in entries:
        directory = base + "/cycles/" + quarter + "/" + _id(entry)
        try:
            _bytes(root, directory + "/review.md")
        except FileNotFoundError:
            continue
        raise ValueError("Existing Markdown history requires storage='markdown' for new publication")
    previous = {}
    if entries:
        leaves = _reviews(root, base, quarter, _adapter._core._instant(review["cutoff"]), "latest", [])
        _require(len(leaves) == 1 and review.get("predecessor") == leaves[0][1]["id"], "predecessor must be current eligible review")
        previous = leaves[0][1]
    else:
        _require(review.get("predecessor") is None, "initial review cannot have predecessor")
    _require(review.get("last_success") == previous.get("last_success"),
             "local publication cannot advance last successful external verification")
    # The frozen metadata and raw hashes keep provenance even after future revisions.
    provenance = {path: _registered_metadata(root, path) for path in expected
                  if path.startswith(base + "/data/sources/") or path.startswith(base + "/data/analysis/")}
    requirements = _unique(_asset_metadata(root, base)["questions"])
    review = dict(review, provenance=provenance, requirements=requirements, publication=dict(run=run_id, complete=complete))
    request = dict(version=1, asset=asset, review=review, files=files, expected=expected, snapshot_scope="managed",
                   previous=previous, complete=complete)
    run = "investing/.research-runs/" + run_id
    _mkdir(root, "investing/.research-runs")
    # Never reuse or repair an existing run implicitly.
    _require(run_id not in _names(root, "investing/.research-runs"), "run exists; use recover")
    _mkdir(root, run, exclusive=True)
    content = _encoded(request)
    _write_new(root, run + "/request.json", content)
    _write_new(root, run + "/journal.json", _encoded(dict(version=1, request_digest=sha256(content).hexdigest())))
    return _recover(root, run_id, action="resume", new_target=True)


def recover(root, run_id, *, action="resume"):
    """Revalidate/resume or safely withdraw only this recorded isolated run."""
    return _recover(root, run_id, action=action, new_target=False)


def _recover(root, run_id, *, action, new_target):
    _id(run_id)
    _require(action in ("resume", "rollback"), "recovery action")
    run = "investing/.research-runs/" + run_id
    try:
        request = _recovery_request(root, run)
        quarter, target = _target(request["asset"], request["review"])
        if new_target:
            # publish already holds the quarter lock.
            return _apply_recovery(root, run_id, request, quarter, target, action, new_target)
        cycle = target.rsplit("/", 1)[0]
        try:
            os.close(_open(root, cycle, True))
        except FileNotFoundError:
            # Older recovery journals may predate creation of the quarter.
            _recovery_preconditions(root, request, target)
            _mkdir(root, cycle)
        with _quarter_lock(root, cycle):
            _require(_adapter._core._same_json(_recovery_request(root, run), request),
                     "Publication conflict: recovery request changed")
            return _apply_recovery(root, run_id, request, quarter, target, action, new_target)
    except (KeyError, TypeError, UnicodeError, NotADirectoryError, IsADirectoryError, FileExistsError) as error:
        raise ValueError("Cannot recover publication; preserve journal and draft: " + str(error)) from error



def _recovery_request(root, run):
    journal = _object(root, run + "/journal.json")
    raw = _bytes(root, run + "/request.json")
    _require(sha256(raw).hexdigest() == journal["request_digest"],
             "Publication conflict: draft edited; preserve it and inspect")
    data = _adapter._json(raw.decode("utf-8"))
    _require(isinstance(data, dict) and type(data.get("version")) is int and data["version"] == 1,
             "unsupported recovery request")
    _require("snapshot_scope" not in data or data["snapshot_scope"] == "managed",
             "unsupported recovery snapshot scope")
    return data


def _recovery_preconditions(root, request, target):
    # An unmarked version-1 journal predates the ordinary note exemption.
    _preconditions(root, request["expected"], target, legacy_all_files="snapshot_scope" not in request)


def _guard_descendants(root, asset, quarter, parent):
    """Refuse withdrawal if either record format relies on this predecessor."""
    cycle = f"investing/assets/equities/{asset}/cycles/{quarter}"
    for name in _managed_directories(root, cycle):
        directory = cycle + "/" + _id(name)
        try:
            legacy = _object(root, directory + "/review.json")
        except FileNotFoundError:
            pass
        else:
            _require(legacy.get("predecessor") != parent, "Publication conflict: descendant review exists")
        try:
            markdown = _bytes(root, directory + "/review.md").decode("utf-8")
        except FileNotFoundError:
            continue
        props, record = _markdown.record(markdown, "review", asset_id=asset, fiscal_quarter=quarter)
        _require(props.get("predecessor") == record.get("predecessor")
                 and _target(asset, record)[1] == directory,
                 "Publication conflict: Markdown descendant identity is not verifiable")
        _require(record.get("predecessor") != parent, "Publication conflict: descendant review exists")


def _apply_recovery(root, run_id, request, quarter, target, action, new_target):
    run = "investing/.research-runs/" + run_id
    _recovery_preconditions(root, request, target)
    staged = run + "/draft"
    _mkdir(root, staged)
    for name, content in request["files"].items():
        reference = staged + "/" + name
        try:
            existing = _bytes(root, reference)
        except FileNotFoundError:
            _write_new(root, reference, content.encode("utf-8"))
        else:
            _require(existing == content.encode("utf-8"), "Publication conflict: saved draft edited: " + reference)
    try:
        present = set(_names(root, target))
        target_exists = True
    except FileNotFoundError:
        present = set()
        target_exists = False
    _require(not new_target or not target_exists,
             "Publication conflict: directory appeared concurrently: " + target)
    marker = "withdrawn.json" if "withdrawn.json" in present else "abandoned.json" if "abandoned.json" in present else None
    allowed = set(request["files"]) | {"pending.json", "review.json"} | ({marker} if marker else set())
    _require(present <= allowed, "Publication conflict: unexpected files in proposed review")
    encoded = _publication_bytes(request, target, run_id)
    for name in present:
        if name == marker:
            continue
        ref = target + "/" + name
        _require(_bytes(root, ref) == encoded[ref], "Publication conflict: user edited " + ref)
    if marker:
        _require(action == "rollback", "run withdrawn; preserve drafts and start a new run")
        frozen = _object(root, target + "/" + marker)
        _require(frozen.get("run") == run_id and frozen.get("files") == {
            ref: sha256(content).hexdigest() for ref, content in encoded.items()
            if ref.rsplit("/", 1)[1] in present}, "Publication conflict: rollback marker edited")
        return dict(status="rolled_back", review=target + "/review.json", run=run_id)
    if action == "rollback":
        if present:
            _guard_descendants(root, request["asset"], quarter, request["review"]["id"])
        _recovery_preconditions(root, request, target)
        _mkdir(root, target)
        marker = "withdrawn.json" if "review.json" in present else "abandoned.json"
        _write_new(root, target + "/" + marker, _encoded(dict(version=1, run=run_id,
            files={ref: sha256(content).hexdigest() for ref, content in encoded.items() if ref.rsplit("/", 1)[1] in present})))
        return dict(status="rolled_back", review=target + "/review.json", run=run_id)
    if "review.json" in present:
        return dict(status="complete" if request["complete"] else "checkpoint", review=target + "/review.json", run=run_id)
    _validate_proposal(root, request, staged)
    # Explicit recovery may find an empty directory left before pending.json.
    # The first exclusive write claims it for this run without replacing files.
    if not target_exists:
        _mkdir(root, target, exclusive=True)
    for reference, content in encoded.items():
        if reference.endswith("/review.json"):
            continue
        if reference.rsplit("/", 1)[1] not in present:
            _write_new(root, reference, content)
    _recovery_preconditions(root, request, target)
    for reference, content in encoded.items():
        if not reference.endswith("/review.json"):
            _require(_bytes(root, reference) == content, "Publication conflict: proposed output edited: " + reference)
    # Exclusive creation is the commit point. No rename can overwrite user files.
    _write_new(root, target + "/review.json", encoded[target + "/review.json"])
    return dict(status="complete" if request["complete"] else "checkpoint", review=target + "/review.json", run=run_id)


def _markdown_drafts(root):
    gaps, targets = [], set()
    try:
        drafts = _names(root, "investing/.research-drafts")
    except FileNotFoundError:
        drafts = []
    for run_id in drafts:
        stage = "investing/.research-drafts/" + _id(run_id)
        try:
            raw = _bytes(root, stage + "/review.md")
            props, record = _markdown.record(raw.decode("utf-8"), "review")
            _, target = _target(props["asset_id"], record)
            if record["publication"]["run"] == run_id:
                try:
                    published = _bytes(root, target + "/review.md")
                except FileNotFoundError:
                    targets.add(target)
                except (OSError, ValueError):
                    # Discovery reports the unsafe marker at its real path.
                    # Its presence is not evidence of an interrupted draft.
                    continue
                else:
                    if published == raw:
                        continue
        except (OSError, ValueError, KeyError, TypeError):
            pass
        gaps.append(dict(record=stage, evidence="publication:" + run_id,
            reason="Unfinished Markdown draft retained; no completed view advanced",
            recovery="Inspect the draft and retry from the previous valid record"))
    return gaps, targets


def discover(root, mode, cutoff, *, candidate_for=None, storage="legacy"):
    """Derive accepted assessment input from saved metadata, without writes.

    Unsupported/ambiguous layouts raise ValueError with existing data preserved.
    Recorded completion checks are attestations, never analytical approval.
    """
    _require(storage in ("legacy", "quarterly"), "unsupported discovery storage")
    if storage == "quarterly":
        boundary = Path(root).absolute()
        _require(not any(p.is_symlink() for p in (boundary, *boundary.parents)), "symlink root")
        with _update.read_barrier(boundary, namespace="equity"):
            return _discover(boundary, mode, cutoff, candidate_for, quarterly=True)
    return _discover(root, mode, cutoff, candidate_for, quarterly=False)


def _discover(root, mode, cutoff, candidate_for, *, quarterly):
    try:
        _adapter._require(mode in ("historical", "latest"), "mode")
        _adapter._timestamp(cutoff)
        boundary = Path(root).absolute()
        _require(not any(p.is_symlink() for p in (boundary, *boundary.parents)), "symlink root")
        if candidate_for is not None:
            asset, quarter = candidate_for
            _require(_id(asset) in _research_config(boundary)["assets"], "asset outside configured scope")
            _require(re.fullmatch(r"[0-9]{4}Q[1-4]", quarter), "invalid fiscal directory")
            candidate_for = (asset, quarter)
        snapshot, gaps, adopted_claims = _snapshot(boundary, _adapter._core._instant(cutoff), mode,
                                                   candidate_for=candidate_for, quarterly=quarterly)
        result = _adapter.assess(snapshot, mode, cutoff)
        if candidate_for is not None:
            base = "investing/assets/equities/" + asset
            note_paths = _note_references(boundary, base, quarter)
            result["candidate_notes"] = [dict(path=path) for path in note_paths]
            result["adopted_claims"] = [dict(claim, note_present=claim["path"] in note_paths)
                                        for claim in adopted_claims]
        if quarterly:
            if gaps:
                result["gaps"].extend(gaps)
                result["status"] = "partial"
            return result
        try:
            runs = _names(boundary, "investing/.research-runs")
        except FileNotFoundError:
            runs = []
        for run_id in runs:
            _id(run_id)
            run = "investing/.research-runs/" + run_id
            try:
                request = _object(boundary, run + "/request.json")
                _, target = _target(request["asset"], request["review"])
                raw = _bytes(boundary, run + "/request.json")
                journal = _object(boundary, run + "/journal.json")
                _require(sha256(raw).hexdigest() == journal["request_digest"], "publication request edited")
                encoded = _publication_bytes(request, target, run_id)
                names = set(_names(boundary, target))
                markers = names & {"withdrawn.json", "abandoned.json"}
                if markers:
                    if len(markers) == 1:
                        marker = _object(boundary, target + "/" + next(iter(markers)))
                        if marker.get("run") == run_id and _rollback_valid(boundary, target, marker):
                            continue
                elif "review.json" in names and names == {ref.rsplit("/", 1)[1] for ref in encoded}:
                    if all(_bytes(boundary, ref) == content for ref, content in encoded.items()):
                        continue
            except (FileNotFoundError, ValueError):
                pass
            gaps.append(dict(record=run, evidence="publication:" + run_id,
                reason="Unfinished publication retained; no completed view advanced",
                recovery="Use recover(root, run_id) to revalidate/resume or action='rollback' to abandon; preserve drafts"))
        draft_gaps, _ = _markdown_drafts(boundary)
        gaps.extend(draft_gaps)
        if gaps:
            result["gaps"].extend(gaps)
            result["status"] = "partial"
        return result
    except (OSError, KeyError, TypeError, UnicodeError) as error:
        raise ValueError(f"Cannot discover version-1 investing research: {error}; supply missing metadata or repair the reference and retry") from error
