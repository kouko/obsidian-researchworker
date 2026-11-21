"""Obsidian properties and versioned Markdown records for the research pilot."""

from datetime import date, datetime
import json
from pathlib import Path
import re
from string import Template


ANALYSIS_ROLES = frozenset({
    "financial-analysis", "operating-analysis", "industry-and-competition",
    "forward-forecast", "valuation-and-risk", "technical-analysis", "synthesis",
})
_RUN_FIELDS = ("asset_id", "fiscal_quarter", "as_of", "review_id", "status")
_ROLE_FIELDS = {
    "research-overview": (),
    "asset-entry": ("asset_id",),
    "quarter-navigation": ("asset_id", "fiscal_quarter"),
    "review": _RUN_FIELDS,
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
    if role in ANALYSIS_ROLES or role == "review":
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
    key = r"""(?:finance_role|'finance_role'|"finance_role")"""
    position = r"(?:^|[,{])[ \t]*" + key + r"[ \t]*:"
    if not header.lstrip().startswith("{") and not re.search(position, header, re.M):
        return False
    try:
        return _mapping(header).get("finance_role") == role
    except ValueError:
        # A recognizable declaration must still reach record validation when
        # the surrounding YAML is malformed or the YAML dependency is absent.
        value = re.escape(role)
        marker = rf"""{position}[ \t]*(?:{value}|'{value}'|"{value}")(?=[ \t]*(?:[,}}]|#|$))"""
        return bool(re.search(marker, header, re.M))


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
    pattern = r"(?m)^## Research record\r?\n\r?\n\x60{3}finance-" + role + r"\r?\n([\s\S]*?)\r?\n\x60{3}\r?$"
    matches = re.findall(pattern, body)
    if len(matches) != 1:
        raise ValueError("expected one " + role + " record")
    return props, _mapping(matches[0])


def _dump(record):
    yaml = _yaml()

    class Dumper(yaml.SafeDumper):
        def ignore_aliases(self, data):
            return True

    return yaml.dump(record, sort_keys=False, allow_unicode=True, Dumper=Dumper)


def render_registration(asset, role, record):
    template = Path(__file__).parents[1] / f"skills/finance-research/templates/{role}-registration.md"
    title = f"{record['id']} {record['identity']}"
    # One scalar per placeholder; quoted escapes protect metadata written by agents.
    context = {
        "title": title.replace("\n", " "),
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
        context["source_link_and_basis"] = f"[Local source](../raw/{Path(record['raw_ref']).name})\n\nOrigin: {origin}"
        if "original_ref" in record:
            context["source_link_and_basis"] += f"\n\n[Original filing](../raw/{Path(record['original_ref']).name})"
    else:
        origin = record.get("origin_reference", record["content_ref"])
        context["method_and_limits"] = f"[Local method](../materials/{Path(record['content_ref']).name})\n\nOrigin: {origin}"
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
    template = Path(__file__).parents[1] / "skills/finance-research/templates/review.md"
    return Template(template.read_text(encoding="utf-8")).substitute(
        title=title, properties=_dump(props), record=_dump(review))
