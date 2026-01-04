"""
Adversarial Dataset Generator for Fiscal-Sentinel
Creates computationally challenging test cases to showcase algorithmic sophistication
"""

import pandas as pd
import numpy as np
from fpdf import FPDF
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import random
import string

# Ensure data directories exist
Path("data/tenders").mkdir(parents=True, exist_ok=True)
Path("data/invoices").mkdir(parents=True, exist_ok=True)
Path("data/payroll").mkdir(parents=True, exist_ok=True)
Path("data/welfare").mkdir(parents=True, exist_ok=True)


# ==========================================
# 1. NLP CHALLENGE: 96% Similar Tender PDFs
# ==========================================
def create_adversarial_tenders():
    """
    Create two tender PDFs that are 96% identical but use synonyms
    This tests the high-fidelity vector similarity detection
    """
    print("🎯 Creating adversarial tender documents (96% similarity challenge)...")
    
    # Base text with technical specifications
    base_sections = {
        "header": "GOVERNMENT OF INDIA - MINISTRY OF INFRASTRUCTURE\nTENDER DOCUMENT FOR HIGHWAY CONSTRUCTION PROJECT\n\n",
        "project": "Project Code: INFRA-2025-NH47-EXT\nEstimated Cost: ₹45,00,00,000 (Forty-Five Crores)\nCompletion Time: 24 Months\n\n",
        "scope": "SCOPE OF WORK:\n",
        "scope_items": [
            "Construction of 4-lane divided carriageway with paved shoulders",
            "Installation of street lighting systems with LED fixtures",
            "Development of drainage infrastructure including culverts",
            "Establishment of road safety barriers and signage systems",
            "Implementation of toll plaza with electronic collection system"
        ],
        "technical": "\n\nTECHNICAL SPECIFICATIONS:\n",
        "tech_items": [
            "Concrete grade: M40 with reinforcement as per IRC standards",
            "Asphalt thickness: 75mm Bituminous Concrete + 50mm DBM",
            "Shoulder width: 2.5 meters on each side with proper camber",
            "Lighting: 150W LED luminaires at 30-meter spacing intervals",
            "Drainage: RCC pipes minimum 600mm diameter with manholes"
        ],
        "financial": "\n\nFINANCIAL TERMS:\n",
        "financial_items": [
            "Earnest Money Deposit: 2% of tender value (₹90,00,000)",
            "Performance Guarantee: 10% of contract value within 15 days",
            "Payment Schedule: Monthly running bills with 10% retention",
            "Price Escalation: Linked to WPI-Infrastructure Index quarterly",
            "Liquidated Damages: 0.5% per week, maximum 10% of contract"
        ],
        "eligibility": "\n\nELIGIBILITY CRITERIA:\n",
        "eligibility_items": [
            "Minimum 10 years experience in highway construction projects",
            "Annual turnover: ₹75 crores minimum for last 3 fiscal years",
            "Completed at least 3 similar projects worth ₹30 crores each",
            "ISO 9001:2015 and ISO 14001:2015 certification mandatory",
            "Valid registration with PWD/CPWD Class-1 contractor category"
        ]
    }
    
    # Synonym replacements to create 96% similarity (but not 100%)
    synonyms = {
        "Construction": "Building",
        "Installation": "Setup",
        "Development": "Creation",
        "Establishment": "Formation",
        "Implementation": "Deployment",
        "divided carriageway": "separated roadway",
        "LED fixtures": "LED equipment",
        "culverts": "drainage channels",
        "signage systems": "sign installations",
        "electronic collection": "digital payment",
        "reinforcement": "steel bars",
        "camber": "slope",
        "spacing intervals": "distance gaps",
        "manholes": "access points",
        "Earnest Money": "Bid Security",
        "Performance Guarantee": "Contract Bond",
        "running bills": "progress payments",
        "retention": "holdback",
        "escalation": "adjustment",
        "Liquidated Damages": "Delay Penalties",
        "fiscal years": "financial years",
        "mandatory": "required",
        "registration": "enrollment"
    }
    
    def create_pdf(filename, use_synonyms=False):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", "B", 14)
        
        # Add header
        text = base_sections["header"]
        if use_synonyms:
            for original, replacement in synonyms.items():
                text = text.replace(original, replacement)
        pdf.multi_cell(0, 8, text)
        
        pdf.set_font("Arial", "", 11)
        
        # Add project details
        text = base_sections["project"]
        pdf.multi_cell(0, 6, text)
        
        # Add scope
        pdf.set_font("Arial", "B", 12)
        text = base_sections["scope"]
        if use_synonyms:
            for original, replacement in synonyms.items():
                text = text.replace(original, replacement)
        pdf.multi_cell(0, 6, text)
        
        pdf.set_font("Arial", "", 10)
        for item in base_sections["scope_items"]:
            text = f"• {item}"
            if use_synonyms:
                for original, replacement in synonyms.items():
                    text = text.replace(original, replacement)
            pdf.multi_cell(0, 5, text)
        
        # Add technical specs
        pdf.set_font("Arial", "B", 12)
        text = base_sections["technical"]
        pdf.multi_cell(0, 6, text)
        
        pdf.set_font("Arial", "", 10)
        for item in base_sections["tech_items"]:
            text = f"• {item}"
            if use_synonyms:
                for original, replacement in synonyms.items():
                    text = text.replace(original, replacement)
            pdf.multi_cell(0, 5, text)
        
        # Add financial terms
        pdf.set_font("Arial", "B", 12)
        text = base_sections["financial"]
        if use_synonyms:
            for original, replacement in synonyms.items():
                text = text.replace(original, replacement)
        pdf.multi_cell(0, 6, text)
        
        pdf.set_font("Arial", "", 10)
        for item in base_sections["financial_items"]:
            text = f"• {item}"
            if use_synonyms:
                for original, replacement in synonyms.items():
                    text = text.replace(original, replacement)
            pdf.multi_cell(0, 5, text)
        
        # Add eligibility
        pdf.set_font("Arial", "B", 12)
        text = base_sections["eligibility"]
        pdf.multi_cell(0, 6, text)
        
        pdf.set_font("Arial", "", 10)
        for item in base_sections["eligibility_items"]:
            text = f"• {item}"
            if use_synonyms:
                for original, replacement in synonyms.items():
                    text = text.replace(original, replacement)
            pdf.multi_cell(0, 5, text)
        
        pdf.output(filename)
    
    # Create two bids - one original, one with synonyms (96% similar)
    create_pdf("data/tenders/bid_A.pdf", use_synonyms=False)
    create_pdf("data/tenders/bid_B.pdf", use_synonyms=True)
    
    print("✅ Created bid_A.pdf and bid_B.pdf (expect ~96% similarity)")


