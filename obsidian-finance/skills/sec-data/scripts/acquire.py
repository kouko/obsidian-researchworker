"""Acquire a source-linked, cutoff-aware SEC data package using stdlib only."""

import argparse
from collections import Counter, defaultdict
from datetime import date, datetime
import json
import os
from pathlib import Path
import re
import sys
import tempfile
from zoneinfo import ZoneInfo

from sec_client import acquire

LIMITATIONS = [
    'Raw endpoint responses are unfiltered latest-source evidence, not historical snapshots.',
    'The cutoff is an inclusive publication date; same-day intraday availability is not established.',
    'Observed concept/unit/period spans do not establish complete quarterly statements or twenty-year coverage.',
    'Companyfacts standard taxonomies do not establish complete custom segment or operating metric coverage.',
    'Annual, year-to-date and shorter observations retain their own durations; no quarterly arithmetic is performed.',
]


class _Parser(argparse.ArgumentParser):
    def error(self, message):
        raise ValueError('INVALID_INPUT: check required command arguments')


def _date(value):
    if not isinstance(value, str) or not re.fullmatch(r'\d{4}-\d{2}-\d{2}', value):
        return None
    try:
        return date.fromisoformat(value)
    except ValueError:
        return None


def _acceptance_date(value):
    if not isinstance(value, str):
        return None
    try:
        timestamp = datetime.fromisoformat(value.replace('Z', '+00:00'))
        # EDGAR filing dates use Eastern time. An explicit zone permits a
        # date comparison without making any claim of intraday eligibility.
        if timestamp.tzinfo is None:
            return None
        return timestamp.astimezone(ZoneInfo('America/New_York')).date()
    except ValueError:
        return None


def _source_url(cik, accession):
    if not isinstance(accession, str) or not re.fullmatch(r'[0-9]{10}-[0-9]{2}-[0-9]{6}', accession):
        return None
    return f'https://www.sec.gov/Archives/edgar/data/{cik}/{accession.replace("-", "")}/{accession}-index.html'


