import importlib
from pathlib import Path
import sys

import pytest

sys.path.insert(0, str(Path(__file__).parents[1] / 'skills/equity-research/scripts'))


def declaration(period='Q3', end='2024-06-29'):
    return ''.join(f'<ix:nonNumeric name="dei:{name}" contextRef="c-1">{value}</ix:nonNumeric>'
        for name, value in [('DocumentFiscalYearFocus', '2024'),
            ('DocumentFiscalPeriodFocus', period), ('DocumentPeriodEndDate', end),
            ('EntityCentralIndexKey', '0000320193')])


def evidence(period='Q3', end='2024-06-29'):
    return dict(company={'cik': 320193}, filings=[dict(accessionNumber='0000320193-24-000081',
        form='10-K' if period == 'FY' else '10-Q', filingDate='2024-08-02',
        reportDate=end, primaryDocument='aapl.htm')], facts={'facts': {'us-gaap': {'Revenue': {
            'units': {'USD': [dict(accn='0000320193-24-000081', end=end, fy=2024,
                fp=period)]}}}}}, sources=[dict(id='primary-0000320193-24-000081',
                    payload=declaration(period, end), status='valid', url='https://www.sec.gov/doc',
                    sha256='hash', retrieved_at='2026-11-15T00:00:00Z')])


@pytest.mark.parametrize('quarter,period', [('2024Q3', 'Q3'), ('2024Q4', 'FY')])
def test_declared_fiscal_quarter(quarter, period):
    mod = importlib.import_module('fiscal_quarter')
    data = evidence(period)
    assert len(mod.candidates(data, quarter, '2024-12-31')) == 1
    result = mod.resolve(data, quarter, '2024-12-31')
    assert result['period_end'] == '2024-06-29'
    assert result['original_accession'] == '0000320193-24-000081'
    assert result['evidence']['sha256'] == 'hash'
    assert result['fiscal_quarter'] == quarter


@pytest.mark.parametrize('mode', ['comparative', 'context', 'identity', 'date',
    'unsupported_transform', 'duplicate', 'future', 'amendment'])
def test_unresolved_period(mode):
    mod = importlib.import_module('fiscal_quarter')
    data = evidence()
    if mode == 'comparative':
        data['filings'][0]['reportDate'] = '2024-09-28'
    elif mode == 'context':
        data['sources'][0]['payload'] = declaration().replace('contextRef="c-1"', 'contextRef="other"', 1)
    elif mode == 'identity':
        data['sources'][0]['payload'] = declaration().replace('0000320193', '0000000001')
    elif mode == 'date':
        data['sources'][0]['payload'] = declaration(end='2024-06-30')
    elif mode == 'unsupported_transform':
        data['sources'][0]['payload'] = declaration().replace('name="dei:DocumentPeriodEndDate"',
            'name="dei:DocumentPeriodEndDate" format="ixt:unknown"')
    elif mode == 'duplicate':
        data['sources'][0]['payload'] += declaration(end='2024-06-30')
    elif mode == 'future':
        data['filings'][0]['filingDate'] = '2025-01-01'
    else:
        data['filings'][0]['form'] = '10-Q/A'
    with pytest.raises(ValueError, match='FISCAL_PERIOD_UNRESOLVED'):
        mod.resolve(data, '2024Q3', '2024-12-31')
