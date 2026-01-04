# Fiscal-Sentinel 🛡️

**Unified AI Platform for Government Spending Fraud Detection**

A comprehensive hackathon project featuring 4 AI-powered modules to detect procurement fraud, over-invoicing, ghost employees, and beneficiary fraud.

---

## 🎯 Project Overview

Fiscal-Sentinel combats financial fraud in government spending through:

1. **Tender-Watch**: Detects bid rigging and cartelization in procurement
2. **Price-Guard**: Identifies over-invoicing and price inflation
3. **Ghost-Hunter**: Finds ghost employees and payroll syndicates
4. **Welfare-Shield**: Flags payments to deceased beneficiaries

---

## 🚀 Quick Start (2 Steps)

### Step 1: Install Dependencies

**Easiest Method** (Recommended):
```bash
python install.py
```

**Alternative Methods**:

Windows Batch File:
```bash
install_dependencies.bat
```

Manual Installation:
```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

**Note**: Installation takes 5-10 minutes on first run (downloads ~500MB of AI models).

### Step 2: Run the Application

**Option A: Streamlit Dashboard** (Recommended for demos):
```bash
run_dashboard.bat
```
OR
```bash
streamlit run streamlit_app.py
```

**Option B: FastAPI Backend** (For API integration):
```bash
run_api.bat
```
OR
```bash
uvicorn app.main:app --reload
```

Access points:
- Streamlit Dashboard: http://localhost:8501
- FastAPI Docs: http://localhost:8000/docs

---

## 📁 Project Structure

```
Fiscal-Sentinel/
├── app/
│   ├── main.py                      # FastAPI application
│   └── modules/
│       ├── tender_watch.py          # Module A: Bid rigging detection
│       ├── price_guard.py           # Module B: Over-invoicing detection
│       ├── graph_fraud.py           # Module C: Ghost employee detection
│       └── welfare_shield.py        # Module D: Beneficiary fraud detection
├── data/
│   └── samples/                     # Sample test data
│       ├── sample_payroll.csv
│       ├── sample_death_registry.csv
│       ├── sample_disbursements.csv
│       ├── sample_tender_1.txt
│       └── sample_tender_2.txt
├── streamlit_app.py                 # Dashboard UI
├── config.py                        # Configuration settings
├── requirements.txt                 # Python dependencies
├── setup.bat                        # Automated setup script
├── run_api.bat                      # Start FastAPI
├── run_dashboard.bat                # Start Streamlit
├── README.md                        # This file
└── DEMO_GUIDE.md                    # Detailed demo instructions
```

---

## 🧪 Test with Sample Data

Sample data is provided in `data/samples/`:

1. **Payroll CSV**: Contains 6 suspicious employees sharing same contact info
2. **Death Registry + Disbursements**: 3-4 deceased persons still receiving payments
3. **Tender Documents**: Two nearly identical bids (>95% similarity)

See [DEMO_GUIDE.md](DEMO_GUIDE.md) for step-by-step testing instructions.

---

## 🛠️ Tech Stack

### Backend
- **FastAPI**: Modern Python web framework
- **Python 3.8+**: Core language

### AI/ML
- **HuggingFace Transformers**: DistilBERT for document similarity
- **PyTorch**: Deep learning framework
- **PyTesseract**: OCR for invoice scanning
- **spaCy**: NLP and named entity recognition

### Data & Analytics
- **pandas**: Data manipulation
- **NetworkX**: In-memory graph analysis
- **Neo4j**: Optional graph database
- **RapidFuzz**: Fuzzy string matching

### Web Scraping
- **BeautifulSoup4**: HTML parsing
- **Selenium**: Browser automation (optional)

### Frontend
- **Streamlit**: Interactive dashboard

---

## 📊 Module Details

### Module A: Tender-Watch
- **Tech**: DistilBERT embeddings + cosine similarity
- **Input**: Multiple PDF tender documents
- **Output**: Pairs with >95% similarity flagged as collusion risk

### Module B: Price-Guard
- **Tech**: PyTesseract OCR + BeautifulSoup price scraping
- **Input**: Invoice images
- **Output**: Items where price > 2x market price

### Module C: Ghost-Hunter
- **Tech**: NetworkX graph analysis + connected components
- **Input**: Payroll CSV
- **Output**: Employee clusters sharing metadata (>5 employees)

### Module D: Welfare-Shield
- **Tech**: RapidFuzz fuzzy matching
- **Input**: Death registry + disbursement CSVs
- **Output**: Beneficiaries matching deceased persons (>85% similarity)

---

## 🎓 For Hackathon Judges

### Key Highlights
✅ **4 Complete AI Modules** - Each solving a real fraud detection problem  
✅ **Production-Ready Code** - Clean, documented, explainable  
✅ **Working Demo** - Full Streamlit dashboard + FastAPI backend  
✅ **Sample Data Included** - Test immediately without setup  
✅ **Scalable Architecture** - Can handle production workloads  

### Innovation Points
- **Multi-modal AI**: Combines NLP, CV, and graph analytics
- **Explainable**: Each decision can be traced and justified
- **Modular**: Each module works independently
- **Practical**: Solves real problems costing billions annually

---

## 🔧 Configuration

Edit `config.py` to customize:
- Model paths and thresholds
- Neo4j connection (optional)
- Data directories

Environment variables:
```bash
set NEO4J_URI=bolt://localhost:7687
set NEO4J_USER=neo4j
set NEO4J_PASSWORD=your_password
```

---

## 📝 API Documentation

When running FastAPI backend, visit:
- Interactive docs: http://localhost:8000/docs
- OpenAPI schema: http://localhost:8000/openapi.json

### Example Endpoints

**POST /tender-watch/scan** - Analyze tender documents  
**POST /price-guard/scan** - Scan invoice image  
**POST /scan-payroll** - Check payroll for ghost employees  
**POST /welfare-shield/scan** - Cross-check beneficiaries  

---

## 🐛 Troubleshooting

**Issue**: PyTesseract not found  
**Solution**: Install Tesseract OCR: https://github.com/UB-Mannheim/tesseract/wiki

**Issue**: Torch installation fails  
**Solution**: `pip install torch --index-url https://download.pytorch.org/whl/cpu`

**Issue**: spaCy model missing  
**Solution**: `python -m spacy download en_core_web_sm`

**Issue**: Out of memory  
**Solution**: Reduce batch size or use smaller model (e.g., `distilbert-base-uncased`)

---

## 🤝 Contributing

This is a hackathon project. For production deployment:
1. Add authentication/authorization
2. Implement database persistence
3. Add comprehensive logging
4. Set up CI/CD pipelines
5. Add unit and integration tests

---

## 📄 License

MIT License - Feel free to use for your hackathon or production needs.

---

## 👥 Team

Built for hackathon demonstration of AI-powered government fraud detection.

---

## 🎬 Demo Video Script

1. **Introduction** (30s): Problem statement - billions lost to fraud
2. **Architecture** (30s): Show 4 modules and tech stack
3. **Live Demo** (3 min): Run through all 4 modules with sample data
4. **Results** (30s): Show flagged fraud cases
5. **Impact** (30s): Scalability and real-world deployment potential

---

**Ready to detect fraud? Run `setup.bat` and then `run_dashboard.bat`!** 🚀
