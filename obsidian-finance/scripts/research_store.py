"""Bounded investing discovery and append publication; see README's v1 contract."""

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
            metadata = _object(root, base + "/data/analysis/" + identity + ".json")
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


def _reviews(root, base, quarter, cutoff, mode, gaps, proposed=None):
    gaps_start = len(gaps)
    saved = {}
    withdrawn = set()
    try:
        directories = _names(root, base + "/cycles/" + quarter)
    except FileNotFoundError:
        _require(proposed is not None, "missing quarter directory")
        directories = []
    for directory in directories:
        _id(directory)
        path = base + "/cycles/" + quarter + "/" + directory
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
                        check = _object(root, unit["verification"])
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
    config = _object(root, "investing/research.json")
    _require(isinstance(config.get("assets"), list) and config["assets"], "missing asset scope")
    assets = [_id(asset) for asset in config["assets"]]
    _require(len(set(assets)) == len(assets), "duplicate asset identity")
    sources, records, gaps = [], [], []
    for asset in assets:
        records_start = len(records)
        base = "investing/assets/equities/" + asset
        metadata = _object(root, base + "/asset.json")
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
            _require(name.endswith(".json"), "unsupported source metadata")
            source = _object(root, base + "/data/sources/" + name)
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
        ambiguous_initial = set()
        for source in selected_sources:
            available = _available(source.get("available_at"), cutoff)
            fiscal = source.get("fiscal")
            if (source["kind"] == "financial_original" and _adapter._core._fiscal(fiscal)
                    and available is not None and available <= cutoff
                    and fiscal["period_end"] <= source["available_at"][:10]):
                quarter = f"{fiscal['year']}{fiscal['period']}"
                if initial.setdefault(quarter, fiscal) != fiscal:
                    ambiguous_initial.add(quarter)
        for quarter in sorted(set(quarters) | initial.keys()):
            _require(re.fullmatch(r"[0-9]{4}Q[1-4]", quarter), "invalid fiscal directory")
            candidate = proposed[2:] if proposed is not None and proposed[:2] == (asset, quarter) else None
            reviews = _reviews(root, base, quarter, cutoff, mode, gaps, candidate) if quarter in quarters else []
            if not reviews and quarter in ambiguous_initial:
                gaps.append(dict(record=asset + "/" + quarter + "/new", evidence="fiscal",
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
                            check = _object(root, unit["verification"])
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
    return dict(version=1, sources=sources, records=records), gaps


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
            if path == "investing/.research-runs" or path == _exclude:
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
    metadata = _object(root, base + "/asset.json")
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
            if ref and ref.startswith(target + "/"):
                name = ref[len(target) + 1:]
                _require(name in files, "missing staged output/check")
                replacement = staged + "/" + name
                if field == "output":
                    unit[field]["path"] = replacement
                else:
                    unit[field] = replacement
    snapshot, _ = _snapshot(root, _adapter._core._instant(review["cutoff"]), "latest", (asset, quarter, target, review))
    result = _adapter.assess(snapshot, "latest", review["cutoff"])
    record = asset + "/" + quarter + "/" + review["id"]
    reusable = {item["work"] for item in result["reusable"] if item["record"] == record}
    _require(not request["complete"] or reusable == questions.keys(), "incomplete units or changed dependencies; save an explicit checkpoint or recompute")
    _require(not request["complete"] or not research["gaps"], "unresolved research gaps remain pending")
    return result


def publish(root, asset, review, files, expected, run_id, *, complete=True):
    """Save one append-only review, completion last; recover using its run ID."""
    _id(run_id)
    _require(type(complete) is bool and isinstance(files, dict), "publication arguments")
    _require(all(isinstance(name, str) and re.fullmatch(r"[a-zA-Z0-9_-]+\.(md|json)", name)
                 and name not in ("review.json", "pending.json", "withdrawn.json", "abandoned.json")
                 and isinstance(content, str) for name, content in files.items()), "plain output filenames and UTF-8 text required")
    _preconditions(root, expected)
    quarter, target = _target(asset, review)
    base = "investing/assets/equities/" + asset
    _require(asset in _object(root, "investing/research.json")["assets"], "asset outside configured scope")
    try:
        entries = _names(root, base + "/cycles/" + quarter)
    except FileNotFoundError:
        entries = []
    _require(target.rsplit("/", 1)[1] not in entries, "review destination already exists; recover its recorded run")
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
    provenance = {path: _object(root, path) for path in expected
                  if path.startswith(base + "/data/sources/") or path.startswith(base + "/data/analysis/")}
    requirements = _unique(_object(root, base + "/asset.json")["questions"])
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
        journal = _object(root, run + "/journal.json")
        raw = _bytes(root, run + "/request.json")
        _require(sha256(raw).hexdigest() == journal["request_digest"], "Publication conflict: draft edited; preserve it and inspect")
        request = _object(root, run + "/request.json")
        quarter, target = _target(request["asset"], request["review"])
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
            # Descendants cannot safely lose their predecessor's completed view.
            for directory in _names(root, "investing/assets/equities/" + request["asset"] + "/cycles/" + quarter) if present else []:
                reference = "investing/assets/equities/" + request["asset"] + "/cycles/" + quarter + "/" + directory + "/review.json"
                try:
                    other = _object(root, reference)
                except FileNotFoundError:
                    continue
                _require(other.get("predecessor") != request["review"]["id"], "Publication conflict: descendant review exists")
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
    except (KeyError, TypeError, UnicodeError, NotADirectoryError, IsADirectoryError, FileExistsError) as error:
        raise ValueError("Cannot recover publication; preserve journal and draft: " + str(error)) from error


def discover(root, mode, cutoff):
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
        if gaps:
            result["gaps"].extend(gaps)
            result["status"] = "partial"
        return result
    except (OSError, KeyError, TypeError, UnicodeError) as error:
        raise ValueError(f"Cannot discover version-1 investing research: {error}; supply missing metadata or repair the reference and retry") from error
