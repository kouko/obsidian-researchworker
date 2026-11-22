"""Recoverable, no-clobber publication of a batch of vault notes."""

import base64
from contextlib import ExitStack, contextmanager
import ctypes
import errno
import fcntl
import json
import os
from pathlib import Path
import re
import stat
import sys
import uuid


_PENDING = ".industry-update.json"
_STAGE_PREFIX = ".industry-stage-"
_DIR_FLAGS = os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW
_UPDATE_NAMES = {
    "industry": (_PENDING, _STAGE_PREFIX),
    "equity": (".equity-update.json", ".equity-stage-"),
}


class UpdateConflict(ValueError):
    """The update cannot proceed without risking existing user data."""


def _parts(path):
    if not isinstance(path, str):
        raise UpdateConflict("Note path must be a vault-relative string")
    parts = path.split("/")
    if (
        any(not part or part in (".", "..") or part.startswith(".") for part in parts)
        or "\\" in path or "\x00" in path or not parts[-1].endswith(".md")
    ):
        raise UpdateConflict(f"Invalid vault-relative note path: {path}")
    return parts


@contextmanager
def _locked_vault(vault, *, write=False):
    with _directory(Path(vault)) as root:
        fcntl.flock(root, fcntl.LOCK_EX if write else fcntl.LOCK_SH)
        yield root


@contextmanager
def _directory(name, parent=None):
    try:
        fd = os.open(name, _DIR_FLAGS, dir_fd=parent)
    except FileNotFoundError:
        raise
    except OSError as exc:
        raise UpdateConflict(f"Cannot safely open directory: {name}") from exc
    try:
        yield fd
    finally:
        os.close(fd)


@contextmanager
def _parent(root, path, *, create=False):
    *parents, name = _parts(path)

    with ExitStack() as stack:
        device = os.fstat(root).st_dev
        current = root
        for child in parents:
            if create:
                try:
                    os.mkdir(child, dir_fd=current)
                except FileExistsError:
                    pass
            current = stack.enter_context(_directory(child, current))
            if os.fstat(current).st_dev != device:
                raise UpdateConflict(f"Note is on another filesystem: {path}")
        yield current, name


def _read(parent, name):
    try:
        fd = os.open(name, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK, dir_fd=parent)
    except FileNotFoundError:
        return None
    except OSError as exc:
        raise UpdateConflict(f"Cannot safely read: {name}") from exc
    with os.fdopen(fd, "rb") as stream:
        if not stat.S_ISREG(os.fstat(stream.fileno()).st_mode):
            raise UpdateConflict(f"Not a regular file: {name}")
        return stream.read()


def _current(root, path):
    try:
        with _parent(root, path) as (parent, name):
            return _read(parent, name)
    except FileNotFoundError:
        return None


@contextmanager
def read_barrier(vault, *, namespace="industry"):
    """Hold the cooperating reader lock while consuming published notes."""
    pending, _ = _UPDATE_NAMES[namespace]
    with _locked_vault(vault) as root:
        if _read(root, pending) is not None:
            raise UpdateConflict(f"{namespace.capitalize()} update pending; recover before reading")
        yield


def inspect(vault, paths):
    """Capture the exact expected note contents for a subsequent apply."""
    with _locked_vault(vault) as root:
        if _read(root, _PENDING) is not None:
            raise UpdateConflict("Industry update pending; recover before reading")
        return {path: _current(root, path) for path in paths}


def _exchange_function():
    libc = ctypes.CDLL(None, use_errno=True)
    if sys.platform == "darwin":
        # renameatx_np(int, const char *, int, const char *, unsigned int):
        # https://github.com/apple-oss-distributions/xnu/blob/main/bsd/sys/stdio.h
        function = getattr(libc, "renameatx_np", None)
        flags = 0x00000002  # RENAME_SWAP
    elif sys.platform.startswith("linux"):
        # https://man7.org/linux/man-pages/man2/rename.2.html
        # https://github.com/torvalds/linux/blob/master/include/uapi/linux/fs.h
        function = getattr(libc, "renameat2", None)
        flags = 2  # RENAME_EXCHANGE
    else:
        function = None
    if function is None:
        raise UpdateConflict("Atomic file exchange is unavailable")
    function.argtypes = [ctypes.c_int, ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p, ctypes.c_uint]
    function.restype = ctypes.c_int
    return function, flags


def _exchange(stage, payload, parent, name):
    _system_exchange(_exchange_function(), stage, payload, parent, name)


def _system_exchange(native, stage, payload, parent, name):
    function, flags = native
    if function(stage, os.fsencode(payload), parent, os.fsencode(name), flags):
        code = ctypes.get_errno()
        if code in (errno.ENOSYS, errno.ENOTSUP, errno.EINVAL, errno.EXDEV):
            raise UpdateConflict(f"Atomic file exchange is unavailable for {name}")
        raise OSError(code, os.strerror(code), name)


def _write_new(parent, name, data):
    fd = os.open(name, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600, dir_fd=parent)
    with os.fdopen(fd, "wb") as stream:
        stream.write(data)
        stream.flush()
        os.fsync(stream.fileno())


def _probe_exchange(native, stage):
    names = ("exchange-a", "exchange-b")
    for name in names:
        _write_new(stage, name, b"")
    try:
        _system_exchange(native, stage, names[0], stage, names[1])
    finally:
        for name in names:
            os.unlink(name, dir_fd=stage)


def _packed(data):
    return None if data is None else base64.b64encode(data).decode("ascii")


def _unpacked(data):
    if data is not None and not isinstance(data, str):
        raise ValueError("Expected encoded bytes")
    return None if data is None else base64.b64decode(data, validate=True)


