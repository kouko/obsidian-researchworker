import importlib.util
from datetime import datetime
from pathlib import Path

import pytest


SCRIPT = (
    Path(__file__).resolve().parents[1]
    / "skills/tw-equity-research/scripts/conference.py"
)
CUTOFF = datetime.fromisoformat("2025-11-30T23:59:59+08:00")
DATE = "2025-11-21T16:00:00+08:00"
RECORDING = "https://www.youtube.com/watch?v=bMWy8nvERVY"
TRANSCRIPT = "https://issuer.example/investor/transcript.pdf"
SRT = "1\n00:00:00,200 --> 00:00:02,900\n管理層說明\n".encode()


@pytest.fixture
def conference():
    spec = importlib.util.spec_from_file_location("tw_equity_conference", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def source(kind, url, date=DATE):
    return {"kind": kind, "url": url, "available_at": date}


def run(conference, root, sources, searches=None):
    return conference.acquire(
        {"sources": sources, "searches": searches or []},
        ticker="1611", quarter="2025Q3", cutoff=CUTOFF, output=root,
    )


def test_published_transcript_precedes_local_fallback(conference, tmp_path, monkeypatch):
    def recover_recording(url, directory):
        return b"recorded speech"

    def no_transcription(*args):
        pytest.fail("published transcript should take precedence")

    monkeypatch.setattr(conference, "_fetch", lambda url: b"%PDF-1.4\n")
    monkeypatch.setattr(conference, "_recording", recover_recording)
    monkeypatch.setattr(conference, "_transcribe", no_transcription)

    result = run(conference, tmp_path, [
        source("transcript", TRANSCRIPT),
        source("recording", RECORDING),
    ])

    assert result["status"]["transcript"] == "acquired"
    assert result["machine_transcript"] is None
    published = result["sources"][0]
    assert (tmp_path / published["path"]).read_bytes().startswith(b"%PDF")
    assert published["url"] == TRANSCRIPT


def test_derived_timestamp_and_recording_provenance(conference, tmp_path, monkeypatch):
    monkeypatch.setattr(conference, "_recording", lambda url, directory: b"sound")
    monkeypatch.setattr(conference, "_captions", lambda url, directory: None)
    monkeypatch.setattr(conference, "_transcribe", lambda *args: ("yap", SRT))

    result = run(conference, tmp_path, [source("recording", RECORDING)])

    item = result["machine_transcript"]
    assert result["status"]["transcript"] == "machine_transcribed"
    assert item["tool"] == "yap"
    assert item["source_url"] == RECORDING
    assert item["recording_available_at"] == DATE
    assert item["recording_sha256"] == result["sources"][0]["sha256"]
    assert (tmp_path / item["path"]).read_bytes() == SRT


def test_captions_can_be_used_when_recording_download_fails(
    conference, tmp_path, monkeypatch,
):
    def fail(*args):
        raise OSError("recording unavailable")

    monkeypatch.setattr(conference, "_recording", fail)
    monkeypatch.setattr(conference, "_captions", lambda url, path: SRT)
    monkeypatch.setattr(conference, "_transcribe", fail)

    result = run(conference, tmp_path, [source("recording", RECORDING)])

    assert result["status"]["recording"] == "failed"
    assert result["status"]["transcript"] == "captions_availability_unverified"
    assert result["captions"]["source_url"] == RECORDING
    assert result["captions"]["available_at"] is None


def test_undated_captions_do_not_block_dated_recording_fallback(
    conference, tmp_path, monkeypatch,
):
    monkeypatch.setattr(conference, "_recording", lambda url, directory: b"sound")
    monkeypatch.setattr(conference, "_captions", lambda url, directory: SRT)
    monkeypatch.setattr(conference, "_transcribe", lambda *args: ("yap", SRT))

    result = run(conference, tmp_path, [source("recording", RECORDING)])

    assert result["status"]["transcript"] == "machine_transcribed"
    assert result["captions"]["status"] == "availability_unverified"


def test_dated_captions_precede_transcription(conference, tmp_path, monkeypatch):
    def fail(*args):
        pytest.fail("dated captions should take precedence")

    monkeypatch.setattr(conference, "_recording", lambda url, directory: b"sound")
    monkeypatch.setattr(conference, "_captions", lambda url, directory: SRT)
    monkeypatch.setattr(conference, "_transcribe", fail)

    result = run(conference, tmp_path, [
        {**source("recording", RECORDING), "caption_available_at": DATE},
    ])

    assert result["status"]["transcript"] == "captions_acquired"
    assert result["captions"]["available_at"] == DATE


def test_failed_transcription_and_search_gaps_are_explicit(
    conference, tmp_path, monkeypatch,
):
    def fail(*args):
        raise OSError("local tool unavailable")

    monkeypatch.setattr(conference, "_recording", lambda url, directory: b"sound")
    monkeypatch.setattr(conference, "_captions", lambda url, directory: None)
    monkeypatch.setattr(conference, "_transcribe", fail)
    searches = [{"place": "MOPS", "status": "checked", "kinds": ["slides"]}]

    result = run(conference, tmp_path, [source("recording", RECORDING)], searches)

    assert result["machine_transcript"]["status"] == "failed"
    assert result["status"] == {
        "recording": "acquired", "slides": "not_found", "transcript": "failed",
    }
    assert result["searches"] == searches


def test_future_and_unverified_sources_never_download(conference, tmp_path, monkeypatch):
    def fail(*args):
        pytest.fail("ineligible source must not be downloaded")

    monkeypatch.setattr(conference, "_fetch", fail)
    monkeypatch.setattr(conference, "_recording", fail)
    monkeypatch.setattr(conference, "_captions", fail)
    result = run(conference, tmp_path, [
        source("slides", "https://issuer.example/slides.pdf", "2025-12-01T00:00:00+08:00"),
        source("recording", RECORDING, None),
    ])

    assert result["status"] == {
        "recording": "availability_unverified",
        "slides": "after_cutoff",
        "transcript": "not_checked",
    }
    assert not list(tmp_path.iterdir())
