"""Render a technical outlook and optionally publish a vault-local note."""

import argparse
import json
import os
import sys
from contextlib import ExitStack, contextmanager
from html import escape
from pathlib import Path
from urllib.parse import quote
from uuid import uuid4

DIRECTORY_FLAGS = os.O_RDONLY | os.O_NOFOLLOW | os.O_DIRECTORY
HORIZON_NAMES = {"short": "Short term", "medium": "Medium term", "long": "Long term"}


def _cell(value):
    value = escape(str(value), quote=False).replace("|", "&#124;").replace("\n", " ")
    return value.replace("[", "&#91;").replace("]", "&#93;").replace("`", "&#96;")


def _span(start, end):
    return f"{start} to {end}" if start is not None and end is not None else "Unavailable"


def _render_patterns(patterns):
    if patterns["status"] == "no_match":
        return ["- Daily chart patterns: no supported pattern matched."]
    if patterns["status"] == "insufficient":
        return [f"- Daily chart patterns: insufficient data. {_cell(patterns['reason'])}"]
    lines = ["- Daily chart patterns:"]
    for match in patterns["matches"]:
        title = match["kind"].replace("_", " ").capitalize()
        lines.append(f"  - **{title} — {match['state']}** (knowable on {match['known_on']}).")
        anchors = "; ".join(
            f"{anchor['kind']} {anchor['price']:.6g} on {anchor['date']} (known on {anchor['confirmed_on']})"
            for anchor in match["anchors"]
        )
        lines.append(f"    - Anchors: {anchors}.")
        boundaries = match["boundaries"]
        lines.append(
            f"    - Boundaries on {boundaries['date']}: lower {boundaries['lower']:.6g}, "
            f"upper {boundaries['upper']:.6g}."
        )
        lines.append(f"    - Confirmation condition: {match['confirmation_condition']}")
        lines.append(f"    - Invalidation condition: {match['invalidation_condition']}")
        for label in ("confirmation", "invalidation"):
            event = match[label]
            if event is None:
                continue
            volume = "unavailable" if event["volume"] is None else str(event["volume"])
            level = "" if event["level"] is None else f", threshold {event['level']:.6g}"
            reason = f", {event['reason']}" if "reason" in event else ""
            direction = f" ({event['direction']})" if "direction" in event else ""
            lines.append(
                f"    - {label.capitalize()}{direction} on {event['date']}: "
                f"close {event['close']:.6g}{level}, volume {volume}{reason}."
            )
    return lines


def render_report(report, *, chart=None, source=None):
    """Render the same horizon conclusions in conversation and in a note."""
    lines = [
        f"# {_cell(report['ticker'])} technical outlook",
        "",
        f"Cutoff: {_cell(report['cutoff'])} ({_cell(report['timezone'])})",
        "",
        "| Horizon | Length | Observed trading dates | Outlook dates | Current conclusion |",
        "| --- | --- | --- | --- | --- |",
    ]
    for horizon in report["horizons"]:
        values = (
            HORIZON_NAMES[horizon["name"]], horizon["length"],
            _span(horizon["observed_start"], horizon["observed_end"]),
            _span(horizon["outlook_start"], horizon["outlook_end"]),
            horizon["trend"].replace("_", " ").capitalize(),
        )
        lines.append("| " + " | ".join(map(_cell, values)) + " |")
    if chart:
        lines.extend(["", f"![Price and volume]({quote(chart)})"])
    for horizon in report["horizons"]:
        lines.extend(["", f"## {HORIZON_NAMES[horizon['name']]}", ""])
        if horizon.get("conclusion"):
            lines.extend([f"**Conclusion:** {_cell(horizon['conclusion'])}", ""])
        lines.extend(f"- {_cell(item)}" for item in horizon["evidence"])
        for label in ("support", "resistance"):
            level = horizon["levels"].get(label)
            if level is not None:
                lines.append(f"- {label.capitalize()}: {_cell(level['price'])} ({_cell(level['date'])})")
        if horizon.get("trigger"):
            lines.append(f"- What would strengthen the view: {_cell(horizon['trigger'])}")
        if horizon.get("invalidation"):
            lines.append(f"- What would change the view: {_cell(horizon['invalidation'])}")
        if horizon.get("alternative"):
            lines.append(f"- Alternative scenario: {_cell(horizon['alternative'])}")
        if "patterns" in horizon:
            lines.extend(_render_patterns(horizon["patterns"]))
        lines.extend(f"- Limitation: {_cell(item)}" for item in horizon["limitations"])
    lines.extend([
        "", "## Data and method", "",
        f"- Source: {_cell(report['source'])}",
        f"- Price adjustment: {_cell(report['adjustment'])}",
        f"- Snapshot available at: {_cell(report['available_at'])}",
        f"- Snapshot identity: `{_cell(report['snapshot_id'])}`",
        f"- Analysis method: `{_cell(report['method'])}`",
    ])
    if source:
        lines.append(f"- [Retained input snapshot]({quote(source)})")
    if report.get("settings"):
        settings = json.dumps(report["settings"], sort_keys=True)
        lines.append(f"- Analysis settings: `{_cell(settings)}`")
    lines.extend(f"- Excluded: {_cell(item)}" for item in report["exclusions"])
    lines.extend(f"- Fetch exclusion: {_cell(item)}" for item in report.get("fetch_exclusions", []))
    return "\n".join(lines) + "\n"


