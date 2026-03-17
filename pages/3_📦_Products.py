"""
pages/3_📦_Products.py — Product Analytics
Product performance, category breakdown, units sold, revenue per product.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from data_generator import load_data
from analytics_engine import run_analytics

st.set_page_config(page_title="Products · Azure Analytics", page_icon="📦", layout="wide")

with st.spinner("Loading product analytics..."):
    tx_df, pr_df = load_data()
    res  = run_analytics(tx_df, pr_df)
    prod = res["products"]
    cat  = res["categories"]

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<h1 style="font-size:1.6rem;font-weight:800;
  background:linear-gradient(90deg,#f59e0b,#ef4444);
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;">
  📦 Product Analytics
</h1>
<p style="color:#64748b;font-size:0.85rem;margin-bottom:1.2rem;">
  Product Performance · Category Breakdown · Inventory Insights
</p>
""", unsafe_allow_html=True)

# ── KPIs ──────────────────────────────────────────────────────────────────────
k1, k2, k3, k4 = st.columns(4)
kpis = [
    (k1, "📦 Total Products",       f"{len(prod):,}",                                   "#f59e0b"),
    (k2, "🏷️ Categories",           f"{prod['category'].nunique()}",                    "#00d4ff"),
    (k3, "📊 Top Product Revenue",  f"${prod['product_revenue'].max():,.0f}",            "#7c3aed"),
    (k4, "📦 Total Units Sold",     f"{int(prod['units_sold'].sum()):,}",                "#10b981"),
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
tab1, tab2, tab3 = st.tabs(["🏷️ Category Performance", "🏆 Top Products", "📋 Full Product Table"])

with tab1:
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("#### Revenue by Category")
        fig_cat = px.bar(
            cat.sort_values("category_revenue"),
            x="category_revenue", y="category",
            orientation="h",
            color="category_revenue",
            color_continuous_scale=["#1a2332","#f59e0b"],
            text="category_revenue",
            labels={"category_revenue": "Revenue ($)", "category": "Category"},
        )
        fig_cat.update_traces(
            texttemplate="$%{text:,.0f}", textposition="outside",
            hovertemplate="<b>%{y}</b><br>$%{x:,.0f}<extra></extra>",
        )
        fig_cat.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#94a3b8", size=11),
            xaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.04)", color="#94a3b8"),
            yaxis=dict(showgrid=False, color="#94a3b8"),
            coloraxis_showscale=False,
            margin=dict(l=0, r=80, t=10, b=0), height=340,
        )
        st.plotly_chart(fig_cat, use_container_width=True)

    with c2:
        st.markdown("#### Units Sold by Category")
        fig_pie = px.pie(
            cat, values="units_sold", names="category",
            color_discrete_sequence=px.colors.qualitative.Bold,
            hole=0.45,
        )
        fig_pie.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#94a3b8", size=11),
            legend=dict(orientation="v", x=1, y=0.5, font=dict(size=10)),
            margin=dict(l=0, r=80, t=10, b=0), height=340,
        )
        fig_pie.update_traces(textinfo="percent+label", textfont_size=10)
        st.plotly_chart(fig_pie, use_container_width=True)

    # Category stats table
    cat_display = cat.copy()
    cat_display["category_revenue"] = cat_display["category_revenue"].apply(lambda x: f"${x:,.2f}")
    st.dataframe(cat_display.rename(columns={
        "category": "Category", "units_sold": "Units Sold", "category_revenue": "Revenue"
    }), use_container_width=True, hide_index=True)

with tab2:
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("#### Top 15 Products by Revenue")
        top_rev = prod.nlargest(15, "product_revenue").sort_values("product_revenue")
        fig_bp = px.bar(
            top_rev, x="product_revenue", y="description",
            orientation="h", color="category",
            labels={"product_revenue": "Revenue ($)", "description": "Product"},
            color_discrete_sequence=px.colors.qualitative.Bold,
        )
        fig_bp.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#94a3b8", size=10),
            xaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.04)", color="#94a3b8"),
            yaxis=dict(showgrid=False, color="#94a3b8"),
            legend=dict(font=dict(size=9)),
            margin=dict(l=0, r=0, t=10, b=0), height=420,
        )
        st.plotly_chart(fig_bp, use_container_width=True)

    with c2:
        st.markdown("#### Top 15 Products by Units Sold")
        top_units = prod.nlargest(15, "units_sold").sort_values("units_sold")
        fig_bu = px.bar(
            top_units, x="units_sold", y="description",
            orientation="h", color="category",
            labels={"units_sold": "Units Sold", "description": "Product"},
            color_discrete_sequence=px.colors.qualitative.Pastel,
        )
        fig_bu.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#94a3b8", size=10),
            xaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.04)", color="#94a3b8"),
            yaxis=dict(showgrid=False, color="#94a3b8"),
            legend=dict(font=dict(size=9)),
            margin=dict(l=0, r=0, t=10, b=0), height=420,
        )
        st.plotly_chart(fig_bu, use_container_width=True)

    # Revenue vs Units scatter
    st.markdown("#### Revenue vs Units Sold (all products)")
    fig_scatter = px.scatter(
        prod, x="units_sold", y="product_revenue",
        color="category", size="product_revenue",
        hover_data=["description"],
        labels={"units_sold": "Units Sold", "product_revenue": "Revenue ($)", "category": "Category"},
        color_discrete_sequence=px.colors.qualitative.Bold,
        size_max=30,
    )
    fig_scatter.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#94a3b8", size=11),
        xaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.04)", color="#94a3b8"),
        yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.04)", color="#94a3b8"),
        margin=dict(l=0, r=0, t=20, b=0), height=350,
    )
    st.plotly_chart(fig_scatter, use_container_width=True)

with tab3:
    st.markdown("#### Full Product Catalog")
    filter_cat = st.selectbox("Filter by category", ["All"] + sorted(prod["category"].unique().tolist()))
    df_show = prod.copy() if filter_cat == "All" else prod[prod["category"] == filter_cat]
    df_show = df_show.sort_values("product_revenue", ascending=False).reset_index(drop=True)
    df_show.index += 1
    st.dataframe(
        df_show.style.format({
            "product_revenue": "${:,.2f}",
        }),
        use_container_width=True, hide_index=False,
    )
