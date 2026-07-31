#!/usr/bin/env python3
"""给 assets/site.js 与 assets/site.css 的引用打内容哈希戳 —— 改了资源, 老访客当天就能拿到新的。

## 为什么需要它

2026-07-31 实测: 给全站导航加「动态」入口后, 骐畅在 enterprise.html 上仍然看不到。
文件是对的(线上 site.js 第 51 行确实有那行), 页面也确实用注入导航(`id="site-nav"` 1 处、
自带 nav-item 0 处), 但服务器给静态资源发的是:

    Cache-Control: public, max-age=604800     ← 7 天强缓存, 不回源校验
    src="assets/site.js"                       ← URL 没有版本号

于是**任何老访客的浏览器都会用旧的那份, 整整一周**。改动等于一周内不生效, 而我们这边
查文件、查线上响应都一切正常 —— 又一例「产物正常 ≠ 功能生效」。

缓存策略在运维侧的 nginx 里(仓库的 deploy/*.conf 没有), 改不了; 能控的是引用方式。

## 做法

把 `assets/site.js` 引用改成 `assets/site.js?v=<内容哈希前 8 位>`。内容一变哈希就变, URL 就变,
浏览器自然重新拉 —— **不依赖任何人记得改版本号**(那正是这个项目反复出错的模式)。

跑法:
    python3 stamp_assets.py          # 打戳/更新戳
    python3 stamp_assets.py --check  # 只检查是否一致(CI 与测试用), 不改文件

`build_news.py` 生成的详情页/概念页同样引用这两个资源, 它在渲染时调用本模块的 `asset_url()`,
所以那 400 多页不用在这里处理。
"""
import argparse
import hashlib
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
ASSETS = ("assets/site.js", "assets/site.css", "assets/askbar.js")
# 只处理**手工维护的页面**: zh/en 是 301 跳转桩(没有资源引用), news/ 与 data/ 是生成物
SKIP_PREFIX = ("zh/", "en/", "news/", "data/", "node_modules/")


def asset_hash(rel: str) -> str:
    """资源内容的短哈希; 文件不在就返回空(调用方按无版本处理, 不炸)。"""
    p = ROOT / rel
    if not p.exists():
        return ""
    return hashlib.sha1(p.read_bytes()).hexdigest()[:8]


def asset_url(rel: str, prefix: str = "") -> str:
    """给渲染方用: 返回带版本戳的引用地址(prefix 是页面到根的相对前缀, 如 '../../')。"""
    h = asset_hash(rel)
    return f"{prefix}{rel}" + (f"?v={h}" if h else "")


def _pages():
    for p in sorted(ROOT.rglob("*.html")):
        rel = str(p.relative_to(ROOT))
        if rel.startswith(SKIP_PREFIX) or ".git" in p.parts:
            continue
        yield p, rel


def run(check_only: bool) -> int:
    hashes = {a: asset_hash(a) for a in ASSETS}
    missing = [a for a, h in hashes.items() if not h]
    if missing:
        print(f"::error::资源不存在: {missing}")
        return 1
    stale, fixed = [], 0
    for p, rel in _pages():
        t = p.read_text(encoding="utf-8")
        orig = t
        for a, h in hashes.items():
            name = a.split("/")[-1]
            # 匹配任意相对前缀 + 可能已有的旧版本戳
            pat = re.compile(r'((?:\.\./)*assets/' + re.escape(name) + r')(\?v=[0-9a-f]+)?')
            t = pat.sub(lambda m: f"{m.group(1)}?v={h}", t)
        if t != orig:
            stale.append(rel)
            if not check_only:
                p.write_text(t, encoding="utf-8")
                fixed += 1
    if check_only:
        if stale:
            print(f"::error::{len(stale)} 个页面的资源版本戳与文件内容不符(改了 assets 但没打戳):")
            for s in stale[:10]:
                print(f"::error::  {s}")
            print("修法: python3 stamp_assets.py")
            return 1
        print(f"资源版本戳一致 ✓ ({', '.join(f'{a}={h}' for a, h in hashes.items())})")
        return 0
    print(f"已打戳 {fixed} 页 ({', '.join(f'{a}={h}' for a, h in hashes.items())})")
    return 0


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true", help="只检查不改文件(CI 用)")
    sys.exit(run(ap.parse_args().check))
