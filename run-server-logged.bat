@echo off
cd /d "%~dp0"
set PY=D:\anaconda3\python.exe
if not exist "%PY%" set PY=python
echo STARTING_%PY% > server-status.txt
start "" http://localhost:8000
"%PY%" -u -m http.server 8000 >> server.log 2>&1
