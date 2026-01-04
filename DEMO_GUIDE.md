# Fiscal-Sentinel Demo Guide

## Quick Start (For Hackathon Judges)

### Installation & Setup

1. **Run the setup script** (Windows):
   ```bash
   setup.bat
   ```
   This will:
   - Create a virtual environment
   - Install all dependencies
   - Download spaCy models

2. **Start the Dashboard**:
   ```bash
   run_dashboard.bat
   ```
   OR manually:
   ```bash
   streamlit run streamlit_app.py
   ```

3. **Start the API** (Optional, in a separate terminal):
   ```bash
   run_api.bat
   ```
   OR manually:
   ```bash
   uvicorn app.main:app --reload
   ```

---

## Module Demonstrations

### Module A: Tender-Watch (Bid Rigging Detection)

**Purpose**: Detect collusion and bid-rigging by comparing textual similarity between tender documents.

**Demo Steps**:
1. Go to the "Tender-Watch" tab in Streamlit
2. Upload sample files:
   - `data/samples/sample_tender_1.txt` (convert to PDF or use as-is if you add txt support)
   - `data/samples/sample_tender_2.txt`
3. Click "Analyze Tenders"
4. **Expected Result**: High similarity score (>95%) indicating possible collusion

**Technical Explanation**:
- Uses DistilBERT to encode each document into a 768-dimensional vector
- Computes cosine similarity between all document pairs
- Flags pairs exceeding the threshold

---

### Module B: Price-Guard (Over-Invoicing Detection)

**Purpose**: Detect inflated prices by comparing invoice amounts with market prices.

**Demo Steps**:
1. Go to the "Price-Guard" tab
2. Create a test invoice image with text like:
   ```
   Office Chair - 5000
   Laptop - 150000
   Pen - 500
   ```
3. Upload the image
4. Click "Scan Invoice"
5. **Expected Result**: Items flagged where invoice price > 2x market price

**Technical Explanation**:
- PyTesseract OCR extracts text from images
- Regex/NER extracts item names and prices
- BeautifulSoup scrapes mock market prices
- Flags items with >2x inflation

---

### Module C: Ghost-Hunter (Payroll Fraud Detection)

**Purpose**: Detect ghost employees and syndicates by analyzing shared metadata.

**Demo Steps**:
1. Go to the "Ghost-Hunter" tab
2. Upload `data/samples/sample_payroll.csv`
3. Set minimum cluster size to 5
4. Click "Scan Payroll"
5. **Expected Result**: Flags cluster of 6 "Fake Person" employees sharing same mobile/address/bank account

**Technical Explanation**:
- Builds a graph where employees sharing mobile/address/bank are connected
- Uses NetworkX to find connected components
- Flags large clusters as suspicious syndicates
- Optional Neo4j integration for production

---

### Module D: Welfare-Shield (Beneficiary Fraud Detection)

**Purpose**: Detect payments to deceased beneficiaries.

**Demo Steps**:
1. Go to the "Welfare-Shield" tab
2. Upload:
   - `data/samples/sample_death_registry.csv`
   - `data/samples/sample_disbursements.csv`
3. Set similarity threshold to 85
4. Click "Cross-Check Beneficiaries"
5. **Expected Result**: Flags 3-4 beneficiaries that match deceased persons in registry

**Technical Explanation**:
- Fuzzy matches beneficiary names with death registry using RapidFuzz
- Handles typos and spelling variations
- Flags matches above similarity threshold

---

## API Testing (Optional)

Visit `http://localhost:8000/docs` for interactive Swagger documentation.

### Example API Calls:

**Tender-Watch**:
```bash
curl -X POST "http://localhost:8000/tender-watch/scan" \
  -F "files=@data/samples/sample_tender_1.txt" \
  -F "files=@data/samples/sample_tender_2.txt"
```

**Ghost-Hunter**:
```bash
curl -X POST "http://localhost:8000/scan-payroll" \
  -F "csv_file=@data/samples/sample_payroll.csv"
```

---

## Troubleshooting

### Common Issues:

1. **PyTesseract error**: Install Tesseract OCR from https://github.com/UB-Mannheim/tesseract/wiki
2. **Torch installation issues**: Use `pip install torch --index-url https://download.pytorch.org/whl/cpu`
3. **spaCy model missing**: Run `python -m spacy download en_core_web_sm`
4. **Neo4j connection**: Set environment variable `NEO4J_URI=bolt://localhost:7687` (optional)

---

## Architecture Overview

```
Frontend (Streamlit) ←→ Backend Modules ←→ AI/ML Models
                              ↓
                         Database Layer
                    (Neo4j + SQLite optional)
```

**Key Technologies**:
- **NLP**: HuggingFace Transformers (DistilBERT)
- **Computer Vision**: PyTesseract OCR
- **Graph Analytics**: NetworkX / Neo4j
- **Fuzzy Matching**: RapidFuzz
- **Web Framework**: FastAPI + Streamlit

---

## Presentation Tips

1. **Start with the problem**: Government loses billions to procurement fraud, ghost employees, etc.
2. **Show the solution**: AI-powered unified platform with 4 specialized modules
3. **Live demo**: Run through all 4 modules with sample data
4. **Explain the AI**: Briefly cover transformers, OCR, graph algorithms
5. **Scale potential**: Mention how it can process thousands of documents in production
