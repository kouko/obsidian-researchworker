"""Bounded, read-only prototype-v1 local evidence adapter; see README input contract."""

import argparse
from datetime import datetime
import importlib.util
import json
import math
import os
from pathlib import Path
import sys
import stat

# Import without adding search paths or writing a bytecode cache in the input tree.
_spec = importlib.util.spec_from_file_location("work_assessment", Path(__file__).with_name("work_assessment.py"))
_core = importlib.util.module_from_spec(_spec)
exec(compile(_spec.loader.get_source("work_assessment"), _spec.origin, "exec"), _core.__dict__)
assess = _core.assess


def _require(condition, field):
    if not condition:
        raise ValueError("invalid field " + field)


def _text(value):
    return isinstance(value, str) and bool(value.strip())


def _strings(value):
    return isinstance(value, list) and all(_text(v) for v in value)


def _timestamp(value):
    _require(_text(value), "cutoff")
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as error:
        raise ValueError("invalid cutoff: " + value) from error
    _require(parsed.utcoffset() is not None, "cutoff timezone")


def _read(root, reference):
    _require(_text(reference), "local reference")
    path = Path(reference)
    if path.is_absolute() or ".." in path.parts:
        raise ValueError("Reference outside assessment root: " + reference)
    _require(bool(path.parts), "local file reference")
    # Reject symlinks before reading; includes intermediate components, even
    # in-root symlinks, to keep the prototype boundary explicit and inspectable.
    current = root
    for part in path.parts:
        current = current / part
        if current.is_symlink():
            raise ValueError("Reference outside assessment root: " + reference)
    resolved = current.resolve()
    if not resolved.is_relative_to(root):
        raise ValueError("Reference outside assessment root: " + reference)
    descriptor = os.open(root, os.O_RDONLY | os.O_DIRECTORY)
    try:
        # dir_fd + O_NOFOLLOW also close the check/open symlink race. Only
        # regular local files are data; opening a FIFO must never block a check.
        for part in path.parts[:-1]:
            child = os.open(part, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=descriptor)
            os.close(descriptor)
            descriptor = child
        child = os.open(path.parts[-1], os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK, dir_fd=descriptor)
        with os.fdopen(child, encoding="utf-8") as stream:
            _require(stat.S_ISREG(os.fstat(stream.fileno()).st_mode), "regular local file " + reference)
            return stream.read()
    except (OSError, UnicodeError) as error:
        raise ValueError(f"{reference}: {error}") from error
    finally:
        os.close(descriptor)


def _json(text):
    def unique(pairs):
        result = {}
        for key, value in pairs:
            _require(key not in result, "duplicate JSON key " + key)
            result[key] = value
        return result
    def invalid(value):
        raise ValueError("non-finite JSON value " + value)
    def number(value):
        result = float(value)
        _require(math.isfinite(result), "finite JSON number")
        return result
    return json.loads(text, object_pairs_hook=unique, parse_constant=invalid, parse_float=number)


