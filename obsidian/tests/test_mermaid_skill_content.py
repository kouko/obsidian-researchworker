"""Content guard: the Mermaid skill targets Obsidian 1.15 (Pele engine).

String checks over SKILL.md and the two cross-type files. They catch a
regression to the retired Mermaid 11.4.1 baseline and re-prohibition of
patterns the new engine fixed; they do not check rendering.
"""

import re
from pathlib import Path

SKILL = Path(__file__).parent.parent / "skills/obsidian-mermaid-visualizer"
FILES = ["SKILL.md", "obsidian-compatibility.md", "obsidian-common-quirks.md"]


def _text(name: str) -> str:
    return (SKILL / name).read_text(encoding="utf-8")


def _all() -> str:
    return "\n".join(_text(n) for n in FILES)


def test_still_broken_patterns_listed():
    quirks = _text("obsidian-common-quirks.md")
    for needle in [
        "style A,B",                 # comma style list -> orphan node
        "A[Call API (v2)]",          # unquoted ASCII parens
        "9:00 : ",                   # timeline time-like text
        "branch 開發",               # gitGraph CJK branch
        "subgraph Core Process",     # bare subgraph name
        "usecase",                   # usecase-beta CJK actor id
        "db:R --> L:server",         # architecture edge form
    ]:
        assert needle in quirks, needle


def test_fixed_patterns_not_prohibited():
    text = _all()
    for banned in [
        "Unsupported markdown: list",
        "❌ [1. Perception]",
        "Does **not** work unquoted",
        "Use v2 (`stateDiagram-v2`) not v1",
    ]:
        assert banned not in text, banned


def test_states_obsidian_1_15():
    for name in FILES:
        text = _text(name)
        assert "Obsidian 1.15" in text, name
    assert "Pele" in _text("obsidian-compatibility.md")
    assert "12.1.0" in _text("obsidian-compatibility.md")


def test_no_11_4_baseline_claim():
    for name in FILES:
        assert not re.search(r"11\.4\.1|11\.5\+", _text(name)), name
    assert "stroke-width: 0" not in _all()
