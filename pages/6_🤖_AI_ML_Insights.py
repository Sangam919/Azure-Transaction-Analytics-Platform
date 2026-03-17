"""
pages/6_🤖_AI_ML_Insights.py — AI/ML Insights Dashboard
Revenue forecasting, customer segmentation, anomaly detection, product recommendations.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from data_generator import load_data
from analytics_engine import run_analytics
from ml_engine import (
    forecast_revenue, segment_customers, detect_anomalies,
    get_recommendations, get_elbow_data
)

st.set_page_config(page_title="AI/ML Insights · Azure Analytics", page_icon="🤖", layout="wide")

with st.spinner("🤖 Running AI/ML models..."):
    tx_df, pr_df = load_data()
    res       = run_analytics(tx_df, pr_df)
    forecast  = forecast_revenue(res["monthly"])
    segments  = segment_customers(res["customers"], res["joined"])
    anomalies = detect_anomalies(res["clean_tx"])
    recs      = get_recommendations(pr_df, tx_df)
    elbow     = get_elbow_data(res["customers"])

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<h1 style="font-size:1.6rem;font-weight:800;
  background:linear-gradient(90deg,#7c3aed,#f59e0b);
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;">
  🤖 AI / ML Insights
</h1>
<p style="color:#64748b;font-size:0.85rem;margin-bottom:1.2rem;">
  Revenue Forecasting · Customer Segmentation · Anomaly Detection · Product Recommendations
</p>
""", unsafe_allow_html=True)

