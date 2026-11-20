"""Independent SEC acquisition. See ../../../PROVENANCE.md for attribution.

fetch(url, headers) may be injected and returns JSON bytes; default transport
uses only the standard library. Returned payloads are unfiltered evidence.
"""

from datetime import date, datetime, timezone
import hashlib
import html as html_entities
from html.parser import HTMLParser
import json
import re
import time
from urllib.error import HTTPError, URLError
from urllib.request import HTTPRedirectHandler, Request, build_opener

TICKERS = 'https://www.sec.gov/files/company_tickers.json'
BASE = 'https://data.sec.gov'

# Each entry claims predecessor filings before its effective date. Competing
# entries for one successor overlap on the historical side.
ISSUER_TRANSITIONS = {
    2115436: (
        dict(predecessor_cik=34088, effective_date='2026-07-01',
             succession_url='https://www.sec.gov/Archives/edgar/data/2115436/000119312526291990/d71068d8k12b.htm',
             predecessor_filing_urls=[
                 'https://www.sec.gov/Archives/edgar/data/34088/000003408824000050/xom-20240630.htm',
                 'https://www.sec.gov/Archives/edgar/data/34088/000003408824000068/xom-20240930.htm',
             ]),
    ),
}


def normalize_cik(value):
    if isinstance(value, str) and re.fullmatch(r'[0-9]{1,10}', value):
        value = int(value)
    if type(value) is int and 0 < value < 10 ** 10:
        return value
    raise ValueError('INVALID_INPUT: CIK must be one to ten digits and greater than zero')


class _NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def _fetch(url, headers):
    headers = dict(headers, **{'User-Agent': headers['User-Agent'].encode('utf-8')})
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