def _select(data, start, end, cutoff):
    """Preserve reported versions; quarantine contradictory publication evidence."""
    excluded = Counter()
    filing_excluded = Counter()
    inventory = []
    valid_filings = []
    filing_errors = {}
    indexed = defaultdict(list)
    cik = data['company']['cik']
    for row in data['filings']:
        accession = row.get('accessionNumber')
        if _source_url(cik, accession) is None:
            filing_excluded['invalid_accession'] += 1
            source = row['source_id']
            filing_errors[source] = dict(source=source, code='INVALID_SOURCE_DATA',
                detail='Malformed filing accession excluded from inventory')
            continue
        valid_filings.append(row)
        indexed[accession].append(row)

    def conflicting(accession, filed):
        for filing in indexed.get(accession, []):
            accepted = filing.get('acceptanceDateTime')
            if _date(filing.get('filingDate')) != filed:
                return True
            if accepted:
                accepted_date = _acceptance_date(accepted)
                if accepted_date is None or accepted_date > filed:
                    return True
        return False

    for row in valid_filings:
        accession = row.get('accessionNumber')
        if row.get('form') not in ('10-K', '10-Q', '10-K/A', '10-Q/A'):
            filing_excluded['other_form'] += 1
            continue
        filed = _date(row.get('filingDate'))
        if filed is None:
            filing_excluded['invalid_filed'] += 1
        elif filed > cutoff:
            filing_excluded['after_cutoff'] += 1
        elif conflicting(accession, filed):
            filing_excluded['conflicting_publication'] += 1
        else:
            inventory.append(dict(row, source_url=_source_url(cik, accession)))
    inventory_accessions = {row.get('accessionNumber') for row in inventory}
    facts_source = next((s for s in data['sources'] if s['id'] == 'companyfacts'), {})
    eligible = []
    malformed = False
    facts = (data['facts'] or {}).get('facts', {})
    for taxonomy, concepts in facts.items():
        if not isinstance(concepts, dict):
            malformed = True
            continue
        for concept, metadata in concepts.items():
            units = metadata.get('units') if isinstance(metadata, dict) else None
            if not isinstance(units, dict):
                malformed = True
                continue
            for unit, observations in units.items():
                if not isinstance(observations, list):
                    malformed = True
                    continue
                for row in observations:
                    if not isinstance(row, dict):
                        excluded['invalid_observation'] += 1
                        malformed = True
                        continue
                    filed, period_end = _date(row.get('filed')), _date(row.get('end'))
                    if filed is None:
                        excluded['invalid_filed'] += 1
                        continue
                    if period_end is None:
                        excluded['invalid_end'] += 1
                        continue
                    if 'start' in row and (_date(row['start']) is None or _date(row['start']) > period_end):
                        excluded['invalid_start'] += 1
                        continue
                    if filed > cutoff:
                        excluded['after_cutoff'] += 1
                        continue
                    if not start <= period_end <= end:
                        excluded['outside_period'] += 1
                        continue
                    accession = row.get('accn')
                    url = _source_url(cik, accession)
                    if url is None or type(row.get('val')) not in (int, float):
                        excluded['invalid_observation'] += 1
                        continue
                    if conflicting(accession, filed):
                        excluded['conflicting_publication'] += 1
                        continue
                    eligible.append(dict(row, taxonomy=taxonomy, concept=concept, unit=unit,
                        source_id='companyfacts', source_url=url,
                        retrieved_at=facts_source.get('retrieved_at'),
                        accession_in_inventory=accession in inventory_accessions))
    spans = {}
    for row in eligible:
        key = (row['taxonomy'], row['concept'], row['unit'])
        if key not in spans:
            spans[key] = dict(taxonomy=key[0], concept=key[1], unit=key[2],
                              earliest_end=row['end'], latest_end=row['end'], observation_count=0)
        span = spans[key]
        span['earliest_end'] = min(span['earliest_end'], row['end'])
        span['latest_end'] = max(span['latest_end'], row['end'])
        span['observation_count'] += 1
    coverage = dict(eligible_fact_count=len(eligible), filing_count=len(inventory),
        excluded=dict(excluded), filing_excluded=dict(filing_excluded),
        filing_errors=list(filing_errors.values()),
        observed_spans=list(spans.values()),
        absent_inventory_accession_count=sum(not row['accession_in_inventory'] for row in eligible),
        inventory_limitation='No matching filings acquired' if not inventory else None,
        limitations=LIMITATIONS)
    return eligible, inventory, coverage, malformed


def _write_json(path, value):
    with path.open('x', encoding='utf-8') as handle:
        json.dump(value, handle, ensure_ascii=False, indent=2, allow_nan=False)
        handle.write('\n')


