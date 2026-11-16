"""OpenCode exposes matching skills and user commands without changing other hosts."""
import json
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
LOADER = ROOT / ".opencode-plugin" / "index.js"


def run_loader(root, expected_count):
    script = r'''
import assert from "node:assert/strict";
import { pathToFileURL } from "node:url";
const [root, count] = process.argv.slice(1);
const {default: plugin} = await import(pathToFileURL(`${root}/.opencode-plugin/index.js`));
assert.equal(plugin.id, "obsidian");
let calls = [];
async function load() {
  const skills = [], commands = [];
  await plugin.setup({
    skill: {transform: async fn => fn({add: s => skills.push(s)})},
    command: {transform: async fn => fn({add: c => commands.push(c)})},
    session: {prompt: async input => { calls.push(input); return "sent"; }},
  });
  return {skills, commands};
}
const first = await load();
const second = await load();
assert.equal(first.skills.length, Number(count));
assert.deepEqual(first.skills.map(s => s.id), second.skills.map(s => s.id));
assert.deepEqual(first.commands.map(c => c.name), first.skills.map(s => s.id));
for (const skill of first.skills) {
  assert.ok(skill.id.startsWith("obsidian:"));
  const command = first.commands.find(c => c.name === skill.id);
  assert.equal(command.description, skill.description);
  const input = {sessionID: "session", prompt: {text: "my task", model: {providerID: "p", modelID: "m"}}, delivery: "queue"};
  assert.equal(await command.execute(input), "sent");
  const sent = calls.at(-1);
  assert.equal(sent.sessionID, input.sessionID);
  assert.equal(sent.delivery, input.delivery);
  assert.deepEqual(sent.model, input.prompt.model);
  assert.ok(sent.text.includes("my task"));
  assert.ok(sent.text.includes(`Base directory for this skill: ${root}/skills/`));
  assert.ok(sent.text.includes(skill.content));
}
'''
    subprocess.run(["node", "--input-type=module", "-e", script, str(root), str(expected_count)], check=True)


def test_shipped_skills_and_slash_commands():
    run_loader(ROOT, 15)


def test_skill_without_description_is_not_registered(tmp_path):
    (tmp_path / ".opencode-plugin").mkdir()
    shutil.copy(LOADER, tmp_path / ".opencode-plugin" / "index.js")
    (tmp_path / "package.json").write_text('{"type":"module"}')
    for name, frontmatter in [("good", "name: good\ndescription: useful"), ("bad", "name: bad")]:
        skill_dir = tmp_path / "skills" / name
        skill_dir.mkdir(parents=True)
        (skill_dir / "SKILL.md").write_text(f"---\n{frontmatter}\n---\nBody of {name}\n")
    before = {p: p.read_bytes() for p in tmp_path.rglob("*") if p.is_file()}
    run_loader(tmp_path, 1)
    assert before == {p: p.read_bytes() for p in tmp_path.rglob("*") if p.is_file()}


def test_package_identity_keeps_repository_and_other_hosts():
    package = json.loads((ROOT / "package.json").read_text())
    marketplace = json.loads((REPO / ".claude-plugin" / "marketplace.json").read_text())
    codex = json.loads((ROOT / ".codex-plugin" / "plugin.json").read_text())
    claude = json.loads((ROOT / ".claude-plugin" / "plugin.json").read_text())
    assert package["name"] == "obsidian"
    assert package["repository"]["url"].endswith("/obsidian-researchworker.git")
    assert marketplace["name"] == "obsidian-researchworker"
    assert marketplace["plugins"][0]["name"] == codex["name"] == claude["name"] == "obsidian"
