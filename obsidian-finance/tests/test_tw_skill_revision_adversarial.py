# concern: Taiwan skill wording must not keep an in-note revision history (2026-11-25-tw-skill-revision-wording)
import re
from pathlib import Path

import test_tw_equity_workflow as workflow_tests

SKILL_FILE = Path(__file__).resolve().parents[1] / "skills/tw-equity-research/SKILL.md"
NEGATIONS = ("不", "無須", "毋須", "勿", "免", "沒有", "非")
CORRECTION = "原值、原始來源及當時判斷"
AFFIRMATIVE = ("寫明", "記錄", "保留", "列出")
IN_NOTE_HISTORY = re.compile(r"同一份(報告|筆記)(內|中)?保存前一版|修訂(紀錄|記錄|歷程|歷史)|變更(紀錄|記錄)")


def _sentences(text):
    return [s for s in re.split(r"[。\n]", text) if s.strip()]


def _affirms(text, literal):
    for sentence in _sentences(text):
        if literal not in sentence:
            continue
        head = sentence[: sentence.index(literal)]
        if any(verb in head for verb in AFFIRMATIVE) and not any(n in sentence for n in NEGATIONS):
            return True
    return False


def test_affirms_selfcheck_affirmative_accepted():
    """An affirmative correction sentence is accepted."""
    assert _affirms("並在正文寫明更正內容的原值、原始來源及當時判斷。", CORRECTION)


def test_affirms_selfcheck_negated_rejected():
    """A negated correction sentence is rejected."""
    assert not _affirms("更正時不需寫明原值、原始來源及當時判斷。", CORRECTION)


def test_skill_correction_sentence_affirmed():
    """The correction instruction affirmatively requires original value, source and judgement."""
    assert _affirms(SKILL_FILE.read_text(), CORRECTION)


def test_skill_whole_text_no_in_note_history():
    """No sentence asks the agent to keep a prior version or revision log inside the note."""
    hits = [s for s in _sentences(SKILL_FILE.read_text()) if IN_NOTE_HISTORY.search(s)]
    assert hits == []


def test_existing_pin_negated_correction_fails(monkeypatch, tmp_path):
    """The shipped pin must turn RED when the correction sentence is negated."""
    text = SKILL_FILE.read_text().replace("並在正文寫明更正內容的", "且正文不需寫明更正內容的")
    fake = tmp_path / "skill"
    fake.mkdir()
    (fake / "SKILL.md").write_text(text)
    monkeypatch.setattr(workflow_tests, "SKILL", fake)
    try:
        workflow_tests.test_skill_drops_in_note_dated_revision_record()
    except AssertionError:
        return
    raise AssertionError("existing pin passed on a negated correction sentence")
