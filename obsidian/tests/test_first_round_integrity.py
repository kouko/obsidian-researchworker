# concern: Evidence replaced during first-round publication is accepted as verified.
import base64
import importlib.util
import io
import json
import sys
from pathlib import Path

HELPER = (
    Path(__file__).resolve().parents[1]
    / "skills/obsidian-research-project/scripts/research_transaction.py"
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
    topic = tmp_path / "topic"
    original_write = transaction.write_initial_file

    def write_with_sync_edit(project_fd, path, data, **kwargs):
        original_write(project_fd, path, data, **kwargs)
        if path.name == "index.md":
            edited = topic / "history/round.md"
            replacement = edited.with_suffix(".tmp")
            replacement.write_text("Concurrent revision.")
            replacement.replace(edited)

    monkeypatch.setattr(transaction, "write_initial_file", write_with_sync_edit)
    monkeypatch.setattr(sys, "argv", [str(HELPER), "create", str(tmp_path), "topic"])
    monkeypatch.setattr(sys, "stdin", io.StringIO(json.dumps(plan)))
    assert transaction.main() == 1

    assert (topic / transaction.FIRST_ROUND_PENDING).is_file()
    assert (topic / "history/round.md").read_text() == "Concurrent revision."
