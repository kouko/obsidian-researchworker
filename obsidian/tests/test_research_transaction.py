"""Exercise the resume transaction against disposable research folders."""
import base64
import fcntl
import json
import subprocess
import sys
from pathlib import Path

import pytest


HELPER = (
    Path(__file__).resolve().parents[1]
    / "skills/obsidian-research-resume/scripts/research_transaction.py"
)
JOURNAL = ".resume-recovery.json"


@pytest.fixture
def folder(tmp_path):
    root = tmp_path / "topic"
    root.mkdir()
    (root / "index.md").write_text("See [prior](prior.md).")
    (root / "prior.md").write_text("Previously completed")
    (root / "judgment.md").write_text("seven")
    (root / "dependent.md").write_text("seven")
    return root


def invoke(folder, action, plan=None, *, options=()):
    return subprocess.run(
        [sys.executable, str(HELPER), action, str(folder.parent), str(folder), *options],
        input=json.dumps(plan),
        capture_output=True,
        text=True,
    )


def contents(folder):
    return {
        path.relative_to(folder).as_posix(): path.read_bytes()
        for path in folder.rglob("*")
        if path.is_file()
    }


def prepare(folder, **writes):
    inspection = invoke(folder, "inspect")
    assert inspection.returncode == 0, inspection.stderr
    return {
        "snapshot": json.loads(inspection.stdout)["snapshot"],
        "entry": "index.md",
        "round": "prior.md",
        "writes": [
            {"path": path, "content": base64.b64encode(value.encode()).decode()}
            for path, value in writes.items()
        ],
        "targets": ["prior.md"],
    }


def test_busy_transaction_preserves_files(folder):
    plan = prepare(folder, **{"judgment.md": "six"})
    before = contents(folder)
    holder = subprocess.Popen(
        [sys.executable, "-c",
         "import fcntl, os, sys; fd = os.open(sys.argv[1], os.O_RDONLY); "
         "fcntl.flock(fd, fcntl.LOCK_EX); print('ready', flush=True); sys.stdin.read()",
         str(folder)],
        stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True,
    )
    try:
        assert holder.stdout.readline() == "ready\n"
        for action in ("inspect", "apply"):
            result = invoke(folder, action, plan)
            assert result.returncode != 0 and "busy" in result.stderr
        assert contents(folder) == before
    finally:
        holder.communicate(timeout=5)


@pytest.fixture
def pause_after_judgment(folder):
    process = None

    def pause():
        nonlocal process
        plan = prepare(folder, **{"judgment.md": "six", "topics/dependent.md": "six"})
        interrupt = (
            "import signal, sys; from pathlib import Path; "
            "sys.path.insert(0, str(Path(sys.argv.pop(1)).parent)); "
            "import research_transaction as transaction\n"
            "write = transaction.replace_file\n"
            "def pause_after_judgment(path, data):\n"
            "    write(path, data)\n"
            "    if path.name == 'judgment.md':\n"
            "        print('paused', flush=True)\n"
            "        signal.pause()\n"
            "transaction.replace_file = pause_after_judgment\n"
            "raise SystemExit(transaction.main())"
        )
        process = subprocess.Popen(
            [sys.executable, "-c", interrupt, str(HELPER), "apply",
             str(folder.parent), str(folder)],
            stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True,
        )
        process.stdin.write(json.dumps(plan))
        process.stdin.close()
        assert process.stdout.readline() == "paused\n"
        return process, plan

    yield pause
    if process is not None and process.poll() is None:
        process.kill()
        process.wait(timeout=5)


def test_interrupted_transaction_recovers(folder, pause_after_judgment):
    writer, plan = pause_after_judgment()
    assert (folder / JOURNAL).is_file()
    assert (folder / "judgment.md").read_text() == "six"
    assert not (folder / "topics/dependent.md").exists()
    partial = contents(folder)
    for action in ("inspect", "apply"):
        result = invoke(folder, action, plan)
        assert result.returncode != 0 and "busy" in result.stderr
    assert contents(folder) == partial
    writer.kill()
    writer.wait(timeout=5)
    result = invoke(folder, "inspect", options=("--read", "../outside.md"))
    assert result.returncode != 0 and "unsafe" in result.stderr
    assert contents(folder) == partial
    result = invoke(folder, "inspect", options=("--read", "topics/dependent.md"))
    assert result.returncode == 0, result.stderr
    inspected = json.loads(result.stdout)
    assert inspected["recovery"] == "completed"
    assert base64.b64decode(inspected["files"]["topics/dependent.md"]) == b"six"
    assert (folder / "topics/dependent.md").read_text() == "six"
    assert not (folder / JOURNAL).exists()


def test_unplanned_edit_blocks_recovery(folder, pause_after_judgment):
    writer, _ = pause_after_judgment()
    writer.kill()
    writer.wait(timeout=5)
    (folder / "prior.md").write_text("external revision")
    partial = contents(folder)
    result = invoke(folder, "inspect")
    assert result.returncode != 0 and "unexpected folder changes" in result.stderr
    assert contents(folder) == partial


def test_stale_snapshot_preserves_files(folder):
    plan = prepare(folder, **{"judgment.md": "six"})
    (folder / "dependent.md").write_text("external revision")
    before = contents(folder)
    result = invoke(folder, "apply", plan)
    assert result.returncode != 0 and "stale" in result.stderr
    assert contents(folder) == before


@pytest.mark.parametrize("destination", ["../outside.md", "alias/outside.md"])
def test_rejects_escaped_paths(folder, destination):
    outside = folder.parent / "outside.md"
    outside.write_text("outside")
    (folder / "alias").symlink_to(folder.parent, target_is_directory=True)
    plan = prepare(folder, **{destination: "changed"})
    before = contents(folder)
    assert invoke(folder, "apply", plan).returncode != 0
    assert contents(folder) == before
    assert outside.read_text() == "outside"


def test_replay_does_not_write(folder):
    plan = prepare(folder, **{"judgment.md": "six"})
    result = invoke(folder, "apply", plan)
    assert result.returncode == 0, result.stderr
    before = contents(folder)
    before_mtime = (folder / "judgment.md").stat().st_mtime_ns
    replay = prepare(folder, **{"judgment.md": "six"})
    result = invoke(folder, "apply", replay)
    assert result.returncode == 0, result.stderr
    assert json.loads(result.stdout)["changed"] == []
    assert contents(folder) == before
    assert (folder / "judgment.md").stat().st_mtime_ns == before_mtime
