@echo off
echo Starting Fiscal-Sentinel FastAPI Backend...
echo.
echo Navigate to http://localhost:8000/docs for the API documentation
echo.
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
