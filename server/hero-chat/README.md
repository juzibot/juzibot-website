# Hero 对话代理 · hero-chat

官网首页 Hero「直接和 AI 客服对话」的后端薄代理。前端只调同源 `POST /api/hero-chat`，
本服务持有 Insight 密钥、缓存 token、限流，再转发到 `/openapi/bot/message`。

> **为什么不让前端直连 Insight？** 鉴权 token 能调所有 `/openapi` 接口（含删除知识库）。
> 放进静态页的 JS = 谁都能 F12 盗走盗刷甚至搞破坏。所以必须有这层服务端代理。

## 它做了什么

- `accessKeyId/Secret → accessToken` 自动换取并**内存缓存**，剩余 <30min 才续期（贴合 Insight 自身复用语义）
- 对外只暴露 `POST /api/hero-chat`，固定 `botId`，只收 `text`，前端无法越权调别的接口
- 每 IP + 每 sessionId 双重限流；单条消息长度上限；上游超时保护；错误不外泄密钥
- 返回精简归一结构，前端可直接渲染：
  ```json
  { "code": 0, "data": { "message": "...", "references": [{"label":"…","similarity":"0.93"}],
                          "handover": false, "domain": "…", "fileUrls": [] } }
  ```

## 本地跑通

```bash
cd server/hero-chat
cp .env.example .env          # 填 JZ_ACCESS_KEY_ID / JZ_ACCESS_KEY_SECRET / JZ_BOT_ID
node --env-file=.env server.js
# → [hero-chat] listening on :8787 → upstream https://insight.juzibot.com …

# 另开一个终端测：
curl -s localhost:8787/api/hero-chat -H 'Content-Type: application/json' \
  -d '{"sessionId":"test-1","message":"你们和普通客服机器人有什么区别？"}' | jq
```

本地连前端预览：起一个静态服务器开 `proposals/ai-native-home/index.html`，并让代理放行该来源：

```bash
# 终端 A：代理（放行本地前端来源）
JZ_ALLOW_ORIGINS=http://localhost:8080 node --env-file=.env server.js
# 终端 B：静态站
python3 -m http.server 8080      # 然后访问 http://localhost:8080/proposals/ai-native-home/index.html
```

> 后端没起也没关系：前端会自动降级——点建议气泡走脚本答案，自由输入走离线兜底文案。
> 单文件直接用浏览器打开仍是纯演示，不受影响。

## 生产部署（自建 nginx 服务器）

1. **跑服务**（systemd，监听 `127.0.0.1:8787`）：把下面的 unit 存为
   `/etc/systemd/system/juzibot-hero-chat.service`，密钥写在 `EnvironmentFile`：

   ```ini
   [Unit]
   Description=Juzibot hero-chat proxy
   After=network.target

   [Service]
   WorkingDirectory=/opt/www/juzibot/server/hero-chat
   EnvironmentFile=/opt/www/juzibot/server/hero-chat/.env
   ExecStart=/usr/bin/node server.js
   Restart=always
   User=www-data

   [Install]
   WantedBy=multi-user.target
   ```
   ```bash
   sudo systemctl daemon-reload && sudo systemctl enable --now juzibot-hero-chat
   curl -s localhost:8787/api/hero-chat/health   # → {"ok":true,...}
   ```

2. **接 nginx**：按 `deploy/nginx-hero-chat.conf` 把 `/api/hero-chat` 反代到 `:8787`，
   注意放在 `nginx-never-404.conf` 的 404 兜底之前。

3. 验证：`curl -s https://juzibot.com/api/hero-chat/health`

> 注意：现有 `deploy.yml` 只 `git pull + build_pages.py` 静态内容，**不会**自动重启本服务。
> 改了 `server.js` 后需 `sudo systemctl restart juzibot-hero-chat`（可后续加进部署脚本）。

## 门面 bot 建议

专门建一个营销知识库 + bot 作为 `JZ_BOT_ID`，知识范围限定「怎么落地 / 接入多久 /
数据安全 / 和普通机器人区别 / 价格区间」，跑题温和挡回。这样首页这个 bot 既真实、
又不会被人带跑偏乱承诺。
