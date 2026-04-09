# Architecture Overview

This project simulates an end-to-end enterprise Business Intelligence platform built on a modern lakehouse architecture using Databricks and Power BI.

The goal of the solution is to transform raw transactional data into business-ready insights that support analytical use cases such as revenue tracking, customer segmentation, and churn analysis.

---

# Data Flow Overview

The platform follows a layered architecture:

Source → Bronze → Silver → Gold → Analytics → Power BI

Each layer has a clearly defined responsibility and level of data refinement.

---

# Bronze Layer (Raw Data Ingestion)

The Bronze layer represents raw data ingestion into the platform.

- Data is ingested as-is from source systems
- No transformations or business logic are applied
- Schema is preserved as close as possible to the source
- Serves as a historical and auditable data layer

Example:
- Raw transaction data loaded into Databricks tables

Purpose:
- Traceability
- Reprocessing capability
- Data lineage foundation

---

# Silver Layer (Data Cleaning & Standardization)

The Silver layer is responsible for data quality and standardization.

Key transformations:
- Data type casting (e.g. amounts, dates)
- Handling null values and invalid records
- Data validation rules (DQ checks)
- Standardizing formats (ZIP codes, transaction types)

Additionally:
- Invalid records are separated into dedicated tables for monitoring and auditing
- Cleaned dataset is stored as `transactions_clean`

Purpose:
- Ensure consistent, reliable data
- Prepare data for downstream business logic
- Improve data trustworthiness

---

# Gold Layer (Business Data Model)

The Gold layer represents the business-ready data model using a star schema approach.

## Core tables:

### Fact table:
- `fact_transactions`
  - Contains transactional data at the lowest granularity
  - Includes surrogate keys to dimensions

### Dimension tables:
- `dim_client`
- `dim_merchant`
- `dim_date`

Key concepts implemented:
- Surrogate keys
- Slowly Changing Dimensions (SCD Type 2) for merchants
- Time dimension for analytical slicing

Purpose:
- Provide a scalable and flexible analytical model
- Enable efficient joins and aggregations
- Support BI tools with a clean semantic structure

---

# Analytics Layer (Serving Layer for BI)

This layer contains pre-aggregated and business-focused datasets optimized for reporting and dashboarding.

Instead of querying large fact tables directly, Power BI consumes these lightweight tables.

## Examples:

- `dashboard_revenue_trend`
  - Monthly revenue, transaction count, average transaction value

- `dashboard_rfm_segments`
  - Customer segmentation based on Recency, Frequency, Monetary metrics

- `dashboard_merchant_performance`
  - Top merchants by revenue and activity

- `dashboard_customer_activity`
  - Customer-level activity, churn indicators, and behavioral metrics

- `dashboard_churn_trend`
  - Monthly trend of churned customers

Additionally:
- Aggregation tables such as `agg_client_lifetime` support advanced analytics and ad-hoc exploration

Purpose:
- Improve performance of BI tools
- Simplify data consumption for analysts
- Provide reusable analytical datasets

---

# Data Processing Engine

The entire data transformation pipeline is executed in Databricks.

## Key capabilities used:

- PySpark for distributed data processing
- Delta Lake for storage and ACID transactions
- Incremental processing patterns
- Schema enforcement and evolution handling

Databricks acts as:
- Data processing engine
- Storage layer (Delta tables)
- Transformation orchestration environment

---

# BI Layer (Power BI)

Power BI is used as the consumption layer for business users.

## Connection:
- Direct connection to Databricks using Import mode

## Data model approach:
- Lightweight star schema ("star schema light")
- Focus on aggregated datasets rather than raw facts

## Capabilities demonstrated:
- KPI dashboards
- Time series analysis (revenue trends)
- Customer segmentation (RFM)
- Churn analysis
- Interactive filtering and drill-down

Purpose:
- Deliver insights to business users
- Enable self-service analytics
- Provide fast and responsive dashboards

---

# Key Design Decisions

## 1. Layered Architecture
Separates concerns between raw data, cleaned data, and business logic.

## 2. Pre-aggregations for BI
Improves performance and reduces complexity in Power BI.

## 3. Use of Date (not only keys)
Ensures compatibility with Power BI time intelligence functions.

## 4. SCD Type 2
Allows tracking historical changes (e.g. merchant attributes over time).

## 5. Reusable Analytical Datasets
Supports both dashboards and ad-hoc analysis.

---

# Summary

This project demonstrates how to design and implement a modern BI platform that:

- Processes large-scale transactional data
- Applies data quality and transformation logic
- Builds a scalable analytical model
- Delivers insights through Power BI

The architecture balances:
- Data engineering best practices
- BI performance optimization
- Business usability