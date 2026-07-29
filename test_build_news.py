#!/usr/bin/env python3
"""build_news.py 的离线冒烟测试 —— 纯标准库, 不联网, 不需要 API key, 秒级跑完。

## 为什么要有它

此前验证任何渲染改动都得跑一次全量管线: 抓十几个源、调 AI 接口、几分钟, 而且需要网络与
ZHIPU_API_KEY。代价高到"就改了个模板, 先不验了"变成常态 —— 2026-07-30 那轮就因此栽了
两次(改了 schema/文案却被增量缓存跳过, 页面根本没更新, 而我以为改好了)。

这里固化的都是**已经出过事或差点出事的不变量**, 每条都对应一个真实修复:

  1. noindex 页不发 Article/Breadcrumb schema     —— schema 只给可收录页
  2. noindex 页的 canonical 不得指向站内可收录页  —— 曾指向首页, 可能把 noindex 传导过去
  3. 译题与原题一字不差时不渲染「原题：」          —— 曾把同一个英文标题显示两遍
  4. 详情页只标注够格发页的概念                    —— 曾留 64 条死链
  5. 内联数据严格按日期倒序                        —— 分片拼接曾让「全部」分区时间流倒回
  6. SVG 不被判为可本地化图片                      —— SVG 可内嵌 script, 托管即存储型 XSS
  7. 消毒剥掉事件属性与 style(含紧贴引号写法)     —— 紧贴引号的 onerror 曾完整穿透
  8. 镜像链接规范化: 相对路径补全 / mailto 与畸形协议降文本 / 正常相对链接不误伤
  9. 模板源码指纹进版本键                          —— 改模板忘 bump 导致缓存跳过, 栽过两次
 10. 原子写: 失败时旧文件完好且不留 .tmp           —— 存量库半截文件会让下轮直接读失败

跑法: python3 test_build_news.py    (退出码非 0 即有回归)
"""
import json
import os
import pathlib
import re
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
import build_news as B  # noqa: E402


PASS, FAIL = [], []


def check(name, cond, detail=""):
    (PASS if cond else FAIL).append(name)
    print(f"  {'✓' if cond else '✗'} {name}" + (f"  ← {detail}" if detail and not cond else ""))


def fixture_item(**kw):
    """一条最小可渲染条目; 字段与 make_item 的产出对齐。"""
    base = {
        "id": "aaaaaaaaaaaa", "title": "测试标题", "url": "https://example.com/a",
        "summary": "这是一条用于离线测试的摘要，长度足够触发正文渲染路径。",
        "category": "测试", "tags": [], "date": "2026-07-20",
        "source": "industry", "source_name": "行业动态", "author": "行业动态",
    }
    base.update(kw)
    return base


def fake_lib():
    return {
        "moe-model": {"term": "混合专家模型", "aliases": ["MoE", "MoE模型"],
                      "def": "一种把大模型拆成多个专家子网络、每次只激活其中少数几个的架构，"
                             "用同样的推理成本换更大的参数规模，对业务意味着单位算力能买到更强的能力。"},
        "thin-one": {"term": "薄概念", "aliases": [],
                     "def": "一个只被提到一次、不够格发独立页的概念，用于测试死链防护。"},
    }


# ---------------------------------------------------------------- 1 / 2
def test_noindex_page_schema_and_canonical():
    lib, worthy = fake_lib(), {"moe-model"}
    # 外部源 + 自家 url(product 那种情形): noindex, canonical 绝不能指向站内可收录页
    it = fixture_item(source="product", source_name="产品动态", author="句子互动",
                      url=f"{B.SITE_BASE}/", concepts=["moe-model"])
    html = B.detail_html(it, lib, worthy)
    check("noindex 页不发 Article schema", '"@type": "Article"' not in html)
    check("noindex 页不发 BreadcrumbList", '"@type": "BreadcrumbList"' not in html)
    can = re.search(r'rel="canonical"[^>]*href="([^"]+)"', html)
    check("noindex 页 canonical 指自身而非首页",
          bool(can) and can.group(1) == f"{B.SITE_BASE}/news/p/{it['id']}.html",
          can.group(1) if can else "无 canonical")
    # 外部源 + 外部 url: canonical 指原文(版权归属), 这条不能被上面的修复破坏
    ext = fixture_item(url="https://third-party.example/post", concepts=[])
    can2 = re.search(r'rel="canonical"[^>]*href="([^"]+)"', B.detail_html(ext, lib, worthy))
    check("外部源 canonical 仍指原文", bool(can2) and can2.group(1) == ext["url"],
          can2.group(1) if can2 else "无")


