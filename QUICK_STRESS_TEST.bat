@echo off
echo ========================================
echo RISK ENGINE - QUICK STRESS TEST
echo ========================================
echo.
echo Running sequential stress test with 10 iterations...
echo This is a rapid validation test.
echo.

python stress_test.py --test sequential --iterations 10

echo.
echo ========================================
echo Quick stress test completed!
echo ========================================
pause
