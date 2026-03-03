from pyspark.sql import SparkSession

def setup_adls_connection():
    """Set up ADLS Gen2 connection."""
    try:
        storage_account = "mydatalake2004"
        container = "transaction-data"
        access_key = dbutils.secrets.get(scope="azure-storage", key="storage-access-key")
        spark = SparkSession.getActiveSession()
        spark.conf.set(f"fs.azure.account.key.{storage_account}.dfs.core.windows.net", access_key)
        print("✅ ADLS connection successful.")
        return storage_account, container
    except Exception as e:
        print(f"❌ Failed to connect to ADLS: {e}")
        return None, None

def verify_files_exist(account, container):
    """Verify files exist in ADLS Gen2."""
    try:
        base_path = f"abfss://{container}@{account}.dfs.core.windows.net/"
        files = dbutils.fs.ls(base_path)
        for file in files:
            print(f"📄 {file.name} - {file.size} bytes")
        return [f.name for f in files]
    except Exception as e:
        print(f"❌ Could not list files: {e}")
        return []
