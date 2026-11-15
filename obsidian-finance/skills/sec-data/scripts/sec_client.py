"""Independent SEC acquisition. See ../../../PROVENANCE.md for attribution.

fetch(url, headers) may be injected and returns JSON bytes; default transport
uses only the standard library. Returned payloads are unfiltered evidence.
"""

from datetime import date, datetime, timezone
import hashlib
import json
import re
import time
from urllib.error import HTTPError, URLError
from urllib.request import HTTPRedirectHandler, Request, build_opener

TICKERS = 'https://www.sec.gov/files/company_tickers.json'
BASE = 'https://data.sec.gov'


class _NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def _fetch(url, headers):
    with build_opener(_NoRedirect()).open(Request(url, headers=headers), timeout=30) as response:
        return response.read()


def _rows(block):
    if not isinstance(block, dict) or any(not isinstance(v, list) for v in block.values()):
        raise ValueError('filing columns must be arrays')
    count = max((len(v) for v in block.values()), default=0)
    if count and not {'accessionNumber', 'form', 'filingDate'} <= block.keys():
        raise ValueError('missing required filing columns')
    # Pad WITHIN each block, never concatenate short columns across pages.
    return [{k: v[i] if i < len(v) else None for k, v in block.items()}
            for i in range(count)]


def acquire(ticker, as_of, identity, fetch=None):
    """Return company, identity_valid, sources, filings, facts and errors.

    Each source has id/url/status/retrieved_at/payload/raw_bytes/sha256; errors carry
    source/code/detail. Filings retain SEC column names plus source_id.
    A mismatched issuer invalidates the entire result's analytical inputs.
    Input errors raise ValueError before any request. No files are written.
    """
    if not isinstance(identity, str) or not re.search(r'\S+@[^\s@]+\.[^\s@]+', identity) or any(c in identity for c in '\r\n'):
        raise ValueError('SEC_IDENTITY_REQUIRED: supply an identifying name and contact email')
    if not isinstance(ticker, str) or not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9.-]{0,14}', ticker):
        raise ValueError('INVALID_INPUT: invalid ticker')
    try:
        cutoff = date.fromisoformat(as_of)
        if cutoff > date.today():
            raise ValueError()
    except (ValueError, TypeError):
        raise ValueError('INVALID_INPUT: as_of must be a non-future ISO date') from None
    ticker = ticker.upper()
    result = dict(company=None, identity_valid=True, sources=[], filings=[], facts=None, errors=[])
    transport = fetch or _fetch

    def error(source, code, detail):
        source['status'] = 'error'
        result['errors'].append(dict(source=source['id'], code=code, detail=detail))

    def get(source_id, url, validate):
        source = dict(id=source_id, url=url, status='error', retrieved_at=None, payload=None, raw_bytes=None, sha256=None)
        result['sources'].append(source)
        # URLs are constructed here; remote archive names must pass the
        # issuer-specific filename rule below. Redirects are never followed.
        for attempt in range(3):
            try:
                time.sleep(0.11)
                raw = transport(url, {'User-Agent': identity, 'Accept': 'application/json'})
                if not isinstance(raw, bytes):
                    raise ValueError('transport must return JSON bytes')
                source['retrieved_at'] = datetime.now(timezone.utc).isoformat()
                source['raw_bytes'] = raw
                source['sha256'] = hashlib.sha256(raw).hexdigest()
                source['payload'] = json.loads(raw)
                validate(source['payload'])
                source['status'] = 'valid'
                return source['payload']
            except HTTPError as exc:
                retry = exc.code == 429 or 500 <= exc.code < 600
                code = 'RATE_LIMITED' if exc.code == 429 else 'HTTP_ERROR'
                detail = f'HTTP {exc.code}'
            except (OSError, URLError) as exc:
                retry, code, detail = True, 'SOURCE_UNAVAILABLE', type(exc).__name__
            except (ValueError, TypeError, KeyError, AttributeError):
                error(source, 'INVALID_SOURCE_DATA', 'Malformed or inconsistent SEC response')
                return None
            if not retry or attempt == 2:
                error(source, code, detail)
                return None
            time.sleep(2 ** attempt)

    def registry_valid(payload):
        if not isinstance(payload, dict) or not all(isinstance(v, dict) for v in payload.values()):
            raise ValueError()

    registry = get('tickers', TICKERS, registry_valid)
    if registry is None:
        return result
    entries = [v for v in registry.values() if v.get('ticker') == ticker]
    if len(entries) != 1:
        error(result['sources'][0], 'ISSUER_NOT_FOUND', 'Verify ticker in SEC registry')
        return result
    entry = entries[0]
    cik = entry.get('cik_str')
    if type(cik) is not int or not 0 < cik < 10 ** 10 or not isinstance(entry.get('title'), str):
        error(result['sources'][0], 'INVALID_SOURCE_DATA', 'Invalid registry identity')
        return result
    result['company'] = dict(ticker=ticker, cik=cik, name=entry['title'])

    def issuer(payload):
        if not isinstance(payload, dict):
            raise ValueError()
        value = payload.get('cik')
        if type(value) is not int and not (
            isinstance(value, str) and re.fullmatch(r'[0-9]{1,10}', value)
        ):
            raise ValueError()
        matches = int(value) == cik
        if not matches:
            result['identity_valid'] = False
            raise ValueError()

    def submissions_valid(payload):
        issuer(payload)
        if ticker not in payload.get('tickers', []):
            result['identity_valid'] = False
            raise ValueError()
        _rows(payload['filings']['recent'])
        if not isinstance(payload['filings']['files'], list):
            raise ValueError()

    submissions = get('submissions', f'{BASE}/submissions/CIK{cik:010d}.json', submissions_valid)
    if submissions is not None:
        result['filings'].extend(dict(row, source_id='submissions') for row in _rows(submissions['filings']['recent']))
        seen = set()
        for index, page in enumerate(submissions['filings']['files']):
            if isinstance(page, dict):
                try:
                    if date.fromisoformat(page.get('filingFrom')) > cutoff:
                        continue
                except (TypeError, ValueError):
                    pass
            name = page.get('name') if isinstance(page, dict) else None
            source_id = f'archive-{index}'
            if not isinstance(name, str) or not re.fullmatch(rf'CIK{cik:010d}-submissions-\d+\.json', name):
                source = dict(id=source_id, url=None, status='error', retrieved_at=None, payload=page, raw_bytes=None, sha256=None)
                result['sources'].append(source)
                error(source, 'INVALID_SOURCE_DATA', 'Invalid issuer-specific archive filename')
                continue
            if name in seen:
                continue
            seen.add(name)
            payload = get(source_id, f'{BASE}/submissions/{name}', _rows)
            if payload is not None:
                result['filings'].extend(dict(row, source_id=source_id) for row in _rows(payload))

    def facts_valid(payload):
        issuer(payload)
        if not isinstance(payload.get('facts'), dict) or not isinstance(payload.get('entityName'), str):
            raise ValueError()

    result['facts'] = get('companyfacts', f'{BASE}/api/xbrl/companyfacts/CIK{cik:010d}.json', facts_valid)
    if not result['identity_valid']:
        result['facts'] = None
        result['filings'] = []
        for e in result['errors']:
            if e['source'] in ('submissions', 'companyfacts') and e['code'] == 'INVALID_SOURCE_DATA':
                e['code'] = 'ISSUER_MISMATCH'
    return result