def _render_chart(report):
    bars = report["bars"]
    width, left, right = 760, 58, 722
    prices = [bar["close"] for bar in bars]
    floor, ceiling = min(bar["low"] for bar in bars), max(bar["high"] for bar in bars)
    volumes = [bar["volume"] for bar in bars if bar["volume"] is not None]
    max_volume = max(volumes, default=0) or 1
    step = (right - left) / max(1, len(bars) - 1)
    spread = ceiling - floor or 1

    def y(price):
        return 236 - 190 * ((price - floor) / spread)

    points = " ".join(f"{left + i * step:.2f},{y(price):.2f}" for i, price in enumerate(prices))
    elements = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="366" viewBox="0 0 {width} 366">',
        "<title>Daily closing price and volume</title>",
        '<rect width="760" height="366" fill="#ffffff"/>',
        '<g font-family="sans-serif" font-size="12" fill="#182138">',
        f'<text x="58" y="24">{escape(report["ticker"])} daily closing price and volume</text>',
        f'<text x="8" y="52">{ceiling:.2f}</text>',
        f'<text x="8" y="236">{floor:.2f}</text>',
        '<text x="8" y="267">Volume</text>',
        f'<text x="{left}" y="352">{escape(bars[0]["date"])}</text>',
        f'<text x="{right}" y="352" text-anchor="end">{escape(bars[-1]["date"])}</text>',
        "</g>",
        '<path d="M 58 46 V 236 H 722 M 58 269 V 329 H 722" stroke="#a3adc3" fill="none"/>',
        f'<polyline points="{points}" fill="none" stroke="#2458ac" stroke-width="2"/>',
    ]
    if len(bars) == 1:
        elements.append(f'<circle cx="{left}" cy="{y(prices[0]):.2f}" r="3" fill="#2458ac"/>')
    # The note lists every horizon's levels. Mark the nearest-term view on
    # the chart to keep repeated or tightly spaced labels readable.
    short = next(horizon for horizon in report["horizons"] if horizon["name"] == "short")
    for label, color, offset in (("support", "#126449", 14), ("resistance", "#943e2b", -4)):
        level = short["levels"].get(label)
        if level is None:
            continue
        level_y = y(level["price"])
        elements.extend([
            f'<path d="M {left} {level_y:.2f} H {right}" stroke="{color}" stroke-dasharray="5 4"/>',
            f'<text x="{right}" y="{level_y + offset:.2f}" fill="{color}" '
            f'text-anchor="end" font-family="sans-serif" font-size="11">'
            f'Short {label} {level["price"]:.6g}</text>',
        ])
    for i, bar in enumerate(bars):
        if bar["volume"] is None:
            continue
        x = left + i * step
        height = 58 * (bar["volume"] / max_volume)
        elements.append(
            f'<rect x="{x:.2f}" y="{329-height:.2f}" width="{min(step * .75, 10):.2f}" '
            f'height="{height:.2f}" fill="#7e9dcc"/>'
        )
    elements.append("</svg>")
    return "\n".join(elements).encode("utf-8")


@contextmanager
def _open_destination(vault, note):
    root = Path(vault)
    relative = Path(note)
    if not root.is_absolute():
        raise ValueError("The vault path must be absolute.")
    if relative.is_absolute() or ".." in relative.parts or relative.suffix.lower() != ".md":
        raise ValueError("The note must be a relative Markdown path within the vault.")
    with ExitStack() as stack:
        current = os.open(root.anchor, DIRECTORY_FLAGS)
        stack.callback(os.close, current)
        for part in (*root.parts[1:], *relative.parts[:-1]):
            if part == "..":
                raise ValueError("The vault path must not contain parent traversal.")
            current = os.open(part, DIRECTORY_FLAGS, dir_fd=current)
            stack.callback(os.close, current)
        yield current, relative.name


