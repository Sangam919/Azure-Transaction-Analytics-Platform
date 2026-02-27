from pyspark.sql.functions import count, when, col, current_timestamp, hash, mean, stddev

def detect_outliers(df, column):
    """Detect outliers in a numerical column using mean ± 3*stddev."""
    stats = df.select(mean(column).alias("mean"), stddev(column).alias("std")).collect()[0]
    mean_val, std_val = stats["mean"], stats["std"]
    return df.withColumn(f"{column}_is_outlier",
                        (col(column) > (mean_val + 3 * std_val)) | (col(column) < (mean_val - 3 * std_val))) 

def clean_data(df, name):
    """Clean DataFrame by removing nulls and duplicates."""
    try:
        print(f"🧹 Cleaning {name} data")
        df = df.dropna(how="all").dropDuplicates()
        df.select([count(when(col(c).isNull(), c)).alias(c) for c in df.columns]).show()
        if name == "transactions":
            df = detect_outliers(df, "quantity")
            df = detect_outliers(df, "price")
        return df
    except Exception as e:
        print(f"❌ Error cleaning {name}: {e}")
        return df

def add_quality_flags(df):
    """Add data quality flags and metadata."""
    return df.withColumn("data_quality_score", when(col("transaction_id").isNull(), 0.0).otherwise(1.0))\
            .withColumn("processed_at", current_timestamp())\
            .withColumn("record_hash", hash(*[col(c) for c in df.columns]))
