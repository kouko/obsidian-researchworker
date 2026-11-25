"""Obsidian properties and versioned Markdown records for the research pilot."""

from datetime import date, datetime
from html import escape, unescape
import json
from pathlib import Path
import re
from string import Template
from urllib.parse import quote


ANALYSIS_ROLES = frozenset({
    "financial-analysis", "operating-analysis", "industry-and-competition",
    "forward-forecast", "valuation-and-risk", "technical-analysis", "synthesis",
})
_RUN_FIELDS = ("asset_id", "fiscal_quarter", "as_of", "review_id", "status")
_SCALAR_STRING_TAG = r"(?:(?:!!str|!<tag:yaml\.org,2002:str>)[ \t]+)?"
_ROLE_FIELDS = {
    "research-overview": (),
    "asset-entry": ("asset_id",),
    "quarter-navigation": ("asset_id", "fiscal_quarter"),
    "review": _RUN_FIELDS,
    "quarter-overview": _RUN_FIELDS,
    "source-registration": ("asset_id", "source_id", "source_version"),
    "method-registration": ("asset_id", "method_id", "method_version"),
    **dict.fromkeys(ANALYSIS_ROLES, _RUN_FIELDS),
}


def _validate_role_properties(props, role):
    for field in _ROLE_FIELDS[role]:
        value = props.get(field)
        if not isinstance(value, str) or not value.strip():
            raise ValueError("invalid or missing Obsidian property: " + field)
    for field in ("asset_id", "review_id", "source_id", "method_id", "predecessor"):
        if field in props and (not isinstance(props[field], str)
                or not re.fullmatch(r"[a-zA-Z0-9_-]+", props[field])):
            raise ValueError("invalid Obsidian identity: " + field)
    if "fiscal_quarter" in props and (not isinstance(props["fiscal_quarter"], str)
            or not re.fullmatch(r"[0-9]{4}Q[1-4]", props["fiscal_quarter"])):
        raise ValueError("invalid Obsidian fiscal quarter")
    for field in ("as_of", "available_at", "authored_at"):
        if field not in props:
            continue
        value = props[field]
        try:
            if not isinstance(value, str):
                raise ValueError
            if field == "available_at" and re.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2}", value):
                date.fromisoformat(value)
            elif "T" not in value or datetime.fromisoformat(value).utcoffset() is None:
                raise ValueError
        except ValueError as error:
            raise ValueError("invalid Obsidian date or timezone: " + field) from error
    if role in ANALYSIS_ROLES or role in ("review", "quarter-overview"):
        statuses = ("partial", "complete", "draft") if role in ANALYSIS_ROLES else ("partial", "complete")
        if props["status"] not in statuses:
            raise ValueError("invalid Obsidian status")

def _yaml():
    try:
        import yaml
    except ImportError as error:
        raise ValueError("Markdown research records require PyYAML") from error
    return yaml


def _mapping(text):
    yaml = _yaml()

    class Loader(yaml.SafeLoader):
        yaml_implicit_resolvers = {
            key: [rule for rule in rules if rule[0] != "tag:yaml.org,2002:timestamp"]
            for key, rules in yaml.SafeLoader.yaml_implicit_resolvers.items()
        }

        def compose_node(self, parent, index):
            event = self.peek_event()
            if isinstance(event, yaml.AliasEvent) or getattr(event, "anchor", None) is not None:
                raise ValueError("YAML anchors and aliases are unsupported in managed notes")
            return super().compose_node(parent, index)

        def construct_mapping(self, node, deep=False):
            result = {}
            for key_node, value_node in node.value:
                key = self.construct_object(key_node, deep=deep)
                if not isinstance(key, str) or key in result:
                    raise ValueError("managed note properties require unique text keys")
                result[key] = self.construct_object(value_node, deep=deep)
            return result

    try:
        value = yaml.load(text, Loader=Loader)
    except yaml.YAMLError as error:
        raise ValueError("invalid managed note YAML") from error
    if not isinstance(value, dict):
        raise ValueError("managed note metadata must be a mapping")
    return value


