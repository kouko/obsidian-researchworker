# concern: oversized fragmented terminal input re-enabling echo before the contact line ends
import json
import os
from pathlib import Path
import pty
import select
import subprocess
import sys


def test_oversized_terminal_line_stays_hidden_through_its_end(tmp_path, monkeypatch):
    monkeypatch.setenv('HOME', str(tmp_path))
    script = Path(__file__).resolve().parents[1] / 'skills/sec-data/scripts/acquire.py'
    command = [sys.executable, str(script), '--setup-contact']
    original = {'name': 'Original Operator', 'email': 'original@example.invalid'}
    subprocess.run(command, input=json.dumps(original).encode(), capture_output=True, check=True)
    profile = tmp_path / '.config/obsidian-finance/sec-contact.json'
    previous = profile.read_bytes()
    contact = {'name': 'Terminal Probe Operator', 'email': 'terminal-probe@example.invalid'}
    master, slave = pty.openpty()
    process = subprocess.Popen([*command, '--terminal'], stdin=slave, stdout=slave, stderr=slave)
    try:
        assert select.select([master], [], [], 5)[0]
        assert os.read(master, 8192).strip() == b'READY_FOR_SEPARATE_INPUT'
        assert os.write(master, b' ' * 8193) == 8193
        # Simulate an input transport pause after the byte cap but before the line ends.
        output = os.read(master, 8192) if select.select([master], [], [], 0.5)[0] else b''
        os.write(master, json.dumps(contact).encode() + b'\n')
        assert process.wait(timeout=5) == 64
        while select.select([master], [], [], 0)[0]:
            output += os.read(master, 8192)
        assert all(value.encode() not in output for value in contact.values())
        assert b'SEC_CONTACT_INVALID' in output
        assert profile.read_bytes() == previous
    finally:
        if process.poll() is None:
            process.kill()
            process.wait()
        os.close(master)
        os.close(slave)
