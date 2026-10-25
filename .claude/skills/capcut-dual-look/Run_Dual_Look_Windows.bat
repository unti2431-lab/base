@echo off
setlocal
cd /d "%~dp0"
if "%~1"=="" (
  echo Drag video files or folders onto this BAT.
  echo Default: 4K filter -^> Auto Adjust, 1080p source resolution preserved.
  pause
  exit /b 1
)
where py >nul 2>&1
if not errorlevel 1 (
  py -3 "%~dp0scripts\apply.py" --mode both --encoder auto %*
) else (
  where python >nul 2>&1
  if errorlevel 1 (
    echo Python 3 is required. Install Python 3 and FFmpeg.
    pause
    exit /b 2
  )
  python "%~dp0scripts\apply.py" --mode both --encoder auto %*
)
if errorlevel 1 echo One or more inputs were not processed. See errors above.
pause
