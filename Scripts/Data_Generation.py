"""
Synthetic SaaS Dataset Generator

This script generates synthetic datasets that simulate a B2B SaaS business.

The company sells subscription licenses across four tiers:
Starter, Growth, Business, Enterprise

And operates across three regions:
Europe, North America, APAC.

Datasets generated:

1. accounts
2. usage_events
3. support_tickets
4. invoices
5. renewals
6. nps_survey

Intentional data quality issues included:

- duplicate rows
- missing values
- inconsistent categorical values
- orphaned foreign keys
- impossible date relationships
- currency inconsistencies
- support tickets without account ids
- renewal records referencing missing accounts

The dataset is fully reproducible using a fixed random seed.
"""

# Import necessary libraries

import pandas as pd
import numpy as np
from faker import Faker
from datetime import timedelta

# ////// accounts Dataset Generation //////

# ------ Set random seed for reproducibility ------

fake = Faker()

np.random.seed(42)


# ------ Define Business Model Parameters ------

# number of simulated customer accounts
N_ACCOUNTS = 500

# product tiers
TIERS = ["Starter", "Growth", "Business", "Enterprise"]

# regions where company operates
REGIONS = ["Europe", "North America", "APAC"]


# ------ Function to generate synthetic accounts dataset ------
# ------ Each account has: account_id, company name, tier, region, ARR, contract start/end dates, account manager ------


def generate_accounts():

    records = []

    for i in range(N_ACCOUNTS):

        start_date = fake.date_between(start_date="-2y", end_date="-1y")

        end_date = start_date + timedelta(days=365)

        tier = np.random.choice(TIERS)

        # ARR depends on tier
        if tier == "Starter":
            arr = np.random.randint(2000, 5000)

        elif tier == "Growth":
            arr = np.random.randint(6000, 12000)

        elif tier == "Business":
            arr = np.random.randint(15000, 30000)

        else:
            arr = np.random.randint(40000, 90000)

        record = {

            "account_id": i + 1,

            "company": fake.company(),

            "tier": tier,

            "region": np.random.choice(REGIONS),

            "arr": arr,

            "contract_start": start_date,

            "contract_end": end_date,

            "account_manager": fake.name()

        }

        records.append(record)

    df = pd.DataFrame(records)




# ------ Introduce Inconsistent Categorical Values ------
   
    df.loc[df.sample(10).index, "tier"] = "enterprise "
    df.loc[df.sample(10).index, "tier"] = "ENTERPRISE"



# ------ Introduce Missing Values ------

    df.loc[df.sample(15).index, "account_manager"] = np.nan



# ------ Introduce Duplicate Rows ------

    df = pd.concat([df, df.sample(5)], ignore_index=True)


    return df



# ================================================================================================



# ////// usage_events Dataset Generation //////

# ------ Product Features by Tier ------

FEATURES_BY_TIER = {

    "Starter": ["dashboard", "reports"],

    "Growth": ["dashboard", "reports", "automation"],

    "Business": ["dashboard", "reports", "automation", "integrations"],

    "Enterprise": ["dashboard", "reports", "automation", "integrations", "api"]
}


# ------ Function to generate synthetic usage events dataset ------
# ------ Each event has: event_id, account_id, week_start, tier, feature, usage ------

def generate_usage_events(accounts_df):

    records = []

    event_id = 1

    for _, row in accounts_df.iterrows():

        account_id = row["account_id"]

        tier = row["tier"].strip().capitalize()

        features = FEATURES_BY_TIER.get(tier, FEATURES_BY_TIER["Starter"])

        # simulate 52 weeks of usage
        for week in range(52):

            week_start = pd.Timestamp("2024-01-01") + pd.Timedelta(weeks=week)

            for feature in features:

                usage = np.random.poisson(lam=10)

                record = {

                    "event_id": event_id,

                    "account_id": account_id,

                    "week_start": week_start,

                    "tier": tier,

                    "feature": feature,

                    "usage_count": usage

                }

                records.append(record)

                event_id += 1

    df = pd.DataFrame(records)




