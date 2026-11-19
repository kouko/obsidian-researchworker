"""Create, inspect, or apply a research project transaction in a local vault."""

import argparse
import base64
import hashlib
import json
import os
import stat
import sys
from contextlib import contextmanager
from pathlib import Path
from unicodedata import normalize

try:
    import fcntl
except ImportError:
    fcntl = None


JOURNAL = ".resume-recovery.json"
STAGING = ".resume-staging"
STAGING_MARKER = ".research-transaction-v1"
STAGING_PAYLOAD = "payload"
FIRST_ROUND_PENDING = ".research-first-round-pending"


class TransactionError(Exception):
    """The update cannot safely proceed."""


def spelling_key(name):
    return normalize("NFD", normalize("NFD", name).casefold())


def require_spelling(path):
    if not path.parent.is_dir():
        return
    names = os.listdir(path.parent)
    if path.name in names:
        return
    if path.exists() or path.is_symlink() or any(
        spelling_key(name) == spelling_key(path.name) for name in names
    ):
        raise TransactionError(f"path aliases an existing entry: {path}")


def local_path(folder, name):
    if not isinstance(name, str):
        raise TransactionError("expected a relative file path")
    path = Path(name)
    if path.is_absolute() or not path.parts or ".." in path.parts:
        raise TransactionError(f"unsafe relative path: {name}")
    target = folder
    for part in path.parts:
        spelling = spelling_key(part)
        if spelling in (JOURNAL, STAGING, FIRST_ROUND_PENDING):
            raise TransactionError(f"reserved transaction path: {name}")
        target /= part
        require_spelling(target)
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


def require_snapshot_content(entries, name, data):
    observed = None if data is None else ["file", hashlib.sha256(data).hexdigest()]
    if entries.get(name) != observed:
        raise TransactionError("stale snapshot; inspect the folder again")


def encode(data):
    return None if data is None else base64.b64encode(data).decode("ascii")


def decode(data):
    if not isinstance(data, str):
        raise TransactionError("expected base64 file content")
    return base64.b64decode(data, validate=True)


def clear_staging(folder):
    stage = folder / STAGING
    require_spelling(stage)
    try:
        info = stage.lstat()
    except FileNotFoundError:
        return
    if not stat.S_ISDIR(info.st_mode) or info.st_uid != os.getuid() or info.st_mode & 0o077:
        raise TransactionError("unsafe staging location")
    children = {child.name: child.lstat() for child in stage.iterdir()}
    marker = children.get(STAGING_MARKER)
    if (marker is None or marker.st_size
            or children.keys() - {STAGING_MARKER, STAGING_PAYLOAD}
            or any(not stat.S_ISREG(info.st_mode) or info.st_uid != os.getuid()
                   for info in children.values())):
        raise TransactionError("unrecognized staging contents")
    (stage / STAGING_PAYLOAD).unlink(missing_ok=True)
    (stage / STAGING_MARKER).unlink()
    stage.rmdir()