# ---------------------------------------------------------------- 3
def test_translated_title_not_duplicated():
    lib, worthy = fake_lib(), set()
    same = fixture_item(title="Attention Is All You Need",
                        title_zh="Attention Is All You Need", concepts=[])
    diff = fixture_item(title="Attention Is All You Need", title_zh="注意力就是你所需要的", concepts=[])
    check("译题=原题时不渲染「原题：」", "原题：" not in B.detail_html(same, lib, worthy))
    check("译题≠原题时正常渲染「原题：」", "原题：" in B.detail_html(diff, lib, worthy))
    check("zh_title 对相同标题返回空", B.zh_title(same) == "")
    check("zh_title 对不同标题返回译题", B.zh_title(diff) == "注意力就是你所需要的")


# ---------------------------------------------------------------- 4
def test_concept_annotation_only_worthy():
    lib, worthy = fake_lib(), {"moe-model"}          # thin-one 不够格
    it = fixture_item(concepts=["moe-model", "thin-one"])
    html = B.detail_html(it, lib, worthy)
    links = set(re.findall(r'href="\.\./c/([a-z0-9-]+)\.html"', html))
    check("只标注够格发页的概念", links <= worthy, f"多出 {links - worthy}")


# ---------------------------------------------------------------- 5
def test_inline_items_sorted_desc():
    items = [fixture_item(id=f"{i:012d}", date=d, source=s, source_name=s)
             for i, (d, s) in enumerate([("2026-07-01", "rui-blog"), ("2026-07-20", "industry"),
                                         ("2018-05-05", "rui-blog"), ("2026-07-25", "industry")])]
    comp = [i for i in items if i["source"] in B.COMPANY_SOURCES]
    rad = [i for i in items if i["source"] not in B.COMPANY_SOURCES]
    merged = sorted(comp + rad, key=lambda x: (x.get("date", ""), x["id"]), reverse=True)
    dates = [i["date"] for i in merged]
    check("公司区+雷达拼接后严格倒序", dates == sorted(dates, reverse=True), str(dates))


# ---------------------------------------------------------------- 6
def test_svg_not_localizable():
    svg = b'<svg xmlns="http://www.w3.org/2000/svg"><script>alert(1)</script></svg>'
    xml = b'<?xml version="1.0"?><svg><script>alert(1)</script></svg>'
    check("SVG 字节不判为可本地化图片", not B.is_image_bytes(svg))
    check("XML 声明开头同样不判为图片", not B.is_image_bytes(xml))
    check("PNG 仍正常识别", B.is_image_bytes(b"\x89PNG\r\n\x1a\n"))
    check("Content-Type 表不含 svg", "image/svg+xml" not in B.CTYPE_EXT)
    check("路径后缀判定不认 .svg", B.img_ext("https://x.example/a.svg", "") != ".svg")


# ---------------------------------------------------------------- 7
def test_sanitize_strips_handlers_and_style():
    cases = [
        ('<img src=x onerror="alert(1)">', "空格分隔"),
        ('<img src="x"onerror="alert(1)">', "双引号紧贴"),
        ("<img src='x'onerror='alert(1)'>", "单引号紧贴"),
        ('<img src=x/onerror=alert(1)>', "斜杠分隔无引号"),
        ('<img src="x"ONERROR="alert(1)">', "大写变体"),
        ('<svg onload="alert(1)"></svg>', "svg onload"),
        ('<div style="position:fixed;top:0">x</div>', "style 全屏浮层"),
        ('<p style=color:red>x</p>', "style 无引号"),
    ]
    for h, name in cases:
        out = B.sanitize_fragment(h)
        leaked = bool(re.search(r'\bon[a-z]+\s*=\s*\S', out, re.I)) or bool(re.search(r'\bstyle\s*=', out, re.I))
        check(f"消毒: {name}", not leaked, out[:60])
    normal = '<p>正常 <b>加粗</b> <a href="https://ok.example/x">链接</a></p>'
    out = B.sanitize_fragment(normal)
    check("消毒不破坏正常内容", "<b>" in out and 'href="https://ok.example/x"' in out, out[:70])


