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
// Exit:  0 = all blocks render (or none found), 1 = any FAIL, 2 = bad usage or pele cannot load.

import { readFileSync } from 'node:fs';
import { join } from 'node:path';
import { pathToFileURL } from 'node:url';

if (!process.env.PELE_DIR) {
  console.error('validate.mjs: PELE_DIR is not set; run via validate.sh');
  process.exit(2);
}
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

let render;
try {
  ({ render } = await import(pathToFileURL(join(process.env.PELE_DIR, 'dist', 'pele.js')).href));
} catch (e) {
  console.error(`validate.mjs: cannot load pele from ${process.env.PELE_DIR} (${e.message})`);
  process.exit(2);
}

// Fences as Obsidian sees them: ``` or ~~~ (3+), indented at most 3 spaces,
// optionally inside (nested) callout '>' prefixes; closed only by the same
// char at least as long. Any fence (not only mermaid) is tracked so a
// ```mermaid line inside an outer ````markdown fence stays literal code.
const blocks = [];
let open = null; // { char, len, mermaid, line, body }
text.split(/\r?\n/).forEach((raw, i) => {
  let line = raw;
  while (/^ {0,3}>/.test(line)) line = line.replace(/^ {0,3}> ?/, '');
  const m = /^ {0,3}(`{3,}|~{3,})(.*)$/.exec(line);
  if (open === null) {
    if (m && !(m[1][0] === '`' && m[2].includes('`'))) {
      open = { char: m[1][0], len: m[1].length, mermaid: m[2].trim().split(/\s+/)[0] === 'mermaid', line: i + 1, body: [] };
    }
  } else if (m && m[1][0] === open.char && m[1].length >= open.len && m[2].trim() === '') {
    if (open.mermaid) blocks.push(open);
    open = null;
  } else {
    open.body.push(line);
  }
});
if (open !== null && open.mermaid) blocks.push({ ...open, unclosed: true });

if (blocks.length === 0) {
  console.log(`no mermaid diagrams found in: ${path}`);
  process.exit(0);
}

let fail = 0;
blocks.forEach((b, i) => {
  let err = b.unclosed ? 'mermaid fence is not closed before end of file' : '';
  if (!err) try {
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
