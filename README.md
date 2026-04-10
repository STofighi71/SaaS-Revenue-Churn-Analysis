# SaaS Revenue & Churn Analysis

## Project Overview

This project analyzes customer renewal behavior and revenue retention
for a fictional B2B SaaS company. The goal is to understand **customer
churn, revenue expansion, contraction, and retention patterns** using a
full data analytics workflow.

The project demonstrates the following skills:

-   Data generation and preparation with Python
-   Exploratory Data Analysis (EDA)
-   SaaS revenue metric calculations
-   Data modeling (Star Schema)
-   Business KPI analysis
-   Interactive dashboard development in Power BI
-   Documentation and portfolio-ready repository structure

------------------------------------------------------------------------

# Business Objectives

The analysis focuses on answering several business questions commonly
asked in SaaS companies:

1.  How much revenue is retained from existing customers?
2.  What percentage of revenue expansion comes from upsells?
3.  Which customers or tiers experience the highest churn?
4.  Is customer product usage related to renewal probability?
5.  Do support tickets correlate with churn risk?
6.  Which segments generate the highest revenue growth?

------------------------------------------------------------------------

# Key SaaS Metrics Used

## ARR (Annual Recurring Revenue)

Total yearly subscription revenue from customers.

## Net ARR

Revenue change from the same customer base.

## Expansion ARR

Additional revenue gained from existing customers upgrading or expanding
usage.

## Contraction ARR

Revenue lost when customers downgrade their subscription.

## Churn ARR

Revenue lost from customers who cancel.

## NRR (Net Revenue Retention)

Formula:

NRR = (Starting ARR + Expansion ARR - Contraction ARR - Churn ARR) /
Starting ARR

NRR measures how much revenue is retained from existing customers.

------------------------------------------------------------------------

# Project Workflow

## STEP 1 --- Data Generation (Python)

Synthetic SaaS datasets were generated to simulate realistic company
data.

Datasets created:

-   customers
-   subscriptions
-   renewals
-   product usage
-   support tickets
-   account metadata

Python libraries used:

-   pandas
-   numpy

Output files were exported as CSV files for further analysis.

------------------------------------------------------------------------

## STEP 2 --- Data Preparation

Data cleaning tasks included:

-   Checking missing values
-   Verifying ARR calculations
-   Removing duplicates
-   Standardizing column names
-   Ensuring correct data types

Prepared datasets were stored in a structured format for analytics.

------------------------------------------------------------------------

## STEP 3 --- Data Modeling

A **Star Schema** was implemented for analysis.

Fact Tables:

-   renewals
-   usage
-   support_tickets

Dimension Tables:

-   customers
-   tiers
-   regions
-   time

Relationships were created in Power BI Model View.

This structure improves:

-   query performance
-   analytical flexibility
-   dashboard clarity

------------------------------------------------------------------------

# STEP 4 --- Advanced Exploratory Data Analysis (Python)

EDA was performed to explore patterns across all datasets.

## Univariate Analysis

Distribution analysis of:

-   ARR
-   product usage
-   support ticket counts
-   customer tiers

## Bivariate Analysis

Relationships explored between:

-   product usage vs renewal outcome
-   support tickets vs churn
-   tier vs ARR

## Correlation Analysis

Examined correlation between:

-   support ticket volume
-   churn likelihood

------------------------------------------------------------------------

# STEP 5 --- Power BI Dashboard

An interactive dashboard was created to visualize key SaaS KPIs.

## Dashboard Pages

### Page 1 --- Executive Overview

Key KPIs:

-   Total ARR
-   Net Revenue Retention
-   Expansion ARR
-   Contraction ARR
-   Churn ARR

Visualizations:

-   ARR distribution by tier
-   ARR by region
-   ARR growth summary

Purpose:

Provide executives with a quick view of revenue health.

------------------------------------------------------------------------

### Page 2 --- Revenue Breakdown

Visualizations:

-   ARR by product tier
-   ARR by region
-   Customer count by segment

Purpose:

Identify high-value segments and revenue sources.

------------------------------------------------------------------------

### Page 3 --- Revenue Movements

Visualizations:

ARR Movement Waterfall Chart

Components:

-   Starting ARR
-   Expansion ARR
-   Contraction ARR
-   Churn ARR
-   Ending ARR

Purpose:

Explain how revenue changes over time.

Cards:

-   Expansion ARR
-   Contraction ARR
-   Churn ARR

------------------------------------------------------------------------

# Power BI Measures

Examples of measures created:

### Expansion ARR

SUM of additional ARR gained from renewals.

### Contraction ARR

SUM of ARR lost from downgrades.

### Churn ARR

SUM of ARR lost from cancellations.

### Net ARR

Expansion ARR - Contraction ARR - Churn ARR

### NRR

NRR = DIVIDE( SUM(renewals\[new_arr\]), SUM(renewals\[previous_arr\]) )

------------------------------------------------------------------------

# Key Insights

Example findings from the analysis:

-   Customers with low product usage are more likely to churn.
-   Higher support ticket volume may indicate product friction.
-   Enterprise tier generates the majority of ARR.
-   Expansion revenue significantly offsets contraction losses.


------------------------------------------------------------------------

# Tools Used

Python

Libraries:

-   pandas
-   numpy
-   matplotlib

BI Tool:

Power BI

Version control:

Git + GitHub

------------------------------------------------------------------------

# How to Run the Project

1.  Clone the repository

2.  Install dependencies

pip install pandas numpy matplotlib

3.  Run data generation script

python scripts/data_generation.py

4.  Perform EDA analysis

python scripts/eda_analysis.py

5.  Open Power BI dashboard

------------------------------------------------------------------------

# Portfolio Value

This project demonstrates:

-   SaaS KPI analytics
-   Revenue retention analysis
-   Customer churn analysis
-   Python data analysis
-   Power BI dashboard development
-   End-to-end analytics workflow

------------------------------------------------------------------------

