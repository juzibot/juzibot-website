# 部署手册 · 含 Git LFS 图片资产

动态页 `news/img/**` 下的抓取图片（约 33 MB、且随 6 小时 cron 持续增长）改由
**Git LFS** 托管：Git 仓库里存的是几十字节的“指针文件”，真图存在 GitHub 的 LFS
对象库。这样 `git clone` / 仓库历史不再被图片撑大。

> ⚠️ **核心前提**：**部署服务器必须装 git-lfs 并初始化过**，否则 `git checkout`
> 拿到的是指针文件、`news/img` 全站图裂。下面每一步都是围绕这条展开的。

---

## 0. 一次性：服务器安装 git-lfs（每台部署机只需做一次）

```bash
# Ubuntu / Debian
sudo apt-get update && sudo apt-get install -y git-lfs

# CentOS / RHEL
# sudo yum install -y git-lfs

# 全局安装 LFS 的 git 过滤器（对该机所有仓库生效，一次即可）
git lfs install --system
```

验证：

```bash
git lfs version      # 打印出版本号即 OK，例如 git-lfs/3.x.x
```

装好之后，**普通的 `git checkout` 会自动把指针文件还原成真图**（smudge 过滤器），
理论上不用改任何部署脚本。下面的 `git lfs pull` 是“即使 smudge 没触发也保底”的
显式兜底，建议保留。

---

## 1. 首次部署（全新拉一份）

```bash
BRANCH=main                        # 生产用 main；预览用 stage-1 / stage-2
TARGET=/opt/www/jz-$BRANCH

git clone https://github.com/juzibot/juzibot-website.git "$TARGET"
cd "$TARGET"
git checkout "$BRANCH"
git lfs pull origin                # 拉取本次 checkout 引用的所有 LFS 图片对象
```

---

## 2. 更新部署（已有目录，拉最新并覆盖）

现有 stage 部署脚本大致是 `git checkout -f` + `git clean -fd`。在其后**加一行
`git lfs pull`** 即可（若 git-lfs 已 `install --system`，checkout 时通常已自动
还原，这行是保底）：

```bash
BRANCH=main
cd /opt/www/jz-$BRANCH

git fetch origin "$BRANCH"
git reset --hard "origin/$BRANCH"  # 或沿用原来的 git checkout -f
git clean -fd                      # 注意：不会删被 .gitignore 的文件
git lfs pull origin                # ★ 关键新增：把 news/img 的指针还原成真图
```

> 把 `git lfs pull origin` 追加进服务器上的 `deploy-stage.sh`（在 `git clean -fd`
> 之后）即可让预览部署也自动就绪。

---

## 3. 部署后验证（务必看一眼）

```bash
cd /opt/www/jz-$BRANCH

# 随手抽一张图：应是 "JPEG image data ..." / "PNG image data ..."，
# 若显示 "ASCII text" 且只有一百多字节 → 说明是指针没还原，见下方排查
file news/img/*/*.jpg 2>/dev/null | head -3
find news/img -type f | head -1 | xargs wc -c   # 真图是几十~几百 KB，指针是 ~130 字节

# 确认本地已拉全 LFS 对象（Downloading 数应为 0 或很快完成）
git lfs pull origin
```

浏览器再打开 `/news.html` 里任一带图详情页确认不裂即可。

---

## 4. 排查：图裂 / 显示成一串文本

症状：页面图片裂开，或 `file news/img/xxx.jpg` 显示 `ASCII text`、文件只有约
130 字节，内容形如：

```
version https://git-lfs.github.com/spec/v1
oid sha256:...
size 145995
```

这就是**指针文件没被还原**，几乎都是这两种原因：

| 原因 | 处理 |
|---|---|
| 服务器没装 / 没 `install` git-lfs | 回到第 0 步装好，再 `git lfs pull origin` |
| checkout 时 LFS 对象没拉下来 | 在部署目录执行 `git lfs pull origin` |

强制重拉全部 LFS 对象：

```bash
cd /opt/www/jz-$BRANCH
git lfs fetch --all origin
git lfs checkout        # 用本地 LFS 对象重写工作树里的指针为真图
```

---

## 5. 关于 LFS 配额（需留意）

GitHub 免费额度是 **存储 1 GB / 流量 1 GB / 月**。`news/img` 当前约 33 MB，但
`news-cron` 每 6 小时抓新图、会持续增长，迟早撞配额。届时二选一：

- 在 GitHub 购买 LFS data pack（存储+流量按包扩容）；
- 或改为「外站图不镜像、只留自家源（rui 博客/公众号）图」，把增长摁住。

到时再定，先知道有这回事。

---

## 6. 附：把其它分支也迁到 LFS（可选，服务器就绪后再做）

目前只有 `feat/dynamic-news-page`（PR#100）的 `news/img` 已迁到 LFS。合并到
`main` 后，`main` 自动带上 LFS 配置。若要让**预览分支 `stage-2`** 和其上的
`news-cron` 也走 LFS（否则 cron 新抓的图仍是裸二进制，预览分支会继续变大），
在**服务器确认装好 git-lfs 后**，本地执行：

```bash
git checkout stage-2
git lfs migrate import --include="news/img/**" --include-ref=refs/heads/stage-2
git lfs checkout                 # 还原工作树为真图
git push --force origin stage-2  # 会先上传 LFS 对象，再强推重写后的历史
```

> ⚠️ 强推 `stage-2` 会触发一次预览部署；**务必先确认服务器已装 git-lfs**，
> 否则这次预览会图裂。`.gitattributes` 里的 `news/img/** filter=lfs ...` 一旦随
> 分支就位，之后 cron 新增的图会被自动纳入 LFS，无需再手动迁移。

---

## 备忘：LFS 是怎么配置的

- `.gitattributes`：`news/img/** filter=lfs diff=lfs merge=lfs -text` —— 圈定
  只有 `news/img` 走 LFS，`assets/`、`careers/` 等手维护的站点图不受影响。
- 真图对象存 GitHub LFS 库；Git 里只有指针。`git push` 会自动先传 LFS 对象。
