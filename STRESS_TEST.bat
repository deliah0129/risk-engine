@echo off
setlocal enabledelayedexpansion

:MENU
cls
echo ========================================
echo RISK ENGINE - STRESS TEST SUITE
echo ========================================
echo.
echo 1. Run ALL tests (recommended)
echo 2. Sequential throughput test only
echo 3. Concurrent sessions test only
echo 4. State persistence test only
echo 5. Determinism verification only
echo 6. Custom configuration
echo Q. Quit
echo.
echo ========================================

choice /C 123456Q /N /M "Select an option: "

if errorlevel 7 goto END
if errorlevel 6 goto CUSTOM
if errorlevel 5 goto DETERMINISM
if errorlevel 4 goto PERSISTENCE
if errorlevel 3 goto CONCURRENT
if errorlevel 2 goto SEQUENTIAL
if errorlevel 1 goto ALL

:ALL
cls
echo ========================================
echo Running ALL tests...
echo ========================================
echo.
python stress_test.py --test all
echo.
echo ========================================
echo Press any key to return to menu...
pause >nul
goto MENU

:SEQUENTIAL
cls
echo ========================================
echo Running Sequential Throughput Test...
echo ========================================
echo.
python stress_test.py --test sequential --iterations 100
echo.
echo ========================================
echo Press any key to return to menu...
pause >nul
goto MENU

:CONCURRENT
cls
echo ========================================
echo Running Concurrent Sessions Test...
echo ========================================
echo.
python stress_test.py --test concurrent --sessions 10
echo.
echo ========================================
echo Press any key to return to menu...
pause >nul
goto MENU

:PERSISTENCE
cls
echo ========================================
echo Running State Persistence Test...
echo ========================================
echo.
python stress_test.py --test persistence --cycles 50
echo.
echo ========================================
echo Press any key to return to menu...
pause >nul
goto MENU

:DETERMINISM
cls
echo ========================================
echo Running Determinism Verification...
echo ========================================
echo.
python stress_test.py --test determinism
echo.
echo ========================================
echo Press any key to return to menu...
pause >nul
goto MENU

:CUSTOM
cls
echo ========================================
echo Custom Configuration
echo ========================================
echo.
echo Select test type:
echo 1. Sequential
echo 2. Concurrent
echo 3. Persistence
echo 4. Determinism
echo.

choice /C 1234 /N /M "Test type: "

if errorlevel 4 (
    set TEST_TYPE=determinism
    set /p PARAM="Enter number of runs [10]: "
    if "!PARAM!"=="" set PARAM=10
    python stress_test.py --test !TEST_TYPE! --runs !PARAM!
) else if errorlevel 3 (
    set TEST_TYPE=persistence
    set /p PARAM="Enter number of cycles [50]: "
    if "!PARAM!"=="" set PARAM=50
    python stress_test.py --test !TEST_TYPE! --cycles !PARAM!
) else if errorlevel 2 (
    set TEST_TYPE=concurrent
    set /p PARAM="Enter number of sessions [10]: "
    if "!PARAM!"=="" set PARAM=10
    python stress_test.py --test !TEST_TYPE! --sessions !PARAM!
) else if errorlevel 1 (
    set TEST_TYPE=sequential
    set /p PARAM="Enter number of iterations [100]: "
    if "!PARAM!"=="" set PARAM=100
    python stress_test.py --test !TEST_TYPE! --iterations !PARAM!
)

echo.
echo ========================================
echo Press any key to return to menu...
pause >nul
goto MENU

:END
cls
echo ========================================
echo Exiting stress test suite...
echo ========================================
endlocal
exit /b 0
