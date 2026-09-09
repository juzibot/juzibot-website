#!/usr/bin/env python3
"""公众号「发布记录」→ 飞书登记表 自动登记(mp_publish_sync)。

## 这是什么

公众号源的进站路径是: 飞书《官网动态发布登记》表 → 运营勾「上官网」→ build_news.py 拉过闸行。
这条闸门(佳芮设计)本脚本**不碰**——它只解决闸门上游的体力活: 把微信「发布能力」接口里
已发布的文章(标题+永久链接+发布日期)自动登记成表里的新行, **不勾「上官网」**,
上不上站仍由人决定。跑一次, 运营就不用再手工贴链接。

## 覆盖边界(2026-08-12 穷尽验证, 详见 docs/NEWS_HANDOFF.md §6.5)

微信"发出去的文章"分两条通道, API 只看得见其中一条:
  发布(freepublish)  → 本脚本覆盖(实测 32 篇, 2023-09~2025-02)
  群发(常规推文)      → 无任何接口可枚举, 只能人工在后台复制链接
所以这个 feeder 补的是「接口发布」通道的存量与未来增量; 群发文章的登记仍走人工。

## IP 白名单

微信 token 接口按**调用方出口 IP** 鉴权, 白名单目前只有 38.76.164.215(佳芮 2026-08 配置)。
本机不在白名单时用 `--via-ssh root@38.76.164.215`: 抓取脚本经 stdin 送到远端执行,
secret 不出现在远端命令行(ps 看不见)、不落远端磁盘。

## 用法

  python3 mp_publish_sync.py                          # 干跑: 只打印将新增哪些行
  python3 mp_publish_sync.py --apply                  # 真写入登记表
  python3 mp_publish_sync.py --via-ssh root@38.76.164.215 --apply
  python3 mp_publish_sync.py --from-json arts.json    # 用现成抓取结果(跳过微信 API)

凭据: 环境变量 MP_APPID / MP_APPSECRET, 缺省退回 ~/projects/API-KEYS.md(与智谱 key 同款纪律,
**密钥严禁进仓库**)。⚠️ 白名单里有生产 IP = 有线上服务在用同一个 secret,
**绝不能调 reset/refresh 类接口**; 本脚本只用 token + freepublish/batchget 两个只读端点。

## 纪律

- 数据不进 git: 本脚本不写仓库任何文件, 产出只有登记表新行(方向 1 不破例)。
- 幂等: 链接已在表里 → 跳过; 归一化标题与已有行相同 → 也跳过(防止和运营手工登记的行
  重复——同一篇文章手工行往往先有标题后补链接, 只按链接判重会造出两行)。
- CI 不跑它: 依赖本机 lark-cli + 白名单出口, 与公众号源"CI 必然失败属设计内"同款约定。
"""
import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import urllib.request
from pathlib import Path

BASE_TOKEN = "HhPubortTafxOssddqJc4m9Znkd"
TABLE_ID = "tblykah8iZAdwLfF"
ACCOUNT = "句子互动官方"        # freepublish 归属号 = 凭据对应的号; 接其他号时传 --account
KEYS_FILE = Path.home() / "projects" / "API-KEYS.md"

