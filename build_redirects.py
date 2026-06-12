#!/usr/bin/env python3
# 旧双语站 /zh/* 和 /en/* 路由已下线，新官网无 locale 前缀，导致这些被 Google 索引的旧链 404。
# 本脚本为每个旧路由生成一个 301 跳转桩（meta refresh + JS replace + canonical 指向主页），
# 让所有真实存在的旧链都跳回 https://juzibot.com/，并通过 noindex,follow 让 Google 淘汰旧链。
#
# 路由来源：Wayback CDX 抓取的 /zh /en 历史路由 + 人工发现的 /zh/culture 等 + 两语言互相镜像补全。
# 注意：这只能覆盖"已知/可枚举"的旧路由。对任意未知路径的兜底要靠 nginx error_page 404（见 deploy/nginx-never-404.conf）。

import os

ROOT = os.path.dirname(os.path.abspath(__file__))
HOME = "https://juzibot.com/"

TEMPLATE = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<link rel="icon" href="/favicon.ico" />
<title>句子互动 · 为企业部署 AI 员工</title>
<!-- 旧站 locale 路径已下线，跳回干净主页（绝对地址，不保留端口/路径/参数），权重归并到 canonical -->
<link rel="canonical" href="{home}">
<meta name="robots" content="noindex, follow">
<meta http-equiv="refresh" content="0; url={home}">
<script>location.replace('{home}');</script>
</head>
<body>
<p>页面已迁移，正在跳转到 <a href="{home}">juzibot.com</a>……</p>
</body>
</html>
"""

# 旧站每个 locale 下的页面后缀（不含前缀斜杠）。"" 代表 locale 根。
SUFFIXES = [
    "",
    "about-us",
    "about-us-m",
    "culture",
    "chatbot/practice-guide",
    # features
    "features/ai",
    "features/case",
    "features/internet",
    "features/rpa",
    "features/contact-platform",
    "features/customer",
    "features/customer-acquisition",
    "features/data-center",
    "features/management",
    "features/security",
    "features/sop",
    # solutions
    "solutions/consumer-goods",
    "solutions/customer-service",
    "solutions/education",
    "solutions/finance",
    "solutions/general",
    "solutions/health",
    "solutions/increase",
    "solutions/operate",
    # cases
    "cases",
    "cases/_26",
]
# 英文案例页 /en/cases/01 .. /en/cases/32（旧站抓到 01-32，缺 26，另有 _26）
SUFFIXES += [f"cases/{i:02d}" for i in range(1, 33) if i != 26]

LOCALES = ["zh", "en"]

# 旧站抓到的少量异常重复前缀，单独补
EXTRA_PATHS = [
    "en/en/features/ai",
    "en/en/features/rpa",
]


def write_stub(rel_dir):
    out_dir = os.path.join(ROOT, rel_dir) if rel_dir else ROOT
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, "index.html"), "w", encoding="utf-8") as f:
        f.write(TEMPLATE.format(home=HOME))


def main():
    paths = set()
    for loc in LOCALES:
        for suf in SUFFIXES:
            paths.add(f"{loc}/{suf}".rstrip("/"))
    paths.update(EXTRA_PATHS)

    for p in sorted(paths):
        write_stub(p)
    print(f"generated {len(paths)} redirect stubs under /zh and /en")


if __name__ == "__main__":
    main()
