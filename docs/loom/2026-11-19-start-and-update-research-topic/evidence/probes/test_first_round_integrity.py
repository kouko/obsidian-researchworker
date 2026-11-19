# concern: Evidence replaced during first-round publication is accepted as verified.
import base64
import importlib.util
from pathlib import Path

import pytest


HELPER = (
    Path(__file__).resolve().parents[5]
    / "obsidian/skills/obsidian-research-project/scripts/research_transaction.py"
)
SPEC = importlib.util.spec_from_file_location("research_transaction", HELPER)
transaction = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(transaction)


def test_create_concurrentedit_stayspending(tmp_path, monkeypatch):
    """Preserve an edited first round without marking it complete."""
    notes = {
        "index.md": "[Conclusion](history/round.md)",
        "history/round.md": "The verified conclusion.",
    }
    plan = {
        "entry": "index.md",
        "round": "history/round.md",
        "writes": [
            {"path": name, "content": base64.b64encode(content.encode()).decode()}
            for name, content in notes.items()
        ],
        "targets": ["history/round.md"],
    }
    original_write = transaction.write_atomically

    def write_with_sync_edit(path, data, *, folder, **kwargs):
        original_write(path, data, folder=folder, **kwargs)
        if path.name == "index.md":
            edited = folder / "history/round.md"
            replacement = edited.with_suffix(".tmp")
            replacement.write_text("Concurrent revision.")
            replacement.replace(edited)

    monkeypatch.setattr(transaction, "write_atomically", write_with_sync_edit)
    with pytest.raises(transaction.TransactionError):
        transaction.create_project(tmp_path, Path("topic"), plan)

    topic = tmp_path / "topic"
    assert (topic / transaction.FIRST_ROUND_PENDING).is_file()
    assert (topic / "history/round.md").read_text() == "Concurrent revision."
