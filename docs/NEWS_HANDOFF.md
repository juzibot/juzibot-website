# 官网动态页 · 交接书(HANDOFF)

> 写于 2026-07-29。接手人先读这一页,再读 `CLAUDE.md` 的「动态页 news.html 与 build_news.py」节(那节是长期规格,本页是**当下状态与待办**)。
> 一句话现状:**代码与评审都齐了(PR#103 已收敛),卡在运维的一步 nginx include + 一次 seed,没上线。**

---

## 1. 这是什么

`news.html`(卡片版 A,进导航「动态」)与 `news-c.html`(聚合版 C,noindex + canonical 指 A)两页同源多源信息流:
八个内容源 → AI 加工(筛选/锐评/简报译题/全文翻译/概念抽取)→ 静态详情页 `news/p/<id>.html` + 概念页 `news/c/<slug>.html`。
管线是 `build_news.py`(单文件,增量,可安全反复运行);定时靠 `.github/workflows/news-cron.yml` 每 6 小时。

**当前八源**:rui 博客 / 公众号(飞书登记表闸门) / 产品动态 / 媒体报道 / 行业动态(5 路 RSS) / 大咖观点(8 路 RSS) / Hacker News / 齐思。
**已下线源**:Wechaty(2026-07-07,开发者向内容对官网受众是噪音)、**企微生态 wecom(2026-07-27,佳芮:企微不出现在任何页面)**——两者恢复/删除的痕迹都在 build_news.py 注释里。

## 2. 架构裁决(为什么长这样,别推翻)

**方向 1:生成物不进 git**(2026-07-23 佳芮裁决,PR#103 的核心重构)。
仓库只留「配方」:`build_news.py` + 两个 workflow + 页面模板壳 + 人工种子(`data/product-news.json`、`data/press-news.json`)。
`news/`、`data/news.json`、`data/concepts.json`、`data/render-cache.json`、`data/news-content/` 全部 gitignore。

数据流(**状态以服务器为准闭环**):
```
CI 每 6h:  rsync 拉服务器 /opt/www/jz-news/{data,news}/ → 跑 build_news.py(增量) → rsync --delete 推回
           不 commit、不 push、仓库零机器提交
对外路由:  nginx 把 /news.html /news-c.html /news/ 指到 /opt/www/jz-news/(data/ 不对外)
```
被否掉的两条路(别走回头路):①生成物入库(仓库膨胀 + 每天 4 个机器 commit 和人的分支互相 rebase);②Git LFS(只解决图片体积,没解决生成物入库这件事本身;且免费额度 1GB/月会撞限)。

## 3. 当前状态(2026-07-29 实测)

| 项 | 状态 |
|---|---|
| **PR#103**(feat/dynamic-news-page) | **OPEN,已收敛**——HEAD `9418c55`,Bugbot 审的就是 HEAD、零未解决发现 |
| 佳芮 2026-07-24 三条 review | 全部已改并回帖:①筛选栏样式 ②去企微 ③首屏公司相关优先 |
| main | 不含动态页(`23df654`,PR#104 口径清理已并) |
| stage-2 预览 | 已推:overlay 三文件 + 本地真跑管线产物(仅预览,**不回流 PR**) |
| 线上 juzibot.com | **动态页尚未上线**(等第 4 节的三步) |

**stage-2 预览是怎么回事(重要,别搞混)**:stage-2 仍是老架构(生成物入库),PR#103 是新架构(不入库),两者**不能直接 merge**(会把 stage-2 的 news 页变空壳且它没配 nginx-news)。所以预览用的是「**文件覆盖 + 本地真跑管线**」:把 feat 的 `build_news.py`/`news.html`/`news-c.html` 三个文件覆盖到 stage-2,本地跑一遍管线,产物提交进 stage-2。**这是一次性预览手段,不是流程**;PR#103 合并后 stage-2 应回到统一架构。

## 4. 上线三步(唯一待办路径)

1. **运维:nginx include**——把 `deploy/nginx-news.conf`(三条 location:`/news.html`、`/news-c.html`、`/news/`)include 进 jz-main / jz-stage-* 的 server 块并 reload。**这是唯一需要人肉配合的一步。**
2. **跑一次 seed**——Actions → news-cron → Run workflow → 勾 `seed`:从 `SEED_REF`(64bec20,最后一个含全量产物的提交,图片在 LFS)把存量推到 `/opt/www/jz-news/`。**只需一次**;不 seed 的话常规轮会按设计直接失败(防止空状态全量重抓烧光 AI 配额)。
3. **合并 PR#103** —— schedule 只认默认分支上的 workflow 文件,进 main 后每 6 小时定时才生效。

①② 做完页面即刻有内容,③ 的顺序无硬依赖。完整手册见 `docs/DEPLOY.md`。

## 5. 运维须知(踩过的坑)

- **智谱 key**:仓库 Secret `ZHIPU_API_KEY`(模型 `glm-4-air`;flash 会把非 AI 资讯放进来,已弃)。缺 key 时管线**优雅降级**——新条目 pending 暂缓上站,下轮补判,已上站内容不受影响。本地开发退回读 `~/projects/API-KEYS.md`;**密钥严禁进仓库**。
- **公众号源在 CI 里必然失败**(依赖本机 lark-cli):这是设计内的,管线沿用旧数据。公众号新文要本机跑一次 `python3 build_news.py` 再手动 rsync。
- **图片不 --delete**:`news/img/` 一次性下载不可重下,推送步骤故意不带 `--delete`,并且推送前 `mkdir -p news/img` 兜底(否则目录缺失会 set -e 中断,造成「p/c 已删完而 data/ 没推回」的页与状态不一致)。
- **拉回状态有校验门**:`data/news.json` 缺失/解析失败/零条目一律中止——防止随后的 `--delete` 清空服务器。
- **别跑 `build_pages.py`**(仓库另一个脚本,已 STALE,会把手工页面打回旧版)。`build_news.py` 则可安全反复跑。

## 6. 改动纪律

- **模板成对同步**:`card_html()` ↔ news.html 的 `cardHTML()`;`feed_item_html()/feed_list()` ↔ news-c.html 的 `itemHTML()/render()`。改一处必须同步另一处,否则预渲染(SEO 入口)与前端渲染会不一致。
- **管线只重写三个标记区块**:`<!-- NEWS:LIST:BEGIN/END -->`(前 20 条预渲染)、`<script id="news-data">`(内联数据)、`<b id="newsTotal">`。页面其余部分手工维护——**手改壳走 PR,不要在服务器上改**。
- **首屏公司相关优先**(佳芮 2026-07-24)只对 news.html 生效:`COMPANY_SOURCES = {rui-blog, wechat-mp, product, press}` 置顶,各组内保持时间序;`news-c.html` 是按月分组,打乱时间序会让月份头错乱,故保持纯时间序。
- **口径**:企微/企业微信不出现在任何页面(替代写法按语境用「私域」「微信客服」「多 IM」)。

## 7. 已知的账(接手人可以挑着还)

1. **公众号源自动化**:CI 无 lark-cli → 每次公众号发文要人肉跑+rsync。可选修法:把飞书登记表读取改成 CI 可用的方式(bot token 直连飞书开放接口,不依赖本机 lark-cli 授权)。
2. **孤儿图清理**:`news/img/` 永不 --delete,长期会攒孤儿图。占用极小,但需要时得另开一条清理路径(别放进热路径)。
3. **stage-2 架构统一**:PR#103 合并后,stage-2 上的老生成物应清掉、改走 jz-news 目录,否则两套架构并存会让人困惑。
4. **`docs/DEPLOY.md` 可能过时**:它写于 LFS 方案时期,方向 1 重构后部分内容(git lfs pull 那段)已不适用,值得复核一遍。
5. **概念页 SEO 效果未验证**:概念页是原创内容、放开 index(与镜像详情页 noindex 相反),上线后值得观察收录情况——这是动态页在 GEO 上的主要赌注。

## 8. 关键文件索引

| 文件 | 作用 |
|---|---|
| `build_news.py` | 管线本体(源 adapter / AI 加工 / 详情页 / 概念页 / 注入) |
| `.github/workflows/news-cron.yml` | 每 6h 定时:拉状态 → 校验门 → 跑管线 → 推回 |
| `deploy/nginx-news.conf` | 对外路由片段(**待运维 include**) |
| `docs/DEPLOY.md` | 上线手册(注意第 7.4 条:可能过时) |
| `news.html` / `news-c.html` | 两版页面模板壳(注入区为空) |
| `data/product-news.json` / `press-news.json` | 人工种子(产品动态 / 媒体报道登记位) |
