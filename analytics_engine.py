"""
analytics_engine.py — Pandas-based Analytics Engine
Mirrors the PySpark ETL pipeline logic from the original src/ modules
but runs locally using pandas for the Streamlit dashboard.
"""

import numpy as np
import pandas as pd
import streamlit as st


# ─── Data Cleaning (mirrors data_cleaner.py) ─────────────────────────────────
def clean_transactions(df: pd.DataFrame) -> dict:
    """Remove nulls / duplicates, detect outliers. Returns cleaned df + stats."""
    before = len(df)
    df = df.dropna(how="all").drop_duplicates()
    after = len(df)

    # 3-sigma outlier detection on quantity and price
    for col in ["quantity", "price"]:
        mean_v = df[col].mean()
        std_v  = df[col].std()
        df[f"{col}_is_outlier"] = (
            (df[col] > mean_v + 3 * std_v) | (df[col] < mean_v - 3 * std_v)
        )

    # Quality score
    df["data_quality_score"] = df["transaction_id"].notna().astype(float)

    # Channel enrichment from transaction_id prefix
    def _channel(txn_id):
        if str(txn_id).startswith("WEB"): return "Web"
        if str(txn_id).startswith("MOB"): return "Mobile"
        return "In-Store"

    df["channel"] = df["transaction_id"].apply(_channel)

    stats = {
        "before":         before,
        "after":          after,
        "removed":        before - after,
        "null_counts":    df.isnull().sum().to_dict(),
        "outliers_qty":   int(df["quantity_is_outlier"].sum()),
        "outliers_price": int(df["price_is_outlier"].sum()),
        "quality_pct":    round(df["data_quality_score"].mean() * 100, 2),
    }
    return df, stats


# ─── Analytics Engine (mirrors analytics.py) ─────────────────────────────────
@st.cache_data(show_spinner=False)
def run_analytics(_tx_df: pd.DataFrame, _pr_df: pd.DataFrame):
    """Join transactions + products and compute all KPIs. Results cached."""

    # Clean first
    tx, quality_stats = clean_transactions(_tx_df.copy())

    # Join
    joined = tx.merge(_pr_df, on="product_id", how="left")
    joined["revenue"] = joined["quantity"] * joined["price"]

    # ── Customer KPIs ─────────────────────────────────────────────────────
    cust = (
        joined.groupby("customer_id")
        .agg(
            total_transactions=("transaction_id", "count"),
            total_revenue=("revenue", "sum"),
            first_purchase=("transaction_date", "min"),
            last_purchase=("transaction_date", "max"),
        )
        .reset_index()
    )
    cust["avg_order_value"] = cust["total_revenue"] / cust["total_transactions"]
    m, s = cust["total_revenue"].mean(), cust["total_revenue"].std()
    cust["is_revenue_outlier"] = (cust["total_revenue"] > m + 3 * s) | (cust["total_revenue"] < m - 3 * s)

    # ── Product KPIs ──────────────────────────────────────────────────────
    prod = (
        joined.groupby(["product_id", "description", "category"])
        .agg(units_sold=("quantity", "sum"), product_revenue=("revenue", "sum"))
        .reset_index()
    )

    # ── Category KPIs ─────────────────────────────────────────────────────
    cat = (
        joined.groupby("category")
        .agg(units_sold=("quantity", "sum"), category_revenue=("revenue", "sum"))
        .reset_index()
        .sort_values("category_revenue", ascending=False)
    )

    # ── Campaign KPIs ─────────────────────────────────────────────────────
    camp = (
        joined[joined["campaign_id"].notna()]
        .groupby("campaign_id")
        .agg(
            total_transactions=("transaction_id", "count"),
            campaign_revenue=("revenue", "sum"),
            unique_customers=("customer_id", "nunique"),
        )
        .reset_index()
    )
    camp["avg_revenue_per_customer"] = camp["campaign_revenue"] / camp["unique_customers"]

    # ── Channel KPIs ──────────────────────────────────────────────────────
    channel = (
        joined.groupby("channel")
        .agg(transactions=("transaction_id", "count"), revenue=("revenue", "sum"))
        .reset_index()
    )

    # ── Monthly Revenue ───────────────────────────────────────────────────
    joined["year_month"] = pd.to_datetime(joined["transaction_date"]).dt.to_period("M")
    monthly = (
        joined.groupby("year_month")
        .agg(revenue=("revenue", "sum"), transactions=("transaction_id", "count"))
        .reset_index()
    )
    monthly["year_month"] = monthly["year_month"].astype(str)

    # ── Summary KPIs ──────────────────────────────────────────────────────
    summary = {
        "total_revenue":       round(joined["revenue"].sum(), 2),
        "total_transactions":  len(joined),
        "total_customers":     joined["customer_id"].nunique(),
        "total_products":      joined["product_id"].nunique(),
        "avg_order_value":     round(joined["revenue"].mean(), 2),
        "top_channel":         joined.groupby("channel")["revenue"].sum().idxmax(),
        "top_category":        joined.groupby("category")["revenue"].sum().idxmax(),
        "outlier_count":       int(tx["price_is_outlier"].sum()),
        "data_quality_pct":    quality_stats["quality_pct"],
    }

    return {
        "joined":        joined,
        "customers":     cust,
        "products":      prod,
        "categories":    cat,
        "campaigns":     camp,
        "channels":      channel,
        "monthly":       monthly,
        "quality_stats": quality_stats,
        "summary":       summary,
        "clean_tx":      tx,
    }
