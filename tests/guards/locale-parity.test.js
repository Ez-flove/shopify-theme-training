'use strict';
/**
 * @guard watches: a storefront string added to locales/en.default.json without its translation in locales/vi.json. Dawn turns MatchingTranslations off in .theme-check.yml, so Theme Check never reports it; the /vi storefront then shows "Translation missing: vi.…" where the text should be.
 * @guard extend: a new key in en.default.json needs the same key in vi.json. A pluralised string (an object of one/other …) needs at least "other" in vi.json, because Vietnamese has no grammatical plural. A string that stays English on purpose still goes into vi.json, with the English text.
 */

// What this cannot catch:
// - Wrong or untranslated text: an English sentence copied into vi.json passes.
// - The other 49 storefront locales (EX-01 D-5) and the *.schema.json files, which only the admin reads.

const { test } = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');

const LOCALES = path.resolve(__dirname, '..', '..', 'locales');
const PLURAL = new Set(['zero', 'one', 'two', 'few', 'many', 'other']);

function read(file) {
  return JSON.parse(fs.readFileSync(path.join(LOCALES, file), 'utf8'));
}

// key → 'text' | 'plural'. A plural group is an object whose keys are all CLDR plural categories.
function strings(object, prefix = '', out = new Map()) {
  for (const [name, value] of Object.entries(object)) {
    const key = prefix ? `${prefix}.${name}` : name;
    if (value && typeof value === 'object') {
      const names = Object.keys(value);
      if (names.length > 0 && names.every((category) => PLURAL.has(category))) out.set(key, 'plural');
      else strings(value, key, out);
    } else {
      out.set(key, 'text');
    }
  }
  return out;
}

function lookup(object, key) {
  return key.split('.').reduce((node, name) => (node == null ? undefined : node[name]), object);
}

const en = read('en.default.json');
const vi = read('vi.json');

test('every en.default.json string has a vi.json translation', () => {
  const english = strings(en);
  // Dawn ships 385 storefront strings; a parse that finds far fewer is not looking at the real file.
  assert.ok(english.size > 300, `only ${english.size} strings read from en.default.json`);
  const missing = [];
  for (const [key, kind] of english) {
    const value = lookup(vi, key);
    if (kind === 'plural' ? !(value && typeof value.other === 'string') : typeof value !== 'string') {
      missing.push(key);
    }
  }
  assert.deepEqual(missing, [], 'missing from vi.json (a plural needs "other")');
});
