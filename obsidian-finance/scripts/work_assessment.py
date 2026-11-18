"""Pure offline assessment of normalized prototype-v1 snapshots.

assess(snapshot, mode, cutoff) accepts JSON-compatible data, never paths to read.
snapshot = {version: 1, sources: [...], records: [...]}.
Sources: unique id, issuer, kind, version, projection (relevant values INCLUDING
units), available_at (ISO aware timestamp or date, interpreted as end of day in
the cutoff timezone), optional consumers. Financial-original sources also need
fiscal {year, period: Q1..Q4, period_end: ISO date, original_accession}.
Records: unique id, issuer, fiscal, cutoff, required_sources [source ids], work.
Work: unique id, status (complete or missing), depends_on [work ids], consumed
{source id: {version, projection}}, output {content: str, digest: SHA256 hex},
completion_evidence (nonempty local verification reference). Output content and
projection must be supplied by a bounded adapter; filenames alone prove nothing.
Optional execution_state, last_attempt and last_success are reported unchanged.
Unknown metadata including mtime/fetch time is not analytical evidence. The
adapter validates structure and references; this core rejects invalid request
parameters, unsupported versions and duplicate identities rather than guessing.
Results use stable sorted decisions/gaps/exclusions/reusable work, and always
declare supplied-local scope and unverified external freshness. No execution,
source authenticity, arbitrary selectors or external freshness is inferred.
"""

from datetime import date, datetime, time
from hashlib import sha256
import json


def _instant(value):
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        raise ValueError("cutoff requires timezone")
    return parsed


def _fiscal(value):
    if not isinstance(value, dict):
        return False
    try:
        date.fromisoformat(value["period_end"])
        return (type(value["year"]) is int and value["period"] in ("Q1", "Q2", "Q3", "Q4")
                and isinstance(value["original_accession"], str)
                and bool(value["original_accession"].strip()))
    except (KeyError, TypeError, ValueError):
        return False


def _indexed(items):
    result = {item["id"]: item for item in items}
    if len(result) != len(items):
        raise ValueError("duplicate identity")
    return result


def _same_json(left, right):
    """Compare JSON recursively, preserving booleans but allowing 1 == 1.0."""
    if isinstance(left, bool) or isinstance(right, bool):
        return type(left) is type(right) and left == right
    if isinstance(left, dict) and isinstance(right, dict):
        return left.keys() == right.keys() and all(_same_json(left[key], right[key]) for key in left)
    if isinstance(left, list) and isinstance(right, list):
        return len(left) == len(right) and all(_same_json(a, b) for a, b in zip(left, right))
    return left == right


