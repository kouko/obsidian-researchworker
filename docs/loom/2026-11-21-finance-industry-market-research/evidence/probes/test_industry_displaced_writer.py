# concern: A late write through an editor's open descriptor can disappear during cleanup.
import os
from pathlib import Path
import sys

FINANCE_TESTS = Path(__file__).resolve().parents[5] / "obsidian-finance" / "tests"
sys.path.insert(0, str(FINANCE_TESTS))
from test_industry_update import update


def test_publication_retains_editor_writes_to_displaced_open_inode(tmp_path, monkeypatch):
    note = tmp_path / "note.md"
    note.write_bytes(b"old research")
    expected = update.inspect(tmp_path, ["note.md"])
    unlink = update.os.unlink
    external = b"user edit through a descriptor opened before the swap"

    with note.open("r+b", buffering=0) as editor:
        def save_external_edit():
            editor.write(external)
            os.fsync(editor.fileno())

        def write_when_barrier_clears(path, *args, **kwargs):
            if path == ".industry-update.json":
                save_external_edit()
            return unlink(path, *args, **kwargs)

        monkeypatch.setattr(update.os, "unlink", write_when_barrier_clears)
        try:
            update.apply(tmp_path, expected, {"note.md": b"new research"})
        except update.UpdateConflict:
            pass
        if editor.tell() == 0:
            save_external_edit()

    assert any(external == path.read_bytes() for path in tmp_path.rglob("*") if path.is_file())
