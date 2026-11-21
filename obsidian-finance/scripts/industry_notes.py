"""Resolve and render the Obsidian notes of a quarterly industry study."""

from dataclasses import dataclass
from datetime import date
import json
from pathlib import Path
import re
import unicodedata

from market_evidence import _parse_time


_START = "<!-- industry-research:start -->"
_END = "<!-- industry-research:end -->"
_SUFFIXES = {
    "en": (" Overview", "Overview", "Size and Market Share", "Supply Chain", "Guidance and Outlook"),
    "ja": ("の概要", "概要", "規模と市場シェア", "サプライチェーン", "ガイダンスと見通し"),
    "zh-TW": ("總覽", "總覽", "規模與市佔率", "供應鏈", "指引與展望"),
}
_ROLES = ("project", "overview", "size-share", "supply-chain", "outlook")
_FIELDS = {
    "type", "market", "market_name", "language", "quarter", "status",
    "as_of", "updated", "company",
}
_STATUSES = {"draft", "in-progress", "completed", "partial", "complete"}


@dataclass(frozen=True)
class Study:
    vault: Path
    path: Path
    identifier: str
    name: str
    language: str


def _identifier(value):
    if not isinstance(value, str) or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", value):
        raise ValueError("Expected a stable lowercase identifier")
    return value


def _fold(text):
    return unicodedata.normalize("NFC", text).casefold()


def _component(name):
    if (
        not isinstance(name, str) or not name or name != name.strip()
        or name in {".", ".."} or name.endswith(".")
        or any(ord(char) < 32 or char in '/\\:<>|?*"#^[]' for char in name)
    ):
        raise ValueError(f"Unsafe vault path component: {name!r}")
    return name


def _child(parent, name, *, directory):
    _component(name)
    child = parent / name
    if parent.exists():
        matches = [entry.name for entry in parent.iterdir() if _fold(entry.name) == _fold(name)]
        if matches and matches != [name]:
            raise ValueError(f"Filename collision at {child}: {', '.join(matches)}")
    if child.is_symlink() or (
        child.exists() and not (child.is_dir() if directory else child.is_file())
    ):
        raise ValueError(f"Unsafe or unexpected vault path: {child}")
    return child


def _vault_root(vault):
    try:
        root = Path(vault).resolve(strict=True)
    except (OSError, RuntimeError) as error:
        raise ValueError("An existing Obsidian vault is required") from error
    marker = root / ".obsidian"
    if not marker.is_dir() or marker.is_symlink():
        raise ValueError("An existing Obsidian vault with a local .obsidian folder is required")
    return root


def _inside(vault, path, *, directory):
    candidate = Path(path)
    if not candidate.is_absolute():
        candidate = vault / candidate
    try:
        parts = candidate.relative_to(vault).parts
    except ValueError as error:
        raise ValueError("Destination is outside the selected Obsidian vault") from error
    if not parts or parts[0].startswith(".") or ".." in parts:
        raise ValueError("Expected an ordinary path within the selected Obsidian vault")
    current = vault
    for index, name in enumerate(parts):
        current = _child(current, name, directory=directory or index < len(parts) - 1)
    return current


def resolve_study(vault, study_id, *, destination=None):
    """Resolve a proposed vault-local study directory without writing."""
    root = _vault_root(vault)
    study_id = _identifier(study_id)
    target = destination if destination is not None else Path("investing/industries") / study_id
    return _inside(root, target, directory=True)


def _header(text):
    lines = text.splitlines(keepends=True)
    if not lines or lines[0].rstrip("\r\n") != "---":
        raise ValueError("Missing Obsidian frontmatter")
    for index, line in enumerate(lines[1:], 1):
        if line.rstrip("\r\n") == "---":
            return lines[:index + 1], "".join(lines[index + 1:])
    raise ValueError("Unclosed Obsidian frontmatter")


def _field(line):
    match = re.match(r"""^([a-z_][a-z0-9_]*|'[a-z_][a-z0-9_]*'|"[a-z_][a-z0-9_]*")\s*:(.*)$""", line)
    if match:
        return match[1].strip("'\""), match[2].strip()
    return None, None