# 远端抓取脚本模板: 只读 token + freepublish 翻页, 纯 stdlib。
# 经 stdin 传给远端 python3 执行, 凭据以格式化方式嵌入(不走命令行参数)。
_FETCH_SRC = r'''
import json, sys, urllib.request
APPID, SECRET = {appid!r}, {secret!r}
API = "https://api.weixin.qq.com"
def get(u):
    with urllib.request.urlopen(u, timeout=25) as r: return json.loads(r.read().decode())
def post(u, b):
    q = urllib.request.Request(u, data=json.dumps(b).encode(),
                               headers={{"Content-Type": "application/json"}})
    with urllib.request.urlopen(q, timeout=25) as r: return json.loads(r.read().decode())
tok = get(f"{{API}}/cgi-bin/token?grant_type=client_credential&appid={{APPID}}&secret={{SECRET}}")
if "access_token" not in tok:
    print(json.dumps({{"ok": False, "stage": "token", "resp": tok}})); sys.exit(1)
at = tok["access_token"]
items, off = [], 0
while True:
    d = post(f"{{API}}/cgi-bin/freepublish/batchget?access_token={{at}}",
             {{"offset": off, "count": 20, "no_content": 1}})
    if d.get("errcode"):
        print(json.dumps({{"ok": False, "stage": "batchget", "resp": d}})); sys.exit(1)
    b = d.get("item", [])
    for it in b:
        for a in (it.get("content") or {{}}).get("news_item", []):
            items.append({{"title": a.get("title", ""), "url": a.get("url", ""),
                           "update_time": it.get("update_time")}})
    off += len(b)
    if not b or off >= d.get("total_count", 0):
        break
print(json.dumps({{"ok": True, "items": items}}, ensure_ascii=False))
'''


def _keys_text():
    try:
        return KEYS_FILE.read_text(encoding="utf-8")
    except OSError:
        return ""


def mp_creds():
    """MP_APPID/MP_APPSECRET 环境变量优先, 退回 API-KEYS.md 的公众号行。"""
    appid = os.environ.get("MP_APPID", "")
    secret = os.environ.get("MP_APPSECRET", "")
    if appid and secret:
        return appid, secret
    t = _keys_text()
    m = re.search(r"AppID `(wx[0-9a-f]+)`.{0,80}?AppSecret `([0-9a-f]{32})`", t, re.S)
    if m:
        return m.group(1), m.group(2)
    raise SystemExit("缺公众号凭据: 设 MP_APPID/MP_APPSECRET 或在 API-KEYS.md 登记")


def fetch_published(via_ssh=""):
    """拉发布记录。via_ssh 非空时在远端(白名单机)执行, 否则本机直连。

    两种模式都是「脚本经 stdin 喂给 python3 -」: 凭据只存在于管道里,
    不上命令行(本机/远端的 ps 都看不见)、不落盘。本机直连仅当出口 IP 在白名单时可用。
    """
    appid, secret = mp_creds()
    src = _FETCH_SRC.format(appid=appid, secret=secret)
    cmd = (["ssh", via_ssh, "python3", "-"] if via_ssh
           else [sys.executable, "-"])
    p = subprocess.run(cmd, input=src, capture_output=True, text=True, timeout=180)
    raw = p.stdout
    i = raw.find('{"ok"')
    if i < 0:
        raise SystemExit(f"抓取无输出(白名单/网络?): {raw[-200:] or '(空)'}")
    d = json.loads(raw[i:raw.rindex("}") + 1])
    if not d.get("ok"):
        raise SystemExit(f"微信接口失败: {json.dumps(d, ensure_ascii=False)[:300]}")
    return d["items"]


def norm_title(s):
    """标题归一化判重: 去空白与常见标点、小写。表里手工行常与接口标题差个标点。"""
    s = re.sub(r"[\s　]+", "", s or "")
    return re.sub(r"[|｜,，。、!！?？:：\"\"''《》〈〉«»——\-–—…()（）\[\]【】]", "", s).lower()


def table_rows():
    """读登记表现状(标题/链接/记录 id), 供判重。依赖本机已授权 lark-cli。"""
    if not shutil.which("lark-cli"):
        raise SystemExit("lark-cli 不在 PATH(判重与写入都依赖它)")
    p = subprocess.run(["lark-cli", "base", "+record-list",
                        "--base-token", BASE_TOKEN, "--table-id", TABLE_ID,
                        "--limit", "200", "--format", "json"],   # CLI 上限 200; 表逼近时需翻页
                       capture_output=True, text=True, timeout=90)
    raw = p.stdout
    if "{" not in raw:
        raise SystemExit(f"record-list 无输出: {p.stderr[:200]}")
    d = json.loads(raw[raw.index("{"):])
    if not d.get("ok"):
        raise SystemExit(f"record-list 失败: {d.get('error')}")
    fields = d["data"]["fields"]
    return [dict(zip(fields, row)) for row in d["data"]["data"]]


