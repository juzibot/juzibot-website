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
