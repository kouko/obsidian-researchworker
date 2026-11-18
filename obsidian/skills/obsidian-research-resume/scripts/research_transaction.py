"""Lock, apply, and recover a preflighted research update on a local vault."""

import argparse
import base64
import hashlib
import json
import os
import re
import stat
import sys
import tempfile
from pathlib import Path

try:
    import fcntl
except ImportError:
    fcntl = None


JOURNAL = ".resume-recovery.json"
TEMP_PREFIX = ".resume-write-"
TEMP_NAME = re.compile(r"\.resume-write-[a-z0-9_]{8}")


class TransactionError(Exception):
    """The update cannot safely proceed."""


def local_path(folder, name):
    if not isinstance(name, str):
        raise TransactionError("expected a relative file path")
    path = Path(name)
    if path.is_absolute() or not path.parts or ".." in path.parts:
        raise TransactionError(f"unsafe relative path: {name}")
    target = folder
    for part in path.parts:
        if part == JOURNAL or TEMP_NAME.fullmatch(part):
            raise TransactionError(f"reserved transaction path: {name}")
        target /= part
        if target.is_symlink():
            raise TransactionError(f"symlink in transaction path: {name}")
    return target


def raise_scan_error(error):
    raise error


def snapshot_entries(folder):
    entries = {}
    for directory, subdirs, files in os.walk(folder, onerror=raise_scan_error):
        for filename in subdirs + files:
            path = Path(directory) / filename
            name = path.relative_to(folder).as_posix()
            if name == JOURNAL:
                continue
            if path.is_symlink():
                entries[name] = ["symlink", os.readlink(path)]
            elif path.is_dir():
                entries[name] = ["dir"]
            elif path.is_file():
                if not TEMP_NAME.fullmatch(filename):
                    entries[name] = ["file", hashlib.sha256(path.read_bytes()).hexdigest()]
            else:
                raise TransactionError(f"unsupported directory entry: {name}")
    return entries


def state_digest(entries):
    return hashlib.sha256(json.dumps(entries, sort_keys=True).encode()).hexdigest()


def file_content(path):
    if not path.exists():
        return None
    if not path.is_file():
        raise TransactionError(f"expected a regular file: {path}")
    return path.read_bytes()


def encode(data):
    return None if data is None else base64.b64encode(data).decode("ascii")


def decode(data):
    if not isinstance(data, str):
        raise TransactionError("expected base64 file content")
    return base64.b64decode(data, validate=True)


def write_atomically(path, data, *, exclusive=False):
    fd, temporary_name = tempfile.mkstemp(prefix=TEMP_PREFIX, dir=path.parent)
    temporary = Path(temporary_name)
    try:
        with os.fdopen(fd, "wb") as stream:
            if path.exists():
                os.fchmod(stream.fileno(), stat.S_IMODE(path.stat().st_mode))
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        if exclusive:
            os.link(temporary, path)
        else:
            os.replace(temporary, path)
    finally:
        temporary.unlink(missing_ok=True)


def replace_file(path, data):
    write_atomically(path, data)


def valid_history(folder, entry, completed_round, writes):
    for name in (entry, completed_round):
        path = local_path(folder, name)
        data = writes[path][0] if path in writes else file_content(path)
        if path.suffix != ".md" or not data or not data.strip():
            raise TransactionError(f"missing prior entry or completed round: {name}")


def read_writes(folder, records, *, recovery=False):
    if not isinstance(records, list):
        raise TransactionError("expected an ordered list of writes")
    writes = {}
    for record in records:
        path = local_path(folder, record["path"])
        if path in writes:
            raise TransactionError(f"duplicate write: {record['path']}")
        after = decode(record["content"])
        old = record["before"] if recovery else None
        before = (None if old is None else decode(old)) if recovery else file_content(path)
        writes[path] = (before, after)
    for path in writes:
        for parent in path.parents:
            if parent == folder:
                break
            if parent in writes or (parent.exists() and not parent.is_dir()):
                raise TransactionError(f"invalid parent for write: {path}")
    return writes


def check_targets(folder, names, writes):
    if not isinstance(names, list):
        raise TransactionError("expected a list of required targets")
    for name in names:
        path = local_path(folder, name)
        if path not in writes and not path.is_file():
            raise TransactionError(f"required local target is missing: {name}")


