# SaaS Revenue & Churn Analysis

## Project Overview

This project simulates a full end-to-end analytics workflow for a B2B SaaS company selling subscription licenses across four product tiers and three global regions.

The objective of the analysis is to identify the drivers behind declining renewal rates and rising support costs and provide actionable insights for executive leadership before a board meeting.

The entire project was built from scratch, including synthetic data generation, automated data cleaning pipelines, analytical modeling, churn prediction, and an executive dashboard.

---

# Project Structure

```
saas-revenue-churn-analysis

Data/
    Raw/
    Cleaned/

Scripts/
    Data_Generation.py
    Cleaning_Pipeline.py

Notebooks/
    01_Data_Cleaning.ipynb
    Analysis.ipynb

SQL/
    queries.sql

Power-BI-Dashboard/
    dashboard.pbix

Outputs/
    Figures/
    Tables/

churn_risk_register.xlsx
assumptions_log.md
requirements.txt
README.md
```

---

# Data Generation

Since no real data was provided, all datasets were programmatically generated using Python.

The script creates six interconnected datasets:

• accounts
• usage_events
• support_tickets
• invoices
• renewals
• nps_survey

Real-world data quality issues were intentionally embedded, including:

* Duplicate records
* Missing values with different patterns
* Inconsistent categorical values
* Orphaned foreign keys
* Impossible date relationships
* Currency inconsistencies

This ensures that the project realistically reflects common challenges in production analytics environments.

---

# Data Cleaning Pipeline

A fully automated Python pipeline audits and cleans all datasets.

The pipeline performs:

* Data quality auditing
* Duplicate detection and removal
* Missing value handling
* Categorical normalization
* Foreign key validation
* Currency normalization (USD → EUR)
* Date validation

Clean datasets are exported to:

```
Data/Cleaned/
```

---

# Data Modeling

The cleaned data is modeled using a **star schema** in SQLite to support analytical queries.

Key SQL analyses include:

* Rolling 12-month ARR
* Month-over-month churn rate
* Cohort retention analysis
* Days Sales Outstanding (DSO)
* Support-driven downgrade analysis

---

# Exploratory Data Analysis

The analysis notebook includes:

* Univariate and bivariate analysis
* Correlation analysis
* Usage segmentation
* NPS analysis with non-response bias discussion

More than 10 publication-quality visualizations are included with clear business interpretation.

---

# KPI Engineering

Key SaaS metrics were calculated, including:

* ARR / MRR
* Net Revenue Retention
* Gross Revenue Retention
* Churn Rate
* Average Contract Value
* Expansion Revenue
* LTV/CAC proxy
* Support Ticket Rate
* Days Sales Outstanding
* NPS by segment

---

# Churn Prediction Model

A machine learning model was developed to identify accounts most likely to churn.

Steps included:

* Feature engineering from multiple datasets
* Training multiple models
* Evaluation using ROC-AUC and precision-recall
* Feature importance analysis

The final output is a ranked list of the **top 20 accounts most at risk of churn in the next 90 days.**

---

# Dashboard

An interactive dashboard was built in Power BI including:

• Executive KPI overview
• Churn risk monitoring
• Revenue health analysis
• Cohort retention heatmap
• Support-renewal correlation

---

# Key Business Questions Addressed

The project answers critical leadership questions such as:

* Which product tier has the highest churn?
* Is there a usage threshold predicting churn?
* Do high-support accounts renew less often?
* Which region has the worst payment behavior?
* Can NPS reliably predict renewal outcomes?

---

# How to Run the Project

1. Install dependencies

```
pip install -r requirements.txt
```

2. Generate data

```
python Scripts/Data_Generation.py
```

3. Run cleaning pipeline

```
python Scripts/Cleaning_Pipeline.py
```

4. Run analysis notebook

```
jupyter notebook Notebooks/Analysis.ipynb
```

---

# Author

Data Analytics Portfolio Project
End-to-end SaaS Revenue & Churn Analysis.