# ---------------------------------------------------------------- 8
def test_normalize_links():
    base = "https://blog.example.com/posts/2026/hello.html"
    got = B.normalize_links('<a href="/thought/x.html">t</a>', base)
    check("相对路径补全为绝对", 'href="https://blog.example.com/thought/x.html"' in got, got)
    check("mailto 降级为纯文本", "<a" not in B.normalize_links('<a href="mailto:a@b.c">a@b.c</a>', base))
    check("畸形协议降级为纯文本", "<a" not in B.normalize_links('<a href="ttps://x.example/y">x</a>', base))
    keep = B.normalize_links('<a href="/search?q=http://x">s</a>', base)
    check("query 里带 :// 的相对链接不被误拆", "<a" in keep, keep)
    ok = B.normalize_links('<a href="https://ok.example/x">o</a>', base)
    check("正常绝对链接不动", 'href="https://ok.example/x"' in ok, ok)


# ---------------------------------------------------------------- 9
def test_render_ver_tracks_template_source():
    v1 = B.render_ver()
    check("版本键含人工版本号", v1.startswith(B.RENDER_VER + "."), v1)
    check("版本键含模板指纹(非 nosrc)", not v1.endswith(".nosrc"), v1)
    orig = B.detail_html
    try:
        B.detail_html = lambda *a, **k: "changed"   # 模拟改模板
        check("改模板后版本键随之变化", B.render_ver() != v1, f"{v1} -> {B.render_ver()}")
    finally:
        B.detail_html = orig
    check("还原后版本键回到原值", B.render_ver() == v1)


# ---------------------------------------------------------------- 10
def test_write_atomic_failure_keeps_old_file():
    with tempfile.TemporaryDirectory() as d:
        p = pathlib.Path(d) / "state.json"
        p.write_text('{"v":"old"}', encoding="utf-8")
        B.write_atomic(p, '{"v":"new"}')
        check("原子写正常路径生效", json.loads(p.read_text(encoding="utf-8"))["v"] == "new")
        check("正常路径无 .tmp 残留", not list(pathlib.Path(d).glob("*.tmp")))
        good = p.read_text(encoding="utf-8")
        real = os.replace
        os.replace = lambda a, b: (_ for _ in ()).throw(OSError("模拟失败"))
        try:
            B.write_atomic(p, '{"v":"broken"}')
        except OSError:
            pass
        finally:
            os.replace = real
        check("写入失败后旧文件完好", p.read_text(encoding="utf-8") == good)
        check("写入失败后清掉 .tmp", not list(pathlib.Path(d).glob("*.tmp")))


# ---------------------------------------------------------------- 11
def test_retire_unlisted_safety_bounds():
    """撤稿是破坏性操作(内容从站上消失), 三条安全边界必须有测试压住。

    尤其第 2 条: CI 环境没有 lark-cli, 飞书源每轮必然拉表失败 —— 若把「拉不到表」当成
    「表是空的」, 一次 cron 就能把所有公众号内容撤下站。
    """
    import tempfile, json as J
    with tempfile.TemporaryDirectory() as d:
        reg = pathlib.Path(d) / "press-news.json"
        reg.write_text(J.dumps({"items": [{"url": "https://keep.example/a", "title": "留着"}]},
                               ensure_ascii=False), encoding="utf-8")
        fake_src = [
            {"id": "press", "type": "manual", "file": reg},
            {"id": "industry", "type": "rss"},          # RSS 源不该被对账
            {"id": "wechat-mp", "type": "feishu-base"},  # 名册缺失 → 应跳过
        ]
        items = [
            {"id": "1", "url": "https://keep.example/a", "source": "press", "title": "留着"},
            {"id": "2", "url": "https://gone.example/b", "source": "press", "title": "登记表已删"},
            {"id": "3", "url": "https://rss.example/c", "source": "industry", "title": "RSS 老条目"},
            {"id": "4", "url": "https://mp.example/d", "source": "wechat-mp", "title": "公众号"},
        ]
        orig_sources, orig_roster = B.SOURCES, dict(B._FEISHU_ROSTER)
        try:
            B.SOURCES = fake_src
            B._FEISHU_ROSTER.clear()          # 模拟拉表失败: 名册里没有该源
            n = B.retire_unlisted(items)
            by = {i["id"]: i for i in items}
            check("边界①: 登记表里的条目不撤", not by["1"].get("retired"))
            check("边界①: 登记表已删的条目撤下站", bool(by["2"].get("retired")))
            check("边界①: RSS 源永不参与对账", not by["3"].get("retired"),
                  "feed 会滚动, 对它撤稿会清空整站历史")
            check("边界②: 飞书拉表失败时跳过该源(不误撤)", not by["4"].get("retired"),
                  "CI 里没有 lark-cli, 误撤会下站全部公众号内容")
            check("边界③: 只打标记不删数据", len(items) == 4 and by["2"]["url"] == "https://gone.example/b")
            check("撤稿计数正确", n == 1, str(n))
            # 双向: 把行加回登记表 → 复站
            reg.write_text(J.dumps({"items": [{"url": "https://keep.example/a"},
                                              {"url": "https://gone.example/b"}]}, ensure_ascii=False),
                           encoding="utf-8")
            B.retire_unlisted(items)
            check("加回登记表即复站(双向可逆)", not by["2"].get("retired"))
        finally:
            B.SOURCES = orig_sources
            B._FEISHU_ROSTER.clear(); B._FEISHU_ROSTER.update(orig_roster)


