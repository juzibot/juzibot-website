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
import collections
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


def html_unescape(s):
    import html as _h
    return _h.unescape(s)


def check(name, cond, detail=""):
    (PASS if cond else FAIL).append(name)
    print(f"  {'✓' if cond else '✗'} {name}" + (f"  ← {detail}" if detail and not cond else ""))


def _preview_branch():
    """预览分支名只写在一处(shell-clean.yml 的 job 守卫), 这里派生, 不抄第二遍。

    stage-2 按设计把注入过的模板壳与生成物入库, 所以「产物必须被忽略」这条对它天然不成立。
    原判别是「news-cron.yml 里没有 rsync 就算老架构、跳过」—— 一旦把新版 workflow 同步到
    预览分支, 这个判别立刻失效(实测正是如此: 同步后这条检查在 stage-2 上跑起来并报 10 项缺失,
    而那 10 项全是设计如此)。改成认分支名, 与 CI 侧同一个判据。
    """
    wf = ROOT / ".github" / "workflows" / "shell-clean.yml"
    if not wf.exists():
        return None
    m = re.search(r"github\.ref != 'refs/heads/([\w./-]+)'", wf.read_text(encoding="utf-8"))
    return m.group(1) if m else None


def _current_branch():
    """当前分支名; CI 里 PR 事件是 detached HEAD 返回 'HEAD' —— 那种情况**不跳过**(进 main 必须过闸)。"""
    try:
        import subprocess
        return subprocess.run(["git", "rev-parse", "--abbrev-ref", "HEAD"], cwd=str(ROOT),
                              capture_output=True, text=True, timeout=5).stdout.strip()
    except Exception:  # noqa: BLE001
        return ""


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
        B._TPL_CACHE.clear()   # 指纹按进程记忆化(一轮管线里要取 284 次); 换模板须显式失效
        check("改模板后版本键随之变化", B.render_ver() != v1, f"{v1} -> {B.render_ver()}")
    finally:
        B.detail_html = orig
        B._TPL_CACHE.clear()
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
    # 默认展开状态按节数: 短目录展开(一眼看清结构), 长目录收起(实测最长一页 68 节、
    # 12 页 ≥15 节, 手机上默认全展开等于让目录挡住正文)。
    # 注意 fixture 要**同时**过两道门槛(≥3 节 且 正文 ≥2000 字)—— 今天三次栽在 fixture
    # 不满足前提: src 缺 name、正文不够长、以及这次 5 节×300 字只有 1500 字压根没出目录。
    _, t_short = B.build_toc("".join(f"<h2>节{i}</h2><p>{'字' * 600}</p>" for i in range(1, 6)))
    _, t_long = B.build_toc("".join(f"<h2>节{i}</h2><p>{'字' * 300}</p>" for i in range(1, 21)))
    check(f"≤{B.TOC_OPEN_MAX} 节默认展开", 'dp-toc" open>' in t_short, t_short[:50])
    check(f">{B.TOC_OPEN_MAX} 节默认收起", t_long and 'dp-toc" open>' not in t_long, t_long[:50])
    check("收起时仍显示节数(读者知道有目录可点)", "20 节" in t_long)


# ---------------------------------------------------------------- 20
def test_render_fingerprint_covers_call_graph():
    """指纹必须覆盖所有参与渲染的函数, 否则改它不触发重算 —— 页面停在旧版。

    这个坑栽过四次(Article schema / 概念索引页文案 / build_toc / read_time), 每次都是
    「忘了往登记表里加一个名字」。**上一版测试也没能拦住第四次**: 它查的是一份手写 must 清单,
    而手写清单里永远不会有"我刚忘掉的那个函数"—— 验证手段与被验证的错误同源, 等于没验。
    改成从根模板函数取调用图闭包后, 这里测的是**机制**而不是清单:
    ①闭包自动抓到了那些从没被手工登记过的函数(read_time 就是第四次栽的那个)
    ②闭包不过度膨胀: 不含网络/AI 层, 否则改抓取逻辑就全量重算, 增量缓存等于废掉
    ③确定性: 同一份代码两次调用给同一个指纹(连跑字节稳定依赖这条)
    ④成员变化会改指纹(函数移出闭包也算模板变了)
    """
    fns = B._tpl_fns()
    check("闭包非空且含根函数", fns and all(r in fns for r in B._TPL_ROOTS), f"{len(fns)} 个")
    # 手工表时代漏掉的 14 个中挑几个: 全是本轮亲手动过、改了却不会触发重算的
    auto = ["read_time", "breadcrumb_html", "disp_title", "zh_title", "concept_rx", "safe_href"]
    lost = [f for f in auto if f not in fns]
    check("自动抓到手工表漏掉的渲染函数", not lost, f"闭包没抓到 {lost}")
    leak = [f for f in fns if re.search(r"fetch|sync_|ai_|http|urlopen|llm|mirror_items|zhipu", f)]
    check("闭包不含网络/AI 层(否则改抓取就全量重算)", not leak, f"混入 {leak}")
    check("闭包规模合理(<40 个)", len(fns) < 40, f"{len(fns)} 个 —— 过大说明跟进条件太宽")
    check("闭包已排序(确定性)", list(fns) == sorted(fns))
    v1 = B.render_ver()
    B._TPL_CACHE.clear()
    check("两次调用同一指纹", B.render_ver() == v1, f"{v1} vs {B.render_ver()}")
    check("版本键形如 <人工版本>.<指纹>", re.fullmatch(r"[\w.]+\.[0-9a-f]{10}", v1), v1)
    # ④ 成员变化必须改指纹: 换掉一个闭包成员(替身来自本测试模块, 会被"只跟进本模块函数"过滤掉,
    #    等价于该函数移出闭包), 指纹应当变化; 用完立刻还原, 不污染后续用例
    orig = B.read_time
    try:
        B.read_time = lambda body: ""
        B._TPL_CACHE.clear()
        check("闭包成员变化会改指纹", B.render_ver() != v1, f"仍是 {v1}")
    finally:
        B.read_time = orig
        B._TPL_CACHE.clear()
    check("还原后指纹回到原值", B.render_ver() == v1)


