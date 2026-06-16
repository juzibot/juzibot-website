"""
Generate all sub-pages from structured data.
Pages: products/{miaohui,miaodong,shouhu}.html, workforce/{6 roles}.html, enterprise.html
"""
import os, sys, html

ROOT = os.path.dirname(os.path.abspath(__file__))


# ────────────────────────── shared snippets ──────────────────────────

def nav_html(rel):
    """Site navigation incl. both dropdowns, login/contact, burger.

    Identical across every page except the `rel` path prefix (Req 8.3, 8.5).
    Dropdown triggers are real <button>s so the menus reveal on hover AND
    keyboard focus via the CSS :focus-within rule (Req 4.3, 11.3). The burger
    and contact trigger carry accessible names (Req 11.3). rel: '' for root,
    '../' for /products and /workforce subdirs.
    """
    products = [
        ("products/miaodong.html", "句子秒懂 · 大脑", "业务人员不写代码也能搭 Agent"),
        ("products/shouhu.html", "句子守护 · 主管", "Agent 上线前测过、上线后管着"),
        ("products/canmou.html", "句子参谋 · 参谋", "对话式数据洞察，一句话问数"),
        ("products/dongxing.html", "句子智库 · 记忆", "知识工程，把散乱知识炼成可检索资产"),
        ("products/miaohui.html", "句子秒回 · 工位", "Agent 和人协作的 IM 工作台"),
        ("products/cli.html", "句子 CLI · 手", "操作一切人用软件的执行层"),
        ("products/zhizao.html", "句子智造 · 地基", "补齐客户数字化基建，一客一环境"),
    ]
    workforce = [
        ("workforce/sales.html", "AI 销售", "直播搬家、私域承接、漏斗跟进——首单成交全程接管"),
        ("workforce/marketing.html", "AI 导购", "头部零售品牌的私域导购运营，长尾客户也覆盖"),
        ("workforce/service.html", "AI 客服", "从售前到售后都接得住 · 5 年 BadCase 积累"),
        ("workforce/government.html", "AI 社工 / 调解员", "政务高合规要求 + 全程可追溯 · 已稳步落地"),
        ("workforce/finance.html", "AI 理财顾问", "银行 / 证券 / 保险头部机构落地 · 多年风控话术"),
        ("workforce/hr.html", "AI HR", "简历初筛 + AI 语音面试，HR 只看 Top 20%"),
    ]

    def dropdown_links(items):
        return '\n          '.join(
            f'<a class="dropdown-link" href="{rel}{href}">'
            f'<span class="dropdown-title">{title}</span>'
            f'<span class="dropdown-desc">{desc}</span></a>'
            for href, title, desc in items
        )

    top_links = [
        ("industries.html", "客户与行业"),
        ("enterprise.html", "企业级能力"),
        ("fde.html", "FDE 交付结果"),
        ("about.html", "AI 原生组织"),
        ("careers/index.html", "加入我们"),
    ]
    top_links_html = '\n      '.join(
        f'<div class="nav-item"><a href="{rel}{href}">{label}</a></div>'
        for href, label in top_links
    )

    return f"""
<nav class="nav">
  <div class="container nav-inner">
    <a href="{rel}index.html" class="brand">
      <img class="brand-mark" src="/assets/brand/logo.png" alt="句子互动" width="30" height="30" />
      句子互动 <small>JuziBot</small>
    </a>
    <div class="nav-links">
      <div class="nav-item">
        <button type="button" class="nav-trigger" aria-haspopup="true">产品 <span class="nav-caret"></span></button>
        <div class="dropdown dropdown--wide">
          {dropdown_links(products)}
        </div>
      </div>
      <div class="nav-item">
        <button type="button" class="nav-trigger" aria-haspopup="true">AI 员工 <span class="nav-caret"></span></button>
        <div class="dropdown dropdown--wide">
          {dropdown_links(workforce)}
        </div>
      </div>
      {top_links_html}
    </div>
    <div class="nav-right">
      <a class="nav-cta" style="cursor:pointer" role="button" tabindex="0" aria-label="联系我们" onclick="openContact('导航·联系我们')">联系我们 →</a>
      <a href="https://insight.juzibot.com/auth/login?from=juzibot.com&amp;type=register" class="nav-login">登录 / 注册</a>
    </div>
    <button class="nav-burger" type="button" aria-label="菜单" aria-expanded="false">☰</button>
  </div>
</nav>
""".strip()


def footer_html(rel):
    """Footer with product/industry/company columns.

    Shared across pages with path-prefix-only variance (Req 8.3, 10.5).
    """
    return f"""
<footer class="site-footer">
  <div class="container">
    <div class="footer-grid">
      <div class="footer-brand">
        <div class="brand">
          <img class="brand-mark" src="/assets/brand/logo.png" alt="句子互动" width="30" height="30" />
          句子互动 <small>JuziBot</small>
        </div>
        <p>为企业部署 AI 员工。<br/>1000+ 家中国企业在用 · 覆盖 5 大高合规行业。</p>
      </div>
      <div class="footer-col">
        <h6>产品 · 7 个</h6>
        <ul>
          <li><a href="{rel}products/miaohui.html">句子秒回 · 工位</a></li>
          <li><a href="{rel}products/miaodong.html">句子秒懂 · 大脑</a></li>
          <li><a href="{rel}products/shouhu.html">句子守护 · 主管</a></li>
          <li><a href="{rel}products/canmou.html">句子参谋 · 参谋</a></li>
          <li><a href="{rel}products/dongxing.html">句子智库 · 记忆</a></li>
          <li><a href="{rel}products/cli.html">句子 CLI · 手</a></li>
          <li><a href="{rel}products/zhizao.html">句子智造 · 地基</a></li>
        </ul>
      </div>
      <div class="footer-col">
        <h6>行业</h6>
        <ul>
          <li><a href="{rel}industries.html#education">在线教育</a></li>
          <li><a href="{rel}industries.html#ecommerce">消费品电商</a></li>
          <li><a href="{rel}industries.html#finance">金融</a></li>
          <li><a href="{rel}industries.html#gov">政务 · 司法</a></li>
          <li><a href="{rel}industries.html#internet">泛互联网</a></li>
        </ul>
      </div>
      <div class="footer-col">
        <h6>公司</h6>
        <ul>
          <li><a href="{rel}fde.html">FDE 交付结果</a></li>
          <li><a href="{rel}industries.html">客户与行业</a></li>
          <li><a href="{rel}about.html">AI 原生组织</a></li>
          <li><a href="{rel}index.html#cta">联系我们</a></li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      <div>Copyright © 2019 北京句子互动科技有限公司　京ICP备19049435号-1　京公网安备 11010802033527号</div>
      <div>为企业部署 AI 员工</div>
    </div>
  </div>
</footer>
""".strip()


def announcement_html():
    """Scrolling marquee announcement bar (Req 7.1, 8.5).

    The message set is rendered twice into the track so the -50% CSS translate
    loop is seamless and no message is truncated. Every message string is from
    the Preserved_Content set (verbatim).
    """
    messages = [
        ("在线教育", "几百家头部公司已部署，AI 销售人均承接 5 倍以上"),
        ("消费品电商", "几百家头部品牌私域导购上线，长尾客户再不流失"),
        ("金融", "银行 · 证券 · 保险头部机构落地，合规边界提前写死"),
        (None, "1000+ 大型企业已在用 · 扎在这 5 个行业 · 接入 10+ 主流 IM 渠道"),
        ("在线教育", "几百家头部公司已部署，AI 销售人均承接 5× 以上"),
        ("消费品电商", "几百家头部品牌私域导购上线，长尾客户再不流失"),
        ("金融", "银行 · 证券 · 保险头部机构落地，合规边界提前写死"),
        (None, "1000+ 大型企业已在用 · 扎在这 5 个行业 · 接入 10+ 主流 IM 渠道"),
    ]

    def item(tag, text):
        tag_html = f'<span class="marquee-tag">{tag}</span>' if tag else ''
        return (f'<span class="marquee-item">'
                f'<span class="marquee-dot"></span>{tag_html}{text}</span>')

    items = '\n      '.join(item(tag, text) for tag, text in messages)
    return f"""
<div class="announcement" aria-label="公告">
  <div class="marquee-track">
      {items}
      {items}
  </div>
</div>
""".strip()


def contact_module(rel):
    """Floating panel + contact modal markup (Req 7.2, 7.3, 7.4, 7.5, 11.3, 11.4).

    Single shared snippet reused across every page; only the QR `rel` prefix
    varies. The floating panel is hidden + non-interactive until the inline JS
    adds `.is-visible` past 200px of scroll. The modal exposes the official QR
    Preserved_Asset; its close control carries an accessible name.
    """
    return f"""
<!-- ════════════ FLOATING PANEL ════════════ -->
<div class="floating-panel" aria-label="快捷联系">
  <button type="button" class="fp-btn" aria-label="在线咨询" onclick="openContact('悬浮·在线咨询','在线咨询')">
    <span class="fp-icon">💬</span>在线<br/>咨询
    <span class="fp-tip">在线咨询</span>
  </button>
  <button type="button" class="fp-btn fp-btn--2" aria-label="预约 Demo 演示" onclick="openContact('悬浮·预约演示','预约演示')">
    <span class="fp-icon">📅</span>预约<br/>演示
    <span class="fp-tip">预约 Demo 演示</span>
  </button>
  <button type="button" class="fp-btn fp-btn--3" aria-label="获取行业解决方案" onclick="openContact('悬浮·获取方案','获取方案')">
    <span class="fp-icon">📋</span>获取<br/>方案
    <span class="fp-tip">获取行业解决方案</span>
  </button>
</div>

<!-- ════════════ CONTACT MODAL ════════════ -->
<div class="modal-overlay" id="contactModal">
  <div class="modal modal--qr" role="dialog" aria-modal="true" aria-labelledby="contactModalTitle">
    <button type="button" class="modal-close" onclick="closeModal()" aria-label="关闭">×</button>
    <div class="modal-eyebrow">联系我们</div>
    <h2 class="modal-title" id="contactModalTitle">扫码加企业微信</h2>
    <img class="modal-qr-img" src="{rel}assets/brand/qr-qiwei.png" alt="企业微信二维码" width="200" height="200" />
    <p class="modal-note">直接和我们聊，工作日当天回复</p>
  </div>
</div>
""".strip()


def behavior_script():
    """Dependency-free inline JS shared by every page (Req 7.x, 9.2, 11.4).

    Covers: contact modal open/close (X, overlay click, Escape) with scroll
    lock + restore; burger toggle; mobile dropdown accordion (desktop relies on
    CSS hover/focus only); floating-panel scroll threshold. The marquee needs no
    JS — it is duplicated in markup. The 句子秒懂 demo `fit()` routine ships
    inline with that page body and is preserved separately (Req 7.8).
    """
    return """
<script>
(function(){
  var savedScroll = 0;
  var overlay = document.querySelector('.modal-overlay');

  // Contact modal (Req 7.2, 7.3, 11.4) — lock body scroll, remember + restore position
  window.openContact = function(){
    if(!overlay) return;
    savedScroll = window.pageYOffset || document.documentElement.scrollTop || 0;
    overlay.classList.add('is-open');
    document.body.style.overflow = 'hidden';
  };
  window.closeModal = function(){
    if(!overlay) return;
    overlay.classList.remove('is-open');
    document.body.style.overflow = '';
    window.scrollTo(0, savedScroll);
  };
  if(overlay){
    overlay.addEventListener('click', function(e){ if(e.target === overlay) window.closeModal(); });
  }
  document.addEventListener('keydown', function(e){
    if((e.key === 'Escape' || e.key === 'Esc') && overlay && overlay.classList.contains('is-open')) window.closeModal();
  });

  // Burger toggle (Req 7.7)
  Array.prototype.forEach.call(document.querySelectorAll('.nav-burger'), function(b){
    b.addEventListener('click', function(){
      var nav = b.closest('.nav');
      if(!nav) return;
      var open = nav.classList.toggle('nav-open');
      b.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
  });

  // Mobile dropdown accordion (Req 7.6) — desktop reveal is pure CSS hover/focus
  Array.prototype.forEach.call(document.querySelectorAll('.nav-trigger'), function(t){
    t.addEventListener('click', function(){
      var item = t.closest('.nav-item');
      if(item) item.classList.toggle('is-open');
    });
  });

  // Floating panel scroll threshold (Req 7.4, 7.5)
  var panel = document.querySelector('.floating-panel');
  function syncPanel(){
    if(!panel) return;
    var y = window.pageYOffset || document.documentElement.scrollTop || 0;
    if(y > 200) panel.classList.add('is-visible');
    else panel.classList.remove('is-visible');
  }
  window.addEventListener('scroll', syncPanel, {passive:true});
  syncPanel();
})();
</script>
""".strip()


def cta_band(text="把第一个 AI 员工装进你的业务流程",
             sub="从一个 AI 角色起步，逐步扩展到多个 Agent。90 天内，第一个 AI 员工即在客户的 IM 中上岗。",
             button="预约演示", source="底部CTA·预约演示", intent="预约演示"):
    """Inline call-to-action band on a solid accent fill (Req 3.3).

    The button sits on the accent surface, so it uses the canonical
    `.btn-on-accent` variant rather than a page-local override (Req 10.1).
    """
    return f"""
<div class="cta-band">
  <div>
    <h4>{text}</h4>
    <p>{sub}</p>
  </div>
  <button type="button" class="btn btn-on-accent" onclick="openContact('{source}','{intent}')">{button} <span class="btn-arrow">→</span></button>
</div>
""".strip()


def page_layout(*, title, description, rel, breadcrumbs, hero_kicker, hero_h1, hero_lede,
                pills, body):
    """Generate a complete sub-page shell with semantic landmarks (Req 10.4).

    Exactly one <main>, plus <header> (announcement + nav), <nav> (inside the
    header), and <footer>. Document language is `zh-CN` (Req 2.4). The caller
    supplies a unique, bounded title (1–60 chars) and description (1–160 chars)
    per page (Req 10.2). Shared regions vary only by the `rel` path prefix
    (Req 8.3, 8.5).
    """
    crumbs_html = ' <span class="sep">/</span> '.join(
        f'<a href="{href}">{label}</a>' if href else f'<span class="here">{label}</span>'
        for label, href in breadcrumbs
    )
    kicker_html = ''
    if hero_kicker:
        kicker_html = f'<div class="kicker"><span class="dot"></span>{hero_kicker}</div>'
    pills_html = ''
    if pills:
        pills_html = '<div class="pill-row">' + ''.join(
            f'<span class="pill"><span class="dot"></span>{p}</span>' for p in pills
        ) + '</div>'

    return f"""<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8" />
<link rel="icon" href="/favicon.ico" />
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover" />
<title>{title}</title>
<meta name="description" content="{description}" />
<link rel="stylesheet" href="{rel}assets/style.css">
</head>
<body>

<header>
{announcement_html()}

{nav_html(rel)}
</header>

<main>
<section class="page-hero">
  <div class="container">
    <div class="crumbs">{crumbs_html}</div>
    {kicker_html}
    <h1>{hero_h1}</h1>
    <p class="lede">{hero_lede}</p>
    {pills_html}
  </div>
</section>

{body}
</main>

{footer_html(rel)}

{contact_module(rel)}

{behavior_script()}

</body>
</html>
"""


# ════════════════════════ shared structured snippets ════════════════════════
# Each structured component below is ONE reusable function emitting the canonical
# class contract from the rebuilt Design_System (assets/style.css). They are
# reused by every page body — no per-page duplicated component markup
# (Req 5.4, 8.5). Functions that emit <img> take an explicit alt so informative
# assets get a non-empty text alternative and decorative assets get alt=""
# (Req 11.1, 11.2).

# Maps the legacy short colour codes still passed by page bodies onto the three
# canonical accent variants of the feature-icon tile.
_ICON_ACCENT = {'bl': '', 'or': ' feature-icon--2', 'gr': ' feature-icon--3',
                'pu': ' feature-icon--3', 'te': ' feature-icon--3'}


def image(src, alt="", *, width=None, height=None, cls=None, loading="lazy"):
    """Single <img> helper with explicit text-alternative handling (Req 11.1, 11.2).

    `alt` is ALWAYS emitted: pass a non-empty description for an informative
    image, or alt="" for a purely decorative one so assistive tech skips it.
    """
    attrs = [f'src="{src}"', f'alt="{alt}"']
    if cls:
        attrs.insert(0, f'class="{cls}"')
    if width:
        attrs.append(f'width="{width}"')
    if height:
        attrs.append(f'height="{height}"')
    if loading:
        attrs.append(f'loading="{loading}"')
    return f'<img {" ".join(attrs)} />'


def block(eyebrow, title, sub, content, alt=False, start=False):
    """Section wrapper + eyebrow/title/sub head (snippet: block).

    Emits `.block` (`.block--muted` when alt) > `.block-head`
    (`.block-head--start` when start) with `.block-eyebrow` / `.block-title`
    (accept inline `.accent` spans) / `.block-sub`, wrapped in `.container`.
    """
    sec_cls = "block block--muted" if alt else "block"
    head_cls = "block-head block-head--start" if start else "block-head"
    eyebrow_html = f'<div class="block-eyebrow">{eyebrow}</div>' if eyebrow else ''
    title_html = f'<h2 class="block-title">{title}</h2>' if title else ''
    sub_html = f'<p class="block-sub">{sub}</p>' if sub else ''
    return f"""
<section class="{sec_cls}">
  <div class="container">
    <div class="{head_cls}">
      {eyebrow_html}
      {title_html}
      {sub_html}
    </div>
    {content}
  </div>
</section>
""".strip()


def feat_grid(items, cols=3):
    """Responsive grid of canonical feature cards (snippet: feat_grid).

    items: list of (icon, title, desc, color_class[, punch]) tuples. The icon
    is rendered inside the `.feature-icon` tile; color_class selects the accent
    variant; an optional 5th element renders a `.feature-punch` footer line.
    """
    cards = []
    for it in items:
        icon, title, desc, color = it[0], it[1], it[2], it[3]
        punch = it[4] if len(it) > 4 else None
        icon_cls = _ICON_ACCENT.get(color, '')
        punch_html = f'<div class="feature-punch">{punch}</div>' if punch else ''
        cards.append(
            f'<div class="card card--hover feature-card">'
            f'<div class="feature-icon{icon_cls}">{icon}</div>'
            f'<h3 class="feature-title">{title}</h3>'
            f'<p class="feature-desc">{desc}</p>'
            f'{punch_html}'
            f'</div>'
        )
    grid_cls = f"feature-grid feature-grid--{cols}"
    return f'<div class="{grid_cls}">{"".join(cards)}</div>'


def feature_list(items, check=False):
    """Scannable accent-marked list (snippet: feature_list, Req 5.1).

    Lets a >60-word block be re-presented as a structured list without dropping
    any string. `check=True` swaps the bar marker for a check glyph.
    """
    cls = "feature-list feature-list--check" if check else "feature-list"
    lis = ''.join(f'<li>{i}</li>' for i in items)
    return f'<ul class="{cls}">{lis}</ul>'


def kpi_row(items):
    """Metric strip (snippet: kpi_row). items: list of (value, label)."""
    cells = ''.join(
        f'<div class="kpi"><div class="kpi-value">{v}</div><div class="kpi-label">{l}</div></div>'
        for v, l in items
    )
    return f'<div class="kpi-row">{cells}</div>'


def split_section(*, eyebrow, title, paragraphs, bullets=None, visual_html=None,
                   media_img=None, media_alt="", color="bl", reverse=False,
                   bullets_check=False):
    """Two-column text + media block (snippet: split_section).

    Emits `.split` (`.split--reverse` when reverse) > `.split-body`
    (`.block-eyebrow` + h3 + paragraphs + optional `.feature-list`) and
    `.split-media`. Supply EITHER `media_img` (an asset path — pass a non-empty
    `media_alt` when informative, "" when decorative, Req 11.1/11.2) OR raw
    `visual_html` (a custom inline visual). `color` is accepted for call-site
    compatibility but the canonical media surface no longer tints by colour.
    """
    p_html = ''.join(f'<p>{p}</p>' for p in paragraphs)
    bullets_html = feature_list(bullets, check=bullets_check) if bullets else ''
    media_inner = image(media_img, media_alt) if media_img else (visual_html or '')
    split_cls = "split split--reverse" if reverse else "split"
    eyebrow_html = f'<div class="block-eyebrow">{eyebrow}</div>' if eyebrow else ''
    return f"""
<section class="block">
  <div class="container">
    <div class="{split_cls}">
      <div class="split-body">
        {eyebrow_html}
        <h3>{title}</h3>
        {p_html}
        {bullets_html}
      </div>
      <div class="split-media">
        {media_inner}
      </div>
    </div>
  </div>
</section>
""".strip()


def comparison_table(headers, rows):
    """Semantic comparison table in a horizontal-scroll wrapper (snippet: comparison_table).

    headers: list of column header strings (the first labels the row-header
    column). rows: list of row tuples whose first element is the row header and
    whose remaining cells are either a string or a (text, is_positive) tuple;
    positive cells get the `.is-positive` class.
    """
    head_cells = ''.join(f'<th scope="col">{h}</th>' for h in headers)
    thead = f'<thead><tr>{head_cells}</tr></thead>'
    body_rows = []
    for row in rows:
        row_head, cells = row[0], row[1:]
        tds = []
        for cell in cells:
            if isinstance(cell, (tuple, list)):
                text, positive = cell[0], (len(cell) > 1 and cell[1])
            else:
                text, positive = cell, False
            cls = ' class="is-positive"' if positive else ''
            tds.append(f'<td{cls}>{text}</td>')
        body_rows.append(
            f'<tr><th scope="row">{row_head}</th>{"".join(tds)}</tr>'
        )
    tbody = f'<tbody>{"".join(body_rows)}</tbody>'
    return f'<div class="comparison-table"><table>{thead}{tbody}</table></div>'


def timeline(items):
    """Vertical timeline (snippet: timeline). items: list of (year, body)."""
    lis = ''.join(
        f'<li class="timeline-item">'
        f'<div class="timeline-year">{year}</div>'
        f'<div class="timeline-body">{body}</div>'
        f'</li>'
        for year, body in items
    )
    return f'<ul class="timeline">{lis}</ul>'


def tag_categories(groups):
    """Grouped tag clusters (snippet: tag_categories).

    groups: list of (group_title, tags) where each tag is either a string or a
    (text, is_accent) tuple; accent tags get the `.tag--accent` variant.
    """
    blocks = []
    for group_title, tags in groups:
        chips = []
        for tag in tags:
            if isinstance(tag, (tuple, list)):
                text, accent = tag[0], (len(tag) > 1 and tag[1])
            else:
                text, accent = tag, False
            cls = "tag tag--accent" if accent else "tag"
            chips.append(f'<span class="{cls}">{text}</span>')
        blocks.append(
            f'<div class="tag-group">'
            f'<div class="tag-group-title">{group_title}</div>'
            f'<div class="tag-list">{"".join(chips)}</div>'
            f'</div>'
        )
    return f'<div class="tag-categories">{"".join(blocks)}</div>'


