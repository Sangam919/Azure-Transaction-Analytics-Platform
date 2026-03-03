from pyspark.sql import SparkSession
from config import setup_adls_connection, verify_files_exist
from data_loader import load_transaction_data
from data_cleaner import clean_data, add_quality_flags
from analytics import enrich_channels, generate_analytics
from delta_utils import create_delta_table, optimize_table, create_data_quality_table

def execute_pipeline():
    """Execute the data engineering pipeline."""
    print("🚀 Executing Data Engineering Pipeline")
    
    # Initialize Spark session
    spark = SparkSession.builder \
        .appName("TransactionAnalysis") \
        .config("spark.jars.packages", "io.delta:delta-core_2.12:2.4.0") \
        .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
        .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") \
        .getOrCreate()
    
    # Step 1: Set up ADLS connection
    account, container = setup_adls_connection()
    if not account:
        return
    
    # Step 2: Verify files
    if not verify_files_exist(account, container):
        return
    
    # Step 3: Load data
    tx_df, pr_df = load_transaction_data(account, container)
    if tx_df is None or pr_df is None:
        return
    
    # Step 4: Clean and enrich data
    tx_df = clean_data(tx_df, "transactions")
    pr_df = clean_data(pr_df, "products")
    tx_df = add_quality_flags(tx_df)
    pr_df = add_quality_flags(pr_df)
    tx_df = enrich_channels(tx_df)
    
    # Step 5: Generate analytics
    joined, cust_df, prod_df, cat_df, camp_df = generate_analytics(tx_df, pr_df)
    
    # Step 6: Save to Delta tables
    create_delta_table(joined, "transactions_insights")
    create_delta_table(cust_df, "customer_analytics")
    create_delta_table(prod_df, "product_analytics")
    create_delta_table(cat_df, "category_analytics")
    create_delta_table(camp_df, "campaign_analytics")
    create_data_quality_table(tx_df)
    
    # Step 7: Optimize all Delta tables
    tables = ["transactions_insights", "customer_analytics", "product_analytics", "category_analytics", "campaign_analytics"]
    for table in tables:
        optimize_table(f"analytics_db.{table}")
    
    print("🎉 Pipeline execution complete.")
    spark.stop()

if __name__ == "__main__":
    execute_pipeline()