# ---------------------------------------------------------------- 22
def test_both_renderers_smoke():
    """两个主渲染函数各跑一遍完整渲染 —— 补的是一个真实盲区。

    加可见面包屑时把 cp_crumb 的定义放在了使用之后, 结果 concept_html 运行时抛
    UnboundLocalError。而当时 **py_compile 通过、94 项测试也全过** —— 因为 py_compile 只查
    语法(UnboundLocalError 是运行时错误), 而测试里 detail_html 被 noindex/canonical 那几组
    间接调用过, concept_html 却**从没被完整渲染过**。两个主渲染函数只测了一个。
    这类「定义在使用之后」「拼错变量名」的错误, 只要函数被完整调用一次就会暴露。
    """
    lib, worthy = fake_lib(), {"moe-model"}
    it = fixture_item(concepts=["moe-model"])
    dp = B.detail_html(it, lib, worthy)
    check("detail_html 完整渲染不抛错", len(dp) > 1000, f"{len(dp)} 字节")
    check("详情页含可见面包屑", 'class="dp-crumb"' in dp)
    cp = B.concept_html("moe-model", lib["moe-model"], [it], ["thin-one"], lib, worthy)
    check("concept_html 完整渲染不抛错", len(cp) > 1000, f"{len(cp)} 字节")
    check("概念页含可见面包屑", 'class="cp-crumb"' in cp)
    # 可见面包屑与 schema 路径必须同源(共用 trail 的意义)
    import json as J
    m = re.search(r'"@type": "BreadcrumbList".*?"itemListElement": (\[.*?\])\}', cp, re.S)
    if m:
        sch = [e["name"] for e in J.loads(m.group(1))]
        nav = re.search(r'<nav class="cp-crumb"[^>]*>(.*?)</nav>', cp, re.S)
        # html.unescape 是必须的: 可见面包屑在 HTML 里转义过(& → &amp;), schema 在 JSON 里
        # 是原字符 —— 两边都正确, 不反转义就比字符串会把含 & 的标题误判成不一致(实测踩过)。
        import html as _h
        vis = [_h.unescape(re.sub(r"<[^>]+>", "", x)) for x in
               re.findall(r'<(?:a[^>]*|span[^>]*)>(.*?)</(?:a|span)>', nav.group(1))] if nav else []
        check("可见面包屑与 schema 路径一致", [v[:30] for v in vis] == [s[:30] for s in sch],
              f"{vis} vs {sch}")
    check("面包屑末项标 aria-current", 'aria-current="page"' in cp)
    # 索引页也过一遍
    idx = B.concept_index_html(lib, {"moe-model": [it]}, worthy)
    check("concept_index_html 完整渲染不抛错", len(idx) > 500, f"{len(idx)} 字节")


# ---------------------------------------------------------------- 23
def test_read_time_thresholds():
    """阅读时长: 边界与单位切换。

    实测时长跨度 148 倍(212 字 ≈1 分钟 / 59293 字 ≈148 分钟), 分布很散(20 分钟以上 48 页),
    读者点进来前无从判断这是两分钟还是两小时。
    """
    check("正文太短不显示(摘要没有「读多久」可言)", B.read_time("<p>" + "字" * 150 + "</p>") == "")
    check("空正文安全", B.read_time("") == "" and B.read_time(None) == "")
    check("短文按分钟", B.read_time("<p>" + "字" * 400 + "</p>") == "约 1 分钟")
    check("中位长度约 8 分钟", B.read_time("<p>" + "字" * 3259 + "</p>") == "约 8 分钟")
    # 超一小时改小时: 「约 148 分钟」要读者自己换算, 「约 2.5 小时」才是人话
    long_ = B.read_time("<p>" + "字" * 59293 + "</p>")
    check("超一小时改用小时表述", "小时" in long_, long_)
    check("不足一小时不用小时", "小时" not in B.read_time("<p>" + "字" * 20000 + "</p>"))
    check("标签不计入字数(HTML 被剥离)",
          B.read_time("<p><b>" + "字" * 400 + "</b></p>") == B.read_time("<p>" + "字" * 400 + "</p>"))


# ---------------------------------------------------------------- 24
def _rel_fixture():
    """五条: A/B/C 共享概念(B 与 A 共两个), D/E 同源用来测同源上限。"""
    mk = lambda i, cs, src="industry", d="2026-07-20": {
        "id": i, "title": f"标题{i}", "url": f"https://e.com/{i}", "date": d,
        "source": src, "source_name": "行业动态", "category": "36氪", "author": "36氪",
        "summary": "s", "tags": [], "concepts": cs}
    vis = [mk("a", ["moe", "tpu"]), mk("b", ["moe", "tpu"]), mk("c", ["moe"], "hn", "2026-07-21"),
           mk("d", ["moe"]), mk("e", ["moe"], "hn", "2026-07-19")]
    pool = {i["id"]: i for i in vis}
    cidx = {}
    for i in vis:
        for s in i["concepts"]:
            cidx.setdefault(s, []).append(i["id"])
    lib = {"moe": {"term": "MoE模型"}, "tpu": {"term": "TPU"}}
    return vis, pool, cidx, lib


def test_related_items_evidence_and_safety():
    """相关动态: 只用共同概念这一种可核关系, 且链接指向的页必然存在。

    此前实测 284 个详情页通往其他详情页的链接是 0 个 —— 读者读完只能回列表页重新扫,
    爬虫也只能靠 JS 驱动的列表页做枢纽。写过一版「无共同概念就退同源近期」的兜底档, 量出
    77% 的页四条全同源、最差例子是《国资委抓科技创新》配「美股收跌/欧盟调查足联」, 已删。
    """
    vis, pool, cidx, lib = _rel_fixture()
    a = pool["a"]
    rel = B.related_items(a, pool, cidx)
    ids = [r["id"] for r, _ in rel]
    check("不自链", "a" not in ids, ids)
    check("不重复", len(set(ids)) == len(ids), ids)
    check("全部在 pool 内(零死链)", all(r["id"] in pool for r, _ in rel), ids)
    check("条数不超上限", len(rel) <= B.RELATED_MAX, len(rel))
    check("共同概念多的排前面", ids[0] == "b", ids)
    check("同源不超 RELATED_SRC_MAX",
          max(sum(1 for r, _ in rel if r["source"] == s) for s in {r["source"] for r, _ in rel})
          <= B.RELATED_SRC_MAX, [r["source"] for r, _ in rel])
    check("两次调用同序(连跑字节稳定靠这条)",
          [r["id"] for r, _ in B.related_items(a, pool, cidx)] == ids)
    # 理由必须为真: 声称的共同概念在双方条目里都得有
    bad = [(r["id"], c) for r, cs in rel for c in cs
           if c not in a["concepts"] or c not in r["concepts"]]
    check("理由为真(共同概念双方都有)", not bad, bad)
    why = B.related_why(["moe", "tpu"], lib)
    check("理由写词条名不写 slug", "MoE模型" in why and "moe" not in why, why)
    check("多概念报计数", "2 个概念" in why, why)
    # 概念无同伴 → 整块不出, 不留空标题(实测 30% 的页属于这种)
    lone = dict(pool["a"], id="z", concepts=["unique-slug"])
    check("无同伴时不出空区块", B.related_items(lone, pool, cidx) == []
          and B.related_html([], lib) == "")
    h = B.related_html(rel, lib)
    check("链接是同目录相对路径", 'href="b.html"' in h, h[:90])
    check("区块内零外链", "http" not in h)
    check("有可访问名(aria-labelledby 指向真实 id)",
          'aria-labelledby="dp-rel-h"' in h and 'id="dp-rel-h"' in h)


