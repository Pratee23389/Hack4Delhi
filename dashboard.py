"""
Fiscal-Sentinel Streamlit Dashboard
Interactive UI for testing all 4 fraud detection modules
"""

import streamlit as st
import requests
import json

# Configuration
API_URL = "http://localhost:8000"

st.set_page_config(
    page_title="Fiscal-Sentinel",
    page_icon="🛡️",
    layout="wide"
)

# Title
st.title("🛡️ Fiscal-Sentinel: AI-Powered Fraud Detection")
st.markdown("**Unified Platform for Government Spending Fraud Detection**")
st.markdown("---")

# Create tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "📄 Procurement (Tender-Watch)",
    "💰 Spending (Price-Guard)",
    "👥 Payroll (Ghost-Hunter)",
    "🏥 Welfare (Welfare-Shield)"
])

# Tab 1: Procurement/Tender Analysis
with tab1:
    st.header("Module A: Tender-Watch - Bid Rigging Detection")
    st.markdown("Upload multiple tender PDFs to detect collusion and cartelization")
    
    uploaded_pdfs = st.file_uploader(
        "Upload Tender PDFs (2 or more)",
        type=['pdf'],
        accept_multiple_files=True,
        key="tender_pdfs"
    )
    
    if st.button("🔍 Analyze Tenders", key="analyze_tenders"):
        if uploaded_pdfs and len(uploaded_pdfs) >= 2:
            with st.spinner("Analyzing tender documents with AI..."):
                try:
                    files = [('files', (pdf.name, pdf, 'application/pdf')) for pdf in uploaded_pdfs]
                    response = requests.post(f"{API_URL}/api/tender", files=files)
                    
                    if response.status_code == 200:
                        result = response.json()
                        st.success(f"Analysis Complete! Status: {result['status']}")
                        
                        st.json(result)
                        
                        if result['flagged_pairs']:
                            st.error("⚠️ COLLUSION DETECTED!")
                            for pair in result['flagged_pairs']:
                                st.warning(f"🚨 {pair['reason']}")
                        else:
                            st.success("✅ No collusion detected")
                    else:
                        st.error(f"Error: {response.text}")
                except Exception as e:
                    st.error(f"Error: {str(e)}")
                    st.info("Make sure the backend is running: `uvicorn app.main:app --reload`")
        else:
            st.warning("Please upload at least 2 PDF files")

# Tab 2: Invoice/Price Analysis
with tab2:
    st.header("Module B: Price-Guard - Over-Invoicing Detection")
    st.markdown("Upload an invoice image to detect price inflation")
    
    uploaded_invoice = st.file_uploader(
        "Upload Invoice Image",
        type=['png', 'jpg', 'jpeg'],
        key="invoice_image"
    )
    
    if uploaded_invoice:
        st.image(uploaded_invoice, caption="Uploaded Invoice", width=400)
    
    if st.button("🔍 Scan Invoice", key="scan_invoice"):
        if uploaded_invoice:
            with st.spinner("Running OCR and analyzing prices..."):
                try:
                    files = {'file': (uploaded_invoice.name, uploaded_invoice, uploaded_invoice.type)}
                    response = requests.post(f"{API_URL}/api/price", files=files)
                    
                    if response.status_code == 200:
                        result = response.json()
                        st.success(f"Analysis Complete! Status: {result['status']}")
                        
                        with st.expander("📄 OCR Extracted Text"):
                            st.text(result['ocr_text'])
                        
                        st.json(result)
                        
                        if result['flagged_items']:
                            st.error("⚠️ OVER-INVOICING DETECTED!")
                            for item in result['flagged_items']:
                                col1, col2, col3 = st.columns(3)
                                col1.metric("Item", item['item'])
                                col2.metric("Invoice Price", f"₹{item['extracted_price']:,}")
                                col3.metric("Market Price", f"₹{item['market_price']:,}")
                                st.error(f"🚨 Price inflated by {item['inflation_percent']:.1f}%!")
                        else:
                            st.success("✅ No over-invoicing detected")
                    else:
                        st.error(f"Error: {response.text}")
                except Exception as e:
                    st.error(f"Error: {str(e)}")
                    st.info("Make sure the backend is running and Tesseract OCR is installed")
        else:
            st.warning("Please upload an invoice image")

