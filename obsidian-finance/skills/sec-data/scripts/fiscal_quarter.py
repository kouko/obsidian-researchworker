"""Bind a fiscal quarter to primary-filing declarations, never calendar guesses."""

from datetime import date, datetime
from html.parser import HTMLParser
import re
from zoneinfo import ZoneInfo


ACCESSION = re.compile(r'[0-9]{10}-[0-9]{2}-[0-9]{6}')


class NoEligibleOriginal(ValueError):
    """No verified original is eligible for this filer and cutoff."""


class AmbiguousOriginal(ValueError):
    """More than one original satisfies the same fiscal request."""


class MalformedCompanyfacts(ValueError):
    """Malformed observations prevent ruling out an original."""


def _unresolved(detail):
    return ValueError('FISCAL_PERIOD_UNRESOLVED: ' + detail)


def _date(value):
    if not isinstance(value, str) or not re.fullmatch(r'[0-9]{4}-[0-9]{2}-[0-9]{2}', value):
        return None
    try:
        return date.fromisoformat(value)
    except ValueError:
        return None


def conflicting_publication(filings, filed):
    """Check every same-accession row, including evidence beyond the cutoff."""
    for filing in filings:
        if _date(filing.get('filingDate')) != filed:
            return True
        accepted = filing.get('acceptanceDateTime')
        if accepted:
            try:
                timestamp = datetime.fromisoformat(accepted.replace('Z', '+00:00'))
                # Official filing dates use Eastern time; earlier acceptance is
                # valid and does not establish intraday publication eligibility.
                if timestamp.tzinfo is None or timestamp.astimezone(ZoneInfo('America/New_York')).date() > filed:
                    return True
            except (ValueError, AttributeError, TypeError):
                return True
    return False


def candidates(data, quarter, cutoff):
    """Companyfacts focus only nominates documents with matching report endpoints."""
    selected, _, _ = _candidates(data, quarter, cutoff)
    return selected


def _candidates(data, quarter, cutoff):
    year, period = quarter[:4], 'FY' if quarter[-1] == '4' else quarter[4:]
    original_form = '10-K' if period == 'FY' else '10-Q'
    cutoff_date = _date(cutoff)
    nominations = {}
    malformed = False
    malformed_target = False
    for concepts in (data.get('facts') or {}).get('facts', {}).values():
        if not isinstance(concepts, dict):
            malformed = True
            continue
        for metadata in concepts.values():
            units = metadata.get('units') if isinstance(metadata, dict) else None
            if not isinstance(units, dict):
                malformed = True
                continue
            for rows in units.values():
                if not isinstance(rows, list):
                    malformed = True
                    continue
                for row in rows:
                    if not isinstance(row, dict):
                        malformed = True
                        continue
                    if str(row.get('fy')) == year and row.get('fp') == period:
                        accession, end = row.get('accn'), row.get('end')
                        if isinstance(accession, str) and ACCESSION.fullmatch(accession) and _date(end):
                            nominations.setdefault(accession, set()).add(end)
                        else:
                            filed = _date(row.get('filed'))
                            form = row.get('form')
                            if filed is not None and filed > cutoff_date:
                                continue
                            if isinstance(form, str) and form.strip() and form != original_form:
                                continue
                            malformed_target = True
    selected = {}
    nominated_ends = {end for ends in nominations.values() for end in ends}
    for row in data['filings']:
        filed = _date(row.get('filingDate'))
        accession, endpoint = row.get('accessionNumber'), row.get('reportDate')
        form = row.get('form')
        if filed is not None and filed > cutoff_date:
            continue
        if not isinstance(accession, str) or not ACCESSION.fullmatch(accession):
            if form == original_form and isinstance(endpoint, str) and endpoint in nominated_ends:
                raise _unresolved('invalid original filing accession for a nominated period')
            continue
        if accession not in nominations:
            continue
        if not isinstance(form, str) or not form.strip():
            raise _unresolved('invalid original filing form for a nominated accession')
        if form != original_form:
            continue
        report_end = _date(endpoint)
        if report_end is None:
            raise _unresolved('invalid report end for a nominated original filing')
        if endpoint not in nominations[accession]:
            continue
        if filed is None:
            raise _unresolved('invalid filing date for a nominated original filing')
        if filed < report_end:
            raise _unresolved('original filing date precedes its report end')
        document = row.get('primaryDocument')
        if (not isinstance(document, str)
                or not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_-]*\.(?:htm|html)', document)):
            raise _unresolved('invalid primary-document accession or basename')
        versions = [other for other in data['filings'] if other.get('accessionNumber') == accession]
        if conflicting_publication(versions, filed):
            raise _unresolved('conflicting original filing publication evidence')
        if any(other.get(k) != row.get(k) for other in versions
                for k in ('reportDate', 'primaryDocument', 'form')):
            raise _unresolved('conflicting original filing metadata')
        selected[accession] = row
    return list(selected.values()), malformed, malformed_target