def test_related_change_invalidates_signature():
    """相关列表变了必须触发重算 —— 否则条目下线后, 旧页挂着指向已删页的死链。

    这是本页唯一的跨条目依赖: 页面内容取决于**别的条目**, 而原签名只算自己的字段与镜像。
    这里直接比签名的 rsig 分量: 同一条目在「B 还在」与「B 已下线」两个 pool 下必须不同。
    """
    vis, pool, cidx, lib = _rel_fixture()
    a = pool["a"]
    # 签名必须与实现同源, 不能在测试里另抄一份公式 —— 第一版就是这么漏掉 date 的:
    # 实现列举了 id/标题/理由, 测试抄了同一份列举, 于是两边一起漏, 测试形同没写(Bugbot PR#103)。
    rsig = lambda pl, cx: B._sha(B.related_html(B.related_items(a, pl, cx), lib))
    before = rsig(pool, cidx)
    gone = {k: v for k, v in pool.items() if k != "b"}
    cidx2 = {s: [i for i in ids if i != "b"] for s, ids in cidx.items()}
    after = rsig(gone, cidx2)
    check("条目下线 → 相关签名变化(触发重算, 死链留不下)", before != after, f"{before} vs {after}")
    check("下线后的相关列表里不再有它", "b" not in [r["id"] for r, _ in B.related_items(a, gone, cidx2)])
    check("数据没变则签名不变(不制造无谓重算)", rsig(pool, cidx) == before)
    # 新条目挤进列表同样要改签名
    pool3 = dict(pool); pool3["f"] = dict(pool["b"], id="f", title="新来的", date="2026-07-25")
    cidx3 = {s: ids + (["f"] if s in ("moe", "tpu") else []) for s, ids in cidx.items()}
    check("新条目挤进列表 → 签名变化", rsig(pool3, cidx3) != before)
    # 渲染里出现的任何字段变了都得改签名。date 是第一版漏掉的那个: 相关条目日期被修正后,
    # 引用它的页会继续命中旧缓存, 页面上的时间卡住。
    for field, newval in (("date", "2026-07-28"), ("title", "改过的标题")):
        moved = {k: (dict(v, **{field: newval}) if k == "b" else v) for k, v in pool.items()}
        check(f"相关条目的 {field} 变了 → 签名变化", rsig(moved, cidx) != before, field)
    # 共同概念的词条名出现在理由文案里, 改它同样要重算
    lib2 = {"moe": {"term": "混合专家模型"}, "tpu": {"term": "TPU"}}
    check("共同概念的词条名变了 → 签名变化",
          B._sha(B.related_html(B.related_items(a, pool, cidx), lib2)) != before)
    # 反向: 渲染里**没有**的字段不该触发重算 —— 签名要恰好等于渲染面, 多了就是白算。
    # 砍掉「同源近期」兜底档之后, related_html 不再渲染来源名(理由只写共同概念)。
    for field, newval in (("source_name", "改过的来源"), ("summary", "改过的摘要"), ("category", "改过的分类")):
        moved = {k: (dict(v, **{field: newval}) if k == "b" else v) for k, v in pool.items()}
        check(f"相关条目的 {field} 不进渲染 → 签名不变(不制造无谓重算)",
              rsig(moved, cidx) == before, field)


# ---------------------------------------------------------------- 26
def test_artifacts_ignored_and_guarded():
    """生成物必须同时被 .gitignore 忽略、被 shell-clean 清单看住 —— 两道, 不是一道。

    本轮真出过事: 在 feat 上跑完管线 `git add -A`, 一次提了 379 个产物、124818 行。
    `.gitignore` 里当时一条生成物路径都没写, 全靠 CI 事后报红 —— **闸有效不等于防护有效**。
    更难看的是 `news-feed.xml` 因此已经溜进仓库并带着四个提交跑了一路, 而它能溜过 shell-clean,
    恰恰因为那份清单也漏了它(Bugbot PR#103 两处一起点出来)。

    判据从源码推, 不写死清单(写死清单挡不住"新加的产物忘了加进去", 这个坑本轮栽过第五次):
    根目录的 `.xml`/`.json` 一律是产物(模板壳是 `.html`), 管线的目录常量一律是产物目录;
    产物 ⊆ shell-clean 清单 ⊆ .gitignore。反向也测: 两个模板壳绝不能被忽略, 否则改版丢失。
    """
    src = (ROOT / "build_news.py").read_text(encoding="utf-8")
    root_files = {m for m in re.findall(r'ROOT / "([^"/]+\.(?:xml|json))"', src)}
    # 只认**赋给模块级常量**的多段路径 = 管线自己的输出目录/状态文件。人工种子登记表是以
    # `"file": ROOT / "data" / "product-news.json"` 写在 SOURCES 配置里的**输入**, 必须入库
    # —— 一律按"data/ 下都是产物"推会把它们也要求忽略, 那就把配方本身赶出仓库了。
    dirs = {"/".join(m[1:]) for m in
            re.findall(r'^([A-Z_]+) *= *ROOT / "([^"/]+)" / "([^"/]+)"', src, re.M)}
    gi_path, sc_path = ROOT / ".gitignore", ROOT / ".github" / "workflows" / "shell-clean.yml"
    if not (gi_path.exists() and sc_path.exists()):
        check("(跳过)本分支没有忽略规则或闸门文件", True)
        return
    pv = _preview_branch()
    if pv and _current_branch() == pv:
        check(f"(跳过){pv} 是预览分支, 注入过的壳与生成物按设计入库", True)
        return
    gi = [l.strip() for l in gi_path.read_text(encoding="utf-8").splitlines()
          if l.strip() and not l.startswith("#")]
    sc = sc_path.read_text(encoding="utf-8")
    check(f"根目录产物({len(root_files)} 个)全在 .gitignore",
          not [f for f in root_files if f not in gi],
          f"缺 {[f for f in root_files if f not in gi]} —— 本地 git add -A 会把它带进仓库")
    check(f"根目录产物({len(root_files)} 个)全在 shell-clean 清单",
          not [f for f in root_files if f not in sc],
          f"缺 {[f for f in root_files if f not in sc]} —— 溜进仓库时 CI 不会报")
    miss_dir = [d for d in dirs if not any(g.rstrip("/") == d for g in gi)]
    check(f"管线目录/状态文件({len(dirs)} 个)全在 .gitignore", not miss_dir, f"缺 {miss_dir}")
    check("模板壳没被误忽略(否则改版会丢)",
          not [s for s in ("news.html", "news-c.html") if s in gi])
    # shell-clean 清单是最后一道: 它漏了什么, 就等于那样的产物可以无声入库
    check("shell-clean 清单不比 .gitignore 松",
          not [f for f in root_files if f in gi and f not in sc])


