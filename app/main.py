"""
Fiscal-Sentinel FastAPI Backend
Asynchronous API endpoints for Advanced Algorithmic Fraud Detection
Production-level performance with async/await patterns
"""

from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import sys
from pathlib import Path

# Add parent directory to path for config import
sys.path.insert(0, str(Path(__file__).parent.parent))
from config import SystemConfig

from app.modules import tender, price, ghost, welfare

# Initialize FastAPI with production config
app = FastAPI(
    title=SystemConfig.API_TITLE,
    version=SystemConfig.API_VERSION,
    description="High-performance fraud detection using Graph Theory, NLP, and Statistical Analysis"
)

# Enable CORS for Streamlit dashboard
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """System status and available modules"""
    return {
        "service": SystemConfig.API_TITLE,
        "version": SystemConfig.API_VERSION,
        "status": "ONLINE - Defense Systems Active",
        "async_enabled": SystemConfig.ENABLE_ASYNC,
        "modules": {
            "tender_watch": "NLP/Vector Embeddings",
            "graph_fraud": "Connected Components/Centrality",
            "price_guard": "Statistical Analysis (2σ)",
            "welfare_shield": "Fuzzy String Matching"
        }
    }


@app.post("/api/tender")
async def analyze_tenders(files: List[UploadFile] = File(...)):
    """
    Tender-Watch: Analyze tender PDFs for collusion using vector embeddings
    Algorithm: 384-dimensional cosine similarity in high-dimensional space
    Accepts: Multiple PDF files
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
    Price-Guard: Analyze invoice for over-invoicing using statistical analysis
    Algorithm: 2σ standard deviation detection + weighted Levenshtein distance
    Accepts: Image file (PNG, JPG)
    """
    image_bytes = await file.read()
    result = price.analyze_invoice(image_bytes)
    return result


@app.post("/api/ghost")
async def analyze_payroll(file: UploadFile = File(...)):
    """
    Ghost-Hunter: Detect ghost employees using graph theory
    Algorithm: Connected components + betweenness centrality for kingpin detection
    Accepts: CSV file with columns: Employee_ID, Name, Mobile, Bank_Acc
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
    Welfare-Shield: Cross-check pension list against death registry
    Algorithm: Fuzzy string matching (handles NP-Hard string alignment)
    Accepts: Two CSV files - pension list and death registry
    """
    pension_bytes = await pension_file.read()
    death_bytes = await death_file.read()
    
    result = welfare.analyze_welfare(pension_bytes, death_bytes)
    return result

