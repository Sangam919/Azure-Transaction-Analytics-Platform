"""
data_generator.py — Synthetic Transaction Data Generator
Generates realistic multi-channel retail transaction data for demo purposes.
Mirrors the ADLS Gen2 data structure described in the notebook.
"""

import numpy as np
import pandas as pd
import streamlit as st
from datetime import datetime, timedelta

# ─── Constants ───────────────────────────────────────────────────────────────
CATEGORIES     = ["Electronics", "Clothing", "Home & Kitchen", "Sports", "Books", "Beauty", "Food & Grocery"]
CAMPAIGNS      = ["CAMP_001", "CAMP_002", "CAMP_003", "CAMP_004", "CAMP_005", None, None, None]  # None = no campaign
CHANNEL_PREFIX = {"WEB": 0.40, "MOB": 0.35, "STR": 0.25}   # Web 40%, Mobile 35%, In-store 25%

# ─── Product Catalog ─────────────────────────────────────────────────────────
def _make_products(n=100, seed=42) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    products = []
    pid = 1
    for category in CATEGORIES:
        count = n // len(CATEGORIES)
        for _ in range(count):
            price_ranges = {
                "Electronics":    (50, 1500),
                "Clothing":       (15, 200),
                "Home & Kitchen":  (10, 300),
                "Sports":         (20, 500),
                "Books":          (5,  60),
                "Beauty":         (8,  150),
                "Food & Grocery": (2,  50),
            }
            lo, hi = price_ranges[category]
            unit_price = round(float(rng.uniform(lo, hi)), 2)
            products.append({
                "product_id":  f"PROD_{pid:04d}",
                "description": f"{category} Product {pid:04d}",
                "category":    category,
                "unit_price":  unit_price,
            })
            pid += 1
    return pd.DataFrame(products)


# ─── Transactions ─────────────────────────────────────────────────────────────
def _make_transactions(products: pd.DataFrame, n=5000, seed=42) -> pd.DataFrame:
    rng   = np.random.default_rng(seed)
    start = datetime(2024, 4, 1)
    end   = datetime(2025, 3, 31)
    days  = (end - start).days

    product_ids = products["product_id"].tolist()
    prices      = dict(zip(products["product_id"], products["unit_price"]))

    rows = []
    channels = list(CHANNEL_PREFIX.keys())
    weights  = list(CHANNEL_PREFIX.values())

    for i in range(1, n + 1):
        channel = rng.choice(channels, p=weights)
        txn_id  = f"{channel}_{i:06d}"
        cust_id = f"CUST_{rng.integers(1, 501):04d}"
        prod_id = rng.choice(product_ids)

        # Seasonal quantity boost: Q4 (Oct-Dec) buys more
        txn_date = start + timedelta(days=int(rng.integers(0, days)))
        qty_boost = 1.5 if txn_date.month in [10, 11, 12] else 1.0
        quantity  = max(1, int(rng.integers(1, 6) * qty_boost))

        # Small % of price anomalies (fraud-like outliers)
        price = prices[prod_id]
        if rng.random() < 0.02:         # 2% anomalously high
            price = price * rng.uniform(8, 15)
        elif rng.random() < 0.01:       # 1% near-zero (data quality)
            price = round(float(rng.uniform(0.01, 0.10)), 2)

        campaign_id = rng.choice(CAMPAIGNS)

        rows.append({
            "transaction_id":   txn_id,
            "customer_id":      cust_id,
            "product_id":       prod_id,
            "quantity":         quantity,
            "price":            round(float(price), 2),
            "transaction_date": txn_date,
            "campaign_id":      campaign_id,
        })

    df = pd.DataFrame(rows)
    # Introduce ~1% deliberate nulls for data quality demo
    null_mask = rng.random(len(df)) < 0.01
    df.loc[null_mask, "campaign_id"] = None
    dup_mask = rng.choice(df.index, size=25, replace=False)
    df = pd.concat([df, df.loc[dup_mask]], ignore_index=True)
    return df


# ─── Public cache-wrapped loader ─────────────────────────────────────────────
@st.cache_data(show_spinner=False)
def load_data():
    """Return (transactions_df, products_df) — cached across Streamlit reruns."""
    products     = _make_products(n=98)         # 98 → 14 per category × 7
    transactions = _make_transactions(products, n=5000)
    return transactions, products