def faq_accordion(items):
    """Native <details>/<summary> FAQ, no JS required (snippet: faq_accordion, Req 9.2).

    items: list of (question, answer).
    """
    details = ''.join(
        f'<details class="faq-item">'
        f'<summary class="faq-q">{q}</summary>'
        f'<div class="faq-a">{a}</div>'
        f'</details>'
        for q, a in items
    )
    return f'<div class="faq-accordion">{details}</div>'


def cta_section(*, title="把第一个 AI 员工装进你的业务流程",
                sub="从一个 AI 角色起步，逐步扩展到多个 Agent。90 天内，第一个 AI 员工即在客户的 IM 中上岗。",
                primary="预约演示", secondary=None,
                source="底部CTA·预约演示", intent="预约演示"):
    """Full-width closing CTA on a solid accent fill (snippet: cta_section).

    Emits `.cta-section` > `.container` with title/sub and a `.cta-actions`
    row. On-accent buttons use the canonical `.btn-on-accent` /
    `.btn-on-accent-outline` variants (Req 10.1).
    """
    secondary_html = ''
    if secondary:
        secondary_html = (
            f'<button type="button" class="btn btn-on-accent-outline" '
            f'onclick="openContact(\'{source}·{secondary}\',\'{secondary}\')">{secondary}</button>'
        )
    return f"""
<section class="cta-section">
  <div class="container">
    <h2>{title}</h2>
    <p class="sub">{sub}</p>
    <div class="cta-actions">
      <button type="button" class="btn btn-on-accent" onclick="openContact('{source}','{intent}')">{primary} <span class="btn-arrow">→</span></button>
      {secondary_html}
    </div>
  </div>
</section>
""".strip()


# ────────────────────────── page bodies ──────────────────────────

def page_miaohui():
    body = ''
    # NEW module order (Req 4.1): pre-redesign opened with the workbench mockup.
    # Here the capability grid leads; the IM-channel grid and the SOP "主动触达"
    # split follow; the 架构 split and the preserved .ui-mock workbench come
    # later; KPIs close the body. The mockup markup is captured here and placed
    # mid-body so the preserved interactive workbench stays intact (Req 7).
    mock_section = '''
<section class="product-shot-section">
  <div class="container">
    <div class="ui-mock">
      <div class="ui-topbar">
        <span class="ui-dot r"></span><span class="ui-dot y"></span><span class="ui-dot g"></span>
        <span class="ui-title">句子秒回 · 聚合聊天工作台</span>
        <span class="ui-tabs"><span class="on">聚合聊天</span><span>AI 运营</span><span>企业控制台</span></span>
      </div>
      <div class="ui-body">
        <div class="ui-rail">
          <div class="ui-rail-h">全部对话 · 12</div>
          <div class="ui-acct"><i class="ch xhs">书</i><div><b>小红书 · 客服1号</b><span>种草沟通</span></div><em>3</em></div>
          <div class="ui-acct"><i class="ch dy">音</i><div><b>抖音 · 销售2号</b><span>私信 + 直播</span></div><em>5</em></div>
          <div class="ui-acct on"><i class="ch wx">微</i><div><b>微信客服 · 客服1号</b><span>私域承接</span></div><em>2</em></div>
          <div class="ui-acct"><i class="ch wa">W</i><div><b>WhatsApp · 海外</b><span>海外业务</span></div></div>
          <div class="ui-acct"><i class="ch fs">飞</i><div><b>飞书 · 企业 IM</b><span>内部协同</span></div></div>
        </div>
        <div class="ui-chat">
          <div class="ui-chat-h"><b>王女士</b><span>微信客服 · 意向客户</span></div>
          <div class="ui-msgs">
            <div class="bub in">您好，看到课程介绍，想了解下体验课</div>
            <div class="bub out">您好～体验课本周开放预约，给您发个入口 👍</div>
            <div class="bub ai"><span class="ai-tag">AI 起草</span>已根据她的浏览记录推荐「国画体验课」，待确认发送</div>
          </div>
          <div class="ui-input">输入回复…<span class="ui-send">发送</span></div>
        </div>
        <div class="ui-side">
          <div class="ui-side-h">客户档案</div>
          <div class="ui-tagrow"><span>意向 · 高</span><span>到课 3 次</span><span>未续费</span></div>
          <div class="ui-side-h">AI 跟进建议</div>
          <div class="ui-sug">主推大师班，附续费优惠；建议 24 小时内一对一跟进。</div>
          <div class="ui-stat"><b>+38%</b><span>本月转化</span></div>
        </div>
      </div>
    </div>
  </div>
</section>
'''.strip()
    body += block(        "核心能力",
        "Agent 在 IM 通道上岗，需要的不止是聊天框",
        "句子秒回是 AI 员工的工位。11 个 IM 通道聚合到一个工作台，Agent 像真人一样工作、与同事协作，并接受统一管理。",
        feat_grid([
            ("01", "多平台聚合", "11 个 IM 通道（小红书、抖音、微信客服、微信公众号、小程序、WhatsApp、飞书、钉钉、TikTok、Instagram）统一到一个工作台，海内外账号一起管。", "bl"),
            ("02", "主动触达", "私聊 / 群聊群发、SOP 自动跟进、自动加好友、新客欢迎语——一次配置批量执行，不受原生应用群发次数限制。", "or"),
            ("03", "人机协作", "AI 全自动 / 人机协作 / 纯人工三种模式，AI 无法处理的对话自动转人工，每条消息可追溯。", "gr"),
            ("04", "员工协作", "一人管多账号、多人管一账号都支持。系统智能分配消息，管理者统一查看营销数据和员工绩效。", "pu"),
            ("05", "聊天历史", "每一条对话安全留存，支持按客户、关键词、时间多维搜索，导出方便后续分析。", "te"),
            ("06", "API 集成", "对接客户已有的 CRM / 工单 / 知识库系统，Agent 上岗就接管真实业务流，不孤立运行。", "bl"),
        ], cols=3),
    )

    body += block(        "11 个 IM 通道",
        "客户在哪个 IM 上，Agent 就去哪个 IM 上岗",
        "多年积累的 IM 通道适配。国内的、海外 WhatsApp 的、抖音直播私信、飞书企业 IM，一个工作台管完。",
        '<div style="display:grid;grid-template-columns:repeat(4,1fr);gap:14px;max-width:920px;margin:0 auto;">'
        + ''.join(
            f'<div style="padding:18px 16px;background:#fff;border:1px solid var(--gray-line);border-radius:12px;text-align:center;"><div style="font-size:24px;margin-bottom:6px;">{ic}</div><div style="font-size:13.5px;font-weight:700;">{n}</div><div style="font-size:11.5px;color:var(--gray-text);margin-top:2px;">{d}</div></div>'
            for ic, n, d in [
                ("📕", "小红书", "种草沟通"),
                ("🎵", "抖音", "私信 + 直播"),
                ("☎️", "电话", "外呼触达"),
                ("💬", "微信客服", "私域承接"),
                ("📟", "微信小程序", "客服入口"),
                ("☁️", "飞书", "企业 IM"),
                ("📱", "钉钉", "企业 IM"),
                ("📢", "微信公众号", "私域承接"),
                ("✉️", "WhatsApp", "海外业务"),
                ("🌍", "TikTok", "海外短视频"),
                ("📷", "Instagram", "海外种草"),
                ("➕", "...", "持续接入"),
            ]
        )
        + '</div>',
        alt=True,
    )

    body += split_section(
        eyebrow="主动触达",
        title="配一次，自动批量执行的 SOP 引擎",
        paragraphs=[
            "传统群发受 IM 平台规则限制：次数有限、时间窗口固定、无法定向。句子秒回的 SOP 引擎突破这些限制，Agent 按节奏持续跟进客户。",
        ],
        bullets=[
            "私聊 / 群聊群发：一次配置自动发给成百上千客户",
            "SOP 自动执行：Day 1 欢迎语、Day 3 产品介绍、Day 7 优惠券——按时间线推进",
            "自动加好友：批量导入目标客户，系统按节奏发申请",
            "新客欢迎语：添加好友后自动响应，避免冷场",
            "海内外账号一起管：海外业务也走同一套 SOP",
        ],
        visual_html="""
<div style="background:#fff;border-radius:12px;padding:18px;border:1px solid var(--gray-line);">
<div style="font-size:13px;font-weight:700;margin-bottom:14px;color:var(--blue);">SOP · 客户首次建联后跟进</div>
<div style="display:flex;flex-direction:column;gap:10px;font-size:13px;">
<div style="display:flex;align-items:center;gap:10px;"><div style="width:64px;font-size:11px;color:var(--gray-text);font-weight:700;">立即</div><div style="flex:1;background:var(--blue-light);padding:9px 13px;border-radius:8px;color:var(--blue);">发送欢迎语 + 产品介绍</div></div>
<div style="display:flex;align-items:center;gap:10px;"><div style="width:64px;font-size:11px;color:var(--gray-text);font-weight:700;">+ 1 天</div><div style="flex:1;background:var(--blue-light);padding:9px 13px;border-radius:8px;color:var(--blue);">关怀提醒 + 体验邀约</div></div>
<div style="display:flex;align-items:center;gap:10px;"><div style="width:64px;font-size:11px;color:var(--gray-text);font-weight:700;">+ 3 天</div><div style="flex:1;background:var(--orange-lt);padding:9px 13px;border-radius:8px;color:var(--orange);">未响应客户 → AI 二次跟进</div></div>
<div style="display:flex;align-items:center;gap:10px;"><div style="width:64px;font-size:11px;color:var(--gray-text);font-weight:700;">+ 7 天</div><div style="flex:1;background:var(--green-lt);padding:9px 13px;border-radius:8px;color:var(--green);">高意向客户 → 优惠券触发</div></div>
<div style="display:flex;align-items:center;gap:10px;"><div style="width:64px;font-size:11px;color:var(--gray-text);font-weight:700;">+ 14 天</div><div style="flex:1;background:var(--gray-bg);padding:9px 13px;border-radius:8px;color:var(--gray-text);">流失客户 → 召回话术</div></div>
</div>
</div>
""",
        color="or",
        reverse=True,
    )

    body += split_section(
        eyebrow="架构",
        title="两大控制台 + 两个工作台，覆盖企业全角色",
        paragraphs=[
            "句子秒回按企业组织结构搭协作系统。管理者、小组负责人、一线客服、AI 运营各有自己的入口，权限和数据分开。",
        ],
        bullets=[
            "<strong>企业控制台</strong>：管理者全局视角，跨小组操作，全公司数据看板",
            "<strong>小组控制台</strong>：小组负责人配置 SOP、群发、加好友、群运营",
            "<strong>聚合聊天工作台</strong>：客服 / 销售日常回复，AI 辅助 + 团队协作",
            "<strong>AI 运营工作台</strong>：AI 运营人员效果调优、数据洞察",
        ],
        visual_html="""
<div style="background:#fff;padding:22px;border-radius:14px;border:1px solid var(--gray-line);">
<div style="font-weight:800;color:var(--blue);margin-bottom:14px;font-size:13px;">句子互动 · 句子秒回 工作台</div>
<div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;">
  <div style="background:var(--blue-light);border-radius:10px;padding:14px;">
    <div style="font-weight:700;font-size:13px;color:var(--blue);">企业控制台</div>
    <div style="font-size:11px;color:var(--gray-text);margin-top:5px;">管理者 · 全局数据看板</div>
  </div>
  <div style="background:var(--orange-lt);border-radius:10px;padding:14px;">
    <div style="font-weight:700;font-size:13px;color:var(--orange);">小组控制台</div>
    <div style="font-size:11px;color:var(--gray-text);margin-top:5px;">运营组长 · 配 SOP / 群发</div>
  </div>
  <div style="background:var(--green-lt);border-radius:10px;padding:14px;">
    <div style="font-weight:700;font-size:13px;color:var(--green);">聚合聊天工作台</div>
    <div style="font-size:11px;color:var(--gray-text);margin-top:5px;">客服 / 销售 · 日常回复</div>
  </div>
  <div style="background:var(--purple-lt);border-radius:10px;padding:14px;">
    <div style="font-weight:700;font-size:13px;color:var(--purple);">AI 运营工作台</div>
    <div style="font-size:11px;color:var(--gray-text);margin-top:5px;">AI 运营 · 效果调优 / 洞察</div>
  </div>
</div>
</div>
""",
    )

    # Preserved interactive workbench mockup (Req 7), now placed mid-body.
    body += mock_section

    body += block(        "结果",
        "客户用句子秒回拿到的实际效果",
        "数据来自 多年部署的真实客户案例。",
        kpi_row([
            ("11 个", "已接入 IM 通道"),
            ("89%", "对话自动完成率"),
            ("5×", "人均承接客户量提升"),
            ("1000+", "企业客户验证"),
        ]),
    )

    body += f"""
<section class="section-block">
  <div class="container">
    {cta_band("把句子秒回装进你的 IM 通道")}
  </div>
</section>
""".strip()

    return page_layout(
        title="句子秒回 · IM 通道里的 AI 员工工位 | 句子互动",
        description="句子秒回是企业级多 IM 聚合管理平台——11 个 IM 通道一个工作台管完，AI 智能回复、SOP 自动跟进、人机协作。1000+ 企业客户验证。",
        rel="../",
        breadcrumbs=[("首页", "../index.html"), ("产品", None), ("句子秒回", None)],
        hero_kicker="产品 · 01",
        hero_h1='句子秒回 · <span class="accent">AI 员工的 IM 工位</span>',
        hero_lede="把企业的 11 个 IM 通道（小红书、抖音、微信客服、微信公众号、小程序、WhatsApp 等）聚合到一个工作台，<strong>Agent 真的在客户面前接管对话</strong>——主动触达、智能回复、人机协作、多平台一个工作台管完。",
        pills=["11 个 IM 通道", "1000+ 企业客户", "89% 对话自动完成率", "多年通道适配积累"],
        body=body,
    )


def page_miaodong():
    body = ''
    # NEW module order (Req 4.1): pre-redesign opened with the Canvas mockup.
    # Here the capability grid leads; the knowledge-base split and the industry
    #策略库 grid follow; the 智能体/工作流 split and the preserved Canvas demo
    # come later; KPIs close. The Canvas demo (with its fit() script) is captured
    # here and placed mid-body so the preserved interactive demo stays intact
    # (Req 7.8).
    mock_section = '''
<section class="product-shot-section">
  <div class="container">
    <div class="canvas-mock">
      <div class="cm-topbar">
        <span class="cm-back">‹</span>
        <span class="cm-logo">句</span>
        <span class="cm-ttl"><b>售前咨询 · Agent 工作流</b><i></i></span>
        <span class="cm-tbtns">
          <span class="cm-tbtn icon">◷</span>
          <span class="cm-tbtn hide-sm">隐藏上次运行结果</span>
          <span class="cm-tbtn hide-sm">复制</span>
          <span class="cm-tbtn pub">➤ 发布</span>
        </span>
      </div>
      <div class="cm-stage" data-w="1180" data-h="560">
        <div class="cm-scaler">
          <svg class="cm-links" viewBox="0 0 1180 560" preserveAspectRatio="none" aria-hidden="true">
            <path class="l1" d="M242 270 C301 270 301 125 360 125"/>
            <path class="l2" d="M242 270 C301 270 301 278 360 278"/>
            <path class="l3" d="M242 270 C301 270 301 448 360 448"/>
            <path class="l4" d="M596 125 C641 125 641 206 686 206"/>
            <path class="l5" d="M596 278 C641 278 641 399 686 399"/>
            <path class="l6" d="M596 448 C641 448 641 399 686 399"/>
            <path class="l7" d="M926 206 C946 206 946 399 966 399"/>
            <path class="l8" d="M922 399 C944 399 944 399 966 399"/>
            <circle cx="242" cy="270" r="3.5"/>
            <circle cx="360" cy="125" r="3.5"/><circle cx="596" cy="125" r="3.5"/>
            <circle cx="360" cy="278" r="3.5"/><circle cx="596" cy="278" r="3.5"/>
            <circle cx="360" cy="448" r="3.5"/><circle cx="596" cy="448" r="3.5"/>
            <circle cx="686" cy="206" r="3.5"/><circle cx="926" cy="206" r="3.5"/>
            <circle cx="686" cy="399" r="3.5"/><circle cx="922" cy="399" r="3.5"/>
            <circle cx="966" cy="399" r="3.5"/>
          </svg>

          <div class="cm-node d1" style="left:30px;top:200px;width:212px">
            <div class="cm-nhd"><span class="cm-ic ic-llm">✦</span><b>大模型</b><span class="cm-play">▷</span><span class="cm-more">···</span></div>
            <div class="cm-row"><span>输入</span><i class="bar"></i></div>
            <div class="cm-row"><span>输出</span><i class="bar"></i></div>
            <div class="cm-row"><span>模型</span><span class="cm-chip"><i class="md"></i>DeepSeek-V3</span></div>
          </div>

          <div class="cm-node d2" style="left:360px;top:70px;width:236px">
            <div class="cm-nhd"><span class="cm-ic ic-tool">⚙</span><b>MCP 工具</b><span class="cm-play">▷</span><span class="cm-more">···</span></div>
            <div class="cm-row"><span>输入</span><i class="bar"></i></div>
            <div class="cm-row"><span>输出</span><i class="bar"></i><i class="bar s"></i></div>
          </div>

          <div class="cm-node d3" style="left:360px;top:212px;width:236px">
            <div class="cm-nhd"><span class="cm-ic ic-kb">☰</span><b>知识库</b><span class="cm-play">▷</span><span class="cm-more">···</span></div>
            <div class="cm-row"><span>输入</span><i class="bar"></i></div>
            <div class="cm-row"><span>输出</span><i class="bar"></i></div>
            <div class="cm-row"><span>来源</span><span class="cm-chip">产品文档 · 247 篇</span></div>
          </div>

          <div class="cm-node d4" style="left:360px;top:382px;width:236px">
            <div class="cm-nhd"><span class="cm-ic ic-mem">◈</span><b>记忆</b><span class="cm-play">▷</span><span class="cm-more">···</span></div>
            <div class="cm-row"><span>输入</span><i class="bar"></i></div>
            <div class="cm-row"><span>输出</span><i class="bar"></i></div>
            <div class="cm-row"><span>读取</span><span class="cm-chip">客户档案 · 长期</span></div>
          </div>

          <div class="cm-node d5" style="left:686px;top:128px;width:240px">
            <div class="cm-nhd"><span class="cm-ic ic-agent">✺</span><b>Agent 推理</b><span class="cm-play">▷</span><span class="cm-more">···</span></div>
            <div class="cm-row"><span>输入</span><i class="bar"></i></div>
            <div class="cm-row"><span>输出</span><i class="bar"></i></div>
            <div class="cm-row"><span>模型</span><span class="cm-chip"><i class="md"></i>DeepSeek-V3</span></div>
            <div class="cm-row"><span>工具</span><span class="cm-chip">自动调用 · 4</span></div>
          </div>

          <div class="cm-node d6" style="left:686px;top:344px;width:236px">
            <div class="cm-nhd"><span class="cm-ic ic-code">‹›</span><b>代码</b><span class="cm-play">▷</span><span class="cm-more">···</span></div>
            <div class="cm-row"><span>输入</span><i class="bar"></i></div>
            <div class="cm-row"><span>输出</span><i class="bar"></i><i class="bar s"></i></div>
          </div>

          <div class="cm-node d7" style="left:966px;top:344px;width:198px">
            <div class="cm-nhd"><span class="cm-ic ic-end">■</span><b>End</b><span class="cm-play">▷</span><span class="cm-more">···</span></div>
            <div class="cm-row"><span>输出</span><i class="bar"></i></div>
            <div class="cm-row"><span>回复</span><span class="cm-chip">流式输出</span></div>
          </div>
        </div>

        <div class="cm-toolbar">
          <span class="cm-tool">⛶</span>
          <span class="cm-tool">−</span>
          <span class="cm-tool">+</span>
          <span class="cm-div"></span>
          <span class="cm-tool on">⊞</span>
          <span class="cm-tool run">▷</span>
        </div>
      </div>
    </div>
  </div>
</section>
<script>
(function(){
  function fit(){
    var W=1180,H=560;
    var stages=document.querySelectorAll('.cm-stage');
    for(var i=0;i<stages.length;i++){
      var st=stages[i], sc=st.querySelector('.cm-scaler');
      if(!sc) continue;
      var s=st.clientWidth/W; if(s>1)s=1; if(s<0.6)s=0.6;
      var tf='scale('+s+')';
      if(sc.style.transform!==tf) sc.style.transform=tf;
      var hpx=Math.round(H*s)+'px';
      if(st.style.height!==hpx) st.style.height=hpx;
      st.classList.toggle('scroll', W*s>st.clientWidth+1);
    }
  }
  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',fit); else fit();
  window.addEventListener('resize',fit);
  if(window.ResizeObserver){var ro=new ResizeObserver(fit);var ss=document.querySelectorAll('.cm-stage');for(var j=0;j<ss.length;j++)ro.observe(ss[j]);}
})();
</script>
'''.strip()
    body += block(        "核心能力",
        "一个企业级 Agent 开发平台，该有的都有",
        "句子秒懂是 AI 员工的「大脑」。可视化搭 Agent、接知识、调工具、选模型、发渠道——业务人员不写代码，就能把企业的流程和知识装进 Agent。",
        feat_grid([
            ("01", "可视化编排", "Canvas 拖拽节点连成 Agent——条件、循环、并行、转人工，每一步看得见、改得动，运营不写代码也能配。", "or"),
            ("02", "多 Agent 协作", "复杂业务拆成各管一段的 Agent，主管 Agent 统一调度，比单个几百节点的大流程更好维护、效果更好。", "bl"),
            ("03", "知识库", "产品文档、FAQ、网页、表格、API 一次导入，自动建索引，回答带出处、不跑偏。", "gr"),
            ("04", "插件与工具", "接 CRM、工单、订单、自定义 API，Agent 不止于回复，还能查库存、发券、改订单。", "pu"),
            ("05", "100+ 大模型", "DeepSeek、智谱、通义、文心、GPT 任选，按场景和成本随时切换，不绑死任何一家。", "te"),
            ("06", "一键发布多渠道", "配好的 Agent 直接发布到 11 个 IM 通道、网页和 API，复用到销售、客服、招聘等多个场景。", "or"),
        ], cols=3),
    )

    body += split_section(
        eyebrow="知识库",
        title="大模型不是在猜——它是真读过你的业务文档",
        paragraphs=[
            "通用大模型的回答来自公开语料。它不知道你的产品参数，不懂你的合规边界，不知道你的促销规则。",
            "句子秒懂的知识库让 AI 基于<strong>企业自己的文档</strong>回答客户：FAQ、产品手册、网页内容、内部规则、合规话术，一次导入，长期可检索。",
        ],
        bullets=[
            "支持文档、网页、表格、API 等多种格式导入",
            "AI 自动分块 + 向量化，毫秒级检索匹配",
            "知识覆盖度分析：哪些问题客户问了但 AI 没答好",
            "版本管理：文档更新后 AI 同步更新",
            "多知识库隔离：不同业务线、不同行业各管各的",
        ],
        visual_html="""
<div class="kb-anim" style="background:#fff;border-radius:12px;padding:18px;border:1px solid var(--gray-line);">
<div style="font-size:12px;font-weight:700;color:var(--gray-text);margin-bottom:14px;letter-spacing:.04em;">知识库 · 已导入 · 247 篇</div>
<div class="kb-rows" style="display:flex;flex-direction:column;gap:8px;font-size:13px;">
<div style="display:flex;align-items:center;gap:10px;padding:8px 10px;background:var(--blue-light);border-radius:8px;"><span style="font-size:16px;">📄</span><span style="flex:1;">产品规格手册 v3.2</span><span style="font-size:11px;color:var(--gray-text);">128 chunks</span></div>
<div style="display:flex;align-items:center;gap:10px;padding:8px 10px;background:var(--orange-lt);border-radius:8px;"><span style="font-size:16px;">❓</span><span style="flex:1;">FAQ · 售前售后</span><span style="font-size:11px;color:var(--gray-text);">312 chunks</span></div>
<div style="display:flex;align-items:center;gap:10px;padding:8px 10px;background:var(--green-lt);border-radius:8px;"><span style="font-size:16px;">🔒</span><span style="flex:1;">合规话术库</span><span style="font-size:11px;color:var(--gray-text);">86 chunks</span></div>
<div style="display:flex;align-items:center;gap:10px;padding:8px 10px;background:var(--purple-lt);border-radius:8px;"><span style="font-size:16px;">💰</span><span style="flex:1;">2026 Q1 促销规则</span><span style="font-size:11px;color:var(--gray-text);">42 chunks</span></div>
<div style="display:flex;align-items:center;gap:10px;padding:8px 10px;background:var(--gray-bg);border-radius:8px;color:var(--gray-text);"><span style="font-size:16px;">🌐</span><span style="flex:1;">官网内容（自动同步）</span><span class="kb-syncing" style="font-size:11px;">同步中</span></div>
</div>
</div>
""",
    )

    body += block(        "5 个高合规高垂直行业的策略库",
        "开通就带一套现成的行业打法",
        "每个行业的话术、SOP、合规边界，我们都内置好了——多年沉下来的行业经验，你不用从零调，开通就能用。",
        '<div style="display:grid;grid-template-columns:repeat(5,1fr);gap:14px;">'
        + ''.join(
            f'<div style="padding:24px 18px;background:#fff;border:1px solid var(--gray-line);border-radius:12px;text-align:center;"><div style="font-size:32px;margin-bottom:8px;">{ic}</div><div style="font-size:14px;font-weight:800;margin-bottom:6px;">{n}</div><div style="font-size:11.5px;color:var(--gray-text);line-height:1.55;">{d}</div></div>'
            for ic, n, d in [
                ("📚", "在线教育", "话术库 · 报名漏斗 · 续费策略"),
                ("🛍️", "消费品电商", "导购话术 · 售后处理 · 私域召回"),
                ("🏦", "金融", "合规话术 · 风控边界 · KYC 流程"),
                ("⚖️", "政务 · 司法", "调解话术 · 普法应答 · 公文规范"),
                ("🌐", "泛互联网", "客服 SOP · 用户分层 · 留存策略"),
            ]
        )
        + '</div>',
        alt=True,
    )

    body += split_section(
        eyebrow="智能体 + 工作流",
        title="可视化拼装 Agent，不用写代码",
        paragraphs=[
            "Canvas 可视化编辑器——拖拽节点连成 Agent 工作流。条件判断、知识库查询、模型调用、工具调用、转人工——每一步都看得见、改得动。",
            "运营人员即可配置 Agent 行为，无需等待开发排期。Agent 表现不符合预期时，运营在 Canvas 上即可调整。",
        ],
        bullets=[
            "三种智能体：对话型 / 任务型 / 多 Agent 协作",
            "100+ 种主流大模型可选：DeepSeek、智谱、文心、通义、GPT 等",
            "版本管理 + 灰度发布：新版本可控上线",
            "工作流模板库：每个行业都有起跑模板",
        ],
        visual_html="""
<div class="wf-anim" style="background:#fff;border-radius:12px;padding:18px;border:1px solid var(--gray-line);font-family:monospace;font-size:11.5px;">
<div style="font-weight:700;color:var(--orange);margin-bottom:14px;font-family:'PingFang SC';font-size:13px;">智能体 · 售前咨询 v2.1</div>
<div class="wf-steps" style="display:flex;flex-direction:column;gap:6px;color:var(--gray-text);">
<div style="background:var(--orange-lt);color:var(--orange);padding:8px 12px;border-radius:6px;font-weight:600;">▼ 用户提问</div>
<div style="padding-left:12px;color:var(--gray-text);">↓</div>
<div style="background:var(--blue-light);color:var(--blue);padding:8px 12px;border-radius:6px;font-weight:600;">→ 知识库检索</div>
<div style="padding-left:12px;color:var(--gray-text);">↓ 命中？</div>
<div style="display:grid;grid-template-columns:1fr 1fr;gap:6px;">
<div style="background:var(--green-lt);color:var(--green);padding:8px 12px;border-radius:6px;font-weight:600;font-size:11px;">命中 → 模型生成</div>
<div style="background:var(--purple-lt);color:var(--purple);padding:8px 12px;border-radius:6px;font-weight:600;font-size:11px;">未命中 → 转人工</div>
</div>
<div style="padding-left:12px;color:var(--gray-text);">↓</div>
<div style="background:var(--teal-lt);color:var(--teal);padding:8px 12px;border-radius:6px;font-weight:600;">✓ 输出回复 + 打标</div>
</div>
</div>
""",
        color="or",
        reverse=True,
    )

    # Preserved interactive Canvas demo (Req 7.8), now placed mid-body.
    body += mock_section

    body += block(        "结果",
        "AI 真懂业务的客户拿到的效果",
        "AI 不止于回复，还能承接后续业务。",
        kpi_row([
            ("100+", "支持的大模型种类"),
            ("89%", "对话自动完成率"),
            ("5 个", "高合规行业策略库"),
            ("多年", "行业数据沉淀"),
        ]),
    )

    body += f"""
<section class="section-block">
  <div class="container">
    {cta_band("用句子秒懂训练你的 AI 员工")}
  </div>
</section>
""".strip()

    return page_layout(
        title="句子秒懂 · AI 员工的「大脑」 | 句子互动",
        description="句子秒懂是企业级 Agent 开发平台——可视化搭 Agent、接知识库、调工具、选模型、一键发布多渠道。业务人员不写代码，就能把企业流程和知识装进 AI。100+ 大模型、Canvas 工作流、5 个行业策略库。",
        rel="../",
        breadcrumbs=[("首页", "../index.html"), ("产品", None), ("句子秒懂", None)],
        hero_kicker="产品 · 02",
        hero_h1='句子秒懂 · <span class="accent">让 AI 真的懂你的业务</span>',
        hero_lede="通用大模型不懂你的业务。把产品文档、SOP、合规规则装进 Agent，AI 才能用企业自己的知识回答客户、按企业的流程办事。",
        pills=["100+ 大模型支持", "Canvas 可视化工作流", "5 个高合规行业策略库", "多年行业数据沉淀"],
        body=body,
    )


