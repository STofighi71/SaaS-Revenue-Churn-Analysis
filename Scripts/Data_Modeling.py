"""
data_modeling.py

Purpose
-------
Build a star schema in SQLite from the cleaned CSV datasets.
Populate fact and dimension tables for downstream analytics and KPI calculation.

Steps
-----
1. Load cleaned CSVs
2. Create SQLite database and tables
3. Insert data into dimension and fact tables
4. Ensure referential integrity between tables
5. Save database for analysis and queries

Output
------
- SQLite DB: data_cleaned.db
"""

# Import necessary libraries

import pandas as pd
import sqlite3
from pathlib import Path



# Define file paths and database connection parameters

BASE_DIR = Path(__file__).resolve().parents[1]
CLEAN_DATA_PATH = BASE_DIR / "Data" / "Cleaned"
DB_PATH = BASE_DIR / "Data" / "data_cleaned.db"



# create SQLite database and tables and connect to it

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()



# Load cleaned CSV datasets into pandas DataFrames

accounts = pd.read_csv(CLEAN_DATA_PATH / "accounts_clean.csv")
usage = pd.read_csv(CLEAN_DATA_PATH / "usage_events_clean.csv")
tickets = pd.read_csv(CLEAN_DATA_PATH / "support_tickets_clean.csv")
nps = pd.read_csv(CLEAN_DATA_PATH / "nps_clean.csv")
renewals = pd.read_csv(CLEAN_DATA_PATH / "renewals_clean.csv")
invoices = pd.read_csv(CLEAN_DATA_PATH / "invoices_clean.csv")



# Create dimension tables and insert data

accounts.to_sql("accounts_dim", conn, if_exists="replace", index=False)
usage.to_sql("usage_dim", conn, if_exists="replace", index=False)
tickets.to_sql("support_dim", conn, if_exists="replace", index=False)
nps.to_sql("nps_dim", conn, if_exists="replace", index=False)



# Create fact tables and insert data

renewals.to_sql("renewals_fact", conn, if_exists="replace", index=False)
invoices.to_sql("invoices_fact", conn, if_exists="replace", index=False)



# Check for referential integrity - find any renewals that do not have a corresponding account
# This is a critical step to ensure our star schema is properly linked and we can trust our analytics results.

orphan_renewals = pd.read_sql("""
SELECT * FROM renewals_fact
WHERE account_id NOT IN (SELECT account_id FROM accounts_dim)
""", conn)

print("Orphan renewals: ", len(orphan_renewals))


# save and close the database connection
conn.commit()
conn.close()
print("SQLite database created and populated successfully!")