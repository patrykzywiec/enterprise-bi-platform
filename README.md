# Enterprise BI Platform

## Overview

This project simulates an end-to-end enterprise Business Intelligence platform built on a modern lakehouse architecture using Databricks and Power BI.

It demonstrates how raw transactional data can be transformed into a structured, scalable, and analytics-ready solution using layered data processing (Bronze → Silver → Gold → Analytics).

The platform is designed as a realistic portfolio project that combines data engineering, data modeling, and business analytics.

---

## Executive Summary

Many organizations collect large volumes of transactional data but struggle to transform it into actionable insights.

This project addresses that problem by building a complete BI platform that:

- cleans and validates raw data
- structures it into a business-friendly model
- prepares optimized datasets for reporting
- enables advanced analytics such as RFM segmentation, churn detection, and customer lifetime value

The result is a system that supports both operational reporting and strategic decision-making.

---

## What this project demonstrates

- Data ingestion and raw data storage (Bronze)
- Data cleaning and validation (Silver)
- Dimensional modeling (Gold)
- Pre-aggregated analytics datasets
- Customer analytics (RFM, churn, CLV)
- Power BI-ready data modeling
- End-to-end data pipeline design

---

## Architecture at a glance

Source Data
   → Bronze (raw)
   → Silver (cleaned)
   → Gold (dimensional model)
   → Analytics (aggregated datasets)
   → Power BI

## Technology stack

- Databricks (Apache Spark)
- Delta Lake
- PySpark / Spark SQL
- Power BI
- GitHub

Core datasets
- Gold layer
- gold.fact_transactions
gold.dim_date
gold.dim_client
gold.dim_merchant
Analytics layer
analytics.dashboard_revenue_trend
analytics.dashboard_churn_trend
analytics.dashboard_rfm_segments
analytics.dashboard_merchant_performance
analytics.dashboard_customer_activity
analytics.agg_client_lifetime
analytics.agg_merchant_daily
Documentation
Business case → docs/business_case.md
Data flow → architecture/data_flow.md
Data model → models/data_model.md
Metrics definition → docs/metrics_definition.md
Power BI design approach

Power BI is designed to consume the Analytics layer first, because:

datasets are smaller and faster
logic is already prepared
dashboards are easier to build

The Gold layer remains available for deeper analysis.

---

## Business Context

A financial services company needs a data platform to analyze customer transactions and support decision-making. Key requirements include:
- **Revenue Monitoring:** Track total revenue and trends over time.
- **Customer Segmentation:** Score customers by Recency, Frequency, Monetary (RFM) value to target marketing.
- **Churn Analysis:** Identify customers who have lapsed and measure churn rates.
- **Merchant Performance:** Rank top merchants by transaction volume and value.
- **Secure Self-Service:** Provide business users with a single source of truth and self-service capabilities in Power BI.

Without this platform, analysts would spend hours writing ad-hoc queries on raw data. The solution streamlines reporting and allows stakeholders (Executives, Finance, Marketing) to quickly access insights on KPIs and customer behavior.

---

## Architecture & Data Flow

**High-Level Pipeline:**

```
Raw CSV Files 
    → Spark (Databricks CE) 
    → Delta Lake (Bronze / Silver / Gold Tables) 
    → Analytics Layer (aggregated tables) 
    → Power BI semantic model
```

1. **Bronze (Raw Data Ingestion):** Load raw data into Delta tables (`bronze.transactions_raw`). The schema matches source CSVs; we capture full history and audit metadata.
2. **Silver (Cleansed Data):** Apply data quality and cleaning (e.g. filter nulls, correct formats). Store results in `silver.transactions_clean`. This layer “conforms” the data (e.g. standardized date formats)【9†L237-L243】【9†L247-L254】.
3. **Gold (Business Tables):** Build dimensional model tables:
    - **Fact table (`gold.fact_transactions`):** Grain = one transaction. Includes foreign keys to dimensions and metrics (amount).
    - **Dim tables (`gold.dim_date`, `gold.dim_client`, `gold.dim_merchant`):** Provide descriptive attributes for analysis. E.g. `dim_date` contains date attributes (year, month name, etc.), `dim_client` has customer info, etc.
    - Data in Gold is denormalized for speed (Kimball-style star schema)【21†L231-L239】.
4. **Analytics Layer:** Create aggregated tables optimized for BI queries. Examples:
    - `dashboard_revenue_trend`: Monthly revenue and transaction counts (with a `month_date` column).
    - `dashboard_rfm_segments`: Customer RFM scores and segment labels.
    - `dashboard_merchant_performance`: Top merchants by revenue.
    - `dashboard_customer_activity`: Customer-level metrics (recency, churn flag, etc.).
    - Additional tables like `agg_client_lifetime` (customer lifetime value) and `agg_merchant_daily` (daily merchant aggregates) support advanced analysis.