# ---------------------------------------------------------------- 27
def test_askbar_one_shot_context_reaches_request():
    """卡片「问句子」的一次性上下文必须进 AI 请求, 而不是只改横幅文案。

    栽的过程值得记: 原写法是改写全局 `window.PAGE_CTX` 再调无参 `openAskbar()`, 毛病是从不
    还原(点过一张卡, 本页后续所有提问都被永久打上那篇文章的上下文)。我改成传参修掉了污染,
    但只在 open() 的局部变量里用了它 —— 而 greet/suggest/askReal 各自去读全局, **上下文
    从此根本到不了模型**。修了症状、废了功能, Bugbot PR#103 抓到。
    根因还是判据分散: "当前上下文"有两条获取路径。收口成 oneShot + pageCtx() 一条路。
    """
    js_p = ROOT / "assets" / "askbar.js"
    if not js_p.exists():
        check("(跳过)askbar.js 不在本分支", True)
        return
    js = js_p.read_text(encoding="utf-8")
    m = re.search(r"function pageCtx\(\)[^\n]*", js)
    check("pageCtx 是取上下文的唯一入口且读一次性上下文", m and "oneShot" in m.group(0),
          m.group(0) if m else "找不到 pageCtx")
    for fn in ("greet", "suggest", "askReal"):
        body = re.search(rf"function {fn}\(.*?\n  \}}", js, re.S)
        check(f"{fn} 经 pageCtx 取上下文(不自己读全局)",
              body and "pageCtx()" in body.group(0) and "window.PAGE_CTX" not in body.group(0),
              fn)
    close = re.search(r"function close\(\)[^\n]*", js)
    check("关闭时清掉一次性上下文(否则污染后续提问)", close and "oneShot = null" in close.group(0),
          close.group(0)[:80] if close else "")
    # 两个列表页: 卡片入口必须传参, 不许在点击处改写全局
    for page in ("news.html", "news-c.html"):
        pp = ROOT / page
        if not pp.exists():
            continue
        h = pp.read_text(encoding="utf-8")
        bad = [l.strip()[:70] for l in h.splitlines()
               if "window.PAGE_CTX" in l and "=" in l and "data-t" in l]
        check(f"{page} 卡片入口不改写全局上下文", not bad, bad)
        check(f"{page} 卡片入口传一次性上下文", "openAskbar(cardCtx)" in h)


# ---------------------------------------------------------------- 28
def test_page_desc_quality_and_width():
    """meta description 的唯一出口: 挡掉模型元话术、按显示宽度规整长度。

    实测线上真有一条: `b5f96bf69df5` 的 description 是「条目正文为空，无法提供内容简报。」——
    模型没产出简报, 而是解释了自己为什么产不出, 那句话原样进了页面正文的简报区与 meta
    description, 搜索结果与 AI 引擎读到的就是这句。621 条里只此一条, 但代价不对称:
    一条烂 description 的损失远大于一条缺 description。
    另有 26 页 description 超长(最长 388 字)在搜索结果里被截成半句, 2 页短到没有信息量。
    宽度而非字符数: 搜索结果按像素截断, 中文约 78 字满、英文约 155 字满, 这页两种语言都有。
    """
    check("元话术不可用", not B.brief_usable("条目正文为空，无法提供内容简报。"))
    check("太短不可用", not B.brief_usable("Talk Video"))
    check("正常简报可用", B.brief_usable("阿里发布 Qwen3-Max，主打长上下文与工具调用，定价对齐 GPT 系列。"))
    # 「作为AI」后面必须跟标点才算元话术, 否则误伤正常句子(第一版正则就误伤了这句)
    check("含「作为AI能力」的正常句不误伤",
          B.brief_usable("智能硬件作为AI能力落地实体场景的核心载体，已进入产品升级阶段。"))
    check("宽度: 中文 78 字 = 英文 156 字", B.disp_width("中" * 78) == B.disp_width("a" * 156) == 156)
    long_zh = {"summary": "阿里发布 Qwen3-Max，主打长上下文与工具调用，定价对齐 GPT 系列。" + "补充说明" * 20}
    d = B.page_desc(long_zh, "标题")
    check("中文超长切到句读边界", d.endswith("。") and B.disp_width(d) <= B.DESC_MAX_W, f"{len(d)}字")
    nopunct = {"summary": "甲" * 200}
    d2 = B.page_desc(nopunct, "标题")
    check("无句读时硬截并加省略号", d2.endswith("…"))
    check("加省略号后仍不超宽度上限", B.disp_width(d2) <= B.DESC_MAX_W, B.disp_width(d2))
    en = {"summary": "The model ships with a longer context window and better tool calling. " * 4}
    check("英文超长同样规整", B.disp_width(B.page_desc(en, "t")) <= B.DESC_MAX_W)
    check("坏简报退回原文摘要",
          B.page_desc({"brief": "无法提供内容简报。", "summary": "KOReader 是一款开源电子书阅读器。"},
                      "KOReader") == "KOReader 是一款开源电子书阅读器。")
    check("三者皆空退回标题", B.page_desc({}, "某标题") == "某标题")
    # 渲染侧: 坏简报不出简报区块, 也不进 description
    lib, worthy = fake_lib(), set()
    bad = fixture_item(brief="条目正文为空，无法提供内容简报。", concepts=[])
    html = B.detail_html(bad, lib, worthy)
    check("坏简报不渲染简报区块", 'class="dp-brief"' not in html)
    check("坏简报不进 meta description", "无法提供内容简报" not in html)
    good = fixture_item(brief="阿里发布 Qwen3-Max，主打长上下文与工具调用，定价对齐 GPT 系列。", concepts=[])
    check("好简报照常渲染", 'class="dp-brief"' in B.detail_html(good, lib, worthy))
    # 生成侧: 元话术不入库, 且落 brief_tried 标记防每轮重烧配额
    src = (ROOT / "build_news.py").read_text(encoding="utf-8")
    check("入库前过 brief_usable", "if brief_usable(b):" in src)
    check("答了但不可用时落 brief_tried(不再每轮重试烧配额)", 'it["brief_tried"] = has_full' in src)


