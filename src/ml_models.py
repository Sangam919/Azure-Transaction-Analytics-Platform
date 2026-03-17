"""
src/ml_models.py — PySpark-compatible ML Models
Provides AI/ML capabilities that run within the Azure Databricks notebook.
Mirrors the logic in the top-level ml_engine.py but adapted for PySpark DataFrames.
"""

from pyspark.sql import DataFrame, SparkSession
from pyspark.sql.functions import col, mean, stddev, datediff, max as spark_max, lit
from pyspark.ml.feature import VectorAssembler, StandardScaler
from pyspark.ml.clustering import KMeans
from pyspark.ml.evaluation import ClusteringEvaluator


# ─── 1. Customer Segmentation (K-Means RFM) ──────────────────────────────────
def compute_rfm(transactions: DataFrame, reference_date=None) -> DataFrame:
    """
    Compute RFM (Recency, Frequency, Monetary) features from transaction data.
    Args:
        transactions: Cleaned transactions DataFrame
        reference_date: Reference date for recency calc (defaults to max date in data)
    Returns:
        DataFrame with customer_id, recency_days, frequency, monetary columns
    """
    spark = SparkSession.getActiveSession()

    if reference_date is None:
        reference_date = transactions.agg(spark_max("transaction_date")).collect()[0][0]

    rfm = transactions.groupBy("customer_id").agg(
        datediff(lit(reference_date), spark_max("transaction_date")).alias("recency_days"),
        col("transaction_id").alias("frequency"),
        (col("quantity") * col("price")).alias("monetary"),
    )
    # Re-aggregate properly
    from pyspark.sql.functions import count, sum as spark_sum
    rfm = transactions.groupBy("customer_id").agg(
        datediff(lit(reference_date), spark_max("transaction_date")).alias("recency_days"),
        count("transaction_id").alias("frequency"),
        spark_sum(col("quantity") * col("price")).alias("monetary"),
    )
    return rfm


def segment_customers_spark(rfm_df: DataFrame, k: int = 4) -> DataFrame:
    """
    Apply K-Means clustering to RFM data using PySpark MLlib.
    Args:
        rfm_df: DataFrame with recency_days, frequency, monetary columns
        k: Number of clusters
    Returns:
        DataFrame with additional 'segment' column
    """
    assembler = VectorAssembler(
        inputCols=["recency_days", "frequency", "monetary"],
        outputCol="features_raw"
    )
    scaler = StandardScaler(inputCol="features_raw", outputCol="features", withStd=True, withMean=True)

    from pyspark.ml import Pipeline
    pipeline = Pipeline(stages=[assembler, scaler])
    model    = pipeline.fit(rfm_df)
    scaled   = model.transform(rfm_df)

    kmeans  = KMeans(k=k, seed=42, featuresCol="features", predictionCol="segment")
    km_model = kmeans.fit(scaled)

    # Silhouette score
    evaluator = ClusteringEvaluator(featuresCol="features")
    silhouette = evaluator.evaluate(km_model.transform(scaled))
    print(f"   ✅ K-Means trained | k={k} | Silhouette Score: {silhouette:.4f}")

    result = km_model.transform(scaled).select("customer_id", "recency_days", "frequency", "monetary", "segment")
    return result


# ─── 2. Anomaly Detection (Statistical — 3-Sigma) ────────────────────────────
def detect_transaction_anomalies(df: DataFrame) -> DataFrame:
    """
    Apply 3-sigma rule anomaly detection on price and quantity.
    More production-appropriate for Databricks than sklearn's Isolation Forest.
    Returns DataFrame with is_anomaly column.
    """
    stats = df.select(
        mean("price").alias("price_mean"),   stddev("price").alias("price_std"),
        mean("quantity").alias("qty_mean"),  stddev("quantity").alias("qty_std"),
    ).collect()[0]

    pm, ps = stats["price_mean"],    stats["price_std"]
    qm, qs = stats["qty_mean"],      stats["qty_std"]

    from pyspark.sql.functions import when
    result = df.withColumn(
        "is_anomaly",
        (
            (col("price") > pm + 3 * ps) | (col("price") < pm - 3 * ps) |
            (col("quantity") > qm + 3 * qs) | (col("quantity") < qm - 3 * qs)
        )
    )
    anomaly_count = result.filter(col("is_anomaly")).count()
    print(f"   ⚠️  Anomaly Detection: {anomaly_count:,} transactions flagged")
    return result


# ─── 3. Revenue Trend (per-period aggregation) ───────────────────────────────
def compute_monthly_revenue(df: DataFrame) -> DataFrame:
    """
    Aggregate revenue by month for trend analysis.
    Returns: DataFrame with year_month, revenue, transaction_count columns.
    """
    from pyspark.sql.functions import date_format, sum as spark_sum, count
    result = df.withColumn("year_month", date_format("transaction_date", "yyyy-MM")) \
               .groupBy("year_month") \
               .agg(
                   spark_sum(col("quantity") * col("price")).alias("revenue"),
                   count("transaction_id").alias("transaction_count")
               ) \
               .orderBy("year_month")
    return result
