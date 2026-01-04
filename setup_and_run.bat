@echo off
REM ================================================================
REM Fiscal-Sentinel Defense Systems - Automated Setup & Launch
REM One-Click Deployment for Competitive Programming Demo
REM ================================================================

echo.
echo ================================================================
echo    FISCAL-SENTINEL DEFENSE SYSTEMS v2.0
echo    Automated Setup and Deployment
echo ================================================================
echo.

REM Step 1: Install Dependencies
echo [1/5] Installing Python dependencies...
echo ----------------------------------------------------------------
python -m pip install --quiet --upgrade pip
python -m pip install --quiet -r requirements.txt
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)
echo DONE: All dependencies installed
echo.

REM Step 2: Generate Adversarial Test Data
echo [2/5] Generating adversarial test datasets...
echo ----------------------------------------------------------------
python create_complex_data.py
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Failed to generate test data
    pause
    exit /b 1
)
echo DONE: Complex test data generated
echo.

REM Step 3: Start Backend API Server
echo [3/5] Launching FastAPI Backend (Port 8000)...
echo ----------------------------------------------------------------
start /B "Fiscal-Sentinel-Backend" python -m uvicorn app.main:app --reload --port 8000
timeout /t 3 /nobreak >nul
echo DONE: Backend API online at http://localhost:8000
echo.

REM Step 4: Start Frontend Dashboard
echo [4/5] Launching Streamlit Dashboard (Port 8502)...
echo ----------------------------------------------------------------
start /B "Fiscal-Sentinel-Frontend" streamlit run dashboard.py --server.port 8502
timeout /t 5 /nobreak >nul
echo DONE: Dashboard online at http://localhost:8502
echo.

REM Step 5: Display System Status
echo [5/5] System Status
echo ================================================================
echo.
echo    FISCAL-SENTINEL DEFENSE SYSTEMS: ONLINE
echo.
echo    Backend API:      http://localhost:8000
echo    Frontend Dashboard: http://localhost:8502
echo.
echo    Algorithms Active:
echo      - Tender-Watch:    384-dim Vector Embeddings (NLP)
echo      - Ghost-Hunter:    Connected Components + Centrality
echo      - Price-Guard:     Statistical Analysis (2-sigma)
echo      - Welfare-Shield:  Fuzzy String Matching (NP-Hard)
echo.
echo    Test Data Generated:
echo      - Adversarial Tenders (96%% similarity)
echo      - Complex Payroll (500 rows, 10-person clique)
echo      - Noisy Welfare Records (OCR corruption)
echo      - Statistical Outlier Invoice
echo.
echo ================================================================
echo    Ready for Demo! Press CTRL+C in terminals to stop services.
echo ================================================================
echo.

REM Open dashboard in default browser
timeout /t 2 /nobreak >nul
start http://localhost:8502

pause
