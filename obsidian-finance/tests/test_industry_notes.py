from pathlib import Path
import sys

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from industry_notes import (
    identify_study,
    managed_body,
    note_link,
    note_path,
    parse_note,
    render_note,
    resolve_study,
)


@pytest.fixture
def vault(tmp_path):
    path = tmp_path / "My Vault"
    path.mkdir()
    (path / ".obsidian").mkdir()
    return path


@pytest.fixture
def study(vault):
    return identify_study(vault, "smartphones", name="全球智慧型手機市場", language="zh-TW")


def save(path, body):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(body, encoding="utf-8")


def quarter_note(study, body, **fields):
    return render_note(
        study, "overview", body, quarter="2024Q3", status="in-progress",
        as_of="2024-10-31T23:59:59-07:00", updated="2026-11-21", **fields,
    )


def test_vault_default_and_relative_override(vault):
    assert resolve_study(vault, "smartphones") == vault / "investing/industries/smartphones"
    assert resolve_study(vault, "phones", destination="research/phones") == vault / "research/phones"
    assert resolve_study(vault, "phones", destination=vault / "research/phones") == vault / "research/phones"
    assert not (vault / "investing").exists()


def test_missing_vault_traversal_and_symlink_escapes(vault, tmp_path):
    with pytest.raises(ValueError, match="vault"):
        resolve_study(tmp_path, "phones")
    with pytest.raises(ValueError):
        resolve_study(vault, "phones", destination="../outside")
    with pytest.raises(ValueError):
        resolve_study(vault, "phones", destination=vault / "research" / ".." / "phones")
    outside = tmp_path / "outside"
    outside.mkdir()
    (vault / "jump").symlink_to(outside, target_is_directory=True)
    with pytest.raises(ValueError):
        resolve_study(vault, "phones", destination="jump/phones")
    assert list(outside.iterdir()) == []


def test_unrelated_existing_destination_is_preserved(vault):
    foreign = vault / "research/phones"
    save(foreign / "personal.md", "My own note")
    with pytest.raises(ValueError, match="study"):
        identify_study(vault, "phones", name="Phones", destination=foreign)
    assert (foreign / "personal.md").read_text() == "My own note"


def test_localized_identity_does_not_change_on_resume(study):
    project = note_path(study, "project")
    save(project, render_note(study, "project", "Shared definitions"))
    resumed = identify_study(study.vault, "smartphones", name="Smartphones", language="en")
    assert resumed == study
    path = note_path(resumed, "overview", quarter="2024Q3")
    assert path.name == "2024Q3 全球智慧型手機市場-總覽.md"
    note = quarter_note(resumed, "Summary")
    assert "# 2024Q3 全球智慧型手機市場-總覽\n" in note
    assert 'as_of: "2024-10-31T23:59:59-07:00"' in note
    props = parse_note(note)
    assert props["type"] == "industry-overview"
    assert props["market"] == "smartphones"
    assert props["quarter"] == "2024Q3"
    assert props["updated"] == "2026-11-21"


def test_vault_links_and_company_identity(study):
    company = note_path(study, "company", quarter="2024Q3", company="aapl", company_name="Apple")
    with pytest.raises(ValueError, match="target"):
        note_link(study, company)
    assert note_link(study, company, planned=[company]) == (
        "[[investing/industries/smartphones/2024Q3/companies/2024Q3 全球智慧型手機市場-供應鏈-Apple]]"
    )
    save(company, render_note(
        study, "company", "Observation", quarter="2024Q3", company="aapl",
        company_name="Apple", status="in-progress", as_of="2024-10-31", updated="2026-11-21",
    ))
    assert note_path(study, "company", quarter="2024Q3", company="aapl") == company


def test_collision_and_unowned_note_fail_closed(study):
    path = note_path(study, "overview", quarter="2024Q3")
    alternate = path.with_name(path.name.replace("2024Q3", "2024q3"))
    save(alternate, "ordinary")
    with pytest.raises(ValueError, match="collision"):
        note_path(study, "overview", quarter="2024Q3")
    alternate.unlink()
    save(path, "ordinary")
    with pytest.raises(ValueError):
        note_path(study, "overview", quarter="2024Q3")
    assert path.read_text() == "ordinary"
    unicode = identify_study(study.vault, "other", name="Café", language="en")
    target = note_path(unicode, "overview", quarter="2024Q3")
    save(target.with_name(target.name.replace("é", "e\u0301")), "ordinary")
    with pytest.raises(ValueError, match="collision"):
        note_path(unicode, "overview", quarter="2024Q3")


def test_update_preserves_user_body_frontmatter_and_reports_type_conflict(study):
    note = quarter_note(study, "Earlier")
    note = note.replace('type: "industry-overview"\n', 'type: "industry-overview"\ntags:\n  - private\n')
    note += "\nMy handwritten analysis.\n"
    changed = quarter_note(study, "Updated", existing=note)
    assert "tags:\n  - private\n" in changed
    assert changed.endswith("\nMy handwritten analysis.\n")
    assert managed_body(changed) == "Updated"
    types = study.vault / ".obsidian/types.json"
    save(types, '{"types":{"as_of":"date"}}')
    with pytest.raises(ValueError, match="as_of"):
        quarter_note(study, "Updated", existing=note)
    assert types.read_text() == '{"types":{"as_of":"date"}}'
