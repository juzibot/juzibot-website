#!/usr/bin/env python3
"""mp_publish_sync 的离线测试(纯 stdlib, 不联网, 不要凭据, 秒级)。

守的都是真踩过或必然会踩的坑:
- 判重必须双通道(链接 + 归一化标题): 运营手工行常「先有标题、链接空着」——
  只按链接判重会给同一篇文章造出第二行, 13 行手工登记正是这个形态。
- 标题归一化要吃掉标点差异: 接口标题带书名号/竖线, 手工抄写常丢。
- 发布日期转毫秒: 飞书 datetime 列收 ms, 传秒会变成 1970 年。
- 干跑不写: plan() 是纯函数, 不许有任何副作用。
"""
import sys

import mp_publish_sync as M

FAIL = 0


def check(name, cond, detail=""):
    global FAIL
    if cond:
        print(f"  ok  {name}")
    else:
        FAIL += 1
        print(f"  FAIL {name}  {detail}")


print("norm_title:")
check("标点差异归一", M.norm_title("句子干货｜《22张活动执行表格》") == M.norm_title("句子干货 22张活动执行表格"))
check("空白归一", M.norm_title("A  B　C") == M.norm_title("ABC"))
check("大小写归一", M.norm_title("Bot Friday") == M.norm_title("bot friday"))
check("空串安全", M.norm_title(None) == "")

print("plan 判重:")
existing = [
    {"文章标题": "已有链接的行", "公众号正式链接": "https://mp.weixin.qq.com/s/abc"},
    {"文章标题": "只有标题的手工行（链接空）", "公众号正式链接": None},
]
items = [
    {"title": "新文章一", "url": "https://mp.weixin.qq.com/s/new1", "update_time": 1700000000},
    {"title": "已有链接的行", "url": "https://mp.weixin.qq.com/s/abc", "update_time": 1700000000},
    {"title": "只有标题的手工行（链接空）", "url": "https://mp.weixin.qq.com/s/new2", "update_time": 1700000000},
    {"title": "", "url": "https://mp.weixin.qq.com/s/notitle", "update_time": 1700000000},
    {"title": "无链接文章", "url": "", "update_time": 1700000000},
    {"title": "新文章一", "url": "https://mp.weixin.qq.com/s/dup-in-batch", "update_time": 1700000000},
]
add, skip_url, skip_title = M.plan(items, existing)
check("只新增 1 行", len(add) == 1, f"got {len(add)}: {[r['文章标题'] for r in add]}")
check("链接判重命中 1", skip_url == 1, f"got {skip_url}")
check("标题判重命中手工行+批内重复", skip_title == 2, f"got {skip_title}")
check("缺题/缺链接静默丢弃", all(r["文章标题"] and r["公众号正式链接"] for r in add))

print("行构造:")
row = add[0]
check("日期转毫秒", row["发布日期"] == 1700000000 * 1000, f"got {row.get('发布日期')}")
check("默认归属号", row["属于哪个号"] == "句子互动官方")
check("不带上官网字段(闸门归人)", "上官网" not in row)
check("备注注明来源", "自动登记" in row["备注"])

print("plan 无副作用:")
before = [dict(r) for r in existing]
M.plan(items, existing)
check("existing 未被改动", existing == before)

print("凭据纪律:")
src = open("mp_publish_sync.py", encoding="utf-8").read()
import re
check("仓库无明文 AppSecret", not re.search(r"[\"'][0-9a-f]{32}[\"']", src))
check("仓库无明文 AppID", not re.search(r"wx[0-9a-f]{16}", src))

if FAIL:
    print(f"\n{FAIL} 项失败")
    sys.exit(1)
print("\n全部通过")
