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
from datetime import date, datetime, time

_spec = importlib.util.spec_from_file_location("assess_work", Path(__file__).with_name("assess_work.py"))
_adapter = importlib.util.module_from_spec(_spec)
exec(compile(_spec.loader.get_source("assess_work"), _spec.origin, "exec"), _adapter.__dict__)


_markdown_spec = importlib.util.spec_from_file_location("research_markdown", Path(__file__).with_name("research_markdown.py"))
_markdown = importlib.util.module_from_spec(_markdown_spec)
_markdown_spec.loader.exec_module(_markdown)


def _require(value, message):
    if not value:
        raise ValueError(message)


def _id(value):
    _require(isinstance(value, str) and re.fullmatch(r"[a-zA-Z0-9_-]+", value), "ambiguous identity")
    return value


def _open(root, reference, directory=False):
    path = Path(reference)
    _require(not path.is_absolute() and path.parts and path.parts[0] == "investing" and ".." not in path.parts, "escaping reference")
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


def _bytes(root, reference):
    with os.fdopen(_open(root, reference), "rb") as stream:
        _require(stat.S_ISREG(os.fstat(stream.fileno()).st_mode), "regular local file required")
        return stream.read()


def _names(root, reference):
    fd = _open(root, reference, True)
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
    props, record = _markdown.record(_bytes(root, reference).decode("utf-8"),
                                     kind + "-registration", asset_id=asset)
    _require(type(record.get("version")) is int and record["version"] == 1
             and props.get(kind + "_id") == record.get("id")
             and props.get(kind + "_version") == record.get("identity"),
             "Markdown research registration identity mismatch")
    if kind == "source" and "available_at" in props:
        _require(props["available_at"] == record.get("available_at"), "Markdown source availability mismatch")
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
            if name.endswith(".md") and stat.S_ISREG(os.stat(name, dir_fd=fd, follow_symlinks=False).st_mode):
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


def _analysis_valid(root, base, required, consumed, record, gaps):
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
            reference = base + "/data/analysis/" + identity
            try:
                metadata = _registered_metadata(root, reference + ".md")
            except FileNotFoundError:
                metadata = _registered_metadata(root, reference + ".json")
            _require(metadata.get("id") == identity and metadata.get("kind") in ("method", "assumption"), "local analysis identity/kind")
            _require(not {"available_at", "fiscal", "raw_ref"} & metadata.keys(), "economic evidence cannot be a local analysis input")
            _adapter._timestamp(metadata["authored_at"])
            _require(_adapter._text(metadata.get("identity")), "local analysis version")
            current = {key: metadata[key] for key in fields - {"version"}}
            current["version"] = metadata["identity"]
            content = _bytes(root, metadata["content_ref"])
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


def _note_references(root, base, quarter):
    path = base + "/cycles/" + quarter
    try:
        fd = _open(root, path, True)
    except FileNotFoundError:
        return []
    try:
        return [path + "/" + name for name in sorted(os.listdir(fd))
                if name.endswith(".md") and name != "index.md"
                and stat.S_ISREG(os.stat(name, dir_fd=fd, follow_symlinks=False).st_mode)]
    finally:
        os.close(fd)


def _candidate_evidence_valid(root, base, quarter, cutoff, unit, sources):
    references = unit.get("candidate_notes", [])
    _require(isinstance(references, list), "candidate notes must be a list")
    if not references:
        return True
    allowed = set(_note_references(root, base, quarter))
    for citation in references:
        _require(isinstance(citation, dict) and all(_adapter._text(citation.get(key))
                 for key in ("path", "digest", "claim", "source_id", "source_version", "source_available_at")),
                 "incomplete candidate note evidence")
        source_id = _id(citation["source_id"])
        source = sources.get(source_id, {})
        fiscal = source.get("fiscal", {})
        published = _available(source.get("available_at"), cutoff)
        bound = unit.get("consumed", {}).get(source_id, {})
        if (citation["path"] not in allowed or not published or published > cutoff
                or f"{fiscal.get('year', '')}{fiscal.get('period', '')}" != quarter
                or citation["source_available_at"] != source["available_at"]
                or citation["source_version"] != source.get("version")
                or bound.get("version") != source.get("version")
                or not _adapter._core._same_json(bound.get("projection"), source.get("projection"))):
            return False
        content = _bytes(root, citation["path"])
        if sha256(content).hexdigest() != citation["digest"] or citation["claim"] not in content.decode("utf-8"):
            return False
    return True


