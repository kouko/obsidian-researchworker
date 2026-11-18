"""Local SEC operator contact, separate from research data."""

from contextlib import contextmanager
import json
import os
from pathlib import Path
import re
import select
import signal
import stat
import time
from secrets import token_hex
import unicodedata

MAX_PROFILE = 8192
TERMINAL_TIMEOUT = 60
INPUT_UNAVAILABLE = 'SEC_CONTACT_INPUT_UNAVAILABLE: supply one JSON line through private stdin'
PROFILE = '~/.config/obsidian-finance/sec-contact.json'
INVALID = 'SEC_CONTACT_INVALID: supply a valid operator name and contact email'
UNUSABLE = f'SEC_CONTACT_UNUSABLE: repair the private profile at {PROFILE}'
SAVE_FAILED = f'SEC_CONTACT_SAVE_FAILED: allow writing the private profile at {PROFILE}'
LOCAL_PART = r"[A-Za-z0-9!#$%&'*+/=?^_`{|}~-]+"
DOMAIN_LABEL = r'[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?'


def validate(value):
    if not isinstance(value, dict) or value.keys() != {'name', 'email'}:
        raise ValueError(INVALID)
    if any(not isinstance(field, str) or any(
            unicodedata.category(char) in ('Cc', 'Cs', 'Zl', 'Zp') for char in field)
            for field in value.values()):
        raise ValueError(INVALID)
    name = value['name'].strip()
    email = value['email'].strip()
    if (not name or len(email) > 254 or len(email.partition('@')[0]) > 64
            or not re.fullmatch(rf'{LOCAL_PART}(?:\.{LOCAL_PART})*@{DOMAIN_LABEL}(?:\.{DOMAIN_LABEL})+', email)
            or len(f'{name} {email}'.encode('utf-8')) > 1024):
        raise ValueError(INVALID)
    return {'name': name, 'email': email}


def parse(payload):
    if len(payload) > MAX_PROFILE:
        raise ValueError(INVALID)
    try:
        return validate(json.loads(payload))
    except (ValueError, RecursionError):
        raise ValueError(INVALID) from None


def read_terminal(stream):
    """Read one bounded line after confirming the terminal cannot echo it."""
    try:
        import termios
    except ImportError:
        raise ValueError(INPUT_UNAVAILABLE) from None
    try:
        if stream is None or not stream.isatty():
            raise OSError()
        fd = stream.fileno()
        original = termios.tcgetattr(fd)
        quiet = original[:]
        quiet[6] = original[6][:]
        quiet[0] &= ~(termios.IXON | termios.ISTRIP | termios.INLCR | termios.IGNCR)
        quiet[0] |= termios.ICRNL
        echo = termios.ECHO | termios.ECHONL
        quiet[3] &= ~(echo | termios.ICANON | termios.IEXTEN | termios.ISIG)
        quiet[6][termios.VMIN] = 1
        quiet[6][termios.VTIME] = 0
    except (OSError, termios.error, ValueError):
        raise ValueError(INPUT_UNAVAILABLE) from None

    previous_handlers = {}
    cancelled = waiting = False

    def cancel(signum, frame):
        nonlocal cancelled
        cancelled = True
        if waiting:
            raise InterruptedError()

    try:
        for signum in (signal.SIGINT, signal.SIGTERM, signal.SIGHUP):
            previous_handlers[signum] = signal.signal(signum, cancel)
        try:
            termios.tcsetattr(fd, termios.TCSAFLUSH, quiet)
            if termios.tcgetattr(fd)[3] & (echo | termios.ICANON):
                raise OSError()
            waiting = True
            if cancelled:
                raise InterruptedError()
            print('READY_FOR_SEPARATE_INPUT', flush=True)
            return _read_terminal_line(fd)
        finally:
            waiting = False
            termios.tcsetattr(fd, termios.TCSAFLUSH, original)
    except (OSError, termios.error, KeyboardInterrupt):
        raise ValueError(INPUT_UNAVAILABLE) from None
    finally:
        for signum, handler in previous_handlers.items():
            signal.signal(signum, handler)


def _read_terminal_line(fd):
    deadline = time.monotonic() + TERMINAL_TIMEOUT
    payload = bytearray()
    while True:
        remaining = deadline - time.monotonic()
        if remaining <= 0 or not select.select([fd], [], [], remaining)[0]:
            raise OSError()
        chunk = os.read(fd, 1024)
        if not chunk or any(cancel in chunk for cancel in (b'\x03', b'\x04', b'\x1a')):
            raise OSError()
        line, newline, trailing = chunk.partition(b'\n')
        if payload is not None:
            if len(payload) + len(line) <= MAX_PROFILE:
                payload.extend(line)
            else:
                # Discard this frame through its newline with echo still off.
                payload = None
        if newline:
            if payload is None or trailing:
                raise ValueError(INVALID)
            return bytes(payload)


@contextmanager
def _profile_directory(path):
    directory = os.open(path.parent, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
    try:
        yield directory
    finally:
        os.close(directory)


def load():
    try:
        path = Path(PROFILE).expanduser()
        with _profile_directory(path) as directory:
            flags = os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK
            with os.fdopen(os.open(path.name, flags, dir_fd=directory), 'rb') as handle:
                info = os.fstat(handle.fileno())
                if (not stat.S_ISREG(info.st_mode) or info.st_uid != os.geteuid()
                        or stat.S_IMODE(info.st_mode) != 0o600):
                    raise ValueError(UNUSABLE)
                return parse(handle.read(MAX_PROFILE + 1))
    except FileNotFoundError:
        raise ValueError('SEC_CONTACT_REQUIRED: set up a local SEC contact') from None
    except (ValueError, OSError, RuntimeError):
        raise ValueError(UNUSABLE) from None


def save(contact):
    contact = validate(contact)
    try:
        path = Path(PROFILE).expanduser()
        path.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
        with _profile_directory(path) as directory:
            temporary = '.sec-contact-' + token_hex(16)
            flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW
            descriptor = os.open(temporary, flags, 0o600, dir_fd=directory)
            try:
                with os.fdopen(descriptor, 'w', encoding='utf-8') as handle:
                    os.fchmod(handle.fileno(), 0o600)
                    json.dump(contact, handle, ensure_ascii=False)
                    handle.write('\n')
                    handle.flush()
                    os.fsync(handle.fileno())
                os.replace(temporary, path.name, src_dir_fd=directory, dst_dir_fd=directory)
            finally:
                try:
                    os.unlink(temporary, dir_fd=directory)
                except OSError:
                    pass
    except (OSError, RuntimeError):
        raise ValueError(SAVE_FAILED) from None