def finish(folder, writes, targets):
    check_targets(folder, targets, writes)
    states = {path: file_content(path) for path in writes}
    for path, (before, after) in writes.items():
        if states[path] not in (before, after):
            raise TransactionError(f"unexpected edit blocks recovery: {path}")
    for path, (_, after) in writes.items():
        if states[path] != after:
            local_path(folder, path.relative_to(folder).as_posix())
            path.parent.mkdir(parents=True, exist_ok=True)
            replace_file(path, after)
    for path, (_, after) in writes.items():
        if file_content(path) != after:
            raise TransactionError(f"write could not be verified: {path}")
    check_targets(folder, targets, {})


def missing_directories(folder, writes):
    directories = set()
    for path in writes:
        for parent in path.parents:
            if parent == folder:
                break
            if not parent.exists():
                directories.add(parent.relative_to(folder).as_posix())
    return sorted(directories)


def check_recovery_snapshot(folder, plan, writes):
    entries = snapshot_entries(folder)
    for path, (before, _) in writes.items():
        name = path.relative_to(folder).as_posix()
        if before is None:
            entries.pop(name, None)
        else:
            entries[name] = ["file", hashlib.sha256(before).hexdigest()]
    for name in plan["directories"]:
        path = local_path(folder, name)
        if not any(path in destination.parents for destination in writes):
            raise TransactionError(f"unexpected recovery directory: {name}")
        if name in entries and entries[name] != ["dir"]:
            raise TransactionError(f"unexpected edit to recovery directory: {name}")
        entries.pop(name, None)
    if state_digest(entries) != plan["snapshot"]:
        raise TransactionError("unexpected folder changes block recovery")


def check_journal(folder):
    journal = folder / JOURNAL
    if journal.is_symlink() or (journal.exists() and not journal.is_file()):
        raise TransactionError("unsafe recovery record")
    return journal


def recover(folder):
    journal = check_journal(folder)
    if not journal.exists():
        return None
    plan = json.loads(journal.read_text())
    writes = read_writes(folder, plan["writes"], recovery=True)
    valid_history(folder, plan["entry"], plan["round"], writes)
    check_recovery_snapshot(folder, plan, writes)
    finish(folder, writes, plan["targets"])
    journal.unlink()
    return "completed"


def apply(folder, plan):
    journal = check_journal(folder)
    if journal.exists() or plan["snapshot"] != state_digest(snapshot_entries(folder)):
        raise TransactionError("stale snapshot; inspect the folder again")
    writes = read_writes(folder, plan["writes"])
    valid_history(folder, plan["entry"], plan["round"], writes)
    check_targets(folder, plan["targets"], writes)
    writes = {path: (before, after) for path, (before, after) in writes.items()
              if before != after}
    if not writes:
        return []
    paths = [path.relative_to(folder).as_posix() for path in writes]
    record = {
        "snapshot": plan["snapshot"],
        "directories": missing_directories(folder, writes),
        "entry": plan["entry"],
        "round": plan["round"],
        "targets": plan["targets"],
        "writes": [
            {"path": path.relative_to(folder).as_posix(),
             "before": encode(before), "content": encode(after)}
            for path, (before, after) in writes.items()
        ],
    }
    write_atomically(journal, json.dumps(record).encode(), exclusive=True)
    finish(folder, writes, record["targets"])
    journal.unlink()
    return paths


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("inspect", "apply"))
    parser.add_argument("vault", type=Path)
    parser.add_argument("folder", type=Path)
    parser.add_argument("--read", action="append", default=[], metavar="RELATIVE_FILE")
    args = parser.parse_args()
    if args.action == "apply" and args.read:
        parser.error("--read is only available with inspect")
    try:
        if fcntl is None:
            raise TransactionError("directory locking is unavailable")
        vault = args.vault.resolve(strict=True)
        folder = (vault / args.folder).resolve(strict=True)
        if folder == vault or not folder.is_relative_to(vault) or not folder.is_dir():
            raise TransactionError("research folder must be inside the selected vault")
        fd = os.open(folder, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
        try:
            try:
                fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
            except BlockingIOError as error:
                raise TransactionError("research folder is busy") from error
            if args.action == "inspect":
                read_paths = {name: local_path(folder, name) for name in args.read}
                recovery = recover(folder)
                entries = snapshot_entries(folder)
                files = {name: encode(file_content(path)) for name, path in read_paths.items()}
                print(json.dumps({
                    "recovery": recovery,
                    "snapshot": state_digest(entries),
                    "paths": sorted(entries),
                    "files": files,
                }))
            else:
                changed = apply(folder, json.load(sys.stdin))
                print(json.dumps({"changed": changed}))
        finally:
            os.close(fd)
    except (TransactionError, OSError, KeyError, TypeError, ValueError) as error:
        print(f"research transaction: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
