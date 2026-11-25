# concern: one failed native registration prevents unrelated skills loading
"""A rejected registration must not hide the remaining native skills."""

import subprocess
from pathlib import Path

import pytest


@pytest.mark.parametrize("package_name", ("obsidian", "obsidian-finance"))
def test_rejected_skill_registers_remaining(package_name):
    """A single rejected native skill must not prevent later registrations."""
    script = r'''
import assert from "node:assert/strict";
const [packageName] = process.argv.slice(1);
const {default: plugin} = await import(`./${packageName}/.opencode-plugin/index.js`);
const skills = [];
const accepted = [];
let rejected;
await plugin.setup({
  skill: {transform: async f => f({add: skill => {
    skills.push(skill.id);
    if (!rejected) {
      rejected = skill.id;
      throw Error("registration rejected");
    }
    accepted.push(skill.id);
  }})},
});
assert.ok(skills.length > 1);
assert.equal(rejected, skills[0]);
assert.deepEqual(accepted, skills.slice(1));
'''
    subprocess.run(
        ["node", "--input-type=module", "-e", script, package_name],
        cwd=Path(__file__).resolve().parents[2],
        check=True,
    )
