@echo off
chcp 65001 >nul
cd /d "D:\juzibot-website\juzibot-website"
(
echo ===== identity =====
git config user.name "Anna Looper"
git config user.email "meetingturing@gmail.com"
echo ===== commit =====
git commit -m "feat: fde 卡片与场景选择台重排；workforce 七页人物海报 hero + 能力卡升级"
echo ===== push =====
git push -f origin stage-2
echo ===== result =====
git log --oneline -2
echo ===== DEPLOY_SCRIPT_DONE2 =====
) > deploy-stage2b.log 2>&1
exit