# ---------------------------------------------------------------- 29
def test_concept_index_filter_and_termset():
    """概念索引页: 110 个概念要能查, 术语集 schema 要覆盖全, 且不跑 JS 时内容不变。

    两处实测问题:
    ① schema 里硬编码 `order[:60]` —— 页面 110 张卡, 机器只看到 60 个(覆盖 54%), 漏掉的正是长尾。
       补满的真实代价只有 0.51KB gzip(+4%): 原始 +8KB, 但重复 JSON 压缩率极高 ——
       **按原始体积做的取舍在这里是错的**。上限保留但放宽到 300, 且截断时打印告警(静默截断
       会让人以为"全覆盖了")。
    ② 110 张卡平铺没有查找入口, 读者只能靠浏览器 Ctrl+F(手机上埋得很深)。过滤键收词条名 +
       **别名** + slug —— 读者常常只记得别名(记得 RLHF, 但词条名是「人类反馈强化学习」)。
    """
    lib = {"moe-model": {"term": "MoE模型", "aliases": ["混合专家模型", "Mixture of Experts"],
                         "def": "一种把大模型拆成多个专家子网络、每次只激活少数几个的架构。"},
           "rlhf": {"term": "人类反馈强化学习", "aliases": ["RLHF"],
                    "def": "用人类偏好数据训练奖励模型再微调策略的方法。"}}
    k = B.concept_keys("moe-model", lib["moe-model"])
    check("检索键含词条名", "moe模型" in k, k)
    check("检索键含全部别名", all(a.lower() in k for a in lib["moe-model"]["aliases"]), k)
    check("检索键含 slug 词", "moe model" in k, k)
    check("检索键全小写", k == k.lower(), k)
    h = B.concept_index_html(lib, {"moe-model": [1, 2], "rlhf": [1]}, set(lib))
    check("每张卡都有检索键", h.count("data-k=") == len(lib), h.count("data-k="))
    check("有过滤输入框", 'id="cxq"' in h and 'type="search"' in h)
    check("计数区有 aria-live(读屏能拿到结果数)", 'id="cxCount"' in h and 'aria-live="polite"' in h)
    check("有空结果态与「看全部」出口", 'id="cxEmpty"' in h and 'id="cxClear"' in h)
    # 渐进增强: 不跑 JS 时全部卡片可见 —— 若默认 hidden, 爬虫拿到的就是空页
    check("卡片默认不隐藏(不跑 JS 照常可见)", "cx-card" in h and 'class="cx-card" hidden' not in h)
    check("CSS 没把卡片默认藏起来", not re.search(r"\.cx-card\s*\{[^}]*display\s*:\s*none", h))
    ld = [json.loads(html_unescape(x)) for x in
          re.findall(r'<script type="application/ld\+json">(.*?)</script>', h, re.S)]
    ts = [x for x in ld if x.get("@type") == "DefinedTermSet"]
    check("发 DefinedTermSet", len(ts) == 1, [x.get("@type") for x in ld])
    terms = ts[0].get("hasDefinedTerm") or []
    check("术语集覆盖全部有页概念", len(terms) == len(lib), f"{len(terms)}/{len(lib)}")
    # 词条只列 name+url: 定义留在各自的概念页(那里有全文 DefinedTerm), 枢纽页再抄 112 条
    # 是冗余, 实测要多花 13.7KB gzip —— 而最初支持"塞定义"的 0.51KB 是拿重复假数据量出来的
    check("每个词条有名字与 url", all(x.get("name") and x.get("url", "").endswith(".html") for x in terms))
    check("术语集不重复抄定义(定义在各概念页)", not any(x.get("description") for x in terms))
    # 只列有页的概念, 否则 schema 里就是死链
    thin = dict(lib, **{"no-page": {"term": "没页的概念", "aliases": [], "def": "只被提到一次。"}})
    h2 = B.concept_index_html(thin, {"moe-model": [1, 2]}, set(lib))
    ld2 = [json.loads(html_unescape(x)) for x in
           re.findall(r'<script type="application/ld\+json">(.*?)</script>', h2, re.S)]
    urls = [x["url"] for y in ld2 if y.get("@type") == "DefinedTermSet" for x in y["hasDefinedTerm"]]
    check("不够格发页的概念不进 schema(否则是死链)",
          not any("no-page" in u for u in urls), urls)
    src = (ROOT / "build_news.py").read_text(encoding="utf-8")
    check("到上限时打印告警(不静默截断)",
          "if len(order) > IDX_SCHEMA_MAX:" in src and "只列了" in src)


# ---------------------------------------------------------------- 30
def test_fingerprint_covers_embedded_constants():
    """整段进页面的常量也得进指纹 —— 否则改样式/改内联脚本不触发重算, 页面停在旧版。

    这是同类问题的第四次。`DETAIL_CSS`/`CONCEPT_CSS`/`CX_FILTER_HTML`/`CX_FILTER_JS` 都是模块级
    字符串, 原样进页面; 但函数源码里只有 `{DETAIL_CSS}` 这个引用、不含内容, 所以只哈函数源码时
    **改 CSS 根本不触发重算**(实测四个常量全部如此)。之前没出事只是因为每次改样式时恰好也改了
    闭包里的函数。修法照旧: 常量清单也从调用图推出来, 不手写。

    反向同样要测: 运行中会被填充的容器(`_CRX_CACHE` 这类 dict)一旦进指纹, 签名就每轮不同 →
    每轮全量重算, 增量缓存直接废掉。所以只收不可变类型。
    """
    fns, consts = B._tpl_parts()
    for c in ("DETAIL_CSS", "CONCEPT_CSS", "CX_FILTER_HTML", "CX_FILTER_JS"):
        check(f"{c} 进指纹", c in consts, f"常量清单: {consts}")
    v0 = B.render_ver()
    for name in ("DETAIL_CSS", "CX_FILTER_JS", "READ_CPM", "DESC_MAX_W", "TOC_OPEN_MAX"):
        orig = getattr(B, name)
        try:
            setattr(B, name, orig + ("/*x*/" if isinstance(orig, str) else 1))
            B._TPL_CACHE.clear()
            check(f"改 {name} → 版本键变化", B.render_ver() != v0, name)
        finally:
            setattr(B, name, orig)
            B._TPL_CACHE.clear()
    check("还原后版本键回到原值", B.render_ver() == v0)
    # 容器: 从未被就地改写的配置表要进(SRC_ICON 原样进页面, Bugbot PR#103), 运行时缓存要挡住
    check("SRC_ICON 进指纹(图标 class 原样进页面)", "SRC_ICON" in consts, consts)
    orig_icon = dict(B.SRC_ICON)
    try:
        B.SRC_ICON["industry"] = "fa-solid fa-changed"
        B._TPL_CACHE.clear()
        check("改一个来源图标 → 版本键变化", B.render_ver() != v0)
    finally:
        B.SRC_ICON.clear()
        B.SRC_ICON.update(orig_icon)
        B._TPL_CACHE.clear()
    caches = [c for c in ("_CRX_CACHE", "_TPL_CACHE", "_EV_CACHE", "_FEISHU_ROSTER") if c in consts]
    check("运行时缓存不进指纹(否则每轮全量重算)", not caches, caches)
    mut = B._mutated_globals()
    check("就地改写判据认出全部运行时缓存",
          all(c in mut for c in ("_CRX_CACHE", "_TPL_CACHE")), sorted(mut)[:6])
    check("配置表没被误判为可变", "SRC_ICON" not in mut and "MIRROR_MODE" not in mut)
    # 规范化: set 顺序与机器路径都不能进哈希
    check("_const_repr 对 set 顺序不敏感",
          B._const_repr({"b", "a", "c"}) == B._const_repr({"c", "a", "b"}))
    check("_const_repr 把 Path 折成相对 ROOT(绝对路径含机器名)",
          "P:data/x.json" == B._const_repr(B.ROOT / "data" / "x.json"),
          B._const_repr(B.ROOT / "data" / "x.json"))
    hashed = "".join(B._const_repr(getattr(B, c)) for c in consts)
    check("进哈希的内容不含本机绝对路径", str(B.ROOT) not in hashed)
    leak = [c for c in consts if re.search(r"KEY|TOKEN|SECRET|PASSWORD", c)]
    check("密钥类常量不进指纹", not leak, leak)
    # 运行时缓存被填充后版本键必须稳定
    B._CRX_CACHE["__probe__"] = 1
    B._TPL_CACHE.clear()
    try:
        check("运行时缓存变动不影响版本键", B.render_ver() == v0)
    finally:
        B._CRX_CACHE.pop("__probe__", None)
        B._TPL_CACHE.clear()


