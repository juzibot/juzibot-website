@echo off
chcp 65001 >nul
cd /d "D:\juzibot-website\juzibot-website"
(
echo ===== push via clash proxy 7890 =====
set HTTPS_PROXY=http://127.0.0.1:7890
set HTTP_PROXY=http://127.0.0.1:7890
git push -f origin stage-2
if errorlevel 1 (
  echo ===== proxy failed, retry direct =====
  set HTTPS_PROXY=
  set HTTP_PROXY=
  git push -f origin stage-2
)
echo ===== DONE4 =====
) > deploy-stage2d.log 2>&1
exit
