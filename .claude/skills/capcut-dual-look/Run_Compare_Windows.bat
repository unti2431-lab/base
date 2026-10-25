@echo off
setlocal
cd /d "%~dp0"
if "%~1"=="" (
 echo Drag video files onto this BAT to render a 4-way comparison image
 echo (ORIGINAL ^| 4K / AUTO ^| 4K+AUTO) at 1.0s plus a 2-second comparison clip.
 pause
 exit /b 1
)
where py >nul 2>&1
if not errorlevel 1 (
 py -3 "%~dp0scripts\compare.py" --at 1.0 --video 2 %*
) else (
 python "%~dp0scripts\compare.py" --at 1.0 --video 2 %*
)
pause
