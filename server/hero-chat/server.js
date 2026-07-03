#!/usr/bin/env node
/**
 * 句子互动官网首页 Hero 对话代理 (juzibot-website hero-chat proxy)
 * ───────────────────────────────────────────────────────────────────────────
 * 为什么需要它:
 *   官网是纯静态站, 而 Insight 开放平台用 accessKeyId/Secret 换 Bearer token,
 *   且同一 token 能调所有 /openapi 接口(含删除知识库)。把密钥放进前端 = 谁都能
 *   F12 盗走盗刷甚至搞破坏。所以由这个同机小服务持有密钥, 对外只暴露一个受限的
 *   POST /api/hero-chat, 内部固定转发到一个"门面 bot"的 /openapi/bot/message。
 *
 * 特性:
 *   - accessToken 内存缓存, 剩余 < 30min 才续期(贴合 Insight 自身的复用语义)
 *   - 只允许 text 消息, 长度上限, 固定 botId(前端无法指定其它 bot/接口)
 *   - 每 IP + 每 sessionId 双重限流, 封盗刷与成本
 *   - 上游超时保护, 错误不外泄密钥
 *   - 返回精简归一结构: { message, references[], handover, domain, fileUrls[] }
 *
 * 零依赖, Node 18+ (用到全局 fetch / AbortSignal.timeout)。
 * 配置全走环境变量, 见同目录 .env.example。
 */
'use strict';

const http = require('http');

// ── 配置 ─────────────────────────────────────────────────────────────────────
const CFG = {
  base:        (process.env.JZ_BASE || 'https://insight.juzibot.com').replace(/\/+$/, ''),
  keyId:       process.env.JZ_ACCESS_KEY_ID || '',
  keySecret:   process.env.JZ_ACCESS_KEY_SECRET || '',
  botId:       process.env.JZ_BOT_ID || '',
  port:        parseInt(process.env.PORT || '8787', 10),
  // 限流
  ipWindowMs:  parseInt(process.env.JZ_IP_WINDOW_MS || '300000', 10),  // 5 分钟
  ipMax:       parseInt(process.env.JZ_IP_MAX || '30', 10),            // 每 IP / 窗口
  sessionMax:  parseInt(process.env.JZ_SESSION_MAX || '40', 10),       // 每会话累计
  msgMaxLen:   parseInt(process.env.JZ_MSG_MAX_LEN || '500', 10),      // 单条字数
  upstreamTimeoutMs: parseInt(process.env.JZ_UPSTREAM_TIMEOUT_MS || '50000', 10), // 实测该 bot 20~37s, 留足余量
  // CORS: 逗号分隔的允许来源; 默认只放本地开发。生产同源(nginx 反代)无需 CORS。
  allowOrigins: (process.env.JZ_ALLOW_ORIGINS ||
    'http://localhost:8080,http://127.0.0.1:8080,http://localhost:5500,http://127.0.0.1:5500')
    .split(',').map(s => s.trim()).filter(Boolean),
};

if (!CFG.keyId || !CFG.keySecret || !CFG.botId) {
  console.error('[hero-chat] 缺少必填环境变量 JZ_ACCESS_KEY_ID / JZ_ACCESS_KEY_SECRET / JZ_BOT_ID');
  console.error('[hero-chat] 复制 .env.example 为 .env 填好后再启动 (见 README.md)。');
  process.exit(1);
}

// ── accessToken 缓存 ─────────────────────────────────────────────────────────
let tokenCache = { token: null, expiresAt: 0 };
let inflightToken = null;

async function getToken() {
  const now = Date.now();
  // 剩余有效期 > 30min 直接复用
  if (tokenCache.token && tokenCache.expiresAt - now > 30 * 60 * 1000) return tokenCache.token;
  if (inflightToken) return inflightToken; // 防并发重复申请
  inflightToken = (async () => {
    const res = await fetch(`${CFG.base}/openapi/get-access-token`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ accessKeyId: CFG.keyId, accessKeySecret: CFG.keySecret }),
      signal: AbortSignal.timeout(CFG.upstreamTimeoutMs),
    });
    const json = await res.json().catch(() => ({}));
    if (!res.ok || json.code !== 0 || !json.data?.accessToken) {
      throw new Error(`get-access-token failed: http ${res.status} code ${json.code}`);
    }
    const expiresInSec = Number(json.data.expiresIn) || 7200;
    tokenCache = { token: json.data.accessToken, expiresAt: Date.now() + expiresInSec * 1000 };
    return tokenCache.token;
  })();
  try { return await inflightToken; }
  finally { inflightToken = null; }
}

// ── 限流(内存, 单实例足够; 多实例需换 Redis) ─────────────────────────────────
const ipHits = new Map();       // ip -> number[] timestamps
const sessionCount = new Map();  // sessionId -> count