def parse_note(text):
    """Read the flat fields owned by this skill; leave user YAML untouched."""
    header, _ = _header(text)
    result = {}
    for index, line in enumerate(header[1:-1], 1):
        key, value = _field(line)
        if key not in _FIELDS:
            continue
        if key in result:
            raise ValueError(f"Duplicate managed property: {key}")
        if not value or header[index + 1].startswith((" ", "\t")):
            raise ValueError(f"Expected a flat text property: {key}")
        if value.startswith('"'):
            try:
                value = json.loads(value)
            except ValueError as error:
                raise ValueError(f"Invalid managed property: {key}") from error
        elif value.startswith("'") and value.endswith("'"):
            value = value[1:-1].replace("''", "'")
        elif (
            key == "as_of" or value[0] in "[{>|&*!?"
            or re.fullmatch(r"true|false|null|~|[+-]?[0-9]+(?:\.[0-9]+)?", value, re.I)
        ):
            raise ValueError(f"Invalid managed property: {key}")
        if not isinstance(value, str) or not value:
            raise ValueError(f"Invalid managed property: {key}")
        result[key] = value
    note_type = result.get("type", "")
    if note_type in {f"industry-{role}" for role in (*_ROLES, "company")}:
        _identifier(result.get("market"))
        if note_type == "industry-project":
            _component(result.get("market_name"))
            if result.get("language") not in _SUFFIXES:
                raise ValueError("Invalid industry naming language")
        else:
            if not re.fullmatch(r"[0-9]{4}Q[1-4]", result.get("quarter", "")):
                raise ValueError("Invalid industry calendar quarter")
            if result.get("status") not in _STATUSES:
                raise ValueError("Invalid industry research status")
            _parse_time(result.get("as_of"))
            _date(result.get("updated"))
            if note_type == "industry-company":
                _identifier(result.get("company"))
    return result


def _notes(directory, role):
    if not directory.exists():
        return
    for path in sorted(directory.iterdir()):
        if path.suffix != ".md" or not path.is_file() or path.is_symlink():
            continue
        try:
            text = path.read_bytes().decode("utf-8")
        except UnicodeDecodeError:
            continue
        if not text.startswith(("---\n", "---\r\n")):
            continue
        try:
            props = parse_note(text)
        except ValueError:
            # A malformed industry note must not disappear from discovery.
            opening = text.splitlines()[1:]
            if "---" in opening:
                opening = opening[:opening.index("---")]
            if any(f"industry-{role}" in line for line in opening):
                raise
            continue
        if props.get("type") == f"industry-{role}":
            yield path, props


def identify_study(vault, study_id, *, name=None, language=None, destination=None):
    """Recover established display metadata, or establish it for a new study."""
    root = _vault_root(vault)
    path = resolve_study(root, study_id, destination=destination)
    entries = list(_notes(path, "project"))
    if entries:
        if len(entries) != 1 or entries[0][1].get("market") != study_id:
            raise ValueError(f"Ambiguous industry study at {path}")
        entry, properties = entries[0]
        name, language = properties.get("market_name"), properties.get("language")
    elif path.exists() and any(path.iterdir()):
        raise ValueError(f"Existing destination has no matching industry study: {path}")
    else:
        entry = None
        language = language or "en"
    _component(name)
    if language not in _SUFFIXES:
        raise ValueError("Naming language must be en, ja, or zh-TW")
    study = Study(root, path, study_id, name, language)
    if entry is not None and note_path(study, "project") != entry:
        raise ValueError(f"Industry study overview does not match its recorded title: {entry}")
    return study


def _role_dir(study, role, quarter, company):
    if role == "project":
        if quarter is not None or company is not None:
            raise ValueError("Project overview has neither a quarter nor a company")
        return _inside(study.vault, study.path, directory=True)
    if role not in (*_ROLES, "company"):
        raise ValueError("Unknown industry note role")
    if not isinstance(quarter, str) or not re.fullmatch(r"[0-9]{4}Q[1-4]", quarter):
        raise ValueError("Expected a calendar quarter in YYYYQn format")
    path = study.path / quarter
    if role == "company":
        _identifier(company)
        path /= "companies"
    elif company is not None:
        raise ValueError("Company identifiers belong on company notes")
    return _inside(study.vault, path, directory=True)


