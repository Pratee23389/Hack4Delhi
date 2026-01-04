"""Utility script to generate additional sample data for testing"""

import pandas as pd
from pathlib import Path
import random
from datetime import datetime, timedelta

# Create data directory if it doesn't exist
data_dir = Path("data/samples")
data_dir.mkdir(parents=True, exist_ok=True)

print("Generating additional sample data...")

# Generate larger payroll dataset
print("\n1. Generating extended payroll data...")
employees = []
base_id = 1000

# Add legitimate employees
for i in range(50):
    employees.append({
        'employee_id': f'E{base_id + i}',
        'name': f'Employee {i+1}',
        'mobile': f'98765{str(i).zfill(5)}',
        'address': f'{i+1} Street, City',
        'bank_account': f'ACC{str(i+1).zfill(5)}'
    })

# Add suspicious cluster 1 (ghost employees)
ghost_mobile = '9999999999'
ghost_address = '999 Fake Street'
ghost_bank = 'ACC99999'
for i in range(8):
    employees.append({
        'employee_id': f'GHOST{i+1}',
        'name': f'Ghost Employee {i+1}',
        'mobile': ghost_mobile,
        'address': ghost_address,
        'bank_account': ghost_bank
    })

# Add suspicious cluster 2 (syndicate)
syndicate_mobile = '8888888888'
syndicate_address = '888 Syndicate Lane'
for i in range(6):
    employees.append({
        'employee_id': f'SYN{i+1}',
        'name': f'Syndicate Member {i+1}',
        'mobile': syndicate_mobile,
        'address': syndicate_address,
        'bank_account': f'ACC888{i+1}'
    })

df = pd.DataFrame(employees)
df.to_csv(data_dir / 'payroll_extended.csv', index=False)
print(f"   ✓ Created payroll_extended.csv with {len(df)} employees")

# Generate realistic death registry
print("\n2. Generating extended death registry...")
deaths = []
start_date = datetime(2020, 1, 1)
for i in range(100):
    birth_date = start_date - timedelta(days=random.randint(20000, 30000))
    death_date = start_date + timedelta(days=random.randint(1, 1500))
    deaths.append({
        'name': f'Deceased Person {i+1}',
        'date_of_birth': birth_date.strftime('%Y-%m-%d'),
        'date_of_death': death_date.strftime('%Y-%m-%d'),
        'id_number': f'ID{str(i+1).zfill(5)}'
    })

df = pd.DataFrame(deaths)
df.to_csv(data_dir / 'death_registry_extended.csv', index=False)
print(f"   ✓ Created death_registry_extended.csv with {len(df)} records")

# Generate disbursements (including to deceased)
print("\n3. Generating pension disbursements...")
disbursements = []

# Add legitimate disbursements
for i in range(80):
    birth_date = (datetime(1950, 1, 1) - timedelta(days=random.randint(0, 7300))).strftime('%Y-%m-%d')
    disbursements.append({
        'beneficiary_name': f'Active Beneficiary {i+1}',
        'date_of_birth': birth_date,
        'account_number': f'BANK{str(i+1).zfill(5)}',
        'payment_id': f'PAY{str(i+1).zfill(5)}',
        'amount': random.randint(3000, 8000)
    })

# Add fraudulent disbursements (to deceased persons)
for i in range(15):
    deceased = deaths[i]
    # Introduce slight variations in names to test fuzzy matching
    name_variations = [
        deceased['name'],
        deceased['name'].replace('Person', 'Persn'),  # typo
        deceased['name'].replace(' ', '  '),  # extra space
    ]
    disbursements.append({
        'beneficiary_name': random.choice(name_variations),
        'date_of_birth': deceased['date_of_birth'],
        'account_number': f'BANKFRAUD{i}',
        'payment_id': f'PAYFRAUD{i}',
        'amount': random.randint(5000, 10000)
    })

df = pd.DataFrame(disbursements)
df.to_csv(data_dir / 'disbursements_extended.csv', index=False)
print(f"   ✓ Created disbursements_extended.csv with {len(df)} records")
print(f"     (includes ~15 fraudulent payments to deceased)")

# Generate invoice sample text
print("\n4. Generating sample invoice text...")
invoice_text = """GOVERNMENT INVOICE

Vendor: ABC Supplies Pvt Ltd
Invoice No: INV-2025-001
Date: 04-01-2025

ITEMS:
Office Chair - 5000.00
Office Desk - 15000.00
Laptop Computer - 150000.00
Printer - 25000.00
Pen Box (100 pcs) - 5000.00
Stapler - 500.00

SUBTOTAL: 200500.00
GST (18%): 36090.00
TOTAL: 236590.00

Payment Terms: Net 30 Days
Bank: ICICI Bank, Acc: 123456789
"""

with open(data_dir / 'sample_invoice.txt', 'w') as f:
    f.write(invoice_text)
print("   ✓ Created sample_invoice.txt")

print("\n" + "="*60)
print("SAMPLE DATA GENERATION COMPLETE!")
print("="*60)
print("\nGenerated files:")
print("  • payroll_extended.csv (64 employees, 2 suspicious clusters)")
print("  • death_registry_extended.csv (100 deceased persons)")
print("  • disbursements_extended.csv (95 payments, ~15 fraudulent)")
print("  • sample_invoice.txt (for OCR testing)")
print("\nYou can use these files for more comprehensive testing!")
