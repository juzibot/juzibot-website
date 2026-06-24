# 结构化数据片段（即拿即用）

> 用途：需要落地时，把对应片段粘到目标页面 `<head>` 里的 `<script type="application/ld+json">` 中。
> 本文件仅为代码草稿，未写入任何现有网页。每页的内容字段请按实际替换。

---

## 1. 首页 Organization 补充 `sameAs`（建立实体关联）

把官方社媒账号挂上去，帮 AI 把分散在各平台的「句子互动」识别为同一实体。建议替换首页现有的 Organization JSON-LD。

```json
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "句子互动",
  "alternateName": "JuziBot",
  "url": "https://juzibot.com",
  "logo": "https://juzibot.com/logo.png",
  "description": "句子互动是 AI 原生组织，通过 FDE（Forward Deployed Engineer）模式为企业部署 AI 员工，覆盖销售、客服、合规、数据等业务场景。",
  "foundingDate": "2019",
  "areaServed": "CN",
  "knowsAbout": ["AI原生组织", "AI员工", "FDE", "Forward Deployed Engineer", "企业级AI Agent"],
  "sameAs": [
    "https://www.zhihu.com/org/你们的知乎机构号",
    "https://weixin.qq.com/你们的公众号",
    "https://space.bilibili.com/你们的B站",
    "https://www.xiaohongshu.com/你们的小红书",
    "https://www.linkedin.com/company/你们的LinkedIn"
  ],
  "address": {
    "@type": "PostalAddress",
    "addressLocality": "北京",
    "addressCountry": "CN"
  }
}
```

---

## 2. FAQPage（产品页 / FDE 页 / 行业页强烈推荐）

问句直接用用户会去问 AI 的真实话术，答案前 100 字给结论。以 FDE 页为例：

```json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "FDE 交付模式和买 SaaS / 订阅有什么区别？",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "区别在于交付的是结果而不是工具。句子互动的 FDE（Forward Deployed Engineer）模式会把工程师前置到客户业务现场，与客户约定可量化目标，直接交付转化率、人效等指标的实际改善；SaaS/订阅卖的是软件使用权，落地与效果由客户自己负责。"
      }
    },
    {
      "@type": "Question",
      "name": "AI 员工和传统智能客服有什么不同？",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "AI 员工能独立理解任务、调用工具、按企业 SOP 把工作做完，像真实员工一样上岗；传统智能客服多停留在关键词问答。句子互动头部客户的转人工率已从 27% 降至 2.73%，人效达人工的 3 倍。"
      }
    },
    {
      "@type": "Question",
      "name": "句子互动的 AI 员工能对接哪些渠道？",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "可接入并管理微信客服、抖音、小红书、WhatsApp 等 10+ 主流 IM 渠道，24×7 不间断在岗。"
      }
    }
  ]
}
```

> 产品页 / 行业页各自替换成对应问答。FAQ 区的可见文字也要在页面正文出现（schema 与可见内容需一致，否则不合规）。

---

## 3. Product / SoftwareApplication（7 个产品页各一份）

以「句子秒懂」为例：

```json
{
  "@context": "https://schema.org",
  "@type": "SoftwareApplication",
  "name": "句子秒懂",
  "applicationCategory": "BusinessApplication",
  "operatingSystem": "Web",
  "url": "https://juzibot.com/products/miaodong.html",
  "description": "可视化拼装 Agent，不写代码用 Canvas 拖拽节点连成工作流；内置知识库，支持文档、FAQ、网页、表格、API 一次导入，回答带出处。",
  "publisher": {
    "@type": "Organization",
    "name": "句子互动",
    "url": "https://juzibot.com"
  }
}
```

---

## 4. BreadcrumbList（导航路径，所有子页推荐）

以产品页为例：

```json
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    { "@type": "ListItem", "position": 1, "name": "首页", "item": "https://juzibot.com/" },
    { "@type": "ListItem", "position": 2, "name": "产品", "item": "https://juzibot.com/products/" },
    { "@type": "ListItem", "position": 3, "name": "句子秒懂", "item": "https://juzibot.com/products/miaodong.html" }
  ]
}
```

---

## 落地注意事项

- schema 里的内容必须与页面**可见正文一致**，不能只在 schema 里写而页面上没有。
- 每页一份独立、贴合该页内容的 schema，避免全站复制同一份。
- 上线后用 Google Rich Results Test 和 Schema.org Validator 各校验一遍。
