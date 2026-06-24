# 句子互动 GEO 优化交付包 · 执行计划与检查清单

> 本目录是一份「不改动任何现有网页」的 GEO 建议交付包。所有文件均为新增草稿/模板，落地时再由你决定是否实施。
> GEO = Generative Engine Optimization，目标是让句子互动被 ChatGPT / Gemini / Perplexity / 豆包 / 文心等 AI 引用和推荐。

## 文件清单

| 文件 | 作用 | 落地动作 |
|------|------|----------|
| `llms.txt` | 给 AI 的官网导航页（新兴事实标准） | 确认后放到网站根目录 |
| `robots-建议草稿.txt` | 显式放行 AI 爬虫、放开图片资源 | 确认后替换现有 robots.txt |
| `schema结构化数据片段.md` | FAQPage/Product/Breadcrumb/sameAs 代码 | 落地时粘到对应页面 head |
| `事实速览与FAQ文案块.md` | 页面可见正文草稿（schema 需与之一致） | 落地时加到对应页面正文 |
| `AI引用监测表.md` | 每月测 AI 是否引用你 | 立即可用，建基线 |
| `社媒选题清单.md` | 知乎/公众号/B站等内容规划 | 立即可用，排期生产 |

---

## 现状诊断小结（来自对官网的核对）

做对的：首页 TDK / OG / Twitter Card / Organization JSON-LD / canonical / robots 都齐全，SEO 地基好。

GEO 四个短板：
1. robots.txt 未显式放行 AI 爬虫，且 `Disallow: /assets/` 挡住产品截图与信息图（多模态吃亏）。
2. 只有 Organization schema，缺 FAQPage / Product / Breadcrumb，AI 最爱的问答结构没喂给它。
3. sitemap `lastmod` 停在 2025-06-23，新鲜度信号弱，正文缺时间锚。
4. 关键数据（3 倍人效、27%→2.73%）散在动效里，缺一段可被原样摘抄的纯文本事实区。

---

## 30 天执行计划

### 第 1 周 · 技术基础（见效最快）
- [ ] 用 `robots-建议草稿.txt` 替换 robots.txt，放行 GPTBot / Google-Extended / PerplexityBot / ClaudeBot / Bytespider 等
- [ ] 重新评估并放开 `/assets/` 下的图片资源
- [ ] 把 `llms.txt` 放到网站根目录
- [ ] 刷新 sitemap.xml 的 lastmod，对齐真实更新频率
- [ ] 自查：禁用 JS 后首屏核心内容是否仍在 HTML 源码中

### 第 2 周 · 内容结构
- [ ] 首页 / FDE / about 页加「事实速览」纯文本块（见文案块文件）
- [ ] 各产品页、FDE 页、行业页加 FAQ 可见区 + FAQPage schema
- [ ] 7 个产品页补 Product/SoftwareApplication schema
- [ ] 子页补 BreadcrumbList schema
- [ ] 首页 Organization 补 `sameAs`（社媒账号）
- [ ] 关键数据改写成「主体+数字+来源+时间」的完整句子
- [ ] 重要页面加「更新于 2026 年 X 月」时间锚
- [ ] 全站图片补精准 Alt；重要信息图配纯文本版

### 第 3 周 · 社媒起盘
- [ ] 按 `社媒选题清单.md` 在知乎 + 公众号围绕「AI 原生组织 / FDE / AI 员工」各出 1 组内容
- [ ] 完善各平台简介与官网回链
- [ ] 启动「一鱼多吃」复用流水线

### 第 4 周 · 监测闭环
- [ ] 用 `AI引用监测表.md` 跑首次全平台基线
- [ ] 记录被引用页面与表述错误项
- [ ] 定下按月复测节奏

---

## 上线后校验清单
- [ ] Google Rich Results Test 校验所有 schema
- [ ] Schema.org Validator 复核
- [ ] 确认 FAQ 可见文字与 schema 内容一致
- [ ] robots.txt 未误拦截重要页面与 CSS/JS
- [ ] llms.txt 可正常访问（https://juzibot.com/llms.txt）

---

## 衡量标准（GEO 不看排名，看引用）
- 月度 AI 提及率（15 题中被提及的比例）持续上升
- 被引用来源更多指向 juzibot.com 及官方社媒
- AI 对句子互动的定位、数据、术语表述准确无误
