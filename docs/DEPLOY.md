# 动态页(news)部署手册 · 生成物不入库架构

> 2026-07-23 定稿(佳芮裁决方向): **动态页生成物不进 git**。CI 每 6 小时跑
> `build_news.py`,产物 rsync 到服务器独立目录 `/opt/www/jz-news/`,nginx 把
> `/news*` 路由指过去。仓库只留"配方":`build_news.py`、workflow、页面模板壳、
> 人工种子(`data/product-news.json`、`data/press-news.json`)。
>
> (旧方案 git LFS 已废弃——它只省 git 体积,解决不了生成物入库本身:仓库每 6h
> 长一个机器 commit、PR 混入几百个生成页、LFS 免费带宽也扛不住 cron 频率。)

## 架构一图流

```
GitHub 仓库(只有配方)                服务器
┌─────────────────────┐             ┌──────────────────────────────┐
│ build_news.py        │   每6h CI   │ /opt/www/jz-<branch>/        │← deploy.yml
│ news.html (模板壳)   │  ┌───────┐  │   git checkout -f + clean    │  (代码,照旧)
│ news-c.html (模板壳) │→ │跑管线 │  ├──────────────────────────────┤
│ data/*-news.json种子 │  └───┬───┘  │ /opt/www/jz-news/            │← news-cron rsync
│ .github/workflows/   │      │      │   news.html news-c.html      │  (产物,独立)
└─────────────────────┘      │      │   news/{p,c,img}/            │
        状态拉回 ┌───────────┘      │   data/ (管线状态,不对外)    │
        产物推去 └─────rsync───────→└──────────────────────────────┘
                                     nginx: /news.html /news-c.html /news/ → jz-news
```

- **状态以服务器为准闭环**:CI 每轮先把 `/opt/www/jz-news/{data,news}/` rsync
  拉回(增量管线的记忆:去重/AI判定缓存、概念库、渲染签名、正文镜像、已下载图片),
  跑完再 `--delete` 推回。仓库零膨胀,无机器 commit。
- **页面模板壳以仓库为准**:`news.html`/`news-c.html` 在仓库里是注入区为空的壳,
  手工改壳走 PR;CI 注入数据后把完整页推到服务器。
- **代码部署完全不变**:`deploy.yml` 照旧 checkout 到 `/opt/www/jz-<branch>`,
  与 `/opt/www/jz-news/` 互不干扰。

## 上线步骤(一次性)

按顺序做三件事:

**① nginx 加路由**(需运维,一次)

把 `deploy/nginx-news.conf` 存为 `/etc/nginx/snippets/jz-news.conf`,在 jz-main
与 jz-stage-* 的每个 server 块里加一行:

```nginx
include snippets/jz-news.conf;
```

```bash
nginx -t && systemctl reload nginx
```

**② seed 存量**(GitHub Actions,一次)

Actions → news-cron → Run workflow → 勾上 `seed` → Run。它会从 git 历史最后一个
含全量产物的提交(`SEED_REF`,图片在 LFS)把存量推到 `/opt/www/jz-news/`。

**③ 合并 PR 进 main** —— schedule 只认默认分支上的 workflow 文件,合并后每 6
小时自动增量同步。

> 顺序说明:①② 先做,页面立即有内容;③ 合并后壳版 `news.html` 进入
> `/opt/www/jz-main/`,但 nginx 已把 `/news.html` 指向 jz-news,壳不会被访问到。
> 若 ① 未配就合并,`/news.html` 会短暂显示空壳列表(不 404,可接受但难看)。

## 日常运维

- **验证一轮同步**:Actions → news-cron 最近 run 是否绿;或看
  `ls -lt /opt/www/jz-news/news/p/ | head`。
- **手动触发一轮**:Actions → news-cron → Run workflow(不勾 seed)。
- **公众号新文**:CI 无 lark-cli,公众号源在 CI 里单源失败并沿用旧数据(设计内)。
  本机跑 `python3 build_news.py` 后手动推:
  ```bash
  rsync -az --delete news/ <USER>@<HOST>:/opt/www/jz-news/news/
  rsync -az --delete data/ <USER>@<HOST>:/opt/www/jz-news/data/
  rsync -az news.html news-c.html <USER>@<HOST>:/opt/www/jz-news/
  ```
- **常规轮失败"拉取服务器状态失败"**:说明 `/opt/www/jz-news/` 不存在(还没
  seed)或 SSH 不通。先跑 seed;SSH 问题查 Secrets 的 `SSH_KEY/HOST/USER`。
- **本地开发**:`data/`、`news/` 已 gitignore,本地状态文件照常读写,
  `python3 build_news.py` 行为不变;智谱 key 本地退回读 `~/projects/API-KEYS.md`。

## 为什么常规轮拉不到状态要直接失败

防呆:如果拉取失败还继续跑,管线会把服务器上已有的全部条目当新条目重抓、重新过
一遍 AI 判定/简报/翻译——烧一整轮 API 配额还可能把旧内容顶乱。失败即停,等人来
看,是更便宜的错误。

## Secrets 清单(仓库已有,无需新增)

| Secret | 用途 |
|---|---|
| `SSH_KEY` / `HOST` / `USER` | rsync/SSH 到服务器(与 deploy.yml 共用) |
| `ZHIPU_API_KEY` | 智谱 GLM(筛选/简报/翻译/概念);缺失时管线优雅降级 |