def assess(snapshot, mode, cutoff):
    """Return deterministic necessary work, retaining independent evidence gaps."""
    if mode not in ("historical", "latest"):
        raise ValueError("mode must be historical or latest")
    boundary = _instant(cutoff)
    if snapshot.get("version") != 1:
        raise ValueError("Unsupported assessment input version")
    records = _indexed(snapshot["records"])
    sources = _indexed(snapshot["sources"])
    result = dict(version=1, scope="supplied_local_evidence", external_freshness="unverified",
                  mode=mode, cutoff=cutoff, decisions=[], gaps=[], excluded=[], reusable=[], observations=[])

    def gap(record, evidence, reason):
        result["gaps"].append(dict(record=record, evidence=evidence, reason=reason,
                                   recovery="Supply or verify the identified local evidence and retry"))

    def decision(record, action, work, evidence, reason, affected):
        result["decisions"].append(dict(record=record, action=action, work=work,
            evidence=sorted(evidence), reason=reason, affected=sorted(affected)))

    eligible = {}
    incomplete_candidates = {}
    for sid, source in sorted(sources.items()):
        try:
            value = source.get("available_at")
            available = (datetime.combine(date.fromisoformat(value), time(23, 59, 59), boundary.tzinfo)
                         if len(value) == 10 else _instant(value))
            reason = "after_cutoff" if available > boundary else None
        except (TypeError, ValueError, AttributeError):
            reason = "unverified_availability"
        if reason:
            result["excluded"].append(dict(evidence=sid, reason=reason))
        elif source.get("version") and "projection" in source:
            eligible[sid] = source
        else:
            missing = ([] if source.get("version") else ["version"]) + ([] if "projection" in source else ["projection"])
            incomplete_candidates[sid] = "Time-eligible source lacks " + ", ".join(missing)

    if not records:
        gap(None, "records", "No research records supplied")

    def quarter_identity(item):
        fiscal = item["fiscal"]
        return item["issuer"], fiscal["year"], fiscal["period"], fiscal["period_end"]

    represented = {quarter_identity(record) for record in records.values()
                   if _fiscal(record.get("fiscal"))}
    proposed = set()
    quarter_evidence = {}
    for sid, source in sorted(eligible.items()):
        if (source.get("kind") == "financial_original" and _fiscal(source.get("fiscal"))
                and source["fiscal"]["period_end"] <= source["available_at"][:10]):
            quarter_evidence.setdefault(quarter_identity(source), []).append(sid)
    for rid, record in sorted(records.items()):
        if mode == "historical" and _instant(record["cutoff"]) != boundary:
            raise ValueError("historical cutoff must match saved record cutoff")
        start = len(result["decisions"])
        gaps_start = len(result["gaps"])
        for sid, reason in incomplete_candidates.items():
            if sources[sid].get("issuer") == record["issuer"]:
                gap(rid, sid, reason)
        for excluded in result["excluded"]:
            if (excluded["reason"] == "unverified_availability" and
                    sources[excluded["evidence"]].get("issuer") == record["issuer"]):
                gap(rid, excluded["evidence"], "Source availability cannot be verified at cutoff")
        for key in ("execution_state", "last_attempt", "last_success"):
            if key in record:
                result["observations"].append(dict(record=rid, field=key, value=record[key]))
        if record.get("execution_state"):
            gap(rid, "execution_state", "Inspect saved execution metadata; no claim acquired or cleared")
        for sid in sorted(set(record["required_sources"])):
            if sid not in eligible or eligible[sid].get("issuer") != record["issuer"]:
                gap(rid, sid, "Required source missing, inconsistent or ineligible")
        if not _fiscal(record.get("fiscal")):
            gap(rid, "fiscal", "Saved source-declared fiscal identity is incomplete")
        for sid, source in sorted(eligible.items()):
            if source.get("issuer") != record["issuer"] or source.get("kind") != "financial_original":
                continue
            fiscal = source.get("fiscal")
            if not _fiscal(fiscal):
                gap(rid, sid, "Source-declared fiscal identity is incomplete")
            elif fiscal["period_end"] > source["available_at"][:10]:
                gap(rid, sid, "Fiscal period ends after declared publication")
            elif (_fiscal(record.get("fiscal")) and
                  (fiscal["year"], fiscal["period"]) == (record["fiscal"]["year"], record["fiscal"]["period"]) and
                  fiscal["period_end"] != record["fiscal"]["period_end"]):
                gap(rid, sid, "Contradictory fiscal period end for saved quarter")
            elif _fiscal(record.get("fiscal")) and (fiscal["year"], fiscal["period"]) > (record["fiscal"]["year"], record["fiscal"]["period"]):
                target = quarter_identity(source)
                if target not in represented and target not in proposed:
                    proposed.add(target)
                    decision(rid, "create_next_quarter_analysis", None, quarter_evidence[target],
                             "Eligible source declares an unrepresented later fiscal quarter", ["financial-analysis", "business-analysis", "forecast", "valuation", "synthesis"])

        work = _indexed(record["work"])
        if not work:
            gap(rid, "work", "No work completion evidence supplied")
        valid, reasons, changed = {}, {}, {}
        for wid, item in sorted(work.items()):
            consumed = item.get("consumed", {})
            expected = set(consumed) | {sid for sid in record["required_sources"]
                                       if wid in sources.get(sid, {}).get("consumers", [])}
            changed[wid] = []
            reasons[wid] = []
            for sid in sorted(expected):
                current = eligible.get(sid)
                if not current or current.get("issuer") != record["issuer"] or sid not in consumed:
                    reasons[wid].append("Missing eligible dependency or consumed identity: " + sid)
                elif not _same_json(consumed[sid], {k: current[k] for k in ("version", "projection")}):
                    changed[wid].append(sid)
            output = item.get("output", {})
            content = output.get("content")
            output_ok = (isinstance(content, str) and bool(content) and
                         output.get("digest") == sha256(content.encode()).hexdigest())
            if item.get("status") == "complete" and (not output_ok or not item.get("completion_evidence")):
                reasons[wid].append("Missing or mismatched output content or completion evidence")
            valid[wid] = item.get("status") == "complete" and not reasons[wid] and not changed[wid]
        # A saved cycle cannot prove any member's prerequisite completion.
        def cyclic(wid, trail):
            if wid in trail:
                return True
            return any(cyclic(dep, trail | {wid}) for dep in work.get(wid, {}).get("depends_on", []))

        for wid in work:
            if cyclic(wid, set()):
                valid[wid] = False
                reasons[wid].append("Cyclic prerequisite evidence cannot verify completion")
        # Conservative fixed point: a missing/changed prerequisite invalidates consumers.
        for _ in work:
            for wid, item in sorted(work.items()):
                if any(not valid.get(dep, False) for dep in item.get("depends_on", [])):
                    valid[wid] = False
        for wid, item in sorted(work.items()):
            if valid[wid]:
                result["reusable"].append(dict(record=rid, work=wid))
                continue
            dependencies = list(item.get("consumed", {})) + item.get("depends_on", [])
            if reasons[wid]:
                gap(rid, wid, "; ".join(reasons[wid]))
            action = ("append_revision_same_quarter" if changed[wid] else
                      "invalidate_dependent_checkpoint_and_recompute" if item.get("status") == "complete" else
                      "resume_incomplete_work")
            decision(rid, action, wid, dependencies or [wid],
                     "; ".join(reasons[wid]) or ("Relevant consumed inputs changed" if changed[wid] else
                     "Work or prerequisites are incomplete"), [wid])
        if len(result["gaps"]) > gaps_start:
            decision(rid, "record_gap_and_continue_independent_work", None,
                     [g["evidence"] for g in result["gaps"][gaps_start:]], "Evidence requires recovery", [])
        elif len(result["decisions"]) == start:
            decision(rid, "no_analysis_update", None, list(record["required_sources"]) or [rid],
                     "Completed outputs and relevant dependencies agree within supplied evidence", [])
    for key in ("decisions", "gaps", "excluded", "reusable", "observations"):
        unique = {json.dumps(item, sort_keys=True): item for item in result[key]}
        result[key] = [unique[key] for key in sorted(unique)]
    result["status"] = "partial" if result["gaps"] else "complete"
    return result
