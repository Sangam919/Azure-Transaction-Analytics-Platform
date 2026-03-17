"""
pages/2_👥_Customers.py — Customer Analytics
Customer LTV, segmentation, revenue distribution, outlier flagging.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from data_generator import load_data
from analytics_engine import run_analytics
from ml_engine import segment_customers

st.set_page_config(page_title="Customers · Azure Analytics", page_icon="👥", layout="wide")

with st.spinner("Loading customer analytics..."):
    tx_df, pr_df = load_data()
    res  = run_analytics(tx_df, pr_df)
    cust = res["customers"]
    segs = segment_customers(cust, res["joined"])

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<h1 style="font-size:1.6rem;font-weight:800;
  background:linear-gradient(90deg,#00d4ff,#7c3aed);
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;">
  👥 Customer Analytics
</h1>
<p style="color:#64748b;font-size:0.85rem;margin-bottom:1.2rem;">
  Customer LTV · RFM Segmentation · Outlier Detection
</p>
""", unsafe_allow_html=True)

# ── KPIs ──────────────────────────────────────────────────────────────────────
k1, k2, k3, k4 = st.columns(4)
kpis = [
    (k1, "👥 Total Customers",     f"{len(cust):,}",                                 "#00d4ff"),
    (k2, "💰 Avg LTV",             f"${cust['total_revenue'].mean():,.2f}",           "#7c3aed"),
    (k3, "🛒 Avg Order Value",     f"${cust['avg_order_value'].mean():,.2f}",         "#f59e0b"),
    (k4, "⚠️ Revenue Outliers",    f"{int(cust['is_revenue_outlier'].sum())}",        "#ef4444"),
]
for col, label, value, color in kpis:
    with col:
        st.markdown(f"""
        <div class="kpi-card" style="--accent:{color};">
          <div class="kpi-label">{label}</div>
          <div class="kpi-value">{value}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Tabs ──────────────────────────────────────────────────────────────────────
tab1, tab2, tab3 = st.tabs(["📋 Customer Table", "🔬 RFM Segmentation", "📊 Revenue Distribution"])

with tab1:
    st.markdown("#### Customer Leaderboard")
    search = st.text_input("🔍 Search Customer ID", placeholder="e.g. CUST_0042")
    df_show = cust.copy()
    if search:
        df_show = df_show[df_show["customer_id"].str.contains(search, case=False, na=False)]

    df_show = df_show.sort_values("total_revenue", ascending=False).reset_index(drop=True)
    df_show.index += 1
    df_show["last_purchase"] = pd.to_datetime(df_show["last_purchase"]).dt.strftime("%Y-%m-%d")
    df_show["first_purchase"] = pd.to_datetime(df_show["first_purchase"]).dt.strftime("%Y-%m-%d")
    df_show["is_revenue_outlier"] = df_show["is_revenue_outlier"].map({True: "⚠️ Yes", False: "✅ No"})

    st.dataframe(
        df_show[["customer_id","total_transactions","total_revenue","avg_order_value","is_revenue_outlier","last_purchase"]]
        .style.format({
            "total_revenue": "${:,.2f}",
            "avg_order_value": "${:,.2f}",
        }),
        use_container_width=True, hide_index=False,
    )

with tab2:
    st.markdown("#### K-Means RFM Customer Segmentation")
    c1, c2 = st.columns([3, 1])

    with c2:
        st.markdown("<br>", unsafe_allow_html=True)
        seg_counts = segs["segment_label"].value_counts().reset_index()
        seg_counts.columns = ["Segment", "Count"]
        for _, row in seg_counts.iterrows():
            colors = {
                "🏆 Champions": "#fbbf24",
                "🌟 Loyal Customers": "#00d4ff",
                "⚡ Potential Loyalists": "#7c3aed",
                "😴 At-Risk": "#ef4444",
            }
            c = colors.get(row["Segment"], "#94a3b8")
            st.markdown(f"""
            <div class="kpi-card" style="--accent:{c}; padding:0.7rem 1rem; margin-bottom:0.5rem;">
              <div class="kpi-label" style="font-size:0.7rem;">{row['Segment']}</div>
              <div class="kpi-value" style="font-size:1.2rem;">{row['Count']} customers</div>
            </div>
            """, unsafe_allow_html=True)

    with c1:
        color_map = {
            "🏆 Champions":          "#fbbf24",
            "🌟 Loyal Customers":     "#00d4ff",
            "⚡ Potential Loyalists": "#7c3aed",
            "😴 At-Risk":            "#ef4444",
        }
        fig = px.scatter(
            segs, x="recency", y="monetary",
            size="frequency", color="segment_label",
            color_discrete_map=color_map,
            hover_data=["customer_id", "total_transactions", "avg_order_value"],
            labels={
                "recency": "Recency (days since last purchase)",
                "monetary": "Monetary Value ($)",
                "segment_label": "Segment",
            },
            size_max=25,
        )
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#94a3b8", size=11),
            xaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.04)", color="#94a3b8"),
            yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.04)", color="#94a3b8"),
            legend=dict(font=dict(size=9)),
            margin=dict(l=0, r=0, t=20, b=0), height=380,
        )
        st.plotly_chart(fig, use_container_width=True)

with tab3:
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("#### Total Revenue Distribution")
        fig_hist = px.histogram(
            cust, x="total_revenue", nbins=40,
            color_discrete_sequence=["#00d4ff"],
            labels={"total_revenue": "Total Revenue ($)"},
        )
        fig_hist.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#94a3b8", size=11),
            xaxis=dict(showgrid=False, color="#94a3b8"),
            yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.04)", color="#94a3b8"),
            margin=dict(l=0, r=0, t=10, b=0), height=300,
        )
        st.plotly_chart(fig_hist, use_container_width=True)

    with c2:
        st.markdown("#### Avg Order Value Distribution")
        fig_box = px.box(
            segs, x="segment_label", y="avg_order_value",
            color="segment_label",
            color_discrete_map={
                "🏆 Champions": "#fbbf24",
                "🌟 Loyal Customers": "#00d4ff",
                "⚡ Potential Loyalists": "#7c3aed",
                "😴 At-Risk": "#ef4444",
            },
            labels={"segment_label": "Segment", "avg_order_value": "Avg Order Value ($)"},
        )
        fig_box.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#94a3b8", size=11),
            xaxis=dict(showgrid=False, color="#94a3b8", tickangle=-15),
            yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.04)", color="#94a3b8"),
            showlegend=False,
            margin=dict(l=0, r=0, t=10, b=0), height=300,
        )
        st.plotly_chart(fig_box, use_container_width=True)
