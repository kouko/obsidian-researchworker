"""Exercise the resume transaction against disposable research folders."""
import base64
import fcntl
import json
import signal
import subprocess
import sys
from pathlib import Path

import pytest


HELPER = (
    Path(__file__).resolve().parents[1]
    / "skills/obsidian-research-project/scripts/research_transaction.py"
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


def invoke(folder, action, plan=None, *, options=(), vault=None):
    return subprocess.run(
        [sys.executable, str(HELPER), action, str(vault or folder.parent), str(folder), *options],
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


def first_round():
    return {
        "entry": "index.md",
        "round": "history/2026-11-19-R01.md",
        "writes": [
            {"path": path, "content": base64.b64encode(note.encode()).decode()}
            for path, note in {
                "index.md": "See [first round](history/2026-11-19-R01.md).",
                "history/2026-11-19-R01.md": "See [evidence](../sources/S1.md).",
                "sources/S1.md": "First source.",
            }.items()
        ],
        "targets": ["history/2026-11-19-R01.md", "sources/S1.md"],
    }


def test_create_first_round_then_resume(tmp_path):
    topic = tmp_path / "research" / "topic"
    plan = first_round()
    result = invoke(topic, "create", plan, vault=tmp_path)
    assert result.returncode == 0, result.stderr
    assert json.loads(result.stdout)["changed"][-1] == "index.md"
    assert set(contents(topic)) == {write["path"] for write in plan["writes"]}
    assert list(topic.parent.iterdir()) == [topic]

    update = prepare(topic, **{"index.md": "Updated"})
    update["round"] = plan["round"]
    update["targets"] = plan["targets"]
    assert invoke(topic, "apply", update).returncode == 0
    assert (topic / "index.md").read_text() == "Updated"


@pytest.mark.parametrize(
    ("obstacle", "diagnostic"),
    [
        ("existing", "already exists"),
        ("symlink", "symlink"),
        ("traversal", "unsafe relative path"),
        ("missing-evidence", "required local target is missing"),
    ],
)
def test_create_rejects_unsafe_target_without_changes(tmp_path, obstacle, diagnostic):
    topic = tmp_path / "research" / "topic"
    plan = first_round()
    if obstacle == "existing":
        topic.mkdir(parents=True)
        (topic / "personal.md").write_text("Keep this.")
    elif obstacle == "symlink":
        (tmp_path / "research").symlink_to(tmp_path, target_is_directory=True)
    elif obstacle == "traversal":
        topic = tmp_path / "research" / ".." / "topic"
    else:
        plan["writes"].pop()
    before = sorted(tmp_path.rglob("*"))

    result = invoke(topic, "create", plan, vault=tmp_path)

    assert result.returncode != 0 and diagnostic in result.stderr
    assert sorted(tmp_path.rglob("*")) == before
    if obstacle == "existing":
        assert (topic / "personal.md").read_text() == "Keep this."


def test_interrupted_first_round_is_preserved_but_cannot_resume(tmp_path):
    topic = tmp_path / "topic"
    script = (
        "import os, sys; from pathlib import Path; "
        "sys.path.insert(0, str(Path(sys.argv.pop(1)).parent)); "
        "import research_transaction as transaction\n"
        "original = transaction.write_initial_file\n"
        "def stop_before_entry(project_fd, path, *args, **kwargs):\n"
        "    if path.name == 'index.md':\n"
        "        os._exit(7)\n"
        "    original(project_fd, path, *args, **kwargs)\n"
        "transaction.write_initial_file = stop_before_entry\n"
        "raise SystemExit(transaction.main())"
    )
    result = subprocess.run(
        [sys.executable, "-c", script, str(HELPER), "create", str(tmp_path), str(topic)],
        input=json.dumps(first_round()), capture_output=True, text=True, check=False,
    )
    assert result.returncode == 7, result.stderr
    assert not topic.exists()
    stage, = tmp_path.glob(".research-first-round-*")
    before = contents(stage)
    assert "sources/S1.md" in before
    assert "index.md" not in before
    inspection = invoke(stage, "inspect")
    assert inspection.returncode != 0 and "incomplete first round" in inspection.stderr
    assert contents(stage) == before


def test_create_preserves_directory_that_appears_before_publication(tmp_path):
    topic = tmp_path / "topic"
    script = (
        "import os, sys; from pathlib import Path; "
        "sys.path.insert(0, str(Path(sys.argv.pop(1)).parent)); "
        "import research_transaction as transaction\n"
        "original = transaction.write_initial_file\n"
        "def add_destination(project_fd, path, *args, **kwargs):\n"
        "    result = original(project_fd, path, *args, **kwargs)\n"
        "    if path.name == 'index.md':\n"
        "        destination = Path(sys.argv[-1])\n"
        "        destination.mkdir()\n"
        "        print(destination.stat().st_ino, flush=True)\n"
        "    return result\n"
        "transaction.write_initial_file = add_destination\n"
        "raise SystemExit(transaction.main())"
    )
    result = subprocess.run(
        [sys.executable, "-c", script, str(HELPER), "create", str(tmp_path), str(topic)],
        input=json.dumps(first_round()), capture_output=True, text=True, check=False,
    )
    assert result.returncode == 1 and "already exists" in result.stderr
    assert topic.stat().st_ino == int(result.stdout)
    assert not list(topic.iterdir())
    stage, = tmp_path.glob(".research-first-round-*")
    assert (stage / "index.md").is_file()
    assert (stage / ".research-first-round-pending").is_file()


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
            "write = transaction.write_atomically\n"
            "def pause_after_judgment(path, data, **kwargs):\n"
            "    write(path, data, **kwargs)\n"
            "    if path.name == 'judgment.md':\n"
            "        signal.pthread_sigmask(signal.SIG_BLOCK, {signal.SIGUSR1})\n"
            "        print('paused', flush=True)\n"
            "        signal.sigwait({signal.SIGUSR1})\n"
            "transaction.write_atomically = pause_after_judgment\n"
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



def test_external_edit_between_destinations_is_preserved(folder, pause_after_judgment):
    writer, _ = pause_after_judgment()
    dependent = folder / "topics/dependent.md"
    dependent.parent.mkdir()
    dependent.write_text("ordinary editor")
    writer.send_signal(signal.SIGUSR1)
    assert writer.wait(timeout=5) != 0
    assert dependent.read_text() == "ordinary editor"
    assert (folder / JOURNAL).is_file()


@pytest.mark.parametrize("edit_after_staging", [False, True])
def test_staged_write_checks_destination_after_pause(folder, edit_after_staging):
    plan = prepare(folder, **{"judgment.md": "six"})
    script = (
        "import os, signal, sys; from pathlib import Path; "
        "sys.path.insert(0, str(Path(sys.argv.pop(1)).parent)); "
        "import research_transaction as transaction\n"
        "sync = os.fsync\n"
        "count = 0\n"
        "def interrupt(fd):\n"
        "    global count\n"
        "    sync(fd)\n"
        "    count += 1\n"
        "    if count == 2:\n"
        "        signal.pthread_sigmask(signal.SIG_BLOCK, {signal.SIGUSR1})\n"
        "        print('staged', flush=True)\n"
        "        signal.sigwait({signal.SIGUSR1})\n"
        "os.fsync = interrupt\n"
        "raise SystemExit(transaction.main())"
    )
    writer = subprocess.Popen(
        [sys.executable, "-c", script, str(HELPER), "apply",
         str(folder.parent), str(folder)],
        stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True,
    )
    try:
        writer.stdin.write(json.dumps(plan))
        writer.stdin.close()
        assert writer.stdout.readline() == "staged\n"
        assert (folder / JOURNAL).is_file()
        judgment = folder / "judgment.md"
        assert judgment.read_text() == "seven"
        if edit_after_staging:
            judgment.write_text("ordinary editor")
            writer.send_signal(signal.SIGUSR1)
            assert writer.wait(timeout=5) != 0
            assert judgment.read_text() == "ordinary editor"
            assert (folder / JOURNAL).is_file()
            assert not (folder / ".resume-staging").exists()
            return
        writer.kill()
        writer.wait(timeout=5)
        result = invoke(folder, "inspect")
        assert result.returncode == 0, result.stderr
        assert json.loads(result.stdout)["recovery"] == "completed"
        assert (folder / "judgment.md").read_text() == "six"
        assert sorted(path.name for path in folder.iterdir()) == [
            "dependent.md", "index.md", "judgment.md", "prior.md",
        ]
    finally:
        if writer.poll() is None:
            writer.kill()
            writer.wait(timeout=5)



@pytest.mark.parametrize("action", ["inspect", "apply"])
def test_unmarked_empty_staging_is_not_removed(tmp_path, action):
    topic = tmp_path / "topic"
    stage = topic / ".resume-staging"
    stage.mkdir(parents=True, mode=0o700)

    result = invoke(topic, action)

    assert result.returncode != 0
    assert "unrecognized staging" in result.stderr
    assert list(topic.iterdir()) == [stage]
    assert list(stage.iterdir()) == []


def test_unrecognized_staging_files_are_not_removed(folder):
    stage = folder / ".resume-staging"
    stage.mkdir(mode=0o700)
    personal = stage / "personal.md"
    personal.write_text("user data")
    before = contents(folder)
    result = invoke(folder, "inspect")
    assert result.returncode != 0 and "unrecognized staging" in result.stderr
    assert contents(folder) == before


@pytest.mark.parametrize("destination", ["mounted/dependent.md", "mounted/new/dependent.md"])
def test_cross_device_plan_rejected_before_writes(folder, destination):
    (folder / "mounted").mkdir()
    plan = prepare(folder, **{"judgment.md": "six", destination: "six"})
    before = contents(folder)
    script = (
        "import os, sys; from pathlib import Path; "
        "sys.path.insert(0, str(Path(sys.argv.pop(1)).parent)); "
        "import research_transaction as transaction\n"
        "original = Path.stat\n"
        "def mounted_stat(path, *args, **kwargs):\n"
        "    result = original(path, *args, **kwargs)\n"
        "    if path.name == 'mounted':\n"
        "        fields = list(result)\n"
        "        fields[2] = result.st_dev + 1\n"
        "        return os.stat_result(fields)\n"
        "    return result\n"
        "Path.stat = mounted_stat\n"
        "raise SystemExit(transaction.main())"
    )
    result = subprocess.run(
        [sys.executable, "-c", script, str(HELPER), "apply", str(folder.parent), str(folder)],
        input=json.dumps(plan), capture_output=True, text=True, check=False,
    )
    assert result.returncode != 0 and "different filesystem" in result.stderr
    assert contents(folder) == before
    assert not (folder / ".resume-staging").exists()
@pytest.mark.parametrize(
    ("action", "changed"),
    [
        ("apply", "judgment.md"),
        ("apply", "new.md"),
        ("apply", "dependent.md"),
        ("inspect", "judgment.md"),
    ],
)
def test_edit_after_snapshot_is_not_accepted(folder, action, changed):
    plan = prepare(folder, **{"judgment.md": "six", "new.md": "new evidence"})
    expected = contents(folder)
    expected[changed] = b"manual edit"
    script = (
        "import sys; from pathlib import Path; "
        "sys.path.insert(0, str(Path(sys.argv.pop(1)).parent)); "
        "changed = sys.argv.pop(1); "
        "import research_transaction as transaction\n"
        "original = transaction.snapshot_entries\n"
        "def snapshot_then_edit(folder):\n"
        "    entries = original(folder)\n"
        "    transaction.snapshot_entries = original\n"
        "    (folder / changed).write_bytes(b'manual edit')\n"
        "    return entries\n"
        "transaction.snapshot_entries = snapshot_then_edit\n"
        "raise SystemExit(transaction.main())"
    )
    options = ("--read", changed) if action == "inspect" else ()
    result = subprocess.run(
        [sys.executable, "-c", script, str(HELPER), changed, action,
         str(folder.parent), str(folder), *options],
        input=json.dumps(plan), capture_output=True, text=True, check=False,
    )
    assert result.returncode == 1
    assert not result.stdout
    assert "stale snapshot" in result.stderr
    assert contents(folder) == expected
    assert not (folder / JOURNAL).exists()


def test_new_file_does_not_overwrite_late_creation(folder):
    plan = prepare(folder, **{"new.md": "planned"})
    expected = contents(folder)
    expected["new.md"] = b"manual edit"
    script = (
        "import sys; from pathlib import Path; "
        "sys.path.insert(0, str(Path(sys.argv.pop(1)).parent)); "
        "import research_transaction as transaction\n"
        "original = transaction.file_content\n"
        "def create_after_check(path):\n"
        "    data = original(path)\n"
        "    if path.name == 'new.md' and (path.parent / transaction.STAGING).exists():\n"
        "        path.write_bytes(b'manual edit')\n"
        "    return data\n"
        "transaction.file_content = create_after_check\n"
        "raise SystemExit(transaction.main())"
    )
    result = subprocess.run(
        [sys.executable, "-c", script, str(HELPER), "apply",
         str(folder.parent), str(folder)],
        input=json.dumps(plan), capture_output=True, text=True, check=False,
    )
    assert result.returncode == 1
    assert (folder / JOURNAL).is_file()
    assert {k: v for k, v in contents(folder).items() if k != JOURNAL} == expected