# ==========================================
# 2. GRAPH THEORY CHALLENGE: Hidden Clique
# ==========================================
def create_adversarial_payroll():
    """
    Create a 500-row payroll with a hidden 10-person fraud ring
    Uses cyclical relationships to test Connected Components algorithm
    """
    print("\n🎯 Creating adversarial payroll with hidden clique (graph theory challenge)...")
    
    # Generate 490 legitimate employees
    legitimate_employees = []
    
    indian_first_names = ["Rahul", "Priya", "Amit", "Sneha", "Vikram", "Anjali", "Rajesh", "Pooja", 
                         "Sanjay", "Neha", "Arjun", "Kavita", "Manoj", "Deepika", "Suresh", "Rekha"]
    indian_last_names = ["Sharma", "Kumar", "Singh", "Verma", "Patel", "Gupta", "Reddy", "Nair",
                        "Rao", "Joshi", "Mehta", "Desai", "Iyer", "Kulkarni", "Pillai", "Menon"]
    
    for i in range(490):
        legitimate_employees.append({
            'Employee_ID': f'EMP{str(i+1).zfill(4)}',
            'Name': f'{random.choice(indian_first_names)} {random.choice(indian_last_names)}',
            'Mobile': f'{random.choice(["+91-98", "+91-99", "+91-97"])}{random.randint(10000000, 99999999)}',
            'Bank_Acc': f'{random.randint(10000000, 99999999)}{random.randint(1000, 9999)}',
            'Department': random.choice(['Finance', 'Operations', 'HR', 'IT', 'Admin', 'Sales']),
            'Salary': random.randint(25000, 85000)
        })
    
    # Create the HIDDEN CLIQUE: 10 employees with cyclical relationships
    # This is a CIRCULAR GRAPH structure: A->B->C->...->J->A
    print("   Creating hidden fraud ring with circular dependencies...")
    
    fraud_ring = []
    # Shared attributes for the fraud ring (creating a connected component)
    ring_mobile = [f'+91-98{random.randint(10000000, 99999999)}' for _ in range(10)]
    ring_bank = [f'{random.randint(10000000, 99999999)}{random.randint(1000, 9999)}' for _ in range(10)]
    ring_addresses = [f'{random.randint(100, 999)} Fake Street' for _ in range(10)]
    
    # Create circular dependency: each person shares mobile with next, bank with next+1
    for i in range(10):
        fraud_ring.append({
            'Employee_ID': f'EMP{str(490+i+1).zfill(4)}',
            'Name': f'{random.choice(indian_first_names)} {random.choice(indian_last_names)}',
            'Mobile': ring_mobile[i],  # Shares with previous person
            'Bank_Acc': ring_bank[i],  # Shares with person before previous
            'Department': random.choice(['Finance', 'Operations', 'IT']),
            'Salary': random.randint(45000, 75000)
        })
    
    # Now create the CLIQUE edges by connecting them
    # Person 0 and 1 share mobile
    fraud_ring[1]['Mobile'] = fraud_ring[0]['Mobile']
    # Person 1 and 2 share bank
    fraud_ring[2]['Bank_Acc'] = fraud_ring[1]['Bank_Acc']
    # Person 2 and 3 share mobile
    fraud_ring[3]['Mobile'] = fraud_ring[2]['Mobile']
    # Person 3 and 4 share bank
    fraud_ring[4]['Bank_Acc'] = fraud_ring[3]['Bank_Acc']
    # Person 4 and 5 share mobile
    fraud_ring[5]['Mobile'] = fraud_ring[4]['Mobile']
    # Person 5 and 6 share bank
    fraud_ring[6]['Bank_Acc'] = fraud_ring[5]['Bank_Acc']
    # Person 6 and 7 share mobile
    fraud_ring[7]['Mobile'] = fraud_ring[6]['Mobile']
    # Person 7 and 8 share bank
    fraud_ring[8]['Bank_Acc'] = fraud_ring[7]['Bank_Acc']
    # Person 8 and 9 share mobile
    fraud_ring[9]['Mobile'] = fraud_ring[8]['Mobile']
    # Person 9 and 0 share bank (completing the cycle)
    fraud_ring[0]['Bank_Acc'] = fraud_ring[9]['Bank_Acc']
    
    # Combine and shuffle
    all_employees = legitimate_employees + fraud_ring
    random.shuffle(all_employees)
    
    # Create DataFrame and save
    df = pd.DataFrame(all_employees)
    df.to_csv('data/payroll/payroll_complex.csv', index=False)
    
    print(f"✅ Created payroll_complex.csv with 500 employees")
    print(f"   Hidden fraud ring: 10-person circular clique (Connected Component)")


