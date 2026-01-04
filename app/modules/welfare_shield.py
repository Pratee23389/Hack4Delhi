"""Welfare-Shield module

Detects possible payments to deceased or fake beneficiaries by
cross-referencing a death registry with pension disbursement records.

High-level idea:
- Load two CSVs into pandas DataFrames:
  * Death Registry: name, date_of_birth, date_of_death, id_number
  * Pension Disbursement: beneficiary_name, date_of_birth, account_number, payment_id
- Use fuzzy matching on (name, date_of_birth) to match beneficiaries to
  death records even if there are minor spelling differences.
- Flag any disbursement where a strong fuzzy match exists in the
  death registry as "High Risk".
"""

from __future__ import annotations

from io import BytesIO
from typing import Dict, Any, List

import pandas as pd
from rapidfuzz import fuzz, process


def _load_death_registry(df_bytes: bytes) -> pd.DataFrame:
    df = pd.read_csv(BytesIO(df_bytes))
    # Normalize column names for robustness
    df.columns = [c.strip().lower() for c in df.columns]
    required = ["name", "date_of_birth"]
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise ValueError(f"Death registry missing required columns: {missing}")
    return df


def _load_disbursements(df_bytes: bytes) -> pd.DataFrame:
    df = pd.read_csv(BytesIO(df_bytes))
    df.columns = [c.strip().lower() for c in df.columns]
    required = ["beneficiary_name", "date_of_birth"]
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise ValueError(f"Disbursement file missing required columns: {missing}")
    return df


def _make_key(name: str, dob: str) -> str:
    return f"{name.strip().lower()}|{str(dob).strip()}"


def cross_reference_death_registry(
    death_registry_bytes: bytes,
    disbursement_bytes: bytes,
    similarity_threshold: int = 85,
) -> Dict[str, Any]:
    """Main entrypoint used by FastAPI and Streamlit.

    Args:
        death_registry_bytes: CSV bytes of the death registry.
        disbursement_bytes: CSV bytes of pension disbursements.
        similarity_threshold: Fuzzy similarity above which we flag.
    """

    death_df = _load_death_registry(death_registry_bytes)
    disb_df = _load_disbursements(disbursement_bytes)

    # Create string keys combining name and DOB for fuzzy comparison
    death_df["match_key"] = death_df.apply(
        lambda r: _make_key(r.get("name", ""), r.get("date_of_birth", "")), axis=1
    )
    disb_df["match_key"] = disb_df.apply(
        lambda r: _make_key(r.get("beneficiary_name", ""), r.get("date_of_birth", "")), axis=1
    )

    death_keys = death_df["match_key"].tolist()

    high_risk_records: List[Dict[str, Any]] = []

    # For each disbursement, find the best fuzzy match in the death registry
    for _, row in disb_df.iterrows():
        key = row["match_key"]
        if not key.strip():
            continue

        best_match = process.extractOne(key, death_keys, scorer=fuzz.token_sort_ratio)
        if best_match is None:
            continue

        matched_key, score, idx = best_match
        if score >= similarity_threshold:
            death_record = death_df.iloc[int(idx)].to_dict()
            risk = {
                "beneficiary_name": row.get("beneficiary_name"),
                "beneficiary_dob": row.get("date_of_birth"),
                "payment_row": row.to_dict(),
                "matched_death_record": death_record,
                "similarity_score": int(score),
                "flag": "Beneficiary appears in death registry",
            }
            high_risk_records.append(risk)

    return {
        "similarity_threshold": similarity_threshold,
        "num_disbursements": int(len(disb_df)),
        "num_deceased_matches": len(high_risk_records),
        "high_risk_payments": high_risk_records,
    }