def write_atomically(path, data, *, folder, expected=None, exclusive=False):
    stage = folder / STAGING
    stage.mkdir(mode=0o700)
    temporary = stage / STAGING_PAYLOAD
    try:
        (stage / STAGING_MARKER).touch(mode=0o600, exist_ok=False)
        fd = os.open(temporary, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        with os.fdopen(fd, "wb") as stream:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
            if exclusive:
                check_journal(folder)
            else:
                local_path(folder, path.relative_to(folder).as_posix())
                if expected is not None and path.is_file():
                    os.fchmod(stream.fileno(), stat.S_IMODE(path.stat().st_mode))
                if file_content(path) != expected:
                    raise TransactionError(f"unexpected edit before replacement: {path}")
            if expected is None:
                os.link(temporary, path)
            else:
                os.replace(temporary, path)
    finally:
        clear_staging(folder)


def valid_history(folder, entry, completed_round, writes, *, creating=False):
    for name in (entry, completed_round):
        path = local_path(folder, name)
        if creating:
            data = writes[path][1] if path in writes else None
        else:
            data = writes[path][0] if path in writes else file_content(path)
        if path.suffix != ".md" or not data or not data.strip():
            raise TransactionError(f"missing prior entry or completed round: {name}")


def read_writes(folder, records, *, recovery=False):
    if not isinstance(records, list):
        raise TransactionError("expected an ordered list of writes")
    writes = {}
    spellings = {}
    for record in records:
        path = local_path(folder, record["path"])
        if path in writes:
            raise TransactionError(f"duplicate write: {record['path']}")
        parts = path.relative_to(folder).parts
        for length in range(1, len(parts) + 1):
            prefix = parts[:length]
            key = tuple(spelling_key(part) for part in prefix)
            if spellings.setdefault(key, prefix) != prefix:
                raise TransactionError(f"planned paths alias each other: {record['path']}")
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


def check_write_devices(folder, writes):
    device = folder.stat().st_dev
    for path in writes:
        parent = path.parent
        while not parent.exists():
            parent = parent.parent
        if parent.stat().st_dev != device:
            name = path.relative_to(folder)
            raise TransactionError(f"write destination is on a different filesystem: {name}")


def finish(folder, writes, targets):
    check_write_devices(folder, writes)
    check_targets(folder, targets, writes)
    for path, (before, after) in writes.items():
        if file_content(path) not in (before, after):
            raise TransactionError(f"unexpected edit blocks recovery: {path}")
    for path, (before, after) in writes.items():
        local_path(folder, path.relative_to(folder).as_posix())
        current = file_content(path)
        if current == after:
            continue
        if current != before:
            raise TransactionError(f"unexpected edit before replacement: {path}")
        path.parent.mkdir(parents=True, exist_ok=True)
        write_atomically(path, after, folder=folder, expected=before)
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


def check_recovery_snapshot(folder, plan, writes, *, completed=False):
    entries = snapshot_entries(folder)
    for path, (before, after) in writes.items():
        name = path.relative_to(folder).as_posix()
        if completed and entries.get(name) != ["file", hashlib.sha256(after).hexdigest()]:
            raise TransactionError(f"write could not be verified: {path}")
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
    require_spelling(journal)
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
    check_recovery_snapshot(folder, plan, writes, completed=True)
    journal.unlink()
    return "completed"


def apply(folder, plan):
    journal = check_journal(folder)
    if journal.exists():
        raise TransactionError("stale snapshot; inspect the folder again")
    entries = snapshot_entries(folder)
    if plan["snapshot"] != state_digest(entries):
        raise TransactionError("stale snapshot; inspect the folder again")
    writes = read_writes(folder, plan["writes"])
    for path, (before, _) in writes.items():
        require_snapshot_content(entries, path.relative_to(folder).as_posix(), before)
    valid_history(folder, plan["entry"], plan["round"], writes)
    check_targets(folder, plan["targets"], writes)
    writes = {path: (before, after) for path, (before, after) in writes.items()
              if before != after}
    if not writes:
        return []
    check_write_devices(folder, writes)
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
    if snapshot_entries(folder) != entries:
        raise TransactionError("stale snapshot; inspect the folder again")
    write_atomically(journal, json.dumps(record).encode(), folder=folder, exclusive=True)
    finish(folder, writes, record["targets"])
    check_recovery_snapshot(folder, record, writes, completed=True)
    journal.unlink()
    return paths


def require_child_spelling(fd, name):
    key = spelling_key(name)
    if any(child != name and spelling_key(child) == key for child in os.listdir(fd)):
        raise TransactionError(f"path aliases an existing entry: {name}")


@contextmanager
def open_directories(root_fd, parts, *, create=False, exclusive=False, identities=None):
    fd = os.dup(root_fd)
    try:
        for index, name in enumerate(parts):
            require_child_spelling(fd, name)
            if create:
                try:
                    os.mkdir(name, dir_fd=fd)
                except FileExistsError:
                    if exclusive and index == len(parts) - 1:
                        raise
            expected = os.stat(name, dir_fd=fd, follow_symlinks=False)
            child_fd = os.open(name, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=fd)
            os.close(fd)
            fd = child_fd
            observed = os.fstat(fd)
            if not os.path.samestat(expected, observed):
                raise TransactionError(f"directory changed during initial save: {name}")
            if identities is not None:
                path = parts[:index + 1]
                if not os.path.samestat(identities.setdefault(path, observed), observed):
                    raise TransactionError(f"directory changed during initial save: {name}")
        yield fd
    finally:
        os.close(fd)


def write_initial_file(project_fd, path, data, *, identities):
    with open_directories(project_fd, path.parent.parts, create=True, identities=identities) as fd:
        if os.fstat(fd).st_dev != os.fstat(project_fd).st_dev:
            raise TransactionError(f"write destination is on a different filesystem: {path}")
        require_child_spelling(fd, path.name)
        flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW
        with os.fdopen(os.open(path.name, flags, mode=0o600, dir_fd=fd), "wb") as stream:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
            return os.fstat(stream.fileno())


def verify_initial_writes(project_fd, writes, identities):
    for path, expected in writes.items():
        with open_directories(project_fd, path.parent.parts, identities=identities) as fd:
            require_child_spelling(fd, path.name)
            flags = os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK
            with os.fdopen(os.open(path.name, flags, dir_fd=fd), "rb") as stream:
                opened = os.fstat(stream.fileno())
                if not stat.S_ISREG(opened.st_mode) or stream.read() != expected:
                    raise TransactionError(f"initial write could not be verified: {path}")
                if not os.path.samestat(opened, os.stat(path.name, dir_fd=fd, follow_symlinks=False)):
                    raise TransactionError(f"file changed during initial save: {path}")


def create_project(vault, destination, plan):
    folder = local_path(vault, destination.as_posix())
    if folder.exists():
        raise TransactionError(f"project destination already exists: {folder}")
    writes = read_writes(folder, plan["writes"])
    entry = local_path(folder, plan["entry"])
    if entry == local_path(folder, plan["round"]):
        raise TransactionError("entry and completed round must be different files")
    valid_history(folder, plan["entry"], plan["round"], writes, creating=True)
    check_targets(folder, plan["targets"], writes)
    relative_writes = {path.relative_to(folder): data for path, (_, data) in writes.items()}
    entry = entry.relative_to(folder)
    entry_content = relative_writes.pop(entry)
    root_fd = os.open(vault.anchor, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
    try:
        vault_ids = {}
        vault_parts = vault.parts[1:]
        with open_directories(root_fd, vault_parts, identities=vault_ids) as vault_fd:
            save_initial_project(root_fd, vault_fd, vault_parts, vault_ids, destination,
                                 relative_writes, entry, entry_content)
    finally:
        os.close(root_fd)
    return [path.as_posix() for path in (*relative_writes, entry)]


def save_initial_project(root_fd, vault_fd, vault_parts, vault_ids, destination,
                         writes, entry, entry_content):
    project_ids = {}

    def verify_project_location():
        with open_directories(root_fd, vault_parts, identities=vault_ids) as current_vault:
            with open_directories(current_vault, destination.parts, identities=project_ids):
                pass

    try:
        with open_directories(vault_fd, destination.parts, create=True, exclusive=True,
                              identities=project_ids) as project_fd:
            lock_folder(project_fd)
            evidence_ids = {}
            pending = Path(FIRST_ROUND_PENDING)
            marker = write_initial_file(project_fd, pending, b"", identities=evidence_ids)
            for path, data in writes.items():
                write_initial_file(project_fd, path, data, identities=evidence_ids)
            verify_initial_writes(project_fd, writes, evidence_ids)
            verify_project_location()
            write_initial_file(project_fd, entry, entry_content, identities=evidence_ids)
            verify_initial_writes(project_fd, writes | {entry: entry_content}, evidence_ids)
            verify_project_location()
            current_marker = os.stat(pending, dir_fd=project_fd, follow_symlinks=False)
            if not os.path.samestat(marker, current_marker):
                raise TransactionError("pending marker changed during initial save")
            os.unlink(pending, dir_fd=project_fd)
    except FileExistsError as error:
        raise TransactionError(f"project destination or file already exists: {destination}") from error


def lock_folder(fd):
    try:
        fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError as error:
        raise TransactionError("research folder is busy") from error


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("inspect", "apply", "create"))
    parser.add_argument("vault", type=Path)
    parser.add_argument("folder", type=Path)
    parser.add_argument("--read", action="append", default=[], metavar="RELATIVE_FILE")
    args = parser.parse_args()
    if args.action != "inspect" and args.read:
        parser.error("--read is only available with inspect")
    try:
        if fcntl is None:
            raise TransactionError("directory locking is unavailable")
        vault = args.vault.resolve(strict=True)
        if args.action == "create":
            destination = args.folder
            if destination.is_absolute():
                supplied_vault = args.vault.absolute()
                if destination.is_relative_to(supplied_vault):
                    destination = destination.relative_to(supplied_vault)
                elif destination.is_relative_to(vault):
                    destination = destination.relative_to(vault)
                else:
                    raise TransactionError("research folder must be inside the selected vault")
            changed = create_project(vault, destination, json.load(sys.stdin))
            print(json.dumps({"changed": changed}))
            return 0
        folder = (vault / args.folder).resolve(strict=True)
        if folder == vault or not folder.is_relative_to(vault) or not folder.is_dir():
            raise TransactionError("research folder must be inside the selected vault")
        fd = os.open(folder, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
        try:
            lock_folder(fd)
            pending = folder / FIRST_ROUND_PENDING
            require_spelling(pending)
            if pending.exists() or pending.is_symlink():
                raise TransactionError(f"incomplete first round; preserved for inspection: {folder}")
            if args.action == "inspect":
                read_paths = {name: local_path(folder, name) for name in args.read}
                clear_staging(folder)
                recovery = recover(folder)
                entries = snapshot_entries(folder)
                files = {}
                for name, path in read_paths.items():
                    data = file_content(path)
                    require_snapshot_content(entries, path.relative_to(folder).as_posix(), data)
                    files[name] = encode(data)
                print(json.dumps({
                    "recovery": recovery,
                    "snapshot": state_digest(entries),
                    "paths": sorted(entries),
                    "files": files,
                }))
            else:
                plan = json.load(sys.stdin)
                clear_staging(folder)
                changed = apply(folder, plan)
                print(json.dumps({"changed": changed}))
        finally:
            os.close(fd)
    except (TransactionError, OSError, KeyError, TypeError, ValueError) as error:
        print(f"research transaction: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