def page_shouhu():
    body = ''

    # NEW module order (Req 4.1): pre-redesign ran 为什么 → 健康度看板 → 六道关口
    # → 测试报告. Here the six gates lead, the 上一代/守护 comparison follows
    # (now the shared comparison_table component, Req 5.1/5.4), then the report
    # split, and the health dashboard closes the body. Gate markers restored to
    # the preserved 01–06 (Req 5.2/8.4).

    # ── 六道关口 ──
    body += block(        "六道关口",
        "每个 Agent 上线，都要过六道关口",
        "把上线前、上线中、上线后该做的检查排成六道关，哪关没过就不让它上。",
        feat_grid([
            ("01", "AI 生成测试用例 · 上线前", "AI 读懂流程引擎配置和业务场景，几分钟生成上百条用例。结果不满意可对话调整、重新生成。还可输入 SOP 流程图、客户资料包、历史对话、新旧版本差异作为依据，覆盖提示词的改动。", "bl"),
            ("02", "批量验收 · 上线前", "单轮通过率 98% 看似达标，但大模型每次输出存在波动。设定轮数与并发跑多轮，逐条判断回复是否正确，筛出未通过的用例修正，合格用例纳入回归集。", "or"),
            ("03", "灰度测试 · 上线中", "需验证新版又要避免影响线上。开启灰度生成密钥，仅持有密钥的会话进入新版，其余会话维持原版。效果可对比，一键关闭即回退正式版。", "gr"),
            ("04", "回归测试 · 放行前强制", "新版一改，老功能可能悄悄坏。回归集跟版本绑定，上线前强制跑：不少于 50 条、通过率必须 100% 才放行。每次结果归档，质量怎么变的可追溯。", "pu"),
            ("05", "AI 工单 · 上线后", "AI 应答出错难以避免，问题在于客户缺少反馈渠道，也无从知晓是否有人跟进。客户在对话中点踩后，工单同步进入调优中心和客户侧看板，处理完成后回执状态。", "te"),
            ("06", "AI 质检 · 上线后", "人工质检成本高、覆盖有限。建立质检模板，对线上对话批量抽检，输出会话数与未通过比例，支持二次复检，人工客服与 AI 客服统一标准。", "bl"),
        ], cols=3),
    )

    # ── 为什么：上一代 vs 守护（comparison_table，Req 5.1/5.4）──
    body += block(
        "为什么要守护",
        "上线前测试不充分，问题会直接暴露给客户",
        "某家电客户上线前的一轮自动化测试中，28 条用例全部未通过，主要短板是故障咨询应答不达标，问题在上线前被拦下。Agent 上线不能止于流程搭建，上线前需充分测试，上线后需持续监控。",
        comparison_table(
            ["上一代 · 搭完流程就交付", "句子守护 · 守护你的 AI 员工"],
            [
                ("测试用例靠人手写，几十条到头，覆盖不全", ("AI 读懂业务流程，几分钟生成上百条用例", True)),
                ("上线就是终点，坏了没人知道、客户看不到", ("六道关口逐关把关，不达标不上线", True)),
                ("版本一改，老功能悄悄崩，上线才暴露", ("上线后 AI 工单、质检接着盯，问题主动冒出来", True)),
                ("做了多少质量活，客户完全无感", ("Agent 健康度看板，做了什么客户一眼看见", True)),
            ],
        ),
        alt=True,
    )

    # ── 一键测试报告 ──
    body += split_section(
        eyebrow="让客户看得见",
        title="一句话生成一份测试报告——把工程量摆到客户面前",
        paragraphs=[
            "六道关口背后是大量工程活，客户感受不到的话，跟没做也差不多。",
            "每次版本交付，一句话生成一份标准测试报告：用例通过情况、上线前拦截的问题、问题定位。即便通过率不高，也意味着问题已全部拦截，未流入线上。",
        ],
        bullets=[
            "一句话生成，样式可调、偏好可存",
            "PDF / PNG 导出，桌面和手机都自适应",
            "公开链接或密码访问，权限可控",
            "每次交付攒一份，客户那边的质量证据越来越厚",
        ],
        visual_html="""
<div style="background:#fff;border-radius:12px;padding:20px;border:1px solid var(--gray-line);">
<div style="font-size:12px;font-weight:700;color:var(--gray-text);margin-bottom:14px;">客户服务 Agent · 自动化测试报告</div>
<div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:10px;margin-bottom:14px;">
<div style="text-align:center;background:var(--gray-bg);padding:12px 8px;border-radius:8px;"><div style="font-size:22px;font-weight:800;color:var(--blue);">28</div><div style="font-size:11px;color:var(--gray-text);">测试用例</div></div>
<div style="text-align:center;background:var(--gray-bg);padding:12px 8px;border-radius:8px;"><div style="font-size:22px;font-weight:800;color:var(--orange);">5 类</div><div style="font-size:11px;color:var(--gray-text);">用例类型</div></div>
<div style="text-align:center;background:var(--gray-bg);padding:12px 8px;border-radius:8px;"><div style="font-size:22px;font-weight:800;color:var(--purple);">9 条</div><div style="font-size:11px;color:var(--gray-text);">故障咨询待修</div></div>
</div>
<div style="font-size:11.5px;color:var(--gray-text);line-height:1.6;background:var(--orange-lt);padding:10px 12px;border-radius:8px;">某家电服务客户上线前一轮：28 条用例全没过，最大短板是故障咨询（9 条）。问题都拦在了上线前，没放到客户面前。</div>
</div>
""",
        color="bl",
        reverse=True,
    )

    # ── 健康度仪表盘（示意数据）──
    body += block(        "客户看得见",
        "每天打开，就知道你的 AI 员工今天健不健康",
        "客户无需询问。一块看板呈现当天为该 Agent 执行的动作、五个维度的各项进展和健康度评分。",
        '''<div style="max-width:1000px;margin:0 auto;background:#fff;border:1px solid var(--gray-line);border-radius:18px;padding:32px;box-shadow:var(--shadow-md);">
<div style="display:flex;align-items:center;gap:24px;flex-wrap:wrap;border-bottom:1px solid var(--gray-line);padding-bottom:22px;margin-bottom:22px;">
  <div style="text-align:center;"><div style="font-size:52px;font-weight:900;color:var(--green);line-height:1;">87</div><div style="font-size:12px;color:var(--gray-text);margin-top:4px;">健康度（较上周 +6）</div></div>
  <div style="flex:1;min-width:240px;">
    <div style="font-size:12px;font-weight:700;color:var(--gray-text);margin-bottom:8px;">行动日历 · 每天为这个 Agent 做了什么</div>
    <div style="display:grid;grid-template-columns:repeat(20,1fr);gap:3px;">''' +
        ''.join(f'<div style="aspect-ratio:1;border-radius:2px;background:{c};"></div>' for c in (
            ['var(--gray-line)','#cde9d6','#9bd3ad','#6cc187','var(--green)']*8)[:40]) +
        '''</div>
  </div>
</div>
<div style="display:grid;grid-template-columns:repeat(5,1fr);gap:14px;">''' +
        ''.join(
            f'<div style="text-align:center;"><div style="font-size:22px;font-weight:800;color:var(--blue);">{v}</div><div style="font-size:12px;color:var(--gray-text);margin-top:4px;">{l}</div></div>'
            for v, l in [("126/98","用例生成 / 采纳"),("18 类","场景覆盖"),("94%","批量验收通过"),("3 版","灰度测试"),("100%","回归测试")]
        ) +
        '''</div>
<div style="font-size:11.5px;color:var(--gray-text);margin-top:18px;text-align:center;">示意数据；正式上线后由每个 Agent 的真实测试数据自动填充。</div>
</div>''',
        alt=True,
    )

    body += f"""
<section class="section-block">
  <div class="container">
    {cta_band("让句子守护把住你的 Agent 质量底线")}
  </div>
</section>
""".strip()

    return page_layout(
        title="句子守护 · 守护你的 AI 员工 | 句子互动",
        description="句子守护——守护你的 AI 员工，Agent 健康度看得见。Agent 上线前测过、上线后管着：AI 生成测试用例、批量验收、灰度测试、回归测试、AI 工单、AI 质检。没人点头就不上线，每一步都留痕、能查。",
        rel="../",
        breadcrumbs=[("首页", "../index.html"), ("产品", None), ("句子守护", None)],
        hero_kicker="产品 · 守护 · 主管",
        hero_h1='句子守护 · <span class="accent">守护你的 AI 员工</span>',
        hero_lede="我们为你的每一个 AI 员工做了什么、效果如何，一眼可见。<strong>Agent 上线前测过、上线后管着</strong>——AI 自动生成用例、批量验收、灰度测试、回归测试、AI 工单、AI 质检。没人拍板不上线，可追溯可审计。",
        pills=["六道关口上线把关", "AI 自动生成用例", "健康度持续监控", "金融政务必过的一关"],
        body=body,
    )


def page_workforce(*, slug, title, kicker, h1, lede, pills, color, industry, role_desc,
                   pain_paragraphs, pain_bullets, pain_visual,
                   capability_block, kpi_items, cta_text):
    """Generate a workforce role page."""
    body = ''
    body += split_section(
        eyebrow="角色画像",
        title=role_desc,
        paragraphs=pain_paragraphs,
        bullets=pain_bullets,
        visual_html=pain_visual,
        color=color,
    )
    body += block(        "能力清单",
        f"{title} 在岗后，做哪些事",
        "每一项都来自头部客户的真实部署。",
        capability_block,
        alt=True,
    )
    body += block(        "结果",
        f"{title} 上岗后客户拿到的实际效果",
        "数据来自真实客户案例。",
        kpi_row(kpi_items),
    )
    body += f"""
<section class="section-block">
  <div class="container">
    {cta_band(cta_text)}
  </div>
</section>
""".strip()

    return page_layout(
        title=f"{title} · {kicker} | 句子互动 AI 员工",
        description=f"{title}——{lede[:120]}",
        rel="../",
        breadcrumbs=[("首页", "../index.html"), ("AI 员工", None), (title, None)],
        hero_kicker=kicker,
        hero_h1=h1,
        hero_lede=lede,
        pills=pills,
        body=body,
    )