def _acquire_filer(ticker, as_of, identity, fetch=None, *, fiscal_quarter=None, cik=None):
    """Return company, identity_valid, sources, filings, facts and errors.

    Each source has id/url/status/retrieved_at/payload/raw_bytes/sha256; errors carry
    source/code/detail. Filings retain SEC column names plus source_id.
    A mismatched issuer invalidates the entire result's analytical inputs.
    Input errors raise ValueError before any request. No files are written.
    """
    if not isinstance(identity, str) or not re.search(r'\S+@[^\s@]+\.[^\s@]+', identity) or any(c in identity for c in '\r\n'):
        raise ValueError('SEC_IDENTITY_REQUIRED: supply an identifying name and contact email')
    if (ticker is None) == (cik is None):
        raise ValueError('INVALID_INPUT: supply either ticker or CIK')
    if cik is not None:
        cik = normalize_cik(cik)
    elif not isinstance(ticker, str) or not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9.-]{0,14}', ticker):
        raise ValueError('INVALID_INPUT: invalid ticker')
    if fiscal_quarter is not None and (not isinstance(fiscal_quarter, str)
            or not re.fullmatch(r'[0-9]{4}Q[1-4]', fiscal_quarter)):
        raise ValueError('INVALID_INPUT: fiscal quarter must be YYYYQq')
    try:
        cutoff = date.fromisoformat(as_of)
        if cutoff > datetime.now(timezone.utc).date():
            raise ValueError()
    except (ValueError, TypeError):
        raise ValueError('INVALID_INPUT: as_of must be a non-future ISO date') from None
    ticker = ticker.upper() if ticker is not None else None
    result = dict(company=None, identity_valid=True, sources=[], filings=[], facts=None, errors=[],
                  resolution=None, issuer_selection=None)
    transport = fetch or _fetch
    name, _, email = identity.rpartition(' ')
    bounded_name = rf'(?<!\w){re.escape(name)}(?!\w)'
    phrase = re.compile(bounded_name, re.IGNORECASE) if ' ' in name else None
    token = re.compile(bounded_name) if len(name) > 1 and phrase is None else None
    folded_name, folded_email = name.casefold(), email.casefold()
    if len(name) == 1:
        quoted_name = re.compile('|'.join(re.escape(json.dumps(name, ensure_ascii=ascii_only))
                                         for ascii_only in (False, True)), re.IGNORECASE)
    else:
        quoted_name = None

    def reflects_contact(text, *, decoded_field=False):
        text = html_entities.unescape(text)
        folded = text.casefold()
        return (bool(folded_email and folded_email in folded)
                or bool(folded_name and folded.strip() == folded_name)
                or bool(phrase and phrase.search(text))
                or bool(decoded_field and token and token.search(text)))

    class _ContactInHtml(HTMLParser):
        found = False

        def handle_data(self, data):
            self.found = self.found or reflects_contact(data, decoded_field=True)

        handle_comment = handle_data
        handle_decl = handle_data
        handle_pi = handle_data
        unknown_decl = handle_data

        def handle_starttag(self, tag, attrs):
            self.found = self.found or any(
                value and reflects_contact(value, decoded_field=True) for _, value in attrs)

    def payload_reflects_contact(value):
        pending = [value]
        while pending:
            item = pending.pop()
            if isinstance(item, str) and reflects_contact(item, decoded_field=True):
                return True
            if isinstance(item, list):
                pending.extend(item)
            if isinstance(item, dict):
                pending.extend(item)
                pending.extend(item.values())
        return False

    def error(source, code, detail):
        source['status'] = 'error'
        result['errors'].append(dict(source=source['id'], code=code, detail=detail))

    def get(source_id, url, validate, *, html=False):
        source = dict(id=source_id, url=url, status='error', retrieved_at=None, payload=None, raw_bytes=None, sha256=None)
        result['sources'].append(source)
        # URLs are constructed here; remote archive names must pass the
        # issuer-specific filename rule below. Redirects are never followed.
        for attempt in range(3):
            try:
                time.sleep(0.11)
                raw = transport(url, {'User-Agent': identity, 'Accept': 'text/html' if html else 'application/json'})
                if not isinstance(raw, bytes):
                    raise ValueError('transport must return JSON bytes')
                source['retrieved_at'] = datetime.now(timezone.utc).isoformat()
                raw_text = raw.decode('utf-8', errors='replace')
                if reflects_contact(raw_text):
                    error(source, 'CONTACT_REFLECTED', 'Response withheld because it reflected operator contact')
                    return None
                try:
                    payload = raw.decode('utf-8') if html else json.loads(raw)
                except ValueError:
                    if (reflects_contact(raw_text, decoded_field=True)
                            or (quoted_name and quoted_name.search(raw_text))):
                        error(source, 'CONTACT_REFLECTED', 'Response withheld because it reflected operator contact')
                        return None
                    # Preserve malformed source evidence after checking the response text.
                    source['raw_bytes'] = raw
                    source['sha256'] = hashlib.sha256(raw).hexdigest()
                    raise
                if html:
                    scanner = _ContactInHtml()
                    try:
                        scanner.feed(payload)
                        scanner.close()
                        reflected = scanner.found
                    except AssertionError:
                        # HTMLParser can reject an unknown marked section.
                        reflected = scanner.found or reflects_contact(raw_text, decoded_field=True)
                else:
                    reflected = payload_reflects_contact(payload)
                if reflected:
                    error(source, 'CONTACT_REFLECTED', 'Response withheld because it reflected operator contact')
                    return None
                source['raw_bytes'] = raw
                source['sha256'] = hashlib.sha256(raw).hexdigest()
                source['payload'] = payload
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

    if ticker is not None:
        registry = get('tickers', TICKERS, registry_valid)
        if registry is None:
            return result
        entries = [v for v in registry.values() if v.get('ticker') == ticker]
        if len(entries) != 1:
            detail = 'Verify ticker in SEC registry or select the filer explicitly with --cik'
            error(result['sources'][0], 'ISSUER_NOT_FOUND', detail)
            return result
        entry = entries[0]
        cik = entry.get('cik_str')
        if type(cik) is not int or not 0 < cik < 10 ** 10 or not isinstance(entry.get('title'), str):
            error(result['sources'][0], 'INVALID_SOURCE_DATA', 'Invalid registry identity')
            return result
        company_name = entry['title']
    else:
        company_name = None
    result['company'] = dict(ticker=ticker, cik=cik, name=company_name)
    result['issuer_selection'] = dict(method='ticker_registry' if ticker is not None else 'explicit_cik', cik=cik)

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
        if ticker is not None and ticker not in payload.get('tickers', []):
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
    if company_name is None:
        submissions_name = (submissions or {}).get('name')
        result['company']['name'] = (submissions_name if isinstance(submissions_name, str)
                                     else (result['facts'] or {}).get('entityName'))
    if not result['identity_valid']:
        result['facts'] = None
        result['filings'] = []
        for e in result['errors']:
            if e['source'] in ('submissions', 'companyfacts') and e['code'] == 'INVALID_SOURCE_DATA':
                e['code'] = 'ISSUER_MISMATCH'
    elif fiscal_quarter:
        from fiscal_quarter import candidates
        try:
            for row in candidates(result, fiscal_quarter, as_of):
                accession = row['accessionNumber']
                url = (f'https://www.sec.gov/Archives/edgar/data/{cik}/'
                       f'{accession.replace("-", "")}/{row["primaryDocument"]}')
                get('primary-' + accession, url, lambda value: None, html=True)
        except ValueError as exc:
            result['errors'].append(dict(source='fiscal-quarter', code='FISCAL_PERIOD_UNRESOLVED', detail=str(exc)))
    return result


