#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_news.py — 「动态」信息聚合管线（多源）

用法:
  python3 build_news.py            # 增量: 只抓 data/news.json 里还没有的条目
  python3 build_news.py --full     # 全量重抓(元数据变更/首次初始化)
  python3 build_news.py --limit 5  # 调试: 本次每源最多抓 5 条新内容

内容源(SOURCES)按 type 走不同 adapter:
  sitemap      逐篇抓文章页解析 JSON-LD(rui.juzi.bot 创始人博客)
  rss          RSS2/Atom 通吃 + 脏 XML 正则兜底(Wechaty 社区博客+Releases、36氪)
  feishu-base  发布闸门: 走本机 lark-cli 读飞书多维表格《官网动态发布登记》,
               只拉「上官网=勾 且 有公众号正式链接」的行, og 元数据自动补齐。
               三个公众号(句子互动官方/AI对话未来/佳芮的创业笔记)同表, 账号名落 category。
  manual       本地 JSON 投递位(备用, 当前无源使用): {url,title,date,...} 贴进去即合流

产出(只写标记区块, 页面其余部分手工维护, 可安全反复运行——与已废弃的 build_pages.py 不同):
  data/news.json       {sources:[源健康元数据], items:[全量条目]}
  三个平行页面(PAGES), 每页三个注入点:
    <!-- NEWS:LIST:BEGIN/END -->               前 PRERENDER 条静态预渲染(SEO 唯一入口)
    <script id="news-data">…</script>          内联数据(A/B=items 数组, C=完整对象含 sources)
    <b id="newsTotal">…</b>                    内容总数
  news.html   卡片流(A 版, 进全站导航)
  news-b.html 知乎式列表流(B 版, noindex)
  news-c.html 多源聚合流(C 版, noindex, 按月分组 + 源面板)

模板同构约束(改任一处必须同步对应页面 JS):
  card_html() ↔ news.html cardHTML() | row_html() ↔ news-b.html rowHTML()
  feed_list() ↔ news-c.html renderBatch()(含月份分组逻辑)