def _reviews(root, base, quarter, cutoff, mode, gaps, proposed=None):
    gaps_start = len(gaps)
    saved = {}
    withdrawn = set()
    try:
        directories = _managed_directories(root, base + "/cycles/" + quarter)
    except FileNotFoundError:
        _require(proposed is not None, "missing quarter directory")
        directories = []
    for directory in directories:
        _id(directory)
        path = base + "/cycles/" + quarter + "/" + directory
        try:
            markdown = _bytes(root, path + "/review.md").decode("utf-8")
        except FileNotFoundError:
            pass
        else:
            try:
                asset = base.rsplit("/", 1)[1]
                props, review = _markdown.record(markdown, "review", asset_id=asset, fiscal_quarter=quarter)
                rid = _id(review["id"])
                complete = review.get("publication", {}).get("complete")
                _require(type(review.get("version")) is int and review["version"] == 1
                         and type(complete) is bool
                         and props.get("status") == ("complete" if complete else "partial")
                         and props.get("predecessor") == review.get("predecessor")
                         and props.get("review_id") == rid and props.get("as_of") == review["cutoff"]
                         and _target(asset, review)[1] == path, "Markdown review identity mismatch")
                _require(not {"review.json", "pending.json", "withdrawn.json", "abandoned.json"} &
                         set(_names(root, path)), "conflicting Markdown and legacy review")
                for unit in review["units"].values():
                    output = unit.get("output", {})
                    if output.get("path", "").startswith(path + "/"):
                        _require(sha256(_bytes(root, output["path"])).hexdigest() == output.get("digest")
                                 and _completion_valid(_verification(root, unit), output["digest"]),
                                 "published Markdown output is changed, incomplete or unverified")
                _require(rid not in saved, "duplicate review identity")
                saved[rid] = (path, review)
            except (FileNotFoundError, ValueError, KeyError, TypeError) as error:
                gaps.append(dict(record=path, evidence="reviews", reason="Invalid Markdown review: " + str(error),
                    recovery="Preserve the draft and resume from the prior valid record"))
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
        rid = _id(review["id"])
        _require(rid not in saved, "duplicate review identity")
        _adapter._timestamp(review["cutoff"])
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
        leaves = [pair for rid, pair in eligible.items() if rid not in parents]
        _require(len(leaves) == 1, "missing cutoff review or ambiguous competing reviews")
        return leaves
    except (ValueError, FileNotFoundError) as error:
        gaps.append(dict(record=base + "/cycles/" + quarter, evidence="reviews", reason=str(error), recovery="Repair review metadata or provide the requested cutoff review; preserve existing research"))
        return []


