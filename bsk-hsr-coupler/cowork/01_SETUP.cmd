@echo off
rem BSK-HSR-COUPLER 01_SETUP  (double-click, or run from Cowork via computer use)
cd /d "%~dp0.."
powershell -NoProfile -ExecutionPolicy Bypass -File RUN_ALL.ps1 -Step setup
echo.
type logs\LAST_STATUS.txt
pause
