# juzibot.com 官网

句子互动的营销官网，纯静态 HTML/CSS/JS，无构建工具。开发约定详见 `CLAUDE.md`（含哪些页面手工维护、哪些脚本可以跑的红线）。

## 动态页管线

```bash
python3 build_news.py          # 增量同步动态页（可安全反复运行）
python3 build_news.py --full   # 全量重抓（只刷新不删除）
```

多源抓取 → AI 筛选/锐评/简报/翻译/概念抽取（智谱 GLM API）→ 注入 `news.html` / `news-c.html` / `news/p/*.html` / `news/c/*.html`。

### 智谱 GLM API（AI 加工层）

- **模型**：`glm-4-air`（2026-07-22 从小米 MiMo 切换；选型实测以筛选判定质量为准——glm-4-air 与既有判定一致 24/28 且分歧均为边界条目，glm-4-flash 仅 18/28 会放进非 AI 资讯，故弃）。
- **端点**：`https://open.bigmodel.cn/api/paas/v4/chat/completions`（OpenAI 兼容，Bearer 鉴权）。
- **用在哪几处**：①内容筛选（`ai_filter` 判定去留）②锐评 quip ③中文简报 brief ④英文译题 title_zh ⑤英文全文翻译 ⑥概念抽取（概念库定义生成）。
- **key 读取顺序**：环境变量 `ZHIPU_API_KEY` 优先（CI 与生产用这个）；本地开发退回读 `~/projects/API-KEYS.md` 里智谱那行。两处都没有时优雅降级——新条目暂缓上站（pending），下轮运行自动重试，已上站内容不受影响。
- **生产部署**：由运维在部署环境配置 `ZHIPU_API_KEY` 环境变量；GitHub Actions 定时任务走仓库 Secret（见下）。

**密钥本体严禁写进仓库任何文件（代码/注释/测试/文档一律只写变量名）。**

## 定时同步（GitHub Actions）

`.github/workflows/news-cron.yml`：每 6 小时（也可在 Actions 页手动 Run workflow）跑一轮 `build_news.py`，有变更自动 commit+push 到 `stage-2` 并触发部署。

需要配置的仓库 Secret（Settings → Secrets and variables → Actions）：

| Secret 名 | 用途 |
| --- | --- |
| `ZHIPU_API_KEY` | 智谱 GLM API key（AI 筛选/锐评/简报/译题/全文翻译/概念抽取，模型 glm-4-air）。不配也能跑，AI 层降级为 pending 攒着 |

另有两点注意：

- **schedule 只认默认分支（main）上的 workflow 文件**。此文件合到 main 后定时才会生效；在那之前用 workflow_dispatch 手动跑。
- 公众号源依赖本机已授权的 lark-cli，CI 里该源必然失败并按设计沿用已有数据；公众号新文仍靠本机运行同步。

## 部署

push 到 `stage-1` / `stage-2` 触发 `.github/workflows/deploy.yml`，SSH 到服务器 checkout 对应分支。`main` 与其它分支不部署。
