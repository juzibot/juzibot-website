# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

The marketing site for 句子互动（JuziBot），served at https://juzibot.com. Pure static HTML/CSS/JS — **no Node, no package.json, no bundler**. Two Python scripts generate a subset of the pages; everything else is hand-edited HTML. All copy is Simplified Chinese.

## Build commands

```bash
python3 build_redirects.py  # regenerate /zh/* and /en/* 301 redirect stubs
# python3 build_pages.py    # ⚠️ STALE — do NOT run, it regresses hand-edited pages (see below)
```

There is no single "build everything" command and no lint/test. The deploy server just serves the working tree, it does not run Python — all HTML is committed and hand-maintained.

## ⚠️ build_pages.py is STALE — do NOT run it

`build_pages.py` generated the first version of the product/workforce/`fde`/`enterprise`/`industries`/`about` pages, but it has **not been kept in sync**. The committed HTML for those pages was hand-edited afterward (e.g. workforce pages got the `role-hero` + 活体工牌条 layout the script never emitted). **Re-running `python3 build_pages.py` regresses all those pages back to the old, plainer output — don't run it.**

Treat **every HTML page as hand-maintained** and edit it directly. The build script is kept only as historical reference; if you change a generated-looking page, change the HTML, not the Python.

Hand-edit these directly:
- `index.html` — the homepage (largest file; all styles inline in a `<style>` block, not site.css). The "在岗 AI 员工" 长廊 is data-driven from the `EMP` array near the bottom; add a role there + a poster in `careers/emp-v2-*.{png,svg}`.
- `products/*.html`, `workforce/*.html`, `fde.html`, `enterprise.html`, `industries.html`, `about.html`
- `careers/`, `products/shouhu-app/`, `en/`, `zh/`

## 动态页 news.html 与 build_news.py（可安全运行）

动态信息流有三个平行版本（互带切换入口，做对比实验），**三版均为全源**：`news.html`（导航「动态」，卡片流 A 版）、`news-b.html`（知乎式双栏列表流 B 版，侧栏带数据源健康面板）、`news-c.html`（齐思式聚合流 C 版，按月分组 + 数据源面板）。B/C **noindex + canonical 指向 A 防重复收录**，未进全站导航。筛选统一为两级：一级按来源，二级分类条仅在选中单一来源且该源分类数 >1 时浮现；每条内容带彩色来源徽章（色值/图标三页需同步：`s-rui-blog`/`s-wechat-mp`/`s-industry` + 各页 JS 的 ICON 表）。Wechaty 源已撤（2026-07-07，开发者向内容对官网受众是噪音），恢复方法见 build_news.py 内注释。

内容源走 adapter（脚本 `SOURCES`）：`sitemap`（rui 博客逐篇抓 JSON-LD）、`rss`（RSS2/Atom 通吃 + 脏 XML 正则兜底；现有 Wechaty 社区博客/Releases、36氪）、`feishu-base`（**公众号发布闸门**：飞书多维表格《官网动态发布登记》https://juzihudong.feishu.cn/base/HhPubortTafxOssddqJc4m9Znkd ，运营发文后贴公众号正式链接+勾「上官网」，管线走本机已授权的 lark-cli 只拉过闸行，og 元数据自动补齐；三个公众号——句子互动官方/AI对话未来/佳芮的创业笔记——同一张表，账号名落 category 显示为条目小标签）、`manual`（本地 JSON 投递位，备用，当前无源使用）。公众号内容的上游草稿在句子互动飞书 wiki「文章初稿」目录，但 wiki 链接访客不可见，官网只放公众号正式链接。

与 build_pages.py 不同，**`python3 build_news.py` 可以安全反复运行**（增量；`--full` 全量重抓，且只刷新不删除——本次没抓回来的历史条目自动沿用旧数据，单篇/单源失败不丢内容）。外部源用 `keep_max` 设存量上限（36氪 60 条，超出修剪最老的），自家内容源不设限。公众号条目拿不到网页发布时间时，退回登记表「发布日期」列；两头都空该行不上站（禁止拿"今天"顶包，那会把旧文顶到流最前）。它每次运行只重写每页三个标记区块——`<!-- NEWS:LIST:BEGIN/END -->`（前 20 条预渲染，SEO 唯一入口）、`<script id="news-data">`（内联数据，A/B=数组、C=含 sources 的对象）、`<b id="newsTotal">`（总数）——页面其余部分照常手工维护。数据落 `data/news.json`（含各源健康元数据）。条目模板成对同步：`card_html()`↔A 页 `cardHTML()`、`row_html()`↔B 页 `rowHTML()`、`feed_item_html()/feed_list()`↔C 页 `itemHTML()/render()`（含月份分组逻辑），改一处必须同步对应 JS。每条「问句子」按钮通过改写 `window.PAGE_CTX` 后调 `window.openAskbar()` 实现，未动 askbar.js 内部。

## Nav & footer are in `assets/site.js`

Subpages inject the shared nav/footer at runtime: `<div id="site-nav"></div>` / `<div id="site-footer"></div>` + `window.SITE_REL` + `assets/site.js`. **The product/workforce menus live in the `NAV`/`FOOTER` strings in `assets/site.js`** — adding a product or AI-员工 role means editing those (plus the `ENT` map + a route in `assets/askbar.js` so the page shows up as a related card / intent answer). `index.html` and `careers/index.html` carry their **own inline nav/footer** (not injected), so update those two by hand as well. Each page sets `window.PAGE_CTX = {entity, type, title}`.

When adding a workforce page, the fastest correct path is to **copy an existing `workforce/*.html` (e.g. `hr.html`)** and rewrite the content — it already has the right chrome, `rel='../'` paths, and reveal animations.

## Styling & assets

- Generated subpages link `assets/site.css`; `index.html` carries its own large inline `<style>`. Changing a generated page's look is usually `assets/site.css`, not the Python.
- `assets/site.js`, `assets/askbar.js` — shared scripts. `assets/demos/*.html` are standalone interactive product mockups embedded via iframe. `assets/product-shots/`, `assets/brand/` hold images (incl. `qr-qiwei.png`, the contact QR).
- Contact CTAs across the site call `openContact(...)` which opens a WeChat-work QR modal — there is no form backend.

## Deploy

`.github/workflows/deploy.yml` triggers on push to **`stage-1`** or **`stage-2`** (and manual dispatch). It SSHes to the server and does `git checkout -f` + `git clean -fd` into `/opt/www/jz-<branch>`. Other branches (including `main` and feature branches like `polish/*`) do **not** deploy. nginx config in `deploy/nginx-never-404.conf` redirects any unknown path back to the homepage instead of 404ing.

`build_redirects.py` exists because the old bilingual site used `/zh/*` and `/en/*` routes that Google indexed; the stubs 301 those legacy URLs to the clean homepage. Re-run it only if legacy routes change.

## Product & role vocabulary

Seven products, each with a body-part metaphor — use these exact names in copy:
秒回·工位、秒懂·大脑、守护·主管、参谋·参谋（句子问数）、智库·记忆、CLI·手、智造·地基。
Seven AI workforce roles: 销售（sales）、导购（marketing）、客服（service）、社工/调解员（government）、理财顾问（finance）、HR（hr）、GEO 优化师（geo）. GEO 优化师 is the only one without an "AI" prefix — it's framed as "AI 时代的 SEO"（生成式引擎优化）, deliberately standing out in the menu.

## Copy & naming rules

This is outward-facing content. Follow the writing style in the global config (Paul-Graham-plain Chinese, no AI-isms). For any signature/author/contact text use **「李佳芮」**, never the English name "Grace" — grep generated output for `grace` before shipping.