# ----- Introduce Duplicate Rows -----

    df = pd.concat([df, df.sample(50)], ignore_index=True)



# ----- Introduce Orphaned Foreign Keys -----

    orphan_rows = df.sample(20).copy()

    orphan_rows["account_id"] = 99999

    df = pd.concat([df, orphan_rows], ignore_index=True)



# ------ Introduce Missing Values ------

    df.loc[df.sample(100).index, "usage_count"] = np.nan


    return df



# ================================================================================================



# ////// support_Tickets Dataset Generation //////

# ------ Support Ticket Categories ------

SUPPORT_CATEGORIES = [
    "bug",
    "billing",
    "feature_request",
    "integration",
    "performance"
]


# ------ Function to generate synthetic support tickets dataset ------
# ------ Each ticket has: ticket_id, account_id, created_at, category, resolution_hours, sentiment_score ------

def generate_support_tickets(accounts_df):

    records = []

    ticket_id = 1

    # simulate about 2000 support tickets
    for i in range(2000):

        account_id = np.random.choice(accounts_df["account_id"])

        created_at = fake.date_between(start_date="-1y", end_date="today")

        category = np.random.choice(SUPPORT_CATEGORIES)

        resolution_hours = np.random.randint(1, 72)

        sentiment = np.random.uniform(-1, 1)

        record = {

            "ticket_id": ticket_id,

            "account_id": account_id,

            "created_at": created_at,

            "category": category,

            "resolution_hours": resolution_hours,

            "sentiment_score": sentiment

        }

        records.append(record)

        ticket_id += 1

    df = pd.DataFrame(records)



# ------ Introduce Missing Account IDs (~12%) ------

    missing_index = df.sample(frac=0.12).index

    df.loc[missing_index, "account_id"] = np.nan



# ----- Introduce Duplicate Rows -----

    df = pd.concat([df, df.sample(30)], ignore_index=True)  



# ------ Introduce Inconsistent Categories ------

    df.loc[df.sample(10).index, "category"] = "Bug "
    df.loc[df.sample(10).index, "category"] = "BILLING"


    return df



# ================================================================================================



# ////// invoice Dataset Generation //////

# ------ Discount Codes and Payment Terms ------
DISCOUNT_CODES = [
    None,
    "PROMO10",
    "SUMMER20",
    "LOYALTY15"
]

PAYMENT_TERMS = [
    "Net 15",
    "Net 30",
    "Net 60"
]


# ------ Function to generate synthetic invoices dataset ------
# ------ Each invoice has: invoice_id, account_id, invoice_date, amount, discount_code, payment_terms ------

def generate_invoices(accounts_df):

    records = []

    invoice_id = 1

    for _, row in accounts_df.iterrows():

        account_id = row["account_id"]

        arr = row["arr"]

        # SaaS invoices usually monthly
        monthly_amount = arr / 12

        for month in range(12):

            invoice_date = pd.Timestamp("2024-01-01") + pd.DateOffset(months=month)

            due_date = invoice_date + pd.Timedelta(days=30)

            paid_date = due_date + pd.Timedelta(days=np.random.randint(-5,20))

            record = {

                "invoice_id": f"INV{invoice_id}",

                "account_id": account_id,

                "invoice_date": invoice_date,

                "due_date": due_date,

                "paid_date": paid_date,

                "amount": round(monthly_amount,2),

                "currency": np.random.choice(["EUR","USD"]),

                "discount_code": np.random.choice(DISCOUNT_CODES),

                "payment_terms": np.random.choice(PAYMENT_TERMS)

            }

            records.append(record)

            invoice_id += 1

    df = pd.DataFrame(records)



 # ------ Introduce Impossible Date Relationships (paid_date before invoice_date) ------

    bad_rows = df.sample(20).index

    df.loc[bad_rows, "paid_date"] = df.loc[bad_rows, "invoice_date"] - pd.Timedelta(days=3)   