def _journal(data, stage_prefix):
    try:
        record = json.loads(data)
        stage = record["stage"]
        if not re.fullmatch(re.escape(stage_prefix) + r"[a-f0-9]{32}", stage):
            raise ValueError("Invalid staging identity")
        changes = {}
        for path, before, after in record["files"]:
            _parts(path)
            previous, intended = _unpacked(before), _unpacked(after)
            if path in changes or intended is None or previous == intended:
                raise ValueError("Invalid staged change")
            changes[path] = (previous, intended)
        if not changes:
            raise ValueError("Empty journal")
        return stage, changes
    except (KeyError, TypeError, ValueError) as exc:
        raise UpdateConflict("Malformed pending note update journal") from exc


def _same_inode(left, left_name, right, right_name):
    first = os.stat(left_name, dir_fd=left, follow_symlinks=False)
    second = os.stat(right_name, dir_fd=right, follow_symlinks=False)
    return os.path.samestat(first, second)


def _update_one(root, stage, payload, path, before, after):
    with _parent(root, path, create=before is None) as (parent, name):
        current, staged = _read(parent, name), _read(stage, payload)
        if before is None:
            if staged != after:
                raise UpdateConflict(f"Creation payload was changed: {path}")
            if current is None:
                try:
                    os.link(payload, name, src_dir_fd=stage, dst_dir_fd=parent, follow_symlinks=False)
                except FileExistsError as exc:
                    raise UpdateConflict(f"Another file appeared: {path}") from exc
            elif current != after or not _same_inode(stage, payload, parent, name):
                raise UpdateConflict(f"Another file appeared: {path}")
        elif current == before and staged == after:
            # Swapping retains any late external write instead of unlinking it.
            _exchange(stage, payload, parent, name)
            if _read(stage, payload) != before:
                raise UpdateConflict(f"Unexpected displaced edit preserved in {payload}: {path}")
        elif staged != before:
            raise UpdateConflict(f"Unexpected displaced or staged content preserved in {payload}: {path}")
        if _read(parent, name) != after:
            raise UpdateConflict(f"Destination changed; prior and intended bytes retained: {path}")
        os.fsync(parent)
        os.fsync(stage)


def _finish(root, stage_name, changes, pending):
    with _directory(stage_name, root) as stage:
        for index, (path, (before, after)) in enumerate(changes.items()):
            _update_one(root, stage, f"{index}.note", path, before, after)
        for index, (path, (before, after)) in enumerate(changes.items()):
            if _current(root, path) != after or _read(stage, f"{index}.note") != (
                after if before is None else before
            ):
                raise UpdateConflict(f"Notes changed before batch publication: {path}")
        os.unlink(pending, dir_fd=root)
        os.fsync(root)
        # An external editor may still hold the displaced inode open. Leave
        # replacements linked so later writes to that inode remain recoverable.
        for index, (before, _) in enumerate(changes.values()):
            if before is None:
                os.unlink(f"{index}.note", dir_fd=stage)
        os.unlink("journal", dir_fd=stage)
        os.fsync(stage)
    if all(before is None for before, _ in changes.values()):
        os.rmdir(stage_name, dir_fd=root)


def apply(vault, expected, intended, *, check_scope=None, namespace="industry"):
    """Check scope and exact bytes under lock before starting a journal."""
    if set(expected) != set(intended):
        raise UpdateConflict("Every write requires an expected value")
    pending, stage_prefix = _UPDATE_NAMES[namespace]
    with _locked_vault(vault, write=True) as root:
        if _read(root, pending) is not None:
            raise UpdateConflict(f"{namespace.capitalize()} update pending; recover before applying")
        if check_scope is not None:
            check_scope()
        changes = {}
        for path, after in intended.items():
            before = expected[path]
            if not isinstance(after, bytes) or (before is not None and not isinstance(before, bytes)):
                raise UpdateConflict("Expected and intended note contents must be bytes")
            if _current(root, path) != before:
                raise UpdateConflict(f"Note was changed before publication: {path}")
            if before != after:
                changes[path] = before, after
        if not changes:
            return
        native = (
            _exchange_function()
            if any(before is not None for before, _ in changes.values())
            else None
        )
        stage_name = stage_prefix + uuid.uuid4().hex
        os.mkdir(stage_name, 0o700, dir_fd=root)
        with _directory(stage_name, root) as stage:
            if native is not None:
                try:
                    _probe_exchange(native, stage)
                except UpdateConflict:
                    os.rmdir(stage_name, dir_fd=root)
                    raise
            record = {"stage": stage_name, "files": []}
            displaced = {}
            for index, (path, (before, after)) in enumerate(changes.items()):
                payload = f"{index}.note"
                _write_new(stage, payload, after)
                record["files"].append([path, _packed(before), _packed(after)])
                if before is not None:
                    displaced[payload] = path
            if displaced:
                _write_new(stage, "displaced.json", json.dumps(displaced).encode())
            _write_new(stage, "journal", json.dumps(record).encode())
            os.fsync(stage)
            os.link("journal", pending, src_dir_fd=stage, dst_dir_fd=root, follow_symlinks=False)
            os.fsync(root)
        _finish(root, stage_name, changes, pending)


def recover(vault, *, namespace="industry", check_scope=None):
    """Finish a recognized interrupted batch; retain both sides on conflict."""
    pending, stage_prefix = _UPDATE_NAMES[namespace]
    with _locked_vault(vault, write=True) as root:
        data = _read(root, pending)
        if data is None:
            return False
        stage, changes = _journal(data, stage_prefix)
        with _directory(stage, root) as directory:
            if not _same_inode(root, pending, directory, "journal"):
                raise UpdateConflict("Unrecognized note staging journal")
        if check_scope is not None:
            check_scope(changes)
        _finish(root, stage, changes, pending)
        return True