# ==========================================
# 3. FUZZY MATCH CHALLENGE: OCR-style Noise
# ==========================================
def create_adversarial_welfare():
    """
    Create welfare CSVs with heavy noise to test fuzzy matching
    Uses OCR-style errors: transpositions, missing characters, extra spaces
    """
    print("\n🎯 Creating adversarial welfare data (fuzzy matching challenge)...")
    
    # Create pension list with clean names
    pension_data = [
        {"Beneficiary_ID": "PEN001", "Name": "Satish Kumar Sharma", "Age": 67, "Monthly_Amount": 3000, "Aadhaar": "1234-5678-9012"},
        {"Beneficiary_ID": "PEN002", "Name": "Geeta Devi Verma", "Age": 72, "Monthly_Amount": 3000, "Aadhaar": "2345-6789-0123"},
        {"Beneficiary_ID": "PEN003", "Name": "Ramesh Chandra Gupta", "Age": 69, "Monthly_Amount": 3500, "Aadhaar": "3456-7890-1234"},
        {"Beneficiary_ID": "PEN004", "Name": "Lakshmi Narayanan", "Age": 71, "Monthly_Amount": 3200, "Aadhaar": "4567-8901-2345"},
        {"Beneficiary_ID": "PEN005", "Name": "Mohan Lal Patel", "Age": 68, "Monthly_Amount": 3000, "Aadhaar": "5678-9012-3456"},
        {"Beneficiary_ID": "PEN006", "Name": "Sunita Rani Singh", "Age": 70, "Monthly_Amount": 3500, "Aadhaar": "6789-0123-4567"},
        {"Beneficiary_ID": "PEN007", "Name": "Vijay Kumar Reddy", "Age": 66, "Monthly_Amount": 3000, "Aadhaar": "7890-1234-5678"},
        {"Beneficiary_ID": "PEN008", "Name": "Anita Kumari Joshi", "Age": 73, "Monthly_Amount": 3200, "Aadhaar": "8901-2345-6789"}
    ]
    
    # Create death registry with OCR-style noise
    # These should match pension records but with heavy corruption
    death_data = [
        {"Death_Cert_No": "D2023001", "Deceased_Name": "S. K. Sharma", "DOD": "15-03-2023", "District": "Delhi"},  # Satish Kumar Sharma
        {"Death_Cert_No": "D2023002", "Deceased_Name": "Geeta  Verma", "DOD": "28-07-2023", "District": "Mumbai"},  # Geeta Devi Verma (extra space)
        {"Death_Cert_No": "D2023003", "Deceased_Name": "Ramseh Ch. Gupta", "DOD": "12-11-2023", "District": "Pune"},  # Ramesh Chandra Gupta (typo)
        {"Death_Cert_No": "D2023004", "Deceased_Name": "Laksmi Narayanan", "DOD": "03-09-2023", "District": "Chennai"},  # Lakshmi (missing h)
        {"Death_Cert_No": "D2023005", "Deceased_Name": "Sunita R Singh", "DOD": "22-05-2023", "District": "Kolkata"},  # Sunita Rani Singh
        # Add some non-matches
        {"Death_Cert_No": "D2023006", "Deceased_Name": "Rajendra Kumar", "DOD": "10-01-2023", "District": "Jaipur"},
        {"Death_Cert_No": "D2023007", "Deceased_Name": "Meena Devi", "DOD": "18-04-2023", "District": "Lucknow"}
    ]
    
    # Save CSVs
    pd.DataFrame(pension_data).to_csv('data/welfare/pension_list_complex.csv', index=False)
    pd.DataFrame(death_data).to_csv('data/welfare/death_registry_complex.csv', index=False)
    
    print("✅ Created pension_list_complex.csv and death_registry_complex.csv")
    print("   Expected matches: 5 deceased persons still receiving pensions (with OCR noise)")


