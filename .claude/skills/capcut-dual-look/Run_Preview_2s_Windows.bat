@echo off
setlocal
cd /d "%~dp0"
if "%~1"=="" (
 echo Drag video files onto this BAT to render a 2-second look preview.
 pause
 exit /b 1
)
where py >nul 2>&1
if not errorlevel 1 (
 py -3 "%~dp0scripts\apply.py" --mode both --encoder auto --preview-seconds 2 %*
) else (
 python "%~dp0scripts\apply.py" --mode both --encoder auto --preview-seconds 2 %*
)
pause
