@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion
cd /d "D:\juzibot-website\juzibot-website"
(
echo ===== [1/5] clean =====
if exist .git\index.lock del /f .git\index.lock
echo ===== [2/5] fetch via proxy, fallback direct =====
set HTTPS_PROXY=http://127.0.0.1:7890
set HTTP_PROXY=http://127.0.0.1:7890
git fetch origin || (set HTTPS_PROXY=&set HTTP_PROXY=&git fetch origin)
echo ===== [3/5] compose deploy commit on origin/stage-2 =====
for /f "usebackq delims=" %%i in (`git commit-tree 8c2c3af^^{tree} -p origin/stage-2 -m "deploy: stage-2 = main + persona hero/cards"`) do set NC=%%i
echo commit: !NC!
echo ===== [4/5] push =====
git push origin !NC!:refs/heads/stage-2 || (set HTTPS_PROXY=&set HTTP_PROXY=&git push origin !NC!:refs/heads/stage-2)
echo ===== [5/5] verify remote =====
git ls-remote origin refs/heads/stage-2
echo ===== DONE =====
) > deploy-stage2e.log 2>&1
type deploy-stage2e.log
echo.
echo 上面 refs/heads/stage-2 的哈希若与 commit 行一致, 部署成功
pause
