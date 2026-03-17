"""
pages/4_📣_Campaigns.py — Campaign Analytics
Campaign ROI, revenue attribution, unique customer reach, avg revenue per customer.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from data_generator import load_data
from analytics_engine import run_analytics

st.set_page_config(page_title="Campaigns · Azure Analytics", page_icon="📣", layout="wide")

with st.spinner("Loading campaign analytics..."):
    tx_df, pr_df = load_data()
    res  = run_analytics(tx_df, pr_df)
    camp = res["campaigns"].sort_values("campaign_revenue", ascending=False)
    chan = res["channels"]

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<h1 style="font-size:1.6rem;font-weight:800;
  background:linear-gradient(90deg,#10b981,#00d4ff);
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;">
  📣 Campaign Analytics
</h1>
<p style="color:#64748b;font-size:0.85rem;margin-bottom:1.2rem;">
  Campaign ROI · Revenue Attribution · Customer Acquisition
</p>
""", unsafe_allow_html=True)

# ── KPIs ──────────────────────────────────────────────────────────────────────
k1, k2, k3, k4 = st.columns(4)
kpis = [
    (k1, "📣 Active Campaigns",        f"{len(camp)}",                                           "#10b981"),
    (k2, "💰 Total Campaign Revenue",   f"${camp['campaign_revenue'].sum():,.0f}",                "#00d4ff"),
    (k3, "👥 Unique Customers Reached", f"{int(camp['unique_customers'].sum()):,}",               "#7c3aed"),
    (k4, "💳 Best Avg Rev/Customer",    f"${camp['avg_revenue_per_customer'].max():,.2f}",        "#f59e0b"),
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

# ── Charts Row 1 ──────────────────────────────────────────────────────────────
c1, c2 = st.columns([3, 2])

with c1:
    st.markdown("#### Campaign Revenue Comparison")
    fig_bar = go.Figure()
    colors  = ["#00d4ff","#7c3aed","#f59e0b","#10b981","#ef4444"]
    for i, (_, row) in enumerate(camp.iterrows()):
        fig_bar.add_trace(go.Bar(
            name=row["campaign_id"],
            x=[row["campaign_id"]],
            y=[row["campaign_revenue"]],
            marker_color=colors[i % len(colors)],
            hovertemplate=f"<b>{row['campaign_id']}</b><br>Revenue: $%{{y:,.0f}}<extra></extra>",
        ))
    fig_bar.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#94a3b8", size=11),
        xaxis=dict(showgrid=False, color="#94a3b8"),
        yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.04)", color="#94a3b8",
                   title="Revenue ($)"),
        showlegend=False,
        margin=dict(l=0, r=0, t=10, b=0), height=300,
    )
    st.plotly_chart(fig_bar, use_container_width=True)

with c2:
    st.markdown("#### Campaign Revenue Share")
    fig_pie = px.pie(
        camp, values="campaign_revenue", names="campaign_id",
        hole=0.55,
        color_discrete_sequence=["#00d4ff","#7c3aed","#f59e0b","#10b981","#ef4444"],
    )
    fig_pie.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#94a3b8", size=11),
        legend=dict(orientation="v", x=1, y=0.5),
        margin=dict(l=0, r=60, t=10, b=0), height=300,
    )
    fig_pie.update_traces(textinfo="percent", textfont_size=11)
    st.plotly_chart(fig_pie, use_container_width=True)

# ── Charts Row 2 ──────────────────────────────────────────────────────────────
c3, c4 = st.columns(2)

with c3:
    st.markdown("#### Unique Customers per Campaign")
    fig_cust = px.bar(
        camp.sort_values("unique_customers", ascending=True),
        x="unique_customers", y="campaign_id",
        orientation="h",
        color="unique_customers",
        color_continuous_scale=["#1a2332","#10b981"],
        labels={"unique_customers": "Unique Customers", "campaign_id": "Campaign"},
    )
    fig_cust.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#94a3b8", size=11),
        xaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.04)", color="#94a3b8"),
        yaxis=dict(showgrid=False, color="#94a3b8"),
        coloraxis_showscale=False,
        margin=dict(l=0, r=0, t=10, b=0), height=260,
    )
    st.plotly_chart(fig_cust, use_container_width=True)

with c4:
    st.markdown("#### Avg Revenue per Customer")
    fig_arpc = px.bar(
        camp.sort_values("avg_revenue_per_customer", ascending=True),
        x="avg_revenue_per_customer", y="campaign_id",
        orientation="h",
        color="avg_revenue_per_customer",
        color_continuous_scale=["#1a2332","#7c3aed"],
        labels={"avg_revenue_per_customer": "Avg Rev/Customer ($)", "campaign_id": "Campaign"},
    )
    fig_arpc.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#94a3b8", size=11),
        xaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.04)", color="#94a3b8"),
        yaxis=dict(showgrid=False, color="#94a3b8"),
        coloraxis_showscale=False,
        margin=dict(l=0, r=0, t=10, b=0), height=260,
    )
    st.plotly_chart(fig_arpc, use_container_width=True)

# ── Campaign Summary Table ────────────────────────────────────────────────────
st.markdown("#### Campaign Summary Table")
camp_display = camp.copy().reset_index(drop=True)
camp_display.index += 1
st.dataframe(
    camp_display.style.format({
        "campaign_revenue": "${:,.2f}",
        "avg_revenue_per_customer": "${:,.2f}",
    }),
    use_container_width=True, hide_index=False,
)

# ── Channel vs Campaign Insight ───────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("#### 📡 Channel Revenue Distribution")
chan_sorted = chan.sort_values("revenue", ascending=False)
cols = st.columns(len(chan_sorted))
colors_ch = {"Web": "#00d4ff", "Mobile": "#7c3aed", "In-Store": "#f59e0b"}
for (_, row), col in zip(chan_sorted.iterrows(), cols):
    with col:
        color = colors_ch.get(row["channel"], "#94a3b8")
        pct   = round(row["revenue"] / chan["revenue"].sum() * 100, 1)
        st.markdown(f"""
        <div class="kpi-card" style="--accent:{color}; text-align:center;">
          <div class="kpi-label">{row['channel']}</div>
          <div class="kpi-value">${row['revenue']:,.0f}</div>
          <div class="kpi-delta delta-up">{pct}% of total</div>
          <div class="kpi-delta" style="color:#94a3b8;">{int(row['transactions']):,} transactions</div>
        </div>
        """, unsafe_allow_html=True)
