#!/usr/bin/env python3
"""动态页内容中台：飞书多维表格 ←→ 管线。

    python3 hub.py pull            # 中台 → 本地投递位(干跑，看会改什么)
    python3 hub.py pull --apply    # 真写本地投递位
    python3 hub.py push            # 管线状态 → 中台回写(干跑)
    python3 hub.py push --apply    # 真回写
    python3 hub.py status          # 一屏看清各源卡在哪

## 为什么要有中台

动态页八个源里，四个靠人工投递。它们现在的入口是散的，而且**大多要开发者才碰得到**：

| 源 | 现在的入口 | 结果 |
|---|---|---|
| 公众号 | 飞书表 | 42 行，运营能自己动 |
| 产品动态 | `data/product-news.json` | 5 条，改一次要找开发者 |
| 媒体报道 | `data/press-news.json` | **0 条，从没人录过** |
| 公司动态 | `data/company-news.json` | 20 条草稿，卡在口径确认 |

媒体报道 0 条是最硬的证据：不是公司没有媒体报道，是**入口在 git 里，运营碰不到**。
唯一一个非开发者能自己动的源（公众号），恰好就是唯一一个有飞书表的源。

## 三个设计决策

**一·一张表，不按源拆表。** 运营的心智是「我要往动态页放一条内容」，不是
「我要往产品动态表放一条」。按源拆表是按系统实现分的，会先逼人做一道
「这该放哪」的选择题。代价是不同源字段不同（公司动态有正文无链接，其余相反），
用「来源」单选 + 按来源的必填校验解决，而不是拆表。

**二·状态必须回写。** 这是中台区别于现有那张登记表的关键。现在那张表**只有输入
没有反馈**：运营勾了「上官网」之后不知道到底上没上、什么时候上的、链接是什么，
每次都得来问开发者。没有回写，中台就只是个提交箱。所以管线要写回四件事：
上站状态 / 站内链接 / 最后同步 / 管线消息。

**三·口径检查前置。** 企微红线现在在 CI 才拦，而 CI 红的时候人已经在别的事上了，
非开发者也看不懂 CI。表里用公式字段当场标出来——录入时就知道，不用等。

## 不做什么（同样是设计）

- **不在表里编辑 HTML 正文。** 公司动态的 body 是 HTML 片段，多维表格没有 HTML
  编辑器，硬编辑只会产出坏 HTML。正文继续走飞书文档，表里放「正文文档」链接。
- **不做自动上站。**「上官网」是佳芮定的人工闸门，中台不绕过它。
- **不替代 git。** 管线代码、页面模板仍在 git；中台只管内容。
- **不碰自动源。** 博客/行业/大咖/HN/齐思本来就不用人管，进中台只会添乱。

## 数据流

    人在表里填 + 勾「上官网」
        ↓  hub.py pull
    data/{product,press,company}-news.json  ← 管线的既有投递位，格式不变
        ↓  build_news.py（一个字没改）
    上站 → data/news.json
        ↓  hub.py push
    表里的「上站状态/站内链接/最后同步」变绿

**刻意让中台落到既有投递位，而不是让 build_news.py 直连中台。** 理由：管线不该
多一个必须联网+授权才能跑的依赖（CI 里没有 lark-cli，这是既定约束）。中台挂了、
飞书挂了、授权过期了，管线照常按上次拉下来的投递位跑——降级成「内容不更新」，
而不是「管线跑不动」。
"""
import argparse
import json
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BASE_TOKEN = "HhPubortTafxOssddqJc4m9Znkd"
TABLE_ID = "tbl6imPDUR9WZFPa"          # 内容中台
SITE_BASE = "https://juzibot.com"

# 中台「来源」→ (本地投递位, 管线里的 source id)
# 公众号不在此列: 它已有「发布登记」表与 feishu-base adapter, 通路是通的,
# 这轮不动它——能用的东西不要为了统一而重做。
DEST = {
    "产品动态": ("data/product-news.json", "product"),
    "媒体报道": ("data/press-news.json", "press"),
    "公司动态": ("data/company-news.json", "company"),
}

# 必填项按来源分。公司动态没有站外原文(正文即内容), 其余必须有链接。
REQUIRED = {
    "产品动态": ("标题", "原文链接"),
    "媒体报道": ("标题", "原文链接"),
    "公司动态": ("标题", "发布日期"),
    "公众号": ("标题", "原文链接"),
}


def lark(args, timeout=120):
    p = subprocess.run(["lark-cli", "base"] + args, capture_output=True, text=True, timeout=timeout)
    if "{" not in p.stdout:
        raise SystemExit(f"lark-cli 无输出（没装或没授权？）: {p.stderr[:200]}")
    d = json.loads(p.stdout[p.stdout.index("{"):])
    if not d.get("ok"):
        raise SystemExit(f"飞书接口失败: {json.dumps(d.get('error'), ensure_ascii=False)[:300]}")
    return d