def run(argv=None, fetch=None):
    """Return a JSON-ready summary, including exit_code; never log identity.

    argv is the same argument list accepted by the CLI. An injected
    fetch(url, headers) returns bytes and exercises the complete pipeline.
    The destination root must exist, or have an existing direct parent.
    """
    parser = _Parser(description=__doc__)
    for name in ('ticker', 'period-start', 'period-end', 'as-of', 'output-dir'):
        parser.add_argument('--' + name, required=True)
    run_path = None
    try:
        args = parser.parse_args(argv)
        start, end, cutoff = map(_date, (args.period_start, args.period_end, args.as_of))
        if None in (start, end, cutoff) or start > end or cutoff > date.today():
            raise ValueError('INVALID_INPUT: use ISO dates, start <= end and a non-future cutoff')
        if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9.-]{0,14}', args.ticker):
            raise ValueError('INVALID_INPUT: invalid ticker')
        identity = os.environ.get('SEC_USER_AGENT', '')
        if not re.search(r'\S+@[^\s@]+\.[^\s@]+', identity) or any(c in identity for c in '\r\n'):
            raise ValueError('SEC_IDENTITY_REQUIRED: set SEC_USER_AGENT to your identifying name and contact email')
        root = Path(args.output_dir).expanduser()
        if root.is_symlink() or not root.parent.is_dir():
            raise ValueError('OUTPUT_UNAVAILABLE: choose a directory with an existing parent')
        try:
            root.mkdir(exist_ok=True)
            if not root.is_dir():
                raise OSError()
            run_path = Path(tempfile.mkdtemp(prefix='sec-run-', dir=root))
        except OSError:
            raise ValueError('OUTPUT_UNAVAILABLE: choose a writable output directory') from None
    except ValueError as exc:
        return dict(status='failed', exit_code=64, error=str(exc), run_path=None)

    try:
        print('Acquiring public SEC submissions and companyfacts', file=sys.stderr)
        data = acquire(args.ticker, args.as_of, identity, fetch)
        sources = []
        (run_path / 'raw').mkdir()
        for source in data['sources']:
            source = dict(source)
            raw = source.pop('raw_bytes')
            source.pop('payload')  # raw files are the authoritative payloads
            source['path'] = None
            if raw is not None:
                filename = f'raw/{source["id"]}.json'
                if source['id'].startswith('archive-'):
                    (run_path / 'raw/archives').mkdir(exist_ok=True)
                    filename = f'raw/archives/{source["id"]}.json'
                with (run_path / filename).open('xb') as handle:
                    handle.write(raw)
                source['path'] = filename
            sources.append(source)
        valid_section = any(s['status'] == 'valid' and s['id'] in ('submissions', 'companyfacts') for s in sources)
        failed = not data['company'] or not data['identity_valid'] or not valid_section
        eligible, inventory, coverage, malformed = ([], [], {}, False) if failed else _select(data, start, end, cutoff)
        errors = list(data['errors'])
        errors.extend(coverage.get('filing_errors', []))
        if malformed:
            errors.append(dict(source='companyfacts', code='INVALID_SOURCE_DATA', detail='Malformed observation structure; invalid sections excluded'))
            if not eligible and not any(s['id'] == 'submissions' and s['status'] == 'valid' for s in sources):
                failed = True
        status = 'failed' if failed else 'partial' if errors else 'empty' if not eligible else 'complete'
        exit_code = {'failed': 1, 'partial': 2, 'empty': 3, 'complete': 0}[status]
        manifest = dict(schema_version=1, status=status, finalized=True,
            company=data['company'], identity_valid=data['identity_valid'],
            request=dict(ticker=args.ticker.upper(), period_start=args.period_start,
                         period_end=args.period_end, as_of=args.as_of),
            sources=sources, errors=errors, raw_evidence='unfiltered', limitations=LIMITATIONS,
            files={} if failed else dict(facts='eligible-facts.json', filings='filings.json', coverage='coverage.json'),
            guidance='Verify source errors and retry into a new run; review requested dates and observed coverage.')
        if not failed:
            _write_json(run_path / 'eligible-facts.json', eligible)
            _write_json(run_path / 'filings.json', inventory)
            _write_json(run_path / 'coverage.json', coverage)
        _write_json(run_path / 'manifest.json', manifest)
        if not failed:
            _write_json(run_path / 'completion.json', dict(status=status, manifest='manifest.json'))
        return dict(status=status, exit_code=exit_code, run_path=str(run_path.resolve()),
            manifest=str((run_path / 'manifest.json').resolve()),
            eligible_fact_count=len(eligible), filing_count=len(inventory), errors=errors,
            limitations=LIMITATIONS)
    except (OSError, ValueError, TypeError):
        # Never include exception messages: source content and operator contact
        # identity must not escape through an error string.
        return dict(status='failed', exit_code=1, run_path=str(run_path.resolve()),
                    error='OUTPUT_WRITE_FAILED: unfinished run; choose a writable new location and retry')


def main(argv=None):
    summary = run(argv)
    print(json.dumps(summary, ensure_ascii=False))
    return summary['exit_code']


if __name__ == '__main__':
    sys.exit(main())
