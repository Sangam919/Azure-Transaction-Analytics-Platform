import pandas as pd
import matplotlib.pyplot as plt
from pyspark.sql import DataFrame

def plot_top_customers(customer_df: DataFrame, top_n: int = 5):
    """Plot a bar chart of top customers by average order value."""
    try:
        # Convert to Pandas for plotting
        pdf = customer_df.select("customer_id", "avg_order_value")\
                        .orderBy("avg_order_value", ascending=False)\
                        .limit(top_n).toPandas()
        
        plt.figure(figsize=(10, 6))
        plt.bar(pdf["customer_id"], pdf["avg_order_value"], color="#1f77b4")
        plt.title(f"Top {top_n} Customers by Average Order Value")
        plt.xlabel("Customer ID")
        plt.ylabel("Average Order Value ($)")
        plt.xticks(rotation=45)
        plt.tight_layout()
        display(plt.gcf())  # Display in Databricks
        plt.close()
    except Exception as e:
        print(f"❌ Error plotting top customers: {e}")

def plot_top_products(product_df: DataFrame, top_n: int = 5):
    """Plot a bar chart of top products by sales volume."""
    try:
        pdf = product_df.select("description", "sold")\
                       .orderBy("sold", ascending=False)\
                       .limit(top_n).toPandas()
        
        plt.figure(figsize=(10, 6))
        plt.bar(pdf["description"], pdf["sold"], color="#ff7f0e")
        plt.title(f"Top {top_n} Products by Units Sold")
        plt.xlabel("Product")
        plt.ylabel("Units Sold")
        plt.xticks(rotation=45)
        plt.tight_layout()
        display(plt.gcf())
        plt.close()
    except Exception as e:
        print(f"❌ Error plotting top products: {e}")

def plot_campaign_revenue(campaign_df: DataFrame):
    """Plot a pie chart of campaign revenue distribution."""
    try:
        pdf = campaign_df.select("campaign_id", "campaign_revenue").toPandas()
        
        plt.figure(figsize=(8, 8))
        plt.pie(pdf["campaign_revenue"], labels=pdf["campaign_id"], autopct="%1.1f%%", colors=["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd"])
        plt.title("Campaign Revenue Distribution")
        plt.tight_layout()
        display(plt.gcf())
        plt.close()
    except Exception as e:
        print(f"❌ Error plotting campaign revenue: {e}")
