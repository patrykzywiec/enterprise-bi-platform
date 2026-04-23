# Metrics Definition

This document defines the key customer and business metrics used in the project: **RFM (Recency, Frequency, Monetary)**, **Customer Churn**, and **Customer Lifetime Value (CLV)**. Each section includes the conceptual definition and example Spark/SQL code to calculate it.

---

## Recency-Frequency-Monetary (RFM) Segmentation

**Definition:** RFM analysis groups customers based on three dimensions【11†L265-L273】:
- **Recency:** How recently the customer made a purchase (e.g. days since last transaction).
- **Frequency:** How often the customer makes purchases (e.g. number of transactions).
- **Monetary:** How much the customer spends (e.g. total transaction value).

RFM scores help identify valuable customers (e.g. *high-frequency, high-monetary* customers) and potential lapsers (customers with low recency). It supports principles like the 80/20 rule (20% of customers often generate 80% of revenue).

**Calculation (Spark example):**

```python
from pyspark.sql.functions import col, max, count, sum, round, datediff, current_date

# Aggregate transactions by customer
rfm = (fact_transactions
    .groupBy("client_sk")
    .agg(
        max("date").alias("last_tx_date"),          # most recent purchase
        count("*").alias("frequency"),              # total transactions
        round(sum("amount"), 2).alias("monetary")   # total spend
    )
    .withColumn("recency_days", datediff(current_date(), col("last_tx_date")))
)
rfm.createOrReplaceTempView("client_rfm")
```

This yields columns: `client_sk`, `last_tx_date`, `frequency`, `monetary`, `recency_days`.  
You can then score or segment customers (e.g. assign quintile ranks 1–5 for each metric). For example:

```sql
SELECT
  client_sk,
  NTILE(5) OVER (ORDER BY recency_days) AS recency_rank,
  NTILE(5) OVER (ORDER BY frequency)    AS frequency_rank,
  NTILE(5) OVER (ORDER BY monetary)     AS monetary_rank
FROM client_rfm;
```

The combination of these ranks forms an RFM segment. For instance, a customer with `(R=5, F=5, M=5)` would be a “Top” customer. Segmentation rules (e.g. “Champions”, “At Risk”) can be based on these scores in the **dashboard_rfm_segments** table.

---

## Customer Churn

**Definition:** *Customer churn* (or attrition) refers to customers who stop doing business (stop purchasing) over a given period【14†L1616-L1620】. In other words, it measures the rate at which customers drop off.

- **Churn Rate (%):**  = (Number of churned customers in period) / (Total customers at start of period) × 100.

In this project, we define a customer as **churned** if their last transaction was more than 90 days ago (90-day inactivity threshold). This is a common rule-of-thumb in retail/financial contexts.

**Calculation (Spark example):**

```python
from pyspark.sql.functions import col, max, date_sub, current_date

churn_threshold = 90

# Find each customer's last transaction date
customer_last_tx = (fact_transactions
    .groupBy("client_sk")
    .agg(max("date").alias("last_tx_date"))
)

# Flag churn: last_tx_date older than 90 days
customer_churn = customer_last_tx.withColumn(
    "is_churned",
    col("last_tx_date") < date_sub(current_date(), churn_threshold)
)
customer_churn.createOrReplaceTempView("customer_churn")
```

This adds a boolean `is_churned`. For example, to get total churned customers by month:

```sql
SELECT
  trunc(date_add(last_tx_date, 90), 'month') AS churn_month,
  SUM(CASE WHEN is_churned THEN 1 ELSE 0 END) AS churned_customers
FROM customer_churn
GROUP BY trunc(date_add(last_tx_date, 90), 'month')
ORDER BY churn_month;
```

This yields a **churn trend** by month (we store this in `dashboard_churn_trend`).  

Churn analysis helps the business identify retention issues. According to Salesforce, customer churn is *“the percentage of customers who end their relationship with your business during a specific time period.”*【14†L1616-L1620】.

---

## Customer Lifetime Value (CLV)

**Definition:** Customer Lifetime Value is the total net profit or worth that a customer contributes over their entire relationship with the company【16†L27-L30】. It encompasses all purchases (and any costs) associated with that customer.

In a simple historical sense, CLV can be calculated as the sum of past transactions for each customer. (More complex/predictive CLV models exist but are beyond this scope).

**Calculation (Spark example):**

```python
from pyspark.sql.functions import sum, count, round, min, max

# Aggregate lifetime metrics by customer
clv = (fact_transactions
    .groupBy("client_sk")
    .agg(
        round(sum("amount"), 2).alias("lifetime_value"),  # total spend
        count("*").alias("total_transactions"),          # total purchases
        min("date").alias("first_tx_date"),
        max("date").alias("last_tx_date")
    )
)
clv.createOrReplaceTempView("client_lifetime")
```

The `lifetime_value` column is the historical CLV for each customer. We store these aggregates in the table `agg_client_lifetime`. This can inform marketing ROI: high-CLV customers may receive loyalty incentives, etc.

Alternatively, a basic formula (for average CLV) is:  
```
CLV = (Average Purchase Value) × (Purchase Frequency) × (Average Customer Lifespan)
``` 
This matches business definitions【16†L27-L30】. In our dataset, we derive it directly from transactions data.
