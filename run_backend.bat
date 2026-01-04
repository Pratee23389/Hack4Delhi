@echo off
echo ========================================
echo Starting Fiscal-Sentinel Backend API
echo ========================================
echo.

echo Installing dependencies...
pip install -r requirements.txt

echo.
echo Starting FastAPI server on http://localhost:8000
echo API Docs will be available at http://localhost:8000/docs
echo.

uvicorn app.main:app --reload
