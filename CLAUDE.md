# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

The marketing site for 句子互动（JuziBot），served at https://juzibot.com. Pure static HTML/CSS/JS — **no Node, no package.json, no bundler**. Two Python scripts generate a subset of the pages; everything else is hand-edited HTML. All copy is Simplified Chinese.

## Build commands

```bash
python3 build_pages.py      # generate the data-driven pages (see below)
python3 build_redirects.py  # regenerate /zh/* and /en/* 301 redirect stubs
```

There is no single "build everything" command and no lint/test. Generated output is **committed to the repo** — the deploy server just serves the working tree, it does not run Python.

## The critical distinction: generated vs hand-edited

`build_pages.py` is a Python file that emits HTML by string concatenation. It overwrites these paths on every run:

- `products/{miaohui,miaodong,shouhu,dongxing,cli}.html`
- `workforce/{sales,marketing,service,government,finance,hr}.html`
- `fde.html`, `enterprise.html`, `industries.html`, `about.html`

**Editing any of those HTML files directly is wasted work — the next `build_pages.py` run wipes it.** To change them, edit the corresponding `page_*()` / shared-snippet function in `build_pages.py`, then re-run it.

Everything else is hand-maintained HTML, edit it directly:
- `index.html` — the homepage (largest file; all styles inline in a `<style>` block, not site.css)
- `products/canmou.html`, `products/zhizao.html` — two product pages NOT in the build script
- `careers/`, `products/shouhu-app/`, `en/`, `zh/`

When unsure whether a page is generated, check the `pages` dict at the bottom of `build_pages.py` (`if __name__ == '__main__'`).

## Architecture of build_pages.py

Shared snippet builders produce the chrome every generated page reuses — keep them as the single source of truth:
- `nav_html(rel)` / `footer_html(rel)` — the nav and footer. The product/workforce menus are hardcoded here, so adding a product means editing these strings.
- `page_layout(...)` — full-page wrapper (head, hero, breadcrumbs, floating contact panel, QR contact modal, `openContact()` JS).
- `feat_grid`, `kpi_row`, `split_section`, `block`, `cta_band`, `cta_section` — content blocks.

The `rel` argument (`''` for root pages, `'../'` for `products/` and `workforce/`) prefixes every internal link and asset path. Pass it correctly for any new page or links/images 404.

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
Six AI workforce roles: 销售、导购、客服、社工/调解员、理财顾问、HR.

## Copy & naming rules

This is outward-facing content. Follow the writing style in the global config (Paul-Graham-plain Chinese, no AI-isms). For any signature/author/contact text use **「李佳芮」**, never the English name "Grace" — grep generated output for `grace` before shipping.