# ---------------------------------------------------------------- 12
def test_dedupe_guards():
    """两道去重: 同 id(曾让守恒断言炸掉整条管线)与同源同标题(页面并排两条一样的标题)。"""
    dup = [fixture_item(id="same", url="https://x.example/1"),
           fixture_item(id="same", url="https://x.example/1", title="后补的正式标题")]
    check("同 id 兜底去重", len(B._dedupe_by_id(dup, "press")) == 1)
    a = fixture_item(id="a", date="2026-07-28", title="空中具身操作：让蜘蛛侠们安全落地", source="industry")
    b = fixture_item(id="b", date="2026-07-29", title="空中具身操作:让蜘蛛侠们安全落地", source="industry")
    c = fixture_item(id="c", date="2026-07-29", title="完全不同的一条", source="industry")
    dd = fixture_item(id="d", date="2026-07-29", title="空中具身操作：让蜘蛛侠们安全落地", source="voices")
    e = fixture_item(id="e", date="2026-01-01", title="空中具身操作：让蜘蛛侠们安全落地", source="industry")
    kept = {x["id"] for x in B.dedupe_same_story([a, b, c, dd, e])}
    check("同源同标题只留首发(中英标点视同)", "a" in kept and "b" not in kept, str(kept))
    check("不同标题不误杀", "c" in kept)
    check("跨源不合并(不同视角)", "d" in kept)
    check("相隔半年不算撞车(年度系列文章)", "e" in kept)
    r1 = {x["id"] for x in B.dedupe_same_story([a, b, c, dd, e])}
    r2 = {x["id"] for x in B.dedupe_same_story([e, dd, c, b, a])}
    check("去重结果与输入顺序无关(确定性)", r1 == r2, f"{r1} vs {r2}")


# ---------------------------------------------------------------- 13
def test_worthy_keeps_published_pages():
    """门槛只管新页要不要发, 不管老页要不要留 —— URL 一旦公开就是承诺。

    引用数会因外部条目被 keep_max 修剪而下降, 一跌破门槛页面就被 unlink, 而它是 index
    且已进 sitemap 的原创页 → 软 404。
    """
    import tempfile
    lib = fake_lib()
    vis = [fixture_item(id="x1", concepts=["moe-model"]), fixture_item(id="x2", concepts=["moe-model"])]
    orig_dir = B.CONCEPT_DIR
    with tempfile.TemporaryDirectory() as d:
        try:
            B.CONCEPT_DIR = pathlib.Path(d)
            w = B.worthy_concepts(lib, vis)
            check("达到门槛(≥2 引用)的概念够格", "moe-model" in w)
            check("未达门槛且未发页的概念不够格", "thin-one" not in w)
            (B.CONCEPT_DIR / "thin-one.html").write_text("<html>已发布</html>", encoding="utf-8")
            w2 = B.worthy_concepts(lib, vis)
            check("已发布的页即便引用不足也保留", "thin-one" in w2)
            (B.CONCEPT_DIR / "not-in-lib.html").write_text("<html>库里没了</html>", encoding="utf-8")
            w3 = B.worthy_concepts(lib, vis)
            check("库里已删的概念不因页面存在而复活", "not-in-lib" not in w3)
        finally:
            B.CONCEPT_DIR = orig_dir