def declares_role(text, role):
    lines = text.splitlines()
    if not lines or lines[0] != "---":
        return False
    try:
        end = lines.index("---", 1)
    except ValueError:
        end = len(lines)
    header = "\n".join(lines[1:end])
    def unescape_identifier(match):
        code = int(match[0][2:], 16)
        if code < 128 and (chr(code).isalnum() or chr(code) in "_-"):
            return chr(code)
        return match[0]

    # Match a quoted block key even when an ASCII identifier character is
    # represented by a YAML escape. The actual loader still decides validity.
    lexical = re.sub(r"\\\n[ \t]*", "", header)
    lexical = re.sub(r"\\(?:x[0-9a-fA-F]{2}|u[0-9a-fA-F]{4}|U[0-9a-fA-F]{8})",
                     unescape_identifier, lexical)
    key = _SCALAR_STRING_TAG + r"""(?:finance_role|'finance_role'|"finance_role")"""
    position = (r"(?:^|[,{])[ \t]*" + key + r"[ \t]*:"
                + r"|^[ \t]*\?[ \t]+" + key + r"[ \t]*\n[ \t]*:")
    if not header.lstrip().startswith("{") and "finance_role" not in lexical:
        return False
    try:
        actual = _mapping(header).get("finance_role")
        return actual == role or (isinstance(actual, str) and bool(re.fullmatch(re.escape(role) + r"[ \t]*\[", actual)))
    except ValueError:
        # A recognizable declaration must still reach record validation when
        # the surrounding YAML is malformed or the YAML dependency is absent.
        value = re.escape(role)
        marker = rf"""(?:{position})[ \t]*{_SCALAR_STRING_TAG}(?:{value}|'{value}'|"{value}")(?=[ \t]*(?:[,}}\[]|#|$))"""
        return bool(re.search(marker, lexical, re.M))


def parse_note(text, role, **expected):
    match = re.fullmatch(r"---\r?\n(.*?)\r?\n---\r?\n(.*)", text, re.S)
    if not match:
        raise ValueError("missing YAML frontmatter")
    props, body = _mapping(match[1]), match[2]
    simple = (str, int, float, bool)
    actual_role = props.get("finance_role")
    allowed = (role,) if isinstance(role, str) else role
    if (type(props.get("finance_schema")) is not int or props["finance_schema"] != 1
            or not isinstance(actual_role, str) or actual_role not in _ROLE_FIELDS
            or actual_role not in allowed or not isinstance(props.get("title"), str)
            or not props["title"].strip() or not re.search(r"(?m)^# \S", body)
            or any(type(value) not in simple and (
                not isinstance(value, list) or not all(type(item) in simple for item in value))
                   for value in props.values())):
        raise ValueError("invalid Obsidian properties or missing note heading")
    _validate_role_properties(props, actual_role)
    for key, value in expected.items():
        if props.get(key) != value:
            raise ValueError("managed Markdown identity mismatch: " + key)
    return props, body


def render_draft(properties, body):
    return "---\n" + _dump(dict(properties, status="draft")) + "---\n" + body


def record(text, role, **expected):
    props, body = parse_note(text, role, **expected)
    matches = re.findall(_record_pattern(role), body)
    if len(matches) != 1:
        raise ValueError("expected one " + role + " record")
    return props, _mapping(matches[0])


def _record_pattern(role):
    return (r"(?m)^## Research record\r?\n\r?\n\x60{3}finance-" + role
            + r"\r?\n([\s\S]*?)\r?\n\x60{3}\r?$")


def _dump(record):
    yaml = _yaml()

    class Dumper(yaml.SafeDumper):
        def ignore_aliases(self, data):
            return True

    return yaml.dump(record, sort_keys=False, allow_unicode=True, Dumper=Dumper)


def _visible_text(value):
    text = " ".join(str(value).split())
    return re.sub(r"([\\`*_{}\[\]()#+!|~])", r"\\\1", escape(text, quote=False))


_SOURCE_CONTEXT_HEADING = "## Original research context"
_CONTEXT_LINK = re.compile(
    r"""!?\[([^\]\n]*)\]\((?:<([^<>\n]*)>|((?:[^\s()<>\\]|\([^\s()<>\\]*\))*))"""
    r"""(?:[ \t]+(?:"[^"\n]*"|'[^'\n]*'|\([^()\n]*\)))?\)"""
)
_PUBLIC_CONTEXT_URL = re.compile(r"https?://[^\s/<>()\[\]\\]+[^\s<>\[\]\\]*", re.I)


