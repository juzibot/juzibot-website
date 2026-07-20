/* ===================================================================
   juzi-nemo 站点共享层 · 单一真源
   - 注入统一 NAV / FOOTER / CONTACT 弹窗（按 window.SITE_REL 适配层级）
   - 通用交互：导航滚动浮起 / 移动菜单 / 进入视口揭示(.rv) / 弹窗
   用法（每个子页）：
     <head> 里 <link rel="stylesheet" href="{REL}assets/site.css">
     <body> 顶部 <div id="site-nav"></div>，底部 <div id="site-footer"></div>
     </body> 前： <script>window.SITE_REL='{REL}'</script><script src="{REL}assets/site.js"></script>
     其中 REL：根目录页 = ''，products/ workforce/ careers/ 等一级子目录 = '../'
   =================================================================== */
(function () {
  var REL = (typeof window.SITE_REL === 'string') ? window.SITE_REL : '';

  var NAV = '' +
    '<nav class="nav" id="nav">' +
    '  <a href="' + REL + 'index.html" class="brand">' +
    '    <img class="brand-logo" src="' + REL + 'logo.png" alt="句子互动" width="29" height="29" decoding="async" />' +
    '    句子互动 <small>JuziBot</small>' +
    '  </a>' +
    '  <div class="nav-links">' +
    '    <div class="nav-item">' +
    '      <button>产品 <span class="caret"></span></button>' +
    '      <div class="dropdown wide">' +
    '        <a href="' + REL + 'products/miaodong.html"><div class="d-title">句子秒懂 · 大脑</div><div class="d-desc">业务人员不写代码也能搭 Agent</div></a>' +
    '        <a href="' + REL + 'products/shouhu.html"><div class="d-title">句子守护 · 主管</div><div class="d-desc">Agent 上线前测过、上线后管着</div></a>' +
    '        <a href="' + REL + 'products/canmou.html"><div class="d-title">句子问数 · 参谋</div><div class="d-desc">一句话查所有业务数据</div></a>' +
    '        <a href="' + REL + 'products/dongxing.html"><div class="d-title">句子懂行 · 知识中枢</div><div class="d-desc">把原始资料变成 AI 能用的干净知识</div></a>' +
    '        <a href="' + REL + 'products/miaohui.html"><div class="d-title">句子秒回 · 工作台</div><div class="d-desc">11 个 IM 通道汇成一个工作台</div></a>' +
    '        <a href="' + REL + 'products/cli.html"><div class="d-title">句子 CLI · 手</div><div class="d-desc">操作一切人用软件的执行层</div></a>' +
    '        <a href="' + REL + 'products/zhizao.html"><div class="d-title">句子制造 · 地基</div><div class="d-desc">补齐客户数字化基建，一客一环境</div></a>' +
    '      </div>' +
    '    </div>' +
    '    <div class="nav-item">' +
    '      <button>AI 员工 <span class="caret"></span></button>' +
    '      <div class="dropdown wide">' +
    '        <a href="' + REL + 'workforce/sales.html"><div class="d-title">AI 销售</div><div class="d-desc">直播搬家、私域承接、漏斗跟进——首单成交全程接管</div></a>' +
    '        <a href="' + REL + 'workforce/marketing.html"><div class="d-title">AI 导购</div><div class="d-desc">头部零售品牌的私域导购运营，长尾客户也覆盖</div></a>' +
    '        <a href="' + REL + 'workforce/service.html"><div class="d-title">AI 客服</div><div class="d-desc">从售前到售后都接得住 · 5 年 BadCase 积累</div></a>' +
    '        <a href="' + REL + 'workforce/government.html"><div class="d-title">AI 社工 / 调解员</div><div class="d-desc">政务高合规要求 + 全程可追溯 · 已稳步落地</div></a>' +
    '        <a href="' + REL + 'workforce/finance.html"><div class="d-title">AI 理财顾问</div><div class="d-desc">银行 / 证券 / 保险头部机构落地 · 多年风控话术</div></a>' +
    '        <a href="' + REL + 'workforce/hr.html"><div class="d-title">AI HR</div><div class="d-desc">简历初筛 + AI 语音面试，HR 只看 Top 20%</div></a>' +
    '        <a href="' + REL + 'workforce/geo.html"><div class="d-title">GEO 优化师</div><div class="d-desc">GEO 让品牌被 AI 推荐，公域到私域跑完全域营销</div></a>' +
    '      </div>' +
    '    </div>' +
    '    <div class="nav-item"><a href="' + REL + 'industries.html">客户与行业</a></div>' +
    '    <div class="nav-item"><a href="' + REL + 'enterprise.html">企业级能力</a></div>' +
    '    <div class="nav-item"><a href="' + REL + 'fde.html">FDE 交付结果</a></div>' +
    '    <div class="nav-item"><a href="' + REL + 'about.html">AI 原生组织</a></div>' +
    '    <div class="nav-item"><a href="' + REL + 'careers/index.html">加入我们</a></div>' +
    '  </div>' +
    '  <div class="nav-right">' +
    '    <a class="nav-cta" style="cursor:pointer" onclick="openContact(\'导航·联系我们\')">联系我们 →</a>' +
    '    <a href="https://az-bg.juzibot.com/auth/register" class="nav-login">登录 / 注册</a>' +
    '  </div>' +
    '  <button class="nav-burger" aria-label="菜单" onclick="this.closest(\'.nav\').classList.toggle(\'menu-open\')">' +
    '    <svg class="bg-open" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 7h16M4 12h16M4 17h16"/></svg>' +
    '    <svg class="bg-close" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M6 6l12 12M18 6L6 18"/></svg>' +
    '  </button>' +
    '</nav>';

  var FOOTER = '' +
    '<footer>' +
    '  <div class="wrap">' +
    '    <div class="footer-grid">' +
    '      <div class="brand-block">' +
    '        <div class="brand"><img class="brand-logo" src="' + REL + 'logo.png" alt="句子互动" width="29" height="29" decoding="async" /> 句子互动 <small>JuziBot</small></div>' +
    '        <p>为企业部署 AI 员工。<br/>1000+ 家中国企业在用 · 覆盖 5 大高合规行业。</p>' +
    '      </div>' +
    '      <div><h6>产品 · 7 个</h6><ul>' +
    '        <li><a href="' + REL + 'products/miaohui.html">句子秒回 · 工作台</a></li>' +
    '        <li><a href="' + REL + 'products/miaodong.html">句子秒懂 · 大脑</a></li>' +
    '        <li><a href="' + REL + 'products/shouhu.html">句子守护 · 主管</a></li>' +
    '        <li><a href="' + REL + 'products/canmou.html">句子问数 · 参谋</a></li>' +
    '        <li><a href="' + REL + 'products/dongxing.html">句子懂行 · 知识中枢</a></li>' +
    '        <li><a href="' + REL + 'products/cli.html">句子 CLI · 手</a></li>' +
    '        <li><a href="' + REL + 'products/zhizao.html">句子制造 · 地基</a></li>' +
    '      </ul></div>' +
    '      <div><h6>AI 员工</h6><ul>' +
    '        <li><a href="' + REL + 'workforce/sales.html">AI 销售</a></li>' +
    '        <li><a href="' + REL + 'workforce/marketing.html">AI 导购</a></li>' +
    '        <li><a href="' + REL + 'workforce/service.html">AI 客服</a></li>' +
    '        <li><a href="' + REL + 'workforce/government.html">AI 社工 / 调解员</a></li>' +
    '        <li><a href="' + REL + 'workforce/finance.html">AI 理财顾问</a></li>' +
    '        <li><a href="' + REL + 'workforce/hr.html">AI HR</a></li>' +
    '        <li><a href="' + REL + 'workforce/geo.html">GEO 优化师</a></li>' +
    '      </ul></div>' +
    '      <div><h6>行业</h6><ul>' +
    '        <li><a href="' + REL + 'industries.html#education">在线教育</a></li>' +
    '        <li><a href="' + REL + 'industries.html#ecommerce">消费品电商</a></li>' +
    '        <li><a href="' + REL + 'industries.html#finance">金融</a></li>' +
    '        <li><a href="' + REL + 'industries.html#gov">政务 · 司法</a></li>' +
    '        <li><a href="' + REL + 'industries.html#internet">泛互联网</a></li>' +
    '      </ul></div>' +
    '      <div><h6>公司</h6><ul>' +
    '        <li><a href="' + REL + 'fde.html">FDE 交付结果</a></li>' +
    '        <li><a href="' + REL + 'industries.html">客户与行业</a></li>' +
    '        <li><a href="' + REL + 'about.html">AI 原生组织</a></li>' +
    '        <li><a href="' + REL + 'careers/index.html">加入我们</a></li>' +
    '      </ul></div>' +
    '    </div>' +
    '    <div class="footer-bottom">' +
    '      <div>Copyright © 2019 北京句子互动科技有限公司　京ICP备19049435号-1　京公网安备 11010802033527号</div>' +
    '      <div>为企业部署 AI 员工</div>' +
    '    </div>' +
    '  </div>' +
    '</footer>';

  var CONTACT = '' +
    '<div class="modal-overlay" id="contactModal">' +
    '  <div class="modal modal-qr" role="dialog" aria-modal="true">' +
    '    <button class="qr-close" onclick="closeModal(\'contactModal\')" aria-label="关闭">×</button>' +
    '    <div class="qr-eyebrow">联系我们</div>' +
    '    <h3 class="qr-title">扫码加企业微信</h3>' +
    '    <img class="qr-img" src="' + REL + 'assets/brand/qr-qiwei.png" alt="企业微信二维码" width="200" height="200" />' +
    '    <p class="qr-note">直接和我们聊，工作日当天回复</p>' +
    '  </div>' +
    '</div>';

  // ---- 注入 ----
  function mount() {
    var n = document.getElementById('site-nav'); if (n) n.outerHTML = NAV;
    var f = document.getElementById('site-footer'); if (f) f.outerHTML = FOOTER;
    document.body.insertAdjacentHTML('beforeend', CONTACT);
    wire();
    // 全站对话层：加载 askbar.js（AI-native 大改核心）
    if (!window.__jzab && !document.querySelector('script[data-jzab]')) {
      var s = document.createElement('script'); s.src = REL + 'assets/askbar.js'; s.defer = true; s.setAttribute('data-jzab', '1'); document.body.appendChild(s);
    }
  }

  // ---- 全局弹窗 API（nav 内联 onclick 依赖）----
  window.openModal = function (id) { var el = document.getElementById(id); if (el) { el.classList.add('open'); document.body.style.overflow = 'hidden'; } };
  window.closeModal = function (id) { var el = document.getElementById(id); if (el) { el.classList.remove('open'); document.body.style.overflow = ''; } };
  window.openContact = function () { window.openModal('contactModal'); };

  function wire() {
    var nav = document.getElementById('nav');
    if (nav) {
      var onScroll = function () { nav.classList.toggle('float', window.scrollY > 20); };
      onScroll(); window.addEventListener('scroll', onScroll, { passive: true });
      nav.querySelectorAll('.nav-links a').forEach(function (a) { a.addEventListener('click', function () { nav.classList.remove('menu-open'); }); });
    }
    // 点遮罩 / Esc 关弹窗
    document.querySelectorAll('.modal-overlay').forEach(function (ov) {
      ov.addEventListener('click', function (e) { if (e.target === ov) window.closeModal(ov.id); });
    });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape') document.querySelectorAll('.modal-overlay.open').forEach(function (m) { window.closeModal(m.id); }); });
    // 进入视口揭示
    var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion:reduce)').matches;
    if ('IntersectionObserver' in window && !reduce) {
      document.documentElement.classList.add('anim');
      var io = new IntersectionObserver(function (es) { es.forEach(function (en) { if (en.isIntersecting) { en.target.classList.add('in'); io.unobserve(en.target); } }); }, { rootMargin: '0px 0px -10% 0px', threshold: .12 });
      document.querySelectorAll('.rv').forEach(function (el) { io.observe(el); });
    }
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', mount);
  else mount();
})();
