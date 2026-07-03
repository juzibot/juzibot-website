# 句子互动 官网

[![Deploy](https://github.com/juzibot/juzibot-website/actions/workflows/deploy.yml/badge.svg)](https://github.com/juzibot/juzibot-website/actions/workflows/deploy.yml)

> 为企业部署 AI 员工 —— [juzibot.com](https://juzibot.com)

句子互动（JuziBot）的企业官网，面向 1000+ 企业客户提供 AI 员工解决方案，覆盖在线教育、消费电商、金融、政务、互联网等行业。

## 技术栈

- **纯静态站点**：HTML / CSS / Vanilla JS，无框架、无构建步骤
- **CSS**：共享设计系统 `assets/site.css`，关键页面内联样式
- **JS**：`assets/site.js`（导航/页脚注入）、`assets/askbar.js`（产品搜索路由）
- **依赖 CDN**：Font Awesome 6.5.2、Lenis 平滑滚动
- **部署**：GitHub Actions → SSH → Nginx

## 项目结构

```
├── index.html              # 首页（最大文件，内联样式）
├── about.html              # 关于我们
├── enterprise.html         # 企业能力
├── fde.html                # 前沿部署工程师
├── industries.html         # 行业解决方案
│
├── assets/
│   ├── site.css            # 共享设计系统
│   ├── site.js             # 导航/页脚注入 + 路由
│   ├── askbar.js           # 产品搜索/意图路由
│   ├── demos/              # 交互产品演示（iframe 嵌入）
│   ├── product-shots/      # 产品截图
│   └── brand/              # 品牌素材
│
├── products/               # 产品页面
│   ├── miaohui.html        # 秒回（工作台）
│   ├── miaodong.html       # 秒懂（大脑）
│   ├── shouhu.html         # 守护（督导）
│   ├── canmou.html         # 参谋（问数）
│   ├── zhizao.html         # 智造（底座）
│   ├── dongxing.html       # 懂行（智库）
│   └── cli.html            # CLI（开发者工具）
│
├── workforce/              # AI 员工角色页面
│   ├── sales.html          # 销售
│   ├── marketing.html      # 导购
│   ├── service.html        # 客服
│   ├── government.html     # 政务
│   ├── finance.html        # 金融
│   ├── hr.html             # HR
│   └── geo.html            # GEO 优化师
│
├── careers/                # 招聘页
├── deploy/                 # Nginx 配置
├── server/                 # 服务端 hero-chat 功能
├── build_redirects.py      # 生成 /zh/* /en/* 301 重定向
├── CLAUDE.md               # AI 辅助开发指引
└── .github/workflows/      # CI/CD
```

## 本地开发

无需安装依赖，直接用任意静态服务器打开：

```bash
# Python
python3 -m http.server 8080

# 或 Node
npx serve .

# 或直接用浏览器打开
open index.html
```

> ⚠️ `build_pages.py` 是历史遗留脚本，**请勿运行**，会覆盖手写内容。

## 部署

- 推送到 **`stage-1`** 或 **`stage-2`** 分支触发自动部署
- GitHub Actions 通过 SSH 在生产服务器执行 `git checkout -f`
- 部署结果通知飞书群
- `main` 分支不触发部署（生产由 `main` 直接管理）

## 贡献指南

1. Fork 本仓库
2. 从 `main` 创建特性分支
3. 提交 PR，填写说明
4. 等待 Review & 合并

添加新产品/角色页面：复制现有页面 → 修改内容 → 更新 `assets/site.js`（导航/页脚）和 `assets/askbar.js`（路由映射）。首页和招聘页有独立导航，需单独更新。

## 许可

Copyright © 句子互动. All rights reserved.