def _unresolved(result, detail):
    result['errors'].append(dict(source='fiscal-quarter', code='FISCAL_PERIOD_UNRESOLVED', detail=detail))


def _resolve_quarter(result, quarter, as_of, *, automatic):
    """Return True only when trustworthy sources establish a clean miss."""
    from fiscal_quarter import AmbiguousOriginal, NoEligibleOriginal, resolve

    if not result['company'] or not result['identity_valid']:
        _unresolved(result, 'trustworthy issuer data unavailable')
        return False
    if any(error['code'] == 'FISCAL_PERIOD_UNRESOLVED' or error['source'].startswith('primary-')
           for error in result['errors']):
        return False
    try:
        result['resolution'] = resolve(result, quarter, as_of)
    except NoEligibleOriginal:
        if not result['errors']:
            return True
        _unresolved(result, 'required issuer source unavailable; original fiscal period could not be verified')
    except AmbiguousOriginal as exc:
        guidance = '; select the filer explicitly with --cik' if automatic else ''
        _unresolved(result, str(exc) + guidance)
    except ValueError as exc:
        _unresolved(result, str(exc))
    return False


def acquire(ticker, as_of, identity, fetch=None, *, fiscal_quarter=None, cik=None):
    """Acquire an explicit SEC CIK or resolve a ticker and its documented predecessor."""
    result = _acquire_filer(ticker, as_of, identity, fetch, fiscal_quarter=fiscal_quarter, cik=cik)
    if fiscal_quarter is None:
        return result

    automatic = ticker is not None
    original_absent = _resolve_quarter(result, fiscal_quarter, as_of, automatic=automatic)
    if not result['company']:
        return result
    current_cik = result['company']['cik']
    transitions = ISSUER_TRANSITIONS.get(current_cik, ()) if automatic else ()
    resolution = result['resolution']
    manual = '; select the filer explicitly with --cik'
    if resolution:
        if any(resolution['period_end'] < entry['effective_date'] for entry in transitions):
            result['resolution'] = None
            _unresolved(result, 'current filer original conflicts with documented succession' + manual)
        return result
    if not original_absent:
        return result
    if len(transitions) != 1:
        detail = 'no eligible source-declared original by the cutoff'
        if automatic:
            detail += '; missing or ambiguous succession evidence' + manual
        _unresolved(result, detail)
        return result

    transition = transitions[0]
    predecessor_cik = transition['predecessor_cik']
    predecessor = _acquire_filer(None, as_of, identity, fetch, fiscal_quarter=fiscal_quarter, cik=predecessor_cik)
    predecessor['issuer_selection'] = None
    predecessor_absent = _resolve_quarter(predecessor, fiscal_quarter, as_of, automatic=True)
    resolution = predecessor['resolution']
    if resolution and predecessor['errors']:
        predecessor['resolution'] = None
        _unresolved(predecessor, 'required predecessor source unavailable; original fiscal period could not be verified')
    elif resolution and max(resolution['period_end'], resolution['original_filing_date']) >= transition['effective_date']:
        predecessor['resolution'] = None
        _unresolved(predecessor, 'original is at or beyond the succession boundary' + manual)
    elif resolution:
        predecessor['company']['ticker'] = ticker.upper()
        predecessor['issuer_selection'] = dict(method='documented_predecessor', cik=predecessor_cik,
                                               current_cik=current_cik, transition=transition)
    elif predecessor_absent:
        _unresolved(predecessor, 'documented predecessor has no eligible source-declared original by the cutoff' + manual)

    # Keep the current issuer's evidence distinct from the predecessor files
    # used for the analytical package.
    predecessor['sources'][:0] = [
        source if source['id'] == 'tickers' else dict(source, id='current-' + source['id'])
        for source in result['sources']
    ]
    return predecessor
