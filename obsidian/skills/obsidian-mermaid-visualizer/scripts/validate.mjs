// validate.mjs — render every ```mermaid block of a markdown file with Pele,
// the Mermaid renderer Obsidian ships since 1.15, and report per-block verdicts.
//
// Pinned: pele 1.13.0 (see package.json). Reason: the Obsidian 1.15.1 app
// bundle's lib/pele.min.js carries the banner "Pele 1.13.0" (checked
// 2026-11-23); the 1.15.0 installer bundled 1.8.0, and both agree on the
// known samples. Re-check the bundle banner when Obsidian updates.
//
// Usage: PELE_DIR=<installed pele package dir> node validate.mjs path/to/note.md
//        (validate.sh sets PELE_DIR to its cache install.)
// Exit:  0 = all blocks render (or none found), 1 = any FAIL, 2 = bad usage.

import { readFileSync } from 'node:fs';
import { join } from 'node:path';
import { pathToFileURL } from 'node:url';

if (!process.env.PELE_DIR) {
  console.error('validate.mjs: PELE_DIR is not set; run via validate.sh');
  process.exit(2);
}
const { render } = await import(pathToFileURL(join(process.env.PELE_DIR, 'dist', 'pele.js')).href);

const args = process.argv.slice(2);
if (args.length !== 1) {
  console.error('usage: validate.sh <note.md>');
  process.exit(2);
}
const path = args[0];
let text;
try {
  text = readFileSync(path, 'utf8');
} catch (e) {
  console.error(`cannot read: ${path} (${e.message})`);
  process.exit(2);
}

const blocks = [];
let cur = null;
text.split(/\r?\n/).forEach((line, i) => {
  if (cur === null && /^\s*```mermaid\s*$/.test(line)) cur = { line: i + 1, body: [] };
  else if (cur !== null && /^\s*```\s*$/.test(line)) { blocks.push(cur); cur = null; }
  else if (cur !== null) cur.body.push(line);
});

if (blocks.length === 0) {
  console.log(`no mermaid diagrams found in: ${path}`);
  process.exit(0);
}

let fail = 0;
blocks.forEach((b, i) => {
  let err = '';
  try {
    const r = render(b.body.join('\n'));
    if (r && r.error) err = String(r.error.message ?? r.error);
    else if (!r || !r.svg) err = 'render produced no output';
  } catch (e) {
    err = String(e?.message ?? e);
  }
  const where = `block ${i + 1} (line ${b.line})`;
  if (err) {
    fail = 1;
    console.log(`FAIL  ${where}  ${err.replace(/\s*\n\s*/g, ' | ')}`);
  } else {
    console.log(`PASS  ${where}`);
  }
});
console.log('---');
console.log('engine: pele 1.13.0 (Obsidian 1.15.1 bundle)');
process.exit(fail);