"""
import argparse
import hashlib
import html as htmllib
import json
import re
import shutil
import subprocess
import sys
import time
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from pathlib import Path
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parent
DATA_FILE = ROOT / "data" / "news.json"
UA = "Mozilla/5.0 (compatible; juzibot-news-sync/1.0; +https://juzibot.com)"
PRERENDER = 20
FETCH_DELAY = 0.25  # 礼貌抓取间隔(秒)
SUMMARY_MAX = 170

SOURCES = [
    {
        "id": "rui-blog",
        "name": "创始人专栏",
        "author": "李佳芮",
        "type": "sitemap",
        "sitemap": "https://rui.juzi.bot/sitemap.xml",
        # 仅收带日期的文章页: https://rui.juzi.bot/<分类>/<YYYY-MM-DD>-<slug>.html
        "post_re": re.compile(r"^https://rui\.juzi\.bot/([a-z0-9-]+)/(\d{4}-\d{2}-\d{2})-[^/]+\.html$"),
        "home": "https://rui.juzi.bot/",
    },
    {
        # 发布闸门: 飞书多维表格《官网动态发布登记》(建于句子互动租户, 2026-07-07)。
        # 运营在公众号发文后到表里贴正式链接+勾「上官网」, 管线只拉过闸行,
        # 标题/日期/摘要自动从 mp.weixin 的 og 标签补齐。需要本机 lark-cli 已授权。
        "id": "wechat-mp",
        "name": "公众号",
        "author": "句子互动",
        "type": "feishu-base",
        "base_token": "HhPubortTafxOssddqJc4m9Znkd",
        "table_id": "tblykah8iZAdwLfF",
        "home": "",
    },
    # Wechaty 源已撤(2026-07-07 用户裁决: 版本发布等开发者向内容对官网受众是噪音)。
    # 如需恢复: 加回 {"id":"wechaty-oss","type":"rss","feeds":[("https://wechaty.js.org/blog/rss.xml","社区博客")],...}
    {
        # 机器之心 RSS 已停(302 到付费数据服务), 2026-07 换 36氪
        "id": "industry",
        "name": "行业·36氪",
        "author": "36氪",
        "type": "rss",
        "feeds": [("https://36kr.com/feed", "行业动态")],
        "max_items": 15,
        "home": "https://36kr.com/",
    },
]


# ---------------- 抓取与通用解析 ----------------

def fetch(url, retries=2, timeout=20):
    last = None
    for i in range(retries + 1):
        try:
            with urlopen(Request(url, headers={"User-Agent": UA}), timeout=timeout) as r:
                return r.read().decode("utf-8", "replace")
        except Exception as e:  # noqa: BLE001 — 网络类异常统一重试
            last = e
            time.sleep(1 + i)
    raise last


def clean_summary(s):
    s = re.sub(r"<[^>]+>", " ", s or "")
    s = htmllib.unescape(s)
    s = re.sub(r"\s+", " ", s).strip()
    return (s[: SUMMARY_MAX - 1] + "…") if len(s) > SUMMARY_MAX else s


def norm_date(raw):
    """RFC822 / ISO8601 / YYYY-MM-DD → YYYY-MM-DD, 解析失败返回 ''。"""
    raw = (raw or "").strip()
    if not raw:
        return ""
    m = re.match(r"\d{4}-\d{2}-\d{2}", raw)
    if m:
        return m.group(0)
    try:
        return parsedate_to_datetime(raw).strftime("%Y-%m-%d")
    except (TypeError, ValueError):
        return ""


def make_item(src, url, title, summary, date, category, tags=None):
    if not (url and title and date):
        return None
    return {
        "id": hashlib.sha1(url.encode()).hexdigest()[:12],
        "title": title.strip(),
        "url": url,
        "summary": clean_summary(summary),
        "category": (category or "").strip() or src.get("default_category", ""),
        "tags": tags or [],
        "date": date,
        "source": src["id"],
        "source_name": src["name"],
        "author": src["author"],
    }


# ---------------- adapter: sitemap(rui 博客) ----------------

def jsonld_blogposting(page):
    for m in re.finditer(r'<script type="application/ld\+json">\s*(\{.*?\})\s*</script>', page, re.S):
        try:
            obj = json.loads(m.group(1))
        except json.JSONDecodeError:
            continue
        if obj.get("@type") == "BlogPosting":
            return obj
    return {}


def meta_content(page, pattern):
    m = re.search(pattern, page)
    return htmllib.unescape(m.group(1)).strip() if m else ""


def parse_blog_article(page, url, url_match, src):
    ld = jsonld_blogposting(page)
    title = (ld.get("headline") or meta_content(page, r'<meta property="og:title" content="([^"]*)"') or "").strip()
    if not title:
        title = re.sub(r"\s*·\s*李佳芮的博客\s*$", "", meta_content(page, r"<title>([^<]*)</title>"))
    summary = (ld.get("description") or meta_content(page, r'<meta name="description" content="([^"]*)"')).strip()
    date = norm_date(str(ld.get("datePublished") or "")) or url_match.group(2)
    cat_m = re.search(r'class="post-cat">([^<]+)<', page)
    category = htmllib.unescape(cat_m.group(1)).strip() if cat_m else url_match.group(1)
    tags = [t.strip() for t in str(ld.get("keywords") or "").split(",") if t.strip()]
    return make_item(src, url, title, summary, date, category, tags)


def sync_sitemap(src, old, limit):
    sitemap = fetch(src["sitemap"])
    urls = re.findall(r"<loc>([^<]+)</loc>", sitemap)
    posts = [(u, m) for u in urls if (m := src["post_re"].match(u.strip()))]
    new_posts = [(u, m) for u, m in posts if u not in old]
    print(f"[{src['id']}] sitemap 共 {len(urls)} 条, 文章 {len(posts)} 篇, 待抓 {len(new_posts)} 篇")
    got, failed = [], []
    for u, m in new_posts:
        if limit and len(got) + len(failed) >= limit:
            break
        try:
            it = parse_blog_article(fetch(u), u, m, src)
            got.append(it) if it else failed.append(u)
        except Exception as e:  # noqa: BLE001
            failed.append(u)
            print(f"  [失败] {u}: {e}")
        time.sleep(FETCH_DELAY)
    return got, failed


# ---------------- adapter: rss(RSS2 / Atom 通吃) ----------------

ATOM = "{http://www.w3.org/2005/Atom}"


def parse_feed_regex(xml_text):
    """脏 XML 兜底: 正则抽 RSS2 item(中文媒体 feed 常有未转义 HTML, 严格解析会炸)。"""
    out = []
    for block in re.findall(r"<item>(.*?)</item>", xml_text, re.S):
        def grab(tag):
            m = re.search(rf"<{tag}[^>]*>\s*(?:<!\[CDATA\[)?(.*?)(?:\]\]>)?\s*</{tag}>", block, re.S)
            return htmllib.unescape(m.group(1)).strip() if m else ""
        out.append({"url": grab("link"), "title": grab("title"), "summary": grab("description"),
                    "date": norm_date(grab("pubDate")), "category": grab("category")})
    return [e for e in out if e["url"]]


def parse_feed(xml_text):
    """返回 [{url,title,summary,date,category}]，兼容 RSS2 与 Atom；坏 XML 走正则兜底。"""
    if re.match(r"\s*<(!doctype\s+)?html", xml_text, re.I):
        raise ValueError("返回的是 HTML 而不是 feed(源可能已下线或跳转)")
    try:
        root = ET.fromstring(re.sub(r"^\s*<\?xml[^>]*\?>", "", xml_text, count=1))
    except ET.ParseError:
        return parse_feed_regex(xml_text)
    out = []
    for node in root.iter("item"):  # RSS2
        link = (node.findtext("link") or "").strip()
        out.append({
            "url": link,
            "title": (node.findtext("title") or "").strip(),
            "summary": node.findtext("description") or "",
            "date": norm_date(node.findtext("pubDate") or ""),
            "category": (node.findtext("category") or "").strip(),
        })
    for node in root.iter(f"{ATOM}entry"):  # Atom
        link = ""
        for ln in node.findall(f"{ATOM}link"):
            if ln.get("rel") in (None, "alternate"):
                link = ln.get("href") or ""
                break
        out.append({
            "url": link.strip(),
            "title": (node.findtext(f"{ATOM}title") or "").strip(),
            "summary": node.findtext(f"{ATOM}summary") or node.findtext(f"{ATOM}content") or "",
            "date": norm_date(node.findtext(f"{ATOM}published") or node.findtext(f"{ATOM}updated") or ""),
            "category": "",
        })
    return [e for e in out if e["url"]]


def sync_rss(src, old, limit):
    got, failed = [], []
    for feed_url, default_cat in src["feeds"]:
        try:
            entries = parse_feed(fetch(feed_url))
        except Exception as e:  # noqa: BLE001
            failed.append(feed_url)
            print(f"  [失败] feed {feed_url}: {e}")
            continue
        fresh = [e for e in entries[: src.get("max_items", 15)] if e["url"] not in old]
        print(f"[{src['id']}] {feed_url} 共 {len(entries)} 条, 收前 {src.get('max_items', 15)}, 新 {len(fresh)} 条")
        for e in fresh:
            if limit and len(got) >= limit:
                break
            it = make_item(src, e["url"], e["title"], e["summary"], e["date"], e["category"] or default_cat)
            if it:
                got.append(it)
    return got, failed


# ---------------- adapter: manual(手动投递位, 公众号) ----------------

def sync_manual(src, old, limit):
    path = src["file"]
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps({
            "_readme": "手动投递位: 往 items 里加 {url,title,date,summary?,category?}。只有 url 时管线尝试抓 mp.weixin 元数据。公众号无公开 RSS; 接 WeRSS/自建服务后可在 build_news.py 里原地改成 rss 源。",
            "items": [],
        }, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"[{src['id']}] 已初始化投递位 {path.relative_to(ROOT)}")
        return [], []
    entries = json.loads(path.read_text(encoding="utf-8")).get("items", [])
    got, failed = [], []
    for e in entries:
        u = (e.get("url") or "").strip()
        if not u or u in old:
            continue
        if limit and len(got) + len(failed) >= limit:
            break
        title, summary, date = e.get("title", ""), e.get("summary", ""), norm_date(e.get("date", ""))
        if not (title and date):  # 信息不全 → 尝试抓页面元数据(mp.weixin 文章页含 og: 标签)
            try:
                page = fetch(u)
                title = title or meta_content(page, r'<meta property="og:title" content="([^"]*)"')
                summary = summary or meta_content(page, r'<meta property="og:description" content="([^"]*)"')
                ct = re.search(r'var\s+ct\s*=\s*"(\d+)"', page)
                date = date or (datetime.fromtimestamp(int(ct.group(1)), tz=timezone.utc).strftime("%Y-%m-%d") if ct else "")
                time.sleep(FETCH_DELAY)
            except Exception as ex:  # noqa: BLE001
                print(f"  [失败] 投递条目抓取 {u}: {ex}")
        it = make_item(src, u, title, summary, date, e.get("category", ""))
        got.append(it) if it else (failed.append(u), print(f"  [跳过] 投递条目缺 title/date 且抓取失败: {u}"))
    print(f"[{src['id']}] 投递位 {len(entries)} 条, 新收 {len(got)} 条")
    return got, failed


# ---------------- adapter: feishu-base(发布登记表, 公众号闸门) ----------------

def wechat_meta(url):
    """抓 mp.weixin 文章页 og 标签, 返回 (title, summary, date)——任一项可能为空。"""
    page = fetch(url)
    title = meta_content(page, r'<meta property="og:title" content="([^"]*)"')
    summary = meta_content(page, r'<meta property="og:description" content="([^"]*)"')
    ct = re.search(r'var\s+ct\s*=\s*"(\d+)"', page)
    date = datetime.fromtimestamp(int(ct.group(1)), tz=timezone.utc).strftime("%Y-%m-%d") if ct else ""
    return title, summary, date


def cell_link(cell):
    """url 字段的取值兼容: 字符串 / {link,text} / 数组。"""
    if isinstance(cell, dict):
        return (cell.get("link") or cell.get("text") or "").strip()
    if isinstance(cell, list):
        return "".join(cell_link(x) for x in cell).strip()
    return str(cell or "").strip()


def sync_feishu_base(src, old, limit):
    if not shutil.which("lark-cli"):
        raise RuntimeError("lark-cli 不在 PATH(登记表 adapter 依赖本机已授权的 lark-cli)")
    cmd = ["lark-cli", "base", "+record-list",
           "--base-token", src["base_token"], "--table-id", src["table_id"],
           "--field-id", "文章标题", "--field-id", "公众号正式链接",
           "--field-id", "属于哪个号", "--field-id", "上官网",
           "--format", "json", "--limit", "200"]
    p = subprocess.run(cmd, capture_output=True, text=True, timeout=90)
    raw = p.stdout
    if "{" not in raw:
        raise RuntimeError(f"lark-cli 无输出: {p.stderr[:200]}")
    d = json.loads(raw[raw.index("{"):])
    if not d.get("ok"):
        raise RuntimeError(f"record-list 失败: {d.get('error', {}).get('message', '未知')}")

    rows = d["data"]["data"]
    got, failed, passed = [], [], 0
    for row in rows:
        title_cell, link_cell, acct_cell, on_site = (list(row) + [None] * 4)[:4]
        link = cell_link(link_cell)
        if not on_site or not link:  # 闸门: 勾了「上官网」且有正式链接才收
            continue
        passed += 1
        if link in old:
            continue
        if limit and len(got) + len(failed) >= limit:
            break
        account = acct_cell[0] if isinstance(acct_cell, list) and acct_cell else str(acct_cell or "")
        title = title_cell if isinstance(title_cell, str) else ""
        summary, date = "", ""
        try:
            t, summary, date = wechat_meta(link)
            title = t or title
            time.sleep(FETCH_DELAY)
        except Exception as ex:  # noqa: BLE001 — 元数据抓不到就用表里的标题兜底
            print(f"  [警告] 公众号元数据抓取失败 {link}: {ex}")
        it = make_item(src, link, title, summary, date or datetime.now().strftime("%Y-%m-%d"), account)
        got.append(it) if it else (failed.append(link), print(f"  [跳过] 登记行缺标题且抓取失败: {link}"))
    print(f"[{src['id']}] 登记表 {len(rows)} 行, 过闸 {passed} 行, 新收 {len(got)} 条")
    return got, failed


ADAPTERS = {"sitemap": sync_sitemap, "rss": sync_rss, "manual": sync_manual, "feishu-base": sync_feishu_base}


# ---------------- 渲染模板(与各页 JS 同构) ----------------

def esc(s):
    return htmllib.escape(str(s if s is not None else ""), quote=True)


def card_html(it):
    """与 news.html 页内 JS cardHTML() 同构(预渲染不带 .in, 交给 site.js 的 .rv 揭示动画)。"""
    icon = SRC_ICON.get(it["source"], "fa-solid fa-newspaper")
    return (
        f'<article class="news-card rv" data-src="{esc(it["source"])}">'
        f'<div class="nc-top"><span class="nc-srcb s-{esc(it["source"])}"><i class="{icon}"></i>{esc(it["source_name"])}</span>'
        + (f'<span class="nc-cat">{esc(it["category"])}</span>' if it["category"] else "")
        + f'<time class="nc-date" datetime="{esc(it["date"])}">{esc(it["date"])}</time></div>'
        f'<h3 class="nc-title"><a href="{esc(it["url"])}" target="_blank" rel="noopener">{esc(it["title"])}</a></h3>'
        f'<p class="nc-sum">{esc(it["summary"])}</p>'
        '<div class="nc-foot">'
        f'<span class="nc-src">{esc(it["author"])}</span>'
        '<span class="nc-actions">'
        f'<button type="button" class="nc-ask" data-t="{esc(it["title"])}"><i class="fa-solid fa-wand-magic-sparkles"></i>问句子</button>'
        f'<a class="nc-read" href="{esc(it["url"])}" target="_blank" rel="noopener">读原文<i class="fa-solid fa-arrow-up-right-from-square"></i></a>'
        "</span></div></article>"
    )


def row_html(it):
    """与 news-b.html 页内 JS rowHTML() 同构。"""
    icon = SRC_ICON.get(it["source"], "fa-solid fa-newspaper")
    tags = "".join(f'<span class="zi-tag">#{esc(t)}</span>' for t in it.get("tags", []))
    return (
        f'<article class="zh-item rv" data-src="{esc(it["source"])}">'
        f'<div class="zi-meta"><span class="zi-srcb s-{esc(it["source"])}"><i class="{icon}"></i>{esc(it["source_name"])}</span>'
        + (f'<span class="zi-cat">{esc(it["category"])}</span>' if it["category"] else "")
        + f'<span class="zi-src">{esc(it["author"])}</span>'
        f'<time class="zi-date" datetime="{esc(it["date"])}">{esc(it["date"])}</time></div>'
        f'<h3 class="zi-title"><a href="{esc(it["url"])}" target="_blank" rel="noopener">{esc(it["title"])}</a></h3>'
        f'<div class="zi-body"><p class="zi-sum">{esc(it["summary"])}</p>'
        + (f'<div class="zi-tags">{tags}</div>' if tags else "")
        + "</div>"
        '<div class="zi-act">'
        f'<button type="button" class="zi-ask" data-t="{esc(it["title"])}"><i class="fa-solid fa-wand-magic-sparkles"></i>问句子</button>'
        f'<a class="zi-link" href="{esc(it["url"])}" target="_blank" rel="noopener"><i class="fa-solid fa-arrow-up-right-from-square"></i>读原文</a>'
        f'<button type="button" class="zi-copy" data-u="{esc(it["url"])}"><i class="fa-solid fa-link"></i>复制链接</button>'
        '<span class="sp"></span>'
        '<button type="button" class="zi-more" aria-expanded="false">展开<i class="fa-solid fa-chevron-down"></i></button>'
        "</div></article>"
    )


SRC_ICON = {  # 与 news-c.html 页内 JS 的 ICON 同步
    "rui-blog": "fa-solid fa-pen-nib",
    "wechat-mp": "fa-brands fa-weixin",
    "wechaty-oss": "fa-solid fa-code-branch",
    "industry": "fa-solid fa-rss",
}


def feed_item_html(it):
    icon = SRC_ICON.get(it["source"], "fa-solid fa-newspaper")
    return (
        f'<article class="fd-item rv" data-src="{esc(it["source"])}">'
        f'<div class="fd-line"><span class="fd-src s-{esc(it["source"])}"><i class="{icon}"></i>{esc(it["source_name"])}</span>'
        + (f'<span class="fd-cat">{esc(it["category"])}</span>' if it["category"] else "")
        + f'<time class="fd-date" datetime="{esc(it["date"])}">{esc(it["date"][5:])}</time></div>'
        f'<h3 class="fd-title"><a href="{esc(it["url"])}" target="_blank" rel="noopener">{esc(it["title"])}</a></h3>'
        + (f'<p class="fd-sum">{esc(it["summary"])}</p>' if it["summary"] else "")
        + '<div class="fd-act">'
        f'<button type="button" class="fd-ask" data-t="{esc(it["title"])}"><i class="fa-solid fa-wand-magic-sparkles"></i>问句子</button>'
        f'<a class="fd-link" href="{esc(it["url"])}" target="_blank" rel="noopener"><i class="fa-solid fa-arrow-up-right-from-square"></i>读原文</a>'
        f'<button type="button" class="fd-copy" data-u="{esc(it["url"])}"><i class="fa-solid fa-link"></i>复制链接</button>'
        "</div></article>"
    )


def month_label(date):
    return f"{date[:4]} 年 {int(date[5:7])} 月"


def feed_list(items):
    """C 版按月分组渲染——与 news-c.html 页内 JS renderBatch() 同构。"""
    out, last = [], ""
    for it in items:
        mon = it["date"][:7]
        if mon != last:
            out.append(f'<div class="fd-month rv"><span>{esc(month_label(it["date"]))}</span></div>')
            last = mon
        out.append(feed_item_html(it))
    return "\n".join(out)


# 三个平行版本均为全源(2026-07-07 用户裁决), payload 均含 sources 元数据供来源筛选/面板使用
PAGES = [
    {"file": ROOT / "news.html", "render_list": lambda its: "\n".join(card_html(i) for i in its), "payload": "full", "only": None},
    {"file": ROOT / "news-b.html", "render_list": lambda its: "\n".join(row_html(i) for i in its), "payload": "full", "only": None},
    {"file": ROOT / "news-c.html", "render_list": lambda its: feed_list(its), "payload": "full", "only": None},
]


# ---------------- 注入 ----------------

def inject_between(text, begin, end, payload, label):
    pattern = re.compile(re.escape(begin) + r".*?" + re.escape(end), re.S)
    if not pattern.search(text):
        sys.exit(f"[错误] 找不到标记区块: {label}")
    return pattern.sub(begin + "\n" + payload + "\n" + end, text, count=1)


def inject_page(spec, items, sources_meta):
    path = spec["file"]
    page = path.read_text(encoding="utf-8")

    if spec["only"]:
        items = [i for i in items if i["source"] in spec["only"]]
    rendered = spec["render_list"](items[:PRERENDER])
    page = inject_between(page, "<!-- NEWS:LIST:BEGIN 此区块由 build_news.py 生成，勿手改 -->", "<!-- NEWS:LIST:END -->", rendered, f"{path.name} NEWS:LIST")

    payload = items if spec["payload"] == "items" else {"sources": sources_meta, "items": items}
    # 内联数据: JSON 放进 <script type="application/json">, 转义 </ 防止提前闭合标签
    data_json = json.dumps(payload, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    page, n = re.subn(
        r'(<script id="news-data" type="application/json">).*?(</script>)',
        lambda m: m.group(1) + data_json + m.group(2),
        page,
        count=1,
        flags=re.S,
    )
    if not n:
        sys.exit(f"[错误] {path.name} 里找不到 <script id=\"news-data\">")

    page, n = re.subn(r'(<b id="newsTotal">)[^<]*(</b>)', lambda m: m.group(1) + str(len(items)) + m.group(2), page, count=1)
    if not n:
        sys.exit(f"[错误] {path.name} 里找不到 <b id=\"newsTotal\">")

    path.write_text(page, encoding="utf-8")


# ---------------- 主流程 ----------------

def main():
    ap = argparse.ArgumentParser(description="多源抓取并更新动态页(A/B/C)与 data/news.json")
    ap.add_argument("--full", action="store_true", help="忽略已有数据, 全量重抓")
    ap.add_argument("--limit", type=int, default=0, help="每源本次最多收 N 条新内容(调试)")
    args = ap.parse_args()

    old = {}
    if DATA_FILE.exists() and not args.full:
        for it in json.loads(DATA_FILE.read_text(encoding="utf-8")).get("items", []):
            old[it["url"]] = it

    now = datetime.now().astimezone().isoformat(timespec="seconds")
    items, sources_meta, all_failed = list(old.values()), [], []
    for src in SOURCES:
        try:
            got, failed = ADAPTERS[src["type"]](src, old, args.limit)
            items.extend(got)
            all_failed.extend(failed)
            status = "ok" if not failed else "warn"
        except Exception as e:  # noqa: BLE001 — 单源整体失败不拖垮其它源
            print(f"[警告] {src['id']} 同步失败({e}), 沿用已有数据")
            status = "fail"
        sources_meta.append({
            "id": src["id"], "name": src["name"], "type": src["type"],
            "home": src.get("home", ""), "status": status, "last_sync": now,
            "count": sum(1 for i in items if i["source"] == src["id"]),
        })

    if not items:
        sys.exit("[错误] 没有任何数据, 不写文件")

    valid = {s["id"] for s in SOURCES}
    dropped = [i for i in items if i["source"] not in valid]
    if dropped:
        print(f"[清理] 移除已下线源的历史条目 {len(dropped)} 条({', '.join(sorted({d['source'] for d in dropped}))})")
        items = [i for i in items if i["source"] in valid]

    items.sort(key=lambda x: (x["date"], x["id"]), reverse=True)
    DATA_FILE.parent.mkdir(exist_ok=True)
    DATA_FILE.write_text(
        json.dumps({"generated_by": "build_news.py", "generated_at": now, "count": len(items),
                    "sources": sources_meta, "items": items}, ensure_ascii=False, indent=1),
        encoding="utf-8",
    )
    for spec in PAGES:
        inject_page(spec, items, sources_meta)

    per_src = " | ".join(f"{m['name']}:{m['count']}" for m in sources_meta)
    print(f"[完成] 共 {len(items)} 条({per_src}), 失败 {len(all_failed)} → data/news.json + " + " + ".join(p["file"].name for p in PAGES))
    if all_failed:
        print("  失败清单:\n  " + "\n  ".join(all_failed))


if __name__ == "__main__":
    main()