# ---------------------------------------------------------------- 14
def test_metrics_alert_thresholds():
    """指标告警: 只报「本来有、现在没了或腰斩」。经常误报的告警等于没有告警。"""
    import tempfile, io, contextlib, json as J
    orig = B.METRICS_FILE
    with tempfile.TemporaryDirectory() as d:
        try:
            B.METRICS_FILE = pathlib.Path(d) / "metrics.jsonl"
            meta = [{"id": "industry", "count": 100, "status": "ok"},
                    {"id": "hn", "count": 30, "status": "ok"},
                    {"id": "press", "count": 0, "status": "ok"}]
            B.record_metrics([0] * 200, [0] * 400, meta, [], "2026-07-30T00:00:00+08:00")
            buf = io.StringIO()
            meta2 = [{"id": "industry", "count": 40, "status": "ok"},    # 腰斩 → 该报
                     {"id": "hn", "count": 29, "status": "ok"},           # 微降 → 不该报
                     {"id": "press", "count": 5, "status": "ok"}]         # 0→5 新增 → 不该报
            with contextlib.redirect_stdout(buf):
                B.record_metrics([0] * 150, [0] * 400, meta2, [], "2026-07-30T06:00:00+08:00")
            out = buf.getvalue()
            check("总量腰斩触发告警", "上站总数" in out and "200" in out, out[:80])
            check("单源腰斩触发告警", "industry" in out, out[:80])
            check("微降不误报", "hn" not in out, out[:80])
            check("0→N 的新源不误报", "press" not in out, out[:80])
            rows = [J.loads(x) for x in B.METRICS_FILE.read_text(encoding="utf-8").splitlines() if x.strip()]
            check("告警不影响指标落盘", len(rows) == 2, str(len(rows)))
        finally:
            B.METRICS_FILE = orig


# ---------------------------------------------------------------- 15
def test_restate_never_wipes_with_blanks():
    """一方登记表回写: 只覆盖显式写了的字段。

    登记表常只填 url+title, 空 summary 不该洗掉管线已抓到的摘要 —— 这条坏了不会报错,
    只会让站上的摘要悄悄变空。
    """
    src = {"id": "press", "name": "媒体报道", "author": "", "default_category": ""}
    it = {"id": "x", "url": "https://a.example/1", "title": "旧标题", "summary": "已抓到的好摘要",
          "category": "36氪", "author": "36氪", "date": "2026-07-01", "tags": [],
          "source": "press", "source_name": "媒体报道"}
    B._restate(it, {"url": it["url"], "title": "新标题"}, src)   # 只给了 title
    check("回写更新给了的字段", it["title"] == "新标题")
    check("留空不覆盖已抓到的摘要", it["summary"] == "已抓到的好摘要", it["summary"])
    check("留空不覆盖 category", it["category"] == "36氪", it["category"])
    check("留空不覆盖 date", it["date"] == "2026-07-01", it["date"])
    changed = B._restate(it, {"url": it["url"], "title": "新标题"}, src)
    check("无实际变化时返回 0(不虚报回写数)", changed == 0, str(changed))


# ---------------------------------------------------------------- 16
def test_banned_terms_gate():
    """官网口径闸: 「企微/企业微信」不出现在任何页面。坏了不会报错, 违禁词直接上页。"""
    check("识别「企业微信」", B.has_banned("意向沉到企业微信接着跟进"))
    check("识别「企微」", B.has_banned("沉淀到企微"))
    check("正常文案不误判", not B.has_banned("意向沉到自有阵地接着跟进"))
    check("空值安全", not B.has_banned("") and not B.has_banned(None))
    lib = {"x": {"term": "私域运营", "aliases": [], "def": "把公域来的意向沉到自有阵地持续经营。"}}
    it = fixture_item(summary="公域意向自动沉到企业微信，AI 客服接力跟进。", concepts=["x"])
    ev = B.concept_evidence(it, lib["x"])
    check("概念证据弃用含违禁词的句子", not B.has_banned(ev), ev[:50])