function rateLimit(ip, sessionId) {
  const now = Date.now();
  const arr = (ipHits.get(ip) || []).filter(t => now - t < CFG.ipWindowMs);
  if (arr.length >= CFG.ipMax) return { ok: false, reason: 'ip' };
  const sc = sessionCount.get(sessionId) || 0;
  if (sc >= CFG.sessionMax) return { ok: false, reason: 'session' };
  arr.push(now); ipHits.set(ip, arr);
  sessionCount.set(sessionId, sc + 1);
  return { ok: true };
}
// 周期清理, 防内存泄漏
setInterval(() => {
  const now = Date.now();
  for (const [ip, arr] of ipHits) {
    const live = arr.filter(t => now - t < CFG.ipWindowMs);
    if (live.length) ipHits.set(ip, live); else ipHits.delete(ip);
  }
  if (sessionCount.size > 5000) sessionCount.clear();
}, 60 * 1000).unref();

// ── 上游对话 ─────────────────────────────────────────────────────────────────
async function askBot({ sessionId, text }) {
  const token = await getToken();
  const res = await fetch(`${CFG.base}/openapi/bot/message`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${token}` },
    body: JSON.stringify({
      botId: CFG.botId,
      sessionId,
      message: { type: 'text', text },
      stream: false,
    }),
    signal: AbortSignal.timeout(CFG.upstreamTimeoutMs),
  });
  const json = await res.json().catch(() => ({}));
  if (json.code !== 0 || !json.data) {
    const err = new Error(`bot/message code ${json.code}`);
    err.upstreamCode = json.code;
    throw err;
  }
  const d = json.data;
  // 归一化 references -> 给前端做"来源"chip; 只露出标题/问句, 不泄露整段知识库内容
  const references = Array.isArray(d.references) ? d.references.slice(0, 3).map(r => {
    const src = r.reference?.source || {};
    const label = src.question || src.title || src.name || r.reference?.type || '知识库';
    return { label: String(label).slice(0, 40), similarity: r.similarity };
  }) : [];
  return {
    message: d.message || '',
    references,
    handover: !!d.handover,
    domain: d.domain || '',
    fileUrls: Array.isArray(d.fileUrls) ? d.fileUrls : [],
  };
}

// ── HTTP ─────────────────────────────────────────────────────────────────────
function clientIp(req) {
  const xff = req.headers['x-forwarded-for'];
  if (xff) return String(xff).split(',')[0].trim();
  return req.socket.remoteAddress || 'unknown';
}
function setCors(req, res) {
  const origin = req.headers.origin;
  if (origin && CFG.allowOrigins.includes(origin)) {
    res.setHeader('Access-Control-Allow-Origin', origin);
    res.setHeader('Vary', 'Origin');
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
    res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  }
}
function sendJson(res, status, obj) {
  const body = JSON.stringify(obj);
  res.writeHead(status, { 'Content-Type': 'application/json; charset=utf-8' });
  res.end(body);
}

const server = http.createServer((req, res) => {
  const url = new URL(req.url, `http://${req.headers.host || 'localhost'}`);
  setCors(req, res);

  if (req.method === 'OPTIONS') { res.writeHead(204); return res.end(); }

  if (url.pathname === '/api/hero-chat/health') {
    return sendJson(res, 200, { ok: true, hasToken: !!tokenCache.token });
  }

  if (url.pathname !== '/api/hero-chat' || req.method !== 'POST') {
    return sendJson(res, 404, { code: -404, message: 'not found' });
  }

  let raw = '';
  req.on('data', c => {
    raw += c;
    if (raw.length > 8192) { req.destroy(); } // 防超大 body
  });
  req.on('end', async () => {
    let body;
    try { body = JSON.parse(raw || '{}'); } catch { return sendJson(res, 400, { code: -400, message: 'bad json' }); }

    const sessionId = String(body.sessionId || '').slice(0, 64);
    const text = typeof body.message === 'string' ? body.message.trim() : '';
    if (!sessionId) return sendJson(res, 400, { code: -400, message: 'missing sessionId' });
    if (!text)      return sendJson(res, 400, { code: -400, message: 'empty message' });
    if (text.length > CFG.msgMaxLen)
      return sendJson(res, 400, { code: -400, message: `message too long (>${CFG.msgMaxLen})` });

    const rl = rateLimit(clientIp(req), sessionId);
    if (!rl.ok) return sendJson(res, 429, { code: -429, reason: rl.reason, message: '请求过于频繁，请稍后再试' });

    try {
      const data = await askBot({ sessionId, text });
      return sendJson(res, 200, { code: 0, data });
    } catch (e) {
      console.error('[hero-chat] upstream error:', e.message);
      // 不外泄密钥/堆栈; 前端会据此降级
      return sendJson(res, 502, { code: -502, message: '客服暂时不可用' });
    }
  });
});

server.listen(CFG.port, () => {
  console.log(`[hero-chat] listening on :${CFG.port}  → upstream ${CFG.base}  botId ${CFG.botId.slice(0, 8)}…`);
});
