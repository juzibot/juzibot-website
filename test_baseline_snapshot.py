"""Unit tests for baseline_snapshot.py extraction logic.

Focused on the core, deterministic helpers: HTML text/link extraction, internal
link classification, and target resolution. These back the three baseline
reference sets (content strings, assets, internal links).
"""

import baseline_snapshot as bs


def _parse(markup):
    p = bs._PageParser()
    p.feed(markup)
    p.close()
    return p


def test_extracts_title_lang_and_meta_description():
    p = _parse(
        '<!DOCTYPE html><html lang="zh-CN"><head>'
        '<title>句子互动 · 测试</title>'
        '<meta name="description" content="一段描述">'
        "</head><body><p>正文</p></body></html>"
    )
    assert p.lang == "zh-CN"
    assert p.title == "句子互动 · 测试"
    assert p.meta_description == "一段描述"


def test_collapses_whitespace_and_skips_empty_strings():
    p = _parse("<body><p>  hello   world  </p><p>\n\t</p></body>")
    assert p.strings == ["hello world"]


def test_skips_script_and_style_text():
    p = _parse(
        "<body><style>.a{color:red}</style>"
        "<script>var x = 1;</script>"
        "<p>可见文案</p></body>"
    )
    assert p.strings == ["可见文案"]


def test_title_text_not_duplicated_into_content_strings():
    p = _parse("<head><title>页面标题</title></head><body><p>正文</p></body>")
    assert p.strings == ["正文"]
    assert p.title == "页面标题"


def test_collects_href_and_src_links():
    p = _parse(
        '<body><a href="products/miaodong.html">x</a>'
        '<img src="/assets/brand/logo.png"></body>'
    )
    assert "products/miaodong.html" in p.raw_links
    assert "/assets/brand/logo.png" in p.raw_links


def test_is_internal_classification():
    assert bs._is_internal("products/miaodong.html")
    assert bs._is_internal("/assets/style.css")
    assert not bs._is_internal("https://juzibot.com/")
    assert not bs._is_internal("//cdn.example.com/x.js")
    assert not bs._is_internal("mailto:hi@juzibot.com")
    assert not bs._is_internal("tel:123")
    assert not bs._is_internal("javascript:void(0)")
    assert not bs._is_internal("#section")


def test_resolve_target_relative_from_subdir():
    # a link from products/miaodong.html to ../about.html resolves to about.html
    assert bs._resolve_target("products/miaodong.html", "../about.html") == "about.html"
    # sibling link
    assert bs._resolve_target("products/miaodong.html", "shouhu.html") == "products/shouhu.html"


def test_resolve_target_root_relative_and_strips_query_fragment():
    assert bs._resolve_target("index.html", "/assets/style.css") == "assets/style.css"
    assert bs._resolve_target("index.html", "about.html?x=1#top") == "about.html"


def test_resolve_target_directory_link_gets_index():
    assert bs._resolve_target("index.html", "careers/") == "careers/index.html"
