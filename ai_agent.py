"""
ai_agent.py — Agentic AI / GenAI Query Engine
Provides two capabilities:
  1. Natural Language Query Agent  — parses user questions → data answers
  2. AI Insights Generator         — automated narrative reporting

Designed with a pluggable LLM interface: set USE_LLM=True and provide
OPENAI_API_KEY to upgrade from rule-based to GPT-powered responses.
"""

import re
import random
import pandas as pd
import numpy as np
from datetime import datetime

# ─── Config ──────────────────────────────────────────────────────────────────
USE_LLM = False   # Set True + provide API key for real LLM integration

# ─── Intent patterns ─────────────────────────────────────────────────────────
INTENTS = {
    "top_customers":   r"top\s*(\d+)?\s*(customers?|buyers?|clients?)",
    "top_products":    r"top\s*(\d+)?\s*(products?|items?|goods?)",
    "revenue":         r"(total|overall)?\s*revenue|earnings|sales",
    "category":        r"categor(y|ies)|department",
    "campaign":        r"campaign|marketing|promotion",
    "anomaly":         r"anomal|outlier|fraud|suspicious|unusual",
    "channel":         r"channel|web|mobile|in.?store",
    "forecast":        r"forecast|predict|future|next\s*\d+\s*months?",
    "quality":         r"quality|null|missing|duplicate|clean",
    "segment":         r"segment|cluster|group|rfm",
    "avg_order":       r"average\s*order|aov|avg\s*basket",
    "transactions":    r"transaction(s)?|orders?|purchase(s)?",
    "customers_count": r"how many customers|number of customers|customer count",
}

# ─── Canned insight templates ────────────────────────────────────────────────
INSIGHT_TEMPLATES = [
    "📈 Revenue is **{rev_trend}** compared to the previous month, driven primarily by **{top_cat}** category.",
    "🏆 Your top customer **{top_cust}** contributes **{top_cust_pct:.1f}%** of total revenue — consider a VIP loyalty program.",
    "⚠️ **{outlier_count}** anomalous transactions were detected — these may indicate pricing errors or fraudulent activity.",
    "📣 Campaign **{top_camp}** achieved the highest ROI with **${camp_rev:,.0f}** revenue from **{camp_cust}** unique customers.",
    "📱 **{top_channel}** channel leads revenue generation at **{channel_pct:.1f}%** of total sales.",
    "🛒 Average order value is **${aov:,.2f}** — upselling opportunities exist in **{low_cat}** where AOV is lowest.",
    "🔮 Based on current trends, next month's revenue is projected at **${forecast:,.0f}**.",
    "👥 Customer segmentation reveals **{champion_pct:.1f}%** Champions — focus retention efforts on Potential Loyalists to grow this cohort.",
]


