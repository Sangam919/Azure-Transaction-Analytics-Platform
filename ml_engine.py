"""
ml_engine.py — AI/ML Models
Implements four ML capabilities that run on top of the analytics data:
  1. Revenue Forecasting     — Linear Regression + trend decomposition
  2. Customer Segmentation   — K-Means RFM clustering
  3. Anomaly Detection       — Isolation Forest on transaction price/quantity
  4. Product Recommendations — Content-based similarity (cosine similarity)
"""

import numpy as np
import pandas as pd
import streamlit as st
from datetime import datetime

from sklearn.cluster import KMeans
from sklearn.ensemble import IsolationForest
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.metrics.pairwise import cosine_similarity


# ─── 1. Revenue Forecasting ──────────────────────────────────────────────────
@st.cache_data(show_spinner=False)
def forecast_revenue(_monthly_df: pd.DataFrame, periods: int = 6) -> pd.DataFrame:
    """
    Fit a linear trend on monthly revenue and forecast future periods.
    Returns a DataFrame with historical + forecast rows and confidence bands.
    """
    df = _monthly_df.copy().sort_values("year_month")
    df["t"] = np.arange(len(df))

    X = df[["t"]].values
    y = df["revenue"].values

    model = LinearRegression()
    model.fit(X, y)
    df["predicted"] = model.predict(X)

    # Residual std for confidence interval
    residuals = y - df["predicted"].values
    std_resid  = residuals.std()

    df["lower_ci"] = df["predicted"] - 1.96 * std_resid
    df["upper_ci"] = df["predicted"] + 1.96 * std_resid
    df["type"]     = "Historical"

    # Forecast
    last_t   = df["t"].max()
    periods_ym = pd.period_range(
        start=pd.Period(df["year_month"].iloc[-1], "M") + 1, periods=periods, freq="M"
    )
    future_t = np.arange(last_t + 1, last_t + 1 + periods)
    future_pred = model.predict(future_t.reshape(-1, 1))

    future_df = pd.DataFrame({
        "year_month": [str(p) for p in periods_ym],
        "revenue":    [None] * periods,
        "t":          future_t,
        "predicted":  future_pred,
        "lower_ci":   future_pred - 1.96 * std_resid,
        "upper_ci":   future_pred + 1.96 * std_resid,
        "type":       ["Forecast"] * periods,
    })

    result = pd.concat([df, future_df], ignore_index=True)
    return result


# ─── 2. Customer Segmentation (RFM + K-Means) ───────────────────────────────
@st.cache_data(show_spinner=False)
def segment_customers(_cust_df: pd.DataFrame, _joined_df: pd.DataFrame, n_clusters: int = 4) -> pd.DataFrame:
    """
    Build RFM features and apply K-Means clustering.
    Returns customer DataFrame with 'segment' and 'segment_label' columns.
    """
    df = _cust_df.copy()

    # Recency = days since last purchase
    max_date = pd.to_datetime(_joined_df["transaction_date"]).max()
    df["recency"]   = (max_date - pd.to_datetime(df["last_purchase"])).dt.days
    df["frequency"] = df["total_transactions"]
    df["monetary"]  = df["total_revenue"]

    features = df[["recency", "frequency", "monetary"]].fillna(0)
    scaler   = StandardScaler()
    X        = scaler.fit_transform(features)

    km = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    df["segment"] = km.fit_predict(X)

    # Label segments by mean monetary value (highest = Champions)
    seg_means = df.groupby("segment")["monetary"].mean().sort_values(ascending=False)
    label_map = {int(k): lbl for k, lbl in zip(
        seg_means.index,
        ["🏆 Champions", "🌟 Loyal Customers", "⚡ Potential Loyalists", "😴 At-Risk"]
    )}
    df["segment_label"] = df["segment"].map(label_map)

    return df


# ─── 3. Anomaly Detection (Isolation Forest) ─────────────────────────────────
@st.cache_data(show_spinner=False)
def detect_anomalies(_tx_df: pd.DataFrame, contamination: float = 0.03) -> pd.DataFrame:
    """
    Flag anomalous transactions using Isolation Forest.
    Returns transaction DataFrame with 'anomaly_score' and 'is_anomaly' columns.
    """
    df = _tx_df.copy()
    features = df[["quantity", "price"]].fillna(0)

    scaler = StandardScaler()
    X      = scaler.fit_transform(features)

    iso = IsolationForest(contamination=contamination, random_state=42, n_estimators=100)
    df["anomaly_label"] = iso.fit_predict(X)           # -1 = anomaly, 1 = normal
    df["anomaly_score"] = iso.score_samples(X)          # more negative = more anomalous
    df["is_anomaly"]    = df["anomaly_label"] == -1

    return df


# ─── 4. Product Recommendations (Content-Based) ──────────────────────────────
@st.cache_data(show_spinner=False)
def get_recommendations(_prod_df: pd.DataFrame, _tx_df: pd.DataFrame, top_n: int = 5) -> dict:
    """
    Build a content-based similarity matrix on product features.
    Returns a dict mapping product_id → list of recommended product_ids.
    """
    df = _prod_df.copy()

    # Encode category as one-hot, normalise price
    cat_dummies = pd.get_dummies(df["category"], prefix="cat")
    price_norm  = MinMaxScaler().fit_transform(df[["unit_price"]])
    feat_matrix = np.hstack([cat_dummies.values, price_norm])

    sim_matrix = cosine_similarity(feat_matrix)

    recs = {}
    for idx, pid in enumerate(df["product_id"]):
        sim_scores = list(enumerate(sim_matrix[idx]))
        sim_scores.sort(key=lambda x: x[1], reverse=True)
        top_ids = [
            df.iloc[i]["product_id"]
            for i, score in sim_scores
            if df.iloc[i]["product_id"] != pid
        ][:top_n]
        recs[pid] = top_ids

    return recs


# ─── Elbow Method helper ──────────────────────────────────────────────────────
def get_elbow_data(_cust_df: pd.DataFrame) -> pd.DataFrame:
    """Compute inertia for k=2..8 for the elbow plot."""
    df = _cust_df.copy()
    features = df[["total_transactions", "total_revenue", "avg_order_value"]].fillna(0)
    scaler   = StandardScaler()
    X        = scaler.fit_transform(features)

    ks       = range(2, 9)
    inertias = []
    for k in ks:
        km = KMeans(n_clusters=k, random_state=42, n_init=10)
        km.fit(X)
        inertias.append(km.inertia_)

    return pd.DataFrame({"k": list(ks), "inertia": inertias})
