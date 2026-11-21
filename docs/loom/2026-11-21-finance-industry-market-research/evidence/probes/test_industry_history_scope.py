# concern: A quarter lookup loses intact earlier evidence or adopts a copied study's release history.
from pathlib import Path
import sys

FINANCE_TESTS = Path(__file__).resolve().parents[5] / "obsidian-finance" / "tests"
sys.path.insert(0, str(FINANCE_TESTS))
from test_market_research import cite, publish, record, resume


def test_latest_only_missing_note_leaves_prior_cutoff_resumable(tmp_path):
    (tmp_path / ".obsidian").mkdir()
    initial = dict(record(), market_name="Phones")
    overview = publish(tmp_path, initial)
    revised = record(revision=2, cutoff="2024-11-05")
    revised["supply_chain"] = "A new investigation into supply relationships."
    assert publish(tmp_path, revised) == overview
    (overview.parent / "2024Q3 Phones-Supply Chain.md").rename(tmp_path / "displaced.md")

    recovered = resume(tmp_path, "phones", "2024Q3", cutoff=initial["cutoff"])
    assert recovered["issues"]
    assert recovered["review"] == str(overview)
    assert recovered["record"]["revision"] == 1
    assert cite(tmp_path, "phones", "2024Q3", "size", initial["cutoff"])["claim"] == initial["claims"]["size"]


def test_copied_managed_history_cannot_certify_another_study(tmp_path):
    (tmp_path / ".obsidian").mkdir()
    donor = publish(tmp_path, dict(record(), market_name="Phones"))
    recipient_snapshot = dict(record(market="chips"), market_name="Chips")
    recipient_snapshot["claims"]["size"]["text"] = "Published chip sales"
    recipient = publish(tmp_path, recipient_snapshot)
    marker = "<!-- industry-research:start -->"
    for topic in ("Overview", "Size and Market Share", "Guidance and Outlook"):
        original = donor.parent / f"2024Q3 Phones-{topic}.md"
        target = recipient.parent / f"2024Q3 Chips-{topic}.md"
        local_identity = target.read_text().partition(marker)[0]
        copied_history = original.read_text().partition(marker)[2]
        target.write_text(local_identity + marker + copied_history)

    assert cite(tmp_path, "chips", "2024Q3", "size", "2024-10-31") is None
