'use strict';
/**
 * @guard watches: a block type declared in a section's {% schema %} that the section never renders, a section with blocks that never outputs {{ block.shopify_attributes }}, and an "@app" block declared but never rendered. All three pass Theme Check and look fine in review; they show up only when a merchant adds the block in the theme editor and nothing appears, or it cannot be selected.
 * @guard extend: a new local block type in a section that branches on block.type needs its own `when 'type'` inside `case block.type` (or a `block.type == 'type'` test). If the case's `else` branch renders it on purpose, add it to ELSE_BRANCH_ALLOWED with the reason.
 */

// What this cannot catch, so nobody reads green as more than it is:
// - It checks that shopify_attributes appears somewhere in the section, not that every branch's
//   wrapper carries it. Dawn often puts it on the loop wrapper outside the case (collage, footer),
//   so a per-branch rule measured 15 exceptions on Dawn v16 — mostly exclusions, protecting nothing.
// - A section with a single local type and no branching renders every block the same way, so it
//   is not checked for a `when`.
// - Theme blocks (blocks/*.liquid, "@theme", {% content_for 'blocks' %}) are not covered. Dawn has
//   none; Theme Check validates the content_for arguments.
// - It reads the section file only. A branch that renders through a snippet counts as rendered.

const { test } = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');

const SECTIONS_DIR = path.resolve(__dirname, '..', '..', 'sections');

// Types a section renders through the `else` of `case block.type` on purpose. Each entry is a
// claim that is checked below: the else must exist and the type must not have its own `when`.
const ELSE_BRANCH_ALLOWED = {
  'main-cart-footer.liquid': {
    buttons: 'the checkout buttons are the fallback of the case; Dawn never gave them a when',
  },
};

const OPENERS = new Set([
  'case', 'if', 'unless', 'for', 'tablerow', 'capture', 'form', 'paginate',
  'style', 'javascript', 'stylesheet',
]);

function blank(match) {
  return ' '.repeat(match.length);
}

// Comments and raw blocks are blanked rather than removed so offsets stay true to the file.
function stripInert(text) {
  return text
    .replace(/\{%-?\s*comment\s*-?%\}[\s\S]*?\{%-?\s*endcomment\s*-?%\}/g, blank)
    .replace(/\{%-?\s*doc\s*-?%\}[\s\S]*?\{%-?\s*enddoc\s*-?%\}/g, blank)
    .replace(/\{%-?\s*raw\s*-?%\}[\s\S]*?\{%-?\s*endraw\s*-?%\}/g, blank);
}

// Every Liquid tag in order, with the lines of a {% liquid %} tag as tags of their own.
function tags(body) {
  const out = [];
  for (const m of body.matchAll(/\{%-?([\s\S]*?)-?%\}/g)) {
    const inner = m[1].trim();
    if (inner.startsWith('#')) continue;
    if (!/^liquid\b/.test(inner)) {
      out.push(inner);
      continue;
    }
    for (const line of inner.replace(/^liquid\b/, '').split('\n')) {
      const text = line.trim();
      if (text && !text.startsWith('#')) out.push(text);
    }
  }
  return out;
}