def _write_stage(stage, name, data):
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW
    with os.fdopen(os.open(name, flags, 0o600, dir_fd=stage), "wb") as stream:
        stream.write(data)
        stream.flush()
        os.fsync(stream.fileno())


def _link_files(parent, stage, payloads):
    linked = []
    try:
        for name in payloads:
            os.link(name, name, src_dir_fd=stage, dst_dir_fd=parent, follow_symlinks=False)
            linked.append(name)
        os.fsync(parent)
    except OSError:
        for name in reversed(linked):
            try:
                current = os.stat(name, dir_fd=parent, follow_symlinks=False)
                staged = os.stat(name, dir_fd=stage, follow_symlinks=False)
                if not os.path.samestat(current, staged):
                    continue
                with os.fdopen(os.open(name, os.O_RDONLY | os.O_NOFOLLOW, dir_fd=parent), "rb") as stream:
                    if stream.read(len(payloads[name]) + 1) != payloads[name]:
                        continue
                os.unlink(name, dir_fd=parent)
            except FileNotFoundError:
                continue
        raise


def _publish(parent, payloads):
    stage_name = ".technical-stage-" + uuid4().hex
    os.mkdir(stage_name, 0o700, dir_fd=parent)
    try:
        stage = os.open(stage_name, DIRECTORY_FLAGS, dir_fd=parent)
        try:
            for name, data in payloads.items():
                _write_stage(stage, name, data)
            _link_files(parent, stage, payloads)
        finally:
            try:
                for name in os.listdir(stage):
                    os.unlink(name, dir_fd=stage)
            finally:
                os.close(stage)
    finally:
        os.rmdir(stage_name, dir_fd=parent)


def _attachment_links(markdown, chart, source):
    if markdown.count("({{source}})") != 1 or markdown.count("{{source}}") != 1:
        raise ValueError("Localized note must include one Markdown link to {{source}}.")
    chart_links = markdown.count("({{chart}})")
    if chart_links != bool(chart) or markdown.count("{{chart}}") != chart_links:
        raise ValueError("Localized note must link to {{chart}} exactly once when bars are available.")
    markdown = markdown.replace("({{source}})", f"({quote(source)})")
    if chart:
        markdown = markdown.replace("({{chart}})", f"({quote(chart)})")
    return markdown


def save_report(report, snapshot, vault, note, *, note_markdown=None):
    """Publish attachments first and expose a complete, new note last."""
    with _open_destination(vault, note) as (parent, name):
        stem = Path(name).stem
        chart = stem + ".chart.svg" if report["bars"] else None
        source = stem + ".source.json"
        payloads = {
            source: (json.dumps(snapshot, ensure_ascii=False, sort_keys=True, indent=2, allow_nan=False) + "\n").encode("utf-8"),
        }
        if chart:
            payloads[chart] = _render_chart(report)
        markdown = (
            render_report(report, chart=chart, source=source) if note_markdown is None
            else _attachment_links(note_markdown, chart, source)
        )
        payloads[name] = markdown.encode("utf-8")
        _publish(parent, payloads)
    return Path(vault) / note


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("snapshot", type=Path, help="Path to a price snapshot JSON file")
    parser.add_argument("--cutoff", help="Offset-aware ISO analysis cutoff (defaults to snapshot availability)")
    parser.add_argument("--vault", type=Path, help="Absolute vault path")
    parser.add_argument("--note", help="New Markdown path relative to the vault")
    parser.add_argument("--note-markdown", type=Path, help="Prepared UTF-8 Markdown for the saved note")
    args = parser.parse_args()
    if bool(args.vault) != bool(args.note):
        parser.error("--vault and --note must be used together")
    if args.note_markdown and not args.note:
        parser.error("--note-markdown requires --vault and --note")
    from analyze import analyze
    from snapshot import validate_snapshot

    try:
        payload = json.loads(args.snapshot.read_text(encoding="utf-8"))
        cutoff = args.cutoff or (payload.get("available_at") if isinstance(payload, dict) else None)
        snapshot = validate_snapshot(payload, cutoff)
        report = analyze(snapshot)
        if args.vault:
            markdown = args.note_markdown.read_text(encoding="utf-8") if args.note_markdown else None
            note = save_report(report, payload, args.vault, args.note, note_markdown=markdown)
            print(f"Saved {note}", file=sys.stderr)
        print(render_report(report), end="")
    except (OSError, ValueError) as exc:
        parser.exit(1, f"Technical analysis unavailable: {exc}\n")


if __name__ == "__main__":
    main()
