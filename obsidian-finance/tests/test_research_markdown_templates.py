"""Exercises bundled note templates and Obsidian property contracts."""

from pathlib import Path
import re
from string import Template

import pytest

from test_research_store import CUTOFF, load


ROLES = {
    "research-overview": (),
    "asset-entry": ("asset_id",),
    "quarter-navigation": ("asset_id", "fiscal_quarter"),
    "review": ("asset_id", "fiscal_quarter", "as_of", "review_id", "status"),
    "source-registration": ("asset_id", "source_id", "source_version"),
    "method-registration": ("asset_id", "method_id", "method_version"),
    **{role: ("asset_id", "fiscal_quarter", "as_of", "review_id", "status")
       for role in ("financial-analysis", "operating-analysis", "industry-and-competition",
                    "forward-forecast", "valuation-and-risk", "technical-analysis", "synthesis")},
}
TEMPLATES = Path(__file__).parents[1] / "skills/equity-research/templates"


def test_equity_skill_uses_fixed_quarter_publication_and_recovery():
    skill = (TEMPLATES.parent / "SKILL.md").read_text()
    assert skill.count('storage="quarterly"') == 2
    assert "run-directory/review.md" not in skill
    assert "recover_quarterly(root, asset_id, quarter)" in skill
    assert "2024Q3 AAPL Apple - 00 Research Overview.md" in skill


VALUES = {
    "title_yaml": '"Apple Research"',
    "asset_id_yaml": '"aapl"',
    "issuer_yaml": '"AAPL"',
    "question_id_yaml": '"finance"',
    "required_sources_yaml": '["filing-{fiscal}"]',
    "depends_on_yaml": "[]",
    "fiscal_quarter_yaml": '"2024Q2"',
    "as_of_yaml": f'"{CUTOFF}"',
    "review_id_yaml": '"q2-a"',
    "status_yaml": '"partial"',
    "source_id_yaml": '"filing-q2"',
    "source_version_yaml": '"q2-v1"',
    "method_id_yaml": '"comparison"',
    "method_version_yaml": '"comparison-v1"',
    "source_record": "version: 1",
    "method_record": "version: 1",
    "overview_record": "version: 1",
    "available_at_properties": "",
}


class SampleValues(dict):
    def __missing__(self, key):
        return "Sample content"


def _render(role, codec):
    if role == "review":
        return codec.render_review("aapl", "2024Q2", {
            "version": 1, "cutoff": CUTOFF, "id": "q2-a",
            "publication": {"complete": False},
        })
    return Template((TEMPLATES / f"{role}.md").read_text()).substitute(SampleValues(VALUES))


@pytest.mark.parametrize("role", ROLES)
def test_role_template_renders_required_flat_obsidian_properties(role):
    codec = load()._markdown
    note = _render(role, codec)
    props, _ = codec.parse_note(note, role)
    assert props["finance_schema"] == 1 and props["finance_role"] == role
    assert ("title" in props and set(ROLES[role]) <= props.keys())
    fields = ROLES[role] or ("title",)
    for missing in fields:
        without_property = re.sub(rf"(?m)^{missing}:.*\n", "", note, count=1)
        with pytest.raises(ValueError, match="invalid"):
            codec.parse_note(without_property, role)


@pytest.mark.parametrize("role, property_edit", [
    ("quarter-navigation", ('fiscal_quarter: "2024Q2"', 'fiscal_quarter: "FY2024"')),
    ("synthesis", (f'as_of: "{CUTOFF}"', 'as_of: "2024-08-31T12:00:00"')),
    ("source-registration", ('source_version: "q2-v1"', 'source_version: [v1]')),
    ("technical-analysis", ('status: "partial"', 'status: "unknown"')),
    ("review", ("title: aapl 2024Q2 Research review", "title:\n  nested: x")),
])
def test_role_template_rejects_invalid_obsidian_values(role, property_edit):
    codec = load()._markdown
    note = _render(role, codec)
    assert property_edit[0] in note
    with pytest.raises(ValueError, match="invalid"):
        codec.parse_note(note.replace(*property_edit, 1), role)


def test_review_render_round_trips_shared_source_data():
    shared = {"value": 124, "unit": "USD"}
    review = dict(id="r1", cutoff="2024-08-31T23:59:59+00:00", publication={"complete": False},
                  units={"financial": {"projection": shared}, "identity": {"projection": shared}})
    markdown = load()._markdown
    _, restored = markdown.record(markdown.render_review("aapl", "2024Q3", review), "review")
    assert restored == review
