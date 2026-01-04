@echo off
echo ========================================
echo Installing Fiscal-Sentinel Dependencies
echo ========================================
echo.
echo This will install all required packages...
echo.

pip install fastapi==0.95.2
pip install uvicorn[standard]==0.22.0
pip install python-multipart==0.0.6
pip install pdfplumber==0.7.6
pip install transformers==4.35.0
pip install torch==2.2.0 --index-url https://download.pytorch.org/whl/cpu
pip install numpy==1.26.4
pip install scikit-learn==1.3.2
pip install pillow==10.1.0
pip install pytesseract==0.3.10
pip install pandas==2.2.2
pip install networkx==3.2
pip install streamlit==1.28.0
pip install beautifulsoup4==4.12.2
pip install spacy==3.6.0
pip install rapidfuzz==2.15.1
pip install requests==2.31.0

echo.
echo ========================================
echo Installing spaCy language model...
echo ========================================
python -m spacy download en_core_web_sm

echo.
echo ========================================
echo Installation Complete!
echo ========================================
echo.
echo Next step: Run run_dashboard.bat to start the demo
echo.
pause
