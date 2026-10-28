@echo off
rem BSK-HSR-COUPLER 03_GPU_TIMING  (double-click, or run from Cowork via computer use)
cd /d "%~dp0.."
powershell -NoProfile -ExecutionPolicy Bypass -File RUN_ALL.ps1 -Step timing -Test all -Preset key4s_gpu
echo.
type logs\LAST_STATUS.txt
pause