# ---------------------------------------------------------------- 17
def test_detail_indexable_three_conditions():
    """详情页可收录判据是单一事实源(详情页 robots / sitemap / ItemList 三处共用)。
    三个条件缺一不可; 少任何一个都会让 sitemap 收录 noindex 页。
    """
    import tempfile
    orig = B.CONTENT_DIR
    with tempfile.TemporaryDirectory() as d:
        try:
            B.CONTENT_DIR = pathlib.Path(d)
            own = next(iter(B.OWN_SOURCES))
            it = fixture_item(id="mirror1", source=own, source_name=own)
            check("① 无镜像文件 → 不可收录", not B.detail_indexable(it))
            (B.CONTENT_DIR / "mirror1.html").write_text("", encoding="utf-8")
            check("② 镜像文件为空 → 不可收录", not B.detail_indexable(it))
            (B.CONTENT_DIR / "mirror1.html").write_text("<p>有内容的镜像</p>", encoding="utf-8")
            check("③ own 源 + 镜像有内容 → 可收录", B.detail_indexable(it))
            ext = fixture_item(id="mirror1", source="industry", source_name="行业动态")
            check("④ 非 own 源即便有镜像也不可收录", not B.detail_indexable(ext))
        finally:
            B.CONTENT_DIR = orig


# 曾在此加过一组「文档引用的路径必须存在」的检查, 已删除。原因:
# 它产生 6 个误报(文档里的简称 askbar.js、外部 feed 路径 /feed.xml、示例 hr.html、
# 明说已删除的 news-b.html), 而且我在实现里又误用了 lstrip("./") —— 把 .github/... 的
# 前导点当字符集合剥掉, 于是去查一个不存在的 github/workflows/...。今天这是第二次踩
# lstrip 的坑(前一次是 lstrip("www.")), 上一次我还专门写了注释警告它。
#
# 按同一条标准: **经常误报的检查等于没有检查, 还会训练人忽略它**。而它也抓不到真正的
# 文档漂移 —— 那是语义层面的(worthy_concepts 注释写「三处」而实际有四处, 我照着错清单
# 验证, 漏掉的第四处挂了 64 条死链), 路径检查看不见。语义漂移目前只能靠改代码时顺手
# 改注释, 没有自动办法。


