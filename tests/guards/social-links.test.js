'use strict';
/**
 * @guard watches: a social link setting declared in config/settings_schema.json (Theme settings → Social media) but missing from one of the theme files that list every social network — the icon rows in the footer, announcement bar and menu drawer, the password page, the "is any social link set" checks and the Organization JSON-LD. Theme Check passes; the icon just never shows on that one surface, or a footer whose only social link is the new one renders no social row at all.
 * @guard extend: a new social_<name>_link in the Social media group must be named in every file this guard lists, the same number of times as the other networks in that file. A file that reads a single network for its own reason (meta-tags.liquid reads only X/Twitter) is not a list and is not checked.
 */

// What this cannot catch:
// - It counts mentions, not meaning: a mention in the wrong branch still counts.
// - It scans sections/, snippets/, layout/ and blocks/. Templates and JavaScript are not read.
// - The storefront label in locales/*.json and the icon file in assets/ are not checked here:
//   Theme Check reports a missing default-locale key, and the icon is checked in the browser.

const { test } = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');

const ROOT = path.resolve(__dirname, '..', '..');
const SCAN_DIRS = ['sections', 'snippets', 'layout', 'blocks'];

// Files that list every network on Dawn v16. Each case checks the scan still finds them, so an
// empty scan cannot pass as "nothing is missing".
const KNOWN_LISTS = ['snippets/social-icons.liquid', 'sections/footer.liquid', 'sections/header.liquid'];

function socialIds() {
  const schema = JSON.parse(fs.readFileSync(path.join(ROOT, 'config', 'settings_schema.json'), 'utf8'));
  return schema
    .flatMap((group) => group.settings || [])
    .map((setting) => setting.id)
    .filter((id) => /^social_[a-z]+_link$/.test(id || ''));
}

function liquidFiles() {
  return SCAN_DIRS.flatMap((dir) => {
    const abs = path.join(ROOT, dir);
    if (!fs.existsSync(abs)) return [];
    return fs
      .readdirSync(abs)
      .filter((name) => name.endsWith('.liquid'))
      .map((name) => `${dir}/${name}`);
  });
}

function mentions(file, ids) {
  const text = fs.readFileSync(path.join(ROOT, file), 'utf8');
  return Object.fromEntries(ids.map((id) => [id, (text.match(new RegExp(`settings\\.${id}\\b`, 'g')) || []).length]));
}

// A file naming two or more networks is a list of networks.
function socialLists(ids) {
  return liquidFiles()
    .map((file) => ({ file, count: mentions(file, ids) }))
    .filter(({ count }) => Object.values(count).filter(Boolean).length >= 2);
}

function assertScanIsReal(lists) {
  const found = lists.map((list) => list.file);
  const lost = KNOWN_LISTS.filter((file) => !found.includes(file));
  assert.deepEqual(lost, [], `the scan no longer finds these known lists: ${lost.join(', ')}`);
}

test('the schema declares the social links to compare against', () => {
  const ids = socialIds();
  assert.ok(ids.length >= 9, `expected Dawn's nine social settings or more, found ${ids.length}: ${ids.join(', ')}`);
});

test('every list of networks names every social link, as often as the others', () => {
  const ids = socialIds();
  const lists = socialLists(ids);
  assertScanIsReal(lists);
  const problems = [];
  for (const { file, count } of lists) {
    const expected = Math.max(...Object.values(count));
    for (const id of ids) {
      if (count[id] !== expected) problems.push(`${file}: ${id} named ${count[id]}×, the other networks ${expected}×`);
    }
  }
  assert.deepEqual(problems, []);
});
