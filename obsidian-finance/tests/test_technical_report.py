"""Publication and date evidence for standalone technical analysis."""

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "skills/technical-analysis/scripts"))

from report import render_report, save_report


@pytest.fixture
def report():
    horizons = [
        dict(
            name=name, length=length, observed_start="2023-02-28",
            observed_end="2024-02-29", outlook_start="2024-03-01",
            outlook_end=end, trend="up", levels={}, metrics={},
            evidence=["Observed price increased."], limitations=[],
            trigger="Watch the next close.", invalidation="Reassess below support.",
        )
        for name, length, end in [
            ("short", "3 weeks", "2024-03-21"),
            ("medium", "3 months", "2024-05-29"),
            ("long", "1 year", "2025-02-28"),
        ]
    ]
    horizons[-1].update(
        observed_start=None, observed_end=None, trend="insufficient",
        evidence=[], limitations=["Insufficient long-term evidence."],
    )
    return dict(
        ticker="TEST", timezone="America/New_York", source="Fixture",
        adjustment="unadjusted", available_at="2024-02-29T17:00:00-05:00",
        cutoff="2024-02-29T17:00:00-05:00", snapshot_id="fixture-id",
        method="fixture-method", exclusions=["Incomplete bar excluded."],
        bars=[dict(date="2024-02-29", open=10, high=12, low=9, close=11, volume=10)],
        horizons=horizons,
    )


def test_reports_three_dated_outlooks_and_evidence(report):
    rendered = render_report(report)
    for length, end in [("3 weeks", "2024-03-21"), ("3 months", "2024-05-29"), ("1 year", "2025-02-28")]:
        assert length in rendered and end in rendered
    for item in ("2023-02-28", "2024-02-29", "2024-03-01", "Insufficient long-term evidence",
                 "fixture-id", "fixture-method", "Incomplete bar excluded", "unadjusted"):
        assert item in rendered


def test_save_note_chart_and_source(report, tmp_path):
    evidence = {**report, "evidence": "Captured at source"}
    note = save_report(report, evidence, tmp_path, "research.md")
    assert note == tmp_path / "research.md"
    assert "research.chart.svg" in note.read_text()
    chart = tmp_path / "research.chart.svg"
    assert "Volume" in chart.read_text()
    source = json.loads((tmp_path / "research.source.json").read_text())
    assert source["snapshot_id"] == "fixture-id"
    assert source["evidence"] == "Captured at source"


def test_note_collision_keeps_existing_content_and_cleans_own_assets(report, tmp_path):
    note = tmp_path / "research.md"
    note.write_text("keep me")
    with pytest.raises(FileExistsError):
        save_report(report, report, tmp_path, note.name)
    assert note.read_text() == "keep me"
    assert list(tmp_path.iterdir()) == [note]


def test_attachment_collision_preserves_existing_asset(report, tmp_path):
    asset = tmp_path / "research.chart.svg"
    asset.write_text("keep me")
    with pytest.raises(FileExistsError):
        save_report(report, report, tmp_path, "research.md")
    assert asset.read_text() == "keep me"
    assert list(tmp_path.iterdir()) == [asset]


def test_vault_confinement_skips_symlinks(report, tmp_path):
    vault = tmp_path / "vault"
    vault.mkdir()
    (vault / "escape").symlink_to(tmp_path, target_is_directory=True)
    with pytest.raises(OSError):
        save_report(report, report, vault, "escape/research.md")
    with pytest.raises(ValueError):
        save_report(report, report, vault, "../research.md")
    assert not (tmp_path / "research.md").exists()


def test_interrupted_publication_cleans_only_its_assets(report, tmp_path, monkeypatch):
    original_link = os.link
    existing = tmp_path / "other.md"
    existing.write_text("prior note")

    def fail_on_chart(source, destination, **kwargs):
        if destination.endswith(".svg"):
            raise OSError("interrupted publication")
        return original_link(source, destination, **kwargs)

    monkeypatch.setattr(os, "link", fail_on_chart)
    with pytest.raises(OSError, match="interrupted publication"):
        save_report(report, report, tmp_path, "research.md")
    assert list(tmp_path.iterdir()) == [existing]
    assert existing.read_text() == "prior note"


def test_cli_retains_original_snapshot_for_exact_cutoff_replay(tmp_path):
    payload = {
        "ticker": "TEST", "timezone": "America/New_York", "source": "Deliberate fixture",
        "adjustment": "unadjusted", "evidence": "Test capture",
        "available_at": "2024-02-29T17:00:00-05:00",
        "bars": [
            {"date": "2024-02-28", "session_close": "2024-02-28T16:00:00-05:00",
             "open": 10, "high": 12, "low": 9, "close": 11, "volume": None},
            {"date": "2024-02-29", "session_close": "2024-02-29T16:00:00-05:00",
             "open": 11, "high": 13, "low": 10, "close": 12, "complete": False},
        ],
    }
    original = tmp_path / "input.json"
    original.write_text(json.dumps(payload))
    cli = Path(__file__).resolve().parents[1] / "skills/technical-analysis/scripts/report.py"
    command = [sys.executable, str(cli)]
    first = subprocess.run(
        [*command, str(original), "--vault", str(tmp_path.resolve()), "--note", "outlook.md"],
        check=True, capture_output=True, text=True,
    )
    retained = tmp_path / "outlook.source.json"
    assert json.loads(retained.read_text()) == payload
    replay = subprocess.run([*command, str(retained)], check=True, capture_output=True, text=True)
    assert first.stdout == replay.stdout
    assert "trading session was incomplete" in replay.stdout