def read_hub():
    """读中台全表 → [{字段: 值, _rid: 记录id}]。"""
    d = lark(["+record-list", "--base-token", BASE_TOKEN, "--table-id", TABLE_ID,
              "--limit", "200", "--format", "json"])
    data = d["data"]
    fields, rids = data["fields"], data["record_id_list"]
    out = []
    for rid, row in zip(rids, data["data"]):
        rec = dict(zip(fields, row))
        rec["_rid"] = rid
        s = rec.get("来源")
        rec["来源"] = s[0] if isinstance(s, list) and s else (s or "")
        out.append(rec)
    return out


def ymd(v):
    """飞书 datetime → YYYY-MM-DD；空返回 ''。

    ★ 写入与回读的形状不一样 ★ 写进去要毫秒时间戳(int)，读出来却是 ISO 字符串
    (`2024-01-10T00:00:00.000+08:00`)。第一版只处理了数字，字符串走 int() 抛异常被
    except 吞成空串——于是公司动态的 (标题,日期) 键全部对不上，body 接回逻辑静默失效，
    **一次 pull 清空了二十篇月报的正文、一万字**（备份救回来的）。
    静默兜底 + 形状假设，是这类数据丢失最常见的组合。"""
    if not v:
        return ""
    if isinstance(v, str):
        return v[:10] if len(v) >= 10 and v[4] == "-" else ""
    try:
        return time.strftime("%Y-%m-%d", time.localtime(int(v) / 1000))
    except (TypeError, ValueError):
        return ""


def one(v):
    """单选字段回读是数组(`['已上站']`)，写入却要标量。取标量。"""
    if isinstance(v, list):
        return v[0] if v else ""
    return v or ""


def url(v):
    """url 字段回读是 Markdown(`[text](href)`)，写入却是裸串。取裸 href。

    不归一化的后果不是显示错，是**每轮都判定"变了"→ 无限重复回写**：
    比较时拿裸 URL 对 Markdown 串，永远不相等。「最后同步」会被刷成噪音，
    也就看不出哪行真的动过——回写的意义正在于让人看出变化。"""
    if not v:
        return ""
    v = str(v).strip()
    if v.startswith("[") and v.endswith(")") and "](" in v:
        return v[v.rindex("](") + 2:-1]
    return v


def gate(rec):
    """这行能不能上站 → (可以吗, 原因)。判据与 build_news 一致, 不另立一套。"""
    src = rec.get("来源") or ""
    if not rec.get("上官网"):
        return False, "未勾「上官网」"
    if rec.get("口径检查"):
        return False, "口径检查未过：含企微字样"
    for f in REQUIRED.get(src, ("标题",)):
        v = rec.get(f)
        if not (str(v).strip() if v else ""):
            return False, f"缺「{f}」"
    return True, ""


