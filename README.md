# Enterprise BI Platform

## Overview

This repository presents an **end-to-end enterprise Business Intelligence platform** designed and implemented as a realistic case study. The goal of the project is to demonstrate senior-level BI skills: data modeling, SQL-based transformations, Spark usage, and delivery of a semantic layer for reporting in Power BI.

The solution follows modern **lakehouse / ELT principles** and is intentionally designed to resemble a real-world corporate BI environment rather than a tutorial-style project.

---

## Business Context

A financial services company needs to analyze customer transactions to:

* monitor revenue and operational KPIs
* support management reporting
* enable secure access to data for different business roles

Source data arrives as raw transactional files and must be transformed into a structured analytical model optimized for BI consumption.

---

## High-Level Architecture

**Data Flow:**

```
Raw CSV files
   → Spark (Databricks Community Edition)
   → Delta Lake (Bronze / Silver / Gold)
   → Power BI semantic model
```

**Key design assumptions:**

* ELT approach (transformations performed after loading)
* SQL-first transformations using Spark SQL
* Clear separation of raw, cleaned, and business-ready data

---

## Technology Stack

| Layer                | Technology                   | Reasoning                                                                     |
| -------------------- | ---------------------------- | ----------------------------------------------------------------------------- |
| Processing Engine    | Apache Spark (Databricks CE) | Industry standard for scalable data processing; browser-based, no local setup |
| Transformations      | Spark SQL                    | SQL-first approach aligned with BI and analytics workloads                    |
| Storage Format       | Delta Lake                   | ACID transactions, schema enforcement, time travel                            |
| Orchestration / Glue | PySpark                      | Lightweight control logic and data loading                                    |
| Semantic Layer       | Power BI Desktop             | Enterprise BI reporting and data modeling                                     |
| Version Control      | GitHub                       | Documentation, task tracking, and delivery transparency                       |

---

## Data Layers

### 🥉 Bronze (Raw)

* Raw CSV files loaded without business logic
* Minimal schema handling
* Purpose: traceability and auditability

### 🥈 Silver (Cleaned)

* Data type casting
* Basic data quality rules
* Removal of invalid or duplicate records

### 🥇 Gold (Business)

* Fact and dimension tables
* Business logic applied
* Optimized for analytical queries and BI tools

---

## Project Structure

```
enterprise-bi-platform/
├── README.md
├── architecture/
│   └── architecture.png
├── data/
│   └── sample_csv/
├── spark/
│   ├── bronze.sql
│   ├── silver.sql
│   └── gold.sql
├── pyspark/
│   └── load_raw.py
├── powerbi/
│   ├── model.md
│   ├── rls.md
│   └── screenshots/
```
## Source Data

This repository contains a **small representative sample** of the source data.
The full dataset is stored externally and used only for data processing in Spark.

---

## Project Plan & Tasks

### Phase 1 – Data Ingestion (Bronze)

* [ ] Upload raw CSV files to Databricks
* [ ] Load raw data using PySpark
* [ ] Store data in Delta Lake Bronze layer

### Phase 2 – Data Cleaning (Silver)

* [ ] Cast columns to proper data types
* [ ] Apply basic data quality rules
* [ ] Create cleaned Delta tables

### Phase 3 – Business Layer (Gold)

* [ ] Build fact and dimension tables
* [ ] Apply business aggregations
* [ ] Prepare data for BI consumption

### Phase 4 – Reporting

* [ ] Power BI data model
* [ ] Measures and KPIs
* [ ] Row-Level Security (RLS)

### Phase 5 – Documentation

* [ ] Architecture diagram
* [ ] Design decisions documented
* [ ] Repository cleanup

---

## Key Design Decisions

* **Spark SQL over heavy PySpark logic** to maximize readability and maintainability
* **Delta Lake** chosen to ensure reliability and consistency of analytical data
* **Power BI semantic layer** separated from transformation logic
* **Cloud-agnostic concepts** applicable to Azure, AWS, and GCP environments

---

## How This Would Look in Production

In a production environment this solution could be deployed using:

* Azure Data Lake Gen2 instead of local storage
* Azure Databricks or Synapse Spark
* Power BI Service with automated refresh and workspace-level security

---

## What This Project Demonstrates

* End-to-end BI platform design
* SQL-based data transformations at scale
* Understanding of lakehouse architecture
* Senior-level approach to data modeling and delivery

---

## Author

**Patryk Zywiec**
