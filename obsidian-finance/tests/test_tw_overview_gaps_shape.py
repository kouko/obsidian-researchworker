# concern: merge regression - US gap rendering runs before the Taiwan branch and crashes on gap shapes Taiwan (6a78dcf) tolerated
import importlib.util
from pathlib import Path

import pytest

_SCRIPT = Path(__file__).resolve().parents[2] / "obsidian-finance/scripts/research_markdown.py"


def _markdown():
    spec = importlib.util.spec_from_file_location("probe_research_markdown", _SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.mark.parametrize("gaps", [None, 5])
def test_render_quarter_overview_taiwan_non_list_gaps_renders_overview(gaps):
    """A Taiwan overview (record_path set) renders its gap section when gaps is not a list, as at 6a78dcf."""
    review = dict(cutoff="2026-05-01T00:00:00Z", id="r1", publication=dict(complete=False),
                  research=dict(gaps=gaps))
    text = _markdown().render_quarter_overview("2330.TW", "2026Q1", review, "T", [],
                                               record_path="data/reviews/x.json")
    assert "## 待補證據" in text
    assert "[研究紀錄](data/reviews/x.json)" in text
