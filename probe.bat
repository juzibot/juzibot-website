@echo off
cd /d "%~dp0"
powershell -NoProfile -Command "try{$r=Invoke-WebRequest -Uri http://localhost:8000/ -UseBasicParsing -TimeoutSec 5; ('HTTP_'+$r.StatusCode) | Out-File -Encoding ascii probe-result.txt}catch{('FAIL '+$_.Exception.Message) | Out-File -Encoding ascii probe-result.txt}"
exit
