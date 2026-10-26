const { test } = require('node:test');
const assert = require('node:assert/strict');
const { randomUUID } = require('node:crypto');
const { mkdtempSync, rmSync } = require('node:fs');
const { tmpdir } = require('node:os');
const { join } = require('node:path');
const { createApp } = require('../dist/main');
const { readConfig, applicationSchema } = require('../dist/config');
const { Store, SubmissionConflict } = require('../dist/store');
const { Service } = require('../dist/service');
const { Feishu, UpstreamError } = require('../dist/feishu');

const config = readConfig({
  AGENTCAMP_APP_ID: 'cli_test', AGENTCAMP_APP_SECRET: 'test-only-not-a-secret',
  AGENTCAMP_BASE_TOKEN: 'testbase', AGENTCAMP_TABLE_ID: 'tblAgentcamp',
  AGENTCAMP_CHAT_ID: 'oc_test', AGENTCAMP_BASE_URL: 'https://example.feishu.cn/base/testbase',
  AGENTCAMP_ORIGINS: 'https://juzibot.com', AGENTCAMP_DB_PATH: ':memory:'
});
const payload = applicationSchema.parse({ name: '测试姓名', company: '测试公司', contact: 'test@example.com',
  task: '处理测试需求', agree: true, page: 'agentcamp' });

function gateway() {
  return { writes: 0, notices: 0, async ensureRecord() { this.writes++; return 'recTest'; }, async notify() { this.notices++; } };
}
async function server(t, overrides = {}) {
  const g = overrides.gateway || gateway();
  const context = await createApp(config, { worker: false, gateway: g, ...overrides });
  await context.app.listen(0, '127.0.0.1');
  const url = await context.app.getUrl();
  t.after(() => context.close());
  return { ...context, gateway: g, async submit(body = payload, id = randomUUID(), headers = {}) {
    return fetch(url + '/api/agentcamp/applications', { method: 'POST',
      headers: { Origin: 'https://juzibot.com', 'Content-Type': 'application/json', 'Idempotency-Key': id, ...headers }, body: JSON.stringify(body) });
  } };
}

test('HTTP rejects malformed input, untrusted origin, extra destination and missing consent before writing', async t => {
  const s = await server(t);
  for (const body of [{ ...payload, agree: false }, { ...payload, company: '' }, { ...payload, contact: 'a@' },
    { ...payload, task: 'x'.repeat(3001) }, { ...payload, table_id: 'tblSDR' }, { ...payload, page: 'sdr' }]) {
    assert.equal((await s.submit(body)).status, 400);
  }
  assert.equal((await s.submit(payload, 'bad-id')).status, 400);
  assert.equal((await s.submit(payload, '123e4567-e89b-12d3-a456-426614174000')).status, 400);
  assert.equal((await s.submit(payload, randomUUID(), { Origin: 'https://untrusted.example' })).status, 403);
  assert.equal((await s.submit(payload, randomUUID(), { 'Content-Type': 'text/plain' })).status, 415);
  assert.equal(s.gateway.writes, 0);
});

test('success means remote record exists; retries and duplicate clicks do not create another lead', async t => {
  const s = await server(t);
  const id = randomUUID();
  const response = await s.submit(payload, id);
  assert.equal(response.status, 200);
  assert.deepEqual(await response.json(), { ok: true, submissionId: id });
  assert.equal(response.headers.get('cache-control'), 'no-store');
  assert.equal((await s.submit(payload, id)).status, 200);
  assert.equal((await s.submit(payload)).status, 200);
  assert.equal(s.gateway.writes, 1);
  assert.equal((await s.submit({ ...payload, company: '不同公司' }, id)).status, 409);
  await s.service.tick();
  await s.service.tick();
  assert.equal(s.gateway.notices, 1);
  assert.equal(s.store.get(id).payload, null);
  assert.equal((await s.submit(payload, id)).status, 200);
});

