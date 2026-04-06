"""
cleaning_pipeline.py

Fully automated data cleaning pipeline for B2B SaaS synthetic dataset.
Handles duplicates, missing values, inconsistent categories, orphaned keys,
impossible dates, and currency conversion.
"""

import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime
from pandas.api.types import is_numeric_dtype, is_string_dtype

# --- Paths ---
BASE_DIR = Path(__file__).resolve().parents[1]
RAW_DATA_PATH = BASE_DIR / "Data" / "Raw"
CLEAN_DATA_PATH = BASE_DIR / "Data" / "Cleaned"
LINEAGE_LOG_PATH = BASE_DIR / "Data" / "data_lineage_log.csv"
CLEAN_DATA_PATH.mkdir(parents=True, exist_ok=True)

# --- Lineage log ---
lineage_log = []

def log_transformation(table, issue, rows_affected, action):
    lineage_log.append({
        "timestamp": datetime.now(),
        "table": table,
        "issue": issue,
        "rows_affected": rows_affected,
        "action": action
    })

# --- Load datasets ---
accounts = pd.read_csv(RAW_DATA_PATH / "accounts.csv")
usage_events = pd.read_csv(RAW_DATA_PATH / "usage_events.csv")
support_tickets = pd.read_csv(RAW_DATA_PATH / "support_tickets.csv")
invoices = pd.read_csv(RAW_DATA_PATH / "invoices.csv")
renewals = pd.read_csv(RAW_DATA_PATH / "renewals.csv")
nps_survey = pd.read_csv(RAW_DATA_PATH / "nps_survey.csv")

# --- Remove duplicates ---
def remove_duplicates(df, table_name):
    before = len(df)
    df = df.drop_duplicates()
    removed = before - len(df)
    if removed > 0:
        log_transformation(table_name, "duplicate_rows", removed, "removed duplicates")
    return df

accounts = remove_duplicates(accounts, "accounts")
usage_events = remove_duplicates(usage_events, "usage_events")
support_tickets = remove_duplicates(support_tickets, "support_tickets")
invoices = remove_duplicates(invoices, "invoices")
renewals = remove_duplicates(renewals, "renewals")
nps_survey = remove_duplicates(nps_survey, "nps_survey")

# --- Missing values ---
def audit_missing(df, table_name):
    missing_report = pd.DataFrame({
        "column": df.columns,
        "missing_count": df.isna().sum(),
        "percent_missing": df.isna().mean() * 100
    })
    print(f"\nMissing values in {table_name}:\n", missing_report)
    return missing_report

def handle_missing(df, table_name):
    missing_report = audit_missing(df, table_name)
    for idx, row in missing_report.iterrows():
        col = row["column"]
        count = row["missing_count"]
        if count == 0:
            continue

        # Categorical / string columns
        if is_string_dtype(df[col]):
            if "account_manager" in col or "region" in col:
                df[col] = df[col].fillna("Unknown")
                log_transformation(table_name, col, count, "filled with 'Unknown'")
            elif "discount" in col:
                df[col] = df[col].fillna("No_Discount")
                log_transformation(table_name, col, count, "filled with 'No_Discount'")
            else:
                df[col] = df[col].fillna("Unknown")
                log_transformation(table_name, col, count, "filled with 'Unknown'")

        # Numeric columns
        elif is_numeric_dtype(df[col]):
            if "usage_count" in col:
                df[col] = df[col].fillna(0)
                log_transformation(table_name, col, count, "filled with 0")
            else:
                df[col] = df[col].fillna(df[col].median())
                log_transformation(table_name, col, count, "filled with median")

        # Other columns (datetime or unknown)
        else:
            df[col] = df[col].fillna("Unknown")
            log_transformation(table_name, col, count, "filled with 'Unknown' (fallback)")
    return df

accounts = handle_missing(accounts, "accounts")
usage_events = handle_missing(usage_events, "usage_events")
support_tickets = handle_missing(support_tickets, "support_tickets")
invoices = handle_missing(invoices, "invoices")
renewals = handle_missing(renewals, "renewals")
nps_survey = handle_missing(nps_survey, "nps_survey")

# --- Standardize tier ---
def standardize_tier(tier):
    if pd.isna(tier):
        return tier
    tier = tier.strip().lower()
    mapping = {
        "starter": "Starter",
        "growth": "Growth",
        "business": "Business",
        "enterprise": "Enterprise"
    }
    return mapping.get(tier, tier)

accounts["tier"] = accounts["tier"].apply(standardize_tier)

# --- Orphaned foreign keys in renewals ---
valid_accounts = set(accounts["account_id"])
before = len(renewals)
renewals = renewals[renewals["account_id"].isin(valid_accounts)]
removed = before - len(renewals)
log_transformation("renewals", "orphaned_account_id", removed, "removed records without valid account")

# --- Impossible dates in invoices ---
invoices["invoice_date"] = pd.to_datetime(invoices["invoice_date"])
invoices["paid_date"] = pd.to_datetime(invoices["paid_date"])
mask = invoices["paid_date"] < invoices["invoice_date"]
count = mask.sum()
invoices.loc[mask, "paid_date"] = invoices.loc[mask, "invoice_date"]
log_transformation("invoices", "paid_before_invoice", int(count), "corrected paid_date")

# --- Currency conversion ---
USD_TO_EUR = 0.92
mask = invoices["currency"] == "USD"
count = mask.sum()
invoices.loc[mask, "amount"] = invoices.loc[mask, "amount"] * USD_TO_EUR
invoices.loc[mask, "currency"] = "EUR"
log_transformation("invoices", "currency_conversion", int(count), "USD converted to EUR")

# --- Save cleaned datasets ---
accounts.to_csv(CLEAN_DATA_PATH / "accounts_clean.csv", index=False)
usage_events.to_csv(CLEAN_DATA_PATH / "usage_events_clean.csv", index=False)
support_tickets.to_csv(CLEAN_DATA_PATH / "support_tickets_clean.csv", index=False)
invoices.to_csv(CLEAN_DATA_PATH / "invoices_clean.csv", index=False)
renewals.to_csv(CLEAN_DATA_PATH / "renewals_clean.csv", index=False)
nps_survey.to_csv(CLEAN_DATA_PATH / "nps_clean.csv", index=False)

# --- Save lineage log ---
lineage_df = pd.DataFrame(lineage_log)
lineage_df.to_csv(LINEAGE_LOG_PATH, index=False)
print("\nData cleaning completed. Cleaned files saved to:", CLEAN_DATA_PATH)
print("Data lineage log saved to:", LINEAGE_LOG_PATH)