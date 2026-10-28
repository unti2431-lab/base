@echo off
rem BSK-HSR-COUPLER 08_RENDER_KEY_B  (double-click, or run from Cowork via computer use)
cd /d "%~dp0.."
powershell -NoProfile -ExecutionPolicy Bypass -File RUN_ALL.ps1 -Step render -Test B -Preset key4s_gpu
echo.
type logs\LAST_STATUS.txt
pause