# Tab 3: Payroll/Ghost Employee Analysis
with tab3:
    st.header("Module C: Ghost-Hunter - Payroll Fraud Detection")
    st.markdown("Upload payroll CSV to detect ghost employees and syndicates")
    
    st.info("CSV should have columns: Employee_ID, Name, Mobile, Bank_Acc")
    
    uploaded_payroll = st.file_uploader(
        "Upload Payroll CSV",
        type=['csv'],
        key="payroll_csv"
    )
    
    if st.button("🔍 Scan Payroll", key="scan_payroll"):
        if uploaded_payroll:
            with st.spinner("Building employee graph and detecting clusters..."):
                try:
                    files = {'file': (uploaded_payroll.name, uploaded_payroll, 'text/csv')}
                    response = requests.post(f"{API_URL}/api/ghost", files=files)
                    
                    if response.status_code == 200:
                        result = response.json()
                        st.success(f"Analysis Complete! Status: {result['status']}")
                        
                        # Display metrics with new format
                        col1, col2, col3, col4 = st.columns(4)
                        col1.metric("Total Employees", result.get('total_employees', 0))
                        col2.metric("Suspicious Clusters", result.get('suspicious_clusters', 0))
                        col3.metric("Graph Density", f"{result.get('graph_metrics', {}).get('overall_density', 0):.4f}")
                        col4.metric("Integrity Score", f"{result.get('integrity_score', 100):.1f}%")
                        
                        # Show graph metrics
                        if 'graph_metrics' in result:
                            st.info(f"📊 **Graph Analysis**: {result['graph_metrics']['total_nodes']} nodes, "
                                   f"{result['graph_metrics']['total_edges']} edges | "
                                   f"Algorithm: {result['graph_metrics'].get('centrality_algorithm', 'betweenness').title()} Centrality")
                        
                        # Display clusters with enhanced information
                        if result.get('clusters'):
                            st.error(f"⚠️ {len(result['clusters'])} FRAUD RING(S) DETECTED!")
                            for cluster in result['clusters']:
                                severity_color = "🔴" if cluster['severity'] == 'CRITICAL' else "🟠" if cluster['severity'] == 'HIGH' else "🟡"
                                with st.expander(f"{severity_color} Cluster {cluster['cluster_id']}: {cluster['size']} employees - {cluster['severity']}"):
                                    col_a, col_b = st.columns(2)
                                    col_a.metric("Cluster Size", cluster['size'])
                                    col_b.metric("Graph Density", f"{cluster['graph_density']:.1%}")
                                    
                                    # Show kingpin information
                                    if 'kingpin' in cluster:
                                        st.warning(f"👑 **Kingpin Identified**: {cluster['kingpin']['name']} "
                                                 f"(ID: {cluster['kingpin']['employee_id']}) | "
                                                 f"Centrality Score: {cluster['kingpin']['centrality_score']:.4f}")
                                        st.caption(f"ℹ️ {cluster['kingpin']['explanation']}")
                                    
                                    st.write(f"**Algorithm**: {cluster.get('algorithm', 'Graph Analysis')}")
                                    st.write(f"**Explanation**: {cluster.get('explanation', '')}")
                                    st.dataframe(cluster['employees'])
                        else:
                            st.success("✅ No suspicious clusters detected - payroll appears clean")
                        
                        # Show full JSON in expander
                        with st.expander("📋 View Full API Response"):
                            st.json(result)
                    else:
                        st.error(f"Error: {response.text}")
                except Exception as e:
                    st.error(f"Error: {str(e)}")
                    st.info("Make sure the backend is running")
        else:
            st.warning("Please upload a payroll CSV file")

# Tab 4: Welfare/Beneficiary Analysis
with tab4:
    st.header("Module D: Welfare-Shield - Beneficiary Fraud Detection")
    st.markdown("Cross-reference pension list with death registry to find deceased beneficiaries")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📋 Pension List")
        pension_file = st.file_uploader(
            "Upload Pension List CSV",
            type=['csv'],
            key="pension_csv"
        )
    
    with col2:
        st.subheader("⚰️ Death Registry")
        death_file = st.file_uploader(
            "Upload Death Registry CSV",
            type=['csv'],
            key="death_csv"
        )
    
    if st.button("🔍 Cross-Check Beneficiaries", key="check_welfare"):
        if pension_file and death_file:
            with st.spinner("Fuzzy matching beneficiaries against death registry..."):
                try:
                    files = {
                        'pension_file': (pension_file.name, pension_file, 'text/csv'),
                        'death_file': (death_file.name, death_file, 'text/csv')
                    }
                    response = requests.post(f"{API_URL}/api/welfare", files=files)
                    
                    if response.status_code == 200:
                        result = response.json()
                        st.success(f"Analysis Complete! Status: {result['status']}")
                        
                        col1, col2, col3 = st.columns(3)
                        col1.metric("Total Beneficiaries", result['total_beneficiaries'])
                        col2.metric("Flagged Cases", result['num_flagged'])
                        col3.metric("Flagged Amount", f"₹{result['total_flagged_amount']:,}")
                        
                        st.json(result)
                        
                        if result['flagged_beneficiaries']:
                            st.error(f"⚠️ {result['num_flagged']} DECEASED BENEFICIARY(IES) FOUND!")
                            for beneficiary in result['flagged_beneficiaries']:
                                with st.expander(f"🚨 {beneficiary['beneficiary_name']} (Match: {beneficiary['match_score']}%)"):
                                    st.write(f"**Beneficiary ID:** {beneficiary['beneficiary_id']}")
                                    st.write(f"**Matched Deceased:** {beneficiary['matched_deceased_name']}")
                                    st.write(f"**Date of Death:** {beneficiary['date_of_death']}")
                                    st.write(f"**Pension Amount:** ₹{beneficiary['pension_amount']:,}")
                        else:
                            st.success("✅ No deceased beneficiaries found")
                    else:
                        st.error(f"Error: {response.text}")
                except Exception as e:
                    st.error(f"Error: {str(e)}")
                    st.info("Make sure the backend is running")
        else:
            st.warning("Please upload both pension list and death registry CSV files")

# Sidebar
with st.sidebar:
    st.markdown("### About")
    st.markdown("""
    Fiscal-Sentinel is an AI-powered platform that detects:
    - 📄 **Bid Rigging** in procurement
    - 💰 **Over-Invoicing** in spending
    - 👥 **Ghost Employees** in payroll
    - 🏥 **Deceased Beneficiaries** in welfare
    """)
    
    st.markdown("### Status")
    try:
        response = requests.get(f"{API_URL}/")
        if response.status_code == 200:
            st.success("✅ Backend Online")
        else:
            st.error("❌ Backend Offline")
    except:
        st.error("❌ Backend Offline")
        st.info("Start backend:\n`uvicorn app.main:app --reload`")
    
    st.markdown("---")
    st.markdown("**Tech Stack:**")
    st.markdown("- Sentence Transformers")
    st.markdown("- PyTesseract OCR")
    st.markdown("- NetworkX Graphs")
    st.markdown("- RapidFuzz Matching")
