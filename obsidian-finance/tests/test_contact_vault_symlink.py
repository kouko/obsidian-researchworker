# concern: a redirected config directory writes operator contact into an Obsidian vault
import json
from pathlib import Path
import subprocess
import sys
import pytest


@pytest.mark.parametrize("ancestor", [False, True])
def test_config_directory_symlink_does_not_store_contact_in_vault(tmp_path, monkeypatch, ancestor):
    monkeypatch.setenv('HOME', str(tmp_path))
    vault = tmp_path / 'vault'
    (vault / '.obsidian').mkdir(parents=True)
    config = tmp_path / '.config'
    if ancestor:
        config.symlink_to(vault, target_is_directory=True)
    else:
        config.mkdir()
        (config / 'obsidian-finance').symlink_to(vault, target_is_directory=True)
    script = Path(__file__).resolve().parents[1] / 'skills/equity-research/scripts/acquire.py'
    result = subprocess.run(
        [sys.executable, str(script), '--setup-contact'],
        input=json.dumps({'name': 'Operator Probe', 'email': 'operator@example.invalid'}),
        text=True, capture_output=True, timeout=10, check=False,
    )
    assert list(vault.iterdir()) == [vault / '.obsidian']
    assert result.returncode != 0
    assert 'SEC_CONTACT_SAVE_FAILED' in result.stdout
