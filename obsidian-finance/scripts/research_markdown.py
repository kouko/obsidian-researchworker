"""Obsidian properties and versioned Markdown records for the research pilot."""

from datetime import date, datetime
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
    frontmatter = text.split("---", 2)
    return (len(frontmatter) >= 2 and frontmatter[0] == ""
            and re.search(r"(?m)^finance_role:\s*['\"]?" + re.escape(role) + r"['\"]?([ \t]+#.*)?[ \t]*\r?$", frontmatter[1]) is not None)


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


def record(text, role, **expected):
    props, body = parse_note(text, role, **expected)
    pattern = r"(?m)^## Research record\r?\n\r?\n\x60{3}finance-" + role + r"\r?\n([\s\S]*?)\r?\n\x60{3}\r?$"
    matches = re.findall(pattern, body)
    if len(matches) != 1:
        raise ValueError("expected one " + role + " record")
    return props, _mapping(matches[0])


def render_review(asset, quarter, review):
    yaml = _yaml()
    title = f"{asset} {quarter} Research review"
    props = dict(finance_schema=1, finance_role="review", title=title, asset_id=asset,
                 fiscal_quarter=quarter, as_of=review["cutoff"], review_id=review["id"],
                 status="complete" if review["publication"]["complete"] else "partial")
    if review.get("predecessor") is not None:
        props["predecessor"] = review["predecessor"]
    options = dict(sort_keys=False, allow_unicode=True)
    template = Path(__file__).parents[1] / "skills/finance-research/templates/review.md"
    return Template(template.read_text(encoding="utf-8")).substitute(
        title=title, properties=yaml.safe_dump(props, **options), record=yaml.safe_dump(review, **options))
