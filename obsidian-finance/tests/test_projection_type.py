# concern: JSON boolean versus numeric dependency changes must invalidate reuse.
import importlib.util
from pathlib import Path

ROOT = next(parent for parent in Path(__file__).resolve().parents
            if (parent / "obsidian-finance/scripts/work_assessment.py").is_file())
SPEC = importlib.util.spec_from_file_location("assessment_tests", ROOT / "obsidian-finance/tests/test_work_assessment.py")
helpers = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(helpers)


def test_projection_typechange_invalidates():
    """Preserve JSON value types when comparing relevant source projections."""
    data = helpers.snapshot()
    data["sources"][0]["projection"]["value"] = True
    data["records"][0]["work"][0]["consumed"]["price"]["projection"]["value"] = 1
    result = helpers.run(data)
    assert result["reusable"] == []
    assert "no_analysis_update" not in helpers.actions(result)