These tables minimize the need for complex joins in Power BI. See **data_flow.md** for details and code snippets.

---

## Technology Stack

| Layer             | Technology                  | Rationale                                                  |
| ----------------- | --------------------------- | ---------------------------------------------------------- |
| Processing Engine | Apache Spark (Databricks)   | Scalable distributed processing; browser-based workspace   |
| Transformations   | Spark SQL                   | SQL-centric ETL fits data warehouse paradigms              |
| Storage Format    | Delta Lake                  | ACID transactions, schema enforcement, time travel【9†L237-L243】 |
| Orchestration     | Databricks Notebooks/Jobs   | Collaborative notebooks; schedule via Databricks Workflows |
| BI Tools          | Power BI (Import mode)      | Rich visualizations; caches data in memory for speed       |

---

## Analytics Tables Overview

| Table                        | Purpose                             | Date Column for BI |
| ---------------------------- | ----------------------------------- | ------------------ |
| `dashboard_revenue_trend`    | Monthly revenue & transactions trend | **Yes** (`month_date`) – enables continuous time axis (needed for Power BI time intelligence) |
| `dashboard_rfm_segments`     | Customer RFM segmentation           | **No** (snapshot of segments)             |
| `dashboard_merchant_performance` | Merchant KPIs (ranking)       | **No** (static ranking)                  |
| `dashboard_customer_activity`| Customer-level metrics (incl. churn) | **No** (per-customer snapshot)          |
| `agg_client_lifetime`        | Lifetime metrics per customer       | **No** (per-customer aggregate)          |
| `agg_merchant_daily`         | Daily revenue per merchant          | **Yes** (`date`) – daily time series      |

Tables used for trend analysis (like revenue and churn) include date fields so that Power BI can apply time intelligence functions and continuous axes【9†L235-L243】【14†L1616-L1620】. Others are snapshots or summary tables where an extra date key isn’t needed.

---

## Setup & Usage

1. **Databricks Environment:** This project was developed on Databricks Community Edition. 
    - Ensure a cluster is running.
    - Upload the raw transaction CSV files to DBFS or a mounted location as expected by the ingestion notebook.
2. **Run Notebooks:** Execute the Python/Spark notebooks in order:
    - `01_ingestion.py` (load raw data into Bronze tables)
    - `02_silver_transformations.py` (clean/standardize data into Silver)
    - `03_gold_dimensions.py` (create dimension tables)
    - `04_gold_facts.py` (populate fact tables)
    - `08_rfm_churn.py` (compute RFM scores, churn flags)
    - `09_dashboard_datasets.py` (build aggregated dashboard tables)
3. **Power BI Connection:** 
    - In Power BI Desktop, choose **Get Data → Azure → Azure Databricks**.
    - Enter the **Server Hostname** and **HTTP Path** from Databricks (found under SQL Warehouses → Connection Details).  
       Example: `Server hostname: adb-1234567890123456.7.azuredatabricks.net`  
       `HTTP Path: /sql/1.0/warehouses/abcdef12-3456-7890-abcd-ef1234567890`  
    - Use **Personal Access Token** for authentication (generate one in your Databricks User Settings).
    - Use **Import** mode for best performance.
4. **Browse the Model:** The model is a “star schema light” with pre-aggregated tables. Power BI will import the tables (`dashboard_*`, `agg_*`, and dimensions). You can then build or view the provided reports.
5. **Connectors:** No private endpoints or network configuration is needed for Databricks CE. (For production, ensure network security as appropriate.)

---

## File Structure

```
enterprise-bi-platform/
├── README.md              # (this file)
├── docs/
│   ├── metrics_definition.md
│   ├── data_flow.md
│   ├── business_case.md
├── models/
│   └── data_model.md
├── notebooks/
│   ├── 01_ingestion.py
│   ├── 02_silver_transformations.py
│   ├── 03_gold_dimensions.py
│   ├── 04_gold_facts.py
│   ├── 08_rfm_churn.py
│   └── 09_dashboard_datasets.py
├── powerbi/
│   ├── dashboard.pbix
│   └── screenshots/
└── data/                  # (optional sample data)
```

Each document (in **docs/** or **models/**) corresponds to a part of the project:
- **metrics_definition.md:** Defines RFM, churn, and CLV (placed under `docs/`).
- **data_flow.md:** Explains the ETL layers and workflow (in `docs/`).
- **business_case.md:** Describes the business use case (in `docs/`).
- **data_model.md:** Describes the star schema (in `models/`).
- Updated **README.md** ties everything together for an outsider.

For example, `docs/metrics_definition.md` contains the metric definitions used in this project (RFM, churn, CLV) with Spark examples. `models/data_model.md` contains the ER diagram of the tables. The **architecture design decisions** (e.g. date vs integer keys) and code snippets are explained in these docs.

For detailed technical instructions and schema, see the individual documents.