test('concurrent submissions share a leased write and only confirm after storage', async t => {
  let release;
  const hold = new Promise(resolve => { release = resolve; });
  const g = gateway();
  g.ensureRecord = async function () { this.writes++; await hold; return 'recOne'; };
  const s = await server(t, { gateway: g });
  const id = randomUUID();
  const first = s.submit(payload, id);
  while (!g.writes) await new Promise(resolve => setTimeout(resolve, 5));
  const second = await s.submit(payload, id);
  assert.equal(second.status, 503);
  assert.equal((await second.json()).code, 'PENDING');
  release();
  assert.equal((await first).status, 200);
  assert.equal(g.writes, 1);
});

test('record failure stays pending; notification failure never changes successful submission response', async t => {
  const g = gateway();
  g.ensureRecord = async () => { throw new UpstreamError('network'); };
  const s = await server(t, { gateway: g });
  const id = randomUUID();
  assert.equal((await s.submit(payload, id)).status, 503);
  assert.equal(s.store.get(id).record_id, null);
  assert.equal(s.store.get(id).attempts, 1);
  assert.equal(s.gateway.notices, 0);
});

test('persistent queue recovers a remote commit after lost response and retries notification after restart', async t => {
  const dir = mkdtempSync(join(tmpdir(), 'agentcamp-'));
  t.after(() => rmSync(dir, { recursive: true, force: true }));
  const path = join(dir, 'state.sqlite');
  let now = 100000;
  const id = randomUUID();
  let committed = false, notices = 0, notificationFails = true;
  const g = {
    async ensureRecord() {
      if (!committed) { committed = true; throw new UpstreamError('lost_response'); }
      return 'recRecovered';
    },
    async notify() { notices++; if (notificationFails) throw new UpstreamError('network'); }
  };
  let store = new Store(path, () => now);
  let service = new Service(store, g);
  store.accept(id, payload);
  await service.deliver(id);
  assert.equal(store.get(id).record_id, null);
  store.close();
  now += 20000;
  store = new Store(path, () => now);
  service = new Service(store, g);
  await service.tick();
  assert.equal(store.get(id).record_id, 'recRecovered');
  await service.tick();
  assert.equal(store.get(id).record_id, 'recRecovered');
  assert.equal(store.get(id).notified_at, null);
  assert.ok(store.get(id).payload);
  store.close();
  now += 20000;
  notificationFails = false;
  store = new Store(path, () => now);
  service = new Service(store, g);
  await service.tick();
  assert.equal(store.get(id).notified_at, now);
  assert.equal(store.get(id).payload, null);
  await service.tick();
  assert.equal(notices, 2);
  store.close();
});

test('lease ownership protects recovery from stale workers', () => {
  let now = 1;
  const store = new Store(':memory:', () => now);
  const id = randomUUID();
  store.accept(id, payload);
  assert.throws(() => store.accept(id, { ...payload, name: 'different' }), SubmissionConflict);
  const first = store.claim(id);
  assert.equal(store.claim(id), undefined);
  now += 120001;
  const second = store.claim(id);
  store.stored(first, 'recStale');
  assert.equal(store.get(id).record_id, null);
  store.stored(second, 'recCurrent');
  assert.equal(store.get(id).record_id, 'recCurrent');
  store.close();
});

test('HTTP rate limiting and body size limits apply', async t => {
  const s = await server(t, { rateLimit: 2 });
  assert.equal((await s.submit()).status, 200);
  assert.equal((await s.submit(payload, randomUUID(), { 'X-Forwarded-For': '198.51.100.7' })).status, 200);
  assert.equal((await s.submit()).status, 429);
  const other = await server(t);
  assert.equal((await other.submit({ ...payload, task: 'x'.repeat(20000) })).status, 413);
});

