# Databricks notebook source
# 03_silver_transform
# Purpose:
# Transform Bronze transactions into clean Silver layer
# Apply data quality rules and typing

# NOTE:
# Transformation logic will be implemented in a dedicated commit
# once data quality rules are finalized via EDA

df_bronze = spark.table("workspace.default.transactions_data")