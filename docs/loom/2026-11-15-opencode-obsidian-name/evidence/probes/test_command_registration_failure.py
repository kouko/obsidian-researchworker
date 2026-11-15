# concern: one failed command registration prevents unrelated commands loading
"""A rejected registration must not hide the remaining skill commands."""

import subprocess


def test_commands_rejected_entry_registers_remaining():
    """A single rejected command must not prevent later registrations."""
    script = r'''
import assert from "node:assert/strict";
import plugin from "./obsidian/.opencode-plugin/index.js";
const accepted = [];
let rejected = false;
await plugin.setup({
  skill: {transform: async f => f({add: () => {}})},
  command: {transform: async f => f({add: command => {
    if (!rejected) { rejected = true; throw Error("registration rejected"); }
    accepted.push(command.name);
  }})},
  session: {prompt: async () => {}},
});
assert.equal(rejected, true);
assert.equal(accepted.length, 13);
assert.ok(accepted.every(name => name.startsWith("obsidian:")));
'''
    subprocess.run(["node", "--input-type=module", "-e", script], check=True)
