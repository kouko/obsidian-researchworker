# concern: malformed fiscal provenance must not authorize new-quarter analysis.
import importlib.util
from pathlib import Path

ROOT = next(parent for parent in Path(__file__).resolve().parents
            if (parent / "obsidian-finance/scripts/work_assessment.py").is_file())
SPEC = importlib.util.spec_from_file_location("assessment_tests", ROOT / "obsidian-finance/tests/test_work_assessment.py")
helpers = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(helpers)


def test_fiscal_objectaccession_quarantines():
    """A JSON object is not an original accession identity."""
    data = helpers.snapshot()
    data["sources"].append(dict(id="q3", issuer="issuer", kind="financial_original",
        version="q3-original", projection={"revenue": 20}, available_at="2024-08-02",
        fiscal=dict(year=2024, period="Q3", period_end="2024-06-29",
                    original_accession={"unverified": True})))
    result = helpers.run(data)
    assert "create_next_quarter_analysis" not in helpers.actions(result)
    assert result["gaps"]
