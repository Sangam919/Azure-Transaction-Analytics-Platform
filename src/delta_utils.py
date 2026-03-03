from pyspark.sql import SparkSession
from pyspark.sql.functions import count, when, col, lit
from delta.tables import DeltaTable

def create_delta_table(df, table_name, db="analytics_db"):
    """Create a Delta table in the specified database."""
    spark = SparkSession.getActiveSession()
    spark.sql(f"CREATE DATABASE IF NOT EXISTS {db}")
    df.write.format("delta").mode("overwrite").saveAsTable(f"{db}.{table_name}")
    print(f"✅ Created table: {db}.{table_name}")

def optimize_table(table):
    """Optimize and vacuum Delta table."""
    spark = SparkSession.getActiveSession()
    spark.sql(f"OPTIMIZE {table} ZORDER BY (customer_id)")
    spark.sql(f"VACUUM {table} RETAIN 168 HOURS")

def create_data_quality_table(df):
    """Create a Delta table for data quality summary."""
    null_summary = df.select([count(when(col(c).isNull(), c)).alias(c) for c in df.columns])
    null_summary = null_summary.withColumn("total_rows", lit(df.count()))
    create_delta_table(null_summary, "data_quality_summary")
