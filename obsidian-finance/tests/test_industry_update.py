import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import industry_update as update


def test_same_path_update_preserves_preexisting_text(tmp_path):
    path = tmp_path / "quarter.md"
    path.write_bytes(b"user text\nold")
    original = update.inspect(tmp_path, ["quarter.md", "sub/notes.md"])
    update.apply(tmp_path, original, {
        "quarter.md": b"user text\nnew", "sub/notes.md": b"research",
    })
    assert path.read_bytes() == b"user text\nnew"
    assert (tmp_path / "sub/notes.md").read_bytes() == b"research"
    assert update.recover(tmp_path) is False


def test_post_swap_interruption_recovers_batch_and_blocks_readers(tmp_path, monkeypatch):
    for name in ("a.md", "b.md"):
        (tmp_path / name).write_bytes(b"before")
    expected = update.inspect(tmp_path, ["a.md", "b.md"])
    exchange = update._exchange

    def interrupt(*args):
        exchange(*args)
        raise RuntimeError("interrupted just after swap")

    monkeypatch.setattr(update, "_exchange", interrupt)
    with pytest.raises(RuntimeError):
        update.apply(tmp_path, expected, {"a.md": b"aftera", "b.md": b"afterb"})
    with pytest.raises(update.UpdateConflict, match="pending"):
        update.inspect(tmp_path, expected)
    monkeypatch.setattr(update, "_exchange", exchange)
    assert update.recover(tmp_path) is True
    assert update.inspect(tmp_path, expected) == {"a.md": b"aftera", "b.md": b"afterb"}


def test_concurrent_edit_between_precheck_and_exchange_is_recoverable(tmp_path, monkeypatch):
    note = tmp_path / "note.md"
    note.write_bytes(b"before")
    expected = update.inspect(tmp_path, ["note.md"])
    exchange = update._exchange

    def race(*args):
        note.write_bytes(b"external editor")
        exchange(*args)

    monkeypatch.setattr(update, "_exchange", race)
    with pytest.raises(update.UpdateConflict, match="displaced"):
        update.apply(tmp_path, expected, {"note.md": b"new research"})
    assert note.read_bytes() == b"new research"
    assert any(
        saved.is_file() and saved.read_bytes() == b"external editor"
        for saved in tmp_path.glob(".industry-stage-*/*")
    )
    with pytest.raises(update.UpdateConflict, match="displaced"):
        update.recover(tmp_path)


def test_existing_file_collision_and_symlink_are_never_overwritten(tmp_path):
    note = tmp_path / "ordinary.md"
    note.write_bytes(b"user")
    with pytest.raises(update.UpdateConflict):
        update.apply(tmp_path, {"ordinary.md": None}, {"ordinary.md": b"new"})
    assert note.read_bytes() == b"user"
    (tmp_path / "elsewhere").symlink_to(tmp_path.parent, target_is_directory=True)
    with pytest.raises(update.UpdateConflict):
        update.apply(tmp_path, {"elsewhere/file.md": None}, {"elsewhere/file.md": b"new"})


def test_unsupported_exchange_fails_closed(tmp_path, monkeypatch):
    note = tmp_path / "note.md"
    note.write_bytes(b"before")

    def unsupported():
        raise update.UpdateConflict("exchange unavailable")

    monkeypatch.setattr(update, "_exchange_function", unsupported)
    with pytest.raises(update.UpdateConflict, match="unavailable"):
        update.apply(tmp_path, {"note.md": b"before"}, {"note.md": b"after"})
    assert note.read_bytes() == b"before"
    assert update.inspect(tmp_path, ["note.md"]) == {"note.md": b"before"}


def test_exchange_probe_checks_filesystem_before_any_batch_write(tmp_path, monkeypatch):
    note = tmp_path / "note.md"
    note.write_bytes(b"before")

    def unsupported(*args):
        raise update.UpdateConflict("Exchange unavailable on this filesystem")

    monkeypatch.setattr(update, "_system_exchange", unsupported)
    with pytest.raises(update.UpdateConflict, match="unavailable"):
        update.apply(
            tmp_path, {"first.md": None, "note.md": b"before"},
            {"first.md": b"new", "note.md": b"after"},
        )
    assert list(tmp_path.iterdir()) == [note]
    assert note.read_bytes() == b"before"


def test_an_ordinary_note_created_after_precheck_wins(tmp_path, monkeypatch):
    link = update.os.link
    note = tmp_path / "new.md"

    def concurrent_link(source, destination, **kwargs):
        if destination == "new.md":
            note.write_bytes(b"ordinary note")
        link(source, destination, **kwargs)

    monkeypatch.setattr(update.os, "link", concurrent_link)
    with pytest.raises(update.UpdateConflict, match="Another file appeared"):
        update.apply(tmp_path, {"new.md": None}, {"new.md": b"research"})
    assert note.read_bytes() == b"ordinary note"
    with pytest.raises(update.UpdateConflict, match="pending"):
        update.inspect(tmp_path, ["new.md"])