def workforce_pages():
    pages = {}

    # ────── AI 销售 ──────
    pages['sales'] = page_workforce(
        slug='sales',
        title='AI 销售',
        kicker='AI 员工 · 销售岗',
        h1='AI 销售 · <span class="accent">从建联到首单成交</span>',
        lede='直播搬家、私域承接、漏斗跟进、续费提醒——<strong>从客户建联到下第一单的全部环节，AI 销售都能接管</strong>。已覆盖直播带货行业头部公司，行业整体提效 80%+。',
        pills=['+80% 行业整体提效', '直播带货头部覆盖', '24×7 在岗', '按结果计价'],
        color='bl',
        industry='直播 · 教育 · 电商',
        role_desc='客户量激增时，传统销售难以承接，AI 销售能顶上',
        pain_paragraphs=[
            '单场直播涌入 5 万人，私域新增 2000 人建联，客户问题集中在开播后 1 小时内，人力难以及时承接。',
            '客户添加后，AI 销售随即接手对话：自我介绍、了解需求、讲解产品、预约课程；遇到复杂情况再转交真人。',
        ],
        pain_bullets=[
            '直播搬家：直播间客户建联后立即由 AI 跟进，避免冷场流失',
            '需求挖掘：3-5 轮对话摸清客户意向、收入水平、购买动机',
            '产品讲解：从知识库里找对应产品，按客户类型推荐',
            '促销执行：限时优惠、价格策略、组合方案，按公司规则执行',
            '续费提醒：到期前 N 天 AI 主动跟进，按客户 RFM 分层',
        ],
        pain_visual="""
<div style="background:#fff;border-radius:12px;padding:18px;border:1px solid var(--gray-line);">
<div style="font-size:12px;font-weight:700;color:var(--blue);margin-bottom:12px;">AI 销售 · 当日数据</div>
<div style="display:flex;flex-direction:column;gap:14px;">
<div><div style="font-size:11px;color:var(--gray-text);">新建联</div><div style="font-size:24px;font-weight:800;color:var(--blue);">2,800+</div></div>
<div><div style="font-size:11px;color:var(--gray-text);">主动触达</div><div style="font-size:24px;font-weight:800;color:var(--orange);">5,100+</div></div>
<div><div style="font-size:11px;color:var(--gray-text);">高意向客户</div><div style="font-size:24px;font-weight:800;color:var(--green);">380+</div></div>
<div><div style="font-size:11px;color:var(--gray-text);">今日成交</div><div style="font-size:24px;font-weight:800;color:var(--purple);">70+ 单 · ¥5.8 万</div></div>
</div>
</div>
""",
        capability_block=feat_grid([
            ('💬', '7×24 在岗', '凌晨时段同样在岗接待，客户不再因客服下班而流失。', 'bl'),
            ('📋', '业务流程标准化', '客户中途更换对接销售，话术口径保持一致，不会因人员流动导致服务质量下降。', 'or'),
            ('🎯', '客户分层', '按 RFM、来源、行为分层，不同客户给不同话术，转化更高。', 'gr'),
            ('🔁', '智能跟进', 'SOP 自动跟进 + AI 决策何时介入：未读消息提醒、流失前召回、续费前转化。', 'pu'),
            ('🤝', '人机协作', '对高意向客户，AI 先完成前期沟通铺垫，再转交真人促成成交。', 'te'),
            ('📊', '数据积累', '每段对话自动打标记录，识别成交率最高的话术并在后续对话中复用。', 'bl'),
        ], cols=3),
        kpi_items=[
            ('80%', '行业整体提效'),
            ('5×', '人均承接客户量'),
            ('24×7', '不下班的销售'),
            ('+38%', '转化率提升（中位数）'),
        ],
        cta_text='让 AI 销售在你的私域上岗',
    )

    # ────── AI 导购 ──────
    pages['marketing'] = page_workforce(
        slug='marketing',
        title='AI 导购',
        kicker='AI 员工 · 零售岗',
        h1='AI 导购 · <span class="accent">长尾客户也覆盖到</span>',
        lede='覆盖主流头部零售品牌的私域导购运营——<strong>人工招呼不过来的长尾客户，由 AI 接管</strong>。24×7 在线响应，转化不掉队。',
        pills=['几百家品牌已部署', '24×7 在线', '私域导购全自动', '到店导购 + 线上协同'],
        color='or',
        industry='消费品 · 零售品牌',
        role_desc='把人工导购的服务能力，复制到每一个长尾客户身上',
        pain_paragraphs=[
            '一家品牌私域有 50 万客户，活跃客户约 5%，其余 95% 长期沉默。人工导购一天至多服务 200 个客户，长尾客户无人覆盖。',
            'AI 导购把人工导购的服务扩展到每一个长尾客户：到货提醒、新品推荐、试穿建议、尺码推荐、活动通知，原本无人跟进的客户也能持续运营。',
        ],
        pain_bullets=[
            '到货提醒：缺码缺色商品到货时主动通知关注客户',
            '新品推荐：按客户偏好（风格、价位、品类）匹配推送',
            '试穿建议：根据客户身材数据推荐合身款式',
            '复购召回：长期未购客户分层唤起',
            '门店协同：线下导购把客户加进私域，AI 接管后续运营',
        ],
        pain_visual="""
<div style="background:#fff;border-radius:12px;padding:18px;border:1px solid var(--gray-line);">
<div style="font-size:13px;color:var(--orange);font-weight:700;margin-bottom:12px;">AI 导购 · 给客户王女士的推送</div>
<div style="display:flex;flex-direction:column;gap:8px;font-size:13px;">
<div style="background:var(--gray-bg);padding:9px 12px;border-radius:8px;">王姐好，您之前看的那款风衣到货了～</div>
<div style="background:var(--gray-bg);padding:9px 12px;border-radius:8px;">您 165cm/52kg 建议 M 码，肩线刚好</div>
<div style="background:var(--gray-bg);padding:9px 12px;border-radius:8px;">还有同色系的腰带搭配，配着穿超有型</div>
<div style="background:var(--orange);color:#fff;margin-left:auto;padding:9px 12px;border-radius:8px;max-width:80%;">嗯帮我拼下单</div>
</div>
<div style="margin-top:12px;display:flex;gap:8px;font-size:11px;">
<div style="flex:1;background:var(--blue-light);color:var(--blue);padding:6px;border-radius:6px;text-align:center;font-weight:700;">已下单</div>
<div style="flex:1;background:var(--green-lt);color:var(--green);padding:6px;border-radius:6px;text-align:center;font-weight:700;">客单 +¥420</div>
</div>
</div>
""",
        capability_block=feat_grid([
            ('🛍️', '商品智能推荐', '基于购买历史、浏览行为与标签体系，为客户匹配推荐。', 'or'),
            ('📅', '活动节奏管理', '双 11、618、品牌日等大促，按计划批量推送给对应客户。', 'bl'),
            ('🎁', '会员运营', '生日礼、积分到期、等级升降，按会员体系自动执行营销动作。', 'gr'),
            ('🛒', '购物车救援', '加购未付款客户分层召回，限时优惠自动触发。', 'pu'),
            ('💼', '门店协同', '线下导购添加客户微信后，AI 接管后续运营，门店人均服务客户量翻倍。', 'te'),
            ('📈', '复购挖掘', 'NPS 调研与老客户回访，唤起长期沉默客户。', 'or'),
        ], cols=3),
        kpi_items=[
            ('几百家', '头部零售品牌部署'),
            ('24×7', '私域全天在岗'),
            ('5×+', '导购人效提升'),
            ('95%+', '客户咨询响应率'),
        ],
        cta_text='让 AI 导购覆盖你的长尾客户',
    )

    # ────── AI 客服 ──────
    pages['service'] = page_workforce(
        slug='service',
        title='AI 客服',
        kicker='AI 员工 · 客服岗',
        h1='AI 客服 · <span class="accent">从售前咨询到售后投诉</span>',
        lede='结合 5 年积累的 BadCase 标注数据——<strong>疑难场景比通用客服处理得深</strong>。售前咨询、订单跟进、投诉处理、退换货全流程接管。',
        pills=['89% 自动完成率', '5 年 BadCase 积累', '全行业可用', '7×24 在岗'],
        color='gr',
        industry='电商 · 教育 · 全行业',
        role_desc='通用客服解决不了的疑难场景，AI 客服接管',
        pain_paragraphs=[
            '通用 AI 客服能应对常见问题（"怎么退款""快递到哪了"）。但客户的真实问题很多是边缘场景：商品破损但快递员说不接受退货、双 11 优惠和会员折扣冲突、跨境订单关税计算，通用客服无法处理。',
            'AI 客服基于 5 年 BadCase 标注数据训练，处理这些边缘场景优于通用方案：疑难问题先由 AI 尝试解决，超出能力再转人工。八成以上的工单在 AI 这一层完成。',
        ],
        pain_bullets=[
            '售前咨询：商品参数、库存、配送、活动一次回答清楚',
            '订单跟进：物流查询、配送时效、签收确认',
            '投诉处理：先共情再分类，按 SOP 给解决方案',
            '退换货：判定是否符合规则 + 流程自动化执行',
            '工单转接：超出 AI 能力的问题转给对应客服组',
        ],
        pain_visual="""
<div style="background:#fff;border-radius:12px;padding:18px;border:1px solid var(--gray-line);">
<div style="font-size:13px;color:var(--green);font-weight:700;margin-bottom:14px;">AI 客服 · 工单处理</div>
<div style="display:flex;flex-direction:column;gap:10px;">
<div style="display:flex;align-items:center;justify-content:space-between;font-size:13px;"><span>售前咨询</span><span style="color:var(--green);font-weight:700;">94% 自动</span></div>
<div style="height:8px;background:var(--gray-bg);border-radius:4px;overflow:hidden;"><div style="height:100%;width:94%;background:var(--green);"></div></div>
<div style="display:flex;align-items:center;justify-content:space-between;font-size:13px;"><span>订单查询</span><span style="color:var(--green);font-weight:700;">98% 自动</span></div>
<div style="height:8px;background:var(--gray-bg);border-radius:4px;overflow:hidden;"><div style="height:100%;width:98%;background:var(--green);"></div></div>
<div style="display:flex;align-items:center;justify-content:space-between;font-size:13px;"><span>退换货</span><span style="color:var(--orange);font-weight:700;">76% 自动</span></div>
<div style="height:8px;background:var(--gray-bg);border-radius:4px;overflow:hidden;"><div style="height:100%;width:76%;background:var(--orange);"></div></div>
<div style="display:flex;align-items:center;justify-content:space-between;font-size:13px;"><span>投诉处理</span><span style="color:var(--orange);font-weight:700;">68% 自动</span></div>
<div style="height:8px;background:var(--gray-bg);border-radius:4px;overflow:hidden;"><div style="height:100%;width:68%;background:var(--orange);"></div></div>
<div style="display:flex;align-items:center;justify-content:space-between;font-size:13px;border-top:1px solid var(--gray-line);padding-top:10px;margin-top:6px;"><span style="font-weight:700;">综合自动完成率</span><span style="color:var(--orange);font-weight:800;font-size:18px;">89%</span></div>
</div>
</div>
""",
        capability_block=feat_grid([
            ('💬', '多轮对话', '不止于一问一答，可与客户连续对话 5-10 轮，一次解决问题。', 'gr'),
            ('🔍', '工单分类', '客户问题自动打标分类，统计高频问题反向优化业务流程。', 'bl'),
            ('🎯', '情绪识别', '识别客户情绪（愤怒、焦虑、满意），决定是否提前转人工。', 'or'),
            ('📞', '人机协作', '转人工时，把对话上下文和 AI 试过的方案一起给客服，客户不用再说一遍。', 'pu'),
            ('🌍', '多语言', '中英双语，海外业务可扩展更多语种，全球客户共用一套客服。', 'te'),
            ('📚', 'BadCase 积累', '每次失败都会记录、标注并用于训练，再次遇到同类问题不会重复出错。', 'gr'),
        ], cols=3),
        kpi_items=[
            ('89%', '对话自动完成率'),
            ('5 年', 'BadCase 标注积累'),
            ('80%+', '工单 AI 接住'),
            ('15s', '平均响应时间'),
        ],
        cta_text='让 AI 客服接管 80% 的工单',
    )

    # ────── AI 社工 / 调解员 ──────
    pages['government'] = page_workforce(
        slug='government',
        title='AI 社工 / 调解员',
        kicker='AI 员工 · 政务岗',
        h1='AI 社工 / 调解员 · <span class="accent">高合规下也跑得稳</span>',
        lede='AI 普法调解员、AI 社工已在 <strong>城市基层试点</strong>率先落地——AI 社工 7×24 响应，累计服务居民约 50 万人次；AI 普法调解员参与调解近百起，成功率约 93%，获评地方法治实践优秀案例。每一句输出都有日志记录、可逐句倒查——这是政务和金融客户最看重的一点。',
        pills=['城市基层试点落地', '高合规 + 全程可审计', '居民服务约 50 万人次', '调解成功率约 93%'],
        color='pu',
        industry='政务 · 司法 · 公共服务',
        role_desc='政务场景对 AI 的要求最高：合规、可审计、说错一句都不行',
        pain_paragraphs=[
            '政务 AI 不能像电商客服那样先上线再迭代调优，一句话说错就可能引发舆情。而社区调解员人手有限，12345 热线持续高负荷，12348 普法咨询同样排队，供给始终不足。',
            'AI 社工 / 调解员先把人忙不过来的那部分接住——基础咨询能答，矛盾大致分得清类，碰到热点问题自动同步给真人。它说的每句话都有人审过，做的每个判断也都能倒查。',
        ],
        pain_bullets=[
            '普法咨询：依据官方法规库作答，不偏离、不杜撰',
            '矛盾调解：先共情再分类，按调解流程引导双方',
            '社区服务：办事指南、政策解读、邻里纠纷预处理',
            '民意收集：群众反馈结构化整理，热点问题及时同步',
            '全程可审计：每一句 AI 输出都有来源依据，可溯源',
        ],
        pain_visual="""
<div style="background:#fff;border-radius:12px;padding:18px;border:1px solid var(--gray-line);">
<div style="font-size:13px;color:var(--purple);font-weight:700;margin-bottom:12px;">AI 调解员 · 邻里噪音纠纷</div>
<div style="display:flex;flex-direction:column;gap:8px;font-size:12.5px;">
<div style="background:var(--gray-bg);padding:9px 12px;border-radius:8px;">您好张大爷，您说楼上夜里施工我了解了，深夜施工确实违反《环境噪声污染防治法》第 38 条。</div>
<div style="background:var(--gray-bg);padding:9px 12px;border-radius:8px;">建议先尝试沟通——可以请楼栋长上门协调。如果对方不配合，我可以帮您登记诉求，由社区调解员跟进。</div>
<div style="background:var(--purple);color:#fff;margin-left:auto;padding:9px 12px;border-radius:8px;max-width:80%;">那就帮我登记吧</div>
<div style="background:var(--gray-bg);padding:9px 12px;border-radius:8px;">好的张大爷，工单已登记（编号 #20264829），社区调解员 24 小时内联系您。</div>
</div>
<div style="margin-top:12px;font-size:11px;color:var(--gray-text);background:var(--purple-lt);padding:8px 10px;border-radius:6px;">✓ 引用法规来源：环境噪声污染防治法第 38 条 · 已自动归档可追溯</div>
</div>
""",
        capability_block=feat_grid([
            ('📜', '法规库引用', '法律咨询全部基于官方法规库，所引条款均可追溯，而非大模型自由生成。', 'pu'),
            ('🎯', '矛盾分类', '邻里纠纷、消费维权、劳动争议——按场景分类走对应调解流程。', 'bl'),
            ('🤝', '情绪安抚', '识别投诉者的情绪状态，先安抚再处理，避免一开口就激化矛盾。', 'gr'),
            ('📋', '工单流转', '超出 AI 能力的问题自动登记工单，转给真人调解员跟进。', 'or'),
            ('🔒', '全程可审计', '每一次决策、每一次引用都有日志记录，满足合规审查的取证要求。', 'te'),
            ('🌐', '多端接入', '12345 热线、政务 App、公众号、社区微信——一套 Agent 多端服务。', 'pu'),
        ], cols=3),
        kpi_items=[
            ('约 50 万', 'AI 社工累计服务居民（人次）'),
            ('↓ 约 45%', '居民投诉率'),
            ('↑ 约 85%', '居民满意度'),
            ('约 93%', 'AI 调解员调解成功率'),
        ],
        cta_text='把 AI 社工 / 调解员部署到你的政务系统',
    )

    # ────── AI 理财顾问 (金融) ──────
    pages['finance'] = page_workforce(
        slug='finance',
        title='AI 理财顾问',
        kicker='AI 员工 · 金融岗',
        h1='AI 理财顾问 · <span class="accent">合规边界内跑得稳</span>',
        lede='银行、证券、保险多个头部机构落地——<strong>可设的合规边界 + 多年风控话术库</strong>，金融客户敢用。',
        pills=['多家头部金融机构', '多年风控话术库', '可设的合规边界', 'KYC / 反洗钱集成'],
        color='te',
        industry='银行 · 证券 · 保险',
        role_desc='金融对 AI 的合规要求最严，一句话越界就可能触碰监管红线',
        pain_paragraphs=[
            '银行客户经理一人服务 500 个客户已经超负荷，可每个客户对理财、保险、信贷的咨询都不能怠慢。AI 理财顾问接住基础咨询和合规材料解读，人工只管高价值客户。',
            '难点全在合规这一关。不能给投资建议，不能保证收益，更不能误导客户去买。这些话术由风控团队预先划定边界，AI 输出前每句都经过审查。多年金融场景积累的话术库，通用 Agent 平台短期内难以补齐。',
        ],
        pain_bullets=[
            '产品咨询：理财、保险、信贷条款解读',
            '风险揭示：合规话术自动播报，不漏不偏',
            '材料指南：开户、贷款、理赔等流程引导',
            '交叉销售：基于客户画像推荐合规产品',
            'KYC 辅助：客户基础信息收集 + 反洗钱预筛',
        ],
        pain_visual="""
<div style="background:#fff;border-radius:12px;padding:18px;border:1px solid var(--gray-line);">
<div style="font-size:13px;color:var(--teal);font-weight:700;margin-bottom:12px;">AI 理财顾问 · 合规边界</div>
<div style="display:flex;flex-direction:column;gap:10px;font-size:12.5px;">
<div style="background:var(--green-lt);color:var(--green);padding:9px 12px;border-radius:8px;display:flex;align-items:center;gap:8px;"><span>✓</span><span>解读产品条款 / 介绍历史业绩</span></div>
<div style="background:var(--green-lt);color:var(--green);padding:9px 12px;border-radius:8px;display:flex;align-items:center;gap:8px;"><span>✓</span><span>风险等级匹配检查</span></div>
<div style="background:var(--green-lt);color:var(--green);padding:9px 12px;border-radius:8px;display:flex;align-items:center;gap:8px;"><span>✓</span><span>合规材料 + 风险揭示书自动播报</span></div>
<div style="background:var(--orange-lt);color:var(--orange);padding:9px 12px;border-radius:8px;display:flex;align-items:center;gap:8px;"><span>✗</span><span>给具体投资建议 → 拒答</span></div>
<div style="background:var(--orange-lt);color:var(--orange);padding:9px 12px;border-radius:8px;display:flex;align-items:center;gap:8px;"><span>✗</span><span>承诺保本保收益 → 拒答</span></div>
<div style="background:var(--orange-lt);color:var(--orange);padding:9px 12px;border-radius:8px;display:flex;align-items:center;gap:8px;"><span>✗</span><span>诱导销售 / 误导话术 → 拒答</span></div>
</div>
</div>
""",
        capability_block=feat_grid([
            ('🛡️', '可设的合规边界', '风控团队设定的边界 AI 无法越过，输出前先由规则校验。', 'te'),
            ('💼', '产品矩阵覆盖', '理财、保险、基金、信贷、信用卡——所有产品条款随时调取。', 'bl'),
            ('📊', '客户画像匹配', '按风险偏好、资产规模、年龄层级推荐合规产品。', 'or'),
            ('🔒', 'KYC 集成', '客户身份核实、风险等级评估、反洗钱筛查自动化。', 'gr'),
            ('🎯', '机会识别', '从对话中识别理财升级、保险增配等机会，转给真人顾问跟进。', 'pu'),
            ('📋', '全程可审计', '每次决策均留存记录，合规审查或监管核查时可直接调取。', 'te'),
        ], cols=3),
        kpi_items=[
            ('多家', '头部金融机构落地'),
            ('多年', '风控话术库积累'),
            ('100%', '合规可审计'),
            ('5×', '客户经理人均承接'),
        ],
        cta_text='让 AI 理财顾问在你的合规边界内上岗',
    )

    # ────── AI HR ──────
    pages['hr'] = page_workforce(
        slug='hr',
        title='AI HR',
        kicker='AI 员工 · 招聘岗',
        h1='AI HR · <span class="accent">初筛到一面，Agent 全包</span>',
        lede='简历获取、初筛与第一轮语音面试，<strong>全部由 Agent 自动完成</strong>。HR 只看 Top 20% 的候选人，把时间留给深度面试、团队沟通和人才策略。',
        pills=['HR 只看 Top 20%', '多渠道简历自动同步去重', 'AI 语音面试 7×24', '统一题库 + 评分卡'],
        color='bl',
        industry='招聘 · 全行业',
        role_desc='HR 一大半时间，耗在重复的简历筛选和初面上',
        pain_paragraphs=[
            '招聘的时间大量花在重复劳动上：每天在三五个平台下载、去重简历，逐份扫读 80% 会被淘汰的候选人，第一轮面试反复问同样几个标准化问题。响应一慢，候选人就流失了。',
            'AI HR 把这条流水线交给 Agent：简历自动同步去重、解析评分、按岗位匹配；AI 语音面试自动邀约、追问、评分；结果汇到一个控制台，HR 只做最后的录用决策。',
        ],
        pain_bullets=[
            '简历接入：对接主流招聘渠道，职位与简历自动同步、自动去重',
            '自动初筛：解析 30+ 字段，按 JD 算匹配度排序，硬性条件自动过滤',
            '多维评分：专业技能、项目经验、学习潜力多维度综合评分，权重可调',
            'AI 语音面试：自动邀约、动态追问、实时转写、自动评分，可 200+ 场并发',
            '录用决策：评估、报告、漏斗汇到一处，HR 一键定夺',
        ],
        pain_visual="""
<div style="background:#fff;border-radius:12px;padding:18px;border:1px solid var(--gray-line);">
<div style="font-size:13px;color:var(--blue);font-weight:700;margin-bottom:12px;">AI HR · 招聘控制台</div>
<div style="display:flex;flex-direction:column;gap:8px;">
<div style="display:flex;justify-content:space-between;font-size:13px;align-items:center;"><span>今日简历接入</span><span style="color:var(--blue);font-weight:800;font-size:18px;">612</span></div>
<div style="display:flex;justify-content:space-between;font-size:13px;align-items:center;"><span>AI 初筛通过</span><span style="color:var(--purple);font-weight:800;font-size:18px;">118</span></div>
<div style="display:flex;justify-content:space-between;font-size:13px;align-items:center;"><span>今日 AI 面试</span><span style="color:var(--orange);font-weight:800;font-size:18px;">56</span></div>
<div style="display:flex;justify-content:space-between;font-size:13px;align-items:center;"><span>待 HR 决策</span><span style="color:var(--green);font-weight:800;font-size:18px;">14</span></div>
<div style="border-top:1px solid var(--gray-line);padding-top:12px;margin-top:6px;display:flex;flex-direction:column;gap:4px;font-size:11.5px;">
<div style="color:var(--green);font-weight:600;">✓ 候选人 92 分，AI 一面已完成，待 HR 决策</div>
<div style="color:var(--green);font-weight:600;">✓ 已自动向 8 位候选人发出面试邀约</div>
<div style="color:var(--gray-text);">… AI HR 在岗中</div>
</div>
</div>
</div>
""",
        capability_block=feat_grid([
            ('📥', '简历自动接入', '对接 BOSS 直聘 / LinkedIn / Indeed，职位与简历自动同步，多渠道自动去重。', 'bl'),
            ('🔍', 'AI 初筛', '解析 30+ 字段，按 JD 算匹配度排序，不合格简历止步第一关。', 'or'),
            ('🎯', '多维评分', '专业技能、项目经验、学习潜力多维度综合评分，权重可自定义。', 'gr'),
            ('🎙️', 'AI 语音面试', '7×24 自动邀约、提问、追问、记录、评分，单场约 10 分钟。', 'pu'),
            ('📋', '统一题库', '八股题 + 场景题统一题库与评分卡，所有候选人同一把尺子。', 'te'),
            ('✅', '一键录用决策', '评估、报告、漏斗汇到一处，HR 勾选即进下一轮或发感谢信。', 'or'),
        ], cols=3),
        kpi_items=[
            ('5×', '简历处理效率'),
            ('200+', '面试并发场次'),
            ('38→19 天', '招聘周期'),
            ('Top 20%', 'HR 只看这部分'),
        ],
        cta_text='让 AI HR 接住你的招聘初筛与初面',
    )

    return pages


