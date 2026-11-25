#!/usr/bin/env python3
"""Capture vetted public sources for one conference and its local transcript."""

import argparse
import hashlib
import json
import re
import shutil
import subprocess
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlsplit
from urllib.request import urlopen


KINDS = ("slides", "transcript", "recording")
MAX_BYTES = 256 * 1024 * 1024
TIMECODE = re.compile(
    r"(?m)^\s*(?:\d{2,}:)?[0-5]\d:[0-5]\d[.,]\d{3}"
    r" --> (?:\d{2,}:)?[0-5]\d:[0-5]\d[.,]\d{3}(?: [^\r\n]+)?\r?$"
)


def _cutoff_time(value):
    try:
        parsed = datetime.fromisoformat(value)
    except (TypeError, ValueError):
        return None
    return parsed if parsed.utcoffset() is not None else None


def _public_url(value):
    parsed = urlsplit(value)
    if parsed.scheme != "https" or not parsed.hostname or parsed.username or parsed.password:
        raise ValueError("a public HTTPS evidence URL is required")


def _fetch(url):
    with urlopen(url, timeout=30) as response:
        _public_url(response.url)
        payload = response.read(MAX_BYTES + 1)
    if not payload or len(payload) > MAX_BYTES:
        raise ValueError("empty or oversized conference document")
    return payload


def _tool(name, arguments, directory, timeout):
    executable = shutil.which(name)
    if executable is None:
        raise OSError(f"{name} is not available")
    process = subprocess.run(
        [executable, *arguments], cwd=directory, capture_output=True,
        timeout=timeout, check=False, text=True, errors="replace",
    )
    if process.returncode:
        raise OSError(f"{name} exited with status {process.returncode}")
    return process.stdout


def _recording(url, directory):
    _tool("yt-dlp", [
        "--ignore-config", "--no-playlist", "--max-filesize", "256M",
        "--extract-audio", "--audio-format", "wav",
        "--postprocessor-args", "ExtractAudio+ffmpeg_o:-ac 1 -ar 16000",
        "--output", "recording.%(ext)s",
        "--", url,
    ], directory, 600)
    wave = directory / "recording.wav"
    if not wave.is_file() or not 44 < wave.stat().st_size <= MAX_BYTES:
        raise ValueError("no usable recording within capture size")
    return wave.read_bytes()


def _captions(url, directory):
    if urlsplit(url).hostname not in {"youtube.com", "www.youtube.com", "youtu.be"}:
        return None
    _tool("yt-dlp", [
        "--ignore-config", "--no-playlist", "--skip-download", "--write-subs",
        "--write-auto-subs", "--sub-langs", "zh-TW,zh-Hant,zh,zh-orig,en,en-orig",
        "--sub-format", "vtt", "--output", "captions.%(ext)s", "--", url,
    ], directory, 120)
    for lang in ("zh-TW", "zh-Hant", "zh-orig", "zh", "en-orig", "en"):
        path = directory / f"captions.{lang}.vtt"
        if path.is_file():
            payload = path.read_bytes()
            if _timed(payload):
                return payload
    return None


def _timed(payload):
    text = payload.decode("utf-8-sig", errors="replace")
    return any(
        text[match.end():].lstrip("\r\n").split("\n", 1)[0].strip()
        for match in TIMECODE.finditer(text)
    )


def _transcribe(directory, whisper_model):
    try:
        _tool("yap", [
            "transcribe", "--locale", "zh-TW", "recording.wav", "--srt",
            "-o", "yap.srt",
        ], directory, 900)
        transcript = (directory / "yap.srt").read_bytes()
        if _timed(transcript):
            return "yap", transcript
        raise ValueError("yap returned no timed speech")
    except (OSError, ValueError, subprocess.TimeoutExpired) as error:
        if whisper_model is None:
            raise OSError(f"local transcription failed: {error}") from error
    _tool("ffmpeg", [
        "-nostdin", "-v", "error", "-i", "recording.wav", "-ac", "1",
        "-ar", "16000", "whisper.wav",
    ], directory, 120)
    _tool("whisper-cli", [
        "-ng", "-m", str(whisper_model), "-f", "whisper.wav", "-l", "zh",
        "-osrt", "-of", "whisper",
    ], directory, 900)
    return "whisper-cli", (directory / "whisper.srt").read_bytes()


def _suffix(payload):
    if payload.startswith(b"%PDF-"):
        return ".pdf"
    start = payload.lstrip().lower()
    if start.startswith((b"<!doctype html", b"<html", b"<head", b"<body")):
        return ".html"
    try:
        payload.decode("utf-8")
    except UnicodeError:
        return ".bin"
    return ".txt"


def _store(output, kind, payload, suffix):
    digest = hashlib.sha256(payload).hexdigest()
    path = output / f"{kind}-{digest}{suffix}"
    output.mkdir(parents=True, exist_ok=True)
    try:
        with path.open("xb") as stream:
            stream.write(payload)
    except FileExistsError:
        if path.is_symlink() or path.read_bytes() != payload:
            raise OSError(f"conflicting evidence path: {path.name}")
    return {"path": path.name, "sha256": digest}


def _source_status(kind, sources, searches):
    statuses = {item["status"] for item in sources if item["kind"] == kind}
    for status in ("acquired", "failed", "availability_unverified", "after_cutoff"):
        if status in statuses:
            return status
    attempts = {item["status"] for item in searches if kind in item.get("kinds", KINDS)}
    if "failed" in attempts:
        return "search_failed"
    return "not_found" if "checked" in attempts else "not_checked"


