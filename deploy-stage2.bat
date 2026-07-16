@echo off
chcp 65001 >nul
cd /d "D:\juzibot-website\juzibot-website"
(
echo ===== clean stale lock =====
if exist .git\index.lock del /f .git\index.lock
echo ===== fetch =====
git fetch origin
echo ===== stage-2 from origin/main =====
git checkout -B stage-2 origin/main
echo ===== add 9 files =====
git add fde.html workforce/service.html workforce/sales.html workforce/marketing.html workforce/hr.html workforce/government.html workforce/finance.html workforce/geo.html careers/emp-v2-geo-person.png
git diff --cached --stat
echo ===== commit =====
git commit -m "feat: fde 卡片与场景选择台重排；workforce 七页人物海报 hero + 能力卡升级"
echo ===== push =====
git push -f origin stage-2
echo ===== result =====
git log --oneline -2
echo ===== DEPLOY_SCRIPT_DONE =====
) > deploy-stage2.log 2>&1
exit
