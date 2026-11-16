"""Read-only investing metadata discovery. See README for the version-1 contract."""

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
        for part in Path(root).parts[1:]:
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


def _reviews(root, base, quarter, cutoff, mode, gaps):
    saved = {}
    for directory in _names(root, base + "/cycles/" + quarter):
        _id(directory)
        path = base + "/cycles/" + quarter + "/" + directory
        review = _object(root, path + "/review.json")
        rid = _id(review["id"])
        _require(rid not in saved, "duplicate review identity")
        _adapter._timestamp(review["cutoff"])
        saved[rid] = (path, review)
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
        eligible = {rid: pair for rid, pair in saved.items()
                    if (_adapter._core._instant(pair[1]["cutoff"]) == cutoff if mode == "historical"
                        else _adapter._core._instant(pair[1]["cutoff"]) <= cutoff)}
        parents = {pair[1].get("predecessor") for pair in eligible.values()}
        leaves = [pair for rid, pair in eligible.items() if rid not in parents]
        _require(len(leaves) == 1, "missing cutoff review or ambiguous competing reviews")
        return leaves
    except ValueError as error:
        gaps.append(dict(record=base + "/cycles/" + quarter, evidence="reviews", reason=str(error), recovery="Repair review metadata or provide the requested cutoff review; preserve existing research"))
        return []


def _snapshot(root, cutoff, mode):
    config = _object(root, "investing/research.json")
    _require(isinstance(config.get("assets"), list) and config["assets"], "missing asset scope")
    assets = [_id(asset) for asset in config["assets"]]
    _require(len(set(assets)) == len(assets), "duplicate asset identity")
    sources, records, gaps = [], [], []
    for asset in assets:
        base = "investing/assets/equities/" + asset
        metadata = _object(root, base + "/asset.json")
        _require(metadata.get("id") == asset and _adapter._text(metadata.get("issuer")), "asset identity mismatch")
        issuer = metadata["issuer"]
        questions = _unique(metadata["questions"])
        _require(questions, "required questions missing")
        for question in questions.values():
            _require(_adapter._strings(question.get("required_sources")) and _adapter._strings(question.get("depends_on", [])), "question dependencies")
            _require(set(question.get("depends_on", [])) <= questions.keys(), "unknown question dependency")
            _required(question, "2024Q1")  # Validate the sole literal template.
        local = []
        for name in _names(root, base + "/data/sources"):
            _require(name.endswith(".json"), "unsupported source metadata")
            source = _object(root, base + "/data/sources/" + name)
            _require(source.get("issuer") == issuer, "source issuer mismatch")
            _require(_adapter._text(source.get("kind")), "source kind")
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
        if not quarters:
            initial = {}
            for source in selected_sources:
                available = _available(source.get("available_at"), cutoff)
                fiscal = source.get("fiscal")
                if (source["kind"] == "financial_original" and _adapter._core._fiscal(fiscal)
                        and available is not None and available <= cutoff
                        and fiscal["period_end"] <= source["available_at"][:10]):
                    quarter = f"{fiscal['year']}{fiscal['period']}"
                    _require(quarter not in initial or initial[quarter] == fiscal, "ambiguous initial fiscal identity")
                    initial[quarter] = fiscal
            for quarter, fiscal in sorted(initial.items()):
                records.append(dict(id=asset + "/" + quarter + "/new", issuer=issuer, fiscal=fiscal,
                    cutoff=cutoff.isoformat(), required_sources=_required_all(questions, asset, quarter),
                    work=[dict(id=qid, status="missing", depends_on=q.get("depends_on", []), consumed={}) for qid, q in questions.items()]))
            if not initial:
                gaps.append(dict(record=asset, evidence="fiscal", reason="No eligible source-declared initial fiscal quarter", recovery="Supply original filing evidence and fiscal metadata; do not infer a calendar quarter"))
        for quarter in quarters:
            _require(re.fullmatch(r"[0-9]{4}Q[1-4]", quarter), "invalid fiscal directory")
            for path, saved in _reviews(root, base, quarter, cutoff, mode, gaps):
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
                        checks = check.get("checks", {})
                        complete = (isinstance(checks, dict) and set(checks) == {"sources", "citations", "calculations", "counterevidence"}
                                    and all(value is True for value in checks.values())
                                    and check.get("unresolved") == [] and item.get("output", {}).get("digest") == check.get("output_digest"))
                        if complete:
                            item.update(status="complete", completion_evidence=json.dumps(check, sort_keys=True))
                    work.append(item)
                records.append(dict(id=asset + "/" + quarter + "/" + saved["id"], issuer=issuer, fiscal=fiscal,
                    cutoff=saved["cutoff"], required_sources=_required_all(questions, asset, quarter), work=work,
                    **{k: saved[k] for k in ("execution_state", "last_attempt", "last_success") if k in saved}))
    return dict(version=1, sources=sources, records=records), gaps


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
        if gaps:
            result["gaps"].extend(gaps)
            result["status"] = "partial"
        return result
    except (OSError, KeyError, TypeError, UnicodeError) as error:
        raise ValueError(f"Cannot discover version-1 investing research: {error}; supply missing metadata or repair the reference and retry") from error
