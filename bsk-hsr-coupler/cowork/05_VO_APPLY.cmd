@echo off
rem BSK-HSR-COUPLER 05_VO_APPLY  (double-click, or run from Cowork via computer use)
cd /d "%~dp0.."
powershell -NoProfile -ExecutionPolicy Bypass -File RUN_ALL.ps1 -Step vo -Apply
echo.
type logs\LAST_STATUS.txt
pause
