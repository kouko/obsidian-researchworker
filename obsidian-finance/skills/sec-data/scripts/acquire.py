"""Acquire a source-linked, cutoff-aware SEC data package using stdlib only."""

import argparse
from collections import Counter, defaultdict
from datetime import date, datetime, timezone
import json
from pathlib import Path
import re
import sys
import tempfile

import sec_contact
from fiscal_quarter import conflicting_publication
from sec_client import acquire, normalize_cik

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
        return conflicting_publication(indexed.get(accession, []), filed)

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
    issuer = parser.add_mutually_exclusive_group(required=True)
    issuer.add_argument('--ticker')
    issuer.add_argument('--cik')
    parser.add_argument('--output-dir', required=True)
    for name in ('period-start', 'period-end', 'as-of', 'fiscal-quarter'):
        parser.add_argument('--' + name)
    run_path = None
    try:
        args = parser.parse_args(argv)
        mode = 'historical' if args.as_of is not None else 'retrospective'
        if args.fiscal_quarter is not None:
            if (not re.fullmatch(r'[0-9]{4}Q[1-4]', args.fiscal_quarter)
                    or args.period_start is not None or args.period_end is not None):
                raise ValueError('INVALID_INPUT: use YYYYQq without date-range selectors')
            if args.as_of is None:
                args.as_of = datetime.now(timezone.utc).date().isoformat()
            start = end = None
        else:
            start, end = map(_date, (args.period_start, args.period_end))
            if None in (start, end) or start > end or args.as_of is None:
                raise ValueError('INVALID_INPUT: date ranges require start, end and as-of')
        cutoff = _date(args.as_of)
        if cutoff is None or cutoff > datetime.now(timezone.utc).date():
            raise ValueError('INVALID_INPUT: use ISO dates, start <= end and a non-future cutoff')
        cik = normalize_cik(args.cik) if args.cik is not None else None
        if args.ticker is not None and not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9.-]{0,14}', args.ticker):
            raise ValueError('INVALID_INPUT: invalid ticker')
        contact = sec_contact.load()
        identity = f'{contact["name"]} {contact["email"]}'
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
        data = acquire(args.ticker, args.as_of, identity, fetch,
                       fiscal_quarter=args.fiscal_quarter, cik=cik)
        sources = []
        (run_path / 'raw').mkdir()
        for source in data['sources']:
            source = dict(source)
            raw = source.pop('raw_bytes')
            source.pop('payload')  # raw files are the authoritative payloads
            source['path'] = None
            if raw is not None:
                filename = f'raw/{source["id"]}.json'
                source_kind = source['id'].removeprefix('current-').removeprefix('predecessor-')
                if source_kind.startswith('primary-'):
                    filename = f'raw/{source["id"]}.html'
                if source_kind.startswith('archive-'):
                    (run_path / 'raw/archives').mkdir(exist_ok=True)
                    filename = f'raw/archives/{source["id"]}.json'
                with (run_path / filename).open('xb') as handle:
                    handle.write(raw)
                source['path'] = filename
            sources.append(source)
        valid_section = any(s['status'] == 'valid' and s['id'] in ('submissions', 'companyfacts') for s in sources)
        failed = not data['company'] or not data['identity_valid'] or not valid_section
        errors = list(data['errors'])
        resolution = data['resolution']
        if args.fiscal_quarter:
            if resolution is None:
                failed = True
                if not any(error['code'] == 'FISCAL_PERIOD_UNRESOLVED' for error in errors):
                    errors.append(dict(source='fiscal-quarter', code='FISCAL_PERIOD_UNRESOLVED',
                        detail='required primary filing unavailable; original fiscal period could not be verified'))
            else:
                start = end = _date(resolution['period_end'])
        eligible, inventory, coverage, malformed = ([], [], {}, False) if failed else _select(data, start, end, cutoff)
        errors.extend(coverage.get('filing_errors', []))
        if malformed:
            errors.append(dict(source='companyfacts', code='INVALID_SOURCE_DATA', detail='Malformed observation structure; invalid sections excluded'))
            if not eligible and not any(s['id'] == 'submissions' and s['status'] == 'valid' for s in sources):
                failed = True
        status = 'failed' if failed else 'partial' if errors else 'empty' if not eligible else 'complete'
        exit_code = {'failed': 1, 'partial': 2, 'empty': 3, 'complete': 0}[status]
        manifest = dict(schema_version=1, status=status, finalized=True,
            company=data['company'], identity_valid=data['identity_valid'],
            issuer_selection=data['issuer_selection'],
            request=dict(ticker=args.ticker.upper() if args.ticker is not None else None,
                         cik=cik, period_start=args.period_start,
                         period_end=args.period_end, as_of=args.as_of, fiscal_quarter=args.fiscal_quarter),
            mode=mode, effective_cutoff=args.as_of, resolution=resolution,
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
            mode=mode, effective_cutoff=args.as_of, resolution=resolution,
            company=data['company'], issuer_selection=data['issuer_selection'],
            manifest=str((run_path / 'manifest.json').resolve()),
            eligible_fact_count=len(eligible), filing_count=len(inventory), errors=errors,
            limitations=LIMITATIONS)
    except (OSError, ValueError, TypeError):
        # Never include exception messages: source content and operator contact
        # identity must not escape through an error string.
        return dict(status='failed', exit_code=1, run_path=str(run_path.resolve()),
                    error='OUTPUT_WRITE_FAILED: unfinished run; choose a writable new location and retry')


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    if argv in (['--setup-contact'], ['--setup-contact', '--terminal']):
        try:
            if '--terminal' in argv:
                payload = sec_contact.read_terminal(sys.stdin)
            else:
                try:
                    if sys.stdin is None or sys.stdin.isatty():
                        raise ValueError()
                    stream = getattr(sys.stdin, 'buffer', sys.stdin)
                    payload = stream.read(sec_contact.MAX_PROFILE + 1)
                except (OSError, ValueError):
                    raise ValueError(sec_contact.INPUT_UNAVAILABLE) from None
            sec_contact.save(sec_contact.parse(payload))
            summary = dict(status='configured', exit_code=0)
        except ValueError as exc:
            summary = dict(status='failed', exit_code=64, error=str(exc))
    else:
        summary = run(argv)
    print(json.dumps(summary, ensure_ascii=False))
    return summary['exit_code']


if __name__ == '__main__':
    sys.exit(main())