def page_enterprise():
    body = ''
    body += block(        "和 Anthropic 一个判断",
        "企业上线 AI，先问的往往不是它能多聪明，而是敢不敢把活真交给它",
        "TO B 要的是输出稳定、行为可审计、企业级可控。这也是 Anthropic 在 2026 年走的路，更是我们 多年的判断。",
        '<div style="background:var(--blue-light);border-left:4px solid var(--blue);border-radius:0 14px 14px 0;padding:24px 32px;max-width:920px;margin:0 auto;display:flex;gap:18px;align-items:center;"><div style="font-size:42px;font-weight:900;color:var(--blue);line-height:1;">&ldquo;</div><div style="font-size:17px;color:var(--black);font-weight:600;line-height:1.55;">客户问得最多的，不是「哪个模型最强」，而是「哪个能放心接入我的系统」。<small style="display:block;font-size:13.5px;color:var(--gray-text);font-weight:500;margin-top:6px;">—— 过去一年，几乎每位客户都会提出这个问题</small></div></div>',
    )

    deep_items = [
        # (color, num, en, zh, pain, ours, visual_html)
        ('bl', '01', '可预测', '输出可重复',
         '消费场景里偶尔答错影响有限，企业场景则不可接受。生成财务摘要、起草法律文书时，同一个问题三次给出三种答案，业务无法推进。',
         '多年带结果标注的部署数据让 Agent 行为可标定、可回归。<strong>同一个问题，每次给的回答是一致的，不是重新掷一次骰子</strong>。Anthropic 走的是模型对齐这条路，我们靠的是这些行业结果数据。',
         '<div style="font-size:11px;color:var(--gray-text);font-weight:700;letter-spacing:.04em;margin-bottom:8px;">同一个 query × 3</div>'
         '<div style="background:#fff;padding:9px 12px;border-radius:6px;border:1px solid var(--gray-line);font-size:12.5px;color:var(--blue);">→ 您的退款政策是 7 天无理由</div>'
         '<div style="background:#fff;padding:9px 12px;border-radius:6px;border:1px solid var(--gray-line);font-size:12.5px;color:var(--blue);">→ 您的退款政策是 7 天无理由</div>'
         '<div style="background:#fff;padding:9px 12px;border-radius:6px;border:1px solid var(--gray-line);font-size:12.5px;color:var(--blue);">→ 您的退款政策是 7 天无理由</div>'
         '<div style="font-size:11px;color:var(--green);font-weight:800;text-align:right;margin-top:4px;">✓ 一致</div>'),

        ('or', '02', '数据安全', '数据隔离',
         '内部文档、客户信息、专有数据，企业担心被模型留存并泄露给他人。企业 AI 落地，这往往是第一道门槛。',
         '<strong>支持私有化 / 一体机部署，客户数据不出域</strong>。多租户严格隔离 + TLS 1.3 传输 + AES-256 存储 + 数据脱敏。客户数据不用于模型训练（合同里写明）。',
         '<div style="font-size:11px;color:var(--gray-text);font-weight:700;letter-spacing:.04em;margin-bottom:8px;">数据流向</div>'
         '<div style="display:flex;align-items:center;gap:6px;font-size:12px;"><span style="background:#fff;padding:6px 10px;border-radius:6px;border:1px solid var(--gray-line);">企业内部</span><span>→</span><span style="background:var(--orange-lt);color:var(--orange);padding:6px 10px;border-radius:6px;font-weight:700;">私有化 Agent</span></div>'
         '<div style="display:flex;align-items:center;gap:6px;font-size:12px;margin-top:8px;"><span style="background:#fff;padding:6px 10px;border-radius:6px;border:1px solid var(--gray-line);">企业内部</span><span>↛</span><span style="background:#fee;color:#c00;padding:6px 10px;border-radius:6px;text-decoration:line-through;">公网模型</span></div>'
         '<div style="font-size:11px;color:var(--green);font-weight:800;margin-top:4px;">✓ 数据不出域</div>'),

        ('gr', '03', '行为管控', '行为可管控',
         '要 AI 按公司政策回答：能说什么、不能说什么、出了事谁负责，都得事先划好红线。仅在 prompt 里写「请不要 xxx」并不可靠。',
         'workflow 引擎里把<strong>能说什么、不能说什么</strong>提前写死，再配 5 个高合规行业策略库，不靠 prompt 软提示。金融的合规话术、政务的法规引用，AI 跨不出去。',
         '<div style="font-size:11px;color:var(--gray-text);font-weight:700;letter-spacing:.04em;margin-bottom:8px;">行为边界</div>'
         '<div style="background:#fff;padding:8px 11px;border-radius:6px;border:1px solid var(--gray-line);font-size:12px;display:flex;justify-content:space-between;"><span>解读产品条款</span><span style="color:var(--green);font-weight:800;">✓ 允许</span></div>'
         '<div style="background:#fff;padding:8px 11px;border-radius:6px;border:1px solid var(--gray-line);font-size:12px;display:flex;justify-content:space-between;"><span>引用合规话术库</span><span style="color:var(--green);font-weight:800;">✓ 允许</span></div>'
         '<div style="background:#fff;padding:8px 11px;border-radius:6px;border:1px solid var(--gray-line);font-size:12px;display:flex;justify-content:space-between;"><span>给具体投资建议</span><span style="color:#c00;font-weight:800;">✗ 拒答</span></div>'
         '<div style="background:#fff;padding:8px 11px;border-radius:6px;border:1px solid var(--gray-line);font-size:12px;display:flex;justify-content:space-between;"><span>承诺保本保收益</span><span style="color:#c00;font-weight:800;">✗ 拒答</span></div>'),

        ('pu', '04', '可审计', '全程可审计',
         '银保监来检查、政务来巡检、客户起诉，AI 的每一次回答都得能回溯：用了哪个知识库、参考了什么 context、谁批准的版本上线。',
         '<strong>每一次 Agent 决策可追溯</strong>：调用的知识库、用的模型、参考的上下文、决策路径、版本号，全量日志记录。金融、政务客户特别在意这一条，过得了等保三级。',
         '<div style="font-size:11px;color:var(--gray-text);font-weight:700;letter-spacing:.04em;margin-bottom:8px;">Agent 决策日志</div>'
         '<div style="background:#fff;padding:9px 11px;border-radius:6px;border:1px solid var(--gray-line);font-size:11.5px;line-height:1.6;font-family:monospace;">[09:23:04] query → "退款 7 天"<br/>[09:23:04] kb_search → K3#FAQ#142<br/>[09:23:05] model → claude-3.5 v2.1<br/>[09:23:05] reply → "您可享 7 天无理由..."<br/>[09:23:05] log_id → AGT-2026050609234</div>'
         '<div style="font-size:11px;color:var(--purple);font-weight:800;margin-top:4px;">✓ 全量日志归档 7 年</div>'),

        ('te', '05', '能对接', '对接现有系统',
         'AI 不能孤立运行，得接客户已有的 CRM、工单、知识库、订单系统。Agent 上岗第一天就要能查到客户的真实数据，不然就是摆设。',
         '<strong>多年 IM 通道适配 + 企业 CRM / 工单 / 知识库直连</strong>。11 个 IM 通道，加主流企业系统的对接经验。Agent 上岗即接管真实业务流，而非闲置空转。',
         '<div style="font-size:11px;color:var(--gray-text);font-weight:700;letter-spacing:.04em;margin-bottom:8px;">系统对接</div>'
         '<div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:6px;font-size:11px;font-weight:700;text-align:center;">'
         '<div style="background:#fff;padding:8px 4px;border-radius:6px;border:1px solid var(--gray-line);">CRM</div>'
         '<div style="background:#fff;padding:8px 4px;border-radius:6px;border:1px solid var(--gray-line);">工单</div>'
         '<div style="background:#fff;padding:8px 4px;border-radius:6px;border:1px solid var(--gray-line);">订单</div>'
         '</div>'
         '<div style="text-align:center;color:var(--teal);font-size:14px;margin:4px 0;">↕</div>'
         '<div style="background:var(--teal-lt);color:var(--teal);padding:9px 12px;border-radius:6px;text-align:center;font-weight:800;font-size:12.5px;">句子互动 Agent</div>'
         '<div style="text-align:center;color:var(--teal);font-size:14px;margin:4px 0;">↕</div>'
         '<div style="display:grid;grid-template-columns:repeat(5,1fr);gap:4px;font-size:10.5px;font-weight:700;text-align:center;">'
         '<div style="background:#fff;padding:6px 2px;border-radius:5px;border:1px solid var(--gray-line);">微</div>'
         '<div style="background:#fff;padding:6px 2px;border-radius:5px;border:1px solid var(--gray-line);">红</div>'
         '<div style="background:#fff;padding:6px 2px;border-radius:5px;border:1px solid var(--gray-line);">抖</div>'
         '<div style="background:#fff;padding:6px 2px;border-radius:5px;border:1px solid var(--gray-line);">飞</div>'
         '<div style="background:#fff;padding:6px 2px;border-radius:5px;border:1px solid var(--gray-line);">+</div>'
         '</div>'),

        ('bl', '06', '可规模化', '规模化',
         '许多公司的 AI 止步于试点：demo 能跑通，扩到几千客户、几十种业务场景就崩溃。企业 AI 必须从第一天就规划稳定运行。',
         '<strong>1000+ 大型企业客户验证过的部署能力</strong>，在生产环境深耕多年，不是 demo。从单一场景到多职能 Agent 矩阵，从一个客户的私域到集团央企的多租户隔离，都跑得通。',
         '<div style="font-size:11px;color:var(--gray-text);font-weight:700;letter-spacing:.04em;margin-bottom:8px;">部署规模</div>'
         '<div style="display:flex;justify-content:space-between;align-items:baseline;border-bottom:1px solid var(--gray-line);padding:6px 0;font-size:12.5px;"><span>大型企业客户</span><span style="color:var(--blue);font-weight:800;font-size:16px;">1000+</span></div>'
         '<div style="display:flex;justify-content:space-between;align-items:baseline;border-bottom:1px solid var(--gray-line);padding:6px 0;font-size:12.5px;"><span>覆盖高合规行业</span><span style="color:var(--blue);font-weight:800;font-size:16px;">5 大</span></div>'
         '<div style="display:flex;justify-content:space-between;align-items:baseline;border-bottom:1px solid var(--gray-line);padding:6px 0;font-size:12.5px;"><span>日均处理消息</span><span style="color:var(--blue);font-weight:800;font-size:16px;">200 万 +</span></div>'
         '<div style="display:flex;justify-content:space-between;align-items:baseline;padding:6px 0;font-size:12.5px;"><span>SaaS 服务可用性</span><span style="color:var(--green);font-weight:800;font-size:16px;">99.9%</span></div>'),

        ('or', '07', '不锁模型', '不绑死单一模型',
         '企业不愿绑定单一供应商。这个月用 GPT，下个月想切到智谱，年底可能改用 DeepSeek。模型涨价、出现故障、遭遇监管，任何一项都会让企业陷入被动。',
         '<strong>底层不绑死任何一家模型</strong>：DeepSeek、智谱、Qwen、文心一言、GPT 都能换。客户可按场景选择模型，依据价格与性能随时切换。',
         '<div style="font-size:11px;color:var(--gray-text);font-weight:700;letter-spacing:.04em;margin-bottom:8px;">模型矩阵</div>'
         '<div style="display:grid;grid-template-columns:1fr 1fr;gap:6px;font-size:12px;font-weight:700;">'
         '<div style="background:#fff;padding:8px 11px;border-radius:6px;border:1px solid var(--gray-line);display:flex;justify-content:space-between;align-items:center;"><span>DeepSeek-V3</span><span style="color:var(--green);">●</span></div>'
         '<div style="background:#fff;padding:8px 11px;border-radius:6px;border:1px solid var(--gray-line);display:flex;justify-content:space-between;align-items:center;"><span>智谱 GLM-4</span><span style="color:var(--green);">●</span></div>'
         '<div style="background:#fff;padding:8px 11px;border-radius:6px;border:1px solid var(--gray-line);display:flex;justify-content:space-between;align-items:center;"><span>Qwen 3</span><span style="color:var(--green);">●</span></div>'
         '<div style="background:#fff;padding:8px 11px;border-radius:6px;border:1px solid var(--gray-line);display:flex;justify-content:space-between;align-items:center;"><span>文心 5.0</span><span style="color:var(--green);">●</span></div>'
         '<div style="background:#fff;padding:8px 11px;border-radius:6px;border:1px solid var(--gray-line);display:flex;justify-content:space-between;align-items:center;"><span>GPT-5</span><span style="color:var(--green);">●</span></div>'
         '<div style="background:var(--orange-lt);color:var(--orange);padding:8px 11px;border-radius:6px;display:flex;justify-content:center;align-items:center;font-weight:800;">+ 100 种</div>'
         '</div>'),
    ]
    deep_html = '<div class="deep-list">'
    for color, num, en, zh, pain, ours, visual in deep_items:
        deep_html += f'''
<div class="deep-card {color}">
  <div class="dc-head">
    <div class="dc-num">{num}</div>
    <div class="dc-en">{en}</div>
    <h3>{zh}</h3>
  </div>
  <div class="dc-text">
    <div class="label">企业的真实痛点</div>
    <p class="pain">{pain}</p>
    <div class="label">句子互动怎么做</div>
    <p class="ours">{ours}</p>
  </div>
  <div class="dc-visual">{visual}</div>
</div>'''
    deep_html += '</div>'

    body += block(        "7 件事",
        "客户上线企业 AI 时，会问的 7 个问题——逐项有答案",
        "这些是客户在每个项目里真问过的问题，不是功能清单。每一项都讲清楚痛点，再讲我们怎么答。",
        deep_html,
        alt=True,
    )

    body += block(        "自研引擎",
        "成本和交付周期压下来，<span class=\"accent\">才扩得起来</span>",
        "AI 员工要能上岗、能复制、还得算得过账。自研 Token 成本控制引擎和 Agent 工厂 2.0，对的就是企业最担心的两件事：烧钱、上线慢。",
        '<div style="max-width:1000px;margin:0 auto;display:grid;grid-template-columns:repeat(3,1fr);gap:22px;">'
        '<div style="background:#fff;border:1px solid var(--gray-line);border-radius:16px;padding:30px 24px;text-align:center;"><div style="font-size:40px;font-weight:900;color:var(--blue);letter-spacing:-.02em;line-height:1;">↓ 87%</div><div style="font-size:14px;font-weight:800;margin:14px 0 8px;">大模型调用成本</div><div style="font-size:13px;color:var(--gray-text);line-height:1.6;">自研 Token 成本控制引擎 + 按任务分层做模型路由，把大模型调用成本降低约 87%。</div></div>'
        '<div style="background:#fff;border:1px solid var(--gray-line);border-radius:16px;padding:30px 24px;text-align:center;"><div style="font-size:40px;font-weight:900;color:var(--orange);letter-spacing:-.02em;line-height:1;">↓ 70%</div><div style="font-size:14px;font-weight:800;margin:14px 0 8px;">AI 员工定制交付周期</div><div style="font-size:13px;color:var(--gray-text);line-height:1.6;">Agent 工厂 2.0 的 SOP 模板化能力，让 AI 员工定制与交付周期缩短约 70%。</div></div>'
        '<div style="background:#fff;border:1px solid var(--gray-line);border-radius:16px;padding:30px 24px;text-align:center;"><div style="font-size:40px;font-weight:900;color:var(--green);letter-spacing:-.02em;line-height:1;">↑ 30–40%</div><div style="font-size:14px;font-weight:800;margin:14px 0 8px;">客户转化率</div><div style="font-size:13px;color:var(--gray-text);line-height:1.6;">在销售与服务场景，AI 员工帮客户把转化率提升约 30%—40%。</div></div>'
        '</div>',
    )

    body += split_section(
        eyebrow="部署模式",
        title="四种部署模式，按合规要求任选",
        paragraphs=[
            '不同行业对部署模式要求不同——电商客户用 SaaS 即可，金融政务客户要私有化或一体机交付。我们四种模式都跑得通，按客户合规要求选。',
        ],
        bullets=[
            '<strong>SaaS 公有云</strong>：开箱即用，按效果计价，适合电商 / 教育 / 互联网',
            '<strong>私有化部署</strong>：数据不出域，部署在客户自己的机房或专有云，适合金融 / 政务 / 大型央企',
            '<strong>混合部署</strong>：模型在客户私有云，控制台在 SaaS——兼顾合规和运维便利',
            '<strong>一体机交付</strong>：软硬件一体预装，离线即用——适合等保四级、央企总部、绝密场景',
            '<strong>多租户隔离</strong>：集团客户子公司之间数据严格隔离，权限按组织架构分发',
        ],
        visual_html='''
<div style="background:#fff;border-radius:12px;padding:18px;border:1px solid var(--gray-line);">
<div style="font-size:12px;font-weight:700;color:var(--gray-text);margin-bottom:14px;letter-spacing:.04em;">部署架构选项</div>
<div style="display:grid;grid-template-columns:1fr;gap:8px;font-size:12.5px;">
<div style="background:var(--blue-light);color:var(--blue);padding:12px 14px;border-radius:8px;"><div style="font-weight:700;margin-bottom:3px;">SaaS · 公有云</div><div style="font-size:11.5px;">5 分钟开通，按业务结果计价</div></div>
<div style="background:var(--orange-lt);color:var(--orange);padding:12px 14px;border-radius:8px;"><div style="font-weight:700;margin-bottom:3px;">私有化 · 客户机房</div><div style="font-size:11.5px;">数据不出域，金融政务级合规</div></div>
<div style="background:var(--green-lt);color:var(--green);padding:12px 14px;border-radius:8px;"><div style="font-weight:700;margin-bottom:3px;">混合 · 模型私有 + 平台 SaaS</div><div style="font-size:11.5px;">兼顾合规和运维便利</div></div>
<div style="background:var(--purple-lt);color:var(--purple);padding:12px 14px;border-radius:8px;"><div style="font-weight:700;margin-bottom:3px;">一体机 · 软硬件一体交付</div><div style="font-size:11.5px;">离线即用，等保四级 / 绝密场景</div></div>
</div>
</div>
''',
    )

    body += split_section(
        eyebrow="安全与合规",
        title="从底层就为企业级合规设计",
        paragraphs=[
            '合规不是上线之后再补，架构第一天就在做数据隔离、行为审计、权限分发。',
        ],
        bullets=[
            '数据加密：传输 TLS 1.3 + 存储 AES-256',
            '权限管理：RBAC + 细粒度数据权限',
            '审计日志：每一次 Agent 决策可溯源',
            '隐私保护：客户数据不用于模型训练（合同里写明）',
            '合规认证：等保三级（部分客户已通过）',
        ],
        visual_html='''
<div style="background:#fff;border-radius:12px;padding:18px;border:1px solid var(--gray-line);">
<div style="font-size:13px;color:var(--green);font-weight:700;margin-bottom:14px;">企业安全控制</div>
<div style="display:flex;flex-direction:column;gap:8px;font-size:13px;">
<div style="display:flex;align-items:center;gap:10px;padding:8px 12px;background:var(--gray-bg);border-radius:6px;"><span style="color:var(--green);">🔒</span><span>TLS 1.3 + AES-256 加密</span></div>
<div style="display:flex;align-items:center;gap:10px;padding:8px 12px;background:var(--gray-bg);border-radius:6px;"><span style="color:var(--green);">🔐</span><span>RBAC 权限管理</span></div>
<div style="display:flex;align-items:center;gap:10px;padding:8px 12px;background:var(--gray-bg);border-radius:6px;"><span style="color:var(--green);">📝</span><span>全量审计日志</span></div>
<div style="display:flex;align-items:center;gap:10px;padding:8px 12px;background:var(--gray-bg);border-radius:6px;"><span style="color:var(--green);">🛡️</span><span>等保三级（已认证）</span></div>
<div style="display:flex;align-items:center;gap:10px;padding:8px 12px;background:var(--gray-bg);border-radius:6px;"><span style="color:var(--green);">🚫</span><span>客户数据不用于模型训练</span></div>
<div style="display:flex;align-items:center;gap:10px;padding:8px 12px;background:var(--gray-bg);border-radius:6px;"><span style="color:var(--green);">🔄</span><span>异地容灾 + 5 分钟 RPO</span></div>
</div>
</div>
''',
        color='gr',
        reverse=True,
    )

    body += block(        "结果",
        "已经验证过的企业级部署能力",
        "1000+ 大型企业 多年的部署积累，不是 demo。",
        kpi_row([
            ('1000+', '大型企业客户'),
            ('5 个', '高合规高垂直行业'),
            ('100%', 'Agent 决策可追溯'),
            ('99.9%', 'SaaS 服务可用性'),
        ]),
        alt=True,
    )

    body += f"""
<section class="section-block">
  <div class="container">
    {cta_band("把 AI 员工装进你的合规边界内")}
  </div>
</section>
""".strip()

    return page_layout(
        title="企业级能力 · 和 Anthropic 同判断 | 句子互动",
        description="句子互动企业级 AI 能力：输出稳定、行为可审计、企业级可控。7 个 TO B 必过的门槛 + SaaS / 私有化 / 混合 / 一体机部署 + 等保三级合规。",
        rel="",
        breadcrumbs=[("首页", "index.html"), ("企业级能力", None)],
        hero_kicker="生来就是企业级",
        hero_h1='企业要的 AI，<span class="accent">不是更聪明，是更可控</span>',
        hero_lede="TO B 要的是<strong>输出稳定、行为可审计、企业级可控</strong>。这也是 Anthropic 在 2026 年走的路。我们服务企业客户多年，结论一致。",
        pills=["和 Anthropic 同判断", "1000+ 企业验证", "SaaS / 私有化 / 混合 / 一体机", "100% 决策可审计"],
        body=body,
    )


# ────────────────────────── industries page ──────────────────────────

