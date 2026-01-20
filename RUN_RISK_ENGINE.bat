@echo off
setlocal

REM Always run from the folder this .bat lives in
cd /d "%~dp0"

echo Starting RISK: Global Power (v0.1)
echo Folder: %CD%
echo.

REM Ensure expected folders exist (safe even if already there)
if not exist "state" mkdir "state"
if not exist "logs" mkdir "logs"

REM Sanity check: main.py must exist right here
if not exist "main.py" (
  echo ERROR: main.py not found in %CD%
  echo Make sure RUN_RISK_ENGINE.bat is in the same folder as main.py
  echo.
  pause
  exit /b 1
)

REM Prefer Windows Python Launcher (py). Fallback to python.
where py >nul 2>nul
if %errorlevel%==0 (
  py main.py
) else (
  where python >nul 2>nul
  if %errorlevel%==0 (
    python main.py
  ) else (
    echo ERROR: Python not found.
    echo Install Python 3.14+ and make sure "py" or "python" works in Command Prompt.
    echo.
    pause
    exit /b 1
  )
)

echo.
echo -------------------------
echo Engine finished running.
pause