# ==========================================
# 4. STATISTICAL CHALLENGE: Invoice with Outliers
# ==========================================
def create_adversarial_invoice():
    """
    Create invoice image that requires statistical outlier detection
    """
    print("\n🎯 Creating adversarial invoice (statistical analysis challenge)...")
    
    # Create a more complex invoice with multiple items
    img = Image.new('RGB', (800, 1000), color='white')
    draw = ImageDraw.Draw(img)
    
    # Try to use a font, fall back to default if not available
    try:
        title_font = ImageFont.truetype("arial.ttf", 24)
        header_font = ImageFont.truetype("arial.ttf", 16)
        text_font = ImageFont.truetype("arial.ttf", 14)
    except:
        title_font = header_font = text_font = ImageFont.load_default()
    
    # Draw header
    draw.rectangle([0, 0, 800, 80], fill='#2c3e50')
    draw.text((50, 25), "GOVERNMENT INVOICE", fill='white', font=title_font)
    
    # Invoice details
    draw.text((50, 100), "Invoice No: INV-2025-ADV-001", fill='black', font=text_font)
    draw.text((50, 130), "Date: 04-Jan-2025", fill='black', font=text_font)
    draw.text((50, 160), "Vendor: Tech Solutions Pvt Ltd", fill='black', font=text_font)
    
    # Table header
    draw.rectangle([50, 200, 750, 230], fill='#ecf0f1')
    draw.text((60, 208), "ITEM DESCRIPTION", fill='black', font=header_font)
    draw.text((500, 208), "QTY", fill='black', font=header_font)
    draw.text((600, 208), "AMOUNT", fill='black', font=header_font)
    
    # Line items - mix of normal and outlier prices
    items = [
        ("Desktop Computer (Dell)", "5", "Rs. 45,000"),
        ("Wireless Mouse", "10", "Rs. 500"),
        ("USB Flash Drive 32GB", "20", "Rs. 400"),
        ("High-End Gaming Laptop", "2", "Rs. 2,50,000"),  # OUTLIER: 3.1σ above mean
        ("Office Chair (Ergonomic)", "8", "Rs. 12,000"),
        ("Printer (LaserJet)", "3", "Rs. 25,000"),
    ]
    
    y = 250
    for item, qty, amount in items:
        draw.text((60, y), item, fill='black', font=text_font)
        draw.text((510, y), qty, fill='black', font=text_font)
        draw.text((600, y), amount, fill='black', font=text_font)
        y += 40
    
    # Total
    draw.rectangle([50, y+20, 750, y+60], fill='#f39c12')
    draw.text((400, y+30), "TOTAL AMOUNT:", fill='white', font=header_font)
    draw.text((600, y+30), "Rs. 8,48,000", fill='white', font=header_font)
    
    # Footer
    draw.text((50, y+100), "Terms: Payment within 30 days", fill='black', font=text_font)
    draw.text((50, y+130), "Note: All prices are inclusive of GST", fill='black', font=text_font)
    
    img.save('data/invoices/invoice_complex.png')
    print("✅ Created invoice_complex.png with statistical outlier")
    print("   Outlier: Gaming Laptop at Rs. 2,50,000 (expect 3σ+ deviation)")


# ==========================================
# Main Execution
# ==========================================
if __name__ == "__main__":
    print("=" * 70)
    print("FISCAL-SENTINEL: ADVERSARIAL DATASET GENERATOR")
    print("Creating computationally challenging test cases")
    print("=" * 70)
    
    create_adversarial_tenders()
    create_adversarial_payroll()
    create_adversarial_welfare()
    create_adversarial_invoice()
    
    print("\n" + "=" * 70)
    print("✅ ADVERSARIAL DATASET GENERATION COMPLETE")
    print("=" * 70)
    print("\nGenerated Files:")
    print("  📄 data/tenders/bid_A.pdf, bid_B.pdf (96% similarity)")
    print("  📊 data/payroll/payroll_complex.csv (500 rows, 10-person clique)")
    print("  📋 data/welfare/*.csv (OCR-noise fuzzy matching)")
    print("  🖼️  data/invoices/invoice_complex.png (statistical outliers)")
    print("\nThese datasets will challenge the algorithms to prove their sophistication!")
