# concern: contradictory filing publication evidence must not authorize fiscal-quarter resolution
"""Attack quarter resolution with source publication contradictions."""

from pathlib import Path
import sys

import pytest

ROOT = next(parent for parent in Path(__file__).resolve().parents
            if (parent / 'obsidian-finance/tests/test_acquire.py').is_file())
sys.path.insert(0, str(ROOT / 'obsidian-finance/tests'))
import test_acquire as helpers
from test_fiscal_quarter import declaration, evidence


@pytest.mark.parametrize('mode', ['future_acceptance', 'conflicting_future_duplicate'])
def test_quarter_conflictingpublication_unresolved(tmp_path, monkeypatch, mode):
    """Reject a quarter whose original filing has contradictory publication evidence."""
    data = helpers.payloads()
    sample = evidence()
    recent = {key: [value] for key, value in sample['filings'][0].items()}
    if mode == 'future_acceptance':
        recent['acceptanceDateTime'] = ['2025-01-01T15:00:00Z']
    else:
        for key, values in recent.items():
            values.append('2025-01-01' if key == 'filingDate' else values[0])
    data[1]['filings']['recent'] = recent
    observation = data[2]['facts']['us-gaap']['Revenues']['units']['USD'][0]
    observation.update(accn='0000320193-24-000081', filed='2024-08-02',
                       end='2024-06-29', fy=2024, fp='Q3')
    data.append(declaration().encode())
    summary, path, _ = helpers.execute(tmp_path, monkeypatch, data,
        selectors=['--fiscal-quarter', '2024Q3', '--as-of', '2024-12-31'])
    assert (summary['status'], summary['exit_code']) == ('failed', 1), summary
    assert any(error['code'] == 'FISCAL_PERIOD_UNRESOLVED' for error in summary['errors'])
    assert not (path / 'eligible-facts.json').exists()
    assert not (path / 'completion.json').exists()