# ── Model Info Badges ─────────────────────────────────────────────────────────
badges = [
    ("📈 Linear Regression",  "Revenue Forecasting",  "#00d4ff"),
    ("🔬 K-Means (RFM)",      "Customer Segmentation","#7c3aed"),
    ("🚨 Isolation Forest",   "Anomaly Detection",    "#ef4444"),
    ("📦 Cosine Similarity",  "Recommendations",      "#f59e0b"),
]
cols = st.columns(4)
for col, (model, task, color) in zip(cols, badges):
    with col:
        st.markdown(f"""
        <div class="kpi-card" style="--accent:{color}; text-align:center; padding:0.9rem;">
          <div style="font-size:0.82rem;font-weight:700;color:{color};">{model}</div>
          <div style="font-size:0.72rem;color:#64748b;margin-top:0.3rem;">{task}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Tabs ──────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs([
    "📈 Revenue Forecast",
    "🔬 Customer Segmentation",
    "🚨 Anomaly Detection",
    "📦 Recommendations",
])

# ── Tab 1: Revenue Forecast ───────────────────────────────────────────────────
with tab1:
    st.markdown("#### 6-Month Revenue Forecast with Confidence Interval")
    st.caption("Model: Linear Regression on monthly aggregates | 95% Confidence Interval shown")

    col_slider, _ = st.columns([2, 5])
    with col_slider:
        periods = st.slider("Forecast Months", 3, 12, 6)

    forecast = forecast_revenue(res["monthly"], periods=periods)
    hist = forecast[forecast["type"] == "Historical"]
    fut  = forecast[forecast["type"] == "Forecast"]

    fig = go.Figure()
    # Confidence band
    fig.add_trace(go.Scatter(
        x=list(forecast["year_month"]) + list(forecast["year_month"][::-1]),
        y=list(forecast["upper_ci"]) + list(forecast["lower_ci"][::-1]),
        fill="toself", fillcolor="rgba(124,58,237,0.10)",
        line=dict(color="rgba(0,0,0,0)"), name="95% CI", showlegend=True,
    ))
    # Historical
    fig.add_trace(go.Scatter(
        x=hist["year_month"], y=hist["revenue"],
        mode="lines+markers",
        line=dict(color="#00d4ff", width=2.5),
        marker=dict(size=6, color="#00d4ff"),
        name="Actual Revenue",
    ))
    # Trend line (historical)
    fig.add_trace(go.Scatter(
        x=hist["year_month"], y=hist["predicted"],
        mode="lines", line=dict(color="#94a3b8", width=1.5, dash="dot"),
        name="Trend",
    ))
    # Forecast
    fig.add_trace(go.Scatter(
        x=fut["year_month"], y=fut["predicted"],
        mode="lines+markers",
        line=dict(color="#7c3aed", width=2.5, dash="dash"),
        marker=dict(size=8, color="#7c3aed", symbol="diamond"),
        name="Forecast",
    ))
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#94a3b8", size=11),
        xaxis=dict(showgrid=False, tickangle=-30, color="#94a3b8"),
        yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.04)", color="#94a3b8", title="Revenue ($)"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        hovermode="x unified",
        margin=dict(l=0, r=0, t=30, b=0), height=380,
    )
    st.plotly_chart(fig, use_container_width=True)

    if len(fut) > 0:
        next_val = fut["predicted"].iloc[0]
        last_actual = hist["revenue"].dropna().iloc[-1] if hist["revenue"].dropna().any() else 0
        delta = next_val - last_actual
        delta_str = f"+${delta:,.0f}" if delta >= 0 else f"-${abs(delta):,.0f}"
        col_m1, col_m2, col_m3 = st.columns(3)
        col_m1.metric("Next Month Forecast", f"${next_val:,.0f}", delta_str)
        col_m2.metric("Last Actual Revenue",  f"${last_actual:,.0f}")
        avg_forecast = fut["predicted"].mean()
        col_m3.metric("Avg Forecast (period)", f"${avg_forecast:,.0f}")

# ── Tab 2: Customer Segmentation ─────────────────────────────────────────────
with tab2:
    st.markdown("#### RFM Customer Segmentation — K-Means Clustering")
    st.caption("Features: Recency (days), Frequency (transactions), Monetary (revenue) · StandardScaler normalized")

    c1, c2 = st.columns([3, 2])
    with c1:
        color_map = {
            "🏆 Champions": "#fbbf24",
            "🌟 Loyal Customers": "#00d4ff",
            "⚡ Potential Loyalists": "#7c3aed",
            "😴 At-Risk": "#ef4444",
        }
        fig_seg = px.scatter(
            segments,
            x="frequency", y="monetary",
            size="recency",
            color="segment_label",
            color_discrete_map=color_map,
            hover_data=["customer_id", "recency", "avg_order_value"],
            labels={
                "frequency": "Frequency (# transactions)",
                "monetary":  "Monetary Value ($)",
                "segment_label": "Segment",
            },
            size_max=20,
        )
        fig_seg.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#94a3b8", size=11),
            xaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.04)", color="#94a3b8"),
            yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.04)", color="#94a3b8"),
            legend=dict(font=dict(size=9)),
            margin=dict(l=0, r=0, t=20, b=0), height=380,
        )
        st.plotly_chart(fig_seg, use_container_width=True)

    with c2:
        st.markdown("<br>**Segment Summary**", unsafe_allow_html=True)
        seg_summary = (
            segments.groupby("segment_label")
            .agg(
                count=("customer_id", "count"),
                avg_revenue=("monetary", "mean"),
                avg_frequency=("frequency", "mean"),
            )
            .reset_index()
        )
        for _, row in seg_summary.iterrows():
            color = color_map.get(row["segment_label"], "#94a3b8")
            st.markdown(f"""
            <div class="kpi-card" style="--accent:{color}; padding:0.8rem; margin-bottom:0.5rem;">
              <div style="font-weight:700;color:{color};font-size:0.85rem;">{row['segment_label']}</div>
              <div style="display:flex;gap:1rem;margin-top:0.4rem;">
                <div>
                  <div style="color:#64748b;font-size:0.68rem;">CUSTOMERS</div>
                  <div style="color:#f1f5f9;font-weight:600;font-size:0.9rem;">{int(row['count'])}</div>
                </div>
                <div>
                  <div style="color:#64748b;font-size:0.68rem;">AVG REVENUE</div>
                  <div style="color:#f1f5f9;font-weight:600;font-size:0.9rem;">${row['avg_revenue']:,.0f}</div>
                </div>
                <div>
                  <div style="color:#64748b;font-size:0.68rem;">AVG FREQ</div>
                  <div style="color:#f1f5f9;font-weight:600;font-size:0.9rem;">{row['avg_frequency']:.1f}</div>
                </div>
              </div>
            </div>
            """, unsafe_allow_html=True)

    # Elbow method
    st.markdown("#### K-Means Elbow Chart (Optimal k selection)")
    fig_elbow = px.line(
        elbow, x="k", y="inertia",
        markers=True, color_discrete_sequence=["#00d4ff"],
        labels={"k": "Number of Clusters (k)", "inertia": "Inertia (WCSS)"},
    )
    fig_elbow.add_vline(x=4, line_dash="dash", line_color="#7c3aed",
                        annotation_text="Selected k=4", annotation_font_color="#7c3aed")
    fig_elbow.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#94a3b8", size=11),
        xaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.04)", color="#94a3b8", dtick=1),
        yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.04)", color="#94a3b8"),
        margin=dict(l=0, r=0, t=10, b=0), height=260,
    )
    st.plotly_chart(fig_elbow, use_container_width=True)

# ── Tab 3: Anomaly Detection ──────────────────────────────────────────────────
with tab3:
    st.markdown("#### Isolation Forest Anomaly Detection")
    st.caption("Model: Isolation Forest (contamination=3%) | Features: price, quantity")

    n_anomalies = int(anomalies["is_anomaly"].sum())
    n_total     = len(anomalies)
    pct         = round(n_anomalies / n_total * 100, 2)

    a1, a2, a3 = st.columns(3)
    a1.metric("Total Transactions", f"{n_total:,}")
    a2.metric("Anomalies Flagged",  f"{n_anomalies}", f"{pct}% of total")
    a3.metric("Normal Records",     f"{n_total - n_anomalies:,}")

    st.markdown("<br>", unsafe_allow_html=True)

    fig_anm = px.scatter(
        anomalies, x="price", y="quantity",
        color="is_anomaly",
        color_discrete_map={True: "#ef4444", False: "rgba(31,41,55,0.8)"},
        hover_data=["transaction_id", "customer_id", "anomaly_score"],
        labels={"price": "Price ($)", "quantity": "Quantity", "is_anomaly": "Anomaly"},
        opacity=0.75,
    )
    fig_anm.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#94a3b8", size=11),
        xaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.04)", color="#94a3b8"),
        yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.04)", color="#94a3b8"),
        legend=dict(font=dict(size=10)),
        margin=dict(l=0, r=0, t=10, b=0), height=380,
    )
    fig_anm.update_traces(marker=dict(size=5))
    st.plotly_chart(fig_anm, use_container_width=True)

    st.markdown("#### Flagged Anomalous Transactions (sorted by anomaly score)")
    flagged = (
        anomalies[anomalies["is_anomaly"]]
        .sort_values("anomaly_score")
        .head(20)[["transaction_id","customer_id","quantity","price","channel","anomaly_score"]]
        .reset_index(drop=True)
    )
    flagged.index += 1
    st.dataframe(
        flagged.style.format({
            "price": "${:.2f}",
            "anomaly_score": "{:.4f}",
        }),
        use_container_width=True, hide_index=False,
    )

# ── Tab 4: Recommendations ────────────────────────────────────────────────────
with tab4:
    st.markdown("#### Product Recommendation Engine")
    st.caption("Algorithm: Content-based filtering (Cosine Similarity) on category + price features")

    prod_list = pr_df["product_id"].tolist()
    selected  = st.selectbox("Select a Product to Get Recommendations", prod_list)

    rec_ids = recs.get(selected, [])
    rec_prods = pr_df[pr_df["product_id"].isin(rec_ids)].copy()

    st.markdown(f"**Selected:** {pr_df[pr_df['product_id']==selected]['description'].values[0]}")
    st.markdown(f"**Category:** {pr_df[pr_df['product_id']==selected]['category'].values[0]}")
    st.markdown("---")
    st.markdown("**Top 5 Recommended Products:**")

    colors_rec = ["#fbbf24","#00d4ff","#7c3aed","#10b981","#f59e0b"]
    for i, (_, row) in enumerate(rec_prods.iterrows()):
        c = colors_rec[i % len(colors_rec)]
        st.markdown(f"""
        <div class="kpi-card" style="--accent:{c}; display:flex; align-items:center; gap:1.2rem; padding:0.8rem 1.2rem;">
          <div style="background:{c};color:#000;border-radius:50%;width:28px;height:28px;
            display:flex;align-items:center;justify-content:center;font-weight:700;font-size:0.8rem;flex-shrink:0;">
            {i+1}
          </div>
          <div style="flex:1;">
            <div style="font-weight:600;color:#f1f5f9;font-size:0.88rem;">{row['description']}</div>
            <div style="color:#64748b;font-size:0.75rem;">{row['category']}</div>
          </div>
          <div style="text-align:right;">
            <div style="color:{c};font-weight:700;font-size:0.95rem;">${row['unit_price']:,.2f}</div>
            <div style="color:#64748b;font-size:0.70rem;">unit price</div>
          </div>
        </div>
        """, unsafe_allow_html=True)
