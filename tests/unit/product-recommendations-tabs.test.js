'use strict';
// Unit tests for the DOM-free half of assets/product-recommendations-tabs.js. The file is a browser
// script, so it is loaded into a vm context with a bare `window`: without customElements it stops
// after publishing window.ProductRecommendationsTabs.
const { test } = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');

const FILE = path.resolve(__dirname, '..', '..', 'assets', 'product-recommendations-tabs.js');

function load() {
  const context = { window: {}, console };
  vm.runInNewContext(fs.readFileSync(FILE, 'utf8'), context);
  return context.window.ProductRecommendationsTabs;
}

// Arrays made inside the vm context have another realm's prototype; copy before deepEqual.
const plain = (value) => JSON.parse(JSON.stringify(value));

test('updateHistory puts the product first, once, and keeps at most max ids', () => {
  const { updateHistory } = load();
  assert.deepEqual(plain(updateHistory(['2', '1'], 3, 20)), ['3', '2', '1']);
  assert.deepEqual(plain(updateHistory(['2', '3', '1'], 3, 20)), ['3', '2', '1']);
  assert.deepEqual(plain(updateHistory(['1', '2', '3'], 4, 3)), ['4', '1', '2']);
  assert.deepEqual(plain(updateHistory([7, 8], '9', 20)), ['9', '7', '8']);
});

test('idsToShow leaves out the product being viewed and stops at the limit', () => {
  const { idsToShow } = load();
  assert.deepEqual(plain(idsToShow(['5', '4', '3', '2'], '5', 2)), ['4', '3']);
  assert.deepEqual(plain(idsToShow(['5'], 5, 8)), []);
});

test('searchQuery asks for every id with OR', () => {
  const { searchQuery } = load();
  assert.equal(searchQuery(['11', '22']), 'id:11 OR id:22');
});

test('orderByIds sorts by history order and puts unknown ids last', () => {
  const { orderByIds } = load();
  const item = (id) => ({ dataset: { productId: id } });
  const sorted = orderByIds([item('1'), item('9'), item('3')], ['3', '1']);
  assert.deepEqual(plain(sorted.map((entry) => entry.dataset.productId)), ['3', '1', '9']);
});

test('readHistory survives garbage, a non-array and a storage that throws', () => {
  const { readHistory, STORAGE_KEY } = load();
  const storage = (value) => ({ getItem: (key) => (key === STORAGE_KEY ? value : null) });
  assert.deepEqual(plain(readHistory(storage('["3",2]'))), ['3', '2']);
  assert.deepEqual(plain(readHistory(storage('{not json'))), []);
  assert.deepEqual(plain(readHistory(storage('{"a":1}'))), []);
  assert.deepEqual(plain(readHistory(storage(null))), []);
  assert.deepEqual(plain(readHistory({ getItem() { throw new Error('SecurityError'); } })), []);
});

test('writeHistory does not throw when storage refuses the write', () => {
  const { writeHistory } = load();
  assert.doesNotThrow(() => writeHistory({ setItem() { throw new Error('QuotaExceededError'); } }, ['1']));
});

test('TabLoader fetches a tab once and answers later loads from memory', async () => {
  const { TabLoader } = load();
  const urls = [];
  const loader = new TabLoader(async (url) => { urls.push(url); return `<p>${url}</p>`; });
  assert.equal(await loader.load('related', '/a'), '<p>/a</p>');
  assert.equal(await loader.load('related', '/a'), '<p>/a</p>');
  assert.deepEqual(plain(urls), ['/a']);
});

test('TabLoader shares one request between two loads of the same tab', async () => {
  const { TabLoader } = load();
  let calls = 0;
  const loader = new TabLoader(async () => { calls += 1; return 'html'; });
  await Promise.all([loader.load('related', '/a'), loader.load('related', '/a')]);
  assert.equal(calls, 1);
});

test('TabLoader answers null to a load that a later tab overtook', async () => {
  const { TabLoader } = load();
  let release;
  const slow = new Promise((resolve) => { release = resolve; });
  const loader = new TabLoader((url) => (url === '/slow' ? slow : Promise.resolve('fast')));
  const first = loader.load('related', '/slow');
  assert.equal(await loader.load('recently_viewed', '/fast'), 'fast');
  release('slow');
  assert.equal(await first, null);
  assert.equal(await loader.load('related', '/slow'), 'slow');
});

test('TabLoader does not keep a failed request, so the next load retries', async () => {
  const { TabLoader } = load();
  let calls = 0;
  const loader = new TabLoader(async () => { calls += 1; if (calls === 1) throw new Error('offline'); return 'html'; });
  await assert.rejects(loader.load('related', '/a'), /offline/);
  assert.equal(await loader.load('related', '/a'), 'html');
  assert.equal(calls, 2);
});