def page_industries():
    body = ''
    body += block(        "5 个行业",
        "多年扎根这 5 个高合规高垂直行业",
        "我们没有做广覆盖的通用平台，而是在每个行业里积累了头部客户的做法和经验。",
        '',
    )

    industries_detail = [
        ('education', '在线教育', '📚', 'bl', '几百家头部公司已覆盖',
         '从大班课、小班课到 1 对 1，从招生、续费到 NPS，几乎所有头部在线教育公司都在用句子互动。AI 把「低转高」的招生与续费链路跑通——招生漏斗、续费提醒、督学服务、退课处理，每一环都有 AI 在岗。',
         [
             ('400+', '客户'),
             ('头部', '已覆盖'),
             ('多年', '行业积累'),
         ],
         '· 学员建联：自动欢迎语 + 体验课邀约',
         [
             '招生漏斗：直播搬家 → 私域承接 → 体验课 → 正价转化',
             '续费提醒：到期前 N 天分层 SOP，老客户深耕',
             '督学服务：作业提醒、出勤跟进、家长群运营',
             '退课/投诉处理：合规话术 + 真人介入节奏',
         ],
         ['头部大班课', '头部小班课', '头部 1 对 1', '兴趣技能头部', '财经职教头部', '众多头部']),

        ('ecommerce', '消费品电商', '🛍️', 'or', '几百家品牌已上线',
         '从美妆个护到母婴零食、从国货新锐到国际大牌——主流头部消费品牌的私域导购运营，AI 在背后接管长尾客户。',
         [
             ('几百家', '品牌'),
             ('24×7', '私域导购'),
             ('5×+', '导购人效'),
         ],
         '· 老客唤起：商品到货 + 新品种草按偏好推',
         [
             '私域导购：人工招呼不过来的长尾客户由 AI 接管',
             '会员运营：生日礼、积分到期、等级升降按规则执行',
             '购物车救援：加购未付款客户分层召回',
             '门店协同：线下导购把客户加私域，AI 接管后续运营',
         ],
         ['国际美妆头部', '国际护肤头部', '母婴头部', '功能食品头部', '日化头部', '家电头部', '众多品牌']),

        ('finance', '金融', '🏦', 'gr', '银证保多家头部机构',
         '银行、证券、保险。金融对 AI 的管控最严格。我们将合规边界提前固化，配合 多年积累的风控话术库，金融客户才愿意放手使用。',
         [
             ('多家', '头部机构'),
             ('多年', '风控话术库'),
             ('100%', '合规可审计'),
         ],
         '· 产品咨询：理财、保险、信贷条款解读',
         [
             '风险揭示：合规话术自动播报，不漏不偏',
             '材料指南：开户、贷款、理赔等流程引导',
             '交叉销售：基于客户画像推荐合规产品',
             'KYC 辅助：客户基础信息收集 + 反洗钱预筛',
         ],
         ['多家头部银行', '证券机构', '保险机构', '消费金融']),

        ('gov', '政务 · 司法', '⚖️', 'pu', 'AI 社工 / AI 调解员稳步落地',
         '政务对合规的要求最高，AI 一句话出错都可能引发舆情。我们的 AI 社工从海淀东升镇起步，已落地学院路、曙光、万寿路、清河、花园路等多个街道、几十个社区；AI 普法调解员在海淀区司法局上线。',
         [
             ('几十个', '社区落地'),
             ('60%+', '人工减负'),
             ('100%', '决策可审计'),
         ],
         '· 普法咨询：依据法规库答疑',
         [
             '矛盾调解：先共情再分类，按调解流程引导',
             '社区服务：办事指南、政策解读、邻里纠纷预处理',
             '民意收集：群众反馈结构化整理',
             '工单流转：超出 AI 能力自动登记给真人调解员',
         ],
         ['海淀·东升镇', '学院路街道', '曙光街道', '万寿路街道', '清河街道', '花园路街道', '海淀区司法局', '几十个社区']),

        ('internet', '泛互联网', '🌐', 'te', '多家平台型公司部署',
         '电商平台、内容平台、生活服务平台的客服、运营、销售已在使用 AI 员工，承接持续增长的客户量。',
         [
             ('多家', '平台型公司'),
             ('89%', '对话自动'),
             ('200 万+', '日均消息'),
         ],
         '· 客服：售前售后全流程接管',
         [
             '内容运营：批量化内容生产 + 多平台分发',
             '增长营销：用户分层 + 拉新留存策略执行',
             '订单跟进：物流查询、签收确认、售后处理',
             'BD 协同：商家入驻、培训、激励 SOP',
         ],
         ['头部搜索平台', '头部电商平台', '头部短视频平台', '头部分类信息', '头部资讯平台', '众多平台']),
    ]

    logo_cells = {
        'education': [('edu', ci, c) for ci in range(2) for c in range(8)][:15],
        'ecommerce': [('consumer', ci, c) for ci in range(2) for c in range(8)][:15],
        'finance':   [('govfin', 0, c) for c in range(6)],
        'gov':       [],
        'internet':  [('internet', 0, c) for c in range(8)],
    }
    for slug, name, icon, color, tagline, intro, kpis, scene, capabilities, customers in industries_detail:
        lg_cols = 3
        logo_grid_html = ''.join(
            f'<div style="border:1px solid var(--gray-line);border-radius:10px;background:#fff;display:flex;align-items:center;justify-content:center;padding:9px 14px;"><img src="assets/brand/logos/{p}-{ci}-{c}.png" alt="" style="width:100%;height:auto;display:block;" loading="lazy"></div>'
            for p, ci, c in logo_cells[slug]
        )
        kpi_html = ''.join(
            f'<div style="text-align:center;"><div style="font-size:24px;font-weight:800;color:var(--{color}-color, var(--blue));letter-spacing:-.01em;">{v}</div><div style="font-size:12px;color:var(--gray-text);margin-top:2px;">{l}</div></div>'
            for v, l in kpis
        )
        cap_html = ''.join(f'<li>{c}</li>' for c in capabilities)
        cust_html = ''.join(f'<span style="background:#fff;border:1px solid var(--gray-line);border-radius:6px;padding:5px 12px;font-size:12.5px;color:var(--gray-text);font-weight:600;">{c}</span>' for c in customers)
        # color tokens
        ccolor = {'bl': 'var(--blue)', 'or': 'var(--orange)', 'gr': 'var(--green)', 'pu': 'var(--purple)', 'te': 'var(--teal)'}[color]
        clt = {'bl': 'var(--blue-light)', 'or': 'var(--orange-lt)', 'gr': 'var(--green-lt)', 'pu': 'var(--purple-lt)', 'te': 'var(--teal-lt)'}[color]
        logo_card_html = (
            f'<div style="background:#fff;border:1px solid var(--gray-line);border-radius:18px;padding:22px 20px;">'
            f'<div style="font-size:13px;font-weight:800;letter-spacing:.06em;color:{ccolor};text-transform:uppercase;margin-bottom:16px;">部分客户</div>'
            f'<div style="display:grid;grid-template-columns:repeat({lg_cols},1fr);gap:10px;">{logo_grid_html}</div></div>'
        ) if logo_cells[slug] else ''
        # 政务：街道办没有可商用 logo（用政府徽标做商业背书有合规风险），右栏用真实落地街道名做客户墙
        if slug == 'gov':
            gov_sites = ['海淀·东升镇', '学院路街道', '曙光街道', '万寿路街道', '清河街道', '花园路街道', '海淀区司法局']
            gov_cells = ''.join(
                f'<div style="border:1px solid var(--gray-line);border-radius:10px;padding:13px 10px;text-align:center;font-size:13px;font-weight:700;color:var(--black);background:#fff;">{s}</div>'
                for s in gov_sites
            )
            logo_card_html = (
                '<div style="background:#fff;border:1px solid var(--gray-line);border-radius:18px;padding:22px 20px;">'
                '<div style="font-size:13px;font-weight:800;letter-spacing:.06em;color:var(--purple);text-transform:uppercase;margin-bottom:16px;">落地街道 · 北京海淀</div>'
                f'<div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;">{gov_cells}</div>'
                '<div style="margin-top:14px;font-size:12px;color:var(--gray-text);line-height:1.6;">从东升镇起步，已覆盖几十个社区、数百个居民群</div>'
                '</div>'
            )
        rw = 400 if slug == 'gov' else 480
        grid_cols = f'1fr {rw}px' if logo_card_html else '1fr'
        right_col = f'<div>{logo_card_html}</div>' if logo_card_html else ''
        body += f"""
<section class="section-block" id="{slug}">
  <div class="container">
    <div style="display:grid;grid-template-columns:{grid_cols};gap:48px;align-items:start;">
      <div>
        <div style="display:inline-flex;align-items:center;gap:10px;padding:6px 14px;background:{clt};color:{ccolor};border-radius:999px;font-size:13px;font-weight:700;margin-bottom:18px;">
          <span style="font-size:18px;">{icon}</span>{tagline}
        </div>
        <h2 style="font-size:34px;font-weight:800;letter-spacing:-.02em;margin:0 0 16px;">{name}</h2>
        <p style="font-size:16px;color:var(--gray-text);line-height:1.7;margin:0 0 24px;max-width:600px;">{intro}</p>
        <div style="font-size:13px;font-weight:800;letter-spacing:.06em;color:var(--gray-text);text-transform:uppercase;margin-bottom:14px;">典型场景</div>
        <p style="font-size:15px;font-weight:700;color:{ccolor};margin:0 0 12px;">{scene}</p>
        <ul style="margin:0;padding:0;list-style:none;">
          {''.join(f'<li style="padding:6px 0 6px 22px;position:relative;font-size:14.5px;color:var(--black);"><span style="position:absolute;left:0;top:14px;width:14px;height:2px;background:{ccolor};"></span>{c}</li>' for c in capabilities)}
        </ul>
      </div>
      {right_col}
    </div>
  </div>
</section>""".strip()

    body += block(        "为什么在这 5 个行业能直接用",
        "这 5 个行业的难点，我们已逐一沉淀出成熟做法",
        "通用平台能搭出大致框架，但要把行业里的具体场景真正跑通，靠的是对这个行业足够深的理解和积累。",
        '''<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:22px;max-width:1100px;margin:0 auto;">
<div style="padding:28px 24px;background:#fff;border:1px solid var(--gray-line);border-radius:18px;">
  <div style="font-size:13px;font-weight:800;color:var(--orange);letter-spacing:.1em;margin-bottom:12px;">客户拿到什么</div>
  <h4 style="font-size:18px;font-weight:800;margin:0 0 12px;">行业话术和 SOP 已内置</h4>
  <p style="font-size:14px;color:var(--gray-text);line-height:1.7;margin:0;">在线教育的报名漏斗、电商的私域召回、金融的合规话术、政务的调解流程，均已内置，无需从零训练 AI，开通即可使用。</p>
</div>
<div style="padding:28px 24px;background:#fff;border:1px solid var(--gray-line);border-radius:18px;">
  <div style="font-size:13px;font-weight:800;color:var(--blue);letter-spacing:.1em;margin-bottom:12px;">客户拿到什么</div>
  <h4 style="font-size:18px;font-weight:800;margin:0 0 12px;">行业经验已沉淀</h4>
  <p style="font-size:14px;color:var(--gray-text);line-height:1.7;margin:0;">你所在行业的头部公司已使用多年：哪些场景容易出错、合规边界如何把握、客户对哪些话术敏感，我们都清楚，帮你省下大量试错成本。</p>
</div>
<div style="padding:28px 24px;background:#fff;border:1px solid var(--gray-line);border-radius:18px;">
  <div style="font-size:13px;font-weight:800;color:var(--green);letter-spacing:.1em;margin-bottom:12px;">客户拿到什么</div>
  <h4 style="font-size:18px;font-weight:800;margin:0 0 12px;">你的反馈直接进入产品</h4>
  <p style="font-size:14px;color:var(--gray-text);line-height:1.7;margin:0;">每个客户的真实业务结果都会反馈回 Agent。你现场遇到的问题，会进入下一版产品修复。</p>
</div>
</div>''',
        alt=True,
    )

    body += f"""
<section class="section-block">
  <div class="container">
    {cta_band("把 AI 员工部署到你的行业")}
  </div>
</section>
""".strip()

    return page_layout(
        title="客户与行业 · 教育 / 电商 / 金融 / 政务 / 互联网 已部署 | 句子互动",
        description="句子互动 AI 员工已在在线教育、消费品电商、金融、政务·司法、泛互联网 5 个行业头部公司部署。如果你在这些行业，我们已经在这些行业跑了 多年。",
        rel="",
        breadcrumbs=[("首页", "index.html"), ("客户与行业", None)],
        hero_kicker="WHO USES JUZIBOT",
        hero_h1='你的行业里，<span class="accent">已经有人在用了</span>。',
        hero_lede="如果你在<strong>在线教育、消费品电商、金融、政务、互联网</strong>这 5 个行业里，你的同行已经在用句子互动的 AI 员工。这些行业的难点我们已经和他们一起趟过，你不必从零开始。",
        pills=["1000+ 大型企业客户", "5 个行业头部公司在用", "开通即可上岗", "同行已在用"],
        body=body,
    )


# ────────────────────────── about page ──────────────────────────

def page_about():
    # 6 department evidence cards — each rendered as the canonical feature card
    # (Design_System .card/.feature-card) so the category label, headline, and
    # description are all preserved verbatim (Req 5.2, 5.4).
    dept_cards = [
        ("战略", "一句话，75 分钟调研三家公司",
         "一句「判断这家是否为竞争对手」，AI 自动检索、撰写并发布到飞书群。出错后把教训写进 skill，下次自动规避。"),
        ("技术", "AI 自己测 AI、压测自己的系统",
         "测试 Agent、流量回放压测系统，都是团队用 AI 搭出来的，连提示词改动都能跑回归。"),
        ("销售", "跟单小二，每个销售都在用",
         "拜访录音自动转成纪要、回填 CRM、列出下一步该跟进的客户，销售不用再手动记单。"),
        ("法务", "全量合同走「秒审」",
         "销售发合同，AI 分钟级返回审核结果，过的自动走用章，异常的带修改建议推回来。"),
        ("HR · 运营", "一场全靠 AI 办起来的 Hackathon",
         "海报、议程、记分牌、开场视频全是 AI 做的；还把「AI 员工上岗机制」写成了制度。"),
        ("财务", "财务跑在 AI CRM 上",
         "客户、合同、回款、续约都在 AI CRM 里，到期自动提醒、对账异常主动推送，不用人去翻表对数。"),
    ]
    dept_grid = '<div class="feature-grid feature-grid--3">' + ''.join(
        f'<div class="card card--hover feature-card">'
        f'<div class="block-eyebrow">{cat}</div>'
        f'<h3 class="feature-title">{title}</h3>'
        f'<p class="feature-desc">{desc}</p>'
        f'</div>'
        for cat, title, desc in dept_cards
    ) + '</div>'

    # 3 perspective resource cards — canonical card surface as outbound links.
    perspectives = [
        ("https://rui.juzi.bot/slides/files/2026-05-24-dedao-reinvent-organization/index.html",
         "分享 · 得到", "重新发明组织：让小公司也用得起大公司的人",
         "AI 让一家小公司，也能用得起过去只有大公司才养得起的那种人。在得到的现场分享。", "查看分享 →"),
        ("https://rui.juzi.bot/slides/files/2026-04-25-ai-organization-pku/index.html",
         "分享", "AI 原生时代，我们正在交付的产品和还没解的题",
         "重新发明组织——AI 原生时代，一家公司每天怎么用 Agent 干活，哪些跑通了，哪些还在解。", "查看分享 →"),
        ("https://rui.juzi.bot/thought/2026-06-04-pe-to-fde.html",
         "思考", "硅谷今年最火的岗位 FDE，我们闷头干了三年",
         "被中国客户逼着，三年只做一件事：客户业务真的变好，才收钱。这是 AI 原生组织对外的样子。", "阅读全文 →"),
    ]
    persp_grid = '<div class="feature-grid feature-grid--3">' + ''.join(
        f'<a class="card card--hover feature-card" href="{href}" target="_blank" rel="noopener" style="text-decoration:none;color:inherit;">'
        f'<div class="block-eyebrow">{eyebrow}</div>'
        f'<h3 class="feature-title">{title}</h3>'
        f'<p class="feature-desc">{desc}</p>'
        f'<span class="feature-punch">{cta}</span>'
        f'</a>'
        for href, eyebrow, title, desc, cta in perspectives
    ) + '</div>'

    # Rebuilt module order (Req 4.1): department proof → outside perspectives →
    # company KPI strip → closing CTA (was KPI → department → perspectives).
    body = ''
    body += block(
        "AI 下沉到每个部门",
        "不是某个部门在试，是每个部门、每个人都在用",
        "一家公司是不是真正的 AI 原生，关键不在口号，而在 AI 是否落到了每个具体岗位。在句子互动，从管理层到一线，每个部门都有自己日常运行的 AI 工作流。",
        dept_grid,
        alt=True,
    )
    body += block(
        "我们怎么看",
        "AI 原生组织，<span class=\"accent\">长什么样</span>",
        "这些不是写在墙上的口号，是我们自己每天在跑的工作方式。",
        persp_grid,
    )
    body += block(
        "公司简介",
        "我们做的事，<span class=\"accent\">让 AI 在企业真实业务里跑起来</span>",
        "",
        kpi_row([
            ("1000+", "大型企业客户"),
            ("多年", "企业服务深耕"),
            ("4 个", "重点行业"),
            ("10+", "覆盖 IM 渠道"),
        ]),
    )
    body += cta_section(title="聊聊你想部署的 AI 员工")

    return page_layout(
        title="AI 原生组织 · 句子互动",
        description="句子互动是一家 AI 原生组织——不只把 AI 卖给客户，公司内部从管理层到一线，每个部门、每个人每天都在用 Agent 完成工作。已服务 1000+ 大型企业客户。国家高新技术企业、北京市专精特新「小巨人」、公安部等保三级。",
        rel="",
        breadcrumbs=[("首页", "index.html"), ("AI 原生组织", None)],
        hero_kicker="关于句子互动",
        hero_h1='我们自己，<span class="accent">就是一家 AI 原生组织</span>',
        hero_lede="我们不只把 AI 卖给客户——公司内部，从管理层到一线，每个部门、每个人每天都在用 Agent 完成工作。已服务 1000+ 大型企业客户。",
        pills=["1000+ 大型企业客户", "国家高新 · 专精特新", "每个部门都在用 AI"],
        body=body,
    )


# ────────────────────────── insights / AI 原生组织 ──────────────────────────

