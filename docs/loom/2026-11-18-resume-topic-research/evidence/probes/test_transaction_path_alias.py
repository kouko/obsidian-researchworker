# concern: Filesystem path aliases can overwrite the same note twice and strand recovery.
from pathlib import Path
import runpy

import pytest


ROOT = Path(__file__).resolve().parents[5]
helpers = runpy.run_path(str(ROOT / "obsidian/tests/test_research_transaction.py"))
invoke = helpers["invoke"]
prepare = helpers["prepare"]
contents = helpers["contents"]


@pytest.mark.parametrize("existing", [True, False])
def test_transaction_aliases_preserve_files(tmp_path, existing):
    """Preflight overlapping destinations using the actual filesystem semantics."""
    folder = tmp_path / "topic"
    folder.mkdir()
    (folder / "index.md").write_text("See prior.md.")
    (folder / "prior.md").write_text("Completed round.")
    (folder / "probe").touch()
    aliases = (folder / "PROBE").exists()
    (folder / "probe").unlink()
    if existing:
        (folder / "judgment.md").write_text("seven")

    plan = prepare(folder, **{"judgment.md": "six", "JUDGMENT.md": "five"})
    before = contents(folder)
    result = invoke(folder, "apply", plan)

    if result.returncode != 0:
        assert contents(folder) == before
    else:
        assert not aliases, "the transaction accepted two spellings of one destination"
        assert (folder / "judgment.md").read_text() == "six"
        assert (folder / "JUDGMENT.md").read_text() == "five"
