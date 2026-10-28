@echo off
rem BSK-HSR-COUPLER 07_RENDER_KEY_A  (double-click, or run from Cowork via computer use)
cd /d "%~dp0.."
powershell -NoProfile -ExecutionPolicy Bypass -File RUN_ALL.ps1 -Step render -Test A -Preset key4s_gpu
echo.
type logs\LAST_STATUS.txt
pause
