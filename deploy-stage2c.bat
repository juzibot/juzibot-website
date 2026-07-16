@echo off
chcp 65001 >nul
cd /d "D:\juzibot-website\juzibot-website"
(
echo ===== kill stale git =====
taskkill /f /im git.exe 2>nul
taskkill /f /im git-credential-manager.exe 2>nul
if exist .git\index.lock del /f .git\index.lock
echo ===== push =====
git push -f origin stage-2
echo ===== verify =====
git log --oneline -1 stage-2
echo ===== DONE3 =====
) > deploy-stage2c.log 2>&1
exit
