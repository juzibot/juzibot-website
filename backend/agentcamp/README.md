# AgentCamp 报名接口

静态官网通过同域 `POST /api/agentcamp/applications` 提交报名。NestJS 服务用应用身份写入 SDR 所在 Base 中独立的「AgentCamp 线索」表，再向 AgentCamp 线索群发通知。凭证、SQLite 和服务进程均放在静态站点目录外。

## 运行与验证

使用 Node.js 24 LTS（至少 24.14，锁定 24.x）。本服务使用 `node:sqlite`，不能沿用早期部署说明里的 Node 20。

```sh
cd backend/agentcamp
npm ci
npm test
node --env-file=/etc/juzibot/agentcamp.env dist/main.js --check-config
node --env-file=/etc/juzibot/agentcamp.env dist/main.js
```

测试调用本地 HTTP 服务和模拟飞书接口，覆盖真实表单校验、重复提交、丢失响应后的恢复、通知重试、重启恢复和错误展示，不产生真实报名。`--check-config` 只读验证配置、表名和字段类型，不写数据、不发消息。

`npm audit` 的 multer 修复通过同主版本 override 固定到 2.5.0；本服务不接受上传，仍消除该间接依赖的已知漏洞。

## 飞书配置

1. 使用已确认的 SDR Base 链接，先解析成真实 Base token；Wiki 节点 token 不能直接当 Base token。
2. 给 AgentCamp 应用该 Base 的编辑权限。应用权限包括 `bitable:app` 和 `im:message:send_as_bot`，机器人必须在目标通知群内。
3. 查看 Base 的已有表，确认没有同名表后，用 `fields.json` 在同一个 Base 里新建表：

```sh
lark-cli base +url-resolve --url '已确认的 SDR 多维表格链接' --as user
lark-cli base +table-list --base-token '解析后的 Base token' --as user
lark-cli base +table-create --base-token '解析后的 Base token' --name 'AgentCamp 线索' --fields "$(cat fields.json)" --as user
```

建表是一次性的准备操作，运行服务时不会自动创建、改字段或修改 SDR 表。`fields.json` 的第一个字段「提交编号」作为主字段；跟进人和跟进备注留空，状态默认为「待跟进」。运行服务的机器人只需访问已准备好的目标表，不需要用户 OAuth。

将 `config.env.example` 复制到服务器 `/etc/juzibot/agentcamp.env`，填入 App Secret、真实 Base token、新表 ID 和确认后的 Base URL。文件权限设为 0600，不入 Git、不放进 nginx 文档目录。App ID 和群 ID 已给出；表格标识未硬编码，必须来自上述准备结果。

启动会核对指定表的名称和全部字段类型，防止误填 SDR 表 ID。生产表名必须为「AgentCamp 线索」，预览表名必须为「AgentCamp 线索（测试）」。预览配置使用独立表、SQLite 文件、端口和明确标注的通知，不允许预览请求直接走生产服务。

## 提交与恢复

- 请求必须来自配置的官网 Origin，使用 JSON，正文最多 16 KiB；联系方式、必填字段、选项、长度和联系同意均由服务端校验。每个来源 IP 每分钟最多 10 次。
- 前端生成 UUID，通过 `Idempotency-Key` 发送。超时重试沿用该编号；内容改变时更新编号。浏览器只保存随机编号，不保存报名内容。
- SQLite 在调用飞书前保存提交；24 小时内完全相同的内容也会合并。先按提交编号查询飞书，再用同一 `client_token` 写入，处理飞书已写成功但响应丢失的情况。
- 飞书确认写入后接口才返回 `{ok:true, submissionId}`。暂时不能确认时返回 503，页面保留填写内容并提示重试；已经持久化的报名也会由后台继续重试。
- 写表和通知分为两个持久化阶段。通知失败不改变写表结果，按 10 秒到 1 小时的退避持续重试。进程重启后恢复，SQLite 租约防止同一任务并发发送。
- 群通知只含公司、姓名、最多 300 字的需求摘要和记录链接，不包含联系方式；飞书消息使用稳定 UUID。外部平台的去重时间有限，因此网络结果长期不明确时通知按至少一次交付，极端情况下可能重复，线索仍按提交编号归并。
- 通知成功后清除 SQLite 中的报名正文，仅保留去重哈希和状态；未完成任务保留正文用于恢复。日志只记提交编号、阶段和错误码，不记正文或令牌。SQLite 与 WAL 一并按生产敏感数据管理和备份。

## 服务器部署

服务器目前尚未确认安装 Node。请先由运维安装 Node 24，确认 `/usr/bin/node --version` 和到 `open.feishu.cn:443` 的出站连接。不要直接套用旧文档的 Node 20 命令。

1. 将仓库对应版本放到 `/opt/juzibot-agentcamp/releases/<commit>/`，在 `backend/agentcamp` 执行 `npm ci`、`npm test`、`npm prune --omit=dev`。源码版本与静态页面版本保持一致。
2. 创建服务账号 `juzibot-agentcamp`，并由 root 维护 `/etc/juzibot/agentcamp.env`。复制 `deploy/agentcamp.service` 到 `/etc/systemd/system/`。只运行一个 systemd 实例，不再额外用 PM2 启动同一服务。
3. 将 `/opt/juzibot-agentcamp/current` 指向该 release。运行只读配置检查，确认通过后 `systemctl daemon-reload`、`systemctl enable --now agentcamp`。
4. 把 `deploy/nginx-agentcamp.conf` 中的规则合入对应站点的 `server`，与现有规则合并去重（尤其是点文件规则），运行 `nginx -t` 后再重载。接口精确路径必须优先于静态站点的首页兜底。
5. 本机 `curl -f http://127.0.0.1:3010/api/agentcamp/health` 检查进程。经官网填写一条明确标注的测试报名，确认新表有一条记录、群里有通知、刷新重试不会重复入库。

systemd 用 `StateDirectory` 保留 `/var/lib/juzibot-agentcamp`，发版和回滚只切换代码 release，不删除数据库。配置不通过时服务拒绝启动；日志通过 `journalctl -u agentcamp` 查看。当前网站的 SSH 部署工作流只同步静态站点，不会自动安装 Node 或启动新服务；本 PR 提供独立启动配置，首次部署需要上述准备。

## 上线前待填

- 确认 SDR Base 链接、实际 Base token 和新建的数据表 ID，并给应用授权。
- 安装 Node 24、配置私密环境文件、启用 systemd 和 nginx 转发。
- 完成一次真实飞书入库和通知验收。机器人群通知已单独验证过，但不能替代报名接口的端到端验收。
