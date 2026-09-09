# juzibot.com 官网

句子互动的营销官网，纯静态 HTML/CSS/JS，无构建工具。开发约定详见 `CLAUDE.md`（含哪些页面手工维护、哪些脚本可以跑的红线）。

## 动态页管线

```bash
python3 build_news.py          # 增量同步动态页（可安全反复运行）
python3 build_news.py --full   # 全量重抓（只刷新不删除）
python3 build_news.py --clean-shell   # 把两个列表页还原成干净模板壳（注入区清空）
python3 test_build_news.py     # 离线不变量测试（74 项，纯 stdlib、不联网、不要 key、秒级）
```

多源抓取 → AI 筛选/锐评/简报/翻译/概念抽取（智谱 GLM API）→ 注入 `news.html` / `news-c.html` / `news/p/*.html` / `news/c/*.html`。

**改渲染/消毒/写入逻辑前后各跑一次 `test_build_news.py`。** 它固化了 17 组已经出过事的不变量（noindex 页的 schema 与 canonical、概念死链、时间流倒序、SVG 不本地托管、消毒剥事件属性、原子写失败路径、撤稿的安全边界……），不联网不要密钥、秒级跑完——而验证同样的东西靠跑全量管线要几分钟且需要网络与 API key。CI 侧对应 `news-test.yml`，与 `shell-clean.yml`（模板壳/生成物）、`copy-guard.yml`（「企微/企业微信」不出现在任何页面）并列。

### 智谱 GLM API（AI 加工层）

- **模型**：`glm-4-air`（2026-07-22 从小米 MiMo 切换；选型实测以筛选判定质量为准——glm-4-air 与既有判定一致 24/28 且分歧均为边界条目，glm-4-flash 仅 18/28 会放进非 AI 资讯，故弃）。
- **端点**：`https://open.bigmodel.cn/api/paas/v4/chat/completions`（OpenAI 兼容，Bearer 鉴权）。
- **用在哪几处**：①内容筛选（`ai_filter` 判定去留）②锐评 quip ③中文简报 brief ④英文译题 title_zh ⑤英文全文翻译 ⑥概念抽取（概念库定义生成）。
- **key 读取顺序**：环境变量 `ZHIPU_API_KEY` 优先（CI 与生产用这个）；本地开发退回读 `~/projects/API-KEYS.md` 里智谱那行。两处都没有时优雅降级——新条目暂缓上站（pending），下轮运行自动重试，已上站内容不受影响。
- **生产部署**：由运维在部署环境配置 `ZHIPU_API_KEY` 环境变量；GitHub Actions 定时任务走仓库 Secret（见下）。

**密钥本体严禁写进仓库任何文件（代码/注释/测试/文档一律只写变量名）。**

## 定时同步（GitHub Actions）· 生成物不入库

**动态页生成物（`news/`、`data/news.json` 等）不进 git**（2026-07-23 定稿）。`.github/workflows/news-cron.yml` 每 6 小时（也可 Actions 页手动 Run workflow）在 CI 里跑一轮 `build_news.py`：先从服务器 `/opt/www/jz-news/` rsync 拉回上一轮状态 → 增量跑管线 → 把产物与状态 rsync 推回。不 commit、不 push，仓库零膨胀。完整架构、一次性上线步骤（nginx 路由 + seed 存量）与运维手册见 **`docs/DEPLOY.md`**；nginx 配置片段在 `deploy/nginx-news.conf`。

需要的仓库 Secret（均已有，与 deploy 共用）：

| Secret 名 | 用途 |
| --- | --- |
| `SSH_KEY` / `HOST` / `USER` | rsync/SSH 到服务器 |
| `ZHIPU_API_KEY` | 智谱 GLM API key（AI 筛选/锐评/简报/译题/全文翻译/概念抽取，模型 glm-4-air）。不配也能跑，AI 层降级为 pending 攒着 |

另有两点注意：

- **schedule 只认默认分支（main）上的 workflow 文件**。此文件合到 main 后定时才会生效；在那之前用 workflow_dispatch 手动跑。
- 公众号源依赖本机已授权的 lark-cli，CI 里该源必然失败并按设计沿用已有数据；公众号新文仍靠本机运行同步后手动 rsync（命令见 docs/DEPLOY.md）。

## 部署

push 到 `stage-1` / `stage-2` 触发 `.github/workflows/deploy.yml`，SSH 到服务器 checkout 对应分支到 `/opt/www/jz-<branch>`。`main` 与其它分支不部署。动态页产物在独立目录 `/opt/www/jz-news/`（news-cron 维护），不受代码部署的 checkout/clean 影响。
