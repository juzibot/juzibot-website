#!/usr/bin/env python3
"""
baseline_snapshot.py — 改版前站点基线快照生成器（website-redesign / 句子互动）。

在重构开始前，把"改版前"的静态站点固化成机器可读的基线，供 verify_site.py 校验
"内容 100% 保留、资源逐字节保留、内部链接全部可解析"等不变量。

产出三组参考集（设计文档 Baseline Snapshot 数据模型）：
  1. 每页内容字符串（per-page content strings）—— 用于内容保全比对（Req 2.1 / 2.5）。
  2. 资源文件 + 体积 + 校验和（assets size + sha256）—— 用于资源逐字节保全比对（Req 1.2 / 1.5）。
  3. 内部链接目标（internal link targets）—— 用于链接可解析性校验。

同时给当前站点打 git 标签 `pre-redesign`（归档整站源码，可供模块顺序等后续比对），
并把快照持久化到稳定位置 baseline/snapshot.json，verify_site.py 可直接读取。

仅依赖标准库，保持与 build_pages.py / build_redirects.py 一致的零依赖风格。
用法：  python baseline_snapshot.py
"""

import os
import sys
import json
import glob
import hashlib
import posixpath
import subprocess
from datetime import datetime, timezone
from html.parser import HTMLParser

ROOT = os.path.dirname(os.path.abspath(__file__))

# 基线标签 / 持久化位置
GIT_TAG = "pre-redesign"
BASELINE_DIR = os.path.join(ROOT, "baseline")
SNAPSHOT_PATH = os.path.join(BASELINE_DIR, "snapshot.json")

# 站点真实页面所在目录（相对仓库根，使用正斜杠）。
# 注意：zh/ 与 en/ 仅为 301 跳转桩，assets/demos/*.html 属于 Preserved_Asset（演示聊天框），
# 二者都不算"站点页面"，因此不在此处采集内容字符串。
PAGE_GLOBS = [
    "*.html",                       # 根页面：index/about/fde/industries/enterprise
    "products/*.html",              # 7 个产品页
    "products/*/*.html",            # products/shouhu-app/index.html
    "workforce/*.html",             # 6 个 AI 员工页
    "careers/index.html",           # 招聘页
]

# 资源目录（相对仓库根）。assets/ 下全部文件（含 demos/*.html 演示资产）；
# careers/ 下除 index.html（页面）外的全部文件。
ASSET_DIRS = ["assets", "careers"]


# ────────────────────────── HTML 解析 ──────────────────────────

class _PageParser(HTMLParser):
    """提取页面可见文本、标题、meta description、lang 以及 href/src 链接。"""

    # 这些标签内的文本不属于"已发布文案"，跳过。
    SKIP_TAGS = {"script", "style", "noscript", "template"}
    LINK_ATTRS = ("href", "src")

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.strings = []          # 可见文本（按文档顺序）
        self.raw_links = []        # 原始 href/src 属性值
        self.title = None
        self.meta_description = None
        self.lang = None
        self._skip_depth = 0
        self._in_title = False

    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        if tag in self.SKIP_TAGS:
            self._skip_depth += 1
        if tag == "title":
            self._in_title = True
        if tag == "html" and d.get("lang"):
            self.lang = d["lang"]
        if tag == "meta" and (d.get("name") or "").lower() == "description":
            self.meta_description = d.get("content")
        for attr in self.LINK_ATTRS:
            val = d.get(attr)
            if val and val.strip():
                self.raw_links.append(val.strip())

    def handle_startendtag(self, tag, attrs):
        # 自闭合标签（如 <meta/> <img/>）也要采集属性。
        self.handle_starttag(tag, attrs)
        if tag in self.SKIP_TAGS:
            self._skip_depth -= 1

    def handle_endtag(self, tag):
        if tag in self.SKIP_TAGS and self._skip_depth > 0:
            self._skip_depth -= 1
        if tag == "title":
            self._in_title = False

    def handle_data(self, data):
        if self._skip_depth > 0:
            return
        text = " ".join(data.split())  # 折叠空白
        if not text:
            return
        if self._in_title:
            self.title = ((self.title or "") + text).strip()
        else:
            self.strings.append(text)


def _is_internal(url):
    """判断 href/src 是否为站内链接（排除外链 / 协议链接 / 纯锚点）。"""
    low = url.lower()
    if low.startswith((
        "http://", "https://", "//",
        "mailto:", "tel:", "javascript:", "data:",
    )):
        return False
    if url.startswith("#"):
        return False
    return True


def _resolve_target(page_rel, url):
    """把站内链接解析为仓库相对目标路径（去掉查询串与锚点）。"""
    clean = url.split("#", 1)[0].split("?", 1)[0]
    if not clean:
        return None
    if clean.startswith("/"):
        target = clean.lstrip("/")
    else:
        base = posixpath.dirname(page_rel)
        target = posixpath.normpath(posixpath.join(base, clean))
    # 目录链接（以 / 结尾或解析到目录）补 index.html，便于解析校验。
    if url.rstrip().endswith("/") or target.endswith("/"):
        target = posixpath.join(target.rstrip("/"), "index.html")
    return target


