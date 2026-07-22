# juzibot.com 官网

句子互动的营销官网，纯静态 HTML/CSS/JS，无构建工具。开发约定详见 `CLAUDE.md`（含哪些页面手工维护、哪些脚本可以跑的红线）。

## 动态页管线

```bash
python3 build_news.py          # 增量同步动态页（可安全反复运行）
python3 build_news.py --full   # 全量重抓（只刷新不删除）
```

多源抓取 → AI 筛选/锐评/简报/翻译（小米 MiMo API）→ 注入 `news.html` / `news-c.html` / `news/p/*.html`。

### MiMo API key

AI 加工层的 key 按以下顺序取，两处都没有时优雅降级——新条目暂缓上站（pending），下轮运行自动重试，已上站内容不受影响：

1. 环境变量 `MIMO_API_KEY`（CI 用这个）
2. 本机 `~/projects/API-KEYS.md` 里 xiaomimimo 网关那行的 `sk-` key

**密钥严禁写进仓库任何文件。**

## 定时同步（GitHub Actions）

`.github/workflows/news-cron.yml`：每 6 小时（也可在 Actions 页手动 Run workflow）跑一轮 `build_news.py`，有变更自动 commit+push 到 `stage-2` 并触发部署。

需要配置的仓库 Secret（Settings → Secrets and variables → Actions）：

| Secret 名 | 用途 |
| --- | --- |
| `MIMO_API_KEY` | 小米 MiMo API key（AI 筛选/锐评/简报/翻译）。不配也能跑，AI 层降级为 pending 攒着 |

另有两点注意：

- **schedule 只认默认分支（main）上的 workflow 文件**。此文件合到 main 后定时才会生效；在那之前用 workflow_dispatch 手动跑。
- 公众号源依赖本机已授权的 lark-cli，CI 里该源必然失败并按设计沿用已有数据；公众号新文仍靠本机运行同步。

## 部署

push 到 `stage-1` / `stage-2` 触发 `.github/workflows/deploy.yml`，SSH 到服务器 checkout 对应分支。`main` 与其它分支不部署。
