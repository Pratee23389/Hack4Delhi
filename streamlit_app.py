"""Streamlit dashboard for the Fiscal-Sentinel platform.

Provides a simple UI with four tabs:
- Tender-Watch (Procurement Fraud)
- Price-Guard (Spending Fraud)
- Ghost-Hunter (Payroll & Contract Fraud)
- Welfare-Shield (Beneficiary Fraud)

Each tab lets the user upload the relevant files and runs the
corresponding analysis functions directly in-process (no network calls
needed during the hackathon), reusing the same Python modules as the
FastAPI backend.
"""

import streamlit as st
import sys
import traceback

try:
    from app.modules import tender_watch, price_guard, graph_fraud, welfare_shield
    MODULES_LOADED = True
except Exception as e:
    MODULES_LOADED = False
    MODULE_ERROR = str(e)


st.set_page_config(page_title="Fiscal-Sentinel Dashboard", layout="wide")
st.title("Fiscal-Sentinel: Unified AI Fraud Detection for Government Spending")

if not MODULES_LOADED:
    st.error("⚠️ Dependencies Not Installed")
    st.write("""Please install required packages first:
    
```bash
install_dependencies.bat
```

Or manually:
```bash
pip install -r requirements.txt
```
    """)
    st.write(f"**Error Details:** {MODULE_ERROR}")
    st.stop()


tab1, tab2, tab3, tab4 = st.tabs(
    ["Tender-Watch (Procurement)", "Price-Guard (Spending)", "Ghost-Hunter (Payroll)", "Welfare-Shield (Beneficiaries)"]
)


with tab1:
    st.header("Module A: Tender-Watch – Bid Rigging & Cartelization")
    uploaded_pdfs = st.file_uploader(
        "Upload tender / bid PDF documents (2+ files)",
        type=["pdf"],
        accept_multiple_files=True,
    )
    threshold = st.slider("Similarity threshold", min_value=0.7, max_value=0.99, value=0.95, step=0.01)

    if st.button("Analyze Tenders", disabled=not uploaded_pdfs):
        try:
            pdf_bytes_list = [f.read() for f in uploaded_pdfs]
            with st.spinner("Running Transformer model to compare bids..."):
                result = tender_watch.analyze_pdfs(pdf_bytes_list, similarity_threshold=threshold)
            st.subheader("Results")
            st.json(result)
        except Exception as e:
            st.error(f"Error analyzing tenders: {str(e)}")
            st.code(traceback.format_exc())


with tab2:
    st.header("Module B: Price-Guard – Over-Invoicing Detection")
    uploaded_invoice = st.file_uploader(
        "Upload an invoice image (PNG/JPEG)",
        type=["png", "jpg", "jpeg"],
        accept_multiple_files=False,
        key="invoice_upload",
    )

    if st.button("Scan Invoice", disabled=uploaded_invoice is None):
        try:
            invoice_bytes = uploaded_invoice.read()
            with st.spinner("Running OCR and estimating market prices..."):
                result = price_guard.analyze_invoice_image(invoice_bytes)
            st.subheader("Detected Over-Invoicing")
            st.json(result)
        except Exception as e:
            st.error(f"Error scanning invoice: {str(e)}")
            st.code(traceback.format_exc())


with tab3:
    st.header("Module C: Ghost-Hunter – Payroll & Contract Fraud")
    uploaded_csv = st.file_uploader(
        "Upload payroll CSV (employee_id,name,mobile,address,bank_account)",
        type=["csv"],
        accept_multiple_files=False,
        key="payroll_upload",
    )
    min_cluster_size = st.slider("Minimum cluster size to flag", min_value=3, max_value=20, value=5)

    if st.button("Scan Payroll", disabled=uploaded_csv is None):
        try:
            csv_bytes = uploaded_csv.read()
            with st.spinner("Building employee graph and finding suspicious clusters..."):
                result = graph_fraud.scan_payroll_csv(csv_bytes, min_cluster_size=min_cluster_size)
            st.subheader("High-Risk Employee Clusters")
            st.json(result)
        except Exception as e:
            st.error(f"Error scanning payroll: {str(e)}")
            st.code(traceback.format_exc())


with tab4:
    st.header("Module D: Welfare-Shield – Beneficiary Fraud Detection")
    col1, col2 = st.columns(2)
    with col1:
        death_registry_file = st.file_uploader(
            "Upload Death Registry CSV (name,date_of_birth,...) ",
            type=["csv"],
            accept_multiple_files=False,
            key="death_registry_upload",
        )
    with col2:
        disbursement_file = st.file_uploader(
            "Upload Pension Disbursement CSV (beneficiary_name,date_of_birth,...) ",
            type=["csv"],
            accept_multiple_files=False,
            key="disbursement_upload",
        )

    similarity_thresh = st.slider("Name+DOB similarity threshold", 70, 100, 85)

    ready = death_registry_file is not None and disbursement_file is not None
    if st.button("Cross-Check Beneficiaries", disabled=not ready):
        try:
            dr_bytes = death_registry_file.read()
            disb_bytes = disbursement_file.read()
            with st.spinner("Fuzzy matching beneficiaries against death registry..."):
                result = welfare_shield.cross_reference_death_registry(
                    dr_bytes, disb_bytes, similarity_threshold=similarity_thresh
                )
            st.subheader("High-Risk Payments")
            st.json(result)
        except Exception as e:
            st.error(f"Error cross-checking beneficiaries: {str(e)}")
            st.code(traceback.format_exc())

