"""
Generate all sub-pages from structured data.
Pages: products/{miaohui,miaodong,shouhu}.html, workforce/{6 roles}.html, enterprise.html
"""
import os, html

ROOT = os.path.dirname(os.path.abspath(__file__))


# ────────────────────────── shared snippets ──────────────────────────

def nav_html(rel):
    """rel: '' for root, '../' for /products /workforce subdirs"""
    return f"""
<nav class="nav">
  <div class="container nav-inner">
    <a href="{rel}index.html" class="brand">
      <span class="brand-mark">句</span>
      句子互动 <small>JuziBot</small>
    </a>
    <div class="nav-links">
      <div class="nav-item">
        <button>产品 <span class="caret"></span></button>
        <div class="dropdown wide">
          <a href="{rel}products/miaohui.html"><div class="d-title">句子秒回 · 工位</div><div class="d-desc">Agent 和人协作的 IM 工作台</div></a>
          <a href="{rel}products/miaodong.html"><div class="d-title">句子秒懂 · 大脑</div><div class="d-desc">多 Agent 编排，业务人员无代码搭</div></a>
          <a href="{rel}products/shouhu.html"><div class="d-title">句子守护 · 主管</div><div class="d-desc">六道关口管住上线前 / 中 / 后</div></a>
          <a href="{rel}products/canmou.html"><div class="d-title">句子参谋 · 参谋</div><div class="d-desc">对话式数据洞察，一句话问数</div></a>
          <a href="{rel}products/dongxing.html"><div class="d-title">句子智库 · 记忆</div><div class="d-desc">知识工程，把散乱知识炼成可检索资产</div></a>
          <a href="{rel}products/cli.html"><div class="d-title">句子 CLI · 手</div><div class="d-desc">操作一切人用软件的底层 RPA 驱动</div></a>
          <a href="{rel}products/zhizao.html"><div class="d-title">句子智造 · 地基</div><div class="d-desc">补齐客户数字化基建，一客一环境</div></a>
        </div>
      </div>
      <div class="nav-item">
        <button>AI 员工 <span class="caret"></span></button>
        <div class="dropdown wide">
          <a href="{rel}workforce/sales.html"><div class="d-title">AI 销售</div><div class="d-desc">直播搬家、私域承接、漏斗跟进——首单成交全程接管</div></a>
          <a href="{rel}workforce/marketing.html"><div class="d-title">AI 导购</div><div class="d-desc">头部零售品牌的私域导购运营，长尾客户也覆盖</div></a>
          <a href="{rel}workforce/service.html"><div class="d-title">AI 客服</div><div class="d-desc">从售前到售后都接得住 · 5 年 BadCase 积累</div></a>
          <a href="{rel}workforce/government.html"><div class="d-title">AI 社工 / 调解员</div><div class="d-desc">政务高合规要求 + 全程可追溯 · 已稳步落地</div></a>
          <a href="{rel}workforce/finance.html"><div class="d-title">AI 顾问 / 营销</div><div class="d-desc">银行 / 证券 / 保险头部机构落地 · 9 年风控话术</div></a>
          <a href="{rel}workforce/livestream.html"><div class="d-title">AI 解说员 / 主理人</div><div class="d-desc">直播间智能解说 + 全媒体运营，一个人顶十个</div></a>
        </div>
      </div>
      <div class="nav-item"><a href="{rel}industries.html">客户与行业</a></div>
      <div class="nav-item"><a href="{rel}enterprise.html">企业级能力</a></div>
      <div class="nav-item"><a href="{rel}fde.html">FDE 交付团队</a></div>
      <div class="nav-item"><a href="{rel}insights.html">AI 原生组织</a></div>
      <div class="nav-item"><a href="{rel}about.html">关于我们</a></div>
    </div>
    <a href="{rel}index.html#cta" class="nav-cta">联系我们 →</a>
  </div>
</nav>
""".strip()


def footer_html(rel):
    return f"""
<footer>
  <div class="container">
    <div class="footer-grid">
      <div class="brand-block">
        <div class="brand">
          <span class="brand-mark">句</span>
          句子互动 <small>JuziBot</small>
        </div>
        <p>
          为企业部署 AI 劳动力。<br/>
          批量、按结果交付——9 年积累，1000+ 大型企业客户验证。
        </p>
      </div>
      <div>
        <h6>产品</h6>
        <ul>
          <li><a href="{rel}products/miaohui.html">句子秒回 · 工位</a></li>
          <li><a href="{rel}products/miaodong.html">句子秒懂 · 大脑</a></li>
          <li><a href="{rel}products/shouhu.html">句子守护 · 主管</a></li>
          <li><a href="{rel}products/canmou.html">句子参谋 · 参谋</a></li>
          <li><a href="{rel}products/dongxing.html">句子智库 · 记忆</a></li>
          <li><a href="{rel}products/cli.html">句子 CLI · 手</a></li>
          <li><a href="{rel}products/zhizao.html">句子智造 · 地基</a></li>
          <li><a href="{rel}enterprise.html">企业级能力</a></li>
        </ul>
      </div>
      <div>
        <h6>AI 员工</h6>
        <ul>
          <li><a href="{rel}workforce/sales.html">AI 销售</a></li>
          <li><a href="{rel}workforce/marketing.html">AI 导购</a></li>
          <li><a href="{rel}workforce/service.html">AI 客服</a></li>
          <li><a href="{rel}workforce/government.html">AI 社工 / 调解员</a></li>
          <li><a href="{rel}workforce/finance.html">AI 顾问 / 营销</a></li>
          <li><a href="{rel}workforce/livestream.html">AI 解说员 / 主理人</a></li>
        </ul>
      </div>
      <div>
        <h6>公司</h6>
        <ul>
          <li><a href="{rel}about.html">关于我们</a></li>
          <li><a href="{rel}fde.html">FDE 交付团队</a></li>
          <li><a href="{rel}industries.html">客户与行业</a></li>
          <li><a href="{rel}case-xingqudao.html">客户案例 · 在线教育头部</a></li>
          <li><a href="{rel}insights.html">AI 原生组织</a></li>
          <li><a href="{rel}index.html#cta">联系我们</a></li>
          <li><a href="https://github.com/wechaty/wechaty">Wechaty 开源</a></li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      <div>© 2026 句子互动 · JuziBot</div>
      <div>为企业部署 AI 劳动力 · 批量 · 按结果交付</div>
    </div>
  </div>
</footer>
""".strip()


def cta_band(text="把第一个 AI 劳动力装进你的业务流程"):
    return f"""
<div class="cta-band">
  <div>
    <h4>{text}</h4>
    <p>从一个 AI 角色起步，慢慢扩到多个 Agent。90 天内，第一个 AI 劳动力就在你的 IM 里上岗。</p>
  </div>
  <a href="mailto:hello@juzibot.com" class="btn-primary">预约演示 <span class="btn-arrow">→</span></a>
</div>
""".strip()


def page_layout(*, title, description, rel, breadcrumbs, hero_kicker, hero_h1, hero_lede,
                pills, body):
    """Generate a complete sub-page."""
    crumbs_html = ' <span class="sep">/</span> '.join(
        f'<a href="{href}">{label}</a>' if href else f'<span class="here">{label}</span>'
        for label, href in breadcrumbs
    )
    pills_html = ''
    if pills:
        pills_html = '<div class="pill-row">' + ''.join(
            f'<span class="pill"><span class="dot"></span>{p}</span>' for p in pills
        ) + '</div>'
    contact_modal = f"""
<!-- ════════════ RIGHT FLOAT PANEL ════════════ -->
<div class="float-panel" id="floatPanel">
  <button class="fp-btn" onclick="openContact('在线咨询')">
    <span class="fp-icon">💬</span>在线咨询
    <span class="fp-tip">在线咨询</span>
  </button>
  <button class="fp-btn fp-orange" onclick="openContact('预约演示')">
    <span class="fp-icon">📅</span>预约演示
    <span class="fp-tip">预约 Demo 演示</span>
  </button>
  <button class="fp-btn fp-green" onclick="openContact('获取方案')">
    <span class="fp-icon">📋</span>获取<br/>方案
    <span class="fp-tip">获取行业解决方案</span>
  </button>
</div>

<!-- ════════════ CONTACT MODAL ════════════ -->
<div class="modal-overlay" id="contactModal">
  <div class="modal" style="max-width:520px;" role="dialog" aria-modal="true">
    <div class="modal-hd" style="padding:26px 32px 24px;">
      <button class="mclose" onclick="closeModal('contactModal')" aria-label="关闭">×</button>
      <div class="meyebrow">联系我们</div>
      <h3 id="contactTitle" style="font-size:20px;margin-bottom:0;">预约演示 / 获取方案</h3>
    </div>
    <div class="modal-bd">
      <div id="cfForm">
        <div class="cf-row">
          <input class="cf-input" type="text" placeholder="您的姓名 *" id="cf-name">
          <input class="cf-input" type="text" placeholder="公司名称 *" id="cf-company">
        </div>
        <div class="cf-row">
          <input class="cf-input" type="tel" placeholder="手机号 *" id="cf-phone">
          <select class="cf-input" id="cf-industry">
            <option value="" disabled selected>所在行业</option>
            <option>在线教育</option>
            <option>消费品电商</option>
            <option>金融（银行 / 证券 / 保险）</option>
            <option>政务 / 司法</option>
            <option>泛互联网</option>
            <option>其他</option>
          </select>
        </div>
        <div class="cf-row full">
          <textarea class="cf-input" placeholder="想了解什么？具体场景描述一下（选填）" id="cf-msg" style="height:80px;resize:none;"></textarea>
        </div>
        <button class="cf-submit" onclick="submitContact()">提交 — 工作日当天回复</button>
        <p class="m-note" style="margin-top:12px;text-align:center;font-size:12.5px;color:var(--gray-text);">也可以直接发邮件：<a href="mailto:hello@juzibot.com" style="color:var(--blue);font-weight:700;">hello@juzibot.com</a></p>
      </div>
      <div id="cfSuccess" style="text-align:center;padding:32px 20px;display:none;">
        <div style="font-size:48px;margin-bottom:12px;">✅</div>
        <h4 style="font-size:20px;font-weight:800;margin-bottom:8px;">收到了，稍等一下</h4>
        <p style="color:var(--gray-text);font-size:14.5px;">工作日内联系您。如果比较急：<a href="mailto:hello@juzibot.com" style="color:var(--blue);font-weight:700;">hello@juzibot.com</a></p>
      </div>
    </div>
  </div>
</div>

<script>
function openModal(id){{var el=document.getElementById(id);if(!el)return;el.classList.add('open');document.body.style.overflow='hidden';}}
function closeModal(id){{var el=document.getElementById(id);if(!el)return;el.classList.remove('open');document.body.style.overflow='';}}
document.querySelectorAll('.modal-overlay').forEach(function(o){{o.addEventListener('click',function(e){{if(e.target===o)closeModal(o.id);}});}});
document.addEventListener('keydown',function(e){{if(e.key==='Escape')document.querySelectorAll('.modal-overlay.open').forEach(function(m){{closeModal(m.id);}});}});
function openContact(t){{var el=document.getElementById('contactTitle');if(el)el.textContent=t||'联系我们';openModal('contactModal');}}
function submitContact(){{
  var n=(document.getElementById('cf-name').value||'').trim();
  var c=(document.getElementById('cf-company').value||'').trim();
  var p=(document.getElementById('cf-phone').value||'').trim();
  if(!n||!c||!p){{alert('请填写姓名、公司名和手机号');return;}}
  document.getElementById('cfForm').style.display='none';
  document.getElementById('cfSuccess').style.display='block';
}}
(function(){{
  var fp=document.getElementById('floatPanel');if(!fp)return;
  fp.style.opacity='0';fp.style.transition='opacity .3s ease';
  window.addEventListener('scroll',function(){{fp.style.opacity=window.scrollY>200?'1':'0';fp.style.pointerEvents=window.scrollY>200?'':'none';}},{{passive:true}});
}})();
</script>
""".strip()

    return f"""<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover" />
<title>{title}</title>
<meta name="description" content="{description}" />
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' rx='8' fill='%231659E5'/%3E%3Ctext x='16' y='22' font-family='system-ui' font-size='18' font-weight='800' fill='white' text-anchor='middle'%3E句%3C/text%3E%3C/svg%3E" />
<link rel="stylesheet" href="{rel}assets/style.css">
</head>
<body>

<!-- ════════════ ANNOUNCEMENT BAR ════════════ -->
<div class="ann-bar" role="marquee" aria-label="公告">
  <div class="ann-track">
    <span class="ann-item"><span class="dot"></span><span class="tag">在线教育</span>400+ 家头部公司已部署，AI 销售人均承接 5 倍以上</span>
    <span class="ann-item"><span class="dot"></span><span class="tag">消费品电商</span>几百家头部品牌私域导购上线，长尾客户再不流失</span>
    <span class="ann-item"><span class="dot"></span><span class="tag">金融</span>银行 · 证券 · 保险头部机构落地，合规边界提前写死</span>
    <span class="ann-item"><span class="dot"></span>1000+ 大型企业已在用 · 扎在这 5 个行业 · 89% 对话自动完成率</span>
    <span class="ann-item"><span class="dot"></span><span class="tag">在线教育</span>400+ 家头部公司已部署，AI 销售人均承接 5× 以上</span>
    <span class="ann-item"><span class="dot"></span><span class="tag">消费品电商</span>几百家头部品牌私域导购上线，长尾客户再不流失</span>
    <span class="ann-item"><span class="dot"></span><span class="tag">金融</span>银行 · 证券 · 保险头部机构落地，合规边界提前写死</span>
    <span class="ann-item"><span class="dot"></span>1000+ 大型企业已在用 · 扎在这 5 个行业 · 89% 对话自动完成率</span>
  </div>
</div>

{nav_html(rel)}

<header class="page-hero">
  <div class="container">
    <div class="crumbs">{crumbs_html}</div>
    <div style="font-size:13px;font-weight:800;color:var(--orange);letter-spacing:.12em;text-transform:uppercase;margin-bottom:16px;">{hero_kicker}</div>
    <h1>{hero_h1}</h1>
    <p class="lede">{hero_lede}</p>
    {pills_html}
  </div>
</header>

{body}

{footer_html(rel)}

{contact_modal}

</body>
</html>
"""


# ────────────────────────── content for each page ──────────────────────────

def feat_grid(items, cols=3):
    """items: list of (icon, title, desc, color_class)"""
    cls = f"feat-grid-{cols}"
    blocks = ''.join(
        f'<div class="feat-block {color}"><div class="ic">{icon}</div><h3>{title}</h3><p>{desc}</p></div>'
        for icon, title, desc, color in items
    )
    return f'<div class="{cls}">{blocks}</div>'


def kpi_row(items):
    """items: list of (value, label)"""
    cells = ''.join(
        f'<div><div class="v">{v}</div><div class="l">{l}</div></div>'
        for v, l in items
    )
    return f'<div class="kpi-row">{cells}</div>'


def split_section(*, eyebrow, title, paragraphs, bullets, visual_html, color="bl", reverse=False):
    """split section with text on left, visual on right (or reverse)"""
    p_html = ''.join(f'<p>{p}</p>' for p in paragraphs)
    b_html = ''
    if bullets:
        b_html = '<ul>' + ''.join(f'<li>{b}</li>' for b in bullets) + '</ul>'
    rcls = ' reverse' if reverse else ''
    visual_color = {'bl': '', 'or': ' or', 'gr': ' gr'}.get(color, '')
    return f"""
<section class="section-block">
  <div class="container">
    <div class="split{rcls}">
      <div class="split-text">
        <div class="eyebrow">{eyebrow}</div>
        <h3>{title}</h3>
        {p_html}
        {b_html}
      </div>
      <div class="split-visual{visual_color}">
        {visual_html}
      </div>
    </div>
  </div>
</section>
""".strip()


def block(eyebrow, title, sub, content, alt=False):
    cls = " alt" if alt else ""
    return f"""
<section class="section-block{cls}">
  <div class="container">
    <div class="block-head">
      <div class="eyebrow">{eyebrow}</div>
      <h2>{title}</h2>
      <div class="sub">{sub}</div>
    </div>
    {content}
  </div>
</section>
""".strip()


def cta_section(rel="../"):
    return f"""
<section class="section-block">
  <div class="container">
    {cta_band()}
  </div>
</section>
""".strip()


# ────────────────────────── page bodies ──────────────────────────