def note_path(study, role, *, quarter=None, company=None, company_name=None):
    directory = _role_dir(study, role, quarter, company)
    entries = [
        path for path, props in _notes(directory, role)
        if props.get("market") == study.identifier and props.get("quarter") == quarter
        and props.get("company") == company
    ]
    if len(entries) > 1:
        raise ValueError(f"Ambiguous industry note identity for {role}: {directory}")
    suffixes = _SUFFIXES[study.language]
    if role == "project":
        title = study.name + suffixes[0]
    elif role == "company":
        prefix = f"{quarter} {study.name}-{suffixes[3]}-"
        if entries:
            if not entries[0].stem.startswith(prefix):
                raise ValueError(f"Company note does not match its recorded title: {entries[0]}")
            company_name = entries[0].stem[len(prefix):]
        title = prefix + _component(company_name or company)
    else:
        title = f"{quarter} {study.name}-{suffixes[_ROLES.index(role)]}"
    candidate = _child(directory, title + ".md", directory=False)
    if (entries and entries[0] != candidate) or (candidate.exists() and not entries):
        raise ValueError(f"Path is occupied or disagrees with the industry note identity: {candidate}")
    return candidate


def note_link(study, target, *, planned=()):
    target = _inside(study.vault, target, directory=False)
    if target.suffix != ".md" or (not target.is_file() and target not in planned):
        raise ValueError(f"No existing or planned note link target: {target}")
    return f"[[{target.relative_to(study.vault).with_suffix('').as_posix()}]]"


def _managed_region(body):
    start = list(re.finditer(r"^" + re.escape(_START) + r"\r?\n", body, re.M))
    end = list(re.finditer(r"^" + re.escape(_END) + r"(?=\r?$)", body, re.M))
    if len(start) != 1 or len(end) != 1 or start[0].end() > end[0].start():
        raise ValueError("Missing or ambiguous managed industry note region")
    return start[0].end(), end[0].start()


def managed_body(text):
    _, body = _header(text)
    start, end = _managed_region(body)
    return body[start:end].rstrip("\r\n")


def _check_property_types(vault, props):
    path = vault / ".obsidian/types.json"
    if path.is_symlink():
        raise ValueError("Vault property types must be a local file")
    if not path.exists():
        return
    try:
        configured = json.loads(path.read_text(encoding="utf-8"))["types"]
    except (KeyError, TypeError, OSError, ValueError) as error:
        raise ValueError("Could not verify vault property types") from error
    if not isinstance(configured, dict):
        raise ValueError("Could not verify vault property types")
    for key in props:
        expected = "date" if key == "updated" else "text"
        if key in configured and configured[key] != expected:
            raise ValueError(f"Vault property {key} is incompatible with {expected}")


def _date(value):
    if not isinstance(value, str) or not re.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2}", value):
        raise ValueError("Updated date must be YYYY-MM-DD")
    date.fromisoformat(value)
    return value


def render_note(study, role, body, *, quarter=None, status=None, as_of=None,
                updated=None, company=None, company_name=None, existing=None):
    """Render a new note or replace just the owned fields and body region."""
    title = note_path(study, role, quarter=quarter, company=company, company_name=company_name).stem
    if not isinstance(body, str) or _START in body or _END in body:
        raise ValueError("Managed industry note body contains invalid content")
    properties = {"type": f"industry-{role}", "market": study.identifier}
    if role == "project":
        properties.update(market_name=study.name, language=study.language)
    else:
        if status not in _STATUSES:
            raise ValueError("Unknown industry research status")
        _parse_time(as_of)
        properties.update(quarter=quarter, status=status, as_of=as_of, updated=_date(updated))
    if company is not None:
        properties["company"] = company
    _check_property_types(study.vault, properties)
    if existing is None:
        header = ["---\n", "---\n"]
        original_body = f"# {title}\n\n{_START}\n{_END}\n"
    else:
        header, original_body = _header(existing)
        parsed = parse_note(existing)
        identity = ("type", "market", "market_name", "language", "quarter", "company")
        if any(parsed.get(field) != properties.get(field) for field in identity):
            raise ValueError("Existing note has a different industry identity")
        heading = re.search(r"^# (.+?)\r?$", original_body, re.M)
        if heading is None or heading[1] != title:
            raise ValueError("Existing heading conflicts with its industry title")
    newline = "\r\n" if header[0].endswith("\r\n") else "\n"
    owned = {
        key: f"{key}: {value if key == 'updated' else json.dumps(value, ensure_ascii=False)}{newline}"
        for key, value in properties.items()
    }
    preserved = []
    for line in header[1:-1]:
        key, _ = _field(line)
        preserved.append(owned.pop(key, line))
    start, end = _managed_region(original_body)
    replacement = body.rstrip("\r\n") + newline
    return "".join([header[0], *preserved, *owned.values(), header[-1],
                    original_body[:start], replacement, original_body[end:]])
