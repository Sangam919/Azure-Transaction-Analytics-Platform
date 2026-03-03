from pyspark.sql.functions import col, count, sum, countDistinct, mean, stddev

def enrich_channels(df):
    """Enrich transaction data with channel information."""
    return df.withColumn("channel", 
                        when(col("transaction_id").rlike("^WEB"), "web")
                       .when(col("transaction_id").rlike("^MOB"), "mobile")
                       .otherwise("in-store"))

def generate_analytics(transactions, products):
    """Generate analytics from transaction and product data."""
    joined = transactions.join(products, "product_id", "left").cache()

    customer_df = joined.groupBy("customer_id").agg(
        count("transaction_id").alias("transactions"),
        sum(col("quantity") * col("price")).alias("revenue")
    ).withColumn("avg_order_value", col("revenue") / col("transactions"))

    product_df = joined.groupBy("product_id", "description").agg(
        sum("quantity").alias("sold"),
        sum(col("quantity") * col("price")).alias("revenue")
    )

    category_df = joined.groupBy("category").agg(
        sum("quantity").alias("units_sold"),
        sum(col("quantity") * col("price")).alias("category_revenue")
    )

    campaign_df = joined.groupBy("campaign_id").agg(
        count("*").alias("transactions"),
        sum(col("quantity") * col("price")).alias("campaign_revenue"),
        countDistinct("customer_id").alias("unique_customers")
    )

    # Outlier detection on revenue
    revenue_stats = customer_df.select(mean("revenue").alias("mean"), stddev("revenue").alias("std")).collect()[0]
    mean_val, std_val = revenue_stats["mean"], revenue_stats["std"]
    customer_df = customer_df.withColumn(
        "is_outlier", (col("revenue") > (mean_val + 3 * std_val)) | (col("revenue") < (mean_val - 3 * std_val))
    )

    return joined, customer_df, product_df, category_df, campaign_df
