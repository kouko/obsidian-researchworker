"""Obsidian properties and versioned Markdown records for the research pilot."""

from pathlib import Path
import re
from string import Template


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


def is_asset_entry(text):
    frontmatter = text.split("---", 2)
    return (len(frontmatter) >= 2 and frontmatter[0] == ""
            and re.search(r"(?m)^finance_role:\s*['\"]?asset-entry['\"]?([ \t]+#.*)?[ \t]*\r?$", frontmatter[1]) is not None)


def parse_note(text, role, **expected):
    match = re.fullmatch(r"---\r?\n(.*?)\r?\n---\r?\n(.*)", text, re.S)
    if not match:
        raise ValueError("missing YAML frontmatter")
    props, body = _mapping(match[1]), match[2]
    simple = (str, int, float, bool)
    if (type(props.get("finance_schema")) is not int or props["finance_schema"] != 1
            or props.get("finance_role") != role or not isinstance(props.get("title"), str)
            or not props["title"].strip() or not re.search(r"(?m)^# \S", body)
            or any(type(value) not in simple and (
                not isinstance(value, list) or not all(type(item) in simple for item in value))
                   for value in props.values())):
        raise ValueError("invalid Obsidian properties or missing note heading")
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
