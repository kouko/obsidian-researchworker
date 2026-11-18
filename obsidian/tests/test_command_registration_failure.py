# concern: one failed command registration prevents unrelated commands loading
"""A rejected registration must not hide the remaining skill commands."""

import subprocess
from pathlib import Path


def test_commands_rejected_entry_registers_remaining():
    """A single rejected command must not prevent later registrations."""
    script = r'''
import assert from "node:assert/strict";
import plugin from "./obsidian/.opencode-plugin/index.js";
const skills = [];
const accepted = [];
let rejected;
await plugin.setup({
  skill: {transform: async f => f({add: skill => skills.push(skill.id)})},
  command: {transform: async f => f({add: command => {
    if (!rejected) {
      rejected = command.name;
      throw Error("registration rejected");
    }
    accepted.push(command.name);
  }})},
  session: {prompt: async () => {}},
});
assert.ok(skills.length > 1);
assert.equal(rejected, skills[0]);
assert.deepEqual(accepted, skills.slice(1));
'''
    subprocess.run(
        ["node", "--input-type=module", "-e", script],
        cwd=Path(__file__).resolve().parents[2],
        check=True,
    )