def page_insights():
    body = ''
    body += block(        "AI 下沉到每个部门",
        "不是某个部门在试，<span class=\"accent\">是每个部门、每个人都在用</span>",
        "判断一家公司是不是真的 AI 原生，不看它怎么说，看 AI 有没有落到每个具体岗位上。在句子互动，从 CEO 到财务，每个部门都有自己每天在跑的 AI 活。",
        '''<div style="max-width:1100px;margin:0 auto;display:grid;grid-template-columns:repeat(3,1fr);gap:16px;">
<div style="background:#fff;border:1px solid var(--gray-line);border-radius:14px;padding:22px;">
  <div style="font-size:12px;font-weight:800;color:var(--blue);letter-spacing:.06em;margin-bottom:8px;">CEO · 李佳芮</div>
  <div style="font-size:15px;font-weight:800;margin-bottom:8px;">一句话，75 分钟调研三家公司</div>
  <p style="font-size:13px;color:var(--gray-text);line-height:1.6;margin:0;">一句「判断这家是否为竞争对手」，Claude Code 自动检索、撰写并发布到飞书群。出错后将教训写入 skill，下次自动规避。</p>
</div>
<div style="background:#fff;border:1px solid var(--gray-line);border-radius:14px;padding:22px;">
  <div style="font-size:12px;font-weight:800;color:var(--green);letter-spacing:.06em;margin-bottom:8px;">技术</div>
  <div style="font-size:15px;font-weight:800;margin-bottom:8px;">AI 自己测 AI、压测自己的系统</div>
  <p style="font-size:13px;color:var(--gray-text);line-height:1.6;margin:0;">测试 Agent、流量回放压测系统，都是团队用 AI 搭出来的，连提示词改动都能跑回归。</p>
</div>
<div style="background:#fff;border:1px solid var(--gray-line);border-radius:14px;padding:22px;">
  <div style="font-size:12px;font-weight:800;color:var(--orange);letter-spacing:.06em;margin-bottom:8px;">销售</div>
  <div style="font-size:15px;font-weight:800;margin-bottom:8px;">一个销售，月接 200 → 913 人</div>
  <p style="font-size:13px;color:var(--gray-text);line-height:1.6;margin:0;">在线教育头部客户的先锋组，单个销售月接量从 200 增至 913 人，达整体均值数倍，由我们率先验证跑通。</p>
</div>
<div style="background:#fff;border:1px solid var(--gray-line);border-radius:14px;padding:22px;">
  <div style="font-size:12px;font-weight:800;color:var(--purple);letter-spacing:.06em;margin-bottom:8px;">法务</div>
  <div style="font-size:15px;font-weight:800;margin-bottom:8px;">全量合同走「秒审」</div>
  <p style="font-size:13px;color:var(--gray-text);line-height:1.6;margin:0;">销售发合同，AI 分钟级返回审核结果，过的自动走用章，异常的带修改建议推回来。</p>
</div>
<div style="background:#fff;border:1px solid var(--gray-line);border-radius:14px;padding:22px;">
  <div style="font-size:12px;font-weight:800;color:var(--teal);letter-spacing:.06em;margin-bottom:8px;">HR · 运营</div>
  <div style="font-size:15px;font-weight:800;margin-bottom:8px;">一场全靠 AI 办起来的 Hackathon</div>
  <p style="font-size:13px;color:var(--gray-text);line-height:1.6;margin:0;">海报、议程、记分牌、开场视频全是 AI 做的；还把「AI 员工上岗机制」写成了制度。</p>
</div>
<div style="background:#fff;border:1px solid var(--gray-line);border-radius:14px;padding:22px;">
  <div style="font-size:12px;font-weight:800;color:var(--blue);letter-spacing:.06em;margin-bottom:8px;">财务</div>
  <div style="font-size:15px;font-weight:800;margin-bottom:8px;">连财务也用上了 Claude Code</div>
  <p style="font-size:13px;color:var(--gray-text);line-height:1.6;margin:0;">从 2021 年就在公司的财务同事，现在也开始用 Claude Code 干活。</p>
</div>
</div>
<p style="text-align:center;font-size:14.5px;color:var(--gray-text);margin:32px auto 0;max-width:700px;line-height:1.7;">90 后 AI native 配 多年 toB 老兵，<strong style="color:var(--black);">这个组合全市场几乎没有</strong>。我们自己先活成 AI 原生组织，再带客户一起跑。</p>''',
    )

    body += block(        "我们自己先在跑",
        "用 AI，办了一场全程由 AI 共建的 Hackathon",
        "2026 年 4 月，句子互动办了首届 AI Hackathon。海报、议程、BGM、记分牌、开场视频、评分规则，连赛后那篇推文，也是 AI 做的。我们写在开场视频最后一帧：如果没有 AI，这场比赛办不起来。",
        '''<div style="max-width:1080px;margin:0 auto;">
<div style="display:grid;grid-template-columns:repeat(4,1fr);gap:16px;margin-bottom:24px;">
  <div style="text-align:center;background:#fff;border:1px solid var(--gray-line);border-radius:14px;padding:22px 14px;"><div style="font-size:30px;font-weight:900;color:var(--blue);">48 小时</div><div style="font-size:12.5px;color:var(--gray-text);margin-top:6px;">连续开干</div></div>
  <div style="text-align:center;background:#fff;border:1px solid var(--gray-line);border-radius:14px;padding:22px 14px;"><div style="font-size:30px;font-weight:900;color:var(--orange);">10 支</div><div style="font-size:12.5px;color:var(--gray-text);margin-top:6px;">队伍</div></div>
  <div style="text-align:center;background:#fff;border:1px solid var(--gray-line);border-radius:14px;padding:22px 14px;"><div style="font-size:30px;font-weight:900;color:var(--green);">50%</div><div style="font-size:12.5px;color:var(--gray-text);margin-top:6px;">全员参与率</div></div>
  <div style="text-align:center;background:#fff;border:1px solid var(--gray-line);border-radius:14px;padding:22px 14px;"><div style="font-size:30px;font-weight:900;color:var(--purple);">10 个</div><div style="font-size:12.5px;color:var(--gray-text);margin-top:6px;">能上岗的 AI 同事</div></div>
</div>
<div style="display:grid;grid-template-columns:1fr 1fr;gap:18px;">
  <div style="background:#fff;border:1px solid var(--gray-line);border-radius:16px;padding:26px;">
    <div style="font-size:13px;font-weight:800;color:var(--blue);margin-bottom:12px;">Demo Day 的规矩</div>
    <ul style="margin:0;padding-left:18px;font-size:13.5px;color:var(--gray-text);line-height:1.9;">
      <li>不准只讲 PPT，评委当场打开亲测，跑不起来分归零</li>
      <li>方案必须真接进句子秒回或句子秒懂，光有想法不算</li>
      <li>全员非技术的队伍，再加 25% 的分</li>
      <li>评委来自得到、奇绩创坛等机构</li>
    </ul>
  </div>
  <div style="background:#fff;border:1px solid var(--gray-line);border-radius:16px;padding:26px;">
    <div style="font-size:13px;font-weight:800;color:var(--orange);margin-bottom:12px;">冠军不是结束，是开始</div>
    <p style="margin:0 0 10px;font-size:13.5px;color:var(--gray-text);line-height:1.7;">CEO 李佳芮当场宣布：这十个 AI 员工，真在公司上岗了，团队再拿一次奖；上岗后迭代一大版，再拿一次；卖给客户收到钱，再拿一次；客户用起来又迭代，再拿一次。</p>
    <div style="font-size:14px;font-weight:800;color:var(--black);background:var(--orange-lt);padding:10px 14px;border-radius:8px;">上岗一次、迭代一次、卖出去一次、客户再迭代一次——同一个项目能拿到四回奖。</div>
  </div>
</div>
<div style="margin-top:20px;background:linear-gradient(135deg,var(--blue-light),#fff);border-radius:16px;padding:24px 28px;">
  <div style="font-size:13px;font-weight:800;color:var(--blue);margin-bottom:10px;">48 小时造出来的，比如——</div>
  <div style="font-size:13.5px;color:var(--gray-text);line-height:1.9;">发一张表 AI 自己理解字段写回飞书的「句子秒填」 · 把合同审核从逐份人工变成异常兜底的「秒审」 · 把 FAQ 机器人升级成完整售后智能体的「Careloop」 · 用一句大白话就能搭起一整条 workflow 的「句子老懂」 · 把客户群消息自动变工单的「秒通」 · 一行代码 5 分钟接入全渠道触达的「句子灵客」……</div>
  <div style="margin-top:14px;font-size:13px;color:var(--gray-text);">冠军团队三个人——产品、PE、销售，全非技术。这正是我们说的：每个人本身就该带一支 AI 队伍。</div>
</div>
</div>''',
        alt=True,
    )

    body += split_section(
        eyebrow="Claude 永动机",
        title='我在想，<span style="color:var(--blue);">它就在帮我把活干掉</span>',
        paragraphs=[
            '过去能写代码的人是 0.1%，Agent 把这个数字推到 1-3%，翻了几十倍。配环境、查命令、看报错——以前横在我和代码之间的种种琐事，Agent 全部接管了。',
            '我每天稳定的工作方式：构思、写出需求、交给 Claude 执行、我来 review。我的 review 速度跟不上它的产出速度，它几乎不停。<strong>瓶颈只剩"想清楚要什么"。</strong>',
        ],
        bullets=[
            '客户：拆问题 → 出方案 → 整理 PPT / Demo',
            '产品：设计下一代 Agent 工作台 → 跑原型 → 自己上手用',
            '团队：模糊战略 → 拆 OKR → 跟到落地',
            'AI 原生组织实验：人干的活拆成 SOP → Agent 化 → 我 review',
        ],
        visual_html='''
<div style="background:#fff;border-radius:14px;padding:24px;border:1px solid var(--gray-line);">
  <div style="font-size:12px;color:var(--gray-text);font-weight:800;letter-spacing:.06em;margin-bottom:18px;">永动机的循环</div>
  <div style="display:flex;flex-direction:column;gap:12px;font-size:13.5px;">
    <div style="display:flex;align-items:center;gap:12px;background:var(--blue-light);color:var(--blue);padding:12px 16px;border-radius:10px;font-weight:700;"><span style="font-size:18px;">🧠</span><span>人 · 想清楚要什么</span></div>
    <div style="text-align:center;color:var(--gray-text);font-size:14px;">↓</div>
    <div style="display:flex;align-items:center;gap:12px;background:var(--orange-lt);color:var(--orange);padding:12px 16px;border-radius:10px;font-weight:700;"><span style="font-size:18px;">⚡</span><span>Agent · 并行执行</span></div>
    <div style="text-align:center;color:var(--gray-text);font-size:14px;">↓</div>
    <div style="display:flex;align-items:center;gap:12px;background:var(--green-lt);color:var(--green);padding:12px 16px;border-radius:10px;font-weight:700;"><span style="font-size:18px;">✓</span><span>人 · review + 下一题</span></div>
    <div style="text-align:center;color:var(--gray-text);font-size:14px;">↻ 循环到「想完为止」</div>
  </div>
</div>
''',
    )

    body += split_section(
        eyebrow="Vibe X",
        title='从 Vibe Coding 到 <span style="color:var(--orange);">Vibe X</span>——任何用脑子干的活',
        paragraphs=[
            '开始写代码后我很快发现：同一套方法不只用在 coding 上。我每天用 Claude 干的事里，coding 反而是最小的一块。',
            '<strong>X 可以是任何脑力工作</strong>：分析客户数据、改 deck、拆 SOP、写文章、调流程。代码只是最早跑通的场景，它撬动的不止写代码，而是几乎所有脑力工作。',
        ],
        bullets=[
            'Vibe Coding：脑子里想 → AI 写出来',
            'Vibe Analysis：客户数据 → AI 拉透 → 给结论',
            'Vibe Deck：核心论点 → AI 起草 → 改成自己的',
            'Vibe SOP：业务流程 → AI 拆出 SOP → Agent 化',
        ],
        visual_html='''
<div style="background:#fff;border-radius:14px;padding:24px;border:1px solid var(--gray-line);">
  <div style="font-size:12px;color:var(--gray-text);font-weight:800;letter-spacing:.06em;margin-bottom:18px;">Skill 编排</div>
  <div style="font-size:13.5px;color:var(--gray-text);line-height:1.65;margin-bottom:14px;">一个 Agent = 一组编排好的 skill。组织设计可以从「画组织架构图」变成「编排 skill」。</div>
  <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;font-size:12px;font-weight:700;">
    <div style="background:var(--blue-light);color:var(--blue);padding:9px 12px;border-radius:8px;text-align:center;">查 CRM</div>
    <div style="background:var(--blue-light);color:var(--blue);padding:9px 12px;border-radius:8px;text-align:center;">调 API</div>
    <div style="background:var(--orange-lt);color:var(--orange);padding:9px 12px;border-radius:8px;text-align:center;">合规判断</div>
    <div style="background:var(--orange-lt);color:var(--orange);padding:9px 12px;border-radius:8px;text-align:center;">话术匹配</div>
    <div style="background:var(--green-lt);color:var(--green);padding:9px 12px;border-radius:8px;text-align:center;">发优惠券</div>
    <div style="background:var(--green-lt);color:var(--green);padding:9px 12px;border-radius:8px;text-align:center;">回话客户</div>
  </div>
  <div style="margin-top:14px;padding:10px 14px;background:var(--gray-bg);border-radius:8px;font-size:12px;color:var(--gray-text);text-align:center;">↓ 编排成 Agent</div>
  <div style="margin-top:6px;padding:12px 16px;background:linear-gradient(135deg,var(--blue),var(--blue-mid));color:#fff;border-radius:8px;font-size:13px;font-weight:700;text-align:center;">AI 销售  ·  在线</div>
</div>
''',
        color='or',
        reverse=True,
    )

    body += block(        "AI 不可替代的 20%",
        '把 80% 交给 AI，把这 <span class="accent">20%</span> 留给自己',
        '我们和客户聊下来，五件事 AI 替不了：判断、品味、在场、关系、手艺。这是「1 + N」里那个「1」要做的事。',
        '''<div style="display:grid;grid-template-columns:repeat(5,1fr);gap:14px;max-width:1100px;margin:0 auto;">
<div style="padding:24px 18px;background:#fff;border:1px solid var(--gray-line);border-radius:14px;">
  <div style="font-size:28px;margin-bottom:10px;">🎯</div>
  <h4 style="font-size:16px;font-weight:800;margin:0 0 8px;color:var(--blue);">判断</h4>
  <p style="font-size:13px;color:var(--gray-text);line-height:1.65;margin:0;">该不该做、做哪个、什么时候做——没人教过 AI 你公司的边界。</p>
</div>
<div style="padding:24px 18px;background:#fff;border:1px solid var(--gray-line);border-radius:14px;">
  <div style="font-size:28px;margin-bottom:10px;">🎨</div>
  <h4 style="font-size:16px;font-weight:800;margin:0 0 8px;color:var(--orange);">品味</h4>
  <p style="font-size:13px;color:var(--gray-text);line-height:1.65;margin:0;">同样的方案，100 个版本里选定一个——AI 给不了品味，这要靠你自己。</p>
</div>
<div style="padding:24px 18px;background:#fff;border:1px solid var(--gray-line);border-radius:14px;">
  <div style="font-size:28px;margin-bottom:10px;">👁️</div>
  <h4 style="font-size:16px;font-weight:800;margin:0 0 8px;color:var(--green);">在场</h4>
  <p style="font-size:13px;color:var(--gray-text);line-height:1.65;margin:0;">客户当面那一刻、团队遇到难关那一刻，AI 不在场。</p>
</div>
<div style="padding:24px 18px;background:#fff;border:1px solid var(--gray-line);border-radius:14px;">
  <div style="font-size:28px;margin-bottom:10px;">🤝</div>
  <h4 style="font-size:16px;font-weight:800;margin:0 0 8px;color:var(--purple);">关系</h4>
  <p style="font-size:13px;color:var(--gray-text);line-height:1.65;margin:0;">十年的合作伙伴、信任你的客户、敢一起冒险的团队——这是人之间的事。</p>
</div>
<div style="padding:24px 18px;background:#fff;border:1px solid var(--gray-line);border-radius:14px;">
  <div style="font-size:28px;margin-bottom:10px;">⚒️</div>
  <h4 style="font-size:16px;font-weight:800;margin:0 0 8px;color:var(--teal);">手艺</h4>
  <p style="font-size:13px;color:var(--gray-text);line-height:1.65;margin:0;">做完不够，要做到自己满意。一行代码、一段话术、一个细节，都是手艺所在。</p>
</div>
</div>
<p style="text-align:center;font-size:14.5px;color:var(--gray-text);margin:36px auto 0;max-width:680px;line-height:1.7;">另外 80% 交给 AI——<strong style="color:var(--black);">这 5 件事是你与 AI 的分界线</strong>。守住这条线，其余尽可交给它。</p>''',
        alt=True,
    )

    body += block(
        "文章",
        "李佳芮的洞察",
        "句子互动创始人 · 写在 rui.juzi.bot 上",
        '''<div style="display:grid;grid-template-columns:repeat(2,1fr);gap:22px;max-width:1100px;margin:0 auto;">
<a href="https://rui.juzi.bot/thought/2026-06-04-pe-to-fde.html" target="_blank" style="grid-column:1/-1;padding:34px 38px;background:linear-gradient(135deg,var(--blue-light),#fff);border:1px solid var(--gray-line);border-radius:18px;display:block;transition:all .2s ease;text-decoration:none;color:inherit;">
  <div style="font-size:11.5px;font-weight:800;color:var(--blue);letter-spacing:.1em;margin-bottom:12px;">2026-06-04 · FDE · 最新</div>
  <h4 style="font-size:25px;font-weight:800;margin:0 0 14px;letter-spacing:-.01em;line-height:1.3;">硅谷今年最火的岗位 FDE，我们三年前就在干了</h4>
  <p style="font-size:15px;color:var(--gray-text);line-height:1.75;margin:0 0 16px;max-width:760px;">2026 年硅谷集体抢 FDE，a16z 叫它「tech 最火的岗位」，招聘量一年涨 7 倍。这套打法我们 2023 年就在跑，比硅谷早三年：客户业务真做好了才收钱，交个 demo 不算。某在线教育客户的销售，单月承接量从一千增至三千。</p>
  <div style="font-size:14px;color:var(--blue);font-weight:700;">继续读 →</div>
</a>
<a href="https://rui.juzi.bot/thought/2026-04-28-return-to-code.html" target="_blank" style="padding:32px 28px;background:#fff;border:1px solid var(--gray-line);border-radius:18px;display:block;transition:all .2s ease;text-decoration:none;color:inherit;">
  <div style="font-size:11.5px;font-weight:800;color:var(--blue);letter-spacing:.1em;margin-bottom:12px;">2026-04-28 · CLAUDE 永动机</div>
  <h4 style="font-size:20px;font-weight:800;margin:0 0 12px;letter-spacing:-.01em;line-height:1.35;">接近 10 年没写代码了，被 Claude Opus 4.5 拉了回来</h4>
  <p style="font-size:14px;color:var(--gray-text);line-height:1.7;margin:0 0 14px;">十年没碰代码的人又开始写了，不是因为模型多聪明，是因为以前挡在我和代码之间的那堆破事全没了。这里将是我的下一代组织试验田。</p>
  <div style="font-size:13px;color:var(--blue);font-weight:700;">继续读 →</div>
</a>
<a href="https://rui.juzi.bot/thought/2026-05-04-ai-era-competitiveness.html" target="_blank" style="padding:32px 28px;background:#fff;border:1px solid var(--gray-line);border-radius:18px;display:block;transition:all .2s ease;text-decoration:none;color:inherit;">
  <div style="font-size:11.5px;font-weight:800;color:var(--orange);letter-spacing:.1em;margin-bottom:12px;">2026-05-04 · 思考</div>
  <h4 style="font-size:20px;font-weight:800;margin:0 0 12px;letter-spacing:-.01em;line-height:1.35;">AI 不可替代的那 20%：判断、品味、在场、关系、手艺</h4>
  <p style="font-size:14px;color:var(--gray-text);line-height:1.7;margin:0 0 14px;">你工作里那不可替代的 20% 是什么？另外 80% 怎么交给 AI？下一代组织的最小单元是 1 个人 + 一支 Agent 团队——那么"1"自己留下什么，"N"接走什么？</p>
  <div style="font-size:13px;color:var(--orange);font-weight:700;">继续读 →</div>
</a>
<a href="https://rui.juzi.bot/thought/2026-05-06-anthropic-won-enterprise.html" target="_blank" style="padding:32px 28px;background:#fff;border:1px solid var(--gray-line);border-radius:18px;display:block;transition:all .2s ease;text-decoration:none;color:inherit;">
  <div style="font-size:11.5px;font-weight:800;color:var(--green);letter-spacing:.1em;margin-bottom:12px;">2026-05-06 · 思考</div>
  <h4 style="font-size:20px;font-weight:800;margin:0 0 12px;letter-spacing:-.01em;line-height:1.35;">OpenAI 输给 Anthropic，不是输在产品，是输在组织</h4>
  <p style="font-size:14px;color:var(--gray-text);line-height:1.7;margin:0 0 14px;">2026 年企业 LLM API 市场份额，Anthropic 32%，OpenAI 25%。财富 10 强里 8 家在用 Claude。OpenAI 输的不是产品，是被 ChatGPT 训练出来的整套组织。五年前，Anthropic 选了反共识那条路。</p>
  <div style="font-size:13px;color:var(--green);font-weight:700;">继续读 →</div>
</a>
<a href="https://rui.juzi.bot/claude/" target="_blank" style="padding:32px 28px;background:linear-gradient(135deg,var(--blue),var(--blue-mid));color:#fff;border:0;border-radius:18px;display:flex;flex-direction:column;justify-content:center;text-decoration:none;">
  <div style="font-size:11.5px;font-weight:800;color:#FFC78A;letter-spacing:.1em;margin-bottom:12px;">CLAUDE 永动机 · 持续更新</div>
  <h4 style="font-size:22px;font-weight:800;margin:0 0 14px;letter-spacing:-.01em;line-height:1.3;">下一代组织的试验田</h4>
  <p style="font-size:14.5px;line-height:1.7;margin:0 0 16px;opacity:.9;">怎么把"我"变成 1+N 的组织、跑过的长任务、hack Claude 的小实验、失败的实验和原因——所有内容在 rui.juzi.bot/claude/ 持续更新。</p>
  <div style="font-size:14px;font-weight:700;">访问博客 →</div>
</a>
</div>''',
    )

    body += f"""
<section class="section-block">
  <div class="container">
    {cta_band("和我们一起跑 AI 原生组织")}
  </div>
</section>
""".strip()

    return page_layout(
        title="AI 原生组织 · 我们自己怎么活 | 句子互动",
        description="句子互动是一家 AI 原生组织——不是'在用 AI 的公司'，是 AI 已经下沉到每个部门、每个人手上。从 CEO 到财务每天真用 Agent 干活。90 后 AI native × 多年 toB 老兵的组合，全市场几乎没有。这条路我们自己先活成，再带客户一起跑。",
        rel="",
        breadcrumbs=[("首页", "index.html"), ("AI 原生组织", None)],
        hero_kicker="AI 原生组织 · 我们自己怎么活",
        hero_h1='不是「在用 AI 的公司」，<span class="accent">是 AI 下沉到每个人的组织</span>',
        hero_lede="很多公司都说自己在用 AI，但真正让每个人日常都离不开 Agent 的，并不多。在句子互动，<strong>从管理层到一线，每个部门、每个人每天都在用 Agent 干活</strong>——不是多配了个工具，是工作方式本身变了。我们先把自己做成 AI 原生组织，再把这套方法带给客户。",
        pills=["AI 下沉到每个人", "90 后 × 多年 toB", "自己先活成再带客户", "1 + N 组织"],
        body=body,
    )


# ────────────────────────── case · 该客户 ──────────────────────────

# ────────────────────────── build all ──────────────────────────

def page_fde():
    body = ''
    # Rebuilt module order (Req 4.1): the pre-redesign page led with the FDE
    # definition contrast then the method grid. Here the four-step method grid
    # leads, the definition contrast follows (now a semantic comparison table),
    # then the high-value-scenario split, the Echo/Delta pairing, and the global
    # context. Step markers preserved as 01–04 (Req 5.2).
    body += block(
        "FDE 怎么干",
        "贴着客户的业务跑，把脏活在现场解决",
        "AI 落地的难点从来不是模型，而是客户各不相同的真实业务。FDE 正是去解决这一部分。",
        feat_grid([
            ("01", "先搞懂这门生意", "不是先装软件，而是先与客户梳理清楚业务、流程与症结。AI 要承接的工作，必须先有人真正理解。", "bl"),
            ("02", "对结果负责", "与客户签订对赌协议，按结果收费。客户的转化和人效确实改善，我们才收费。", "or"),
            ("03", "能力回流产品", "在一个客户现场踩出来的能力，抽象成产品里的标准能力，下一个客户起步就用得上。做一次，卖多次。", "gr"),
            ("04", "不一定是工程师", "FDE 不限于会写代码的人——很多最好的 FDE 不写代码。真正重要的是理解业务、肯往一线钻，技术背景只是其次。", "pu"),
        ], cols=2),
    )

    body += block(
        "FDE 是什么",
        "把工程师派到客户现场，对结果负责",
        "FDE，Forward Deployed Engineer（前端部署工程师）——前移到客户业务现场的工程师。不止于交付软件，而是与客户一起理解业务，让 AI 真正在其中产出结果。",
        comparison_table(
            ["普通产品工程师", "FDE"],
            [
                ("关心「一个能力，给很多客户」", ("关心「一个客户，很多能力」", True)),
                ("交一套搭好的流程，就算完", ("对客户的业务结果负责，结果没出来不算完", True)),
                ("在公司里写通用功能", ("写两头的代码：现场的定制，抽回产品的标准能力", True)),
            ],
        ),
    )

    body += split_section(
        eyebrow="从高价值场景切入",
        title="先从最影响业绩的场景做起",
        paragraphs=[
            "AI 客服降本，AI 销售增收。FDE 进场的第一步，是帮客户找到对收入影响最大的场景——同一套底层能力，用在销售环节的价值，往往高于客服。",
            "这也是 FDE 与单纯卖软件的根本区别：软件交付即结束，而 FDE 在客户业绩增长之后才获得收入。利益一致，才会有人把繁重的落地工作做到底。",
        ],
        bullets=[
            "AI 客服：接住所有进线，把服务成本降下来",
            "AI 销售：从建联到成交全程接管，直接带来增长",
            "优先从高价值场景切入，再逐步向外扩展",
            "按结果收费：业务结果产出后才收费",
        ],
        visual_html="""
<div style="background:#fff;border-radius:12px;padding:22px;border:1px solid var(--gray-line);">
<div style="font-size:12px;font-weight:700;color:var(--gray-text);margin-bottom:16px;letter-spacing:.04em;">FDE 进场 · 如何选择场景</div>
<div style="display:flex;flex-direction:column;gap:10px;font-size:13px;">
<div style="display:flex;align-items:center;gap:10px;padding:11px 14px;background:var(--gray-bg);border-radius:8px;"><span style="color:var(--blue);font-weight:800;">1</span><span>先理清业务，找到最影响收入的环节</span></div>
<div style="display:flex;align-items:center;gap:10px;padding:11px 14px;background:var(--gray-bg);border-radius:8px;"><span style="color:var(--blue);font-weight:800;">2</span><span>从高价值场景切入，跑出可量化的结果</span></div>
<div style="display:flex;align-items:center;gap:10px;padding:11px 14px;background:var(--blue-light);border-radius:8px;"><span style="color:var(--blue);font-weight:800;">3</span><span style="color:var(--blue);font-weight:600;">按结果收费，客户业绩增长我们才增长</span></div>
</div>
</div>
""",
        color="bl",
        reverse=True,
    )

    # ── Echo + Delta — canonical 2-up feature cards (Req 5.4), no per-card override ──
    echo_delta = (
        '<div class="feature-grid feature-grid--2">'
        '<div class="card feature-card">'
        '<div class="block-eyebrow">ECHO · 懂行业</div>'
        '<p class="feature-desc">钻进客户的生意里，找出真正该解决的问题。FDE 进场的第一件事不是写代码，是把这门生意先搞清楚。</p>'
        '</div>'
        '<div class="card feature-card">'
        '<div class="block-eyebrow">DELTA · 写代码</div>'
        '<p class="feature-desc">快速把现场需要的东西搭出来。Echo 定义问题，Delta 当场实现，两人扎进同一个客户。</p>'
        '</div>'
        '</div>'
        '<p style="text-align:center;font-size:14px;color:var(--gray-text);margin:24px auto 0;max-width:720px;line-height:1.7;">现场踩出来的粗糙定制，后方产品团队再抽象成能跑 5–10 个客户的标准能力——上一个客户踩的坑，成了下一个 FDE 进场的杠杆。</p>'
    )
    body += block(
        "FDE 由两种人搭班子",
        "Echo 懂行业，Delta 写代码",
        "FDE 不是一个全才，而是两种能力的组合。后方还有产品团队，把现场的粗糙定制抽象成可复用的标准产品。",
        echo_delta,
        alt=True,
    )

    # ── 全球 FDE 格局 ──
    body += block(
        "全球验证过的模式",
        "FDE，我们 2023 年就在做",
        "FDE 由 Palantir 首创，如今 OpenAI、Anthropic、谷歌云等都在组建 FDE 团队，把 AI 真正落进企业。句子互动被中国客户逼着，从 2023 年起就按结果交付——比硅谷早了三年。",
        '''<p style="text-align:center;font-size:14.5px;color:var(--black);font-weight:600;margin:0 auto;max-width:720px;line-height:1.7;">想了解我们这三年怎么走过来的？<a href="https://rui.juzi.bot/thought/2026-06-04-pe-to-fde.html" target="_blank" style="color:var(--blue);font-weight:700;">读创始人的完整复盘 →</a></p>''',
    )

    body += cta_section(title="让 FDE 团队进场，把 AI 跑进你的业务")
    return page_layout(
        title="FDE 交付结果 · 对结果负责的工程师 | 句子互动",
        description="FDE（Forward Deployed Engineer，前端部署工程师）——前移到客户业务现场的工程师团队。不只装软件，对客户的业务结果负责：先搞懂这门生意，按结果收费，把现场踩出来的能力回流成产品。",
        rel="",
        breadcrumbs=[("首页", "index.html"), ("FDE 交付结果", None)],
        hero_kicker="FDE · 我们怎么交付",
        hero_h1='一支<span class="accent">对结果负责</span>的 FDE 团队',
        hero_lede="传统软件交付完就结束，用得好不好是客户自己的事。句子互动派出的是 FDE——<strong>Forward Deployed Engineer，前端部署工程师</strong>，前移到客户业务现场：先理解客户的业务，再按结果收费。客户业绩增长，我们才有收入，因此现场积累的能力会回流到产品中。",
        pills=["前移到客户现场", "对业务结果负责", "按结果收费", "能力回流产品"],
        body=body,
    )