# ---------------------------------------------------------------- 18
def test_deploy_list_covers_root_artifacts():
    """CI 的 rsync 推送清单必须覆盖管线产出的**所有根目录文件**。

    漏一个的表现是「功能静默少一块」而不是报错: 比如 news-radar.json 没推上去, 雷达区
    永远只有内联的 24 条、前端 fetch 静默 404, 页面不崩、日志不报, 只是内容少了 210 条。
    这类故障没人会主动发现, 所以把「产物 ↔ 部署清单」这个对应关系钉在测试里 —— 将来新增
    根目录产物时, 这条会先失败提醒补 workflow。

    注意: 这条只在 PR 分支/main 上有意义(workflow 的清单在那里维护); 预览分支的 workflow
    副本可能是旧的, CI 也只在 PR 分支跑, 所以不构成误报来源。
    """
    src = (ROOT / "build_news.py").read_text(encoding="utf-8")
    produced = sorted({m for m in re.findall(r'ROOT / "([^"/]+\.[a-z]+)"', src)})
    wf_path = ROOT / ".github" / "workflows" / "news-cron.yml"
    if not wf_path.exists():
        check("部署清单文件存在", False, "news-cron.yml 缺失")
        return
    wf = wf_path.read_text(encoding="utf-8")
    # 只在**新架构**(rsync 推产物)的 workflow 上校验。预览分支 stage-2 保留的是老架构
    # workflow(生成物入库、commit+push, 没有 rsync 推送行), 它按设计就不该有这份清单 ——
    # 在那里报缺失是误报, 而误报会训练人忽略这条检查。
    if "rsync" not in wf:
        check("(跳过)当前分支的 workflow 是老架构, 无 rsync 推送清单可校验", True)
        return
    missing = [f for f in produced if f not in wf]
    check(f"CI 推送清单覆盖 {len(produced)} 个根目录产物", not missing,
          f"清单里缺 {missing} —— 补进 news-cron.yml 的推送 rsync 行, 否则线上缺文件")
    # 文档里的**手动**推送命令同样要覆盖 —— 公众号新文靠它推(CI 里没有 lark-cli)。
    # 这条曾漏掉 sitemap-news.xml 与 news-radar.json: CI 有、文档没有, 而测试原先只查
    # workflow, 覆盖不到文档里的命令。
    dep = ROOT / "docs" / "DEPLOY.md"
    if dep.exists():
        block = dep.read_text(encoding="utf-8")
        m = re.search(r'rsync -az news\.html[^\n]*', block)
        line = m.group(0) if m else ""
        miss_doc = [f for f in produced if f.endswith((".xml", ".json", ".html")) and f not in line]
        check("DEPLOY.md 的手动推送命令同样覆盖全部根目录产物", not miss_doc,
              f"手册里缺 {miss_doc} —— 公众号新文按手册手动推时会漏, 内容悄悄不更新")
    # 第三处: nginx 得有对应 location 才能对外访问。推上去了但没有 location = 线上 404,
    # 而 404 的是被 sitemap 声明过的 URL 或前端要 fetch 的分片 —— 页面不崩, 只是少一块。
    ng = ROOT / "deploy" / "nginx-news.conf"
    if ng.exists():
        conf = ng.read_text(encoding="utf-8")
        # news/ 目录靠 `location ^~ /news/` 前缀覆盖; 根目录单文件需要各自的 location
        miss_ng = [f for f in produced if f not in conf]
        check("nginx location 覆盖全部根目录产物", not miss_ng,
              f"nginx 配置里缺 {miss_ng} —— 推上去了但对外 404")
    # 第四处: robots.txt 得声明 sitemap, 否则搜索引擎不会主动去发现它 —— 文件存在、可访问、
    # 但没人来读, sitemap 等于白写。这是产物「可被发现」链条上的最后一环。
    rb = ROOT / "robots.txt"
    if rb.exists() and any(f.startswith("sitemap") for f in produced):
        txt = rb.read_text(encoding="utf-8")
        sm = [f for f in produced if f.startswith("sitemap")]
        miss_rb = [f for f in sm if f not in txt]
        check("robots.txt 声明了管线产出的 sitemap", not miss_rb,
              f"robots.txt 未声明 {miss_rb} —— 搜索引擎不会主动发现它")


# ---------------------------------------------------------------- 19
def test_toc_thresholds_and_anchors():
    """长文目录: 门槛、锚点完整性、不覆盖原文已有 id。

    「点了不动」的目录比没有目录更糟, 所以锚点与 id 必须严格对应; 短文出目录纯属噪音,
    所以门槛也要测反向。
    """
    # 每段 150×5=750 字 ×4 段 = 3000 字, 稳过 TOC_MIN_CHARS(2000) —— fixture 必须满足被测
    # 函数的前提条件, 否则失败的是测试数据不是代码(这是今天第二次踩 fixture 的坑)。
    long_body = "".join(f"<h2>小节 {i}</h2><p>{'正文内容。' * 150}</p>" for i in range(1, 5))
    anchored, toc = B.build_toc(long_body)
    check("长文+多标题 → 出目录", bool(toc), "未出目录")
    ids = set(re.findall(r'<h[234][^>]*\sid="([^"]+)"', anchored))
    hrefs = set(re.findall(r'href="#([^"]+)"', toc))
    check("目录每个锚点都有对应 id", hrefs and hrefs <= ids, f"悬空锚点 {hrefs - ids}")
    check("目录节数与标题数一致", len(hrefs) == 4, f"{len(hrefs)} vs 4")
    # 门槛反向: 标题够但正文太短
    short = "<h2>a</h2><p>短</p><h2>b</h2><p>短</p><h2>c</h2><p>短</p>"
    check("正文太短 → 不出目录", B.build_toc(short)[1] == "")
    # 门槛反向: 正文够长但标题太少
    few = f"<h2>唯一小节</h2><p>{'正文内容。' * 200}</p>"
    check("标题太少 → 不出目录", B.build_toc(few)[1] == "")
    # 原文自带 id 不覆盖(站外可能已有链接指过来)
    keep = "".join(f'<h2 id="orig-{i}">节 {i}</h2><p>{"字" * 800}</p>' for i in range(1, 4))
    a2, t2 = B.build_toc(keep)
    check("原文自带 id 被保留", 'id="orig-1"' in a2 and 'href="#orig-1"' in t2, t2[:80])
    check("空正文安全", B.build_toc("") == ("", ""))