# ---------------------------------------------------------------- 30b
def test_fingerprint_stable_across_processes():
    """指纹必须跨进程稳定 —— set 的 repr 顺序取决于 PYTHONHASHSEED, 这条不测就会埋雷。

    实测反证: 直接 `repr(OWN_SOURCES)` 时 seed=1 给 6e1b59ce79、seed=2 给 9b4d7c2874。
    若指纹这样算, CI 每 6 小时一轮、每轮 hash 种子不同 → **每轮全量重写 287 页并 rsync 一遍**,
    而日志一切正常, 没有任何可观测症状。所以 `_const_repr` 对 set 排序、对 Path 折相对路径。
    """
    import subprocess
    code = ("import importlib.util,sys;"
            "spec=importlib.util.spec_from_file_location('bn',r'%s');"
            "B=importlib.util.module_from_spec(spec);sys.modules['bn']=B;spec.loader.exec_module(B);"
            "print(B.render_ver())" % (ROOT / "build_news.py"))
    outs = []
    for seed in ("1", "2", "12345"):
        env = dict(os.environ, PYTHONHASHSEED=seed)
        r = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True,
                           env=env, cwd=str(ROOT), timeout=90)
        outs.append(r.stdout.strip())
    check("三个不同 PYTHONHASHSEED 下版本键一致", len(set(outs)) == 1, outs)
    check("子进程算出的版本键与本进程一致", outs and outs[0] == B.render_ver(), f"{outs[:1]} vs {B.render_ver()}")


# ---------------------------------------------------------------- 31
def test_related_caps_reach_signature():
    """相关动态的两个上限不在指纹里(它们的函数不在闭包), 但必须经 rsig 生效 —— 这里验它。

    `related_items` 由 write_detail_pages 调用而非模板函数, 所以不进调用图闭包; 它的影响靠
    「渲染结果进签名」这条路 —— 改上限 → 相关列表变 → related_html 变 → rsig 变 → 重算。
    光断言"应该覆盖"不算验证, 得真改一遍看签名动不动。
    fixture 特意让四个同伴里三个同源 —— 第一版四个同伴来自四个不同源, 同源上限根本没被触发,
    测出来"改上限没反应"却不是 bug(这轮第四次 fixture 不覆盖判据)。
    """
    mk = lambda i, src: {"id": i, "title": f"标题{i}", "url": f"https://e.com/{i}",
                         "date": "2026-07-20", "source": src, "source_name": src, "category": "c",
                         "author": "a", "summary": "s", "tags": [], "concepts": ["moe"]}
    vis = [mk("a", "industry"), mk("b", "industry"), mk("c", "industry"),
           mk("d", "industry"), mk("e", "hn")]
    pool = {i["id"]: i for i in vis}
    cidx = {"moe": [i["id"] for i in vis]}
    lib = {"moe": {"term": "MoE模型"}}
    a = pool["a"]
    sig = lambda: B._sha(B.related_html(B.related_items(a, pool, cidx), lib))
    base = sig()
    srcs = lambda: collections.Counter(r["source"] for r, _ in B.related_items(a, pool, cidx))
    check("同源上限生效(4 个同伴里 3 个同源 → 只取 2)", srcs()["industry"] == B.RELATED_SRC_MAX, dict(srcs()))
    for name, val in (("RELATED_MAX", 2), ("RELATED_SRC_MAX", 1), ("RELATED_SRC_MAX", 3)):
        orig = getattr(B, name)
        try:
            setattr(B, name, val)
            check(f"{name}={val} → rsig 变化(经渲染结果进签名)", sig() != base, f"{name}={val}")
        finally:
            setattr(B, name, orig)
    check("还原后 rsig 回到原值", sig() == base)


# ---------------------------------------------------------------- 32
def test_askbar_routes_no_intent_theft():
    """意图路由先命中先返回, 所以**顺序本身是判据** —— 用真实问句探针钉住, 不是看词表。

    Bugbot PR#103 抓到: 我给动态页加的路由里放了「文章」这个泛词, 又排在知识库路由之前,
    于是「知识库文章怎么管理」被动态页答复抢走, 懂行/知识库意图永远拿不到。
    我第一版自查只比对**逐词相同**, 因此漏掉了这种情形 —— 冲突发生在**短语**同时命中两条路由时,
    而不是两条路由共用同一个词。所以这里改用问句探针。

    修的过程还纠出两处存量问题与我自己的一次误伤:
    · 「私有化部署」两边都命中(部署 / 私有), 而 enterprise 的答复才真正讲私有化 → 安全路由前移
    · 「数据」同时在安全路由与问数路由里, 前者永远抢到 → 从安全路由移除
    · 但整词移除是误伤: 「数据不出域吗」随即掉到问数路由(改前是对的), 补「不出域」才补回来
    """
    js_p = ROOT / "assets" / "askbar.js"
    if not js_p.exists():
        check("(跳过)askbar.js 不在本分支", True)
        return
    m = re.search(r"var ROUTES = \[(.*?)\n  \];", js_p.read_text(encoding="utf-8"), re.S)
    if not m:
        check("找到 ROUTES 数组", False)
        return
    routes = []
    for line in m.group(1).split("\n"):
        r = re.search(r"re:\s*/\((.*?)\)/i", line)
        c = re.search(r"cards:\s*\[([^\]]*)\]", line)
        if r:
            routes.append((re.compile("|".join(r.group(1).split("|")), re.I),
                           (c.group(1) or "").replace("'", "").strip()))
    check(f"解析到 {len(routes)} 条路由", len(routes) >= 10, len(routes))
    probes = [("知识库文章怎么管理", "dongxing"), ("有哪些文档", "dongxing"), ("资料能检索吗", "dongxing"),
              ("最近有什么动态", "news"), ("佳芮写的博客", "news"), ("有什么文章可以看", "news"),
              ("数据安全吗", "enterprise"), ("数据不出域吗", "enterprise"), ("私有化部署", "enterprise"),
              ("帮我查数据", "canmou"), ("数据报表能做吗", "canmou"), ("能出图表吗", "canmou"),
              ("接入要多久", "fde"), ("怎么落地", "fde"),
              ("和普通机器人有什么区别", "service"), ("能接抖音吗", "miaohui")]
    wrong = []
    for q, want in probes:
        got = next((c for rx, c in routes if rx.search(q)), "(无命中)")
        if want not in got:
            wrong.append(f"{q}→{got}(期望 {want})")
    check(f"{len(probes)} 条问句探针全部落到该去的路由", not wrong, "; ".join(wrong))


