@echo off
echo ========================================
echo Fiscal-Sentinel Setup Script
echo ========================================
echo.
echo Installing dependencies...
echo This will take 5-10 minutes.
echo.

python install.py

echo.
echo ========================================
echo To start the dashboard, run:
echo   run_dashboard.bat
echo.
echo Or manually:
echo   streamlit run streamlit_app.py
echo ========================================
pause