def _snapshot(root, cutoff, mode, proposed=None):
    config = _research_config(root)
    _require(isinstance(config.get("assets"), list) and config["assets"], "missing asset scope")
    assets = [_id(asset) for asset in config["assets"]]
    _require(len(set(assets)) == len(assets), "duplicate asset identity")
    sources, records, gaps = [], [], []
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
        local = []
        for name in _names(root, base + "/data/sources"):
            source = _registered_metadata(root, base + "/data/sources/" + name)
            _require(source.get("issuer") == issuer, "source issuer mismatch")
            _require(_adapter._text(source.get("kind")), "source kind")
            _require(source["kind"] not in ("method", "assumption"), "local analysis inputs must not be economic sources")
            _require("fiscal" not in source or isinstance(source["fiscal"], dict), "source fiscal")
            _require(source.get("identity") is None or _adapter._text(source["identity"]), "source identity")
            _require(source.get("available_at") is None or _adapter._text(source["available_at"]), "source availability")
            raw = _bytes(root, source["raw_ref"])
            _require(sha256(raw).hexdigest() == source["raw_digest"], "source raw digest mismatch")
            _require(source.get("raw_format") in ("json", "text"), "source raw_format")
            if source["raw_format"] == "json":
                _adapter._json(raw.decode("utf-8"))
            else:
                _require(isinstance(source.get("projection"), dict) and source["projection"].get("raw_text") == raw.decode("utf-8"), "free-text projection must retain full raw_text")
            # Raw hashes retain provenance; only declared economic identity and
            # typed relevant projection invalidate the accepted assessor's inputs.
            source["version"] = source.pop("identity", None)
            local.append(source)
        selected_sources = _source_versions(local, cutoff)
        by_source = {source["id"]: source for source in selected_sources}
        for source in selected_sources:
            sid = source["id"]
            source["id"] = asset + ":" + sid
            fiscal = source.get("fiscal", {})
            source_quarter = f"{fiscal.get('year', '')}{fiscal.get('period', '')}"
            source["consumers"] = [qid for qid, q in questions.items() if sid in _required(q, source_quarter)]
            sources.append(source)
        try:
            quarters = _names(root, base + "/cycles")
        except FileNotFoundError:
            quarters = []
        if proposed is not None and proposed[0] == asset:
            quarters = sorted(set(quarters) | {proposed[1]})
        initial = {}
        initial_sources = {}
        ambiguous_initial = set()
        for source in selected_sources:
            available = _available(source.get("available_at"), cutoff)
            fiscal = source.get("fiscal")
            if (source["kind"] == "financial_original" and _adapter._core._fiscal(fiscal)
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
            reviews = _reviews(root, base, quarter, cutoff, mode, gaps, candidate) if quarter in quarters else []
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
                    if not _analysis_valid(root, base, question.get("required_analysis", []),
                            unit.get("analysis_inputs", {}), asset + "/" + quarter + "/" + saved["id"], gaps):
                        # Preserve the saved completion claim for the assessor's
                        # invalidation action, but withdraw its reusable evidence.
                        item.pop("completion_evidence", None)
                    saved_cutoff = _adapter._core._instant(saved["cutoff"])
                    if not _candidate_evidence_valid(root, base, quarter, saved_cutoff, unit, by_source):
                        item.pop("completion_evidence", None)
                        gaps.append(dict(record=asset + "/" + quarter + "/" + saved["id"],
                            evidence="candidate:" + qid, reason="Candidate note or bound source changed or is not cutoff eligible",
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
                records=records), gaps


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


def publication_snapshot(root, *, _exclude=None):
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
                visit(path)
            else:
                result[path] = sha256(_bytes(root, path)).hexdigest()
    try:
        visit("investing")
    except OSError as error:
        raise ValueError("Publication conflict: unsafe or unreadable managed path; preserve files and inspect: " + str(error)) from error
    return result


def _preconditions(root, expected, target=None):
    _require(isinstance(expected, dict) and expected, "publication preconditions required")
    current = publication_snapshot(root, _exclude=target)
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


def _validate_proposal(root, request, staged):
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
    for qid, unit in review["units"].items():
        # Reused units retain all prior economic and authored dependencies.
        previous = request.get("previous", {}).get("units", {}).get(qid, {})
        if previous and unit.get("output") == previous.get("output"):
            _require(_adapter._core._same_json(unit, previous), "reused unit changes dependencies/checks without recomputing output")
            frozen = request.get("previous", {}).get("requirements")
            _require(frozen is None or _adapter._core._same_json(frozen.get(qid), questions[qid]), "reused unit changes declared dependencies")
        for field in ("output", "verification"):
            ref = unit.get(field, {}).get("path") if field == "output" else unit.get(field)
            if isinstance(ref, str) and ref.startswith(target + "/"):
                name = ref[len(target) + 1:]
                _require(name in files, "missing staged output/check")
                replacement = staged + "/" + name
                if field == "output":
                    unit[field]["path"] = replacement
                else:
                    unit[field] = replacement
    snapshot, gaps = _snapshot(root, _adapter._core._instant(review["cutoff"]), "latest", (asset, quarter, target, review))
    record = asset + "/" + quarter + "/" + review["id"]
    _require(not any(gap["record"] == record and gap["evidence"].startswith("candidate:") for gap in gaps),
             "candidate evidence must be independently cutoff eligible and frozen")
    result = _adapter.assess(snapshot, "latest", review["cutoff"])
    reusable = {item["work"] for item in result["reusable"] if item["record"] == record}
    _require(not request["complete"] or reusable == questions.keys(), "incomplete units or changed dependencies; save an explicit checkpoint or recompute")
    _require(not request["complete"] or not research["gaps"], "unresolved research gaps remain pending")
    return result


def _publish_markdown(root, asset, review, files, expected, run_id, complete):
    _require(type(complete) is bool and isinstance(files, dict), "publication arguments")
    _require(all(isinstance(name, str) and re.fullmatch(r"[a-zA-Z0-9_-]+\.md", name)
                 and name != "review.md" and isinstance(content, str)
                 for name, content in files.items()), "Markdown analysis filenames required")
    quarter, target = _target(asset, review)
    base = "investing/assets/equities/" + asset
    _require(asset in _research_config(root)["assets"], "asset outside configured scope")
    _require(isinstance(expected, dict) and expected, "publication preconditions required")
    for content in files.values():
        props, _ = _markdown.parse_note(content, _markdown.ANALYSIS_ROLES, asset_id=asset,
            fiscal_quarter=quarter, as_of=review["cutoff"], review_id=review["id"])
        _require(props.get("status") in ("complete", "partial"), "invalid analysis status")

    stage = "investing/.research-drafts/" + run_id
    _mkdir(root, stage, exclusive=True)
    for name, content in files.items():
        _write_new(root, stage + "/" + name, content.encode("utf-8"))

    cycle = base + "/cycles/" + quarter
    _mkdir(root, cycle)
    with _quarter_lock(root, cycle):
        _preconditions(root, expected)
        gaps = []
        entries = _managed_directories(root, cycle)
        cutoff = _adapter._core._instant(review["cutoff"])
        leaves = _reviews(root, base, quarter, cutoff, "latest", gaps) if entries else []
        _, draft_targets = _markdown_drafts(root)
        inherited = [gap for gap in gaps if gap["record"] not in draft_targets]
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
        for qid, unit in review.get("units", {}).items():
            output_path = unit.get("output", {}).get("path", "")
            if output_path.startswith(target + "/"):
                name = output_path[len(target) + 1:]
                _require(name in files and isinstance(unit.get("verification"), dict)
                         and _completion_valid(_verification(root, unit), unit["output"].get("digest"))
                         and sha256(files[name].encode("utf-8")).hexdigest() == unit["output"]["digest"],
                         "new Markdown output lacks valid inline verification: " + qid)

        provenance = {path: _registered_metadata(root, path) for path in expected
                      if path.startswith(base + "/data/sources/") or path.startswith(base + "/data/analysis/")}
        requirements = _unique(_asset_metadata(root, base)["questions"])
        saved = dict(review, provenance=provenance, requirements=requirements,
                     publication=dict(run=run_id, complete=complete))
        request = dict(asset=asset, review=saved, files=files, previous=previous, complete=complete)
        _validate_proposal(root, request, stage)
        content = _markdown.render_review(asset, quarter, saved)
        _, roundtrip = _markdown.record(content, "review", asset_id=asset, fiscal_quarter=quarter)
        _require(_encoded(roundtrip) == _encoded(saved), "Markdown review does not round-trip")
        _write_new(root, stage + "/review.md", content.encode("utf-8"))
        _mkdir(root, target, exclusive=True)
        for name in files:
            staged_bytes = _bytes(root, stage + "/" + name)
            _require(staged_bytes == files[name].encode("utf-8"), "staged analysis changed")
            _write_new(root, target + "/" + name, staged_bytes)
        _preconditions(root, expected, target)
        _require(all(_bytes(root, target + "/" + name) == files[name].encode("utf-8") for name in files)
                 and _bytes(root, stage + "/review.md") == content.encode("utf-8"), "staged review changed")
        _link_staged(root, stage, target, "review.md")
    return dict(status="complete" if complete else "checkpoint", review=target + "/review.md", run=run_id)


@contextmanager
def _quarter_lock(root, cycle):
    fd = _open(root, cycle, True)
    try:
        fcntl.flock(fd, fcntl.LOCK_EX)
        yield
    finally:
        os.close(fd)


def _link_staged(root, stage, target, name):
    """Commit a flushed marker without linking the editable draft to it."""
    commit = ".publication-marker"
    _write_new(root, stage + "/" + commit, _bytes(root, stage + "/" + name))
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


def publish(root, asset, review, files, expected, run_id, *, complete=True, storage="legacy"):
    """Save one append-only review, completion last; recover using its run ID."""
    _id(run_id)
    _require(storage in ("legacy", "markdown"), "unsupported research storage")
    if storage == "markdown":
        return _publish_markdown(root, asset, review, files, expected, run_id, complete)
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
    request = dict(version=1, asset=asset, review=review, files=files, expected=expected,
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
            _preconditions(root, request["expected"], target)
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
    return data


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
    _preconditions(root, request["expected"], target)
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
        _preconditions(root, request["expected"], target)
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
    _preconditions(root, request["expected"], target)
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
                else:
                    if published == raw:
                        continue
        except (FileNotFoundError, ValueError, KeyError, TypeError, UnicodeError):
            pass
        gaps.append(dict(record=stage, evidence="publication:" + run_id,
            reason="Unfinished Markdown draft retained; no completed view advanced",
            recovery="Inspect the draft and retry from the previous valid record"))
    return gaps, targets


def discover(root, mode, cutoff, *, candidate_for=None):
    """Derive accepted assessment input from saved metadata, without writes.

    Unsupported/ambiguous layouts raise ValueError with existing data preserved.
    Recorded completion checks are attestations, never analytical approval.
    """
    try:
        _adapter._require(mode in ("historical", "latest"), "mode")
        _adapter._timestamp(cutoff)
        boundary = Path(root).absolute()
        _require(not any(p.is_symlink() for p in (boundary, *boundary.parents)), "symlink root")
        snapshot, gaps = _snapshot(boundary, _adapter._core._instant(cutoff), mode)
        result = _adapter.assess(snapshot, mode, cutoff)
        if candidate_for is not None:
            asset, quarter = candidate_for
            _require(_id(asset) in _research_config(boundary)["assets"], "asset outside configured scope")
            _require(re.fullmatch(r"[0-9]{4}Q[1-4]", quarter), "invalid fiscal directory")
            base = "investing/assets/equities/" + asset
            result["candidate_notes"] = [
                dict(path=path, digest=sha256(_bytes(boundary, path)).hexdigest())
                for path in _note_references(boundary, base, quarter)
            ]
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
