# Databricks notebook source
df_bronze = spark.table("workspace.default.transactions_data")

# COMMAND ----------

# Preview a small sample of the raw transactional data
# Used as a basic sanity check to understand column structure and values
display(df_bronze.limit(10))

# COMMAND ----------

# Inspect the inferred schema of the Bronze table
# This helps identify incorrect data types and nullable fields
df_bronze.printSchema()

# COMMAND ----------

# Count total number of records in the dataset
# Useful for validating ingestion completeness
df_bronze.count()

# COMMAND ----------

# Check uniqueness of the business key (transaction id)
# Differences between total count and distinct count indicate duplicates
df_bronze.select("id").distinct().count()

# COMMAND ----------

from pyspark.sql.functions import col

# Assess null values in critical columns
# Key fields should not contain nulls in Silver layer
display(
    df_bronze.selectExpr(
    "count(*) as total_rows",
    "sum(case when id is null then 1 else 0 end) as null_id",
    "sum(case when date is null then 1 else 0 end) as null_date",
    "sum(case when amount is null then 1 else 0 end) as null_amount"
    )
)

# COMMAND ----------

from pyspark.sql.functions import col, sum as _sum, count, when

display(
    df_bronze
        .groupBy("use_chip")
        .agg(
            count("*").alias("total_rows"),
            _sum(when(col("id").isNull(), 1).otherwise(0)).alias("null_id"),
            _sum(when(col("date").isNull(), 1).otherwise(0)).alias("null_date"),
            _sum(when(col("amount").isNull(), 1).otherwise(0)).alias("null_amount")
        )
)


# COMMAND ----------


# Explore distinct values of the amount field
# Amount is currently stored as string and contains currency symbols
display(df_bronze.select("amount").distinct().limit(20))

# COMMAND ----------

# Attempt a numeric comparison on the amount column
# Expected to fail due to non-numeric characters (currency symbol)
# This error is an important EDA insight for Silver layer design
df_bronze.filter(col("amount") <= 0).count()

# COMMAND ----------

# Analyze distribution of transaction types
# Used for later standardization in Silver layer
display(df_bronze.groupBy("use_chip").count())