class _Declarations(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.fields = {}
        self.active = None
        self.depth = 0

    def handle_starttag(self, tag, attrs):
        if self.active is not None:
            self.depth += 1
            return
        attrs = dict(attrs)
        name = attrs.get('name', '')
        if tag in ('ix:nonnumeric', 'ix:nonfraction') and name.startswith('dei:'):
            self.active = (name[4:], attrs, [])
            self.depth = 1

    def handle_data(self, value):
        if self.active is not None:
            self.active[2].append(value)

    def handle_endtag(self, tag):
        if self.active is not None:
            self.depth -= 1
            if self.depth == 0:
                name, attrs, text = self.active
                self.fields.setdefault(name, []).append((attrs, ' '.join(''.join(text).split())))
                self.active = None


def _declarations(html):
    parser = _Declarations()
    parser.feed(html)
    names = ('DocumentFiscalYearFocus', 'DocumentFiscalPeriodFocus',
             'DocumentPeriodEndDate', 'EntityCentralIndexKey')
    values, contexts = {}, set()
    for name in names:
        rows = parser.fields.get(name, [])
        if len(rows) != 1:
            raise _unresolved('missing or contradictory DEI declarations')
        attrs, value = rows[0]
        context = attrs.get('contextref')
        if not context or attrs.get('continuedat') or attrs.get('xsi:nil') in ('true', '1'):
            raise _unresolved('incomplete DEI context or declaration')
        contexts.add(context)
        transform = attrs.get('format')
        if name == 'DocumentPeriodEndDate' and transform:
            if transform.split(':')[-1] != 'date-monthname-day-year-en':
                raise _unresolved('unsupported period-end date transform')
            match = re.fullmatch(r'([A-Za-z]+) ([0-9]{1,2}), ([0-9]{4})', value)
            months = ('January February March April May June July August September October November December').split()
            if not match or match[1] not in months:
                raise _unresolved('invalid month-name period endpoint')
            value = f'{match[3]}-{months.index(match[1]) + 1:02d}-{int(match[2]):02d}'
        elif transform:
            raise _unresolved('unsupported DEI transform')
        values[name] = value
    if len(contexts) != 1:
        raise _unresolved('DEI declarations use different contexts')
    return values, sorted(contexts)


def resolve(data, quarter, cutoff):
    """Require one original filing whose source-bound DEI proves the quarter."""
    matches = []
    filings, malformed, malformed_target = _candidates(data, quarter, cutoff)
    if malformed_target:
        raise MalformedCompanyfacts('malformed Companyfacts evidence for the requested fiscal quarter')
    for filing in filings:
        accession = filing['accessionNumber']
        sources = [s for s in data['sources'] if s['id'] == 'primary-' + accession and s['status'] == 'valid']
        if len(sources) != 1:
            raise _unresolved('primary filing unavailable')
        source = sources[0]
        values, contexts = _declarations(source['payload'])
        cik = values['EntityCentralIndexKey']
        if not re.fullmatch(r'[0-9]{1,10}', cik) or int(cik) != data['company']['cik']:
            raise _unresolved('primary filing issuer mismatch')
        endpoint = values['DocumentPeriodEndDate']
        if not _date(endpoint) or endpoint != filing['reportDate']:
            raise _unresolved('primary declaration contradicts reportDate')
        if (values['DocumentFiscalYearFocus'] != quarter[:4]
                or values['DocumentFiscalPeriodFocus'] != ('FY' if quarter[-1] == '4' else quarter[4:])):
            continue
        matches.append(dict(fiscal_quarter=quarter, fiscal_year=int(quarter[:4]),
            quarter=int(quarter[-1]), period_end=endpoint, original_accession=accession,
            original_filing_date=filing['filingDate'], evidence=dict(
                source_id=source['id'], url=source['url'], sha256=source['sha256'],
                retrieved_at=source['retrieved_at'], contexts=contexts, declarations=values)))
    if not matches:
        if malformed:
            raise MalformedCompanyfacts('malformed Companyfacts structure prevents verifying original filing absence')
        raise NoEligibleOriginal('FISCAL_PERIOD_UNRESOLVED: no eligible source-declared original by the cutoff')
    if len(matches) > 1:
        raise AmbiguousOriginal('FISCAL_PERIOD_UNRESOLVED: multiple source-declared originals')
    return matches[0]
