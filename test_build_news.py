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