def _context_url(link):
    url = link[2] if link[2] is not None else link[3]
    if not link[0].startswith("!") and _PUBLIC_CONTEXT_URL.fullmatch(url):
        return url
    return None


def _context_destination(url):
    return f"<{url}>" if "(" in url or ")" in url else url


def _render_context_paragraph(paragraph):
    parts = []
    offset = 0
    for link in _CONTEXT_LINK.finditer(paragraph):
        url = _context_url(link)
        if url is None:
            continue
        before = paragraph[offset:link.start()]
        parts.append(_visible_text(before))
        if before.endswith(" "):
            parts.append(" ")
        destination = _context_destination(escape(url, quote=False))
        parts.append(f"[{_visible_text(link[1])}]({destination})")
        offset = link.end()
        if paragraph[offset:offset + 1] == " ":
            parts.append(" ")
            offset += 1
    parts.append(_visible_text(paragraph[offset:]))
    return "".join(parts)


def _portable_context_link(link):
    url = _context_url(link)
    if url is None:
        return link[1]
    return f"[{link[1]}]({_context_destination(unescape(url))})"


def registration_context(text, role, *, captured):
    """Retain author prose and portable public citations."""
    _, body = parse_note(text, role)
    prose = re.sub(_record_pattern(role), "", body)
    if captured:
        _, marker, context = prose.partition(_SOURCE_CONTEXT_HEADING + "\n\n")
        if not marker:
            return ()
        context = context.partition("\n## ")[0]
        # Undo our own display escaping. Rendering reapplies it after rebasing.
        return tuple(unescape(re.sub(r"\\([\\`*_{}\[\]()#+!|~])", r"\1", line[2:]))
                     for line in context.splitlines() if line.startswith("> "))
    prose = re.sub(r"(?m)^#{1,6} .*\n", "", prose)
    prose = _CONTEXT_LINK.sub(_portable_context_link, prose)
    prose = re.sub(r"!?\[\[([^|\]\n]*)(?:\|([^\]\n]*))?\]\]",
                   lambda match: match[2] or match[1], prose)
    return tuple(" ".join(section.split()) for section in re.split(r"\n\s*\n", prose.strip())
                 if section.strip())


def render_registration(asset, role, record, *, narrative=()):
    template = Path(__file__).parents[1] / f"skills/equity-research-us/templates/{role}-registration.md"
    title = f"{record['id']} {record['identity']}"
    # One scalar per placeholder; quoted escapes protect metadata written by agents.
    context = {
        "title": _visible_text(title),
        "title_yaml": json.dumps(title, ensure_ascii=False),
        "asset_id_yaml": json.dumps(asset, ensure_ascii=False),
        f"{role}_id_yaml": json.dumps(record["id"], ensure_ascii=False),
        f"{role}_version_yaml": json.dumps(record["identity"], ensure_ascii=False),
        f"{role}_record": _dump(record).rstrip("\n"),
    }
    if role == "source":
        available = record.get("available_at")
        context["available_at_properties"] = "available_at: " + json.dumps(available) + "\n" if available else ""
        origin = record.get("origin_reference", record["raw_ref"])
        kind = _visible_text(record.get("kind", "source"))
        availability = _visible_text(available) if available else "not established"
        context["source_link_and_basis"] = (
            f"Use this captured {kind} to inspect the evidence as it was saved. "
            f"Recorded availability: {availability}.\n\n"
            f"[Local source](../raw/{quote(Path(record['raw_ref']).name)}) · Origin: {_visible_text(origin)}"
        )
        fiscal = record.get("fiscal", {})
        if isinstance(fiscal, dict) and fiscal.get("period_end"):
            context["source_link_and_basis"] += (
                f"\n\nReporting period ended {_visible_text(fiscal['period_end'])}."
            )
        if "original_ref" in record:
            context["source_link_and_basis"] += f"\n\n[Original filing](../raw/{quote(Path(record['original_ref']).name)})"
    else:
        origin = record.get("origin_reference", record["content_ref"])
        context["method_and_limits"] = (
            f"Use this captured {_visible_text(record.get('kind', 'method'))} to repeat the "
            "applied procedure or inspect its assumptions.\n\n"
            f"[Local method](../materials/{quote(Path(record['content_ref']).name)}) · Origin: {_visible_text(origin)}"
        )
        if record.get("authored_at"):
            context["method_and_limits"] += f"\n\nRecorded authorship: {_visible_text(record['authored_at'])}."
    if narrative:
        body_key = "source_link_and_basis" if role == "source" else "method_and_limits"
        quoted = "\n>\n".join(f"> {_render_context_paragraph(paragraph)}" for paragraph in narrative)
        context[body_key] += f"\n\n{_SOURCE_CONTEXT_HEADING}\n\n{quoted}"
    rendered = Template(template.read_text(encoding="utf-8")).substitute(context)
    parse_note(rendered, role + "-registration")
    return rendered