def _load(root, reference):
    data = _json(_read(root, reference))
    _require(isinstance(data, dict), "snapshot object")
    if type(data.get("version")) is not int or data["version"] != 1:
        raise ValueError("Unsupported assessment input version")
    for group in ("sources", "records"):
        _require(isinstance(data.get(group), list), group)
        identities = set()
        for item in data[group]:
            _require(isinstance(item, dict), group + " item")
            _require(_text(item.get("id")) and item["id"] not in identities, group + " unique id")
            identities.add(item["id"])
            _require(_text(item.get("issuer")), group + " issuer")
    for source in data["sources"]:
        _require(_text(source.get("kind")), "source kind")
        for key in ("version", "available_at"):
            _require(source.get(key) is None or _text(source[key]), "source " + key)
        if "projection_ref" in source:
            _require("projection" not in source, "projection or projection_ref, not both")
            source["projection"] = _json(_read(root, source.pop("projection_ref")))
        _require("consumers" not in source or _strings(source["consumers"]), "consumers")
        _require("fiscal" not in source or isinstance(source["fiscal"], dict), "source fiscal")
    for record in data["records"]:
        _timestamp(record.get("cutoff"))
        _require("fiscal" not in record or isinstance(record["fiscal"], dict), "record fiscal")
        _require(_strings(record.get("required_sources")), "required_sources")
        _require(isinstance(record.get("work"), list), "work")
        identities = set()
        for work in record["work"]:
            _require(isinstance(work, dict), "work item")
            _require(_text(work.get("id")) and work["id"] not in identities, "work unique id")
            identities.add(work["id"])
            _require(work.get("status") in ("complete", "missing"), "work status")
            _require(_strings(work.get("depends_on", [])), "depends_on")
            _require(isinstance(work.get("consumed", {}), dict), "consumed")
            for sid, consumed in work.get("consumed", {}).items():
                _require(_text(sid) and isinstance(consumed, dict), "consumed source")
                _require(set(consumed) == {"version", "projection"} and _text(consumed["version"]), "consumed identity")
            if "output" in work:
                output = work["output"]
                _require(isinstance(output, dict) and "content" not in output, "output must reference local content")
                _require("digest" not in output or isinstance(output["digest"], str), "output digest")
                if "path" in output:
                    output["content"] = _read(root, output["path"])
            if "completion_evidence" in work:
                evidence = work["completion_evidence"]
                _require(isinstance(evidence, str), "completion_evidence")
                if evidence:
                    work["completion_evidence"] = _read(root, evidence).strip()
    return data


def run(root, snapshot, mode, cutoff, *, stdout=None, stderr=None):
    """Print one assessment JSON; return 0/2/1/64, never write supplied inputs.

    root is an explicit directory; snapshot and all references are root-relative.
    stdout/stderr may be text streams. KeyboardInterrupt propagates without state.
    """
    stdout = sys.stdout if stdout is None else stdout
    stderr = sys.stderr if stderr is None else stderr
    try:
        _require(mode in ("historical", "latest"), "mode")
        _timestamp(cutoff)
        _require(isinstance(root, (str, Path)) and bool(str(root)), "root")
        _require(_text(snapshot), "snapshot")
    except (ValueError, TypeError, OverflowError) as error:
        print(f"Invalid assessment request: {error}; correct the request and retry", file=stderr)
        return 64
    try:
        boundary = Path(root).resolve(strict=True)
        _require(boundary.is_dir(), "root directory")
        data = _load(boundary, snapshot)
        if mode == "historical" and any(datetime.fromisoformat(r["cutoff"].replace("Z", "+00:00")) != datetime.fromisoformat(cutoff.replace("Z", "+00:00")) for r in data["records"]):
            print("Invalid assessment request: historical cutoff must match saved records; correct cutoff and retry", file=stderr)
            return 64
        result = assess(data, mode, cutoff)
    except (ValueError, TypeError, KeyError, OSError, RecursionError, OverflowError) as error:
        print(f"Cannot read assessment input {snapshot}: {error}; supply correct in-root prototype-v1 evidence and retry", file=stderr)
        return 1
    print(json.dumps(result, sort_keys=True, ensure_ascii=False, allow_nan=False), file=stdout)
    return 2 if result["status"] == "partial" else 0


class _Parser(argparse.ArgumentParser):
    def error(self, message):
        raise ValueError(message)


def main(argv=None):
    parser = _Parser(description=__doc__)
    for name in ("root", "snapshot", "mode", "cutoff"):
        parser.add_argument("--" + name, required=True)
    try:
        args = parser.parse_args(argv)
    except ValueError as error:
        print(f"Invalid assessment request: {error}; correct arguments and retry", file=sys.stderr)
        return 64
    return run(args.root, args.snapshot, args.mode, args.cutoff)


if __name__ == "__main__":
    sys.exit(main())
