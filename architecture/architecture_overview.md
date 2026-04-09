# Architecture Overview

This project simulates an end-to-end enterprise BI platform built using a lakehouse architecture.

## Layers

### Bronze (Raw Data)
Raw transactional data ingested into Databricks.

### Silver (Cleaned Data)
Data is cleaned, standardized, and enriched.

### Gold (Business Layer)
Business-ready tables:
- fact_transactions
- dim_date
- dim_merchant
- client_rfm_metrics

### Analytics Layer
Pre-aggregated datasets optimized for BI:
- dashboard_revenue_trend
- dashboard_rfm_segments
- dashboard_merchant_performance
- dashboard_customer_activity

## BI Layer
Power BI connects to Databricks using Import mode and consumes analytics datasets.

## Key Concepts
- Star schema
- RFM segmentation
- Churn analysis
- Customer Lifetime Value (CLV)