def page_miaohui():
    body = ''
    body += '''
<section class="product-shot-section">
  <div class="container">
    <img src="../assets/product-shots/miaohui-aggregation.png" alt="句子秒回 - 全社交媒体聚合工作台" loading="lazy">
  </div>
</section>
'''.strip()
    body += block(        "5 大核心能力",
        "Agent 在 IM 通道上岗，需要的不止是聊天框",
        "句子秒回是 AI 劳动力的工位。11 个 IM 通道收到一个工作台，Agent 像真人一样上班、协作、接受管理。",
        feat_grid([
            ("📥", "多平台聚合", "11 个 IM 通道（企微、抖音、小红书、WhatsApp、飞书、钉钉、公众号、小程序、TikTok、Instagram）统一到一个工作台，海内外账号一起管。", "bl"),
            ("🎯", "主动外呼", "私聊 / 群聊群发、SOP 自动跟进、自动加好友、新客欢迎语——一次配置批量执行，不受原生应用群发次数限制。", "or"),
            ("🤝", "人机协作", "AI 全自动 / 人机协作 / 纯人工三种模式，AI 干不了的活自动转人工，每条消息可追溯。", "gr"),
            ("👥", "员工协作", "一人管多账号、多人管一账号都支持。系统智能分配消息，管理者统一查看营销数据和员工绩效。", "pu"),
            ("💾", "聊天历史", "每一条对话安全留存，支持按客户、关键词、时间多维搜索，导出方便后续分析。", "te"),
            ("🔌", "API 集成", "对接客户已有的 CRM / 工单 / 知识库系统，Agent 上岗就接管真实业务流，不孤立运行。", "bl"),
        ], cols=3),
    )

    body += split_section(
        eyebrow="架构",
        title="三大控制台 + 一个工作台，覆盖企业全角色",
        paragraphs=[
            "句子秒回按企业组织结构搭协作系统。管理者、小组负责人、一线客服各有自己的工作台，权限和数据分开。",
        ],
        bullets=[
            "<strong>企业控制台</strong>：管理者全局视角，跨小组操作，全公司数据看板",
            "<strong>小组控制台</strong>：小组负责人配置 SOP、群发、加好友、群运营",
            "<strong>聚合聊天工作台</strong>：客服 / 销售日常回复，AI 辅助 + 团队协作",
            "<strong>AI 运营工作台</strong>：AI 运营人员效果调优、数据洞察",
        ],
        visual_html="""
<div style="font-family:monospace;font-size:11.5px;line-height:1.85;color:var(--gray-text);background:#fff;padding:20px;border-radius:12px;border:1px solid var(--gray-line);">
<div style="font-weight:800;color:var(--blue);margin-bottom:12px;font-size:13px;">句子互动 SaaS 平台</div>
<div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:8px;">
  <div style="background:var(--blue-light);border-radius:8px;padding:10px;color:var(--blue);">
    <div style="font-weight:700;font-size:12px;">企业控制台</div>
    <div style="font-size:10.5px;margin-top:4px;">管理者</div>
  </div>
  <div style="background:var(--orange-lt);border-radius:8px;padding:10px;color:var(--orange);">
    <div style="font-weight:700;font-size:12px;">小组控制台</div>
    <div style="font-size:10.5px;margin-top:4px;">运营组长</div>
  </div>
  <div style="background:var(--green-lt);border-radius:8px;padding:10px;color:var(--green);">
    <div style="font-weight:700;font-size:12px;">聚合聊天</div>
    <div style="font-size:10.5px;margin-top:4px;">客服 / 销售</div>
  </div>
</div>
<div style="text-align:center;margin:14px 0;color:var(--gray-text);">▲ AI 能力</div>
<div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;">
  <div style="background:var(--purple-lt);border-radius:8px;padding:10px;color:var(--purple);">
    <div style="font-weight:700;font-size:12px;">秒懂 AI 平台</div>
    <div style="font-size:10.5px;margin-top:4px;">知识库 + 智能体 + 工作流</div>
  </div>
  <div style="background:var(--teal-lt);border-radius:8px;padding:10px;color:var(--teal);">
    <div style="font-weight:700;font-size:12px;">AI 运营</div>
    <div style="font-size:10.5px;margin-top:4px;">AISOP + 调优 + 洞察</div>
  </div>
</div>
</div>
""",
    )

    body += block(        "11 个 IM 通道",
        "客户在哪里，Agent 就在哪里上岗",
        "9 年积累的 IM 通道适配——从国内 IM 通道到海外 WhatsApp，从抖音直播私信到飞书企业 IM，一个工作台管完。",
        '<div style="display:grid;grid-template-columns:repeat(4,1fr);gap:14px;max-width:920px;margin:0 auto;">'
        + ''.join(
            f'<div style="padding:18px 16px;background:#fff;border:1px solid var(--gray-line);border-radius:12px;text-align:center;"><div style="font-size:24px;margin-bottom:6px;">{ic}</div><div style="font-size:13.5px;font-weight:700;">{n}</div><div style="font-size:11.5px;color:var(--gray-text);margin-top:2px;">{d}</div></div>'
            for ic, n, d in [
                ("💬", "企微", "私域核心"),
                ("🏢", "企业微信", "企业号"),
                ("🎵", "抖音", "私信 + 直播"),
                ("📕", "小红书", "种草沟通"),
                ("✉️", "WhatsApp", "海外业务"),
                ("☁️", "飞书", "企业 IM"),
                ("📱", "钉钉", "企业 IM"),
                ("📢", "公众号", "私域承接"),
                ("📟", "小程序", "客服入口"),
                ("🌍", "TikTok", "海外短视频"),
                ("📷", "Instagram", "海外种草"),
                ("➕", "...", "持续接入"),
            ]
        )
        + '</div>',
        alt=True,
    )

    body += split_section(
        eyebrow="主动外呼",
        title="一次配置，批量执行的 SOP 引擎",
        paragraphs=[
            "传统群发受 IM 平台规则限制：次数有限，时间窗口卡死，没法做定向。句子秒回的 SOP 引擎绕开这些限制，Agent 像真人一样按节奏跟进客户。",
        ],
        bullets=[
            "私聊 / 群聊群发：一次配置自动发给成百上千客户",
            "SOP 自动执行：Day 1 欢迎语、Day 3 产品介绍、Day 7 优惠券——按时间线推进",
            "自动加好友：批量导入目标客户，系统按节奏发申请",
            "新客欢迎语：加上好友自动响应，避免冷场",
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

    body += block(        "结果",
        "客户用句子秒回拿到的实际效果",
        "数据来自 9 年部署的真实客户案例。",
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
        title="句子秒回 · IM 通道里的 AI 劳动力工位 | 句子互动",
        description="句子秒回是企业级多 IM 聚合管理平台——11 个 IM 通道一个工作台管完，AI 智能回复、SOP 自动跟进、人机协作。1000+ 企业客户验证。",
        rel="../",
        breadcrumbs=[("首页", "../index.html"), ("产品", None), ("句子秒回", None)],
        hero_kicker="产品 · 01",
        hero_h1='句子秒回 · <span class="accent">让 AI 劳动力在 IM 通道上岗</span>',
        hero_lede="把企业的 11 个 IM 通道（企微、抖音、小红书、WhatsApp 等）聚合到一个工作台，<strong>Agent 真的在客户面前接管对话</strong>——主动外呼、智能回复、人机协作、多平台一个工作台管完。",
        pills=["11 个 IM 通道", "1000+ 企业客户", "89% 对话自动完成率", "9 年通道适配积累"],
        body=body,
    )


def page_miaodong():
    body = ''
    body += '''
<section class="product-shot-section">
  <div class="container">
    <img src="../assets/product-shots/miaodong-matrix.png" alt="句子秒懂 - Agentic AI 平台功能矩阵" loading="lazy">
  </div>
</section>
'''.strip()
    body += block(        "5 大核心模块",
        "Agent 真的「懂业务」的地方",
        "句子秒懂是 AI 劳动力的「大脑」。把企业的流程、知识、规则封装进 Agent，让 AI 不止会聊天，还能替企业干活。",
        feat_grid([
            ("🧠", "知识库管理", "把企业的产品文档、FAQ、网页内容、数据表导入知识库，AI 基于真实业务知识答得准、不跑偏。", "bl"),
            ("🤖", "智能体与工作流", "三种智能体类型 + Canvas 可视化工作流编辑器，不写代码就能配置 Agent 行为逻辑。", "or"),
            ("📊", "知识分析", "AI 自动打标分类、管理标签体系、分析知识覆盖度，找出没覆盖的客户问题。", "gr"),
            ("📝", "会话小结", "AI 自动分析聊天内容生成对话摘要，客户意向、关键诉求、跟进建议一目了然。", "pu"),
            ("🔌", "插件应用", "对接 CRM、工单、订单系统、天气工具等，Agent 不止能回话，能真的执行业务动作。", "te"),
            ("📈", "AI 调优", "BadCase 跟进 + 模型微调 + 调优中心——客户业务结果反馈到 Agent，越用越懂业务。", "bl"),
        ], cols=3),
    )

    body += split_section(
        eyebrow="知识库",
        title="不是大模型在猜，是 AI 真的读过你的业务文档",
        paragraphs=[
            "通用大模型的回答来自公开语料。它不知道你的产品参数，不懂你的合规边界，不知道你的促销规则。",
            "句子秒懂的知识库让 AI 基于<strong>你企业自己的文档</strong>回答客户：FAQ、产品手册、网页内容、内部规则、合规话术，一次导入，AI 永远查得到。",
        ],
        bullets=[
            "支持文档、网页、表格、API 等多种格式导入",
            "AI 自动分块 + 向量化，毫秒级检索匹配",
            "知识覆盖度分析：哪些问题客户问了但 AI 没答好",
            "版本管理：文档更新后 AI 同步更新",
            "多知识库隔离：不同业务线、不同行业各管各的",
        ],
        visual_html="""
<div style="background:#fff;border-radius:12px;padding:18px;border:1px solid var(--gray-line);">
<div style="font-size:12px;font-weight:700;color:var(--gray-text);margin-bottom:14px;letter-spacing:.04em;">知识库 · 已导入 · 247 篇</div>
<div style="display:flex;flex-direction:column;gap:8px;font-size:13px;">
<div style="display:flex;align-items:center;gap:10px;padding:8px 10px;background:var(--blue-light);border-radius:8px;"><span style="font-size:16px;">📄</span><span style="flex:1;">产品规格手册 v3.2</span><span style="font-size:11px;color:var(--gray-text);">128 chunks</span></div>
<div style="display:flex;align-items:center;gap:10px;padding:8px 10px;background:var(--orange-lt);border-radius:8px;"><span style="font-size:16px;">❓</span><span style="flex:1;">FAQ · 售前售后</span><span style="font-size:11px;color:var(--gray-text);">312 chunks</span></div>
<div style="display:flex;align-items:center;gap:10px;padding:8px 10px;background:var(--green-lt);border-radius:8px;"><span style="font-size:16px;">🔒</span><span style="flex:1;">合规话术库</span><span style="font-size:11px;color:var(--gray-text);">86 chunks</span></div>
<div style="display:flex;align-items:center;gap:10px;padding:8px 10px;background:var(--purple-lt);border-radius:8px;"><span style="font-size:16px;">💰</span><span style="flex:1;">2026 Q1 促销规则</span><span style="font-size:11px;color:var(--gray-text);">42 chunks</span></div>
<div style="display:flex;align-items:center;gap:10px;padding:8px 10px;background:var(--gray-bg);border-radius:8px;color:var(--gray-text);"><span style="font-size:16px;">🌐</span><span style="flex:1;">官网内容（自动同步）</span><span style="font-size:11px;">同步中</span></div>
</div>
</div>
""",
    )

    body += split_section(
        eyebrow="智能体 + 工作流",
        title="可视化拼装 Agent，不用写代码",
        paragraphs=[
            "Canvas 可视化编辑器——拖拽节点连成 Agent 工作流。条件判断、知识库查询、模型调用、工具调用、转人工——每一步都看得见、改得动。",
            "运营人员自己就能配 Agent 行为，不用等开发排期。Agent 不对的时候，运营在 Canvas 上改一下就好。",
        ],
        bullets=[
            "三种智能体：对话型 / 任务型 / 多 Agent 协作",
            "100+ 种主流大模型可选：DeepSeek、Claude、文心、通义、GPT 等",
            "版本管理 + 灰度发布：新版本可控上线",
            "工作流模板库：每个行业都有起跑模板",
        ],
        visual_html="""
<div style="background:#fff;border-radius:12px;padding:18px;border:1px solid var(--gray-line);font-family:monospace;font-size:11.5px;">
<div style="font-weight:700;color:var(--orange);margin-bottom:14px;font-family:'PingFang SC';font-size:13px;">智能体 · 售前咨询 v2.1</div>
<div style="display:flex;flex-direction:column;gap:6px;color:var(--gray-text);">
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

    body += block(        "5 个高合规高垂直行业的策略库",
        "9 年扎根，不是通用模板",
        "通用 Agent 平台 1 年能搭出框架，但 5 个行业的 know-how，1 年追不上。",
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

    body += block(        "结果",
        "AI 真懂业务的客户拿到的效果",
        "AI 不止回话，还接管业务。",
        kpi_row([
            ("100+", "支持的大模型种类"),
            ("89%", "对话自动完成率"),
            ("5 个", "高合规行业策略库"),
            ("9 年", "outcome 反馈数据"),
        ]),
    )

    body += f"""
<section class="section-block">
  <div class="container">
    {cta_band("用句子秒懂训练你的 AI 劳动力")}
  </div>
</section>
""".strip()

    return page_layout(
        title="句子秒懂 · AI 劳动力的「大脑」 | 句子互动",
        description="句子秒懂是 Agent workflow 引擎——把企业流程、规则、知识训练进 AI，让 Agent 真的懂业务。100+ 大模型支持、Canvas 可视化工作流、5 个高合规行业策略库。",
        rel="../",
        breadcrumbs=[("首页", "../index.html"), ("产品", None), ("句子秒懂", None)],
        hero_kicker="产品 · 02",
        hero_h1='句子秒懂 · <span class="accent">让 AI 真的懂你的业务</span>',
        hero_lede="不是把通用大模型套上你的 logo，是<strong>把你的产品文档、SOP、合规规则训练进 Agent</strong>——AI 基于你企业自己的知识回答客户、按你的工作流处理业务。",
        pills=["100+ 大模型支持", "Canvas 可视化工作流", "5 个高合规行业策略库", "9 年 outcome 数据反哺"],
        body=body,
    )


def page_shouhu():
    body = ''

    # ── 为什么：上一代 vs 下一代 ──
    body += block(        "为什么要守护",
        "Agent 上线，不能是一场赌博",
        "上一代 AI 搭完流程节点就算交付，上线就撒手。句子守护交付的是一个有人盯着的 AI 员工。上线前测够，上线后看得见。",
        '''<div style="max-width:980px;margin:0 auto;border:1px solid var(--gray-line);border-radius:16px;overflow:hidden;">
<div style="display:grid;grid-template-columns:1fr 1fr;">
  <div style="background:var(--gray-bg);padding:15px 22px;font-weight:800;font-size:13.5px;color:var(--gray-text);">上一代 · 搭完流程就交付</div>
  <div style="background:var(--green-lt);padding:15px 22px;font-weight:800;font-size:13.5px;color:var(--green);">句子守护 · 守护你的 AI 员工</div>
</div>
''' + ''.join(
            f'''<div style="display:grid;grid-template-columns:1fr 1fr;border-top:1px solid var(--gray-line);">
  <div style="padding:14px 22px;font-size:13.5px;color:var(--gray-text);line-height:1.6;">{old}</div>
  <div style="padding:14px 22px;font-size:13.5px;color:var(--black);line-height:1.6;background:#fbfdfc;">{new}</div>
</div>'''
            for old, new in [
                ("测试用例靠人手写，几十条到头，覆盖不全", "AI 读懂业务流程，几分钟生成上百条用例"),
                ("上线就是终点，坏了没人知道、客户看不到", "六道关口逐关把关，不达标不上线"),
                ("版本一改，老功能悄悄崩，上线才暴露", "上线后 AI 工单、质检接着盯，问题主动冒出来"),
                ("做了多少质量活，客户完全无感", "Agent 健康度看板，做了什么客户一眼看见"),
            ]
        ) + '</div>',
    )

    # ── 健康度仪表盘（示意数据）──
    body += block(        "客户看得见",
        "每天打开，就知道你的 AI 员工今天健不健康",
        "客户不用问我们做了什么。一个看板摆在那：今天为这个 Agent 做了哪些动作、五个维度各到什么程度、健康度多少分。",
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

    # ── 六道关口 ──
    body += block(        "六道关口",
        "每个 Agent 上线，都要过六道关口",
        "把上线前、上线中、上线后该做的检查，排成六道关。一关不过，不上线。",
        feat_grid([
            ("①", "AI 生成测试用例 · 上线前", "AI 读懂流程引擎配置和业务场景，几分钟生成上百条用例。不满意接着聊、重新出。还能拿 SOP 流程图、客户资料包、真实历史对话、新旧版本差异来喂——连提示词改了哪都能覆盖。", "bl"),
            ("②", "批量验收 · 上线前", "跑一轮通过率 98% 看着高，其实大模型每次输出有误差。设好轮数和并发跑多轮，逐条判断回复对不对，把没过的挑出来调，好用例攒进回归集。", "or"),
            ("③", "灰度测试 · 上线中", "想验证新版又怕影响线上。开灰度生成密钥，只有拿到密钥的那条会话走新版，其他人照旧。效果可对比，一键关掉就回到正式版。", "gr"),
            ("④", "回归测试 · 放行前强制", "新版一改，老功能可能悄悄坏。回归集跟版本绑定，上线前强制跑：不少于 50 条、通过率必须 100% 才放行。每次结果归档，质量怎么变的可追溯。", "pu"),
            ("⑤", "AI 工单 · 上线后", "AI 答错难免，麻烦的是客户没处反馈，也不知道有没有人管。客户在对话里点踩，工单进我们调优中心，也进客户那边的看板，处理完状态回执。", "te"),
            ("⑥", "AI 质检 · 上线后", "人工质检成本高、覆盖有限。建质检模板,对线上对话批量抽检，给出会话数、未通过比例，可二次复检——人工客服和 AI 客服一套标准。", "bl"),
        ], cols=3),
    )

    # ── 一键测试报告 ──
    body += split_section(
        eyebrow="秀给客户看",
        title="一句话生成一份测试报告——把工程量摆到客户面前",
        paragraphs=[
            "六道关口背后是大量工程活。客户感受不到，就等于没做。",
            "每次版本交付，一句话生成一份标准测试报告：哪些用例过了、哪些被拦在上线前、问题出在哪。哪怕通过率不高，也说明问题全拦住了，没漏到线上。",
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

    body += f"""
<section class="section-block">
  <div class="container">
    {cta_band("让句子守护把住你的 Agent 质量底线")}
  </div>
</section>
""".strip()

    return page_layout(
        title="句子守护 · 守护你的 AI 员工 | 句子互动",
        description="句子守护——守护你的 AI 员工，Agent 健康度看得见。六道关口管住上线前 / 中 / 后：AI 生成测试用例、批量验收、灰度测试、回归测试、AI 工单、AI 质检。没人拍板不上线，可追溯可审计。",
        rel="../",
        breadcrumbs=[("首页", "../index.html"), ("产品", None), ("句子守护", None)],
        hero_kicker="产品 · 守护 · 主管",
        hero_h1='句子守护 · <span class="accent">守护你的 AI 员工</span>',
        hero_lede="我们为你的每一个 AI 员工做了什么、效果如何，一眼可见。<strong>六道关口管住上线前 / 中 / 后</strong>——AI 自动生成用例、批量验收、灰度测试、回归测试、AI 工单、AI 质检。没人拍板不上线，可追溯可审计。",
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
        title=f"{title} · {kicker} | 句子互动 AI 劳动力",
        description=f"{title}——{lede[:120]}",
        rel="../",
        breadcrumbs=[("首页", "../index.html"), ("AI 劳动力", None), (title, None)],
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
        kicker='AI 劳动力 · 销售岗',
        h1='AI 销售 · <span class="accent">从建联到首单成交</span>',
        lede='直播搬家、私域承接、漏斗跟进、续费提醒——<strong>从客户建联到下第一单的全部环节，AI 销售都能接管</strong>。已覆盖直播带货行业头部公司，行业整体提效 80%+。',
        pills=['+80% 行业整体提效', '直播带货头部覆盖', '24×7 在岗', '按结果计价'],
        color='bl',
        industry='直播 · 教育 · 电商',
        role_desc='传统销售跟不上的客户量，AI 销售扛得住',
        pain_paragraphs=[
            '直播间一场流量进来 5 万人，私域 2000 人建联。客户问题都集中在前 1 小时，人手再多也跟不上。',
            '客户一建联，AI 销售就接管对话：自我介绍、问需求、讲产品、约课。难的活才转给真人销售。',
        ],
        pain_bullets=[
            '直播搬家：直播间客户建联后立刻 AI 跟进，不放冷',
            '需求挖掘：3-5 轮对话摸清客户意向、收入水平、购买动机',
            '产品讲解：从知识库里找对应产品，按客户类型推荐',
            '促销执行：限时优惠、价格策略、组合方案，按公司规则执行',
            '续费提醒：到期前 N 天 AI 主动跟进，按客户 RFM 分层',
        ],
        pain_visual="""
<div style="background:#fff;border-radius:12px;padding:18px;border:1px solid var(--gray-line);">
<div style="font-size:12px;font-weight:700;color:var(--blue);margin-bottom:12px;">AI 销售 · 当日数据</div>
<div style="display:flex;flex-direction:column;gap:14px;">
<div><div style="font-size:11px;color:var(--gray-text);">新建联</div><div style="font-size:24px;font-weight:800;color:var(--blue);">2,847</div></div>
<div><div style="font-size:11px;color:var(--gray-text);">主动外呼</div><div style="font-size:24px;font-weight:800;color:var(--orange);">5,124</div></div>
<div><div style="font-size:11px;color:var(--gray-text);">高意向客户</div><div style="font-size:24px;font-weight:800;color:var(--green);">386</div></div>
<div><div style="font-size:11px;color:var(--gray-text);">今日成交</div><div style="font-size:24px;font-weight:800;color:var(--purple);">73 单 · ¥58,420</div></div>
</div>
</div>
""",
        capability_block=feat_grid([
            ('💬', '7×24 在岗', '凌晨 3 点也能接待，客户不再因为客服下班流失。', 'bl'),
            ('📋', '业务流程标准化', '同一个客户换了销售，听到的话术也一样，不会因为人走了就退步。', 'or'),
            ('🎯', '客户分层', '按 RFM、来源、行为分层，不同客户给不同话术，转化更高。', 'gr'),
            ('🔁', '智能跟进', 'SOP 自动跟进 + AI 决策何时介入：未读消息提醒、流失前召回、续费前转化。', 'pu'),
            ('🤝', '人机协作', '高意向客户直接转给真人成交，AI 把客户预热到位再交接。', 'te'),
            ('📊', '数据积累', '每段对话都打标记录，哪句话术成交率最高，下次自动用。', 'bl'),
        ], cols=3),
        kpi_items=[
            ('80%', '行业整体提效'),
            ('5×', '人均承接客户量'),
            ('24×7', '不下班的销售'),
            ('+38.6%', '转化率提升（中位数）'),
        ],
        cta_text='让 AI 销售在你的私域上岗',
    )

    # ────── AI 导购 ──────
    pages['marketing'] = page_workforce(
        slug='marketing',
        title='AI 导购',
        kicker='AI 劳动力 · 零售岗',
        h1='AI 导购 · <span class="accent">长尾客户也覆盖到</span>',
        lede='覆盖主流头部零售品牌的私域导购运营——<strong>人工招呼不过来的长尾客户，由 AI 接管</strong>。24×7 在线响应，转化不掉队。',
        pills=['几百家品牌已部署', '24×7 在线', '私域导购全自动', '到店导购 + 线上协同'],
        color='or',
        industry='消费品 · 零售品牌',
        role_desc='把人工导购的服务能力，复制到每一个长尾客户身上',
        pain_paragraphs=[
            '一家品牌私域有 50 万客户，活跃的 5%，沉睡的 95%。人工导购一天能服务 200 个客户，剩下的没人管。',
            'AI 导购把人工导购的服务能力复制到每一个长尾客户身上：到货提醒、新品种草、试穿建议、尺码推荐、活动通知——长尾客户也被持续唤起。',
        ],
        pain_bullets=[
            '到货提醒：缺码缺色商品到货时主动通知关注客户',
            '新品种草：按客户偏好（风格、价位、品类）推',
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
<div style="background:var(--gray-bg);padding:9px 12px;border-radius:8px;">还有同色系的腰带搭配，配着穿超有型 ✨</div>
<div style="background:var(--orange);color:#fff;margin-left:auto;padding:9px 12px;border-radius:8px;max-width:80%;">嗯帮我拼下单</div>
</div>
<div style="margin-top:12px;display:flex;gap:8px;font-size:11px;">
<div style="flex:1;background:var(--blue-light);color:var(--blue);padding:6px;border-radius:6px;text-align:center;font-weight:700;">已下单</div>
<div style="flex:1;background:var(--green-lt);color:var(--green);padding:6px;border-radius:6px;text-align:center;font-weight:700;">客单 +¥420</div>
</div>
</div>
""",
        capability_block=feat_grid([
            ('🛍️', '商品智能推荐', '基于客户购买历史 + 浏览行为 + 标签体系，对着客户推。', 'or'),
            ('📅', '活动节奏管理', '双 11、618、品牌日等大促，按计划批量推送给对应客户。', 'bl'),
            ('🎁', '会员运营', '生日礼、积分到期、等级升降，按会员体系自动执行营销动作。', 'gr'),
            ('🛒', '购物车救援', '加购未付款客户分层召回，限时优惠自动触发。', 'pu'),
            ('💼', '门店协同', '线下导购加客户企微 → AI 接管后续运营，门店人均服务客户量翻倍。', 'te'),
            ('📈', '复购挖掘', 'NPS 调研 + 老客户回访，把睡着的客户叫回来。', 'or'),
        ], cols=3),
        kpi_items=[
            ('几百家', '头部零售品牌部署'),
            ('24×7', '私域全天在岗'),
            ('5×+', '导购人效杠杆'),
            ('95%+', '客户咨询响应率'),
        ],
        cta_text='让 AI 导购覆盖你的长尾客户',
    )

    # ────── AI 客服 ──────
    pages['service'] = page_workforce(
        slug='service',
        title='AI 客服',
        kicker='AI 劳动力 · 客服岗',
        h1='AI 客服 · <span class="accent">从售前咨询到售后投诉</span>',
        lede='结合 5 年积累的 BadCase 标注数据——<strong>疑难场景比通用客服处理得深</strong>。售前咨询、订单跟进、投诉处理、退换货全流程接管。',
        pills=['89% 自动完成率', '5 年 BadCase 积累', '全行业可用', '7×24 在岗'],
        color='gr',
        industry='电商 · 教育 · 全行业',
        role_desc='通用客服解决不了的疑难场景，AI 客服顶上',
        pain_paragraphs=[
            '通用 AI 客服对常见问题（"怎么退款？""快递到哪了？"）回答 OK。但客户的真实问题很多是边缘场景：商品破损但快递员说不接受退货、双 11 优惠和会员折扣冲突、跨境订单关税计算——通用客服直接卡壳。',
            'AI 客服基于 5 年 BadCase 标注数据训练，处理这些边缘场景比通用方案强。再难的问题先自动试一遍，真搞不定再转人工。八成以上的工单，在 AI 这层就解决了。',
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
            ('💬', '多轮对话', '不是一问一答的机器人，能跟客户连续聊 5-10 轮，一次把问题解决。', 'gr'),
            ('🔍', '工单分类', '客户问题自动打标分类，统计高频问题反向优化业务流程。', 'bl'),
            ('🎯', '情绪识别', '识别客户情绪（愤怒、焦虑、满意），决定是否提前转人工。', 'or'),
            ('📞', '人机协作', '转人工时，把对话上下文和 AI 试过的方案一起给客服，客户不用再说一遍。', 'pu'),
            ('🌍', '多语言', '中英双语 + 海外业务多语言支持，全球客户一套客服。', 'te'),
            ('📚', 'BadCase 积累', '每次失败都记录、标注、拿去训练，同样的问题不会再错。', 'gr'),
        ], cols=3),
        kpi_items=[
            ('89%', '对话自动完成率'),
            ('5 年', 'BadCase 标注积累'),
            ('80%+', '工单 AI 兜住'),
            ('15s', '平均响应时间'),
        ],
        cta_text='让 AI 客服接管你的工单 80%',
    )

    # ────── AI 社工 / 调解员 ──────
    pages['government'] = page_workforce(
        slug='government',
        title='AI 社工 / 调解员',
        kicker='AI 劳动力 · 政务岗',
        h1='AI 社工 / 调解员 · <span class="accent">在政务高合规下跑得通的 AI</span>',
        lede='AI 普法调解员、AI 社工已在 <strong>北京海淀区东升镇</strong>率先落地——AI 社工 7×24 响应，累计服务居民约 50 万人次；AI 普法调解员参与调解近百起，成功率约 93%，拿了海淀区首届法治实践优秀案例。每一句话怎么来的都有日志，可以倒查。政务和金融客户最在意这一条。',
        pills=['海淀东升镇率先落地', '高合规 + 全程可审计', '居民服务约 50 万人次', '调解成功率约 93%'],
        color='pu',
        industry='政务 · 司法 · 公共服务',
        role_desc='政务场景对 AI 的要求最高：合规、可审计、说错一句都不行',
        pain_paragraphs=[
            '政务 AI 不能像电商客服那样"先上线再迭代"，一次说错就是舆情。但社区调解员忙不过来，12345 热线打爆，12348 普法咨询排队，人手永远不够。',
            'AI 社工 / 调解员把人工干不过来的活先接住：基础咨询答得了，矛盾分类做得对，热点问题自动同步给真人。每一句话都有人审过，每一次决策都能倒查。',
        ],
        pain_bullets=[
            '普法咨询：依据法规库答疑、不跑偏 + 不创造',
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
            ('📜', '法规库引用', '所有法律咨询基于官方法规库，引用条款可追溯，不是大模型胡编。', 'pu'),
            ('🎯', '矛盾分类', '邻里纠纷、消费维权、劳动争议——按场景分类走对应调解流程。', 'bl'),
            ('🤝', '情绪安抚', '识别投诉者情绪，先共情再处理，别火上浇油。', 'gr'),
            ('📋', '工单流转', '超出 AI 能力的问题自动登记工单，转给真人调解员跟进。', 'or'),
            ('🔒', '全程可审计', '每一次决策、每一次引用都有日志，合规审查要的就是这个。', 'te'),
            ('🌐', '多端接入', '12345 热线、政务 App、公众号、社区企微——一套 Agent 多端服务。', 'pu'),
        ], cols=3),
        kpi_items=[
            ('约 50 万', 'AI 社工累计服务居民（人次）'),
            ('↓ 约 45%', '居民投诉率'),
            ('↑ 约 85%', '居民满意度'),
            ('约 93%', 'AI 调解员调解成功率'),
        ],
        cta_text='把 AI 社工 / 调解员部署到你的政务系统',
    )

    # ────── AI 顾问 / 营销 (金融) ──────
    pages['finance'] = page_workforce(
        slug='finance',
        title='AI 顾问 / 营销',
        kicker='AI 劳动力 · 金融岗',
        h1='AI 顾问 / 营销 · <span class="accent">在金融合规边界内跑得稳</span>',
        lede='银行、证券、保险多个头部机构落地——<strong>可设的合规边界 + 9 年风控话术库</strong>，金融客户敢用。',
        pills=['多家头部金融机构', '9 年风控话术库', '可设的合规边界', 'KYC / 反洗钱集成'],
        color='te',
        industry='银行 · 证券 · 保险',
        role_desc='金融行业对 AI 最严苛，一句越界都可能踩监管红线',
        pain_paragraphs=[
            '银行客户经理一人服务 500 个客户已经超负荷，可每个客户对理财、保险、信贷的咨询都不能怠慢。AI 顾问接住基础咨询和合规材料解读，人工只管高价值客户。',
            '难点是合规：不能给投资建议、不能保证收益、不能误导销售。AI 顾问的话术由风控团队预设硬边界，每一句都过审。9 年金融场景攒下来的话术库，通用 Agent 平台短期补不上。',
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
<div style="font-size:13px;color:var(--teal);font-weight:700;margin-bottom:12px;">AI 顾问 · 合规边界</div>
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
            ('🛡️', '可设的合规边界', '风控团队设定的边界 AI 跨不出去，每一句都过预设规则审查。', 'te'),
            ('💼', '产品矩阵覆盖', '理财、保险、基金、信贷、信用卡——所有产品条款随时调取。', 'bl'),
            ('📊', '客户画像匹配', '按风险偏好、资产规模、年龄层级推荐合规产品。', 'or'),
            ('🔒', 'KYC 集成', '客户身份核实、风险等级评估、反洗钱筛查自动化。', 'gr'),
            ('🎯', '机会识别', '从对话中识别理财升级、保险增配等机会，转给真人顾问跟进。', 'pu'),
            ('📋', '全程可审计', '每一次决策可溯源，合规审查、银保监检查直接调取。', 'te'),
        ], cols=3),
        kpi_items=[
            ('多家', '头部金融机构落地'),
            ('9 年', '风控话术库积累'),
            ('100%', '合规可审计'),
            ('5×', '客户经理人均承接'),
        ],
        cta_text='让 AI 顾问 / 营销在你的合规边界内上岗',
    )

    # ────── AI 解说员 / 主理人 ──────
    pages['livestream'] = page_workforce(
        slug='livestream',
        title='AI 解说员 / 主理人',
        kicker='AI 劳动力 · 直播岗',
        h1='AI 解说员 / 主理人 · <span class="accent">把直播间人手放大 10 倍</span>',
        lede='全媒体内容运营 + 直播间智能解说——<strong>内容生产 + 分发 + 现场解说一套人马干完</strong>，把直播间人手放大 10 倍。',
        pills=['10× 人手杠杆', '24 小时不下播', '多平台内容矩阵', '互动 + 选品 + 解说'],
        color='or',
        industry='直播电商 · 全媒体',
        role_desc='直播间忙不过来：主播说话、运营盯互动、客服回评论，一晚上累趴',
        pain_paragraphs=[
            '一场带货直播：主播讲产品、运营盯互动、客服回评论、选品师切链接、剪辑剪短视频——一个团队 5-8 人通宵都忙不完。流量大的时候评论刷屏，互动跟不上，单子就漏了。',
            'AI 解说员 / 主理人把这条流水线压缩到 1-2 个真人 + 一套 Agent：AI 24 小时不下播解说、自动回评论、按节奏切链接、自动剪短视频分发到全媒体——把直播间人手放大 10 倍。',
        ],
        pain_bullets=[
            '24×7 直播解说：AI 主理人不下播，半夜流量也接得住',
            '评论互动：直播间评论刷得再快也能回过来',
            '选品节奏：按观众活跃度、库存、利润动态切链接',
            '内容剪辑：直播切片自动生成，分发到抖音 / 小红书 / 视频号',
            '主播协同：和真人主播配合接力，节奏不掉',
        ],
        pain_visual="""
<div style="background:#fff;border-radius:12px;padding:18px;border:1px solid var(--gray-line);">
<div style="font-size:13px;color:var(--orange);font-weight:700;margin-bottom:12px;">AI 主理人 · 直播间实时</div>
<div style="display:flex;flex-direction:column;gap:8px;">
<div style="display:flex;justify-content:space-between;font-size:13px;align-items:center;"><span>当前观看</span><span style="color:var(--orange);font-weight:800;font-size:18px;">12,847</span></div>
<div style="display:flex;justify-content:space-between;font-size:13px;align-items:center;"><span>评论 / 分钟</span><span style="color:var(--blue);font-weight:800;font-size:18px;">328</span></div>
<div style="display:flex;justify-content:space-between;font-size:13px;align-items:center;"><span>本场成交</span><span style="color:var(--green);font-weight:800;font-size:18px;">¥185,420</span></div>
<div style="display:flex;justify-content:space-between;font-size:13px;align-items:center;"><span>已切短视频</span><span style="color:var(--purple);font-weight:800;font-size:18px;">14 条</span></div>
<div style="border-top:1px solid var(--gray-line);padding-top:12px;margin-top:6px;display:flex;flex-direction:column;gap:4px;font-size:11.5px;">
<div style="color:var(--green);font-weight:600;">✓ 实时互动 · 28 条评论已回</div>
<div style="color:var(--green);font-weight:600;">✓ 链接 #4 切上 · 库存 3,200 件</div>
<div style="color:var(--gray-text);">… AI 主理人在岗中</div>
</div>
</div>
</div>
""",
        capability_block=feat_grid([
            ('🎙️', '直播解说', '基于产品库 + 话术库实时解说，节奏紧凑不冷场。', 'or'),
            ('💬', '评论互动', '观众评论实时识别 + 自动回复 + 关键问题升级真人。', 'bl'),
            ('🛒', '智能选品', '按活跃度、利润、库存调整链接节奏，单子多接一点。', 'gr'),
            ('🎬', '内容矩阵', '直播切片自动生成短视频，分发到抖音 / 小红书 / 视频号。', 'pu'),
            ('🎯', '观众分层', '高意向观众单独标记，私信发优惠，把人引到下单。', 'te'),
            ('🤝', '人机接力', '真人主播下播，AI 主理人接着播，直播间 24 小时不熄火。', 'or'),
        ], cols=3),
        kpi_items=[
            ('10×', '人手杠杆放大'),
            ('24×7', '直播间不下播'),
            ('328', '评论 / 分钟（峰值）'),
            ('14+', '日均短视频产出'),
        ],
        cta_text='让 AI 主理人 24 小时给你播货',
    )

    return pages


