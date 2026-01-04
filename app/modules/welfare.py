"""
Welfare-Shield Module
Detects deceased beneficiaries still receiving payments using fuzzy matching
"""

import pandas as pd
from rapidfuzz import fuzz, process
from io import BytesIO


def analyze_welfare(pension_csv_bytes, death_csv_bytes):
    """
    Cross-reference pension list with death registry
    Returns beneficiaries that match deceased persons (fuzzy score > 85)
    """
    # Load both CSVs
    df_pension = pd.read_csv(BytesIO(pension_csv_bytes))
    df_death = pd.read_csv(BytesIO(death_csv_bytes))
    
    # Detect name column (handle different column names)
    pension_name_col = 'Name' if 'Name' in df_pension.columns else 'Beneficiary_Name'
    death_name_col = 'Deceased_Name' if 'Deceased_Name' in df_death.columns else 'Name'
    
    # Get lists of names
    pension_names = df_pension[pension_name_col].tolist()
    death_names = df_death[death_name_col].tolist()
    
    # Find matches using fuzzy matching
    flagged_beneficiaries = []
    
    for idx, pension_name in enumerate(pension_names):
        # Find best match in death registry
        best_match = process.extractOne(
            pension_name,
            death_names,
            scorer=fuzz.token_sort_ratio
        )
        
        if best_match and best_match[1] > 85:  # Score > 85
            matched_name = best_match[0]
            score = best_match[1]
            
            # Get full records
            pension_record = df_pension.iloc[idx].to_dict()
            death_record = df_death[df_death['Name'] == matched_name].iloc[0].to_dict()
            
            flagged_beneficiaries.append({
                'beneficiary_id': pension_record.get('Beneficiary_ID', 'N/A'),
                'beneficiary_name': pension_name,
                'matched_deceased_name': matched_name,
                'match_score': round(score, 2),
                'pension_amount': pension_record.get('Pension_Amount', 0),
                'date_of_death': death_record.get('Date_of_Death', 'N/A'),
                'status': 'DECEASED BENEFICIARY RECEIVING PAYMENT'
            })
    
    total_flagged_amount = sum(b.get('pension_amount', 0) for b in flagged_beneficiaries)
    
    return {
        'total_beneficiaries': len(df_pension),
        'total_deceased_records': len(df_death),
        'flagged_beneficiaries': flagged_beneficiaries,
        'num_flagged': len(flagged_beneficiaries),
        'total_flagged_amount': total_flagged_amount,
        'status': 'WARNING' if flagged_beneficiaries else 'CLEAR'
    }