def render_review(asset, quarter, review):
    title = f"{asset} {quarter} Research review"
    props = dict(finance_schema=1, finance_role="review", title=title, asset_id=asset,
                 fiscal_quarter=quarter, as_of=review["cutoff"], review_id=review["id"],
                 status="complete" if review["publication"]["complete"] else "partial")
    if review.get("predecessor") is not None:
        props["predecessor"] = review["predecessor"]
    template = Path(__file__).parents[1] / "skills/equity-research-us/templates/review.md"
    return Template(template.read_text(encoding="utf-8")).substitute(
        title=title, properties=_dump(props), record=_dump(review))


def render_quarter_overview(asset, quarter, review, title, report_links, *, record_path=None):
    props = dict(finance_schema=1, finance_role="quarter-overview", title=title,
                 asset_id=asset, fiscal_quarter=quarter, as_of=review["cutoff"],
                 review_id=review["id"],
                 status="complete" if review["publication"]["complete"] else "partial")
    links = "\n".join(f"- [{label}]({path})" for label, path in report_links)
    if record_path is not None:
        props["research_record"] = record_path
        research = review["research"]
        horizons = research.get("horizons", {})
        conclusions = [
            f"**{label}**　{judgment}"
            for key, label in (("short", "短期"), ("medium", "中期"), ("long", "長期"))
            if isinstance(judgment := horizons.get(key, {}).get("judgment"), str)
            and judgment not in ("", "insufficient_evidence")
        ]
        gaps = []
        for key in ("gaps", "supplemental_gaps"):
            items = research.get(key, [])
            if not isinstance(items, list):
                items = [] if items is None else [items]
            for item in items:
                if isinstance(item, dict):
                    item = " · ".join(item[field].strip() for field in ("evidence", "reason", "recovery")
                                      if isinstance(item.get(field), str) and item[field].strip())
                gaps.append(item if isinstance(item, str) and item.strip()
                            else "有一項待補證據，詳細內容請見研究紀錄。")
        def list_items(items, empty):
            return "\n".join("- " + " ".join(item.split()) for item in items
                             if isinstance(item, str) and item.strip()) or empty
        return ("---\n" + _dump(props) + "---\n\n# " + title
                + "\n\n資料截至 " + review["cutoff"]
                + "\n\n## 本季判斷\n\n" + list_items(conclusions, "請參閱各分項的研究判斷。")
                + "\n\n## 分項研究\n\n" + links
                + "\n\n## 待補證據\n\n" + list_items(gaps, "本次未列出待補證據。")
                + f"\n\n[研究紀錄]({record_path})\n")
    research = review.get("research", {})
    changes = _visible_text(research.get("changes") or "No change summary was supplied.")
    gaps = "\n".join(f"- {_visible_text(gap)}" for gap in research.get("gaps", []))
    gaps = gaps or "No gaps were recorded."
    links = links or "No analysis reports have been saved for this quarter."
    return ("---\n" + _dump(props) + "---\n\n# " + _visible_text(title)
            + "\n\nUse this note to review changes at the saved cutoff, open the supporting analyses, "
            "and identify what needs more evidence."
            + "\n\n## What changed\n\n" + changes
            + "\n\n## Analysis reports\n\n" + links
            + "\n\n## Evidence gaps\n\n" + gaps
            + "\n\n## Research record\n\n```finance-quarter-overview\n"
            + _dump(review) + "```\n")