def page_enterprise():
    body = ''
    body += block(        "和 Anthropic 一个判断",
        "企业上线 AI，最先问的不是「能多聪明」，是「能不能放心交给它」",
        "TO B 要的是输出稳定、行为可审计、企业级可控。这也是 Anthropic 在 2026 年走的路，更是我们 9 年的判断。",
        '<div style="background:var(--blue-light);border-left:4px solid var(--blue);border-radius:0 14px 14px 0;padding:24px 32px;max-width:920px;margin:0 auto;display:flex;gap:18px;align-items:center;"><div style="font-size:42px;font-weight:900;color:var(--blue);line-height:1;">&ldquo;</div><div style="font-size:17px;color:var(--black);font-weight:600;line-height:1.55;">客户问得最多的，不是「哪个模型最强」，是「哪个能放心装进我的系统」。<small style="display:block;font-size:13.5px;color:var(--gray-text);font-weight:500;margin-top:6px;">—— 过去一年，几乎每个客户都这么问</small></div></div>',
    )

    deep_items = [
        # (color, num, en, zh, pain, ours, visual_html)
        ('bl', '01', 'Predictability', '输出可重复',
         '消费场景偶尔答错没事，企业场景不行。生成财务摘要、起草法律文书，同一个问题问三次给出三个答案，业务跑不下去。',
         '9 年带结果标注的部署数据让 Agent 行为可标定、可回归。<strong>同一个 query 给一致的回答，不是每次掷骰子</strong>。Anthropic 靠模型对齐，我们靠行业结果数据。',
         '<div style="font-size:11px;color:var(--gray-text);font-weight:700;letter-spacing:.04em;margin-bottom:8px;">同一个 query × 3</div>'
         '<div style="background:#fff;padding:9px 12px;border-radius:6px;border:1px solid var(--gray-line);font-size:12.5px;color:var(--blue);">→ 您的退款政策是 7 天无理由</div>'
         '<div style="background:#fff;padding:9px 12px;border-radius:6px;border:1px solid var(--gray-line);font-size:12.5px;color:var(--blue);">→ 您的退款政策是 7 天无理由</div>'
         '<div style="background:#fff;padding:9px 12px;border-radius:6px;border:1px solid var(--gray-line);font-size:12.5px;color:var(--blue);">→ 您的退款政策是 7 天无理由</div>'
         '<div style="font-size:11px;color:var(--green);font-weight:800;text-align:right;margin-top:4px;">✓ 一致</div>'),

        ('or', '02', 'Data Security & Privacy', '数据隔离',
         '内部文档、客户信息、专有数据，怕被模型吃掉再吐给别人。企业 AI 落地，最先卡在这。',
         '<strong>支持私有化 / 一体机部署，客户数据不出域</strong>。多租户严格隔离 + TLS 1.3 传输 + AES-256 存储 + 数据脱敏。客户数据不用于模型训练（合同里写明）。',
         '<div style="font-size:11px;color:var(--gray-text);font-weight:700;letter-spacing:.04em;margin-bottom:8px;">数据流向</div>'
         '<div style="display:flex;align-items:center;gap:6px;font-size:12px;"><span style="background:#fff;padding:6px 10px;border-radius:6px;border:1px solid var(--gray-line);">企业内部</span><span>→</span><span style="background:var(--orange-lt);color:var(--orange);padding:6px 10px;border-radius:6px;font-weight:700;">私有化 Agent</span></div>'
         '<div style="display:flex;align-items:center;gap:6px;font-size:12px;margin-top:8px;"><span style="background:#fff;padding:6px 10px;border-radius:6px;border:1px solid var(--gray-line);">企业内部</span><span>↛</span><span style="background:#fee;color:#c00;padding:6px 10px;border-radius:6px;text-decoration:line-through;">公网模型</span></div>'
         '<div style="font-size:11px;color:var(--green);font-weight:800;margin-top:4px;">✓ 数据不出域</div>'),

        ('gr', '03', 'Governance & Control', '行为可管控',
         '要 AI 按公司政策回答：能说什么、不能说什么、出了事谁负责，都得事先划好红线。光在 prompt 里写「请不要 xxx」顶不住。',
         'workflow 引擎里把<strong>能说什么、不能说什么</strong>提前写死，再配 5 个高合规行业策略库，不靠 prompt 软提示。金融的合规话术、政务的法规引用，AI 跨不出去。',
         '<div style="font-size:11px;color:var(--gray-text);font-weight:700;letter-spacing:.04em;margin-bottom:8px;">行为边界</div>'
         '<div style="background:#fff;padding:8px 11px;border-radius:6px;border:1px solid var(--gray-line);font-size:12px;display:flex;justify-content:space-between;"><span>解读产品条款</span><span style="color:var(--green);font-weight:800;">✓ 允许</span></div>'
         '<div style="background:#fff;padding:8px 11px;border-radius:6px;border:1px solid var(--gray-line);font-size:12px;display:flex;justify-content:space-between;"><span>引用合规话术库</span><span style="color:var(--green);font-weight:800;">✓ 允许</span></div>'
         '<div style="background:#fff;padding:8px 11px;border-radius:6px;border:1px solid var(--gray-line);font-size:12px;display:flex;justify-content:space-between;"><span>给具体投资建议</span><span style="color:#c00;font-weight:800;">✗ 拒答</span></div>'
         '<div style="background:#fff;padding:8px 11px;border-radius:6px;border:1px solid var(--gray-line);font-size:12px;display:flex;justify-content:space-between;"><span>承诺保本保收益</span><span style="color:#c00;font-weight:800;">✗ 拒答</span></div>'),

        ('pu', '04', 'Auditability & Transparency', '全程可审计',
         '银保监来检查、政务来巡检、客户起诉，AI 的每一次回答都得能回溯：用了哪个知识库、参考了什么 context、谁批准的版本上线。',
         '<strong>每一次 Agent 决策可追溯</strong>：调用的知识库、用的模型、参考的上下文、决策路径、版本号，全量日志记录。金融、政务客户特别在意这一条，过得了等保三级。',
         '<div style="font-size:11px;color:var(--gray-text);font-weight:700;letter-spacing:.04em;margin-bottom:8px;">Agent 决策日志</div>'
         '<div style="background:#fff;padding:9px 11px;border-radius:6px;border:1px solid var(--gray-line);font-size:11.5px;line-height:1.6;font-family:monospace;">[09:23:04] query → "退款 7 天"<br/>[09:23:04] kb_search → K3#FAQ#142<br/>[09:23:05] model → claude-3.5 v2.1<br/>[09:23:05] reply → "您可享 7 天无理由..."<br/>[09:23:05] log_id → AGT-2026050609234</div>'
         '<div style="font-size:11px;color:var(--purple);font-weight:800;margin-top:4px;">✓ 全量日志归档 7 年</div>'),

        ('te', '05', 'Integration', '对接现有系统',
         'AI 不能孤立运行，得接客户已有的 CRM、工单、知识库、订单系统。Agent 上岗第一天就要能查到客户的真实数据，不然就是摆设。',
         '<strong>9 年 IM 通道适配 + 企业 CRM / 工单 / 知识库直连</strong>。11 个 IM 通道，加主流企业系统的对接经验。Agent 上岗就接管真实业务流，不在角落空转。',
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
         '<div style="background:#fff;padding:6px 2px;border-radius:5px;border:1px solid var(--gray-line);">企微</div>'
         '<div style="background:#fff;padding:6px 2px;border-radius:5px;border:1px solid var(--gray-line);">抖</div>'
         '<div style="background:#fff;padding:6px 2px;border-radius:5px;border:1px solid var(--gray-line);">飞</div>'
         '<div style="background:#fff;padding:6px 2px;border-radius:5px;border:1px solid var(--gray-line);">+</div>'
         '</div>'),

        ('bl', '06', 'Scalability', '规模化',
         '很多公司的 AI 卡在试点阶段——demo 跑得动，扩到几千客户、几十种业务场景就崩。企业 AI 从第一天就得想清楚怎么跑得稳。',
         '<strong>1000+ 大型企业客户验证过的部署能力</strong>，在生产环境跑了多年，不是 demo。从单一场景到多职能 Agent 矩阵，从一个客户的私域到集团央企的多租户隔离，都跑得通。',
         '<div style="font-size:11px;color:var(--gray-text);font-weight:700;letter-spacing:.04em;margin-bottom:8px;">部署规模</div>'
         '<div style="display:flex;justify-content:space-between;align-items:baseline;border-bottom:1px solid var(--gray-line);padding:6px 0;font-size:12.5px;"><span>大型企业客户</span><span style="color:var(--blue);font-weight:800;font-size:16px;">1000+</span></div>'
         '<div style="display:flex;justify-content:space-between;align-items:baseline;border-bottom:1px solid var(--gray-line);padding:6px 0;font-size:12.5px;"><span>累计服务终端用户</span><span style="color:var(--blue);font-weight:800;font-size:16px;">4 亿 + 人次</span></div>'
         '<div style="display:flex;justify-content:space-between;align-items:baseline;border-bottom:1px solid var(--gray-line);padding:6px 0;font-size:12.5px;"><span>日均处理消息</span><span style="color:var(--blue);font-weight:800;font-size:16px;">200 万 +</span></div>'
         '<div style="display:flex;justify-content:space-between;align-items:baseline;padding:6px 0;font-size:12.5px;"><span>SaaS 服务可用性</span><span style="color:var(--green);font-weight:800;font-size:16px;">99.9%</span></div>'),

        ('or', '07', 'Multi-Model Flexibility', '不绑死单一模型',
         '企业不再赌单一供应商。这个月用 GPT，下个月可能切 Claude，年底说不定上 DeepSeek。模型涨价、出 bug、被监管，任何一个都可能让企业被动。',
         '<strong>模型层抽象</strong>：DeepSeek、Claude、Qwen、文心一言、GPT 都可切换。客户按场景选模型，按价格、性能随时换。',
         '<div style="font-size:11px;color:var(--gray-text);font-weight:700;letter-spacing:.04em;margin-bottom:8px;">模型矩阵</div>'
         '<div style="display:grid;grid-template-columns:1fr 1fr;gap:6px;font-size:12px;font-weight:700;">'
         '<div style="background:#fff;padding:8px 11px;border-radius:6px;border:1px solid var(--gray-line);display:flex;justify-content:space-between;align-items:center;"><span>DeepSeek-V3</span><span style="color:var(--green);">●</span></div>'
         '<div style="background:#fff;padding:8px 11px;border-radius:6px;border:1px solid var(--gray-line);display:flex;justify-content:space-between;align-items:center;"><span>Claude 4.7</span><span style="color:var(--green);">●</span></div>'
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
        title="SaaS、私有化、混合、一体机——四种部署都支持",
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
        "1000+ 大型企业 9 年的部署积累，不是 demo。",
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
    {cta_band("把 AI 劳动力装进你的合规边界内")}
  </div>
</section>
""".strip()

    return page_layout(
        title="企业级能力 · 和 Anthropic 同判断 | 句子互动",
        description="句子互动企业级 AI 能力：输出稳定、行为可审计、企业级可控。7 个 TO B 必过的门槛 + SaaS / 私有化 / 混合 / 一体机部署 + 等保三级合规。",
        rel="",
        breadcrumbs=[("首页", "index.html"), ("企业级能力", None)],
        hero_kicker="生来就是企业级",
        hero_h1='企业上线 AI，最先问的不是<span class="accent">「能多聪明」</span>，是<span class="accent">「能不能放心交给它」</span>',
        hero_lede="TO B 要的是<strong>输出稳定、行为可审计、企业级可控</strong>。这也是 Anthropic 在 2026 年走的路。我们做企业客户也这么多年，结论一样。",
        pills=["和 Anthropic 同判断", "1000+ 企业验证", "SaaS / 私有化 / 混合 / 一体机", "100% 决策可审计"],
        body=body,
    )


# ────────────────────────── industries page ──────────────────────────

def page_industries():
    body = ''
    body += block(        "5 个行业",
        "9 年扎根这 5 个高合规高垂直行业",
        "我们没做广撒网的通用平台。每个行业里都攒了头部客户的做法和经验。",
        '',
    )

    industries_detail = [
        ('education', '在线教育', '📚', 'bl', '400+ 客户 · 头部 RPA 已覆盖',
         '在线教育是句子互动最早进入的行业。9 年下来覆盖了几乎所有头部公司，从大班课、小班课到 1 对 1，从招生、续费到 NPS。其中我们目前成单体量最大的客户，是一家<strong>在线教育头部品牌（兴趣技能赛道）</strong>，AI 把整条「低转高」链路跑通：人效翻倍、单线索成本砍 50~62%、转人工率从 27% 压到 2.73%。<a href="case-xingqudao.html" style="color:var(--blue);font-weight:700;">看完整案例 →</a>',
         [
             ('400+', '客户'),
             ('头部', 'RPA 已覆盖'),
             ('9 年', '行业积累'),
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
         '银行、证券、保险。金融对 AI 最严。合规边界能提前写死，加上 9 年风控话术库，所以金融客户敢用。',
         [
             ('多家', '头部机构'),
             ('9 年', '风控话术库'),
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
         '政务对 AI 要求最高。一句话越界就可能上舆情。我们的 AI 普法调解员、AI 社工已在多个城市试点。',
         [
             ('多个', '城市试点'),
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
         ['多个城市试点', '司法机构', '社区']),

        ('internet', '泛互联网', '🌐', 'te', '多家平台型公司部署',
         '电商平台、内容平台、生活服务平台，这些公司的客服、运营、销售都在用 AI 劳动力，接住越来越多的客户。',
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

    for slug, name, icon, color, tagline, intro, kpis, scene, capabilities, customers in industries_detail:
        kpi_html = ''.join(
            f'<div style="text-align:center;"><div style="font-size:24px;font-weight:800;color:var(--{color}-color, var(--blue));letter-spacing:-.01em;">{v}</div><div style="font-size:12px;color:var(--gray-text);margin-top:2px;">{l}</div></div>'
            for v, l in kpis
        )
        cap_html = ''.join(f'<li>{c}</li>' for c in capabilities)
        cust_html = ''.join(f'<span style="background:#fff;border:1px solid var(--gray-line);border-radius:6px;padding:5px 12px;font-size:12.5px;color:var(--gray-text);font-weight:600;">{c}</span>' for c in customers)
        # color tokens
        ccolor = {'bl': 'var(--blue)', 'or': 'var(--orange)', 'gr': 'var(--green)', 'pu': 'var(--purple)', 'te': 'var(--teal)'}[color]
        clt = {'bl': 'var(--blue-light)', 'or': 'var(--orange-lt)', 'gr': 'var(--green-lt)', 'pu': 'var(--purple-lt)', 'te': 'var(--teal-lt)'}[color]
        body += f"""
<section class="section-block" id="{slug}">
  <div class="container">
    <div style="display:grid;grid-template-columns:1fr 380px;gap:48px;">
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
        <div style="margin-top:24px;display:flex;flex-wrap:wrap;gap:8px;">
          {cust_html}
        </div>
      </div>
      <div>
        <div style="background:{clt};border-radius:18px;padding:32px 28px;">
          <div style="font-size:13px;font-weight:800;letter-spacing:.06em;color:{ccolor};text-transform:uppercase;margin-bottom:20px;">数据快览</div>
          <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:14px;">
            {''.join(f'<div><div style="font-size:22px;font-weight:800;color:{ccolor};letter-spacing:-.01em;line-height:1.1;">{v}</div><div style="font-size:11.5px;color:var(--gray-text);margin-top:3px;">{l}</div></div>' for v, l in kpis)}
          </div>
        </div>
      </div>
    </div>
  </div>
</section>""".strip()

    body += block(        "为什么我们能在这 5 个行业做得动",
        "你买回去能用，是因为这 5 个行业里的坑，我们已经一个个趟过",
        "找个通用平台你也能搭起来。但要跑通你这个行业的具体场景，得找已经踩过坑的人。",
        '''<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:22px;max-width:1100px;margin:0 auto;">
<div style="padding:28px 24px;background:#fff;border:1px solid var(--gray-line);border-radius:18px;">
  <div style="font-size:13px;font-weight:800;color:var(--orange);letter-spacing:.1em;margin-bottom:12px;">客户拿到什么</div>
  <h4 style="font-size:18px;font-weight:800;margin:0 0 12px;">你的行业话术和 SOP 我们已经有底子</h4>
  <p style="font-size:14px;color:var(--gray-text);line-height:1.7;margin:0;">在线教育的报名漏斗、电商的私域召回、金融的合规话术、政务的调解流程——你不用从 0 开始喂 AI，开通就能上岗。</p>
</div>
<div style="padding:28px 24px;background:#fff;border:1px solid var(--gray-line);border-radius:18px;">
  <div style="font-size:13px;font-weight:800;color:var(--blue);letter-spacing:.1em;margin-bottom:12px;">客户拿到什么</div>
  <h4 style="font-size:18px;font-weight:800;margin:0 0 12px;">同行的坑我们都帮你踩过</h4>
  <p style="font-size:14px;color:var(--gray-text);line-height:1.7;margin:0;">你这个行业里头部公司用了多年，什么场景容易出错、合规怎么绕、客户什么话不爱听，我们都见过，能帮你少走半年弯路。</p>
</div>
<div style="padding:28px 24px;background:#fff;border:1px solid var(--gray-line);border-radius:18px;">
  <div style="font-size:13px;font-weight:800;color:var(--green);letter-spacing:.1em;margin-bottom:12px;">客户拿到什么</div>
  <h4 style="font-size:18px;font-weight:800;margin:0 0 12px;">你的反馈直接进入产品</h4>
  <p style="font-size:14px;color:var(--gray-text);line-height:1.7;margin:0;">每个客户的真实业务结果都反馈回 Agent。你今天遇到的问题，下个版本就修好了。</p>
</div>
</div>''',
        alt=True,
    )

    body += f"""
<section class="section-block">
  <div class="container">
    {cta_band("把 AI 劳动力部署到你的行业")}
  </div>
</section>
""".strip()

    return page_layout(
        title="客户与行业 · 教育 / 电商 / 金融 / 政务 / 互联网 已部署 | 句子互动",
        description="句子互动 AI 劳动力已在在线教育、消费品电商、金融、政务·司法、泛互联网 5 个行业头部公司部署。如果你在这些行业，我们已经在这些行业跑了 9 年。",
        rel="",
        breadcrumbs=[("首页", "index.html"), ("客户与行业", None)],
        hero_kicker="WHO USES JUZIBOT",
        hero_h1='你的行业里，<span class="accent">已经有人在用了</span>。',
        hero_lede="如果你在<strong>在线教育、消费品电商、金融、政务、互联网</strong>这 5 个行业里，你的同行（甚至头部公司）已经在用句子互动的 AI 劳动力。这些坑我们陪他们一起踩过，你不用从 0 开始。",
        pills=["1000+ 大型企业客户", "5 个行业头部公司在用", "开通即可上岗", "同行已在用"],
        body=body,
    )


# ────────────────────────── about page ──────────────────────────

def page_about():
    body = ''
    body += block(
        "公司简介",
        "我们做的事，<span class=\"accent\">把 AI 装进企业的真实业务里跑</span>",
        "句子互动是企业级 Agentic AI 平台。把大模型和企业数据接进 IM 通道、抖音、钉钉、飞书、WhatsApp，为企业造能自主决策的 AI 劳动力。",
        '<div style="max-width:920px;margin:0 auto;background:linear-gradient(135deg,var(--blue-light),#fff);border-radius:22px;padding:48px;text-align:center;">'
        '<div style="font-size:18px;color:var(--blue);font-weight:700;letter-spacing:-.005em;margin-bottom:16px;">我们做的事</div>'
        '<div style="font-size:24px;font-weight:800;color:var(--black);line-height:1.55;letter-spacing:-.01em;">在 1000+ 家中国企业的 IM 通道、客服、销售、合规流程里跑——按业务结果计价。</div>'
        '<div style="margin-top:24px;display:flex;justify-content:center;gap:32px;flex-wrap:wrap;">'
        '<div><div style="font-size:32px;font-weight:800;color:var(--orange);letter-spacing:-.01em;line-height:1.1;">1000+</div><div style="font-size:13px;color:var(--gray-text);margin-top:4px;">大型企业客户</div></div>'
        '<div><div style="font-size:32px;font-weight:800;color:var(--blue);letter-spacing:-.01em;line-height:1.1;">4 亿</div><div style="font-size:13px;color:var(--gray-text);margin-top:4px;">累计服务终端用户（人次）</div></div>'
        '<div><div style="font-size:32px;font-weight:800;color:var(--green);letter-spacing:-.01em;line-height:1.1;">5 个</div><div style="font-size:13px;color:var(--gray-text);margin-top:4px;">高合规高垂直行业</div></div>'
        '<div><div style="font-size:32px;font-weight:800;color:var(--purple);letter-spacing:-.01em;line-height:1.1;">9 年</div><div style="font-size:13px;color:var(--gray-text);margin-top:4px;">行业 know-how 积累</div></div>'
        '<div><div style="font-size:32px;font-weight:800;color:var(--black);letter-spacing:-.01em;line-height:1.1;">22k+</div><div style="font-size:13px;color:var(--gray-text);margin-top:4px;">Wechaty GitHub Star</div></div>'
        '</div>'
        '</div>'
    )

    body += block(        "AI 原生团队",
        "大模型时代如何构建 AI Agent——<span class=\"accent\">《Chatbot 从 0 到 1》</span>",
        "由创始人 <strong>李佳芮</strong>（Wechaty 开源作者）带队。团队从 2017 年的 Wechaty 开源框架起步，到 2020 年出版中文首本聊天机器人专著《Chatbot 从 0 到 1》，到 2024 年第二版升级到大模型时代——9 年一直在做企业级 Agent。",
        '''<div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:24px;max-width:1100px;margin:0 auto;">
<div style="padding:28px 24px;background:#fff;border:1px solid var(--gray-line);border-radius:18px;">
  <div style="display:inline-block;font-size:11px;font-weight:800;letter-spacing:.1em;background:var(--blue-light);color:var(--blue);padding:4px 10px;border-radius:6px;margin-bottom:14px;">2020</div>
  <h4 style="font-size:18px;font-weight:800;margin:0 0 12px;">《Chatbot 从 0 到 1》第一版</h4>
  <p style="font-size:14px;color:var(--gray-text);line-height:1.7;margin:0;">中文首本聊天机器人专著。从 0 起步讲怎么做出能干活的对话机器人，把人机交互的根基讲清楚。</p>
</div>
<div style="padding:28px 24px;background:#fff;border:1px solid var(--gray-line);border-radius:18px;">
  <div style="display:inline-block;font-size:11px;font-weight:800;letter-spacing:.1em;background:var(--orange-lt);color:var(--orange);padding:4px 10px;border-radius:6px;margin-bottom:14px;">2024</div>
  <h4 style="font-size:18px;font-weight:800;margin:0 0 12px;">《Chatbot 从 0 到 1》第二版</h4>
  <p style="font-size:14px;color:var(--gray-text);line-height:1.7;margin:0;">大模型时代升级版。从 LLM Agent、工具调用、多 Agent 协作讲到实际部署——把 2020 那套对话机器人方法论升级到 AI 劳动力。</p>
</div>
<div style="padding:28px 24px;background:#fff;border:1px solid var(--gray-line);border-radius:18px;">
  <div style="display:inline-block;font-size:11px;font-weight:800;letter-spacing:.1em;background:var(--green-lt);color:var(--green);padding:4px 10px;border-radius:6px;margin-bottom:14px;">2017 至今</div>
  <h4 style="font-size:18px;font-weight:800;margin:0 0 12px;">Wechaty 开源框架</h4>
  <p style="font-size:14px;color:var(--gray-text);line-height:1.7;margin:0;">全球最大的 IM 自动化开源社区之一，22k+ GitHub Star。这层渠道身份，大模型公司很难复制。</p>
</div>
</div>''',
        alt=True,
    )

    body += block(        "时间线",
        "11 年穿越周期",
        "2018 资本寒冬、2020 疫情、2022 行业大调整、2024 LLM 大爆发，都活下来了。",
        '''<div style="position:relative;padding:48px 0 24px;max-width:1100px;margin:0 auto;">
<div style="position:absolute;left:0;right:0;top:50%;transform:translateY(-50%);height:2px;background:var(--gray-line);"></div>
<div style="display:grid;grid-template-columns:repeat(6,1fr);gap:0;position:relative;">
<div style="text-align:center;position:relative;"><div style="width:16px;height:16px;border-radius:50%;background:var(--orange);margin:0 auto 18px;border:3px solid #fff;box-shadow:0 0 0 2px var(--orange);"></div><div style="font-size:16px;font-weight:800;color:var(--blue);margin-bottom:4px;">2017</div><div style="font-size:12.5px;color:var(--gray-text);line-height:1.5;padding:0 8px;">Wechaty 开源框架发布</div></div>
<div style="text-align:center;position:relative;"><div style="width:16px;height:16px;border-radius:50%;background:var(--orange);margin:0 auto 18px;border:3px solid #fff;box-shadow:0 0 0 2px var(--orange);"></div><div style="font-size:16px;font-weight:800;color:var(--blue);margin-bottom:4px;">2019</div><div style="font-size:12.5px;color:var(--gray-text);line-height:1.5;padding:0 8px;">句子互动成立</div></div>
<div style="text-align:center;position:relative;"><div style="width:16px;height:16px;border-radius:50%;background:var(--orange);margin:0 auto 18px;border:3px solid #fff;box-shadow:0 0 0 2px var(--orange);"></div><div style="font-size:16px;font-weight:800;color:var(--blue);margin-bottom:4px;">2020</div><div style="font-size:12.5px;color:var(--gray-text);line-height:1.5;padding:0 8px;">《Chatbot 从 0 到 1》出版</div></div>
<div style="text-align:center;position:relative;"><div style="width:16px;height:16px;border-radius:50%;background:var(--orange);margin:0 auto 18px;border:3px solid #fff;box-shadow:0 0 0 2px var(--orange);"></div><div style="font-size:16px;font-weight:800;color:var(--blue);margin-bottom:4px;">2023</div><div style="font-size:12.5px;color:var(--gray-text);line-height:1.5;padding:0 8px;">Azure OpenAI 中国首发服务商<br/>WAIC 2023 参展</div></div>
<div style="text-align:center;position:relative;"><div style="width:16px;height:16px;border-radius:50%;background:var(--orange);margin:0 auto 18px;border:3px solid #fff;box-shadow:0 0 0 2px var(--orange);"></div><div style="font-size:16px;font-weight:800;color:var(--blue);margin-bottom:4px;">2024</div><div style="font-size:12.5px;color:var(--gray-text);line-height:1.5;padding:0 8px;">《Chatbot 从 0 到 1》第二版<br/>Agent 流水线成型</div></div>
<div style="text-align:center;position:relative;"><div style="width:16px;height:16px;border-radius:50%;background:var(--orange);margin:0 auto 18px;border:3px solid #fff;box-shadow:0 0 0 2px var(--orange);"></div><div style="font-size:16px;font-weight:800;color:var(--blue);margin-bottom:4px;">2026</div><div style="font-size:12.5px;color:var(--gray-text);line-height:1.5;padding:0 8px;">AI 劳动力规模化部署</div></div>
</div>
</div>''',
    )

    body += block(        "客户矩阵",
        "各行业顶尖商业组织都选择句子互动构建 AI 劳动力",
        "不是一两个标杆——是每个行业都有头部客户。",
        '''<div style="max-width:1100px;margin:0 auto;display:flex;flex-direction:column;gap:18px;">
<div style="display:grid;grid-template-columns:140px 1fr;gap:18px;align-items:center;background:var(--blue-light);border-radius:14px;padding:20px 24px;">
<div style="font-size:15px;font-weight:800;color:var(--blue);">在线教育</div>
<div style="display:flex;flex-wrap:wrap;gap:10px;">
<span style="background:#fff;padding:7px 14px;border-radius:8px;font-size:13px;font-weight:600;color:var(--gray-text);">头部大班课</span>
<span style="background:#fff;padding:7px 14px;border-radius:8px;font-size:13px;font-weight:600;color:var(--gray-text);">头部小班课</span>
<span style="background:#fff;padding:7px 14px;border-radius:8px;font-size:13px;font-weight:600;color:var(--gray-text);">兴趣技能头部</span>
<span style="background:#fff;padding:7px 14px;border-radius:8px;font-size:13px;font-weight:600;color:var(--gray-text);">头部 1 对 1</span>
<span style="background:#fff;padding:7px 14px;border-radius:8px;font-size:13px;font-weight:600;color:var(--gray-text);">财经职教头部</span>
<span style="background:#fff;padding:7px 14px;border-radius:8px;font-size:13px;font-weight:600;color:var(--gray-text);">众多头部</span>
</div>
</div>
<div style="display:grid;grid-template-columns:140px 1fr;gap:18px;align-items:center;background:var(--orange-lt);border-radius:14px;padding:20px 24px;">
<div style="font-size:15px;font-weight:800;color:var(--orange);">消费品牌</div>
<div style="display:flex;flex-wrap:wrap;gap:10px;">
<span style="background:#fff;padding:7px 14px;border-radius:8px;font-size:13px;font-weight:600;color:var(--gray-text);">国际美妆头部</span>
<span style="background:#fff;padding:7px 14px;border-radius:8px;font-size:13px;font-weight:600;color:var(--gray-text);">国际护肤头部</span>
<span style="background:#fff;padding:7px 14px;border-radius:8px;font-size:13px;font-weight:600;color:var(--gray-text);">母婴头部</span>
<span style="background:#fff;padding:7px 14px;border-radius:8px;font-size:13px;font-weight:600;color:var(--gray-text);">功能食品头部</span>
<span style="background:#fff;padding:7px 14px;border-radius:8px;font-size:13px;font-weight:600;color:var(--gray-text);">家电头部</span>
<span style="background:#fff;padding:7px 14px;border-radius:8px;font-size:13px;font-weight:600;color:var(--gray-text);">日化头部</span>
<span style="background:#fff;padding:7px 14px;border-radius:8px;font-size:13px;font-weight:600;color:var(--gray-text);">白电头部</span>
</div>
</div>
<div style="display:grid;grid-template-columns:140px 1fr;gap:18px;align-items:center;background:var(--green-lt);border-radius:14px;padding:20px 24px;">
<div style="font-size:15px;font-weight:800;color:var(--green);">政务金融</div>
<div style="display:flex;flex-wrap:wrap;gap:10px;">
<span style="background:#fff;padding:7px 14px;border-radius:8px;font-size:13px;font-weight:600;color:var(--gray-text);">多家头部银行</span>
<span style="background:#fff;padding:7px 14px;border-radius:8px;font-size:13px;font-weight:600;color:var(--gray-text);">证券机构</span>
<span style="background:#fff;padding:7px 14px;border-radius:8px;font-size:13px;font-weight:600;color:var(--gray-text);">保险机构</span>
<span style="background:#fff;padding:7px 14px;border-radius:8px;font-size:13px;font-weight:600;color:var(--gray-text);">消费金融</span>
<span style="background:#fff;padding:7px 14px;border-radius:8px;font-size:13px;font-weight:600;color:var(--gray-text);">城市政务试点</span>
</div>
</div>
<div style="display:grid;grid-template-columns:140px 1fr;gap:18px;align-items:center;background:var(--purple-lt);border-radius:14px;padding:20px 24px;">
<div style="font-size:15px;font-weight:800;color:var(--purple);">泛互联网</div>
<div style="display:flex;flex-wrap:wrap;gap:10px;">
<span style="background:#fff;padding:7px 14px;border-radius:8px;font-size:13px;font-weight:600;color:var(--gray-text);">头部搜索平台</span>
<span style="background:#fff;padding:7px 14px;border-radius:8px;font-size:13px;font-weight:600;color:var(--gray-text);">头部电商平台</span>
<span style="background:#fff;padding:7px 14px;border-radius:8px;font-size:13px;font-weight:600;color:var(--gray-text);">头部短视频平台</span>
<span style="background:#fff;padding:7px 14px;border-radius:8px;font-size:13px;font-weight:600;color:var(--gray-text);">头部分类信息</span>
<span style="background:#fff;padding:7px 14px;border-radius:8px;font-size:13px;font-weight:600;color:var(--gray-text);">头部资讯平台</span>
<span style="background:#fff;padding:7px 14px;border-radius:8px;font-size:13px;font-weight:600;color:var(--gray-text);">众多平台</span>
</div>
</div>
</div>''',
        alt=True,
    )

    body += block(        "资质与荣誉",
        "国家级资质、行业标准、赛事冠军，<span class=\"accent\">一摞证书摆在这</span>",
        "国家高新技术企业、北京市专精特新「小巨人」、公安部等保三级，做 TO B 客户在意的硬资质都过了。",
        '''<div style="max-width:1100px;margin:0 auto;display:flex;flex-direction:column;gap:18px;">
<div style="display:grid;grid-template-columns:140px 1fr;gap:18px;align-items:center;background:var(--blue-light);border-radius:14px;padding:20px 24px;">
<div style="font-size:15px;font-weight:800;color:var(--blue);">国家级资质</div>
<div style="display:flex;flex-wrap:wrap;gap:10px;">
<span style="background:#fff;padding:7px 14px;border-radius:8px;font-size:13px;font-weight:600;color:var(--gray-text);">国家高新技术企业</span>
<span style="background:#fff;padding:7px 14px;border-radius:8px;font-size:13px;font-weight:600;color:var(--gray-text);">北京市专精特新「小巨人」</span>
<span style="background:#fff;padding:7px 14px;border-radius:8px;font-size:13px;font-weight:600;color:var(--gray-text);">公安部等保三级认证</span>
</div>
</div>
<div style="display:grid;grid-template-columns:140px 1fr;gap:18px;align-items:center;background:var(--green-lt);border-radius:14px;padding:20px 24px;">
<div style="font-size:15px;font-weight:800;color:var(--green);">行业标准 / 计划</div>
<div style="display:flex;flex-wrap:wrap;gap:10px;">
<span style="background:#fff;padding:7px 14px;border-radius:8px;font-size:13px;font-weight:600;color:var(--gray-text);">中国互联网协会 · 智能体创新推进计划合作伙伴（2025—2027）</span>
<span style="background:#fff;padding:7px 14px;border-radius:8px;font-size:13px;font-weight:600;color:var(--gray-text);">工信部年度数字营销服务领航企业</span>
<span style="background:#fff;padding:7px 14px;border-radius:8px;font-size:13px;font-weight:600;color:var(--gray-text);">参与信通院「智能营销」系列标准制定</span>
</div>
</div>
<div style="display:grid;grid-template-columns:140px 1fr;gap:18px;align-items:center;background:var(--orange-lt);border-radius:14px;padding:20px 24px;">
<div style="font-size:15px;font-weight:800;color:var(--orange);">赛事荣誉</div>
<div style="display:flex;flex-wrap:wrap;gap:10px;">
<span style="background:#fff;padding:7px 14px;border-radius:8px;font-size:13px;font-weight:600;color:var(--gray-text);">WAIC 世界人工智能大会 · 全球创新项目路演冠军暨最佳应用奖</span>
<span style="background:#fff;padding:7px 14px;border-radius:8px;font-size:13px;font-weight:600;color:var(--gray-text);">MWC 上海 · 5G 消息创新价值奖</span>
</div>
</div>
<div style="display:grid;grid-template-columns:140px 1fr;gap:18px;align-items:center;background:var(--purple-lt);border-radius:14px;padding:20px 24px;">
<div style="font-size:15px;font-weight:800;color:var(--purple);">权威榜单</div>
<div style="display:flex;flex-wrap:wrap;gap:10px;">
<span style="background:#fff;padding:7px 14px;border-radius:8px;font-size:13px;font-weight:600;color:var(--gray-text);">2025 CHINA AI 100</span>
<span style="background:#fff;padding:7px 14px;border-radius:8px;font-size:13px;font-weight:600;color:var(--gray-text);">高科技高成长新锐企业 TOP50</span>
<span style="background:#fff;padding:7px 14px;border-radius:8px;font-size:13px;font-weight:600;color:var(--gray-text);">Plug and Play × 清华大学全球开放式创新百强</span>
</div>
</div>
</div>''',
    )

    body += block(        "媒体与生态",
        "新闻报道与生态合作",
        "",
        '''<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:22px;max-width:1100px;margin:0 auto;">
<div style="padding:28px 24px;background:#fff;border:1px solid var(--gray-line);border-radius:18px;">
  <div style="font-size:11.5px;font-weight:800;letter-spacing:.1em;color:var(--orange);margin-bottom:12px;">PARTNER · 2023</div>
  <h4 style="font-size:17px;font-weight:800;margin:0 0 12px;">Azure OpenAI 中国首发服务商</h4>
  <p style="font-size:13.5px;color:var(--gray-text);line-height:1.65;margin:0;">作为微软 Azure OpenAI 服务在中国的首批合作服务商之一，把 Azure OpenAI 的模型能力接进中国企业的私域业务。</p>
</div>
<div style="padding:28px 24px;background:#fff;border:1px solid var(--gray-line);border-radius:18px;">
  <div style="font-size:11.5px;font-weight:800;letter-spacing:.1em;color:var(--blue);margin-bottom:12px;">EVENT · 2023</div>
  <h4 style="font-size:17px;font-weight:800;margin:0 0 12px;">WAIC 2023 参展</h4>
  <p style="font-size:13.5px;color:var(--gray-text);line-height:1.65;margin:0;">在世界人工智能大会展出 AI 员工矩阵，把 9 年 IM 自动化积累和现在的 AI 劳动力路径一起摆出来。</p>
</div>
<div style="padding:28px 24px;background:#fff;border:1px solid var(--gray-line);border-radius:18px;">
  <div style="font-size:11.5px;font-weight:800;letter-spacing:.1em;color:var(--green);margin-bottom:12px;">OPEN SOURCE</div>
  <h4 style="font-size:17px;font-weight:800;margin:0 0 12px;">Wechaty 22k+ GitHub Star</h4>
  <p style="font-size:13.5px;color:var(--gray-text);line-height:1.65;margin:0;">全球最大的 IM 自动化开源社区之一，开发者一起建起来的。这层渠道身份，是攒了 9 年才有的。</p>
</div>
</div>''',
    )

    body += f"""
<section class="section-block">
  <div class="container">
    {cta_band("聊聊你想部署的 AI 劳动力")}
  </div>
</section>
""".strip()

    return page_layout(
        title="关于我们 · 关于句子互动 · 一支把 AI 装进企业的团队",
        description="句子互动是企业级 Agentic AI 平台，由 Wechaty 开源作者李佳芮创立。9 年积累，1000+ 大型企业客户、累计服务终端用户约 4 亿人次。国家高新技术企业、北京市专精特新「小巨人」、公安部等保三级，WAIC 全球创新冠军、2025 CHINA AI 100。",
        rel="",
        breadcrumbs=[("首页", "index.html"), ("关于我们", None)],
        hero_kicker="关于句子互动",
        hero_h1='一支<span class="accent">把 AI 装进 1000+ 家企业</span>的团队',
        hero_lede="句子互动是企业级 Agentic AI 平台，<strong>2019 年由 Wechaty 开源作者李佳芮创立</strong>。把大模型 + 企业全域数据接进 IM 通道、抖音、钉钉、飞书、WhatsApp——为企业造能自主决策的 AI 劳动力。团队做对话式 AI 这些年，已服务 1000+ 大型企业客户。",
        pills=["1000+ 大型企业客户", "累计服务 4 亿人次", "国家高新 · 专精特新", "Wechaty 22k+ Star"],
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
  <p style="font-size:13px;color:var(--gray-text);line-height:1.6;margin:0;">早上一句「看看这家是不是竞争对手」，Claude Code 自己查、自己写、自己发到飞书群。错了就把教训存进 skill，下次自动对。</p>
</div>
<div style="background:#fff;border:1px solid var(--gray-line);border-radius:14px;padding:22px;">
  <div style="font-size:12px;font-weight:800;color:var(--green);letter-spacing:.06em;margin-bottom:8px;">技术</div>
  <div style="font-size:15px;font-weight:800;margin-bottom:8px;">AI 自己测 AI、压测自己的系统</div>
  <p style="font-size:13px;color:var(--gray-text);line-height:1.6;margin:0;">测试 Agent、流量回放压测系统，都是团队用 AI 搭出来的，连提示词改动都能跑回归。</p>
</div>
<div style="background:#fff;border:1px solid var(--gray-line);border-radius:14px;padding:22px;">
  <div style="font-size:12px;font-weight:800;color:var(--orange);letter-spacing:.06em;margin-bottom:8px;">销售</div>
  <div style="font-size:15px;font-weight:800;margin-bottom:8px;">一个销售，月接 200 → 913 人</div>
  <p style="font-size:13px;color:var(--gray-text);line-height:1.6;margin:0;">在线教育头部客户的先锋组，一个销售月接从 200 涨到 913 人，是大盘的好几倍，我们自己先跑通的。</p>
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
<p style="text-align:center;font-size:14.5px;color:var(--gray-text);margin:32px auto 0;max-width:700px;line-height:1.7;">90 后 AI native 配 9 年 toB 老兵，<strong style="color:var(--black);">这个组合全市场几乎没有</strong>。我们自己先活成 AI 原生组织，再带客户一起跑。</p>''',
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
    <div style="font-size:14px;font-weight:800;color:var(--black);background:var(--orange-lt);padding:10px 14px;border-radius:8px;">两次对内，两次对外——一个项目最多再拿四次。</div>
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
        title='只要我还在动脑，<span style="color:var(--blue);">它就一直在动手</span>',
        paragraphs=[
            '过去能写代码的人是 0.1%，Agent 把这个数字推到 1-3%，翻了几十倍。配环境、查命令、看报错，以前挡在我和代码之间的那堆破事，Agent 全吃掉了。',
            '我每天最稳定的工作方式：脑子里想，顺手写出来，让 Claude 干，我 review。审得没他写得快，所以他从来不闲着。<strong>瓶颈只剩"我想清楚要什么"。</strong>',
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
            '<strong>X 可以是任何用脑子干的活</strong>：分析客户数据、改 deck、拆 SOP、写文章、调流程。代码只是凑巧最早跑通的那个场景。被打开的不是「写代码」这一件事，是「用脑子干活」整个面。',
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
  <p style="font-size:13px;color:var(--gray-text);line-height:1.65;margin:0;">同样的方案 100 个版本里挑一个，AI 给不了你品味，你得自己有。</p>
</div>
<div style="padding:24px 18px;background:#fff;border:1px solid var(--gray-line);border-radius:14px;">
  <div style="font-size:28px;margin-bottom:10px;">👁️</div>
  <h4 style="font-size:16px;font-weight:800;margin:0 0 8px;color:var(--green);">在场</h4>
  <p style="font-size:13px;color:var(--gray-text);line-height:1.65;margin:0;">客户当面那一刻、团队卡住那一刻，AI 不在场。</p>
</div>
<div style="padding:24px 18px;background:#fff;border:1px solid var(--gray-line);border-radius:14px;">
  <div style="font-size:28px;margin-bottom:10px;">🤝</div>
  <h4 style="font-size:16px;font-weight:800;margin:0 0 8px;color:var(--purple);">关系</h4>
  <p style="font-size:13px;color:var(--gray-text);line-height:1.65;margin:0;">十年的合作伙伴、信任你的客户、敢一起冒险的团队——这是人之间的事。</p>
</div>
<div style="padding:24px 18px;background:#fff;border:1px solid var(--gray-line);border-radius:14px;">
  <div style="font-size:28px;margin-bottom:10px;">⚒️</div>
  <h4 style="font-size:16px;font-weight:800;margin:0 0 8px;color:var(--teal);">手艺</h4>
  <p style="font-size:13px;color:var(--gray-text);line-height:1.65;margin:0;">不是把活做完，是把活做美。一行代码、一段话术、一个细节，这就是手艺。</p>
</div>
</div>
<p style="text-align:center;font-size:14.5px;color:var(--gray-text);margin:36px auto 0;max-width:680px;line-height:1.7;">把另外 80% 交给 AI——但<strong style="color:var(--black);">这 5 件事，是你和 AI 的分界线</strong>。守住这条线，AI 才是帮你放大，而不是抹平你。</p>''',
        alt=True,
    )

    body += block(        "文章",
        "李佳芮的洞察",
        "句子互动创始人 · 写在 rui.juzi.bot 上",
        '''<div style="display:grid;grid-template-columns:repeat(2,1fr);gap:22px;max-width:1100px;margin:0 auto;">
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
        description="句子互动是一家 AI 原生组织——不是'在用 AI 的公司'，是 AI 已经下沉到每个部门、每个人手上。从 CEO 到财务每天真用 Agent 干活。90 后 AI native × 9 年 toB 老兵的组合，全市场几乎没有。这条路我们自己先活成，再带客户一起跑。",
        rel="",
        breadcrumbs=[("首页", "index.html"), ("AI 原生组织", None)],
        hero_kicker="AI 原生组织 · 我们自己怎么活",
        hero_h1='不是「在用 AI 的公司」，<span class="accent">是 AI 下沉到每个人的组织</span>',
        hero_lede="真正活成 AI 原生的组织，市面上很少。在句子互动，<strong>从 CEO 到财务，每个部门、每个人每天都在用 Agent 干活</strong>。不是配个工具，是工作方式本身换了。90 后 AI native 配 9 年 toB 老兵，这个组合全市场几乎没有。这条路我们自己先活成，再带客户一起跑。",
        pills=["AI 下沉到每个人", "90 后 × 9 年 toB", "自己先活成再带客户", "1 + N 组织"],
        body=body,
    )


# ────────────────────────── case · 该客户 ──────────────────────────

def page_case_xingqudao():
    body = ''

    # ── 执行摘要：6 大指标 ──
    metrics = [
        ('200<span style="font-size:18px;color:var(--gray-text);">→</span>913', '人服比（先锋组）<br/>约大盘 2 倍、基准 4.5 倍', 'var(--blue)'),
        ('28 万元', '最高单人月度产出<br/>月人效', 'var(--orange)'),
        ('↓50~62%', '单线索成本<br/>业务线 A ↓50% · 业务线 B ↓62%', 'var(--green)'),
        ('27%<span style="font-size:18px;color:var(--gray-text);">→</span>2.73%', 'AI 转人工率<br/>上线初 → 当前', 'var(--purple)'),
        ('16.26%<span style="font-size:18px;color:var(--gray-text);">→</span>0.13%', '系统故障率<br/>峰值 → 当前', 'var(--teal)'),
        ('24.3 万', '月度服务线索<br/>AI 月回复 211.5 万条消息', 'var(--blue)'),
    ]
    cards = ''.join(
        f'<div style="background:#fff;border:1px solid var(--gray-line);border-radius:16px;padding:26px 22px;text-align:center;">'
        f'<div style="font-size:30px;font-weight:800;color:{c};letter-spacing:-.02em;line-height:1.05;">{v}</div>'
        f'<div style="font-size:13px;color:var(--gray-text);margin-top:8px;line-height:1.5;">{l}</div></div>'
        for v, l, c in metrics
    )
    body += block(        "执行摘要",
        "AI 把整条「低转高」链路跑通",
        "人效翻倍、ROI 不掉、单线索成本砍半。客户敢把活按结果包给我们，就看这几个数。",
        f'<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:18px;max-width:1000px;margin:0 auto;">{cards}</div>'
        '<p style="text-align:center;font-size:13.5px;color:var(--gray-text);margin:28px auto 0;max-width:720px;line-height:1.7;">'
        '月度服务线索 24.3 万条、AI 回复 211.5 万条。跑在生产上，有真实业务量，不是 demo。</p>',
    )

    # ── 客户是谁 + 转化流程 ──
    body += split_section(
        eyebrow="客户是谁",
        title="在线教育头部品牌 · 我们成单体量最大的客户",
        paragraphs=[
            "这家客户做兴趣技能在线教育，旗下业务线 A、业务线 B、瑜伽、健康食养多个事业部。场景是<strong>企业微信 1v1 私聊</strong>，2025 年 6 月启动至今。",
            "线下驻场对比发现：各事业部流程框架一致，只是课程和开营时间不同——<strong>一个事业部跑通的搭法，可以直接复制到下一个</strong>。这是它能不断加业务线的原因，我们这套打法能复制，也是同一个道理。",
        ],
        bullets=[
            "<strong>① 广告投放获客</strong>：信息流广告报名体验营",
            "<strong>② 7 天 6 课体验营</strong>：低价引流，直播 + 回放",
            "<strong>③ 企微 1v1 破冰</strong>：班主任一对一私聊",
            "<strong>④ 识别诉求 / 痛点</strong>：学习目标、身体状况、能否上课",
            "<strong>⑤ 转正价课</strong>：陪学建立信任 → 销转",
        ],
        visual_html="""
<div style="background:#fff;border-radius:12px;padding:20px;border:1px solid var(--gray-line);">
<div style="font-size:12px;font-weight:800;color:var(--gray-text);letter-spacing:.04em;margin-bottom:14px;">客户档案</div>
<div style="display:flex;flex-direction:column;gap:10px;font-size:13.5px;">
<div style="display:flex;justify-content:space-between;"><span style="color:var(--gray-text);">行业</span><span style="font-weight:700;">兴趣技能在线教育</span></div>
<div style="display:flex;justify-content:space-between;"><span style="color:var(--gray-text);">事业部</span><span style="font-weight:700;">业务线 A / 业务线 B / 瑜伽 / 健康食养</span></div>
<div style="display:flex;justify-content:space-between;"><span style="color:var(--gray-text);">场景</span><span style="font-weight:700;">企业微信 · 私聊 1v1</span></div>
<div style="display:flex;justify-content:space-between;"><span style="color:var(--gray-text);">启动</span><span style="font-weight:700;">2025 年 6 月至今</span></div>
<div style="display:flex;justify-content:space-between;"><span style="color:var(--gray-text);">地位</span><span style="font-weight:700;color:var(--blue);">成单体量最大客户</span></div>
</div>
</div>
""",
    )

    # ── AI 干了什么 ──
    body += block(        "AI 干了什么",
        "全程接管：从「人海一对一」变成一套系统在跑",
        "人手不再是接量规模的天花板——接量期破冰挖需、服务期陪学建信任，被动回复 + 主动触达都交给 AI。",
        feat_grid([
            ("📥", "接量期 · 被动回复", "破冰挖需、知识库答疑、通用闲聊；命中严重病症直接转人工。", "bl"),
            ("📤", "接量期 · 主动触达", "加好友 1 小时内触达、对话结束 30 分钟追问、连续 3 天定点催回。", "or"),
            ("📚", "服务期 · 被动回复", "课前软促课、课中引导、课后点评——按学习节奏自适应。", "gr"),
            ("🔔", "服务期 · 主动触达", "第一天课前催自我介绍、每天课后触达、课后半小时催打卡。", "pu"),
        ], cols=2),
    )

    # ── 业务效果 ──
    body += split_section(
        eyebrow="业务效果",
        title="人效翻倍，ROI 不掉",
        paragraphs=[
            "在高人服比下 ROI 不掉。这是客户敢把活按结果包给我们的核心原因。",
            "先锋组人服比做到 <strong>913</strong>，约是大盘的 2 倍、AI 上线前基准的 4.5 倍；最高单人月度产出 <strong>28 万元</strong>。",
        ],
        bullets=[
            "AI 上线前基准人服比：200",
            "大盘均值：456",
            "先锋组最高：913（约大盘 2 倍）",
            "ROI 与大盘持平，部分期次更高",
        ],
        visual_html="""
<div style="background:#fff;border-radius:12px;padding:22px;border:1px solid var(--gray-line);">
<div style="font-size:12px;font-weight:800;color:var(--gray-text);letter-spacing:.04em;margin-bottom:18px;">人服比 · 人 / 周期</div>
<div style="display:flex;flex-direction:column;gap:16px;font-size:13px;">
<div><div style="display:flex;justify-content:space-between;margin-bottom:6px;"><span>AI 前 · 基准</span><span style="font-weight:800;">200</span></div><div style="height:14px;background:var(--gray-bg);border-radius:7px;overflow:hidden;"><div style="width:22%;height:100%;background:var(--gray-text);border-radius:7px;"></div></div></div>
<div><div style="display:flex;justify-content:space-between;margin-bottom:6px;"><span>大盘均值</span><span style="font-weight:800;">456</span></div><div style="height:14px;background:var(--gray-bg);border-radius:7px;overflow:hidden;"><div style="width:50%;height:100%;background:var(--orange);border-radius:7px;"></div></div></div>
<div><div style="display:flex;justify-content:space-between;margin-bottom:6px;"><span style="font-weight:700;color:var(--blue);">先锋组 · 最高</span><span style="font-weight:800;color:var(--blue);">913</span></div><div style="height:14px;background:var(--gray-bg);border-radius:7px;overflow:hidden;"><div style="width:100%;height:100%;background:var(--blue);border-radius:7px;"></div></div></div>
</div>
</div>
""",
        color="bl",
        reverse=True,
    )

    # ── 系统稳定性 ──
    body += split_section(
        eyebrow="系统效果",
        title="转人工率从 27% 压到 2.73%，用了大半年",
        paragraphs=[
            "稳定性不是一上线就有的。靠 badcase 集、回归测试集、评判标准、周例会复盘，一点点压下来。",
            "当前 2.73% 里，74% 是图片 / 视频规则性触发，26% 是意图转人工；异常质检不通过转人工占比 <strong>&lt;0.001%</strong>——AI 自己说错话需要人接管，这种情况几乎不发生。",
        ],
        bullets=[
            "AI 转人工率：27% → 2.73%",
            "系统故障率：16.26% → 0.13%（峰值 → 当前）",
            "AI 首次响应：21.2 秒（用户开口到 AI 回复）",
            "流程引擎执行：1.9 秒（单次链路均值）",
        ],
        visual_html="""
<div style="background:#fff;border-radius:12px;padding:22px;border:1px solid var(--gray-line);">
<div style="font-size:12px;font-weight:800;color:var(--gray-text);letter-spacing:.04em;margin-bottom:16px;">AI 转人工率 · 上线至今</div>
<div style="display:flex;align-items:flex-end;gap:14px;height:140px;">
<div style="flex:1;display:flex;flex-direction:column;align-items:center;justify-content:flex-end;height:100%;"><div style="font-weight:800;color:var(--orange);margin-bottom:6px;">27%</div><div style="width:100%;height:100%;background:var(--orange-lt);border-radius:8px 8px 0 0;"></div><div style="font-size:11px;color:var(--gray-text);margin-top:6px;">上线初</div></div>
<div style="flex:1;display:flex;flex-direction:column;align-items:center;justify-content:flex-end;height:100%;"><div style="font-weight:800;color:var(--gray-text);margin-bottom:6px;">~10%</div><div style="width:100%;height:37%;background:var(--gray-bg);border-radius:8px 8px 0 0;"></div><div style="font-size:11px;color:var(--gray-text);margin-top:6px;">中期</div></div>
<div style="flex:1;display:flex;flex-direction:column;align-items:center;justify-content:flex-end;height:100%;"><div style="font-weight:800;color:var(--green);margin-bottom:6px;">2.73%</div><div style="width:100%;height:10%;background:var(--green);border-radius:8px 8px 0 0;"></div><div style="font-size:11px;color:var(--gray-text);margin-top:6px;">当前</div></div>
</div>
</div>
""",
        color="gr",
    )

    # ── token 效率 ──
    rows = [
        ('2 月', '¥0.89', '4.8w'),
        ('3 月', '¥0.73', '11.5w'),
        ('4 月', '¥0.37', '12.0w'),
        ('5 月', '¥0.44', '16.0w'),
    ]
    table_rows = ''.join(
        f'<tr><td style="padding:10px 14px;border-top:1px solid var(--gray-line);font-weight:700;">{m}</td>'
        f'<td style="padding:10px 14px;border-top:1px solid var(--gray-line);text-align:right;color:var(--green);font-weight:700;">{cost}</td>'
        f'<td style="padding:10px 14px;border-top:1px solid var(--gray-line);text-align:right;font-weight:700;">{leads}</td></tr>'
        for m, cost, leads in rows
    )
    body += block(        "Token 效率",
        "成本砍半的同时，线索量翻 3 倍",
        "先把结果做对，再把每个结果的 token 用量压下来。越懂这门生意，每个结果越省。",
        '<div style="display:grid;grid-template-columns:1fr 1fr;gap:24px;max-width:1000px;margin:0 auto;align-items:start;">'
        '<div style="background:#fff;border:1px solid var(--gray-line);border-radius:14px;padding:20px;">'
        '<div style="font-size:13px;font-weight:800;margin-bottom:8px;">业务线 A正式服 · 月度单线索成本 vs 线索量</div>'
        '<table style="width:100%;border-collapse:collapse;font-size:13.5px;">'
        '<tr><th style="padding:8px 14px;text-align:left;font-size:12px;color:var(--gray-text);">月份</th>'
        '<th style="padding:8px 14px;text-align:right;font-size:12px;color:var(--gray-text);">单线索成本</th>'
        '<th style="padding:8px 14px;text-align:right;font-size:12px;color:var(--gray-text);">线索量</th></tr>'
        + table_rows +
        '</table></div>'
        '<div style="display:flex;flex-direction:column;gap:14px;">'
        '<div style="background:var(--green-lt);border-radius:14px;padding:20px;"><div style="font-size:13px;font-weight:800;color:var(--green);margin-bottom:8px;">成本怎么压下来的</div>'
        '<ul style="margin:0;padding-left:18px;font-size:13px;color:var(--gray-text);line-height:1.7;">'
        '<li><strong>换模型</strong>：按任务分层选模型——判断类用小模型，生成类用便宜的快模型</li>'
        '<li><strong>精简输入</strong>：去掉冗余历史、限制 RAG 检索，砍掉无效 token</li>'
        '<li><strong>链路优化</strong>：上下文重写与意图识别由并行改串行，消息延迟进线合并</li>'
        '</ul></div>'
        '<div style="background:#fff;border:1px solid var(--gray-line);border-radius:14px;padding:18px;text-align:center;">'
        '<div style="font-size:14px;font-weight:800;">业务线 A <span style="color:var(--green);">↓50%</span> · 业务线 B <span style="color:var(--green);">↓62%</span></div>'
        '<div style="font-size:12px;color:var(--gray-text);margin-top:4px;">单线索成本降幅</div></div>'
        '</div>'
        '</div>',
        alt=True,
    )

    # ── 怎么做到的：5 个产品 + FDE ──
    body += block(        "怎么做到的",
        "这套结果，是 5 个产品 + 一支 FDE 团队一起跑出来的",
        "一条消息背后是 6 个节点的自研流程引擎，5 个产品各管一段，FDE 团队贴着客户调，不是套壳调一个模型。",
        feat_grid([
            ("💬", "句子秒回 · 工位", "企业微信 1v1，AI 月回复 211.5 万条消息；全程自动跑，命中严重病症或异常时自动转人工。", "bl"),
            ("🧠", "句子秒懂 · 大脑", "一条消息背后 6 节点：上下文重写 → 意图识别 → 破冰挖需 → 知识库检索 → 生成回复 → 全程质检；按任务分层做模型路由。", "or"),
            ("🛡️", "句子守护 · 主管", "全程质检 + 质检不过二次生成、badcase 集 + 回归测试集——转人工率从 27% 压到 2.73% 靠的就是这套循环。", "gr"),
            ("📊", "句子参谋 · 参谋", "用户画像自动聚合、同步到企微用户描述，给业务老师做销售参考；业务进展一问就出。", "pu"),
            ("🏗️", "句子智造 · 地基", "测试服 / 正式服双环境、毫秒时序对齐、静默时段延迟再生成——真实业务的脏活都在系统里解决。", "te"),
        ], cols=3),
    )

    # ── FDE 交付 ──
    body += split_section(
        eyebrow="FDE 怎么交付",
        title="贴着客户把第一个项目跑通，方法论让下一个客户起步更快",
        paragraphs=[
            "这套交付流程：理解客户业务 → 拆 SOP → 整理知识库 → 设计提示词 + Workflow → 测试调优 → 上线支持 + 周会复盘。",
            "<strong>同一套打法，多家在线教育头部在跑</strong>。一个客户跑出来的方法论，能复制到下一个客户。",
        ],
        bullets=[
            "① 理解客户业务问题",
            "② 拆解 SOP",
            "③ 整理知识库（适配 AI 检索）",
            "④ 设计提示词 + Workflow",
            "⑤ 测试调优（badcase / 回归集）",
            "⑥ 上线支持 + 周会复盘",
        ],
        visual_html="""
<div style="background:#fff;border-radius:12px;padding:22px;border:1px solid var(--gray-line);">
<div style="font-size:12px;font-weight:800;color:var(--gray-text);letter-spacing:.04em;margin-bottom:14px;">同一套打法 · 多家头部在跑</div>
<div style="display:flex;flex-wrap:wrap;gap:10px;">
<span style="background:var(--blue-light);color:var(--blue);padding:8px 16px;border-radius:8px;font-size:14px;font-weight:700;">在线教育头部</span>
<span style="background:var(--gray-bg);padding:8px 16px;border-radius:8px;font-size:14px;font-weight:700;color:var(--gray-text);">头部小班课</span>
<span style="background:var(--gray-bg);padding:8px 16px;border-radius:8px;font-size:14px;font-weight:700;color:var(--gray-text);">成人职教头部</span>
<span style="background:var(--gray-bg);padding:8px 16px;border-radius:8px;font-size:14px;font-weight:700;color:var(--gray-text);">兴趣技能头部</span>
<span style="background:var(--gray-bg);padding:8px 16px;border-radius:8px;font-size:14px;font-weight:700;color:var(--gray-text);">飞书</span>
</div>
<div style="margin-top:16px;font-size:13px;color:var(--gray-text);line-height:1.65;">一个事业部跑通的搭法，复制到下一个事业部；一个客户跑出来的方法论，复制到下一个客户。</div>
</div>
""",
        color="or",
        reverse=True,
    )

    # ── 越用越多 ──
    body += block(        "越用越多",
        "老客户上岗后，线索量一直爬坡",
        "线索量上去，token 消耗就上去，收入跟着上去。客户不流失，还越用越多。",
        '<div style="background:#fff;border:1px solid var(--gray-line);border-radius:16px;padding:28px;max-width:820px;margin:0 auto;">'
        '<div style="font-size:13px;font-weight:800;color:var(--gray-text);margin-bottom:20px;">业务线 A事业部 · 月度服务线索量（万条） · 4 个月 3.3 倍</div>'
        '<div style="display:flex;align-items:flex-end;gap:20px;height:180px;">'
        + ''.join(
            f'<div style="flex:1;display:flex;flex-direction:column;align-items:center;justify-content:flex-end;height:100%;">'
            f'<div style="font-weight:800;color:var(--blue);margin-bottom:6px;">{v}w</div>'
            f'<div style="width:100%;height:{h}%;background:linear-gradient(180deg,var(--blue),var(--blue-mid));border-radius:8px 8px 0 0;"></div>'
            f'<div style="font-size:12px;color:var(--gray-text);margin-top:8px;">{m}</div></div>'
            for m, v, h in [('2 月', '4.8', 30), ('3 月', '11.5', 72), ('4 月', '12.0', 75), ('5 月', '16.0', 100)]
        )
        + '</div></div>',
        alt=True,
    )

    # ── 三大结论 ──
    body += block(        "三大结论",
        "这套模式最完整的一次验证",
        "这家在线教育头部品牌，是我们目前成单体量最大的客户，也是「按结果交付」最完整的一次跑通。",
        feat_grid([
            ("✅", "按结果跑得通", "人服比翻 4.5 倍、约大盘 2 倍，ROI 不掉。这是「客户赚到我们才赚」能成立的前提。", "bl"),
            ("⚡", "token 效率是真省出来的", "单线索成本砍 50~62%，同时线索量翻 3 倍。越懂这门生意，每个结果越省 token。", "or"),
            ("🏗️", "自研平台扛得住生产", "多节点编排、全程质检、二次生成、时序对齐——真实业务的脏活都在系统里解决。", "gr"),
        ], cols=3),
    )

    body += f"""
<section class="section-block">
  <div class="container">
    {cta_band("把这套打法，跑到你的业务里")}
  </div>
</section>
""".strip()

    return page_layout(
        title="客户案例 · 在线教育头部 · AI 跑通低转高整条链路 | 句子互动",
        description="句子互动成单体量最大的客户，是一家在线教育头部品牌。AI 把整条「低转高」链路跑通：人服比 200→913、月人效 28 万、单线索成本砍 50~62%、AI 转人工率从 27% 压到 2.73%、故障率 16.26%→0.13%。月度服务线索 24.3 万条、AI 回复 211.5 万条。",
        rel="",
        breadcrumbs=[("首页", "index.html"), ("客户与行业", "industries.html"), ("在线教育头部客户", None)],
        hero_kicker="客户案例 · 在线教育头部客户",
        hero_h1='在线教育头部客户（兴趣技能赛道） · <span class="accent">AI 把整条低转高链路跑通</span>',
        hero_lede="在线教育头部品牌，<strong>我们目前成单体量最大的客户</strong>。2025-06 启动至今——人效翻倍、单线索成本砍 50~62%、ROI 不掉，AI 转人工率从 27% 压到 2.73%。这是「客户赚到我们才赚」能成立的前提。",
        pills=["2025-06 启动至今", "企业微信 1v1 私聊", "业务线 A / 业务线 B / 瑜伽 / 健康食养", "成单体量最大客户"],
        body=body,
    )


# ────────────────────────── build all ──────────────────────────

def page_fde():
    body = ''
    body += block(        "FDE 是什么",
        "把工程师派到客户现场，对结果负责",
        "FDE，Forward Deployed Engineer——前移到客户业务现场的工程师。不是来装个软件就走，是和客户坐在一起，把这门生意先搞清楚，再让 AI 在里面真正干出结果。",
        '''<div style="max-width:980px;margin:0 auto;border:1px solid var(--gray-line);border-radius:16px;overflow:hidden;">
<div style="display:grid;grid-template-columns:1fr 1fr;">
  <div style="background:var(--gray-bg);padding:15px 22px;font-weight:800;font-size:13.5px;color:var(--gray-text);">普通产品工程师</div>
  <div style="background:var(--blue-light);padding:15px 22px;font-weight:800;font-size:13.5px;color:var(--blue);">FDE</div>
</div>
<div style="display:grid;grid-template-columns:1fr 1fr;border-top:1px solid var(--gray-line);">
  <div style="padding:14px 22px;font-size:14px;color:var(--gray-text);line-height:1.6;">关心「一个能力，给很多客户」</div>
  <div style="padding:14px 22px;font-size:14px;color:var(--black);line-height:1.6;background:#fbfcff;">关心「一个客户，很多能力」</div>
</div>
<div style="display:grid;grid-template-columns:1fr 1fr;border-top:1px solid var(--gray-line);">
  <div style="padding:14px 22px;font-size:14px;color:var(--gray-text);line-height:1.6;">交一套搭好的流程，就算完</div>
  <div style="padding:14px 22px;font-size:14px;color:var(--black);line-height:1.6;background:#fbfcff;">对客户的业务结果负责，结果没出来不算完</div>
</div>
<div style="display:grid;grid-template-columns:1fr 1fr;border-top:1px solid var(--gray-line);">
  <div style="padding:14px 22px;font-size:14px;color:var(--gray-text);line-height:1.6;">在公司里写通用功能</div>
  <div style="padding:14px 22px;font-size:14px;color:var(--black);line-height:1.6;background:#fbfcff;">写两头的代码：现场的定制，抽回产品的标准能力</div>
</div>
</div>''',
    )
    body += block(        "FDE 怎么干",
        "贴着客户的业务跑，把脏活在现场解决",
        "AI 落地难的从来不是模型，是客户那套各不相同的真实业务。FDE 就是去啃这块。",
        feat_grid([
            ("🤝", "先搞懂这门生意", "不是上来就装软件。先和客户把业务、流程、卡点搞清楚。AI 要干的活，得先有人真懂。", "bl"),
            ("🎯", "对结果负责", "和客户签对赌、按结果收费。客户的转化、人效真变好了，我们才拿钱。", "or"),
            ("🔁", "能力回流产品", "在一个客户现场踩出来的能力，抽象成产品里的标准能力，下一个客户起步就用得上。做一次，卖多次。", "gr"),
            ("🧑‍🎓", "不一定是码农", "FDE 不一定要会写代码的人做，不写代码的反而常常做得更好——我们的 FDE 负责人，是个学法语的 00 后。懂业务、肯钻，比什么都重要。", "pu"),
        ], cols=2),
    )
    body += split_section(
        eyebrow="先找离钱最近的场景",
        title="不是哪个好做，是哪个最值钱",
        paragraphs=[
            "AI 客服省成本，AI 销售带增长。FDE 进场第一件事，就是帮客户找到离钱最近的那个场景——同一套底层能力，落在销售上比落在客服上值钱得多。",
            "这也是 FDE 和「卖软件」的根本区别：软件卖出去就结束了，FDE 是客户业绩涨、我们才涨。绑在一起，才有人愿意把脏活干到底。",
        ],
        bullets=[
            "AI 客服：把进线接住、成本压下来",
            "AI 销售：从建联到成交全程接管，直接带增长",
            "先挑最值钱的场景下手，再往外扩",
            "按结果收费——做出来才收钱",
        ],
        visual_html="""
<div style="background:#fff;border-radius:12px;padding:22px;border:1px solid var(--gray-line);">
<div style="font-size:12px;font-weight:700;color:var(--gray-text);margin-bottom:16px;letter-spacing:.04em;">FDE 进场 · 怎么挑场景</div>
<div style="display:flex;flex-direction:column;gap:10px;font-size:13px;">
<div style="display:flex;align-items:center;gap:10px;padding:11px 14px;background:var(--gray-bg);border-radius:8px;"><span style="color:var(--blue);font-weight:800;">1</span><span>先摸清这门生意，哪一环最影响收入</span></div>
<div style="display:flex;align-items:center;gap:10px;padding:11px 14px;background:var(--gray-bg);border-radius:8px;"><span style="color:var(--blue);font-weight:800;">2</span><span>挑离钱最近的场景先上，跑出结果</span></div>
<div style="display:flex;align-items:center;gap:10px;padding:11px 14px;background:var(--blue-light);border-radius:8px;"><span style="color:var(--blue);font-weight:800;">3</span><span style="color:var(--blue);font-weight:600;">按结果收费，客户业绩涨我们才涨</span></div>
</div>
</div>
""",
        color="bl",
        reverse=True,
    )
    body += f"""
<section class="section-block">
  <div class="container">
    {cta_band("让 FDE 团队进场，把 AI 跑进你的业务")}
  </div>
</section>
""".strip()
    return page_layout(
        title="FDE 交付团队 · 对结果负责的工程师 | 句子互动",
        description="FDE（Forward Deployed Engineer）——前移到客户业务现场的工程师团队。不只装软件，对客户的业务结果负责：先搞懂这门生意，按结果收费，把现场踩出来的能力回流成产品。",
        rel="",
        breadcrumbs=[("首页", "index.html"), ("FDE 交付团队", None)],
        hero_kicker="FDE · 我们怎么交付",
        hero_h1='一支<span class="accent">对结果负责</span>的 FDE 团队',
        hero_lede="买软件，员工用不用得好你自己背。我们派的是 FDE——<strong>Forward Deployed Engineer，前移到你业务现场的工程师</strong>。先搞懂这门生意，按结果收费，把现场踩出来的能力回流成产品。客户业绩涨，我们才涨。",
        pills=["前移到客户现场", "对业务结果负责", "按结果收费", "能力回流产品"],
        body=body,
    )


def page_dongxing():
    body = ''
    body += block(        "为什么要先做知识工程",
        "200 万字塞给 AI，反而更答不准",
        "客户常以为把几百万字知识库丢给 AI 就行。结果命中率更低、答得更乱。知识不干净，不赖 AI——是知识本身没整理过。句子智库先把这一层做对，再上 Agent。",
        feat_grid([
            ("🧹", "清洗去重", "几百万字里大量是重复、过期、互相打架的内容。先洗一遍，把矛盾和冗余挑出来，留下真正有用的。", "bl"),
            ("✂️", "结构化切分", "一篇长文档不能整块丢给模型检索。按语义切成合适的块，每块带上下文和标签，AI 才查得准。", "or"),
            ("🎯", "检索优化", "同一个问题，客户有十种问法。把同义、近义、口语化的问法都对上，AI 检索的命中率才稳。", "gr"),
            ("🔁", "持续回流", "上线后哪条没答好，回流进知识资产再修。用得越多，知识越准。不是一次性整理完就不管了。", "pu"),
        ], cols=2),
    )
    body += split_section(
        eyebrow="知识工程",
        title="几百万字 → 二十万字能查的资产",
        paragraphs=[
            "知识工程不是把文档存进数据库。是把客户脑子里、文档里、聊天记录里散着的东西，整理成 AI 查得准、用得上的资产。",
            "我们的做法：先用句子智库把几百万字炼成约二十万字可检索资产，再上其余产品和 FDE 团队。顺序反了，跑不通。",
        ],
        bullets=[
            "文档、表格、历史对话、SOP——多来源一起进",
            "炼成带标签、可检索、可追溯来源的知识块",
            "每条回答都能查到出处，不是模型编的",
            "上线后持续回流，知识越用越干净",
        ],
        visual_html="""
<div style="background:#fff;border-radius:12px;padding:20px;border:1px solid var(--gray-line);">
<div style="display:flex;align-items:center;justify-content:space-between;gap:12px;">
<div style="text-align:center;flex:1;"><div style="font-size:26px;font-weight:900;color:var(--gray-text);">200 万字</div><div style="font-size:12px;color:var(--gray-text);margin-top:4px;">散、乱、重复、过期</div></div>
<div style="font-size:22px;color:var(--purple);">→</div>
<div style="text-align:center;flex:1;"><div style="font-size:26px;font-weight:900;color:var(--purple);">20 万字</div><div style="font-size:12px;color:var(--gray-text);margin-top:4px;">干净、可检索、带出处</div></div>
</div>
<div style="margin-top:16px;font-size:11.5px;color:var(--gray-text);background:var(--purple-lt);padding:10px 12px;border-radius:8px;">先把这层做对，AI 才查得准。知识工程是 Agent 上岗的前提，不是上线后再补的活。</div>
</div>
""",
        color="pu",
        reverse=True,
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
        description="句子智库——AI 员工的记忆。把客户几百万字散乱知识炼成 AI 能查、能用、越用越准的可检索资产。知识工程是 Agent 上岗的前提：先把知识做对，再上产品。",
        rel="../",
        breadcrumbs=[("首页", "../index.html"), ("产品", None), ("句子智库", None)],
        hero_kicker="产品 · 智库 · 记忆",
        hero_h1='句子智库 · <span class="accent">AI 员工的记忆</span>',
        hero_lede="客户给的几百万字知识库，AI 直接用不了：散、乱、格式不一、查不准。<strong>句子智库把它炼成 AI 能查、能用的知识资产，越用越准</strong>。先把知识工程做对，再上 Agent。不然给多少字都跑不通。",
        pills=["知识工程进场第一步", "几百万字 → 可检索资产", "每条回答可追溯出处", "Agent 上岗的前提"],
        body=body,
    )


def page_cli():
    body = ''
    body += block(        "为什么 AI 需要一双手",
        "很多企业的核心系统，没 API、改不动",
        "AI 想接进客户业务，常卡在一个地方：那套用了十几年的老系统没有 API，谁也不敢动。模型再聪明，没手也干不了活。句子 CLI 给 AI 一双手。人能在电脑上点的，它都能替你点。",
        feat_grid([
            ("🖱️", "像人一样操作界面", "没有 API 也能接。CLI 直接驱动鼠标键盘、读屏幕，像人一样操作任何软件界面。", "bl"),
            ("🔗", "跨系统搬运", "从一个系统取数、填进另一个系统，中间没接口的活，CLI 自动跑通，不用人来回复制粘贴。", "or"),
            ("⏱️", "定时批处理", "对账、导表、批量录入这类重复的活，设好就自动跑，人不用守着。", "gr"),
            ("🧱", "真实沙盒隔离", "每个任务在独立沙盒里跑，崩了自动续跑，不影响别的任务、也不碰客户其他系统。", "te"),
        ], cols=2),
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
        description="句子 CLI——AI 员工的手，操作一切人用软件的底层 RPA 驱动。老系统没 API、对接不了？CLI 像人一样直接操作界面，把活干完。",
        rel="../",
        breadcrumbs=[("首页", "../index.html"), ("产品", None), ("句子 CLI", None)],
        hero_kicker="产品 · CLI · 手",
        hero_h1='句子 CLI · <span class="accent">AI 员工的手</span>',
        hero_lede="凡是人能在电脑上点的，CLI 能替它点。<strong>操作一切人用软件的底层 RPA 驱动</strong>——老系统没 API、对接不了？CLI 像人一样直接操作界面，把活干完。",
        pills=["操作一切人用软件", "无 API 也能接", "底层 RPA 驱动", "老系统也能接进来"],
        body=body,
    )


if __name__ == '__main__':
    pages = {
        'products/miaohui.html': page_miaohui(),
        'products/miaodong.html': page_miaodong(),
        'products/shouhu.html': page_shouhu(),
        'products/dongxing.html': page_dongxing(),
        'products/cli.html': page_cli(),
        'fde.html': page_fde(),
        'enterprise.html': page_enterprise(),
        'industries.html': page_industries(),
        'about.html': page_about(),
        'insights.html': page_insights(),
        'case-xingqudao.html': page_case_xingqudao(),
    }
    workforce = workforce_pages()
    for slug, content in workforce.items():
        pages[f'workforce/{slug}.html'] = content

    for relpath, html_content in pages.items():
        full = os.path.join(ROOT, relpath)
        os.makedirs(os.path.dirname(full), exist_ok=True)
        with open(full, 'w', encoding='utf-8') as f:
            f.write(html_content)
        size = os.path.getsize(full)
        print(f"  {relpath}  ({size:,} bytes)")

    print(f"\nbuilt {len(pages)} pages")
