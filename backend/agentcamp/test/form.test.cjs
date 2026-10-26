const { test } = require('node:test');
const assert = require('node:assert/strict');
const { readFileSync } = require('node:fs');
const { resolve } = require('node:path');
const { JSDOM } = require('jsdom');

const root = resolve(__dirname, '../../..');
const html = readFileSync(resolve(root, 'agentcamp.html'), 'utf8');
const script = readFileSync(resolve(root, 'assets/agentcamp.js'), 'utf8');

test('native form fallback never puts lead data in the URL', () => {
  const dom = new JSDOM(html);
  const form = dom.window.document.getElementById('acForm');
  assert.equal(form.method, 'post');
  assert.equal(form.getAttribute('action'), '/api/agentcamp/applications');
  dom.window.close();
});

function page(t, fetcher) {
  const dom = new JSDOM(html, { url: 'https://juzibot.com/agentcamp.html', runScripts: 'outside-only' });
  t.after(() => dom.window.close());
  const w = dom.window, doc = w.document, events = [];
  w.fetch = fetcher;
  w.AbortController = AbortController;
  w.HTMLElement.prototype.scrollIntoView = function () {};
  w.JZAnalytics = { trackButton: (...args) => events.push(args) };
  w.eval(script);
  const values = { 'f-name': '张测试', 'f-company': '测试企业', 'f-contact': 'private@example.com', 'f-task': '需要处理的业务资料' };
  for (const [id, value] of Object.entries(values)) doc.getElementById(id).value = value;
  doc.getElementById('f-agree').checked = true;
  return { w, doc, events, submit() { doc.getElementById('acForm').dispatchEvent(new w.Event('submit', { cancelable: true })); } };
}

async function finished(p) {
  for (let i = 0; i < 100; i++) {
    if (!p.doc.getElementById('acBtn').disabled) return;
    await new Promise(resolve => setTimeout(resolve, 5));
  }
  throw new Error('Form did not finish submitting');
}

test('form requires consent and valid contact, with no outgoing request for invalid input', async t => {
  let calls = 0;
  const p = page(t, async () => { calls++; });
  p.doc.getElementById('f-agree').checked = false;
  p.submit();
  p.doc.getElementById('f-agree').checked = true;
  p.doc.getElementById('f-contact').value = 'not-an-email';
  p.submit();
  assert.equal(calls, 0);
  assert.ok(p.doc.getElementById('f-contact').closest('.ac-field').classList.contains('err'));
});

test('form reports success only after JSON acknowledgement; analytics and browser storage contain no lead data', async t => {
  let sent;
  const p = page(t, async (url, options) => {
    sent = { url, ...options };
    return new Response(JSON.stringify({ ok: true, submissionId: options.headers['Idempotency-Key'] }));
  });
  p.submit();
  assert.equal(p.doc.getElementById('acBtn').disabled, true);
  await finished(p);
  assert.equal(sent.url, '/api/agentcamp/applications');
  assert.equal(JSON.parse(sent.body).agree, true);
  assert.ok(p.doc.getElementById('acForm').classList.contains('sent'));
  assert.equal(p.doc.getElementById('f-contact').value, '');
  assert.equal(p.w.sessionStorage.length, 0);
  assert.deepEqual(JSON.parse(JSON.stringify(p.events.map(e => e[2].submission_result))), ['attempt', 'success']);
  assert.ok(!JSON.stringify(p.events).includes('private@example.com'));
  assert.ok(!JSON.stringify(p.events).includes('测试企业'));
});

test('failed API and static fallback HTML preserve form contents; retry reuses key and suppresses double click', async t => {
  const keys = [];
  let count = 0;
  const p = page(t, async (_url, options) => {
    keys.push(options.headers['Idempotency-Key']);
    if (!count++) return new Response('<html>Homepage fallback</html>', { status: 200 });
    return new Response(JSON.stringify({ ok: true, submissionId: keys[0] }));
  });
  p.submit(); p.submit();
  await finished(p);
  assert.equal(keys.length, 1);
  assert.equal(p.doc.getElementById('f-contact').value, 'private@example.com');
  assert.equal(p.doc.getElementById('acError').hidden, false);
  assert.ok(!p.doc.getElementById('acForm').classList.contains('sent'));
  const storage = p.w.sessionStorage.getItem('agentcamp_submission');
  assert.ok(!storage.includes('private@example.com'));
  assert.ok(!storage.includes('测试企业'));
  p.submit();
  await finished(p);
  assert.equal(keys[1], keys[0]);
  assert.ok(p.doc.getElementById('acForm').classList.contains('sent'));
});

test('changed form gets a new key; rate limit and conflict remain retryable', async t => {
  const keys = [];
  let status = 429;
  const p = page(t, async (_url, options) => {
    keys.push(options.headers['Idempotency-Key']);
    return new Response('{}', { status });
  });
  p.submit(); await finished(p);
  assert.ok(p.doc.getElementById('acError').textContent.includes('一分钟'));
  p.doc.getElementById('f-task').value = '改过的业务';
  status = 409;
  p.submit(); await finished(p);
  assert.notEqual(keys[1], keys[0]);
  assert.equal(p.w.sessionStorage.length, 0);
  p.submit(); await finished(p);
  assert.notEqual(keys[2], keys[1]);
});

test('network error restores controls and never presents successful submission', async t => {
  const p = page(t, async () => { throw new TypeError('Network failed'); });
  p.submit(); await finished(p);
  assert.equal(p.doc.getElementById('acBtn').disabled, false);
  assert.equal(p.doc.getElementById('acForm').hasAttribute('aria-busy'), false);
  assert.equal(p.doc.getElementById('acError').hidden, false);
  assert.ok(!p.doc.getElementById('acForm').classList.contains('sent'));
});
