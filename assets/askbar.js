/* ============================================================================
   句子互动官网 · 全站对话层 askbar.js  （AI-native 大改 · 核心组件）
   - 常驻入口「问句子 ⌘K」+ Cmd/Ctrl-K 唤起的居中聚光对话浮层，贯穿每一页
   - 命中意图 → 秒回 + 可点实体卡（对话即导航）；自由输入 → 真 /api/hero-chat
   - 渲染：证据卡(references/similarity)、转人工决策日志卡(handover)、长延迟体面等待态
   - 每页可设 window.PAGE_CTX = {entity, type, title} 注入上下文
   - 纯前端、零依赖、复用现有 /api/hero-chat；键盘/读屏/移动可用
   ========================================================================== */
(function () {
  if (window.__jzab) return; window.__jzab = true;
  var REL = (typeof window.SITE_REL === 'string') ? window.SITE_REL : '';
  var API = (window.JZAB_API) || (REL + 'api/hero-chat');
  var SID = 'ab-' + Math.random().toString(36).slice(2, 9);
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion:reduce)').matches;

  // ---- 实体库：对话即导航 ----
  var P = function (s) { return REL + 'products/' + s; }, W = function (s) { return REL + 'workforce/' + s; };
  var ENT = {
    miaohui:  { nm: '句子秒回 · 工作台', ds: '11 个 IM 通道汇成一个工作台', ic: 'fa-comments', href: P('miaohui.html') },
    miaodong: { nm: '句子秒懂 · 大脑', ds: '不写代码也能搭 Agent', ic: 'fa-diagram-project', href: P('miaodong.html') },
    shouhu:   { nm: '句子守护 · 主管', ds: '上线前测过、上线后管着', ic: 'fa-shield-halved', href: P('shouhu.html') },
    canmou:   { nm: '句子问数 · 参谋', ds: '一句话查所有业务数据', ic: 'fa-chart-line', href: P('canmou.html') },
    dongxing: { nm: '句子懂行 · 记忆', ds: '散乱知识炼成可检索资产', ic: 'fa-book-bookmark', href: P('dongxing.html') },
    cli:      { nm: '句子 CLI · 手', ds: '操作一切人用软件的执行层', ic: 'fa-terminal', href: P('cli.html') },
    zhizao:   { nm: '句子制造 · 地基', ds: '补齐数字化基建，一客一环境', ic: 'fa-cubes', href: P('zhizao.html') },
    sales:    { nm: 'AI 销售', ds: '建联到首单成交全程接管', ic: 'fa-bullseye', href: W('sales.html') },
    service:  { nm: 'AI 客服', ds: '售前到售后都接得住', ic: 'fa-headset', href: W('service.html') },
    marketing:{ nm: 'AI 导购', ds: '私域导购 24×7 长尾也覆盖', ic: 'fa-store', href: W('marketing.html') },
    finance:  { nm: 'AI 理财顾问', ds: '银行/证券/保险落地·多年风控话术', ic: 'fa-landmark', href: W('finance.html') },
    government:{ nm: 'AI 社工/调解员', ds: '政务高合规·全程可追溯', ic: 'fa-scale-balanced', href: W('government.html') },
    hr:       { nm: 'AI HR', ds: '简历初筛 + AI 语音面试', ic: 'fa-user-tie', href: W('hr.html') },
    geo:      { nm: 'GEO 优化师', ds: 'GEO 让品牌被 AI 推荐·公域到私域', ic: 'fa-bullhorn', href: W('geo.html') },
    enterprise:{ nm: '企业级能力', ds: '和 Anthropic 同判断', ic: 'fa-building-shield', href: REL + 'enterprise.html' },
    news:     { nm: '句子·动态', ds: '博客、公众号与 AI 行业动态，持续更新', ic: 'fa-newspaper', href: REL + 'news.html' },
    industries:{ nm: '客户与行业', ds: '5 大高合规行业落地', ic: 'fa-globe', href: REL + 'industries.html' },
    fde:      { nm: 'FDE 交付', ds: '陪跑落地、交付结果', ic: 'fa-people-carry-box', href: REL + 'fde.html' },
  };
  // ---- 意图路由：命中 → 秒回 + 实体卡（对话即导航，0 延迟、可控口径） ----
  var ROUTES = [
    { re: /(区别|不一样|不同|普通|传统|chatbot|和别的)/i, a: '普通机器人按关键词命中、答不上就转人工；句子是「AI 员工」——理解上下文、查知识库、调 CRM/工单，把活直接干完，真搞不定才转人工。去年真实转人工率 2.73%（行业基线约 27%）。', cards: ['service', 'enterprise'] },
    { re: /(接入|上线|多久|部署|开通|落地|实施)/i, a: '标准 IM 渠道（微信客服/小程序/公众号/抖音/飞书等）最快 1 天就能让第一个 AI 员工上岗；复杂业务由 FDE 团队陪跑约 90 天达成结果指标。', cards: ['fde', 'miaohui'] },
    { re: /(安全|隐私|私有|合规|数据|审计|等保)/i, a: '支持私有化/专属部署，数据不出域、全程加密可审计，已服务金融、政务等高合规行业。能说什么可提前写死，每句决策可追溯。', cards: ['enterprise', 'government'] },
    { re: /(价格|报价|多少钱|收费|计价|预算|成本)/i, a: '按结果/按效果交付——价格随席位与 AI 员工数量、是否私有化而定。把你的场景告诉我，或直接预约演示，我们给一版贴合你行业的方案。', cards: ['fde'], lead: true },
    { re: /(渠道|微信|抖音|飞书|小红书|whatsapp|平台|通道)/i, a: '微信客服、小程序、公众号、抖音、小红书、飞书、WhatsApp 等 10+ 主流 IM，全部收进一个工作台统一接待。', cards: ['miaohui'] },
    { re: /(geo|全域营销|被\s*ai\s*推荐|豆包|deepseek|ai\s*答案|种草)/i, a: 'GEO 优化师专管品牌在豆包/DeepSeek 等 AI 答案里的位置：GEO 监测诊断、内容生产、渠道发布，公域意向自动沉到企微接着复购。', cards: ['geo'] },
    { re: /(销售|获客|线索|成交|转化|直播)/i, a: 'AI 销售从直播搬家、私域承接到漏斗跟进，建联到首单成交全程接管，按置信度三档执行。', cards: ['sales'] },
    { re: /(客服|售后|投诉|工单|接待)/i, a: 'AI 客服售前到售后全链路接得住，5 年 BadCase 沉淀，意图+情绪识别，必要时无缝转人工。', cards: ['service'] },
    { re: /(数据|报表|图表|问数|分析|看板|bi)/i, a: '句子问数：一句话查公司所有数据，秒级出图表，可逐层追问钻取，异常主动预警——不写 SQL、不约 BI。', cards: ['canmou'] },
    { re: /(动态|博客|文章|佳芮|创始人|新闻|访谈|最近在做)/i, a: '「动态」页聚合了我们的博客精选、公众号更新和 AI 行业动态——FDE、AI 员工落地、产品与组织思考，持续更新，每条都能跳原文。', cards: ['news'] },
    { re: /(知识|文档|资料|检索|出处|知识库)/i, a: '句子懂行把散乱资料清洗、切分、对齐问法，炼成能查、带出处的知识资产——这是 Agent 答得准的前提。', cards: ['dongxing'] },
    { re: /(演示|预约|联系|试用|demo|怎么买|顾问)/i, a: '好的，我帮你接一下——留个联系方式，工作日当天会有顾问带着你所在行业的真实场景做演示。', cards: [], lead: true },
    { re: /(产品|有哪些|功能|能力|矩阵)/i, a: '句子有 7 个产品组成 AI 员工的基建：秒回(工作台)、秒懂(大脑)、守护(主管)、问数(参谋)、懂行(记忆)、CLI(手)、制造(地基)。点开看：', cards: ['miaohui', 'miaodong', 'shouhu', 'canmou'] },
    { re: /(员工|岗位|招聘|团队|岗)/i, a: '句子的 AI 员工已在销售、客服、导购、理财顾问、社工/调解、HR 等岗位真实当班。看看他们：', cards: ['sales', 'service', 'finance', 'government'] },
  ];

  // ---- 样式（用 site.css 变量，带兜底）----
  var css = '' +
    '.jzab-trigger{display:inline-flex;align-items:center;gap:7px;font:inherit;font-size:13px;font-weight:650;color:var(--ink,#0b1020);background:var(--bg-2,#fff);border:1px solid var(--line,#e6e8ef);border-radius:999px;padding:7px 13px;cursor:pointer;transition:border-color .2s,box-shadow .2s,transform .2s}' +
    '.jzab-trigger:hover{border-color:var(--blue,#4338CA);box-shadow:0 6px 18px rgba(67,56,202,.12);transform:translateY(-1px)}' +
    '.jzab-trigger .jzab-kbd{font:600 11px/1 ui-monospace,monospace;color:var(--ink-3,#8a92a6);border:1px solid var(--line-2,#d7dae3);border-radius:5px;padding:2px 5px}' +
    '@media(max-width:1080px){.jzab-trigger{display:none}}' + /* 手机/平板：导航 pill 隐藏，右下角浮动按钮兜底，避免撑爆导航 */
    '.jzab-fab{position:fixed;right:max(18px,env(safe-area-inset-right));bottom:max(18px,env(safe-area-inset-bottom));z-index:940;display:inline-flex;align-items:center;gap:8px;font-size:14px;font-weight:700;color:#fff;background:linear-gradient(135deg,var(--blue,#4338CA),#6366F1);border:none;border-radius:999px;padding:13px 18px;cursor:pointer;box-shadow:0 12px 34px rgba(67,56,202,.34);transition:transform .2s,box-shadow .2s}' +
    '.jzab-fab:hover{transform:translateY(-2px);box-shadow:0 18px 44px rgba(67,56,202,.42)}' +
    '.jzab-fab i{font-size:15px}' +
    '@media(max-width:600px){.jzab-fab span{display:none}.jzab-fab{padding:15px}}' +
    '.jzab-ov{position:fixed;inset:0;z-index:980;display:none;align-items:flex-start;justify-content:center;padding:10vh 16px 24px;background:rgba(11,16,32,.46);backdrop-filter:blur(7px);-webkit-backdrop-filter:blur(7px)}' +
    '.jzab-ov.open{display:flex}' +
    '.jzab-panel{width:min(680px,100%);max-height:80vh;display:flex;flex-direction:column;background:var(--bg,#fff);border:1px solid var(--line,#e6e8ef);border-radius:18px;box-shadow:0 40px 120px rgba(11,16,32,.4);overflow:hidden;animation:jzab-in .22s cubic-bezier(.22,1,.36,1)}' +
    '@keyframes jzab-in{from{opacity:0;transform:translateY(-12px) scale(.985)}to{opacity:1;transform:none}}' +
    '@media(prefers-reduced-motion:reduce){.jzab-panel{animation:none}}' +
    '.jzab-head{display:flex;align-items:center;gap:10px;padding:14px 16px;border-bottom:1px solid var(--line,#e6e8ef)}' +
    '.jzab-head .jzab-sp{width:26px;height:26px;border-radius:8px;flex:0 0 26px;display:grid;place-items:center;color:#fff;background:linear-gradient(135deg,var(--blue,#4338CA),#6366F1);font-size:13px}' +
    '.jzab-in{flex:1;min-width:0;border:none;outline:none;background:transparent;font:inherit;font-size:16px;color:var(--ink,#0b1020)}' +
    '.jzab-in::placeholder{color:var(--ink-3,#8a92a6)}' +
    '.jzab-x{border:none;background:transparent;color:var(--ink-3,#8a92a6);font-size:13px;cursor:pointer;border:1px solid var(--line-2,#d7dae3);border-radius:6px;padding:3px 7px}' +
    '.jzab-ctx{padding:8px 16px;font-size:12px;color:var(--ink-3,#8a92a6);border-bottom:1px solid var(--line-2,#eef0f5);display:flex;align-items:center;gap:7px}' +
    '.jzab-ctx b{color:var(--ink-2,#5A6478);font-weight:650}' +
    '.jzab-body{flex:1;overflow-y:auto;padding:16px;display:flex;flex-direction:column;gap:14px;scroll-behavior:smooth}' +
    '.jzab-chips{display:flex;flex-wrap:wrap;gap:8px}' +
    '.jzab-chip{font-size:12.5px;color:var(--ink-2,#5A6478);background:var(--bg-2,#f7f8fb);border:1px solid var(--line-2,#e6e8ef);border-radius:999px;padding:7px 13px;cursor:pointer;transition:border-color .2s,color .2s}' +
    '.jzab-chip:hover{border-color:var(--blue,#4338CA);color:var(--blue,#4338CA)}' +
    '.jzab-msg{max-width:90%;font-size:14.5px;line-height:1.6;padding:11px 14px;border-radius:13px;white-space:pre-wrap}' +
    '.jzab-msg.me{align-self:flex-end;background:linear-gradient(135deg,var(--blue,#4338CA),#6366F1);color:#fff;border-bottom-right-radius:5px}' +
    '.jzab-msg.ai{align-self:flex-start;background:var(--bg-2,#f7f8fb);border:1px solid var(--line,#e6e8ef);color:var(--ink,#0b1020);border-bottom-left-radius:5px}' +
    '.jzab-who{align-self:flex-start;font-size:11px;font-weight:700;color:var(--ink-3,#8a92a6);margin:-6px 0 -8px;display:flex;align-items:center;gap:6px}' +
    '.jzab-typing{align-self:flex-start;display:inline-flex;gap:5px;padding:13px 15px;background:var(--bg-2,#f7f8fb);border:1px solid var(--line,#e6e8ef);border-radius:13px;border-bottom-left-radius:5px}' +
    '.jzab-typing i{width:7px;height:7px;border-radius:50%;background:var(--blue,#4338CA);opacity:.5;animation:jzab-bln 1.1s infinite}' +
    '.jzab-typing i:nth-child(2){animation-delay:.15s}.jzab-typing i:nth-child(3){animation-delay:.3s}' +
    '@keyframes jzab-bln{0%,80%,100%{transform:translateY(0);opacity:.4}40%{transform:translateY(-4px);opacity:1}}' +
    '@media(prefers-reduced-motion:reduce){.jzab-typing i{animation:none}}' +
    '.jzab-wait{align-self:flex-start;font-size:11.5px;color:var(--ink-3,#8a92a6);margin-top:-8px}' +
    '.jzab-cards{align-self:stretch;display:grid;grid-template-columns:1fr 1fr;gap:9px}' +
    '@media(max-width:520px){.jzab-cards{grid-template-columns:1fr}}' +
    '.jzab-card{display:flex;align-items:center;gap:11px;padding:11px 13px;border:1px solid var(--line,#e6e8ef);border-radius:12px;background:var(--bg,#fff);text-decoration:none;color:inherit;transition:border-color .2s,transform .2s,box-shadow .2s}' +
    '.jzab-card:hover{border-color:var(--blue,#4338CA);transform:translateY(-2px);box-shadow:0 10px 26px rgba(67,56,202,.12)}' +
    '.jzab-card .ci{width:34px;height:34px;flex:0 0 34px;border-radius:9px;display:grid;place-items:center;color:var(--blue,#4338CA);background:rgba(67,56,202,.09);font-size:15px}' +
    '.jzab-card .ct{font-size:13.5px;font-weight:700;color:var(--ink,#0b1020)}' +
    '.jzab-card .cd{font-size:11.5px;color:var(--ink-3,#8a92a6);margin-top:2px;line-height:1.4}' +
    '.jzab-card .cgo{margin-left:auto;color:var(--ink-3,#bcc2d0);font-size:12px}' +
    '.jzab-ev{align-self:stretch;border:1px solid var(--line,#e6e8ef);border-radius:12px;overflow:hidden}' +
    '.jzab-ev-h{font-size:11px;font-weight:700;color:var(--ink-2,#5A6478);padding:8px 12px;background:var(--bg-2,#f7f8fb);border-bottom:1px solid var(--line-2,#eef0f5);display:flex;align-items:center;gap:6px}' +
    '.jzab-ev-i{padding:9px 12px;border-bottom:1px solid var(--line-2,#f1f2f6)}' +
    '.jzab-ev-i:last-child{border-bottom:none}' +
    '.jzab-ev-t{font-size:12.5px;color:var(--ink,#0b1020);margin-bottom:5px}' +
    '.jzab-bar{height:5px;border-radius:3px;background:var(--line-2,#eef0f5);overflow:hidden}' +
    '.jzab-bar i{display:block;height:100%;border-radius:3px;background:linear-gradient(90deg,var(--blue,#4338CA),#6366F1)}' +
    '.jzab-bar+span{font-size:10.5px;color:var(--ink-3,#8a92a6);margin-top:3px;display:inline-block}' +
    '.jzab-log{align-self:stretch;display:flex;gap:11px;padding:12px 13px;border:1px solid #2c6045;border-radius:12px;background:rgba(45,212,191,.08)}' +
    '.jzab-log .li{width:30px;height:30px;flex:0 0 30px;border-radius:8px;display:grid;place-items:center;color:#0F766E;background:rgba(45,212,191,.16);font-size:14px}' +
    '.jzab-log .lt{font-size:13px;font-weight:700;color:var(--ink,#0b1020)}' +
    '.jzab-log .ld{font-size:11.5px;color:var(--ink-2,#5A6478);margin-top:2px;line-height:1.5}' +
    '.jzab-cta{align-self:flex-start;display:inline-flex;align-items:center;gap:7px;font-size:13px;font-weight:700;color:#fff;background:var(--blue,#4338CA);border:none;border-radius:999px;padding:9px 16px;cursor:pointer;text-decoration:none}' +
    '.jzab-foot{font-size:11px;color:var(--ink-3,#bcc2d0);text-align:center;padding:8px;border-top:1px solid var(--line-2,#eef0f5)}';

  var st = document.createElement('style'); st.textContent = css; document.head.appendChild(st);

  // ---- DOM ----
  function el(tag, cls, html) { var d = document.createElement(tag); if (cls) d.className = cls; if (html != null) d.innerHTML = html; return d; }
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }

  var ov = el('div', 'jzab-ov'); ov.setAttribute('role', 'dialog'); ov.setAttribute('aria-modal', 'true'); ov.setAttribute('aria-label', '问句子 · AI 对话');
  ov.innerHTML =
    '<div class="jzab-panel">' +
    '  <div class="jzab-head"><span class="jzab-sp"><i class="fa-solid fa-wand-magic-sparkles"></i></span>' +
    '    <input class="jzab-in" type="text" placeholder="问句子的 AI 员工任何事，或试试下面…" aria-label="输入你的问题" autocomplete="off" />' +
    '    <button class="jzab-x" aria-label="关闭 (Esc)">Esc</button></div>' +
    '  <div class="jzab-ctx" hidden></div>' +
    '  <div class="jzab-body" role="log" aria-live="polite" aria-relevant="additions" data-lenis-prevent></div>' +
    '  <div class="jzab-foot">命中常见问题秒答 · 其余实时问真 AI 客服（可能十几秒）</div>' +
    '</div>';
  document.body.appendChild(ov);
  var inp = ov.querySelector('.jzab-in'), body = ov.querySelector('.jzab-body'), ctx = ov.querySelector('.jzab-ctx');
  var busy = false, lastFocus = null, started = false;

  function pageCtx() { var c = window.PAGE_CTX; return (c && c.entity) ? c : null; }
  function scroll() { body.scrollTop = body.scrollHeight; }

  function open() {
    if (ov.classList.contains('open')) return;
    lastFocus = document.activeElement;
    var c = pageCtx();
    if (c) { ctx.hidden = false; ctx.innerHTML = '<i class="fa-solid fa-location-crosshairs"></i> 正在看：<b>' + esc(c.title || c.entity) + '</b> · 可直接就它追问'; }
    else { ctx.hidden = true; }
    if (!started) { greet(); started = true; }
    ov.classList.add('open'); document.body.style.overflow = 'hidden';
    setTimeout(function () { inp.focus(); }, 30);
  }
  function close() { ov.classList.remove('open'); document.body.style.overflow = ''; if (lastFocus && lastFocus.focus) lastFocus.focus(); }

  function greet() {
    var c = pageCtx();
    var hi = c ? ('你好，关于「' + (c.title || c.entity) + '」想了解什么？或问我任何关于 AI 员工怎么落地的问题。')
                : '你好，我是句子的 AI 客服 👋 问我任何关于 AI 员工怎么落地的问题——区别、接入、数据安全、价格、各产品/岗位都行。';
    addAI(hi);
    suggest();
  }
  function suggest() {
    var c = pageCtx();
    var qs = c ? ['它和普通方案有什么区别？', '接入要多久？', '能接我的渠道吗？', '预约一场演示']
               : ['和普通客服机器人有什么区别？', '接入要多久？', '数据安全吗？', '有哪些 AI 员工？'];
    var wrap = el('div', 'jzab-chips');
    qs.forEach(function (q) { var b = el('button', 'jzab-chip', esc(q)); b.onclick = function () { sendText(q); }; wrap.appendChild(b); });
    body.appendChild(wrap); scroll();
  }
  function clearChips() { body.querySelectorAll('.jzab-chips').forEach(function (n) { n.remove(); }); }

  function addMe(t) { var d = el('div', 'jzab-msg me', esc(t)); body.appendChild(d); scroll(); }
  function addAI(t) { var w = el('div', 'jzab-who', '<i class="fa-solid fa-wand-magic-sparkles"></i> 小句 · AI 客服'); var d = el('div', 'jzab-msg ai', esc(t)); body.appendChild(w); body.appendChild(d); scroll(); return d; }
  function addCards(keys) {
    if (!keys || !keys.length) return;
    var wrap = el('div', 'jzab-cards');
    keys.forEach(function (k) {
      var e = ENT[k]; if (!e) return;
      var a = el('a', 'jzab-card');
      a.href = e.href;
      a.innerHTML = '<span class="ci"><i class="fa-solid ' + e.ic + '"></i></span><span><span class="ct">' + esc(e.nm) + '</span><span class="cd">' + esc(e.ds) + '</span></span><span class="cgo"><i class="fa-solid fa-arrow-right"></i></span>';
      wrap.appendChild(a);
    });
    body.appendChild(wrap); scroll();
  }
  function addEvidence(refs) {
    if (!refs || !refs.length) return;
    var box = el('div', 'jzab-ev');
    var h = el('div', 'jzab-ev-h', '<i class="fa-solid fa-quote-right"></i> 这条回答的依据（来自知识库）');
    box.appendChild(h);
    refs.slice(0, 3).forEach(function (r) {
      var pct = r.similarity ? Math.round(parseFloat(r.similarity) * 100) : null;
      var i = el('div', 'jzab-ev-i');
      i.innerHTML = '<div class="jzab-ev-t">' + esc(r.label || '知识库条目') + '</div>' +
        (pct != null ? '<div class="jzab-bar"><i style="width:' + pct + '%"></i></div><span>匹配度 ' + pct + '%</span>' : '');
      box.appendChild(i);
    });
    body.appendChild(box); scroll();
  }
  function addLog() {
    var w = el('div', 'jzab-log');
    w.innerHTML = '<span class="li"><i class="fa-solid fa-user-shield"></i></span><span><span class="lt">AI 判断：该问题超出我的授权范围 → 转接真人</span><span class="ld">这正是「句子守护」管着的事：能说什么提前写死，没把握就转人工、全程留痕。留个联系方式，顾问带你的行业场景来对接。</span></span>';
    body.appendChild(w); scroll();
  }
  function addLead(label) {
    var b = el('a', 'jzab-cta', '<i class="fa-solid fa-headset"></i> ' + esc(label || '预约真人演示'));
    b.href = 'javascript:void 0';
    b.onclick = function () { close(); if (window.openContact) window.openContact('对话层'); };
    body.appendChild(b); scroll();
  }

  function matchRoute(t) { for (var i = 0; i < ROUTES.length; i++) if (ROUTES[i].re.test(t)) return ROUTES[i]; return null; }

  function sendText(v) {
    v = (v || '').trim(); if (!v || busy) return;
    clearChips(); addMe(v);
    var r = matchRoute(v);
    if (r) { // 命中意图：秒回 + 实体卡（对话即导航）
      busy = true;
      var t = typing();
      setTimeout(function () {
        t.remove(); addAI(r.a); if (r.cards) addCards(r.cards); if (r.lead) addLead('预约演示'); suggest(); busy = false;
      }, reduce ? 120 : 480);
      return;
    }
    askReal(v); // 自由输入：真 agent
  }
  function typing() { var d = el('div', 'jzab-typing', '<i></i><i></i><i></i>'); body.appendChild(d); scroll(); return d; }

  function askReal(v) {
    busy = true;
    var t = typing(), note, nt = setTimeout(function () { note = el('div', 'jzab-wait', '正在问真实 AI 客服，可能要十几秒…'); body.appendChild(note); scroll(); }, reduce ? 800 : 3200);
    var c = pageCtx();
    var msg = c ? ('【我正在看' + (c.type === 'product' ? '产品' : c.type === 'workforce' ? 'AI 员工' : '页面') + '：' + (c.title || c.entity) + '】' + v) : v;
    var done = function () { clearTimeout(nt); t.remove(); if (note) note.remove(); };
    fetch(API, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ sessionId: SID, message: msg }) })
      .then(function (r) { return r.ok ? r.json() : (r.status === 429 ? { code: -429 } : Promise.reject(0)); })
      .then(function (j) {
        done();
        if (j && j.code === 0 && j.data) {
          addAI(j.data.message || '（这个问题我先帮你转给真人顾问）');
          if (j.data.references && j.data.references.length) addEvidence(j.data.references);
          if (j.data.handover) { addLog(); addLead('转真人 · 预约演示'); }
          suggest();
        } else if (j && j.code === -429) { addAI('问得有点快，喘口气再问我～'); }
        else throw 0;
      })
      .catch(function () {
        done();
        var r = matchRoute(v);
        addAI(r ? r.a : '我这会儿没连上，先帮你转给真人顾问吧～');
        if (r && r.cards) addCards(r.cards);
        addLead('预约真人演示');
      })
      .then(function () { busy = false; });
  }

  // ---- 触发器与快捷键 ----
  function mountTriggers() {
    // 导航右侧加「问句子 ⌘K」药丸（若存在 .nav-right）
    var nr = document.querySelector('.nav-right');
    if (nr && !nr.querySelector('.jzab-trigger')) {
      var isMac = /Mac|iPhone|iPad/.test(navigator.platform || navigator.userAgent);
      var b = el('button', 'jzab-trigger', '<i class="fa-solid fa-wand-magic-sparkles"></i> 问句子 <span class="jzab-kbd">' + (isMac ? '⌘K' : 'Ctrl K') + '</span>');
      b.type = 'button'; b.setAttribute('aria-haspopup', 'dialog'); b.onclick = open;
      nr.insertBefore(b, nr.firstChild);
    }
    // 常驻浮动入口（所有页兜底）
    if (!document.querySelector('.jzab-fab')) {
      var f = el('button', 'jzab-fab', '<i class="fa-solid fa-wand-magic-sparkles"></i><span>问句子</span>');
      f.type = 'button'; f.setAttribute('aria-haspopup', 'dialog'); f.setAttribute('aria-label', '问句子 · 打开 AI 对话'); f.onclick = open;
      document.body.appendChild(f);
    }
  }

  inp.addEventListener('keydown', function (e) { if (e.key === 'Enter') { e.preventDefault(); var v = inp.value; inp.value = ''; sendText(v); } });
  ov.querySelector('.jzab-x').onclick = close;
  ov.addEventListener('click', function (e) { if (e.target === ov) close(); });
  document.addEventListener('keydown', function (e) {
    if ((e.metaKey || e.ctrlKey) && (e.key === 'k' || e.key === 'K')) { e.preventDefault(); ov.classList.contains('open') ? close() : open(); }
    else if (e.key === 'Escape' && ov.classList.contains('open')) close();
  });

  // nav 由 site.js 异步注入，稍候再挂触发器
  if (document.readyState !== 'loading') { mountTriggers(); setTimeout(mountTriggers, 400); }
  else document.addEventListener('DOMContentLoaded', function () { mountTriggers(); setTimeout(mountTriggers, 400); });

  window.openAskbar = open; // 供页面其它入口调用（如 Fleet "和这位 AI 员工聊"）
})();