def page_dongxing():
    body = ''
    # NEW module order (Req 4.1): pre-redesign led with the four-step grid then
    # the split. Here the "what knowledge engineering is" split leads, and the
    # four-step method follows. Step markers restored to preserved 01–04.
    body += split_section(
        eyebrow="知识工程",
        title="把散落的知识，炼成能查的资产",
        paragraphs=[
            "知识工程不止于把文档存进数据库。客户的经验、文档、历史对话中散落的知识，需整理成 AI 可查准、可调用的资产。",
            "通常先用句子智库把散乱的知识炼成可检索的资产，再引入其余产品与 FDE 团队。顺序颠倒，则无法跑通。",
        ],
        bullets=[
            "文档、表格、历史对话、SOP——多来源一起进",
            "炼成带标签、可检索、可追溯来源的知识块",
            "每条回答可追溯出处，而非模型生成",
            "上线后持续回流，知识越用越准",
        ],
        visual_html="""
<div style="background:#fff;border-radius:12px;padding:20px;border:1px solid var(--gray-line);">
<div style="display:flex;align-items:center;justify-content:space-between;gap:12px;">
<div style="text-align:center;flex:1;"><div style="font-size:26px;font-weight:900;color:var(--gray-text);">原始资料</div><div style="font-size:12px;color:var(--gray-text);margin-top:4px;">散、乱、重复、过期</div></div>
<div style="font-size:22px;color:var(--purple);">→</div>
<div style="text-align:center;flex:1;"><div style="font-size:26px;font-weight:900;color:var(--purple);">知识资产</div><div style="font-size:12px;color:var(--gray-text);margin-top:4px;">干净、可检索、带出处</div></div>
</div>
<div style="margin-top:16px;font-size:11.5px;color:var(--gray-text);background:var(--purple-lt);padding:10px 12px;border-radius:8px;">先把这层做对，AI 才查得准。知识工程是 Agent 上岗的前提，不是上线后再补的活。</div>
</div>
""",
        color="pu",
        reverse=True,
    )
    body += block(
        "知识工程",
        "知识工程：把散落的知识，炼成 AI 答得准的资产",
        "很多客户以为把知识库直接接进 AI 就行，结果命中率反而更低、答得更乱。问题不在 AI，在知识没被整理过。这件事叫知识工程——句子智库用下面四步，把散乱的知识炼成 AI 真正用得上的资产。",
        feat_grid([
            ("01", "清洗去重", "原始资料里，重复的、过期的、互相打架的内容很多。先清一遍，去掉冗余和矛盾，只留下可用的知识。", "bl"),
            ("02", "结构化切分", "整篇长文档直接拿去检索，AI 查不准。按语义切成一块块，每块带好上下文和标签，检索才命中得准。", "or"),
            ("03", "问法对齐", "同一个问题，客户有十种问法。把同义、近义、口语化的说法对齐到一起，命中率才稳定。", "gr"),
            ("04", "持续回流", "上线后没答好的问题，回流进知识库再修正。用得越多、知识越准，不是整理一次就不管了。", "pu"),
        ], cols=2),
        alt=True,
    )
    body += f"""
<section class="section-block">
  <div class="container">
    {cta_band("先把你的知识工程做对，再上 AI 员工")}
  </div>
</section>
""".strip()
    return page_layout(
        title="句子智库 · AI 员工的记忆 | 句子互动",
        description="句子智库——AI 员工的记忆。把客户散乱的知识炼成 AI 能查、能用、越用越准的可检索资产。知识工程是 Agent 上岗的前提：先把知识做对，再上产品。",
        rel="../",
        breadcrumbs=[("首页", "../index.html"), ("产品", None), ("句子智库", None)],
        hero_kicker="产品 · 智库 · 记忆",
        hero_h1='句子智库 · <span class="accent">AI 员工的记忆</span>',
        hero_lede="客户给的一堆知识库资料，AI 直接用不了：散、乱、格式不一、查不准。<strong>句子智库把它炼成 AI 能查、能用的知识资产，越用越准</strong>。知识工程做对，是 Agent 上岗的前提。知识不整理，接再多资料也跑不通。",
        pills=["知识工程进场第一步", "散乱知识 → 可检索资产", "每条回答可追溯出处", "Agent 上岗的前提"],
        body=body,
    )


def page_cli():
    body = ''
    # NEW module order (Req 4.1): the pre-redesign DOM combined the problem
    # framing and the capability grid into ONE block. Here the framing leads as
    # its own module, then the four capabilities follow as a separate grid
    # module. Card markers restored to the preserved 01–04 (Req 5.2/8.4).
    body += block(
        "为什么 AI 需要一双手",
        "很多企业的核心系统，没 API、改不动",
        "AI 接入客户业务时，常受阻于同一处：用了十几年的核心系统没有 API，无人敢动。模型再强，没有执行能力也无法完成任务。句子 CLI 为 AI 配上一双手，让它像人一样直接操作界面。",
        "",
    )
    body += block(
        "",
        "",
        "",
        feat_grid([
            ("01", "像人一样操作界面", "无需 API 即可接入。CLI 直接驱动鼠标键盘、读取屏幕，像人一样操作任何软件界面。", "bl"),
            ("02", "跨系统搬运", "从一个系统取数、填入另一个系统，中间缺少接口的环节由 CLI 自动完成，无需人工来回复制粘贴。", "or"),
            ("03", "定时批处理", "对账、导表、批量录入等重复工作，配置一次即自动执行，无需人工值守。", "gr"),
            ("04", "真实沙盒隔离", "每个任务在独立沙盒中运行，异常时自动恢复，不影响其他任务，也不触及客户的其他系统。", "te"),
        ], cols=2),
        alt=True,
    )
    body += f"""
<section class="section-block">
  <div class="container">
    {cta_band("让 AI 接进你那套改不动的老系统")}
  </div>
</section>
""".strip()
    return page_layout(
        title="句子 CLI · AI 员工的手 | 句子互动",
        description="句子 CLI——AI 员工的手，操作一切人用软件的执行层。有 API 走 API，没 API 就像人一样点界面；老系统不用改造，也能接进上层。",
        rel="../",
        breadcrumbs=[("首页", "../index.html"), ("产品", None), ("句子 CLI", None)],
        hero_kicker="产品 · CLI · 手",
        hero_h1='句子 CLI · <span class="accent">AI 员工的手</span>',
        hero_lede="人在电脑上能操作的界面，CLI 都能代为操作。<strong>操作一切人用软件的执行层</strong>——有 API 走 API，没 API 就像人一样点界面，把活干完。",
        pills=["操作一切人用软件", "无 API 也能接", "老系统不用改造", "落到真实系统"],
        body=body,
    )


def _legacy_shared_proof_modules():
    """Re-present the industry-evidence statements and product positioning lines
    that the canmou & zhizao pages carried in their pre-redesign shared regions.

    Those two pages' baseline captured a stale variant of the announcement
    marquee and product-dropdown copy that the now-canonicalized shared regions
    (one uniform nav/announcement, Req 8.3) no longer emit. To keep 100% of each
    page's Preserved_Content (Req 2.1, 5.2, 8.4) without breaking shared-region
    uniformity, those strings are retained verbatim here as structured
    components built from the shared block/feat_grid snippets (Req 5.1, 5.4, 8.5).
    No text is introduced that is absent from the baseline content set (Req 5.3).
    """
    out = block(
        "客户实证",
        "",
        "1000+ 大型企业已在用 · 覆盖 5 大高合规行业 · 接入 10+ 主流 IM 渠道",
        feat_grid([
            ("01", "在线教育", "销售岗已跑通按结果付费——AI 带来的转化，是人工对照组的 3 倍", "bl"),
            ("02", "消费品电商", "几百家品牌私域导购上线，长尾客户 24×7 接住", "or"),
            ("03", "金融", "银行 · 证券 · 保险头部机构落地，合规边界提前写死", "gr"),
        ], cols=3),
        alt=True,
    )
    out += block(
        "产品",
        "",
        "",
        feat_grid([
            ("01", "句子参谋 · 参谋", "一句话查所有业务数据", "bl"),
            ("02", "句子智库 · 记忆", "知识工程，散乱知识炼成可检索资产", "or"),
            ("03", "句子秒回 · 工位", "11 个 IM 通道汇成一个工位", "gr"),
        ], cols=3),
    )
    return out


def page_canmou():
    body = ''
    # NEW module order (Req 4.1): pre-redesign ran 4件事 → 为什么 → AI分析师 →
    # 结果. Here the "why" split leads (with the role feature_list + phone demo),
    # then the 4件事 grid, the AI分析师 grid, and the KPI close. All preserved
    # strings retained verbatim (Req 5.2/8.4); long copy sits inside structured
    # components (Req 5.1/5.4).
    body += split_section(
        eyebrow="为什么需要它",
        title="BI 得你自己打开才看得到，参谋是它主动来找你",
        paragraphs=[
            "以前看数据，得先让人搭好数据看板，你再定时打开看；发现不对劲，还得找懂 SQL 的人帮你查。慢，而且全靠你自己去翻。",
            "参谋反过来：你直接问一句「这周哪批客户流失了」，秒级就有答案，想细看接着问。真出了异常，不用你盯着，它自己会提醒你。",
        ],
        bullets=[
            "<strong>给老板</strong>：在手机上问一句「今天销售有什么问题」，马上就有答案和建议",
            "<strong>给运营</strong>：问一句「上周续费率为什么降了」，参谋直接帮你定位到是哪个环节",
            "<strong>给业务团队</strong>：随时拉一份客户数据，秒级看 AI 干得怎么样，当天就能调",
        ],
        visual_html="""
<div style="background:#fff;border-radius:12px;padding:18px;border:1px solid var(--gray-line);max-width:380px;margin:0 auto;">
<div style="font-size:12px;font-weight:700;color:var(--gray-text);margin-bottom:14px;">手机上问一句 · 周一早上</div>
<div style="display:flex;flex-direction:column;gap:10px;font-size:13px;">
<div style="align-self:flex-end;background:var(--blue);color:#fff;padding:9px 13px;border-radius:11px;border-bottom-right-radius:3px;max-width:85%;">"上周续费率为什么降了？"</div>
<div style="align-self:flex-start;background:var(--gray-bg);color:var(--black);padding:9px 13px;border-radius:11px;border-bottom-left-radius:3px;max-width:90%;">↓ 续费率：78% → 71%（-7pp）</div>
<div style="align-self:flex-start;background:var(--gray-bg);color:var(--black);padding:9px 13px;border-radius:11px;border-bottom-left-radius:3px;max-width:90%;">主要原因：A 校区课时延期、B 老师离职。</div>
<div style="align-self:flex-start;background:var(--blue-light);color:var(--blue);padding:9px 13px;border-radius:11px;border-bottom-left-radius:3px;max-width:90%;">建议：A 校区先补偿 + B 老师班分流到 C 老师，预计回正 +5pp。</div>
<div style="align-self:flex-end;background:var(--blue);color:#fff;padding:9px 13px;border-radius:11px;border-bottom-right-radius:3px;max-width:85%;">"B 老师那班具体是哪些学生？"</div>
<div style="align-self:flex-start;background:var(--gray-bg);color:var(--black);padding:9px 13px;border-radius:11px;border-bottom-left-radius:3px;max-width:90%;">共 47 人。已生成名单 + 分流建议 →</div>
</div>
<div style="margin-top:14px;text-align:center;font-size:11.5px;color:var(--blue);font-weight:700;">点这里发给招生</div>
</div>
""",
        reverse=True,
    )

    body += block(        "4 件事 · 一次性给你",
        "不写 SQL、不点报表，一句话就把数据问出来",
        "无需写 SQL、查报表、等周报或对接 BI，一句话提问即可获得秒级答案。",
        feat_grid([
            ("💬", "对话即查询", "自然语言问数，秒级返回图表。无需写 SQL 或查报表，一句话即可获得结果，需要细看可继续追问。", "bl"),
            ("🔎", "越问越细", "漏斗在哪一环流失、谁的转化最高、哪段话术退费最低——问一句就有答案；想往深里看，接着追问就行。", "or"),
            ("🚨", "有问题主动提醒你", "退费苗头、客户要流失、话术踩了合规红线——不用你盯着，参谋发现了主动提醒，还会告诉你该怎么处理。", "gr"),
            ("📱", "老板手机就能用", "不用等周报、不用盯着看板，掏出手机问一句就有答案——老板、运营都能直接用。", "pu"),
        ], cols=2),
    )

    body += block(        "AI 数据分析师",
        "参谋就是一个随叫随到的数据分析师",
        "过去你得养一个数据分析师，或者排队等 BI 出报表。参谋把这件事变简单：你用大白话问，它接好公司所有数据，秒级给你图表、给你结论，还告诉你下一步该怎么做。",
        feat_grid([
            ("🔗", "先把你的数据接好", "销售、客服、订单、私域这些散在各处的数据，参谋直接接进来，不用你搭数据管道——问什么都查得到。", "bl"),
            ("💡", "不只出数，还给结论", "好的分析师不会只甩你一张图。参谋会告诉你哪里出了问题、为什么，再给一条能直接干的建议。", "or"),
            ("🔔", "主动盯着，发现就提醒", "退费苗头、客户要流失、话术踩了合规红线——不用你天天盯，参谋发现了主动来找你。", "gr"),
        ], cols=3),
        alt=True,
    )

    body += block(        "结果",
        "参谋上岗后，运营不用再等报表",
        "数据来自客户真实部署反馈。",
        kpi_row([
            ("一句话", "查公司所有数据"),
            ("秒级", "图表 / 表格 / 建议"),
            ("主动", "异常预警 + 建议"),
            ("1000+", "客户数据当样本"),
        ]),
    )

    # Retain the canmou-specific Preserved_Content from its pre-redesign shared
    # regions (Req 5.2/8.4), re-presented as structured components.
    body += _legacy_shared_proof_modules()

    body += f"""
<section class="section-block">
  <div class="container">
    {cta_band("让参谋接上你的所有数据——一句话就能问", sub="从老板的一句话 demo 开始，到运营全员日常使用——90 天内，参谋会接上你的 CRM / 业务系统 / 客服记录。")}
  </div>
</section>
""".strip()

    return page_layout(
        title="句子参谋 · 对话式数据洞察 | 句子互动",
        description="句子参谋是 AI 员工的「参谋」——把公司所有数据接进来，用对话方式问。一句话查、秒级出图表、异常主动预警、给老板用。1000+ 客户数据为样本。",
        rel="../",
        breadcrumbs=[("首页", "../index.html"), ("产品", None), ("句子参谋", None)],
        hero_kicker="产品 · 参谋",
        hero_h1='句子参谋 · <span class="accent">一句话问公司所有数据</span>',
        hero_lede="它不是一块数据看板，而是一个能对话的运营参谋。把公司所有数据接入，用自然语言提问，秒级返回图表，并支持逐层追问。退费苗头、流失风险、合规偏差会主动预警，并附上可执行的建议。老板和运营都能直接使用。",
        pills=["一句话查公司所有数据", "秒级图表 / 表格 / 建议", "异常主动预警", "1000+ 客户数据当样本"],
        body=body,
    )


def page_zhizao():
    body = ''
    # NEW module order (Req 4.1): pre-redesign ran 4件事 → 为什么 → 团队一起跑 →
    # 承诺. Here the "why this layer" split leads (with the bullets feature_list +
    # the isolated-environment panel), then the 4件事 grid, the 团队一起跑 grid,
    # and the 承诺 KPI close. All preserved strings retained verbatim
    # (Req 5.2/8.4); long copy is carried by structured components (Req 5.1/5.4).
    body += split_section(
        eyebrow="为什么需要这一层",
        title="基建不齐，AI 落不了地",
        paragraphs=[
            "金融、政务、头部教育、头部电商——这类客户最在意的，是自身独有的场景能否做下来，标品是否完善是其次。这个场景做不下来，前面的合作往往难以推进。",
            "智造补的就是这一层：团队带着秒懂 / 守护 / 参谋 进入客户现场，把缺失的环境、对接、合规一次补齐，交付一套可直接运行的系统，无需客户自行拼装。",
        ],
        bullets=[
            "<strong>合规 / 数据隔离</strong>：一客一环境，等保 / 私有化 / 国产化按客户来",
            "<strong>系统对接</strong>：CRM / 工单 / 业务库 / IM 通道，客户现有系统逐一接入",
            "<strong>独有业务</strong>：行业内尚无先例的场景，团队当周搭建上线",
            "<strong>反哺标品</strong>：跑通后选择性积累——下一个客户起步就有",
        ],
        visual_html="""
<div style="background:#fff;border-radius:12px;padding:20px;border:1px solid var(--gray-line);">
<div style="font-size:12px;font-weight:700;color:var(--gray-text);margin-bottom:14px;">客户专属环境 · 物理隔离</div>
<div style="display:flex;flex-direction:column;gap:8px;font-size:13px;">
<div style="padding:9px 13px;background:var(--blue-light);border-radius:8px;color:var(--blue);">🏠 算力：客户私有 GPU / 一体机</div>
<div style="padding:9px 13px;background:var(--green-lt);border-radius:8px;color:var(--green);">🗄 数据库：客户域内 · 不出库</div>
<div style="padding:9px 13px;background:var(--orange-lt);border-radius:8px;color:var(--orange);">🤖 Agent 运行环境：独立部署</div>
<div style="padding:9px 13px;background:var(--purple-lt);border-radius:8px;color:var(--purple);">🔌 模型层：可切 智谱 / DeepSeek / Qwen</div>
<div style="padding:9px 13px;background:var(--gray-bg);border-radius:8px;color:var(--gray-text);">↪ 对接：客户 CRM / 工单 / 知识库直连</div>
</div>
</div>
""",
        color="pu",
        reverse=True,
    )

    body += block(        "4 件事 · 智造在做",
        "补齐数字化基建，AI 才能在你的系统里跑起来",
        "AI 要在客户系统里跑，先得有数字化基建。这层缺了，Agent 再好也跑不起来——智造做的就是把它补上。",
        feat_grid([
            ("🛡", "把缺的基建补齐", "客户系统老旧、数据分散、缺少运行 AI 的独立环境。这层基建由我们的团队进场补齐，AI 才能接入。", "bl"),
            ("🏠", "一客一环境", "每个大客户一套独立部署：算力、数据库、Agent 运行环境全部隔离。客户数据不出客户域，合规、审计、政务等保都按客户标准走。", "or"),
            ("⚙️", "基础设施可配", "模型层、数据层、IM 通道层都按客户需求配——支持私有化 / 一体机 / 混合云。原有 CRM / 工单 / 知识库直连，不重做。", "gr"),
            ("🔁", "跑通的能力回流", "在一个客户那补齐的基建、打通的对接，攒成模板——下一个客户起步就少走弯路。", "pu"),
        ], cols=2),
    )

    body += block(        "和我们的团队一起跑",
        "客户的独有问题在这里被解掉",
        "团队驻于客户现场或远程支持，用秒懂搭建 Agent、用守护保障稳定、用参谋分析数据；基建缺口由团队进场补齐。一个客户验证过的对接和模板，下一个客户起步即可复用。",
        feat_grid([
            ("🛠", "进场补齐", "团队现场用智造的工程能力补齐标品未覆盖的部分，无需等待研发版本排期，当天上线。", "bl"),
            ("📦", "客户域内跑", "所有 Agent / 数据 / 模型在客户域内运行——合规、审计、国产化按客户标准走。", "or"),
            ("⚡", "选择性反哺", "跑通的场景 / 策略 / 模板，团队评估后选择性回流标品——下一个客户起步就用上。", "gr"),
        ], cols=3),
        alt=True,
    )

    body += block(        "承诺",
        "对每一个大客户的承诺",
        "把客户缺的数字化基建补齐，是 AI 落地的前提。",
        kpi_row([
            ("地基", "补齐数字化基建"),
            ("一客一环", "数据完全隔离"),
            ("私有化", "/ 一体机 / 混合云"),
            ("积累", "反哺标品，下一个客户起步更快"),
        ]),
    )

    # Retain the zhizao-specific Preserved_Content from its pre-redesign shared
    # regions (Req 5.2/8.4), re-presented as structured components.
    body += _legacy_shared_proof_modules()

    body += f"""
<section class="section-block">
  <div class="container">
    {cta_band("系统缺少 AI 落地的基建？团队可进场补齐", sub="从你最头疼的那一个独有场景开始——90 天内，第一个 Agent 在你的私有环境里上岗。")}
  </div>
</section>
""".strip()

    return page_layout(
        title="句子智造 · 补齐客户数字化基建 | 句子互动",
        description="句子智造给每个大客户补齐数字化基建——AI 要在客户系统里跑，先得有独立环境、接得通的数据、过得了的合规。一客一环境，算力 / 数据库 / Agent 全部隔离。私有化 / 一体机 / 混合云，原有 CRM / 工单 / 知识库直连。",
        rel="../",
        breadcrumbs=[("首页", "../index.html"), ("产品", None), ("句子智造", None)],
        hero_kicker="产品 · 智造 · 地基",
        hero_h1='句子智造 · <span class="accent">AI 落地的数字化地基</span>',
        hero_lede="AI 员工要在客户系统里真正跑起来，先得有数字化基建：一套独立环境、数据能打通、合规能过关。很多大客户恰好缺这一层。<strong>句子智造把这层地基补上</strong>：一客一环境，算力 / 数据库 / Agent 全隔离，支持私有化 / 一体机 / 混合云，原有 CRM / 工单 / 知识库直连。",
        pills=["补齐数字化基建", "一客一环境 · 数据隔离", "私有化 / 一体机 / 混合云", "原系统直连"],
        body=body,
    )


def build_all():
    """Build every configured page with per-page fail-fast handling (Req 8.6).

    Each page is registered as a zero-arg builder so that BOTH its content
    generation (page body / content lookup) AND its file write happen inside
    the same try block. On the first failure the builder reports the failing
    page path and the reason to stderr and exits non-zero, leaving every
    already-written page intact. Writes are atomic (temp file + os.replace) so a
    failure mid-write never corrupts or partially writes a target file.
    """
    import tempfile

    # relpath -> zero-arg callable producing that page's HTML. Generation is
    # deferred into the loop so a content-lookup failure is caught per page.
    page_builders = {
        'products/miaohui.html': page_miaohui,
        'products/miaodong.html': page_miaodong,
        'products/shouhu.html': page_shouhu,
        'products/canmou.html': page_canmou,
        'products/dongxing.html': page_dongxing,
        'products/cli.html': page_cli,
        'products/zhizao.html': page_zhizao,
        'fde.html': page_fde,
        'enterprise.html': page_enterprise,
        'industries.html': page_industries,
        'about.html': page_about,
    }

    # The 6 AI-employee pages share one builder that returns a slug->html map;
    # wrap each slug in its own deferred callable so a single failing workforce
    # page halts with its own path rather than taking down the whole batch.
    try:
        workforce = workforce_pages()
    except Exception as e:
        sys.stderr.write(f"build_pages: FAILED building workforce pages: {e}\n")
        sys.exit(1)
    for slug, content in workforce.items():
        page_builders[f'workforce/{slug}.html'] = (lambda c: (lambda: c))(content)

    built = 0
    for relpath, builder in page_builders.items():
        full = os.path.join(ROOT, relpath)
        try:
            os.makedirs(os.path.dirname(full), exist_ok=True)
            content = builder()                       # content generation / lookup
            if content is None:
                raise ValueError("page builder returned no content")
            # Atomic write: stage to a temp file in the same dir, then replace,
            # so prior successful pages and any existing target stay intact on
            # failure (Req 8.6).
            fd, tmp = tempfile.mkstemp(dir=os.path.dirname(full), suffix='.tmp')
            try:
                with os.fdopen(fd, 'w', encoding='utf-8') as f:
                    f.write(content)
                os.replace(tmp, full)
            except Exception:
                if os.path.exists(tmp):
                    os.remove(tmp)
                raise
        except Exception as e:
            sys.stderr.write(f"build_pages: FAILED on page '{relpath}': {e}\n")
            sys.exit(1)
        built += 1
        size = os.path.getsize(full)
        print(f"  {relpath}  ({size:,} bytes)")

    print(f"\nbuilt {built} pages")


if __name__ == '__main__':
    build_all()