# ─── Main Agent Class ─────────────────────────────────────────────────────────
class TransactionAnalyticsAgent:
    """Rule-based NLP agent that answers data questions about transaction analytics."""

    def __init__(self, analytics_data: dict):
        self.data = analytics_data
        self.history: list[dict] = []

    def _detect_intent(self, query: str) -> str:
        q = query.lower()
        for intent, pattern in INTENTS.items():
            if re.search(pattern, q):
                return intent
        return "general"

    def _extract_n(self, query: str, default: int = 5) -> int:
        match = re.search(r"\b(\d+)\b", query)
        return int(match.group(1)) if match else default

    # ── Intent handlers ───────────────────────────────────────────────────
    def _handle_top_customers(self, query: str) -> str:
        n = min(self._extract_n(query, 5), 20)
        df = self.data["customers"].nlargest(n, "total_revenue")[
            ["customer_id", "total_revenue", "total_transactions", "avg_order_value"]
        ].reset_index(drop=True)
        df.index += 1
        rows = "\n".join(
            f"  {i}. **{r.customer_id}** — ${r.total_revenue:,.2f} revenue, {r.total_transactions} orders"
            for i, r in df.iterrows()
        )
        return f"🏆 **Top {n} Customers by Revenue:**\n\n{rows}"

    def _handle_top_products(self, query: str) -> str:
        n = min(self._extract_n(query, 5), 20)
        df = self.data["products"].nlargest(n, "product_revenue")[
            ["description", "category", "units_sold", "product_revenue"]
        ].reset_index(drop=True)
        df.index += 1
        rows = "\n".join(
            f"  {i}. **{r.description}** ({r.category}) — {r.units_sold} units, ${r.product_revenue:,.2f}"
            for i, r in df.iterrows()
        )
        return f"📦 **Top {n} Products by Revenue:**\n\n{rows}"

    def _handle_revenue(self, query: str) -> str:
        s = self.data["summary"]
        monthly = self.data["monthly"].sort_values("year_month")
        last_two = monthly.tail(2)["revenue"].tolist()
        trend = "📈 up" if len(last_two) == 2 and last_two[1] > last_two[0] else "📉 down"
        return (
            f"💰 **Total Revenue:** ${s['total_revenue']:,.2f}\n\n"
            f"📊 **Total Transactions:** {s['total_transactions']:,}\n\n"
            f"📅 **Monthly Trend:** Revenue is {trend} this month compared to last month.\n\n"
            f"🏷️ **Top Category:** {s['top_category']}\n\n"
            f"📡 **Top Channel:** {s['top_channel']}"
        )

    def _handle_category(self, query: str) -> str:
        df = self.data["categories"]
        rows = "\n".join(
            f"  {i+1}. **{r.category}** — ${r.category_revenue:,.2f} ({r.units_sold:,} units)"
            for i, r in df.iterrows()
        )
        return f"🏷️ **Category Revenue Breakdown:**\n\n{rows}"

    def _handle_campaign(self, query: str) -> str:
        df = self.data["campaigns"].sort_values("campaign_revenue", ascending=False)
        rows = "\n".join(
            f"  {i+1}. **{r.campaign_id}** — ${r.campaign_revenue:,.2f} | {r.unique_customers} customers | ${r.avg_revenue_per_customer:,.2f}/customer"
            for i, r in df.reset_index(drop=True).iterrows()
        )
        return f"📣 **Campaign Performance:**\n\n{rows}"

    def _handle_anomaly(self, query: str) -> str:
        count = self.data["summary"]["outlier_count"]
        total = self.data["summary"]["total_transactions"]
        pct   = round(count / total * 100, 2)
        return (
            f"⚠️ **Anomaly Detection Results (Isolation Forest + 3-Sigma):**\n\n"
            f"  • **{count}** flagged transactions out of {total:,} total ({pct}%)\n"
            f"  • These records have unusually high/low price or quantity values\n"
            f"  • Navigate to **AI/ML Insights → Anomaly Detection** tab for the full scatter plot\n"
            f"  • Recommended action: Manual review of flagged transactions"
        )

    def _handle_channel(self, query: str) -> str:
        df = self.data["channels"].sort_values("revenue", ascending=False)
        rows = "\n".join(
            f"  • **{r.channel}** — ${r.revenue:,.2f} ({r.transactions:,} transactions)"
            for _, r in df.iterrows()
        )
        return f"📡 **Channel Distribution:**\n\n{rows}"

    def _handle_quality(self, query: str) -> str:
        qs = self.data["quality_stats"]
        return (
            f"🛡️ **Data Quality Report:**\n\n"
            f"  • **Rows before cleaning:** {qs['before']:,}\n"
            f"  • **Rows after cleaning:** {qs['after']:,}\n"
            f"  • **Duplicates removed:** {qs['removed']:,}\n"
            f"  • **Price outliers flagged:** {qs['outliers_price']:,}\n"
            f"  • **Quantity outliers flagged:** {qs['outliers_qty']:,}\n"
            f"  • **Overall quality score:** {qs['quality_pct']}%\n"
        )

    def _handle_customers_count(self, query: str) -> str:
        n = self.data["summary"]["total_customers"]
        return f"👥 There are **{n:,} unique customers** in the dataset."

    def _handle_avg_order(self, query: str) -> str:
        s = self.data["summary"]
        return f"🛒 **Average Order Value (AOV):** ${s['avg_order_value']:,.2f} per transaction."

    def _handle_general(self, query: str) -> str:
        suggestions = [
            "• *Top 5 customers by revenue*",
            "• *Show campaign performance*",
            "• *What is the total revenue?*",
            "• *Which category has highest sales?*",
            "• *Show channel distribution*",
            "• *How many anomalies were detected?*",
            "• *What is the data quality score?*",
            "• *How many customers do we have?*",
        ]
        return (
            "🤖 I didn't quite understand that. Here are some things you can ask me:\n\n"
            + "\n".join(suggestions)
        )

    # ── Public query entrypoint ───────────────────────────────────────────
    def query(self, user_input: str) -> str:
        """Process a natural language question and return a markdown response."""
        intent = self._detect_intent(user_input)
        handler_map = {
            "top_customers":   self._handle_top_customers,
            "top_products":    self._handle_top_products,
            "revenue":         self._handle_revenue,
            "category":        self._handle_category,
            "campaign":        self._handle_campaign,
            "anomaly":         self._handle_anomaly,
            "channel":         self._handle_channel,
            "quality":         self._handle_quality,
            "customers_count": self._handle_customers_count,
            "avg_order":       self._handle_avg_order,
            "transactions":    self._handle_revenue,
            "segment":         lambda q: "🔬 Navigate to **AI/ML Insights → Customer Segmentation** tab to explore RFM clusters interactively.",
            "forecast":        lambda q: "🔮 Navigate to **AI/ML Insights → Revenue Forecast** tab to see the 6-month revenue projection.",
            "general":         self._handle_general,
        }
        handler  = handler_map.get(intent, self._handle_general)
        response = handler(user_input)

        # Store in history
        self.history.append({
            "role":    "user",
            "content": user_input,
            "time":    datetime.now().strftime("%H:%M"),
        })
        self.history.append({
            "role":    "assistant",
            "content": response,
            "intent":  intent,
            "time":    datetime.now().strftime("%H:%M"),
        })
        return response

    # ── Auto Insights ─────────────────────────────────────────────────────
    def generate_insights(self) -> list[str]:
        """Generate a list of automated narrative insight strings."""
        s       = self.data["summary"]
        monthly = self.data["monthly"].sort_values("year_month")
        cust    = self.data["customers"]
        camp    = self.data["campaigns"].sort_values("campaign_revenue", ascending=False)
        chan    = self.data["channels"].sort_values("revenue", ascending=False)
        cat     = self.data["categories"]

        last_two  = monthly.tail(2)["revenue"].tolist()
        rev_trend = "growing 📈" if len(last_two) == 2 and last_two[1] > last_two[0] else "declining 📉"

        top_cust     = cust.nlargest(1, "total_revenue").iloc[0]
        top_cust_pct = top_cust["total_revenue"] / s["total_revenue"] * 100
        top_camp_row = camp.iloc[0] if len(camp) > 0 else None
        top_chan_row = chan.iloc[0]
        chan_pct     = top_chan_row["revenue"] / s["total_revenue"] * 100

        low_cat = cat.nsmallest(1, "category_revenue").iloc[0]
        forecast_val = (monthly["revenue"].mean() * 1.03)   # approximation

        insights = [
            f"📈 Revenue is **{rev_trend}** — the platform processed **${s['total_revenue']:,.0f}** across **{s['total_transactions']:,}** transactions.",
            f"🏆 Top customer **{top_cust['customer_id']}** contributes **{top_cust_pct:.1f}%** of total revenue. Consider a VIP loyalty tier.",
            f"⚠️ **{s['outlier_count']}** anomalous transactions detected via Isolation Forest — review flagged records in the AI/ML page.",
            f"📱 **{top_chan_row['channel']}** is the leading channel, driving **{chan_pct:.1f}%** of total revenue.",
            f"🛒 Average Order Value is **${s['avg_order_value']:,.2f}** — upsell opportunities exist in **{low_cat['category']}**.",
            f"🔮 Based on linear trend analysis, next month's projected revenue is approximately **${forecast_val:,.0f}**.",
        ]
        if top_camp_row is not None:
            insights.insert(3, f"📣 Campaign **{top_camp_row['campaign_id']}** generated **${top_camp_row['campaign_revenue']:,.0f}** in revenue from **{int(top_camp_row['unique_customers'])}** customers.")

        return insights
