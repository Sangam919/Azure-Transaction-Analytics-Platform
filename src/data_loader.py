from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DoubleType, TimestampType
transaction_schema = StructType([
    StructField("transaction_id", StringType(), False),
    StructField("customer_id", StringType(), True),
    StructField("product_id", StringType(), False),
    StructField("quantity", IntegerType(), True),
    StructField("price", DoubleType(), True),
    StructField("transaction_date", TimestampType(), True),
    StructField("campaign_id", StringType(), True)
])

product_schema = StructType([
    StructField("product_id", StringType(), False),
    StructField("description", StringType(), True),
    StructField("category", StringType(), True),
    StructField("unit_price", DoubleType(), True)
])

def load_csv(file_path, file_name, schema=None):
    """Load CSV data from ADLS Gen2."""
    try:
        print(f"📥 Loading {file_name}...")
        spark = SparkSession.getActiveSession()
        if schema:
            df = spark.read.schema(schema).option("header", "true").csv(file_path)
        else:
            df = spark.read.option("header", "true").option("inferSchema", "true").csv(file_path)
        print(f"✅ Loaded {df.count()} rows with {len(df.columns)} columns from {file_name}")
        df.show(5)
        return df
    except Exception as e:
        print(f"❌ Error reading {file_name}: {e}")
        return None

def load_transaction_data(account, container):
    """Load transaction and product data."""
    path = f"abfss://{container}@{account}.dfs.core.windows.net/"
    tx_df = load_csv(path + "transactions/*.csv", "transactions", transaction_schema)
    pr_df = load_csv(path + "products.csv", "products", product_schema)
    return tx_df, pr_df