function readSection(file) {
  const text = fs.readFileSync(path.join(SECTIONS_DIR, file), 'utf8');
  const schemaMatch = text.match(/\{%-?\s*schema\s*-?%\}([\s\S]*?)\{%-?\s*endschema\s*-?%\}/);
  if (!schemaMatch) return null;
  const schema = JSON.parse(schemaMatch[1]);
  const declared = (schema.blocks || []).map((b) => b.type);
  const body = stripInert(text.slice(0, schemaMatch.index));

  const whenTypes = new Set();
  let blockCases = 0;
  let caseElse = false;
  let rendersAppBlock = false;
  const stack = [];
  for (const tag of tags(body)) {
    const name = tag.split(/\s+/, 1)[0];
    const args = tag.slice(name.length).trim();
    const top = stack[stack.length - 1];
    if (OPENERS.has(name)) {
      const isBlockCase = name === 'case' && args === 'block.type';
      if (isBlockCase) blockCases += 1;
      stack.push({ name, isBlockCase });
    } else if (name.startsWith('end') && OPENERS.has(name.slice(3))) {
      assert.equal(top && top.name, name.slice(3), `${file}: {% ${name} %} does not close {% ${top && top.name} %}`);
      stack.pop();
    } else if (name === 'when' && top && top.isBlockCase) {
      for (const lit of args.matchAll(/['"]([^'"]+)['"]/g)) whenTypes.add(lit[1]);
    } else if (name === 'else' && top && top.isBlockCase) {
      caseElse = true;
    } else if (name === 'render' && /^block\s*$/.test(args)) {
      rendersAppBlock = true;
    }
  }
  assert.deepEqual(stack.map((s) => s.name), [], `${file}: tags left open at the schema`);

  const compared = new Set();
  for (const m of body.matchAll(/block\.type\s*(?:==|!=)\s*['"]([^'"]+)['"]/g)) compared.add(m[1]);
  for (const m of body.matchAll(/['"]([^'"]+)['"]\s*(?:==|!=)\s*block\.type\b/g)) compared.add(m[1]);

  return {
    file,
    local: declared.filter((t) => !t.startsWith('@')),
    declaresApp: declared.includes('@app'),
    handled: new Set([...whenTypes, ...compared]),
    whenTypes,
    branches: blockCases > 0 || compared.size > 0,
    caseElse,
    rendersAppBlock,
    outputsAttributes: /\bblock\.shopify_attributes\b/.test(body),
  };
}

const sectionFiles = fs.readdirSync(SECTIONS_DIR).filter((f) => f.endsWith('.liquid'));
const sections = sectionFiles.map(readSection).filter(Boolean);

test('every declared block type has a render branch', () => {
  const examined = sections.filter((s) => s.local.length >= 2 || (s.local.length && s.branches));
  assert.ok(examined.length > 0, 'no section branches on block.type — the guard had nowhere to look');

  const missing = [];
  for (const s of examined) {
    const allowed = ELSE_BRANCH_ALLOWED[s.file] || {};
    for (const type of s.local) {
      if (s.handled.has(type)) continue;
      if (allowed[type] && s.caseElse) continue;
      missing.push(`${s.file} → '${type}'`);
    }
  }
  assert.deepEqual(missing, [], 'declared in {% schema %} but no `when` renders it');
});

test('every section with blocks outputs block.shopify_attributes', () => {
  const withBlocks = sections.filter((s) => s.local.length > 0);
  assert.ok(withBlocks.length > 0, 'no section declares local blocks — the guard had nowhere to look');

  const missing = withBlocks.filter((s) => !s.outputsAttributes).map((s) => s.file);
  assert.deepEqual(missing, [], 'the theme editor cannot select or highlight these blocks');
});

test('every section that accepts @app blocks renders them', () => {
  const withApps = sections.filter((s) => s.declaresApp);
  assert.ok(withApps.length > 0, 'no section declares @app — the guard had nowhere to look');

  const missing = withApps.filter((s) => !s.rendersAppBlock).map((s) => s.file);
  assert.deepEqual(missing, [], 'declares "@app" but has no {% render block %}');
});

test('ELSE_BRANCH_ALLOWED entries still hold', () => {
  const stale = [];
  for (const [file, types] of Object.entries(ELSE_BRANCH_ALLOWED)) {
    const s = sections.find((x) => x.file === file);
    if (!s) {
      stale.push(`${file}: section is gone`);
      continue;
    }
    if (!s.caseElse) stale.push(`${file}: no else in case block.type any more`);
    for (const type of Object.keys(types)) {
      if (!s.local.includes(type)) stale.push(`${file} → '${type}': no longer declared`);
      if (s.whenTypes.has(type)) stale.push(`${file} → '${type}': has its own when now — remove the entry`);
    }
  }
  assert.deepEqual(stale, []);
});
