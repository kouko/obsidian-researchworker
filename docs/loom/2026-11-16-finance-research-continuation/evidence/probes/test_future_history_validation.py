# concern: future-only selection must not conceal malformed or incomplete saved research.
"""Exercise the future-only exemption using real disposable folder records."""
import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[5] / 'obsidian-finance/tests'))
from test_research_continuation import two_issuers
from test_research_store import load, put


@pytest.mark.parametrize('state', ['malformed-analysis', 'missing-check'])
def test_futurehistory_malformed_rejected(tmp_path, state):
    """Keep real future-history defects visible without changing any old bytes."""
    assets = two_issuers(tmp_path)
    directory = 'investing/assets/equities/' + assets[0] + '/cycles/2024Q2/2024-08-01-r1'
    ref = directory + '/review.json'
    saved = json.loads((tmp_path / ref).read_text())
    if state == 'malformed-analysis':
        saved['units']['credit']['analysis_inputs'] = {'bad-method': 7}
        put(tmp_path, ref, saved)
    else:
        (tmp_path / saved['units']['credit']['verification']).unlink()
    before = {p: p.read_bytes() for p in tmp_path.rglob('*') if p.is_file()}
    result = load().discover(tmp_path, 'latest', '2024-05-01T23:59:59+00:00')
    assert {p: p.read_bytes() for p in tmp_path.rglob('*') if p.is_file()} == before
    assert result['status'] == 'partial'
    assert any('/cycles/2024Q2' in str(g['record']) for g in result['gaps'])