# ────────────────────────── 采集逻辑 ──────────────────────────

def discover_pages():
    """返回排序后的页面相对路径列表（正斜杠）。"""
    found = set()
    for pattern in PAGE_GLOBS:
        for abs_path in glob.glob(os.path.join(ROOT, pattern.replace("/", os.sep))):
            rel = os.path.relpath(abs_path, ROOT).replace(os.sep, "/")
            found.add(rel)
    return sorted(found)


def snapshot_page(page_rel):
    """采集单个页面：内容字符串 + 元数据 + 内部链接。"""
    with open(os.path.join(ROOT, page_rel), "r", encoding="utf-8") as f:
        markup = f.read()

    parser = _PageParser()
    parser.feed(markup)
    parser.close()

    internal_links = []
    seen = set()
    for raw in parser.raw_links:
        if not _is_internal(raw):
            continue
        target = _resolve_target(page_rel, raw)
        if target is None:
            continue
        key = (raw, target)
        if key in seen:
            continue
        seen.add(key)
        internal_links.append({"raw": raw, "target": target})

    return {
        "title": parser.title,
        "meta_description": parser.meta_description,
        "lang": parser.lang,
        "content_strings": parser.strings,
        "internal_links": internal_links,
    }


def _sha256(abs_path):
    h = hashlib.sha256()
    with open(abs_path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def discover_assets(page_paths):
    """采集 ASSET_DIRS 下全部文件的体积与校验和；跳过被当作页面的文件。"""
    pages = set(page_paths)
    assets = {}
    for top in ASSET_DIRS:
        top_abs = os.path.join(ROOT, top)
        if not os.path.isdir(top_abs):
            continue
        for dirpath, _dirs, files in os.walk(top_abs):
            for name in files:
                abs_path = os.path.join(dirpath, name)
                rel = os.path.relpath(abs_path, ROOT).replace(os.sep, "/")
                if rel in pages:          # careers/index.html 等页面不计入资源
                    continue
                assets[rel] = {
                    "size": os.path.getsize(abs_path),
                    "sha256": _sha256(abs_path),
                }
    return dict(sorted(assets.items()))


# ────────────────────────── git 标签 ──────────────────────────

def _git(*args):
    return subprocess.run(
        ["git", *args], cwd=ROOT,
        capture_output=True, text=True,
    )


def tag_pre_redesign():
    """给当前提交打 `pre-redesign` 标签，归档改版前整站；已存在则保留。返回 (tag, commit)。"""
    commit = _git("rev-parse", "HEAD")
    commit_sha = commit.stdout.strip() if commit.returncode == 0 else None
    if commit_sha is None:
        print("warning: not a git repository or no commits; skipping tag", file=sys.stderr)
        return None, None

    exists = _git("rev-parse", "-q", "--verify", f"refs/tags/{GIT_TAG}")
    if exists.returncode == 0:
        print(f"git tag '{GIT_TAG}' already exists; keeping it")
    else:
        created = _git("tag", "-a", GIT_TAG, "-m", "Pre-redesign baseline snapshot")
        if created.returncode == 0:
            print(f"created git tag '{GIT_TAG}' at {commit_sha[:7]}")
        else:
            print(f"warning: could not create git tag '{GIT_TAG}': {created.stderr.strip()}",
                  file=sys.stderr)
    return GIT_TAG, commit_sha


# ────────────────────────── 主流程 ──────────────────────────

def build_snapshot():
    page_paths = discover_pages()
    pages = {rel: snapshot_page(rel) for rel in page_paths}
    assets = discover_assets(page_paths)
    git_tag, git_commit = tag_pre_redesign()

    total_strings = sum(len(p["content_strings"]) for p in pages.values())
    total_asset_bytes = 0
    for rel in assets:
        total_asset_bytes += assets[rel]["size"]

    return {
        "schema": "juzibot-baseline/1",
        "label": GIT_TAG,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "git_tag": git_tag,
        "git_commit": git_commit,
        "summary": {
            "page_count": len(pages),
            "content_string_count": total_strings,
            "asset_count": len(assets),
            "asset_total_bytes": total_asset_bytes,
        },
        "pages": pages,
        "assets": assets,
    }


def main():
    snapshot = build_snapshot()
    os.makedirs(BASELINE_DIR, exist_ok=True)
    with open(SNAPSHOT_PATH, "w", encoding="utf-8") as f:
        json.dump(snapshot, f, ensure_ascii=False, indent=2, sort_keys=False)
        f.write("\n")

    s = snapshot["summary"]
    rel_snapshot = os.path.relpath(SNAPSHOT_PATH, ROOT).replace(os.sep, "/")
    print(
        f"baseline snapshot written to {rel_snapshot}: "
        f"{s['page_count']} pages, {s['content_string_count']} content strings, "
        f"{s['asset_count']} assets ({s['asset_total_bytes']} bytes)"
    )


if __name__ == "__main__":
    main()
