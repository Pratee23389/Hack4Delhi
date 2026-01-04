"""
Simple Demo Mode for Fiscal-Sentinel
Run this if dependencies are not fully installed yet
"""

import streamlit as st
import json

st.set_page_config(page_title="Fiscal-Sentinel Dashboard (Demo Mode)", layout="wide")

st.title("🛡️ Fiscal-Sentinel: AI Fraud Detection Platform")
st.info("⚠️ Running in DEMO MODE - Install dependencies for full functionality: `python install.py`")

tab1, tab2, tab3, tab4 = st.tabs([
    "Tender-Watch (Procurement)", 
    "Price-Guard (Spending)", 
    "Ghost-Hunter (Payroll)", 
    "Welfare-Shield (Beneficiaries)"
])

with tab1:
    st.header("📄 Module A: Tender-Watch – Bid Rigging Detection")
    st.write("""
    **Technology**: DistilBERT Transformer + Cosine Similarity
    
    **How it works**:
    1. Extracts text from tender PDF documents
    2. Encodes each document into a 768-dimensional vector using DistilBERT
    3. Computes cosine similarity between all pairs
    4. Flags pairs with >95% similarity as potential collusion
    """)
    
    uploaded_pdfs = st.file_uploader(
        "Upload tender / bid PDF documents (2+ files)",
        type=["pdf", "txt"],
        accept_multiple_files=True,
        key="tender_upload"
    )
    
    if st.button("Analyze Tenders (Demo)", disabled=not uploaded_pdfs):
        # Mock result
        result = {
            "total_documents": len(uploaded_pdfs),
            "similarity_threshold": 0.95,
            "flagged_pairs": [
                {
                    "doc_indices": [0, 1],
                    "similarity": 0.97,
                    "collusion_risk": True,
                    "reason": "Very high textual similarity detected - possible bid rigging"
                }
            ]
        }
        st.success("Analysis Complete!")
        st.json(result)

with tab2:
    st.header("💰 Module B: Price-Guard – Over-Invoicing Detection")
    st.write("""
    **Technology**: PyTesseract OCR + BeautifulSoup Web Scraping
    
    **How it works**:
    1. Runs OCR on invoice image to extract text
    2. Parses item names and prices using regex/NER
    3. Scrapes market prices from GeM/Amazon
    4. Flags items where invoice price > 2x market price
    """)
    
    uploaded_invoice = st.file_uploader(
        "Upload an invoice image (PNG/JPEG)",
        type=["png", "jpg", "jpeg"],
        key="invoice_upload"
    )
    
    if st.button("Scan Invoice (Demo)", disabled=uploaded_invoice is None):
        result = {
            "ocr_text_preview": "Office Chair - 5000.00\nLaptop - 150000.00\nPen - 500.00",
            "items_summary": {
                "num_items": 3,
                "num_inflated": 2,
                "inflated_items": [
                    {
                        "name": "Office Chair",
                        "invoice_price": 5000.0,
                        "market_price": 500.0,
                        "price_inflation_factor": 10.0,
                        "flag": "Price Inflation"
                    },
                    {
                        "name": "Pen",
                        "invoice_price": 500.0,
                        "market_price": 50.0,
                        "price_inflation_factor": 10.0,
                        "flag": "Price Inflation"
                    }
                ]
            }
        }
        st.warning("2 items flagged for over-invoicing!")
        st.json(result)

with tab3:
    st.header("👥 Module C: Ghost-Hunter – Payroll Fraud Detection")
    st.write("""
    **Technology**: NetworkX Graph Analysis + Connected Components
    
    **How it works**:
    1. Creates a graph where employees are nodes
    2. Connects employees sharing mobile/address/bank account
    3. Finds clusters using connected components algorithm
    4. Flags clusters with >5 employees as suspicious syndicates
    """)
    
    uploaded_csv = st.file_uploader(
        "Upload payroll CSV (employee_id,name,mobile,address,bank_account)",
        type=["csv"],
        key="payroll_upload"
    )
    
    if st.button("Scan Payroll (Demo)", disabled=uploaded_csv is None):
        result = {
            "num_employees": 15,
            "num_edges": 15,
            "num_risky_clusters": 1,
            "risky_clusters": [
                {
                    "size": 6,
                    "employee_ids": ["GHOST1", "GHOST2", "GHOST3", "GHOST4", "GHOST5", "GHOST6"],
                    "avg_degree": 5.0,
                    "description": "Employees sharing contact or banking details – possible ghost or syndicate."
                }
            ]
        }
        st.error("Suspicious cluster detected!")
        st.json(result)

with tab4:
    st.header("📋 Module D: Welfare-Shield – Beneficiary Fraud Detection")
    st.write("""
    **Technology**: RapidFuzz Fuzzy String Matching
    
    **How it works**:
    1. Loads death registry and pension disbursement CSVs
    2. Uses fuzzy matching on (name + date_of_birth)
    3. Handles typos and spelling variations
    4. Flags beneficiaries with >85% match to deceased persons
    """)
    
    col1, col2 = st.columns(2)
    with col1:
        death_reg = st.file_uploader(
            "Upload Death Registry CSV",
            type=["csv"],
            key="death_upload"
        )
    with col2:
        disbursements = st.file_uploader(
            "Upload Pension Disbursements CSV",
            type=["csv"],
            key="disb_upload"
        )
    
    if st.button("Cross-Check (Demo)", disabled=not (death_reg and disbursements)):
        result = {
            "similarity_threshold": 85,
            "num_disbursements": 6,
            "num_deceased_matches": 3,
            "high_risk_payments": [
                {
                    "beneficiary_name": "Ram Prasad",
                    "beneficiary_dob": "1945-03-15",
                    "matched_death_record": {
                        "name": "Ram Prasad",
                        "date_of_birth": "1945-03-15",
                        "date_of_death": "2023-08-10"
                    },
                    "similarity_score": 100,
                    "flag": "Beneficiary appears in death registry"
                }
            ]
        }
        st.error("3 high-risk payments detected!")
        st.json(result)

st.sidebar.title("ℹ️ About")
st.sidebar.info("""
**Fiscal-Sentinel** detects fraud in government spending using AI:

- **Tender-Watch**: Bid rigging (Transformers)
- **Price-Guard**: Over-invoicing (OCR)
- **Ghost-Hunter**: Payroll fraud (Graphs)
- **Welfare-Shield**: Beneficiary fraud (Fuzzy matching)

**Status**: Demo Mode
**To enable full AI**: Run `python install.py`
""")

st.sidebar.success("""
**Sample Data Available**:
- `data/samples/sample_payroll.csv`
- `data/samples/sample_death_registry.csv`
- `data/samples/sample_disbursements.csv`
- `data/samples/sample_tender_*.txt`
""")