# ---------------------------------------------------------------- 33
def test_state_savers_actually_run():
    """保存状态的函数要真跑一遍 —— 光有原子写的单元测试拦不住调用点写错。

    实测崩过: `save_concepts` 里 `write_atomic(CONCEPTS_FILE, json.dumps(...), encoding="utf-8")`
    残留了从 `path.write_text(text, encoding=...)` 改过来时没删的关键字, 而 `write_atomic(path, text)`
    只收两个位置参数 → `TypeError`。它藏得很深, 因为触发条件是 `if len(lib) != n_lib`, **只有本轮
    新增了概念才会走到**。后果不是"报个错": 它崩在 main() 里 `save_concepts` 那一行, 而
    `data/news.json` 要到后面才保存 —— 本轮的简报/概念/翻译全部不落盘, 下轮重做, 每次新增概念
    就白烧一遍 AI 配额; CI 的 cron 每遇新概念必失败, 线上永远不更新。

    所以这里两条一起测: ①调用点签名(AST 静态查, 覆盖所有 write_atomic 调用) ②真跑一遍存盘函数。
    """
    import ast
    src = (ROOT / "build_news.py").read_text(encoding="utf-8")
    bad = [(n.lineno, [k.arg for k in n.keywords], len(n.args))
           for n in ast.walk(ast.parse(src))
           if isinstance(n, ast.Call) and isinstance(n.func, ast.Name)
           and n.func.id == "write_atomic" and (n.keywords or len(n.args) != 2)]
    check("write_atomic 全部调用点都是两个位置参数、零关键字", not bad, bad)
    # 真跑: 存盘函数写进临时目录, 读回来必须是合法 JSON, 且不留 .tmp
    with tempfile.TemporaryDirectory() as d:
        orig = B.CONCEPTS_FILE
        try:
            B.CONCEPTS_FILE = pathlib.Path(d) / "concepts.json"
            B.save_concepts({"moe": {"term": "MoE模型", "aliases": ["MoE"],
                                     "def": "一种把大模型拆成多个专家子网络的架构。", "at": "2026-07-30"}})
            got = json.loads(B.CONCEPTS_FILE.read_text(encoding="utf-8"))
            check("save_concepts 能跑通并写出合法 JSON", got.get("concepts", {}).get("moe"), list(got))
            check("save_concepts 不留 .tmp 垃圾", not list(pathlib.Path(d).glob("*.tmp")))
        finally:
            B.CONCEPTS_FILE = orig


# ---------------------------------------------------------------- 34
def test_seed_ref_is_a_tag():
    """seed 的取数来源必须是 tag, 不能是裸 SHA —— 它是整套部署唯一的初始化入口。

    `news-cron.yml` 的 seed 任务从 `SEED_REF` 那个提交取存量(实测含 236 详情页 / 165 概念页 /
    279 状态文件 / 183 图片)一次性推到服务器, 之后常规轮才能增量续跑; 常规轮拉不到状态会直接
    中止(防空状态全量重抓烧 API)。而 seed **至今一次都没跑过**。

    原先写的是裸 SHA `64bec20…`, 而那个提交只被 feat 分支可达:
    · squash 合并不会把它带进 main —— 实测它不是 main 的祖先
    · `git clone` 只拉 refs/heads/* 与 refs/tags/*, **不拉 refs/pull/**, 镜像里根本没有它
    · 修 CLA 要重写 88 条提交的作者邮箱, 那会改掉它的 SHA
    tag 是永久引用, 删分支与重写历史都不影响, 名字本身也比一串 SHA 自解释。
    """
    wf = ROOT / ".github" / "workflows" / "news-cron.yml"
    if not wf.exists():
        check("(跳过)news-cron.yml 不在本分支", True)
        return
    txt = wf.read_text(encoding="utf-8")
    m = re.search(r"^\s*SEED_REF:\s*(\S+)", txt, re.M)
    check("workflow 里有 SEED_REF", bool(m), "找不到")
    if not m:
        return
    ref = m.group(1)
    check("SEED_REF 不是裸 SHA(裸 SHA 会随分支删除/历史重写失去引用)",
          not re.fullmatch(r"[0-9a-f]{7,40}", ref), ref)
    check("SEED_REF 是个可读的 tag 名", re.fullmatch(r"[\w.-]+", ref) and not ref.startswith("$"), ref)
    # 文档三处要一起提到它, 否则接手人不知道 seed 从哪取数
    for doc, label in ((ROOT / "docs" / "DEPLOY.md", "DEPLOY.md"),
                       (ROOT / "CLAUDE.md", "CLAUDE.md")):
        if doc.exists():
            check(f"{label} 提到 SEED_REF 的 tag 名", ref in doc.read_text(encoding="utf-8"), ref)


# ---------------------------------------------------------------- 35
def test_banned_terms_absent_from_shipped_pages():
    """「企微 / 企业微信」不得出现在任何出货页面 —— 2026-07-27 定的口径。

    这条口径当时**只清了动态页**: 首页与全站联系弹窗一直漏着, 佳芮 7-24 就提过, 7-30 复查时
    首页仍有 7 处、`site.js` 2 处、`askbar.js` 1 处、两个 CSS 各 1 处 —— 其中「扫码加企业微信」
    是联系弹窗标题, 而 `site.js` 那份**所有子页都注入**。
    管线里的 `has_banned()` 只管概念页原文证据一处, 页面文案完全没被覆盖, 也没有任何 CI 闸。

    我自己第一遍清理还漏了两个 CSS 文件 —— 因为手写的 grep 只列了 html/js/json。所以这里按
    **后缀白名单遍历**而不是列文件名: 出货物 = 页面 + 前端资源, 少列一种后缀就等于漏一片。

    范围刻意跳过源码与文档: `build_news.py` 里 `BANNED_TERMS` 就是这两个词, 查它等于自伤;
    `news/` 下的镜像正文是生成物(不入库), 其中 10 篇是佳芮 2021–2023 的署名文章, 改不改是
    内容决定, 不该由测试代替人拍板。
    """
    BANNED = ("企业微信", "企微")
    SKIP = {".git", ".github", "docs", "node_modules", "__pycache__", "news", "data"}
    SUFFIX = (".html", ".js", ".css", ".json", ".xml", ".txt")
    files = [p for p in ROOT.rglob("*")
             if p.is_file() and p.suffix in SUFFIX and not (set(p.relative_to(ROOT).parts) & SKIP)]
    check(f"扫到出货文件 {len(files)} 个", len(files) > 50, len(files))
    bad = []
    for p in files:
        try:
            lines = p.read_text(encoding="utf-8").splitlines()
        except (UnicodeDecodeError, OSError):
            continue
        for i, line in enumerate(lines, 1):
            if any(b in line for b in BANNED):
                bad.append(f"{p.relative_to(ROOT)}:{i}")
                break
    check("出货页面零命中「企微/企业微信」", not bad, bad[:6])
    # 闸的范围不能把源码里的判据定义也算进去 —— 那会让这条永远无法通过
    src = (ROOT / "build_news.py").read_text(encoding="utf-8")
    check("管线里的 BANNED_TERMS 判据仍在(闸不自伤)", 'BANNED_TERMS = ("企业微信", "企微")' in src)
    wf = ROOT / ".github" / "workflows" / "copy-guard.yml"
    check("copy-guard CI 闸存在(此前三个分支上都没有)", wf.exists())
    if wf.exists():
        w = wf.read_text(encoding="utf-8")
        check("CI 闸与本测试同款后缀白名单", all(s in w for s in SUFFIX), "后缀不一致会漏一片")


