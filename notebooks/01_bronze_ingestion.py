# Databricks notebook source
# 01_bronze_ingestion
# Purpose:
# Ingest raw transactional data into Bronze layer
# This notebook defines the source contract and ingestion boundary

# NOTE:
# In current version, data is already available as a managed table.
# This notebook exists to represent the ingestion layer in the pipeline.

df_bronze = spark.table("workspace.default.transactions_data")
