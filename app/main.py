"""
Fiscal-Sentinel FastAPI Backend
Main API endpoints for all 4 fraud detection modules
"""

from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from typing import List

from app.modules import tender, price, ghost, welfare

app = FastAPI(title="Fiscal-Sentinel API", version="1.0.0")

# Enable CORS for Streamlit
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {
        "service": "Fiscal-Sentinel API",
        "version": "1.0.0",
        "status": "online",
        "modules": ["tender", "price", "ghost", "welfare"]
    }


@app.post("/api/tender")
async def analyze_tenders(files: List[UploadFile] = File(...)):
    """
    Analyze tender PDFs for collusion
    Accepts multiple PDF files
    """
    pdf_bytes_list = []
    for file in files:
        content = await file.read()
        pdf_bytes_list.append(content)
    
    result = tender.analyze_tenders(pdf_bytes_list)
    return result


@app.post("/api/price")
async def analyze_invoice(file: UploadFile = File(...)):
    """
    Analyze invoice image for over-invoicing
    Accepts image file (PNG, JPG)
    """
    image_bytes = await file.read()
    result = price.analyze_invoice(image_bytes)
    return result


@app.post("/api/ghost")
async def analyze_payroll(file: UploadFile = File(...)):
    """
    Analyze payroll CSV for ghost employees
    Accepts CSV file with columns: Employee_ID, Name, Mobile, Bank_Acc
    """
    csv_bytes = await file.read()
    result = ghost.analyze_payroll(csv_bytes)
    return result


@app.post("/api/welfare")
async def analyze_welfare(
    pension_file: UploadFile = File(...),
    death_file: UploadFile = File(...)
):
    """
    Cross-check pension list against death registry
    Accepts two CSV files: pension list and death registry
    """
    pension_bytes = await pension_file.read()
    death_bytes = await death_file.read()
    
    result = welfare.analyze_welfare(pension_bytes, death_bytes)
    return result