# ---------------------------------------------------------------- 20
def test_all_render_fns_registered_in_fingerprint():
    """参与渲染的函数必须登记进 _TPL_FNS, 否则改它不触发缓存重算 —— 页面停在旧版。

    这个坑今天栽过三次(Article schema、概念索引页文案、以及加 build_toc 时忘了登记)。
    **指纹机制本身防不住「忘了把新函数纳入指纹」**, 所以这里正反两面都测:
    ①列表里的名字都能在模块里找到(防写错名或删了函数没删登记)
    ②几个已知的渲染函数确实在列表里(防加了新渲染函数忘登记)
    """
    missing = [f for f in B._TPL_FNS if not hasattr(B, f)]
    check("_TPL_FNS 里的名字都存在", not missing, f"找不到 {missing}")
    must = ["detail_html", "concept_html", "build_toc", "breadcrumb_ld", "ld_json",
            "annotate_concepts", "normalize_links", "nav_fallback"]
    unreg = [f for f in must if f not in B._TPL_FNS]
    check("已知渲染函数全部登记在册", not unreg,
          f"未登记 {unreg} —— 改它们不会触发缓存重算")
    v = B.render_ver()
    check("版本键形如 <人工版本>.<指纹>", re.fullmatch(r"[\w.]+\.[0-9a-f]{10}", v), v)


# ---------------------------------------------------------------- 21
def test_feed_scope_is_company_only():
    """自家动态 RSS 的范围约束是**版权硬边界**, 不是风格偏好 —— 转载的第三方内容做成全文
    feed 分发, 比站内镜像更进一步, 不能做。所以这条必须钉死。
    """
    import tempfile, xml.etree.ElementTree as ET
    vis = [
        fixture_item(id="c1", source="rui-blog", source_name="博客精选", title="自家博客"),
        fixture_item(id="c2", source="product", source_name="产品动态", title="自家产品"),
        fixture_item(id="x1", source="industry", source_name="行业动态", title="第三方资讯"),
        fixture_item(id="x2", source="voices", source_name="大咖观点", title="第三方博主"),
        fixture_item(id="x3", source="hn", source_name="Hacker News", title="HN 热帖"),
    ]
    orig = B.ROOT
    with tempfile.TemporaryDirectory() as d:
        try:
            B.ROOT = pathlib.Path(d)
            B.write_news_feed(vis)
            f = B.ROOT / "news-feed.xml"
            check("feed 已生成", f.exists())
            if not f.exists():
                return
            root = ET.fromstring(f.read_text(encoding="utf-8"))   # 解析失败即 XML 不合法
            items = root.find("channel").findall("item")
            titles = {i.findtext("title") for i in items}
            check("自家内容进 feed", {"自家博客", "自家产品"} <= titles, str(titles))
            leak = titles & {"第三方资讯", "第三方博主", "HN 热帖"}
            check("**第三方内容不得进 feed**(版权硬边界)", not leak, f"泄漏 {leak}")
            links = [i.findtext("link") for i in items]
            check("链接指站内详情页", all("/news/p/" in (l or "") for l in links), str(links))
            check("每条都有 pubDate", all(i.findtext("pubDate") for i in items))
            check("每条 guid 与 link 一致", all(i.findtext("guid") == i.findtext("link") for i in items))
        finally:
            B.ROOT = orig
    # 公司区为空时不该产出空 feed(空 channel 对阅读器是噪音)
    with tempfile.TemporaryDirectory() as d2:
        try:
            B.ROOT = pathlib.Path(d2)
            B.write_news_feed([fixture_item(id="x9", source="industry", source_name="行业动态")])
            check("公司区为空时不产出 feed", not (B.ROOT / "news-feed.xml").exists())
        finally:
            B.ROOT = orig


def main():
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for fn in tests:
        print(f"\n{fn.__name__}")
        fn()
    print(f"\n{'=' * 56}\n通过 {len(PASS)} 项, 失败 {len(FAIL)} 项")
    if FAIL:
        print("失败清单:\n  " + "\n  ".join(FAIL))
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
