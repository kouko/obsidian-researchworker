"""OpenCode exposes native skills from either independently installed package."""
import json
import shutil
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
LOADER = ROOT / ".opencode-plugin" / "index.js"
PACKAGE_NAMES = ("obsidian", "obsidian-finance")


def run_loader(root, package_name, expected_names):
    script = r'''
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { pathToFileURL } from "node:url";
const [root, packageName, ...names] = process.argv.slice(1);
const {default: plugin} = await import(pathToFileURL(`${root}/.opencode-plugin/index.js`));
assert.equal(plugin.id, packageName);
let commandCalls = 0;
async function load() {
  const skills = [];
  await plugin.setup({
    skill: {transform: async fn => fn({add: s => skills.push(s)})},
    command: {transform: async () => { commandCalls++; }},
  });
  return skills;
}
const first = await load();
const second = await load();
assert.deepEqual(first.map(s => s.id).sort(), names.map(name => `${packageName}:${name}`).sort());
assert.deepEqual(first, second);
assert.equal(commandCalls, 0);
for (const skill of first) {
  const directory = skill.id.slice(packageName.length + 1);
  assert.equal(skill.name, directory);
  assert.ok(skill.description.trim());
  assert.equal(skill.path, `${root}/skills/${directory}/SKILL.md`);
  const raw = readFileSync(skill.path, "utf8");
  const header = raw.match(/^---\r?\n[\s\S]*?\r?\n---\r?\n?/);
  assert.ok(header);
  assert.equal(skill.content, raw.slice(header[0].length));
}
'''
    subprocess.run(
        ["node", "--input-type=module", "-e", script, str(root), package_name, *expected_names],
        check=True,
    )


@pytest.mark.parametrize("package_name", PACKAGE_NAMES)
def test_shipped_skills_register_without_commands_from_standalone_package(tmp_path, package_name):
    package = REPO / package_name
    for directory in ("skills", ".opencode-plugin"):
        shutil.copytree(package / directory, tmp_path / directory)
    shutil.copy(package / "package.json", tmp_path / "package.json")
    shipped_names = sorted(path.parent.name for path in (package / "skills").glob("*/SKILL.md"))
    run_loader(tmp_path, package_name, shipped_names)


def test_skill_without_description_is_not_registered(tmp_path):
    (tmp_path / ".opencode-plugin").mkdir()
    shutil.copy(LOADER, tmp_path / ".opencode-plugin" / "index.js")
    (tmp_path / "package.json").write_text('{"type":"module","name":"obsidian"}')
    for name, frontmatter in [("good", "name: good\ndescription: useful"), ("bad", "name: bad")]:
        skill_dir = tmp_path / "skills" / name
        skill_dir.mkdir(parents=True)
        (skill_dir / "SKILL.md").write_text(f"---\n{frontmatter}\n---\nBody of {name}\n")
    before = {p: p.read_bytes() for p in tmp_path.rglob("*") if p.is_file()}
    run_loader(tmp_path, "obsidian", ["good"])
    assert before == {p: p.read_bytes() for p in tmp_path.rglob("*") if p.is_file()}


@pytest.mark.parametrize("package_name", PACKAGE_NAMES)
def test_package_identity_keeps_repository_and_other_hosts(package_name):
    root = REPO / package_name
    package = json.loads((root / "package.json").read_text())
    marketplace = json.loads((REPO / ".claude-plugin" / "marketplace.json").read_text())
    codex = json.loads((root / ".codex-plugin" / "plugin.json").read_text())
    claude = json.loads((root / ".claude-plugin" / "plugin.json").read_text())
    assert package["name"] == package_name
    assert package["repository"]["url"].endswith("/obsidian-researchworker.git")
    assert package["repository"]["directory"] == package_name
    assert marketplace["name"] == "obsidian-researchworker"
    marketplace_entry = next(entry for entry in marketplace["plugins"] if entry["name"] == package_name)
    assert marketplace_entry["name"] == codex["name"] == claude["name"] == package_name


def test_independent_loaders_have_identical_implementations():
    assert LOADER.read_bytes() == (REPO / "obsidian-finance" / ".opencode-plugin" / "index.js").read_bytes()
