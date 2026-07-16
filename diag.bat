@echo off
cd /d "%~dp0"
(
echo === where python ===
where python 2^>^&1
echo === python --version ===
python --version 2^>^&1
echo === where py ===
where py 2^>^&1
echo === candidates ===
if exist "%USERPROFILE%\anaconda3\python.exe" echo FOUND_A %USERPROFILE%\anaconda3\python.exe
if exist "%USERPROFILE%\miniconda3\python.exe" echo FOUND_B %USERPROFILE%\miniconda3\python.exe
if exist "C:\ProgramData\Anaconda3\python.exe" echo FOUND_C C:\ProgramData\Anaconda3\python.exe
if exist "C:\ProgramData\miniconda3\python.exe" echo FOUND_D C:\ProgramData\miniconda3\python.exe
if exist "D:\anaconda3\python.exe" echo FOUND_E D:\anaconda3\python.exe
if exist "D:\Anaconda\python.exe" echo FOUND_F D:\Anaconda\python.exe
where node 2^>^&1
) > diag.txt 2>&1
exit