# ---------------------------------------------------------------- pull
def pull(apply=False):
    """中台 → 本地投递位。只写过闸的行；被拦下的原因原样回写进管线消息。"""
    recs = read_hub()
    buckets = {k: [] for k in DEST}
    blocked = []
    for r in recs:
        src = r.get("来源")
        if src not in DEST:
            continue
        ok, why = gate(r)
        if not ok:
            blocked.append((r, why))
            continue
        e = {"url": url(r.get("原文链接")),
             "title": (r.get("标题") or "").strip(),
             "date": ymd(r.get("发布日期"))}
        for k, f in (("summary", "摘要"), ("category", "分类"), ("author", "署名")):
            v = (r.get(f) or "").strip()
            if v:
                e[k] = v
        buckets[src].append(e)

    for src, (path, _sid) in DEST.items():
        p = ROOT / path
        cur = json.loads(p.read_text(encoding="utf-8")) if p.exists() else {"items": []}
        old_items = cur.get("items", [])
        new_items = buckets[src]

        # 公司动态的正文(body)只在本地 JSON 里, 中台不承载 HTML——按标题+日期把
        # 已有 body 接回去, 否则一次 pull 就把二十篇月报的正文清空了。
        if src == "公司动态":
            bodies = {(i.get("title"), i.get("date")): i.get("body")
                      for i in old_items if i.get("body")}
            for e in new_items:
                b = bodies.get((e["title"], e["date"]))
                if b:
                    e["body"] = b
                e.pop("url", None)          # 公司动态无站外原文, 留空由管线合成锚点

        print(f"  {src:<6s} 中台过闸 {len(new_items):>2d} 条 · 本地现有 {len(old_items):>2d} 条"
              f" → {path}")
        if apply:
            cur["items"] = new_items
            p.write_text(json.dumps(cur, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")

    if blocked:
        print(f"\n  闸外 {len(blocked)} 条：")
        for r, why in blocked[:8]:
            print(f"    · [{r.get('来源')}] {(r.get('标题') or '')[:30]} —— {why}")
        if len(blocked) > 8:
            print(f"    …另 {len(blocked)-8} 条")
    if not apply:
        print("\n  (干跑，加 --apply 真写本地投递位)")
    return blocked


# ---------------------------------------------------------------- push
def push(apply=False):
    """管线状态 → 中台。没有这一步, 中台只是个提交箱。"""
    news = ROOT / "data" / "news.json"
    if not news.exists():
        raise SystemExit("data/news.json 不在——先跑一次 build_news.py（或在有产物的分支上跑）")
    d = json.loads(news.read_text(encoding="utf-8"))
    items = d["items"] if isinstance(d, dict) else d
    # 上站条目按 url 与 (标题,日期) 双索引: 公司动态的 url 是合成锚点, 表里没有
    by_url = {(i.get("url") or "").strip(): i for i in items}
    by_td = {((i.get("title") or "").strip(), (i.get("date") or "")[:10]): i for i in items}

    recs = read_hub()
    updates = []
    for r in recs:
        if r.get("来源") not in DEST and r.get("来源") != "公众号":
            continue
        ok, why = gate(r)
        link_in = url(r.get("原文链接"))
        hit = by_url.get(link_in) if link_in else None
        if hit is None:
            hit = by_td.get(((r.get("标题") or "").strip(), ymd(r.get("发布日期"))))

        if hit:
            state, msg = "已上站", ""
            link = f"{SITE_BASE}/news/p/{hit['id']}.html"
        elif not ok:
            state, msg, link = ("未提交" if why == "未勾「上官网」" else "失败"), why, ""
        else:
            state, msg, link = "待上站", "已过闸，等下一次管线运行", ""

        patch = {"上站状态": state, "管线消息": msg, "站内链接": link,
                 "最后同步": int(time.time() * 1000)}
        # 只在真变了时才写: 每轮无条件回写会把「最后同步」刷成噪音, 也看不出哪行真动过
        if (one(r.get("上站状态")) != state or (r.get("管线消息") or "") != msg
                or url(r.get("站内链接")) != link):
            updates.append((r["_rid"], patch, r))

    print(f"  需回写 {len(updates)} 行（共 {len(recs)} 行）")
    for _rid, p, r in updates[:8]:
        print(f"    · [{r.get('来源')}] {(r.get('标题') or '')[:26]:<28s} → {p['上站状态']}"
              + (f"  {p['管线消息']}" if p["管线消息"] else ""))
    if len(updates) > 8:
        print(f"    …另 {len(updates)-8} 行")
    if not apply:
        print("\n  (干跑，加 --apply 真回写)")
        return updates
    # 逐条 patch: batch-update 的同一 patch 应用到所有记录, 而这里每行状态不同
    for i, (rid, patch, _r) in enumerate(updates, 1):
        lark(["+record-batch-update", "--base-token", BASE_TOKEN, "--table-id", TABLE_ID,
              "--json", json.dumps({"record_id_list": [rid], "patch": patch},
                                   ensure_ascii=False)])
    print(f"  已回写 {len(updates)} 行")
    return updates


# ---------------------------------------------------------------- status
def status():
    """一屏看清各源卡在哪——这个视角现在只存在于开发者脑子里。"""
    recs = read_hub()
    import collections
    by_src = collections.defaultdict(lambda: collections.Counter())
    reasons = collections.Counter()
    for r in recs:
        src = r.get("来源") or "(未填来源)"
        ok, why = gate(r)
        by_src[src]["总数"] += 1
        by_src[src]["过闸" if ok else "闸外"] += 1
        if not ok:
            reasons[why] += 1
    print(f"{'来源':<10s}{'总数':>5s}{'过闸':>6s}{'闸外':>6s}")
    for src, c in sorted(by_src.items()):
        print(f"{src:<10s}{c['总数']:>5d}{c['过闸']:>6d}{c['闸外']:>6d}")
    if reasons:
        print("\n闸外原因分布：")
        for why, n in reasons.most_common():
            print(f"  {n:>3d}  {why}")


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("cmd", choices=["pull", "push", "status"])
    ap.add_argument("--apply", action="store_true", help="真写（默认干跑）")
    a = ap.parse_args()
    {"pull": lambda: pull(a.apply), "push": lambda: push(a.apply), "status": status}[a.cmd]()


if __name__ == "__main__":
    main()