# ----- Introduce Duplicate Rows -----

    df = pd.concat([df, df.sample(20)], ignore_index=True)


    return df



# ================================================================================================



# ////// renewals Dataset Generation //////

# ------ Function to generate synthetic renewals dataset ------
# ------ Each renewal has: renewal_id, account_id, renewal_date, previous_arr, new_arr, outcome ------

def generate_renewals(accounts_df):

    records = []

    renewal_id = 1

    for _, row in accounts_df.iterrows():

        account_id = row["account_id"]

        arr = row["arr"]

        renewal_date = pd.Timestamp("2025-01-01")

        outcome = np.random.choice(
            ["renewed", "churned", "downgraded", "expanded"],
            p=[0.65, 0.15, 0.10, 0.10]
        )

        new_arr = arr

        if outcome == "downgraded":
            new_arr = arr * np.random.uniform(0.7, 0.9)

        elif outcome == "expanded":
            new_arr = arr * np.random.uniform(1.1, 1.4)

        elif outcome == "churned":
            new_arr = 0

        record = {

            "renewal_id": renewal_id,

            "account_id": account_id,

            "renewal_date": renewal_date,

            "previous_arr": arr,

            "new_arr": round(new_arr,2),

            "outcome": outcome

        }

        records.append(record)

        renewal_id += 1

    df = pd.DataFrame(records)



# ----- Add fake accounts ------

    fake_accounts = pd.DataFrame({

    "renewal_id": range(10000,10010),

    "account_id": np.random.randint(10000,10100,10),

    "renewal_date": pd.Timestamp("2025-01-01"),

    "previous_arr": np.random.randint(5000,20000,10),

    "new_arr": np.random.randint(0,20000,10),

    "outcome": np.random.choice(["renewed","churned"],10)

    })

    df = pd.concat([df,fake_accounts],ignore_index=True)


    return df



# ================================================================================================



# ////// nps_survey Dataset Generation //////

# ------ Function to generate synthetic NPS survey responses dataset ------
# ------ Each response has: survey_id, account_id, score, survey_date ------

def generate_nps(accounts_df):

    responses = []

    survey_id = 1

    for _, row in accounts_df.iterrows():

        if np.random.rand() < 0.34:

            score = np.random.randint(0,11)

            responses.append({

                "survey_id": survey_id,

                "account_id": row["account_id"],

                "score": score,

                "survey_date": pd.Timestamp("2024-12-01")

            })

            survey_id += 1

    df = pd.DataFrame(responses)


    return df



# ================================================================================================



# ------ Main Execution Block to generate Datasets and Display Sample Output ------ 

if __name__ == "__main__":
    print("Starting data generation...")
    accounts = generate_accounts()
    usage_events = generate_usage_events(accounts)
    support_tickets = generate_support_tickets(accounts)
    invoices = generate_invoices(accounts)
    renewals = generate_renewals(accounts)
    nps = generate_nps(accounts)
    
    print("Accounts generated")
    print(accounts.head())

    print("Usage events generated")
    print(usage_events.head())

    print("Support tickets generated")
    print(support_tickets.head())
    
    print("Invoices generated") 
    print(invoices.head())

    print("Renewals generated")
    print(renewals.head())

    print("NPS survey responses generated")
    print(nps.head())


# ------ Save generated Datasets to CSV Files for use in Analysis and Modeling ------ 

accounts.to_csv("Data/Raw/accounts.csv", index=False)

usage_events.to_csv("Data/Raw/usage_events.csv", index=False)

support_tickets.to_csv("Data/Raw/support_tickets.csv", index=False)

invoices.to_csv("Data/Raw/invoices.csv", index=False)

renewals.to_csv("Data/Raw/renewals.csv", index=False)

nps.to_csv("Data/Raw/nps_survey.csv", index=False)