"""
Dummy Data Generator for Fiscal-Sentinel
Generates sample PDFs, Images, and CSVs for testing all 4 modules
"""

import os
from pathlib import Path
from fpdf import FPDF
from PIL import Image, ImageDraw, ImageFont
import pandas as pd

# Create directories
Path("data/tenders").mkdir(parents=True, exist_ok=True)
Path("data/invoices").mkdir(parents=True, exist_ok=True)
Path("data/payroll").mkdir(parents=True, exist_ok=True)
Path("data/welfare").mkdir(parents=True, exist_ok=True)

print("=" * 60)
print("FISCAL-SENTINEL DUMMY DATA GENERATOR")
print("=" * 60)

# ===== 1. GENERATE TENDER PDFs (95% identical for collusion test) =====
print("\n1. Generating Tender PDFs...")

# Common text (95% of content)
common_text = """
TENDER DOCUMENT FOR ROAD CONSTRUCTION PROJECT

PROJECT SCOPE:
Construction of 10 km highway with 4-lane configuration.

TECHNICAL SPECIFICATIONS:
- Asphalt thickness: 75mm
- Base layer: WMM (Wet Mix Macadam) 250mm
- Sub-base: GSB (Granular Sub Base) 200mm
- Drainage: RCC side drains at 500m intervals

FINANCIAL BID:
Total estimated cost: Rs. 5,00,00,000 (Five Crore Only)

PAYMENT TERMS:
- 10% advance on contract signing
- 40% on 50% completion
- 40% on 90% completion
- 10% retention money after defect liability period

QUALITY STANDARDS:
- IRC specifications compliance mandatory
- Third party quality testing
- Completion timeline: 18 months

PENALTIES:
Late delivery: Rs. 50,000 per day
Quality failure: 10% of contract value
"""

# Create Bid A
pdf_a = FPDF()
pdf_a.add_page()
pdf_a.set_font("Arial", size=12)
pdf_a.multi_cell(0, 10, "BID SUBMITTED BY: ABC CONSTRUCTION PRIVATE LIMITED")
pdf_a.multi_cell(0, 10, "Company Registration: CIN123456789")
pdf_a.multi_cell(0, 10, common_text)
pdf_a.output("data/tenders/bid_A.pdf")

# Create Bid B (95% identical)
pdf_b = FPDF()
pdf_b.add_page()
pdf_b.set_font("Arial", size=12)
pdf_b.multi_cell(0, 10, "BID SUBMITTED BY: XYZ BUILDERS LIMITED")
pdf_b.multi_cell(0, 10, "Company Registration: CIN987654321")
pdf_b.multi_cell(0, 10, common_text)
pdf_b.output("data/tenders/bid_B.pdf")

print("   ✓ Created bid_A.pdf and bid_B.pdf (95% identical)")

# ===== 2. GENERATE INVOICE IMAGE (with inflated price) =====
print("\n2. Generating Invoice Image...")

img = Image.new('RGB', (800, 600), color='white')
draw = ImageDraw.Draw(img)

# Try to use a better font, fallback to default
try:
    font_large = ImageFont.truetype("arial.ttf", 24)
    font_medium = ImageFont.truetype("arial.ttf", 18)
    font_small = ImageFont.truetype("arial.ttf", 14)
except:
    font_large = ImageFont.load_default()
    font_medium = ImageFont.load_default()
    font_small = ImageFont.load_default()

# Draw invoice content
draw.text((50, 30), "GOVERNMENT INVOICE", fill='black', font=font_large)
draw.text((50, 70), "Invoice No: INV-2025-001", fill='black', font=font_small)
draw.text((50, 100), "Date: 04-Jan-2025", fill='black', font=font_small)
draw.line((50, 130, 750, 130), fill='black', width=2)

draw.text((50, 160), "ITEM DESCRIPTION", fill='black', font=font_medium)
draw.text((500, 160), "AMOUNT", fill='black', font=font_medium)
draw.line((50, 190, 750, 190), fill='black', width=1)

# Inflated item
draw.text((50, 210), "High-End Gaming Laptop", fill='black', font=font_small)
draw.text((500, 210), "Rs. 1,50,000", fill='black', font=font_small)

draw.line((50, 450, 750, 450), fill='black', width=2)
draw.text((400, 470), "TOTAL: Rs. 1,50,000", fill='black', font=font_medium)

img.save("data/invoices/invoice_sample.png")
print("   ✓ Created invoice_sample.png (Laptop: Rs. 1,50,000)")

# ===== 3. GENERATE PAYROLL CSV (with ghost employees) =====
print("\n3. Generating Payroll CSV...")

payroll_data = {
    'Employee_ID': ['E001', 'E002', 'E003', 'E004', 'E005', 'E006'],
    'Name': [
        'Rajesh Kumar',
        'Priya Sharma',
        'Ghost Employee 1',
        'Ghost Employee 2',
        'Ghost Employee 3',
        'Legitimate Worker'
    ],
    'Mobile': [
        '9876543210',
        '9876543211',
        '9999999999',  # Same mobile
        '9999999999',  # Same mobile
        '9999999999',  # Same mobile
        '9876543212'
    ],
    'Bank_Acc': [
        'ACC12345',
        'ACC23456',
        'ACCGHOST',  # Same bank account
        'ACCGHOST',  # Same bank account
        'ACCGHOST',  # Same bank account
        'ACC34567'
    ]
}

df_payroll = pd.DataFrame(payroll_data)
df_payroll.to_csv("data/payroll/payroll.csv", index=False)
print("   ✓ Created payroll.csv (3 ghost employees with shared mobile & bank)")

# ===== 4. GENERATE WELFARE CSVs (with fuzzy matches) =====
print("\n4. Generating Welfare CSVs...")

pension_data = {
    'Beneficiary_ID': ['P001', 'P002', 'P003', 'P004'],
    'Name': [
        'Ramesh Kumar',      # Will match with death registry
        'Lakshmi Devi',      # Will match with death registry
        'Active Person',
        'Another Active'
    ],
    'Pension_Amount': [5000, 5000, 5000, 5000]
}

death_data = {
    'Deceased_ID': ['D001', 'D002', 'D003'],
    'Name': [
        'Ramesh Kr.',        # Fuzzy match with 'Ramesh Kumar'
        'Lakshmi Devi',      # Exact match
        'Some Other Person'
    ],
    'Date_of_Death': ['2023-05-15', '2023-08-20', '2024-01-10']
}

df_pension = pd.DataFrame(pension_data)
df_death = pd.DataFrame(death_data)

df_pension.to_csv("data/welfare/pension_list.csv", index=False)
df_death.to_csv("data/welfare/death_registry.csv", index=False)

print("   ✓ Created pension_list.csv and death_registry.csv")
print("     (2 deceased persons still receiving pensions)")

print("\n" + "=" * 60)
print("DUMMY DATA GENERATION COMPLETE!")
print("=" * 60)
print("\nGenerated Files:")
print("  📄 data/tenders/bid_A.pdf")
print("  📄 data/tenders/bid_B.pdf")
print("  🖼️  data/invoices/invoice_sample.png")
print("  📊 data/payroll/payroll.csv")
print("  📊 data/welfare/pension_list.csv")
print("  📊 data/welfare/death_registry.csv")
print("\nYou can now test all 4 modules!")
print("=" * 60)