def acquire(inventory, *, ticker, quarter, cutoff, output, whisper_model=None):
    if cutoff.utcoffset() is None:
        raise ValueError("research cutoff requires an explicit time zone")
    if not re.fullmatch(r"\d{4}", ticker) or not re.fullmatch(r"\d{4}Q[1-4]", quarter):
        raise ValueError("a Taiwan ticker and YYYYQn quarter are required")
    sources = inventory["sources"]
    searches = inventory.get("searches", [])
    if not isinstance(sources, list) or not isinstance(searches, list):
        raise ValueError("sources and searches must be arrays")
    for item in sources:
        if item["kind"] not in KINDS:
            raise ValueError(f"unknown conference evidence kind: {item['kind']}")
        _public_url(item["url"])
    for item in searches:
        if item["status"] not in {"checked", "failed"} or not item["place"]:
            raise ValueError("search results need a place and checked or failed status")
        if any(kind not in KINDS for kind in item.get("kinds", KINDS)):
            raise ValueError("search results contain an unknown evidence kind")
    captured_at = datetime.now(timezone.utc).isoformat()
    result = {
        "ticker": ticker, "quarter": quarter, "cutoff": cutoff.isoformat(),
        "captured_at": captured_at, "searches": searches, "sources": [],
        "captions": None, "machine_transcript": None,
    }
    with tempfile.TemporaryDirectory(prefix="tw-conference-") as scratch:
        directory = Path(scratch)
        recordings = []
        for source in sources:
            kind, url = source["kind"], source["url"]
            available_at = _cutoff_time(source.get("available_at"))
            item = {"kind": kind, "url": url, "available_at": source.get("available_at")}
            result["sources"].append(item)
            if available_at is None:
                item["status"] = "availability_unverified"
                continue
            if available_at > cutoff:
                item["status"] = "after_cutoff"
                continue
            if kind == "recording":
                work = directory / f"recording-{len(recordings)}"
                work.mkdir()
                caption_date = _cutoff_time(source.get("caption_available_at"))
                captions_eligible = caption_date is not None and caption_date <= cutoff
                recordings.append((item, work, caption_date, captions_eligible))
                continue
            try:
                payload = _fetch(url)
                item.update(_store(output, kind, payload, _suffix(payload)), status="acquired")
            except (OSError, ValueError) as error:
                item.update(status="failed", error=str(error))
        has_transcript = any(
            item["kind"] == "transcript" and item["status"] == "acquired"
            for item in result["sources"] if item["kind"] != "recording"
        )
        for item, work, caption_date, captions_eligible in recordings:
            _capture_recording(
                result, item, work, output, whisper_model, has_transcript,
                caption_date, captions_eligible,
            )
    result["status"] = {
        kind: _source_status(kind, result["sources"], searches) for kind in KINDS
    }
    if result["status"]["transcript"] != "acquired":
        if _usable_captions(result):
            result["status"]["transcript"] = "captions_acquired"
        elif result["machine_transcript"]:
            result["status"]["transcript"] = result["machine_transcript"]["status"]
        elif result["captions"]:
            result["status"]["transcript"] = "captions_" + result["captions"]["status"]
    return result


def _usable_captions(result):
    return result["captions"] and result["captions"]["status"] == "acquired"


def _capture_recording(
    result, item, directory, output, whisper_model, has_transcript,
    caption_date, captions_eligible,
):
    url = item["url"]
    origin = {"source_url": url, "recording_available_at": item["available_at"]}
    if not has_transcript and (result["captions"] is None or (
        captions_eligible and not _usable_captions(result)
    )):
        try:
            captions = _captions(url, directory)
            if captions and _timed(captions):
                suffix = ".vtt" if captions.startswith(b"WEBVTT") else ".srt"
                if captions_eligible:
                    status = "acquired"
                else:
                    status = "after_cutoff" if caption_date else "availability_unverified"
                result["captions"] = {
                    **origin, "status": status,
                    "available_at": caption_date.isoformat() if caption_date else None,
                    **_store(output, "captions", captions, suffix),
                }
        except (OSError, ValueError, subprocess.TimeoutExpired) as error:
            item["captions_error"] = str(error)
    try:
        audio = _recording(url, directory)
        item.update(
            _store(output, "recording", audio, ".wav"),
            status="acquired", capture_format="wav-pcm-mono-16kHz",
        )
    except (OSError, ValueError, subprocess.TimeoutExpired) as error:
        item.update(status="failed", error=str(error))
        return
    if has_transcript or _usable_captions(result) or (
        result["machine_transcript"] and result["machine_transcript"]["status"] == "machine_transcribed"
    ):
        return
    transcript = {**origin, "recording_sha256": item["sha256"]}
    result["machine_transcript"] = transcript
    try:
        tool, payload = _transcribe(directory, whisper_model)
        if not _timed(payload):
            raise ValueError("local transcription returned no timed speech")
        transcript.update(
            _store(output, "machine-transcript", payload, ".srt"),
            status="machine_transcribed", tool=tool,
        )
    except (OSError, ValueError, subprocess.TimeoutExpired) as error:
        transcript.update(status="failed", error=str(error))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ticker", required=True)
    parser.add_argument("--quarter", required=True)
    parser.add_argument("--cutoff", required=True)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--whisper-model", type=Path)
    args = parser.parse_args()
    cutoff = _cutoff_time(args.cutoff)
    if cutoff is None:
        parser.error("cutoff requires an ISO datetime with an explicit time zone")
    try:
        inventory = json.loads(args.input.read_text(encoding="utf-8"))
        model = args.whisper_model.resolve(strict=True) if args.whisper_model else None
        result = acquire(
            inventory, ticker=args.ticker, quarter=args.quarter, cutoff=cutoff,
            output=args.output, whisper_model=model,
        )
    except (OSError, KeyError, TypeError, ValueError) as error:
        parser.error(str(error))
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
