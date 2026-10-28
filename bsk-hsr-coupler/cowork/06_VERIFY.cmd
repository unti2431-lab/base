@echo off
rem BSK-HSR-COUPLER 06_VERIFY  (double-click, or run from Cowork via computer use)
cd /d "%~dp0.."
powershell -NoProfile -ExecutionPolicy Bypass -File RUN_ALL.ps1 -Step verify -Test all
echo.
type logs\LAST_STATUS.txt
pause
