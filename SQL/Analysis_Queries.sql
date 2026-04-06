-- SaaS Revenue Analytics Project
-- STEP 3: Analytical SQL Queries
-- Database: SQLite
-- Schema: Star Schema

-- Tables used in this analysis:
-- accounts_dim
-- renewals_fact
-- invoices_fact
-- support_dim

-- This file contains analytical queries requested in the project:
-- 1. Rolling 12-month ARR per account (window function)
-- 2. Month-over-month churn rate by product tier
-- 3. Cohort analysis by contract start quarter
-- 4. Days Sales Outstanding (DSO) per region
-- 5. Accounts that downgraded within 60 days of a support ticket spike
-- 6. Accounts that upsold more than once (multi-level CTE)

---------------------------------------------------
-- List all tables in the database
---------------------------------------------------

SELECT name 
FROM sqlite_master 
WHERE type='table'



---------------------------------------------------
-- 1 Rolling 12 Month ARR per Account
---------------------------------------------------



SELECT
    account_id,
    renewal_date,
    new_arr,
    SUM(new_arr) OVER (
        PARTITION BY account_id
        ORDER BY renewal_date
        ROWS BETWEEN 11 PRECEDING AND CURRENT ROW
    ) AS rolling_12m_arr
FROM renewals_fact
ORDER BY account_id, renewal_date;



---------------------------------------------------
-- 2 Month over Month Churn Rate by Product Tier
---------------------------------------------------

SELECT
    a.tier,
    strftime('%Y-%m', r.renewal_date) AS month,
    COUNT(*) AS total_accounts,
    SUM(CASE WHEN r.outcome = 'churned' THEN 1 ELSE 0 END) AS churned_accounts,
    ROUND(
        1.0 * SUM(CASE WHEN r.outcome = 'churned' THEN 1 ELSE 0 END) / COUNT(*),
        4
    ) AS churn_rate
FROM renewals_fact r
JOIN accounts_dim a
ON r.account_id = a.account_id
GROUP BY a.tier, month
ORDER BY month;



---------------------------------------------------
-- 3 Cohort Analysis
---------------------------------------------------

SELECT
    strftime('%Y', contract_start) || '-Q' ||
    ((CAST(strftime('%m', contract_start) AS INTEGER)-1)/3 +1) AS cohort_quarter,
    COUNT(account_id) AS accounts
FROM accounts_dim
GROUP BY cohort_quarter
ORDER BY cohort_quarter;



---------------------------------------------------
-- 4 Days Sales Outstanding (DSO)
---------------------------------------------------

SELECT
    a.region,
    AVG(julianday(i.paid_date) - julianday(i.invoice_date)) AS avg_dso
FROM invoices_fact i
JOIN accounts_dim a
ON i.account_id = a.account_id
WHERE i.paid_date IS NOT NULL
GROUP BY a.region;



---------------------------------------------------
-- 5 Self Join - Downgrade After Support Spike
---------------------------------------------------

WITH ticket_spikes AS (
    SELECT
        account_id,
        DATE(created_at) AS ticket_date,
        COUNT(*) AS tickets
    FROM support_dim
    GROUP BY account_id, ticket_date
    HAVING COUNT(*) >= 3
)

SELECT
    r1.account_id,
    r1.renewal_date,
    r1.new_arr AS current_arr,
    r2.new_arr AS previous_arr,
    t.ticket_date
FROM renewals_fact r1
JOIN renewals_fact r2
ON r1.account_id = r2.account_id
AND r2.renewal_date = (
    SELECT MAX(renewal_date)
    FROM renewals_fact
    WHERE account_id = r1.account_id
    AND renewal_date < r1.renewal_date
)
JOIN ticket_spikes t
ON r1.account_id = t.account_id
WHERE r1.new_arr < r2.new_arr
AND ABS(julianday(r1.renewal_date) - julianday(t.ticket_date)) <= 60;



---------------------------------------------------
-- 6 Multi Level CTE - Accounts Upsold More Than Once
---------------------------------------------------

WITH arr_history AS (
    SELECT
        account_id,
        renewal_date,
        new_arr,
        LAG(new_arr) OVER (
            PARTITION BY account_id
            ORDER BY renewal_date
        ) AS previous_arr
    FROM renewals_fact
),

upsells AS (
    SELECT
        account_id,
        renewal_date
    FROM arr_history
    WHERE new_arr > previous_arr
)

SELECT
    account_id,
    COUNT(*) AS upsell_count
FROM upsells
GROUP BY account_id
HAVING COUNT(*) > 1;