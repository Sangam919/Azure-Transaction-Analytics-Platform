"""
pages/5_🛡️_Data_Quality.py — Data Quality Dashboard
Pipeline status, null analysis, outlier detection, quality scores.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from data_generator import load_data
from analytics_engine import run_analytics

st.set_page_config(page_title="Data Quality · Azure Analytics", page_icon="🛡️", layout="wide")

with st.spinner("Running data quality checks..."):
    tx_df, pr_df = load_data()
    res          = run_analytics(tx_df, pr_df)
    qs           = res["quality_stats"]
    clean_tx     = res["clean_tx"]

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<h1 style="font-size:1.6rem;font-weight:800;
  background:linear-gradient(90deg,#10b981,#00d4ff);
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;">
  🛡️ Data Quality Dashboard
</h1>
<p style="color:#64748b;font-size:0.85rem;margin-bottom:1.2rem;">
  3-Sigma Outlier Detection · Null Analysis · Pipeline Lineage
</p>
""", unsafe_allow_html=True)

# ── Quality Score Gauge ───────────────────────────────────────────────────────
c_gauge, c_stats = st.columns([2, 3])

with c_gauge:
    fig_gauge = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=qs["quality_pct"],
        title={"text": "Data Quality Score", "font": {"color": "#94a3b8", "size": 14}},
        number={"suffix": "%", "font": {"color": "#f1f5f9", "size": 36}},
        delta={"reference": 95, "valueformat": ".1f"},
        gauge={
            "axis":       {"range": [0, 100], "tickcolor": "#94a3b8"},
            "bar":        {"color": "#00d4ff"},
            "bgcolor":    "#111827",
            "bordercolor":"#1f2937",
            "steps": [
                {"range": [0, 70],   "color": "rgba(239,68,68,0.15)"},
                {"range": [70, 90],  "color": "rgba(245,158,11,0.15)"},
                {"range": [90, 100], "color": "rgba(16,185,129,0.15)"},
            ],
            "threshold": {"line": {"color": "#7c3aed", "width": 3}, "value": 95},
        },
    ))
    fig_gauge.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#94a3b8"),
        margin=dict(l=20, r=20, t=20, b=20), height=280,
    )
    st.plotly_chart(fig_gauge, use_container_width=True)

with c_stats:
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("#### Pipeline Statistics")
    stats_cols = st.columns(3)
    stats = [
        ("📥 Raw Records",       f"{qs['before']:,}",        "#00d4ff"),
        ("✅ Clean Records",     f"{qs['after']:,}",          "#10b981"),
        ("🗑️ Removed Records",  f"{qs['removed']:,}",        "#ef4444"),
        ("⚠️ Price Outliers",   f"{qs['outliers_price']:,}", "#f59e0b"),
        ("⚠️ Qty Outliers",     f"{qs['outliers_qty']:,}",   "#f59e0b"),
        ("🎯 Quality Score",    f"{qs['quality_pct']}%",     "#7c3aed"),
    ]
    for i, (label, value, color) in enumerate(stats):
        with stats_cols[i % 3]:
            st.markdown(f"""
            <div class="kpi-card" style="--accent:{color}; padding:0.9rem; margin-bottom:0.6rem;">
              <div class="kpi-label" style="font-size:0.7rem;">{label}</div>
              <div class="kpi-value" style="font-size:1.4rem;">{value}</div>
            </div>
            """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Null Analysis ─────────────────────────────────────────────────────────────
tab1, tab2, tab3 = st.tabs(["🔍 Null Analysis", "📊 Outlier Detection", "🔄 Pipeline Lineage"])

with tab1:
    st.markdown("#### Null Value Report by Column")
    null_data = pd.DataFrame(
        list(qs["null_counts"].items()), columns=["Column", "Null Count"]
    ).sort_values("Null Count", ascending=False)
    null_data["Null %"] = (null_data["Null Count"] / qs["after"] * 100).round(2)
    null_data["Status"] = null_data["Null %"].apply(
        lambda x: "✅ Good" if x == 0 else ("⚠️ Warning" if x < 5 else "❌ Critical")
    )

    c1, c2 = st.columns([3, 2])
    with c1:
        fig_null = px.bar(
            null_data[null_data["Null Count"] > 0].sort_values("Null Count"),
            x="Null Count", y="Column", orientation="h",
            color="Null %",
            color_continuous_scale=["#10b981","#f59e0b","#ef4444"],
            labels={"Null Count": "Null Records", "Column": ""},
        )
        fig_null.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#94a3b8", size=11),
            xaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.04)", color="#94a3b8"),
            yaxis=dict(showgrid=False, color="#94a3b8"),
            coloraxis_showscale=True,
            margin=dict(l=0, r=0, t=10, b=0), height=320,
        )
        st.plotly_chart(fig_null, use_container_width=True)

    with c2:
        st.dataframe(
            null_data.style.format({"Null %": "{:.2f}%"}),
            use_container_width=True, hide_index=True,
        )

