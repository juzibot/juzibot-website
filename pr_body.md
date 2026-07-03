PR 包含了以下几项针对样式的修复与优化。

## 改动一览

| # | 改动 | 截图 |
|---|---|---|
| 1 | workforce/ 多页面 (finance, geo, government, marketing) 统一 Pill 标签样式 (桌面端单行不换行) | - |
| 2 | workforce/government.html 调整 .pill-row 和 .hero-art 垂直间距，解决标签遮挡卡片问题 | - |
| 3 | index.html 企业级横向流水线交互结构调整与重构 | - |
| 4 | industries.html 移除多余的 logo 占位 | - |
| 5 | .github/workflows/deploy.yml 配置轻微调整 | - |

---

## 1. 统一 Workforce 页面标签 (Pills) 样式
**问题**: 标签在屏幕较宽时出现换行，影响视觉紧凑感和品牌一致性。
**修复**: 对 inance.html, geo.html, government.html, marketing.html 中的 .pill 添加 white-space: nowrap，同时桌面端（≥900px）下给 .pill-row 设置 lex-wrap: nowrap 确保标签组单行显示。

## 2. 修复 Government 页面标签遮挡卡片
**问题**: 标签数量较多导致与右侧卡片 .hero-art 重叠。
**修复**: 增大桌面端 .pill-row 的 margin-top 并微调 .hero-art 的间距（margin-top: -10px），优化垂直布局空间。

## 3. 首页 (index.html) 企业级流水线重构
**改动**: 更新并重构了首页模块（7 项能力流水线交互），调整了 DOM 结构，提升了切换与悬停的用户体验。

## 4. 行业页 (industries.html) Logo 墙清理
**改动**: 移除了多余的 2 个占位 logo 元素，让视觉布局更紧凑。

