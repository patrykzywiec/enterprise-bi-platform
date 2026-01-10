# Databricks notebook source
# Databricks notebook source
# 03_silver_transform
# Purpose:
# Transform Bronze transactions into clean, typed Silver layer
# Apply data quality rules and separate invalid records

from pyspark.sql.functions import (
    col,
    regexp_replace,
    when,
    trim
)
from pyspark.sql.types import DecimalType

# COMMAND ----------

# Load Bronze table (raw ingested data)
df_bronze = spark.table("workspace.default.transactions_data")

# COMMAND ----------

# Remove currency symbol and cast amount to decimal
df_transformed = (
    df_bronze
    .withColumn(
        "amount_clean",
        regexp_replace(col("amount"), "\\$", "").cast(DecimalType(12, 2))
    )
    .withColumn(
        "zip_clean",
        col("zip").cast("string")
    )
    .withColumn(
        "use_chip_clean",
        trim(col("use_chip"))
    )
)


# COMMAND ----------

# Define validity conditions for Silver layer
valid_condition = (
    col("id").isNotNull() &
    col("date").isNotNull() &
    col("amount_clean").isNotNull() &
    (col("amount_clean") > 0)
)

# COMMAND ----------

# Records that pass data quality rules
df_valid = df_transformed.filter(valid_condition)

# COMMAND ----------

# Rejected records with reason
df_rejected = (
    df_transformed.withColumn(
        "reject_reason",
        when(col("id").isNull(), "NULL_ID")
        .when(col("date").isNull(), "NULL_DATE")
        .when(col("amount_clean").isNull(), "INVALID_AMOUNT_FORMAT")
        .when(col("amount_clean") <= 0, "NON_POSITIVE_AMOUNT")
        .otherwise("UNKNOWN")
    )
    .filter(~valid_condition)
)

# COMMAND ----------

# Select and rename columns for Silver clean table
df_silver_clean = df_valid.select(
    col("id"),
    col("date"),
    col("client_id"),
    col("card_id"),
    col("amount_clean").alias("amount"),
    col("use_chip_clean").alias("use_chip"),
    col("merchant_id"),
    col("merchant_city"),
    col("merchant_state"),
    col("zip_clean").alias("zip"),
    col("mcc"),
    col("errors")
)

# COMMAND ----------

# Write clean Silver data
df_silver_clean.write.mode("overwrite").saveAsTable(
    "silver.transactions_clean"
)

# COMMAND ----------

# DBTITLE 1,Untitled
# Write rejected records with schema update allowed
df_rejected.write \
    .mode("overwrite") \
    .option("overwriteSchema", "true") \
    .saveAsTable("silver.transactions_rejected")

# COMMAND ----------

# Log record counts for monitoring
print("Bronze records:", df_bronze.count())
print("Silver clean records:", df_silver_clean.count())
print("Rejected records:", df_rejected.count())