def plan(items, existing, account=ACCOUNT):
    """算出该新增哪些行。纯函数, 供测试。"""
    seen_url = {(r.get("公众号正式链接") or "").strip() for r in existing}
    seen_title = {norm_title(r.get("文章标题")) for r in existing}
    seen_title.discard("")
    add, skip_url, skip_title = [], 0, 0
    for a in items:
        url = (a.get("url") or "").strip()
        title = (a.get("title") or "").strip()
        if not url or not title:
            continue
        if url in seen_url:
            skip_url += 1
            continue
        nt = norm_title(title)
        if nt in seen_title:
            skip_title += 1
            continue
        seen_url.add(url)
        seen_title.add(nt)
        row = {"文章标题": title, "公众号正式链接": url, "属于哪个号": account,
               "备注": "mp_publish_sync 自动登记(发布记录接口); 上站请勾「上官网」"}
        ts = a.get("update_time")
        if ts:
            row["发布日期"] = int(ts) * 1000     # 飞书 datetime 列收毫秒时间戳
        add.append(row)
    return add, skip_url, skip_title


def batch_create(rows):
    """按 lark-cli batch-create 的 fields+rows 格式写入, 每批 20 行。"""
    cols = ["文章标题", "公众号正式链接", "属于哪个号", "发布日期", "备注"]
    done = 0
    for i in range(0, len(rows), 20):
        chunk = rows[i:i + 20]
        payload = {"fields": cols,
                   "rows": [[r.get(c) for c in cols] for r in chunk]}
        p = subprocess.run(["lark-cli", "base", "+record-batch-create",
                            "--base-token", BASE_TOKEN, "--table-id", TABLE_ID,
                            "--json", json.dumps(payload, ensure_ascii=False)],
                           capture_output=True, text=True, timeout=120)
        out = p.stdout or p.stderr
        if '"ok": true' not in out and '"ok":true' not in out:
            raise SystemExit(f"写入失败(已成功 {done} 行): {out[:300]}")
        done += len(chunk)
    return done


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--apply", action="store_true", help="真写入登记表(默认干跑)")
    ap.add_argument("--via-ssh", default="", metavar="HOST",
                    help="在白名单机器上执行抓取, 如 root@38.76.164.215")
    ap.add_argument("--from-json", default="", metavar="FILE",
                    help="用现成抓取结果文件([{title,url,update_time},…]), 跳过微信 API")
    ap.add_argument("--account", default=ACCOUNT, help="「属于哪个号」列的值")
    args = ap.parse_args()

    if args.from_json:
        items = json.loads(Path(args.from_json).read_text(encoding="utf-8"))
    else:
        items = fetch_published(args.via_ssh)
    print(f"发布记录: {len(items)} 篇")

    existing = table_rows()
    print(f"登记表现有: {len(existing)} 行")

    add, skip_url, skip_title = plan(items, existing, args.account)
    print(f"跳过: 链接已登记 {skip_url} · 标题已登记 {skip_title}")
    print(f"待新增: {len(add)} 行\n")
    for r in add:
        d = r.get("发布日期")
        from datetime import datetime, timezone, timedelta
        ds = (datetime.fromtimestamp(d / 1000, tz=timezone(timedelta(hours=8)))
              .strftime("%Y-%m-%d") if d else "----")
        print(f"  {ds}  {r['文章标题'][:44]}")

    if not add:
        print("\n没有要新增的行, 结束。")
        return
    if not args.apply:
        print("\n(干跑结束——加 --apply 真写入)")
        return
    n = batch_create(add)
    print(f"\n已写入登记表 {n} 行(均未勾「上官网」, 上站与否由运营决定)")


if __name__ == "__main__":
    main()