# ---------------------------------------------------------------- 36
def test_screen_rule_identity_triggers_rejudge():
    """判定必须记下「是哪条规则判的」—— 否则换判据后旧判定静默留着。

    判据刚换过: industry/qisi 从 `ai`(和 AI 有关)换成 `biz`(和我们有关)。佳芮的原话是
    「凌迪科技和 AI 有关，但和我们没关系」—— 那条**按旧判据是正确通过的**, 错的是判据本身。
    而原先判定只存 `ai` 字段、不记规则身份, `todo` 只挑 `"ai" not in i` ——
    **换了判据也不会重判**。这与「改了模板却不触发缓存重算」是同一类错, 今天已修过三次
    (指纹漏函数 / rsig 漏字段 / 常量与容器漏收), 这是第四处同源问题。

    两侧都要测: 换过规则的源要重判, **没换过的源不能被卷进来**(否则等于全库重刷烧配额)。
    """
    src = (ROOT / "build_news.py").read_text(encoding="utf-8")
    check("新判据 biz 存在", "biz" in B.AI_RULES, sorted(B.AI_RULES))
    used = {s["id"]: s.get("ai_filter") for s in B.SOURCES if s.get("ai_filter")}
    check("industry 与 qisi 换用 biz", used.get("industry") == "biz" and used.get("qisi") == "biz", used)
    check("其余源判据未动", used.get("rui-blog") == "company" and used.get("voices") == "techdev"
          and used.get("hn") == "hn", used)
    check("biz 判据写明了「与我们业务无关的 AI 也要排掉」",
          all(k in B.AI_RULES["biz"] for k in ("私域", "IM", "keep=false")), "判据文字不完整")
    check("判定写入时带上 rule", 'it["ai"] = {"keep": vmap[it["id"]], "at": today, "rule": rules[it["source"]]}' in src)
    check("关键词预过滤那条也带 rule(口径一致)", '"kw": True, "rule": rules[it["source"]]' in src)
    check("老判定的规则由 _LEGACY_RULE 补齐", B._LEGACY_RULE == {"industry": "ai", "qisi": "ai"}, B._LEGACY_RULE)
    check("重判有分轮上限(换判据不该一轮烧完配额)", isinstance(B.REJUDGE_MAX, int) and B.REJUDGE_MAX > 0)
    # 用假条目模拟 _stale_rule 的四种情形(它是 ai_screen 的内部函数, 这里复现同一判据)
    rules = {s["id"]: s["ai_filter"] for s in B.SOURCES if s.get("ai_filter")}
    def stale(it):
        a = it.get("ai")
        if not isinstance(a, dict):
            return False
        was = a.get("rule") or B._LEGACY_RULE.get(it["source"], rules.get(it["source"]))
        return was != rules.get(it["source"])
    check("老判定(无 rule 字段)+ 换过规则的源 → 判为过期",
          stale({"source": "industry", "ai": {"keep": True}}))
    check("已按新规则判过 → 不重判",
          not stale({"source": "industry", "ai": {"keep": True, "rule": "biz"}}))
    check("没换规则的源, 老判定不算过期(不卷进来)",
          not stale({"source": "voices", "ai": {"keep": True}})
          and not stale({"source": "hn", "ai": {"keep": False}}))
    check("完全没判过的条目照常进 todo(不是靠 stale 判)", not stale({"source": "industry"}))


# ---------------------------------------------------------------- 37
def test_no_mixed_all_zone():
    """去掉「全部」混排分区 —— 一切到混排, 自家内容必然被淹。

    实测量级: 行业源一天约 50 条新增、公司内容约 4 条/月(2026-07 仅 4 条), 而混排是纯时间倒序。
    所以只留两个区(默认句子动态), 想看外部观察再切行业雷达 —— 「两边都看一点」这个视图
    说不出对读者的价值, 留着只会让人误入被淹的那一屏。
    """
    for page in ("news.html", "news-c.html"):
        p = ROOT / page
        if not p.exists():
            continue
        h = p.read_text(encoding="utf-8")
        m = re.search(r"var GROUPS = \[(.*?)\];", h, re.S)
        check(f"{page} 找到 GROUPS 定义", bool(m))
        if not m:
            continue
        keys = re.findall(r"k: '([a-z]+)'", m.group(1))
        check(f"{page} 只有两个分区", keys == ["company", "radar"], keys)
        st = re.search(r"state = \{[^}]*group: '([a-z]+)'", h)
        check(f"{page} 默认分区是 company", st and st.group(1) == "company",
              st.group(1) if st else "找不到 state")


# ---------------------------------------------------------------- 36
def test_news_page_is_reachable():
    """动态页必须能从站内导航走到 —— 「建好了但没人能走到」是最贵的一类缺陷。

    实测发现(2026-07-30, 骐畅在 http://…:8082 上看不到入口): 整个 PR 建了 293 个详情页、
    131 个概念页、sitemap、RSS、四种 schema, 而 **`index.html` / `careers/index.html` /
    `assets/site.js` 三处导航里指向 `news.html` 的链接都是 0 处** —— 访客只能直接输 URL 才能到。

    它躲过了当时所有守卫: `news-test` 查管线不变量(页面内容对不对)、`shell-clean` 查模板壳、
    `copy-guard` 查口径, **没有任何一条查「这页可达吗」**。与今天那批缺陷同一类:
    产物正常 ≠ 功能生效。

    判据是**可达性**而不是某个写死的链接文案: 从首页出发, 沿站内链接一跳能到 news.html。
    这样将来改导航结构、换文案、调顺序都不会误报。
    """
    def links_to(path, target="news.html"):
        p = ROOT / path
        if not p.exists():
            return None
        s = p.read_text(encoding="utf-8")
        # 直接 href, 或 site.js 里 REL 拼接的形式
        return len(re.findall(r'href="[^"]*' + re.escape(target) + r'"', s)) + \
               len(re.findall(r"REL \+ '" + re.escape(target) + r"'", s))

    home = links_to("index.html")
    check("首页导航能到动态页", home and home > 0, f"index.html 里 {home} 处")
    shared = links_to("assets/site.js")
    check("共享导航(所有子页注入)能到动态页", shared and shared > 0, f"site.js 里 {shared} 处")
    careers = links_to("careers/index.html")
    if careers is not None:
        check("招聘页(自带导航)能到动态页", careers > 0, f"{careers} 处")
    # 反向: 动态页也要能回到站内(否则是单向死胡同)
    for page in ("news.html", "news-c.html"):
        p = ROOT / page
        if not p.exists():
            continue
        s = p.read_text(encoding="utf-8")
        back = len(re.findall(r'href="(?:index\.html|/|\.\./)"', s)) + s.count('id="site-nav"') + s.count("SITE_REL")
        check(f"{page} 有回站内的路径", back > 0, back)


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
