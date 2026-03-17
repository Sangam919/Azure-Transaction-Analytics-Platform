"""
pages/1_📊_Dashboard.py — Overview Dashboard
KPI summary cards, revenue trends, channel distribution, top customers/products, recent transactions.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from data_generator import load_data
from analytics_engine import run_analytics

st.set_page_config(page_title="Dashboard · Azure Analytics", page_icon="📊", layout="wide")

# ── Load data ─────────────────────────────────────────────────────────────────
with st.spinner("⚡ Loading analytics pipeline..."):
    tx_df, pr_df = load_data()
    res = run_analytics(tx_df, pr_df)

s     = res["summary"]
cust  = res["customers"]
prod  = res["products"]
chan  = res["channels"]
mnth  = res["monthly"]
camp  = res["campaigns"]

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<h1 style="font-size:1.6rem;font-weight:800;margin-bottom:0.2rem;
  background:linear-gradient(90deg,#00d4ff,#7c3aed);
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;">
  📊 Overview Dashboard
</h1>
<p style="color:#64748b;font-size:0.85rem;margin-bottom:1.4rem;">
  Real-time KPIs · Multi-channel analytics · April 2024 – March 2025
</p>
""", unsafe_allow_html=True)

# ── KPI Cards ─────────────────────────────────────────────────────────────────
k1, k2, k3, k4, k5 = st.columns(5)
kpis = [
    (k1, "💰 Total Revenue",       f"${s['total_revenue']:,.0f}",      "+12.4% MoM", True,  "#00d4ff"),
    (k2, "🧾 Transactions",         f"{s['total_transactions']:,}",      "+8.1% MoM",  True,  "#7c3aed"),
    (k3, "👥 Customers",            f"{s['total_customers']:,}",          "+5.3% MoM",  True,  "#f59e0b"),
    (k4, "🛒 Avg Order Value",      f"${s['avg_order_value']:,.2f}",      "+3.7% MoM",  True,  "#10b981"),
    (k5, "⚠️ Anomalies Detected",   f"{s['outlier_count']}",              "Flagged",    False, "#ef4444"),
]
for col, label, value, delta, up, color in kpis:
    with col:
        direction = "delta-up" if up else "delta-down"
        st.markdown(f"""
        <div class="kpi-card" style="--accent:{color};">
          <div class="kpi-label">{label}</div>
          <div class="kpi-value">{value}</div>
          <div class="kpi-delta {direction}">{delta}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Charts Row 1 ──────────────────────────────────────────────────────────────
c1, c2 = st.columns([3, 2])

with c1:
    st.markdown('<div class="section-header"><h2>📈 Monthly Revenue Trend</h2></div>', unsafe_allow_html=True)
    mnth_sorted = mnth.sort_values("year_month")
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=mnth_sorted["year_month"], y=mnth_sorted["revenue"],
        mode="lines+markers",
        line=dict(color="#00d4ff", width=2.5),
        marker=dict(size=6, color="#7c3aed"),
        fill="tozeroy",
        fillcolor="rgba(0,212,255,0.08)",
        name="Revenue",
        hovertemplate="<b>%{x}</b><br>Revenue: $%{y:,.0f}<extra></extra>",
    ))
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#94a3b8", size=11),
        xaxis=dict(showgrid=False, tickangle=-30, color="#94a3b8"),
        yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.04)", color="#94a3b8"),
        margin=dict(l=0, r=0, t=10, b=0), height=280,
        showlegend=False, hovermode="x unified",
    )
    st.plotly_chart(fig, use_container_width=True)

with c2:
    st.markdown('<div class="section-header"><h2>📡 Channel Split</h2></div>', unsafe_allow_html=True)
    fig_pie = px.pie(
        chan, values="revenue", names="channel",
        color_discrete_sequence=["#00d4ff", "#7c3aed", "#f59e0b"],
        hole=0.55,
    )
    fig_pie.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#94a3b8", size=11),
        legend=dict(orientation="v", x=1, y=0.5, font=dict(size=10)),
        margin=dict(l=0, r=60, t=10, b=0), height=280,
    )
    fig_pie.update_traces(textposition="inside", textinfo="percent",
                          hovertemplate="<b>%{label}</b><br>$%{value:,.0f}<extra></extra>")
    st.plotly_chart(fig_pie, use_container_width=True)

# ── Charts Row 2 ──────────────────────────────────────────────────────────────
c3, c4 = st.columns(2)

with c3:
    st.markdown('<div class="section-header"><h2>🏆 Top 10 Customers</h2></div>', unsafe_allow_html=True)
    top_c = cust.nlargest(10, "total_revenue").sort_values("total_revenue")
    fig_bc = px.bar(
        top_c, x="total_revenue", y="customer_id",
        orientation="h",
        color="total_revenue",
        color_continuous_scale=["#1a2332","#00d4ff"],
        labels={"total_revenue": "Revenue ($)", "customer_id": "Customer"},
    )
    fig_bc.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#94a3b8", size=10),
        yaxis=dict(showgrid=False, color="#94a3b8"),
        xaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.04)", color="#94a3b8"),
        coloraxis_showscale=False,
        margin=dict(l=0, r=0, t=10, b=0), height=300,
    )
    fig_bc.update_traces(hovertemplate="<b>%{y}</b><br>$%{x:,.0f}<extra></extra>")
    st.plotly_chart(fig_bc, use_container_width=True)

with c4:
    st.markdown('<div class="section-header"><h2>📦 Top 10 Products by Revenue</h2></div>', unsafe_allow_html=True)
    top_p = prod.nlargest(10, "product_revenue").sort_values("product_revenue")
    fig_bp = px.bar(
        top_p, x="product_revenue", y="description",
        orientation="h",
        color="product_revenue",
        color_continuous_scale=["#1a2332","#7c3aed"],
        labels={"product_revenue": "Revenue ($)", "description": "Product"},
    )
    fig_bp.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#94a3b8", size=10),
        yaxis=dict(showgrid=False, color="#94a3b8"),
        xaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.04)", color="#94a3b8"),
        coloraxis_showscale=False,
        margin=dict(l=0, r=0, t=10, b=0), height=300,
    )
    fig_bp.update_traces(hovertemplate="<b>%{y}</b><br>$%{x:,.0f}<extra></extra>")
    st.plotly_chart(fig_bp, use_container_width=True)

# ── Recent Transactions Table ──────────────────────────────────────────────────
st.markdown('<div class="section-header"><h2>🕒 Recent Transactions</h2></div>', unsafe_allow_html=True)
recent = (
    res["clean_tx"]
    .sort_values("transaction_date", ascending=False)
    .head(10)[["transaction_id", "customer_id", "product_id", "channel", "quantity", "price", "campaign_id", "transaction_date"]]
    .reset_index(drop=True)
)
recent["revenue"] = (recent["quantity"] * recent["price"]).round(2)
recent["transaction_date"] = pd.to_datetime(recent["transaction_date"]).dt.strftime("%Y-%m-%d")
st.dataframe(
    recent.style.format({
        "price":   "${:.2f}",
        "revenue": "${:.2f}",
    }),
    use_container_width=True,
    hide_index=True,
)
