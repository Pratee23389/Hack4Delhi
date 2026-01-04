@echo off
echo ========================================
echo Fiscal-Sentinel - Complete Test Suite
echo ========================================
echo.

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo.
echo Running module tests...
python test_modules.py

echo.
echo ========================================
echo Generating extended sample data...
echo ========================================
python generate_sample_data.py

echo.
echo ========================================
echo Test Suite Complete!
echo ========================================
echo.
echo All modules tested and sample data generated.
echo Ready for demo!
echo.
pause
