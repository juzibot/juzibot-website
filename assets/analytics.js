/* ============================================================================
   JuziBot 官网 DataFinder 埋点层
   - 静态站点专用：无构建、无依赖
   - 事件名严格沿用原官网口径：page_view / button_click
   ========================================================================== */
(function () {
  if (window.JZAnalytics && window.JZAnalytics.__installed) return;

  var RAW_CONFIG = window.JZ_ANALYTICS_CONFIG || {};
  var SDK_URL = 'https://lf3-data.volccdn.com/obj/data-static/log-sdk/collect/5.0/collect-rangers-v5.2.11.js';
  var CONFIG = {
    appId: String(RAW_CONFIG.app_id || RAW_CONFIG.appId || '20011391'),
    channel: RAW_CONFIG.channel || 'cn',
    channelDomain: RAW_CONFIG.channel_domain || RAW_CONFIG.channelDomain || 'https://gator.volces.com',
    sdkUrl: RAW_CONFIG.sdk_url || RAW_CONFIG.sdkUrl || SDK_URL,
    enabled: RAW_CONFIG.enabled !== false,
    debug: !!RAW_CONFIG.debug || /(?:^|[?&])jz_analytics_debug=1(?:&|$)/.test(location.search)
  };

  var VISIT_KEY = 'jz_visit_id';
  var LANDING_KEY = 'jz_landing_url';
  var REF_KEY = 'jz_referrer';
  var SID = getOrSetSession(VISIT_KEY, 'v');
  var started = false;
  var lastQrAt = 0;
  var wrappedOpenContact = false;
  var EVENT_PAGE_VIEW = 'page_view';
  var EVENT_BUTTON_CLICK = 'button_click';

  var PAGE_BY_ENTITY = {
    home: { first_menu: '首页', second_menu: '首页', entity_type: 'home', entity_name: '首页' },
    miaohui: { first_menu: '产品', second_menu: '句子秒回', entity_type: 'product', entity_name: '句子秒回 · 工作台' },
    miaodong: { first_menu: '产品', second_menu: '句子秒懂', entity_type: 'product', entity_name: '句子秒懂 · 大脑' },
    shouhu: { first_menu: '产品', second_menu: '句子守护', entity_type: 'product', entity_name: '句子守护 · 主管' },
    mio: { first_menu: '产品', second_menu: 'Mio', entity_type: 'product', entity_name: 'Mio · AI 办公坐席' },
    canmou: { first_menu: '产品', second_menu: 'Mio', entity_type: 'product', entity_name: 'Mio · AI 办公坐席' },
    dongxing: { first_menu: '产品', second_menu: '句子懂行', entity_type: 'product', entity_name: '句子懂行 · 记忆' },
    cli: { first_menu: '产品', second_menu: '句子 CLI', entity_type: 'product', entity_name: '句子 CLI · 手' },
    zhizao: { first_menu: '产品', second_menu: '句子制造', entity_type: 'product', entity_name: '句子制造 · 地基' },
    sales: { first_menu: 'AI 员工', second_menu: 'AI 销售', entity_type: 'workforce', entity_name: 'AI 销售' },
    marketing: { first_menu: 'AI 员工', second_menu: 'AI 导购', entity_type: 'workforce', entity_name: 'AI 导购' },
    service: { first_menu: 'AI 员工', second_menu: 'AI 客服', entity_type: 'workforce', entity_name: 'AI 客服' },
    government: { first_menu: 'AI 员工', second_menu: 'AI 社工 / 调解员', entity_type: 'workforce', entity_name: 'AI 社工 / 调解员' },
    finance: { first_menu: 'AI 员工', second_menu: 'AI 理财顾问', entity_type: 'workforce', entity_name: 'AI 理财顾问' },
    hr: { first_menu: 'AI 员工', second_menu: 'AI HR', entity_type: 'workforce', entity_name: 'AI HR' },
    geo: { first_menu: 'AI 员工', second_menu: 'GEO 优化师', entity_type: 'workforce', entity_name: 'GEO 优化师' },
    industries: { first_menu: '客户与行业', second_menu: '客户与行业', entity_type: 'page', entity_name: '客户与行业' },
    enterprise: { first_menu: '企业级能力', second_menu: '企业级能力', entity_type: 'page', entity_name: '企业级能力' },
    fde: { first_menu: 'FDE 交付结果', second_menu: 'FDE 交付结果', entity_type: 'page', entity_name: 'FDE 交付结果' },
    about: { first_menu: 'AI 原生组织', second_menu: 'AI 原生组织', entity_type: 'page', entity_name: 'AI 原生组织' },
    careers: { first_menu: '加入我们', second_menu: '加入我们', entity_type: 'page', entity_name: '加入我们' }
  };

  var PAGE_BY_PATH = {
    '/': 'home',
    '/index.html': 'home',
    '/products/miaohui.html': 'miaohui',
    '/products/miaodong.html': 'miaodong',
    '/products/shouhu.html': 'shouhu',
    '/products/mio.html': 'mio',
    '/products/canmou.html': 'canmou',
    '/products/dongxing.html': 'dongxing',
    '/products/cli.html': 'cli',
    '/products/zhizao.html': 'zhizao',
    '/workforce/sales.html': 'sales',
    '/workforce/marketing.html': 'marketing',
    '/workforce/service.html': 'service',
    '/workforce/government.html': 'government',
    '/workforce/finance.html': 'finance',
    '/workforce/hr.html': 'hr',
    '/workforce/geo.html': 'geo',
    '/industries.html': 'industries',
    '/enterprise.html': 'enterprise',
    '/fde.html': 'fde',
    '/about.html': 'about',
    '/careers/index.html': 'careers',
    '/careers/': 'careers'
  };

  var HOME_SCREENS = [
    { id: 'why-now', index: 1, name: '为什么是现在' },
    { id: 'paradigm', index: 2, name: '范式转变' },
    { id: 'products', index: 3, name: '七大产品基建' },
    { id: 'howwework', index: 4, name: '我们怎么工作' },
    { id: 'workforce', index: 5, name: 'AI 员工' },
    { id: 'industries', index: 6, name: '客户与行业' },
    { id: 'factory', index: 7, name: '交付工厂' },
    { id: 'enterprise', index: 8, name: '企业级能力' },
    { id: 'moat', index: 9, name: '护城河' },
    { id: 'cta', index: 10, name: '联系我们' }
  ];

  function nowId(prefix) {
    return prefix + '-' + Date.now().toString(36) + '-' + Math.random().toString(36).slice(2, 8);
  }

  function getOrSetSession(key, prefix) {
    try {
      var existing = sessionStorage.getItem(key);
      if (existing) return existing;
      var value = nowId(prefix);
      sessionStorage.setItem(key, value);
      return value;
    } catch (_) {
      return nowId(prefix);
    }
  }

  function getOrSetLanding(key, value) {
    try {
      var existing = sessionStorage.getItem(key);
      if (existing) return existing;
      sessionStorage.setItem(key, value || '');
      return value || '';
    } catch (_) {
      return value || '';
    }
  }

  function params() {
    var out = {};
    try {
      var sp = new URLSearchParams(location.search);
      ['utm_source', 'utm_medium', 'utm_campaign', 'utm_content', 'utm_term'].forEach(function (k) {
        if (sp.has(k)) out[k] = sp.get(k);
      });
    } catch (_) {}
    return out;
  }

  function normalizePath() {
    var path = location.pathname || '/';
    path = path.replace(/\/{2,}/g, '/');
    if (path !== '/' && /\/$/.test(path)) path = path.replace(/\/$/, '/');
    return path || '/';
  }

  function pageMeta() {
    var ctx = window.PAGE_CTX || {};
    var entity = ctx.entity || PAGE_BY_PATH[normalizePath()] || '';
    if (!entity && /\/careers\/?$/.test(normalizePath())) entity = 'careers';
    var meta = PAGE_BY_ENTITY[entity] || {
      first_menu: ctx.type || '其他页面',
      second_menu: ctx.title || document.title || normalizePath(),
      entity_type: ctx.type || 'page',
      entity_name: ctx.title || document.title || normalizePath()
    };
    return {
      first_menu: meta.first_menu,
      second_menu: meta.second_menu,
      page_entity: entity || ctx.entity || '',
      page_entity_type: ctx.type || meta.entity_type,
      page_entity_name: ctx.title || meta.entity_name
    };
  }

  function commonProps() {
    var meta = pageMeta();
    getOrSetLanding(LANDING_KEY, location.href);
    getOrSetLanding(REF_KEY, document.referrer || '');
    return merge({
      app_type: '官网',
      zone: 'Z区',
      first_menu: meta.first_menu,
      second_menu: meta.second_menu
    }, params());
  }

  function merge(a, b) {
    var out = {}, k;
    for (k in a) if (Object.prototype.hasOwnProperty.call(a, k)) out[k] = a[k];
    for (k in b) if (Object.prototype.hasOwnProperty.call(b, k)) out[k] = b[k];
    return out;
  }

  function cleanProps(props) {
    var out = {};
    props = props || {};
    Object.keys(props).forEach(function (key) {
      var value = props[key];
      if (value === undefined || value === null) return;
      if (typeof value === 'string') {
        value = value.trim();
        if (!value) return;
        if (value.length > 1000) value = value.slice(0, 1000);
      } else if (typeof value !== 'number' && typeof value !== 'boolean') {
        value = String(value);
      }
      out[key] = value;
    });
    return out;
  }

  function log() {
    if (!CONFIG.debug || !window.console) return;
    console.log.apply(console, arguments);
  }

  function installStub() {
    var exportObj = 'collectEvent';
    window.LogAnalyticsObject = exportObj;
    if (!window[exportObj]) {
      var collect = function () { collect.q.push(arguments); };
      collect.q = collect.q || [];
      window[exportObj] = collect;
    }
    window[exportObj].l = Number(new Date());
  }

  function loadSdk() {
    if (document.querySelector('script[data-jz-df-sdk]')) return;
    var script = document.createElement('script');
    script.src = CONFIG.sdkUrl;
    script.async = true;
    script.setAttribute('data-jz-df-sdk', '1');
    script.onload = function () { log('[JZAnalytics] SDK loaded'); };
    script.onerror = function () { log('[JZAnalytics] SDK load failed'); };
    (document.head || document.body).appendChild(script);
  }

  function ce() {
    if (!CONFIG.enabled) return;
    if (!window.collectEvent) installStub();
    window.collectEvent.apply(window, arguments);
  }

  function init() {
    if (started) return;
    started = true;
    if (!CONFIG.enabled || !CONFIG.appId || !CONFIG.channelDomain) {
      log('[JZAnalytics] disabled: missing config');
      return;
    }
    installStub();
    ce('init', {
      app_id: /^\d+$/.test(CONFIG.appId) ? Number(CONFIG.appId) : CONFIG.appId,
      channel: CONFIG.channel,
      channel_domain: CONFIG.channelDomain,
      log: CONFIG.debug,
      autotrack: false,
      disable_auto_pv: true
    });
    ce('config', cleanProps({
      app_type: '官网',
      zone: 'Z区',
      site_name: '句子互动官网'
    }));
    ce('start');
    loadSdk();
  }

  function track(eventName, props) {
    init();
    if (eventName !== EVENT_PAGE_VIEW && eventName !== EVENT_BUTTON_CLICK) {
      log('[JZAnalytics] ignored unsupported event', eventName);
      return;
    }
    var payload = cleanProps(merge(commonProps(), props || {}));
    log('[JZAnalytics]', eventName, payload);
    ce(eventName, payload);
  }

  function trackPage() {
    track(EVENT_PAGE_VIEW, {
      view_type: 'page',
      page_title: document.title || '',
      page_path: normalizePath()
    });
  }

  function areaFromSource(source) {
    source = source || '';
    if (/导航/.test(source)) return '顶部导航栏';
    if (/开屏弹窗/.test(source)) return '开屏弹窗';
    if (/悬浮/.test(source)) return '右侧悬浮';
    if (/Hero对话|首屏对话/.test(source)) return '首屏对话区';
    if (/Hero|首屏/.test(source)) return '首屏';
    if (/AI员工/.test(source)) return 'AI 员工卡片';
    if (/页头/.test(source)) return '页头';
    if (/底部CTA|底部/.test(source)) return '页面底部';
    if (/对话层/.test(source)) return '问句子对话层';
    return '页面按钮';
  }

  function inferButtonName(source, explicit) {
    var name = explicit || '';
    source = source || '';
    if (name) return name;
    if (/GEO诊断/.test(source)) return 'GEO诊断';
    if (/免费演示|30 分钟/.test(source)) return '预约 30 分钟演示';
    if (/获取方案/.test(source)) return '获取行业解决方案';
    if (/咨询产品|咨询/.test(source)) return '咨询产品';
    if (/联系|联系我们/.test(source)) return '联系我们';
    return '预约演示';
  }

  function trackButton(name, source, extra) {
    extra = extra || {};
    source = source || extra.button_source || '';
    var buttonName = inferButtonName(source, name || extra.button_name);
    track(EVENT_BUTTON_CLICK, merge({
      button_name: buttonName,
      button_source: source || buttonName,
      button_area: extra.button_area || areaFromSource(source),
      target_url: extra.target_url || ''
    }, extra));
  }

  function trackQuestion(question, extra) {
    extra = extra || {};
    if (!question) return;
    var source = extra.question_source || extra.button_source || '';
    trackButton('问句子提交', source || '问句子', merge({
      button_area: extra.question_surface || extra.surface || '问句子',
      question_text: question,
      question_surface: extra.question_surface || extra.surface || '问句子',
      question_session_id: extra.question_session_id || extra.session_id || SID,
      question_source: source
    }, extra));
  }

  function trackQrExposure(source, extra) {
    var now = Date.now();
    if (now - lastQrAt < 500) return;
    lastQrAt = now;
    extra = extra || {};
    var surface = extra.qr_surface || '企业微信二维码弹窗';
    trackButton('企业微信二维码曝光', source || extra.trigger_source || surface, merge({
      button_area: surface,
      qr_surface: extra.qr_surface || '企业微信二维码弹窗',
      trigger_source: source || extra.trigger_source || '',
      exposure_target: '企业微信二维码'
    }, extra));
  }

  function closest(el, selector) {
    while (el && el !== document) {
      if (el.matches && el.matches(selector)) return el;
      el = el.parentNode;
    }
    return null;
  }

  function bindClickTracking() {
    document.addEventListener('click', function (e) {
      var el = closest(e.target, '[data-track-click], [data-track-name], .nav-login');
      if (!el) return;
      var href = el.getAttribute('href') || '';
      var name = el.getAttribute('data-track-name') || (el.classList && el.classList.contains('nav-login') ? '登录 / 注册' : textOf(el));
      var source = el.getAttribute('data-track-source') || (el.classList && el.classList.contains('nav-login') ? '导航·登录注册' : '');
      var area = el.getAttribute('data-track-area') || areaFromSource(source);
      trackButton(name, source, {
        button_area: area,
        target_url: href && href.indexOf('javascript:') !== 0 ? href : ''
      });
      if (shouldDelayNavigation(e, el, href)) {
        e.preventDefault();
        setTimeout(function () { location.href = href; }, 120);
      }
    }, true);
  }

  function shouldDelayNavigation(e, el, href) {
    if (!href || href.charAt(0) === '#' || href.indexOf('javascript:') === 0) return false;
    if (e.defaultPrevented || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return false;
    if ((el.getAttribute('target') || '').toLowerCase() === '_blank') return false;
    return /^https?:\/\//.test(href);
  }

  function textOf(el) {
    return (el.getAttribute('aria-label') || el.textContent || '').replace(/\s+/g, ' ').trim();
  }

  function wrapOpenContact() {
    if (wrappedOpenContact || typeof window.openContact !== 'function') return;
    var original = window.openContact;
    if (original.__jzAnalyticsWrapped) return;
    window.openContact = function (source, buttonName) {
      source = source || '联系我们';
      var modal = document.getElementById('contactModal');
      if (modal) modal.__jzQrSource = source;
      trackButton(buttonName, source, { button_source: source });
      var result = original.apply(this, arguments);
      setTimeout(function () { trackQrExposure(source); }, 40);
      return result;
    };
    window.openContact.__jzAnalyticsWrapped = true;
    wrappedOpenContact = true;
  }

  function observeContactModal() {
    var modal = document.getElementById('contactModal');
    if (!modal || !window.MutationObserver) return;
    var wasOpen = modal.classList.contains('open');
    var mo = new MutationObserver(function () {
      var open = modal.classList.contains('open');
      if (open && !wasOpen) trackQrExposure(modal.__jzQrSource || '企业微信二维码弹窗');
      wasOpen = open;
    });
    mo.observe(modal, { attributes: true, attributeFilter: ['class'] });
  }

  function bindHomeScreens() {
    var meta = pageMeta();
    if (meta.page_entity !== 'home') return;
    var seen = {};
    function fire(item) {
      if (seen[item.id]) return;
      seen[item.id] = true;
      track(EVENT_PAGE_VIEW, {
        view_type: 'home_screen',
        screen_index: item.index,
        screen_name: item.name,
        screen_id: item.id
      });
    }
    if ('IntersectionObserver' in window) {
      var io = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
          if (!entry.isIntersecting) return;
          var item = entry.target.__jzScreen;
          if (item) {
            fire(item);
            io.unobserve(entry.target);
          }
        });
      }, { threshold: 0.42, rootMargin: '0px 0px -8% 0px' });
      HOME_SCREENS.forEach(function (item) {
        var el = document.getElementById(item.id);
        if (!el) return;
        el.__jzScreen = item;
        io.observe(el);
      });
    } else {
      var onScroll = function () {
        HOME_SCREENS.forEach(function (item) {
          var el = document.getElementById(item.id);
          if (!el || seen[item.id]) return;
          var r = el.getBoundingClientRect();
          if (r.top < window.innerHeight * 0.68 && r.bottom > window.innerHeight * 0.24) fire(item);
        });
      };
      window.addEventListener('scroll', onScroll, { passive: true });
      window.addEventListener('resize', onScroll);
      onScroll();
    }
  }

  function onReady(fn) {
    if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', fn);
    else fn();
  }

  window.JZAnalytics = {
    __installed: true,
    config: CONFIG,
    track: track,
    trackButton: trackButton,
    trackQuestion: trackQuestion,
    trackQrExposure: trackQrExposure,
    wrapOpenContact: wrapOpenContact
  };

  init();
  onReady(function () {
    trackPage();
    bindClickTracking();
    wrapOpenContact();
    observeContactModal();
    bindHomeScreens();
    setTimeout(wrapOpenContact, 300);
  });
})();