function jsonResponse(data, status = 200) { return new Response(JSON.stringify(data), { status, headers: { 'Content-Type': 'application/json' } }); }
function fakeFeishu(handler) {
  const calls = [];
  return { calls, client: new Feishu(config, async (url, options) => {
    calls.push({ url: String(url), options, body: options.body && JSON.parse(options.body) });
    if (String(url).includes('/auth/')) return jsonResponse({ code: 0, tenant_access_token: 'fake-token', expire: 7200 });
    return handler(calls[calls.length - 1]);
  }) };
}

test('Feishu uses dedicated table, remote idempotency, stable source and no credentials in notification', async () => {
  const id = randomUUID();
  const row = { id, payload: JSON.stringify(payload), created_at: 1234567890000, record_id: 'recSaved' };
  const { client, calls } = fakeFeishu(({ url }) => url.includes('/search')
    ? jsonResponse({ code: 0, data: { items: [] } })
    : jsonResponse({ code: 0, data: { record: { record_id: 'recSaved' }, message_id: 'om_test' } }));
  assert.equal(await client.ensureRecord(row), 'recSaved');
  await client.notify(row);
  const create = calls.find(c => c.url.includes('client_token='));
  assert.ok(create.url.includes('/testbase/tables/tblAgentcamp/records?client_token=' + id));
  assert.equal(create.body.fields['来源'], 'AgentCamp');
  assert.equal(create.body.fields['同意联系'], true);
  assert.equal(create.body.fields['提交时间'], row.created_at);
  const notification = calls.find(c => c.url.includes('/im/v1/messages'));
  assert.equal(notification.body.uuid, id);
  assert.equal(notification.body.receive_id, 'oc_test');
  assert.ok(notification.body.content.includes('record=recSaved'));
  assert.ok(!notification.body.content.includes(payload.contact));
  assert.equal(calls.filter(c => c.url.includes('/auth/')).length, 1);
});

test('remote lookup recovers existing record without creating a duplicate', async () => {
  const { client, calls } = fakeFeishu(() => jsonResponse({ code: 0, data: { items: [{ record_id: 'recExisting' }] } }));
  assert.equal(await client.ensureRecord({ id: randomUUID() }), 'recExisting');
  assert.equal(calls.length, 2);
});

test('lead text cannot inject a Feishu all-members mention into notification', async () => {
  const { client, calls } = fakeFeishu(() => jsonResponse({ code: 0, data: { message_id: 'om_test' } }));
  await client.notify({ id: randomUUID(), record_id: 'recSaved', payload: JSON.stringify({ ...payload, task: '<at user_id="all">everyone</at>' }) });
  const content = calls.find(c => c.url.includes('/im/v1/messages')).body.content;
  assert.ok(!content.includes('<at'));
});

test('HTTP success with Feishu error code is failure; errors do not reveal upstream text', async () => {
  const { client } = fakeFeishu(() => jsonResponse({ code: 1254302, msg: 'contains personal data or secrets' }));
  await assert.rejects(client.ensureRecord({ id: randomUUID() }), e => e instanceof UpstreamError && e.code === '1254302' && !e.message.includes('secrets'));
});

test('destination validation refuses the SDR table and mismatched AgentCamp schema', async () => {
  const wrong = fakeFeishu(() => jsonResponse({ code: 0, data: { items: [{ table_id: 'tblAgentcamp', name: 'SDR 线索' }] } }));
  await assert.rejects(wrong.client.verifyDestination(), e => e.code === 'wrong_destination_table');
  const missing = fakeFeishu(({ url }) => jsonResponse({ code: 0, data: { items: url.includes('/fields') ? [] : [{ table_id: 'tblAgentcamp', name: 'AgentCamp 线索' }] } }));
  await assert.rejects(missing.client.verifyDestination(), e => e.code === 'destination_schema_mismatch');
});

test('invalid configuration reports keys only, never credential values', () => {
  assert.throws(() => readConfig({ AGENTCAMP_APP_SECRET: 'private-secret-value' }), e => !e.message.includes('private-secret-value') && e.message.includes('AGENTCAMP_TABLE_ID'));
});