with tab2:
    st.markdown("#### Outlier Detection — 3-Sigma Rule (Price & Quantity)")
    c1, c2 = st.columns(2)

    with c1:
        st.markdown("**Price Distribution with Outlier Flags**")
        fig_price = px.scatter(
            clean_tx.reset_index(),
            x="index", y="price",
            color="price_is_outlier",
            color_discrete_map={True: "#ef4444", False: "#1f2937"},
            labels={"index": "Transaction Index", "price": "Price ($)", "price_is_outlier": "Is Outlier"},
            opacity=0.7,
        )
        fig_price.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#94a3b8", size=11),
            xaxis=dict(showgrid=False, color="#94a3b8"),
            yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.04)", color="#94a3b8"),
            margin=dict(l=0, r=0, t=10, b=0), height=300,
        )
        fig_price.update_traces(marker=dict(size=4))
        st.plotly_chart(fig_price, use_container_width=True)

    with c2:
        st.markdown("**Quantity Distribution with Outlier Flags**")
        fig_qty = px.scatter(
            clean_tx.reset_index(),
            x="index", y="quantity",
            color="quantity_is_outlier",
            color_discrete_map={True: "#f59e0b", False: "#1f2937"},
            labels={"index": "Transaction Index", "quantity": "Quantity", "quantity_is_outlier": "Is Outlier"},
            opacity=0.7,
        )
        fig_qty.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#94a3b8", size=11),
            xaxis=dict(showgrid=False, color="#94a3b8"),
            yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.04)", color="#94a3b8"),
            margin=dict(l=0, r=0, t=10, b=0), height=300,
        )
        fig_qty.update_traces(marker=dict(size=4))
        st.plotly_chart(fig_qty, use_container_width=True)

    # Flagged outlier records
    st.markdown("#### Flagged Outlier Records (sample)")
    outliers = clean_tx[clean_tx["price_is_outlier"] | clean_tx["quantity_is_outlier"]].head(20)
    if len(outliers) > 0:
        st.dataframe(
            outliers[["transaction_id","customer_id","quantity","price",
                       "quantity_is_outlier","price_is_outlier","channel"]].reset_index(drop=True),
            use_container_width=True, hide_index=True,
        )
    else:
        st.success("No outliers detected.")

with tab3:
    st.markdown("#### ETL Pipeline Lineage")
    steps = [
        ("📥", "Data Ingestion",    "Load CSVs from ADLS Gen2 with enforced schemas",          "✅ Complete", "#10b981"),
        ("🧹", "Data Cleaning",     f"Remove {qs['removed']} duplicates & null rows",           "✅ Complete", "#10b981"),
        ("🔍", "Outlier Detection", f"3-Sigma flagging: {qs['outliers_price']} price, {qs['outliers_qty']} qty", "✅ Complete", "#10b981"),
        ("⭐", "Quality Scoring",   "Score each record on completeness & validity",              "✅ Complete", "#10b981"),
        ("🔗", "Channel Enrich",   "Tag Web / Mobile / In-Store from transaction_id prefix",   "✅ Complete", "#10b981"),
        ("📊", "Analytics Engine",  "Compute Customer LTV, Product, Campaign, Category KPIs",   "✅ Complete", "#10b981"),
        ("🤖", "ML Models",         "K-Means segmentation · Isolation Forest · Forecasting",    "✅ Complete", "#7c3aed"),
        ("💾", "Delta Lake",        "Persist to ACID Delta tables with ZORDER optimization",    "☁️ Azure Only","#4b5563"),
    ]
    for icon, title, desc, status, color in steps:
        st.markdown(f"""
        <div style="display:flex;align-items:center;gap:1rem;background:#111827;
          border:1px solid #1f2937;border-left:3px solid {color};
          border-radius:10px;padding:0.7rem 1rem;margin:0.4rem 0;">
          <div style="font-size:1.4rem;min-width:32px;">{icon}</div>
          <div style="flex:1;">
            <div style="font-weight:600;color:#f1f5f9;font-size:0.88rem;">{title}</div>
            <div style="color:#64748b;font-size:0.78rem;">{desc}</div>
          </div>
          <div style="font-size:0.78rem;font-weight:600;color:{color};white-space:nowrap;">{status}</div>
        </div>
        """, unsafe_allow_html=True)
