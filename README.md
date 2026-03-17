# ⚡ Azure Transaction Analytics Platform

[![Python](https://img.shields.io/badge/Python-3.8+-3776ab?logo=python&logoColor=white)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.30+-ff4b4b?logo=streamlit&logoColor=white)](https://streamlit.io)
[![PySpark](https://img.shields.io/badge/Apache%20Spark-3.4+-e25a1c?logo=apache-spark&logoColor=white)](https://spark.apache.org)
[![Delta Lake](https://img.shields.io/badge/Delta%20Lake-2.4+-00ADD8)](https://delta.io)
[![Azure](https://img.shields.io/badge/Azure-ADLS%20Gen2-0078d4?logo=microsoft-azure&logoColor=white)](https://azure.microsoft.com)
[![Scikit-learn](https://img.shields.io/badge/Scikit--learn-1.3+-f7931e?logo=scikit-learn&logoColor=white)](https://scikit-learn.org)
[![Plotly](https://img.shields.io/badge/Plotly-5.18+-3f4f75)](https://plotly.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A **production-grade Data Engineering + AI/ML + GenAI platform** for multi-channel retail transaction analytics. Built with **Azure Databricks**, **Delta Lake**, **PySpark**, and an interactive **Streamlit dashboard** featuring machine learning models and an agentic AI query engine.

> **Developer:** Sangam Srivastav · **Internship:** Celebal Technologies — Data Engineering

---

## 🌟 What This Project Demonstrates

| Domain | Skills Showcased |
|--------|-----------------|
| **Data Engineering** | ETL Pipelines, PySpark, Azure Databricks, ADLS Gen2, Delta Lake, Schema Enforcement, Data Quality |
| **AI / Machine Learning** | K-Means (RFM), Isolation Forest, Linear Regression Forecasting, Content-Based Recommendations |
| **Generative AI** | AI-powered narrative insights, automated trend summaries, actionable recommendations |
| **Agentic AI** | Natural language query agent (13 intent types), autonomous data exploration, context-aware responses |
| **Data Applications** | Streamlit multi-page dashboard, Plotly interactive charts, responsive dark-themed UI |
| **Cloud Architecture** | Azure ADLS Gen2, Databricks Secret Scopes, Delta Lake ACID transactions, ZORDER optimization |

---

## 🏗️ Solution Architecture

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                          FULL-STACK ARCHITECTURE                             │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│   ┌──────────────┐    ┌──────────────┐    ┌──────────────────────┐          │
│   │ Data Sources │───▶│  ADLS Gen2   │───▶│   Azure Databricks   │          │
│   │ • Web        │    │ • Raw CSV    │    │ • Data Ingestion     │          │
│   │ • Mobile     │    │ • Staging    │    │ • Data Cleaning      │          │
│   │ • In-Store   │    │ • Archive    │    │ • Analytics Engine   │          │
│   └──────────────┘    └──────────────┘    └──────────┬───────────┘          │
│                                                       │                      │
│                                                       ▼                      │
│                                           ┌──────────────────────┐          │
│                                           │    Delta Lake Tables  │          │
│                                           │ • customer_analytics  │          │
│                                           │ • product_analytics   │          │
│                                           │ • campaign_analytics  │          │
│                                           │ • data_quality        │          │
│                                           └──────────────────────┘          │
│                                                                              │
├──────────────────────────────────────────────────────────────────────────────┤
│                       STREAMLIT DASHBOARD (Local Demo)                       │
│                                                                              │
│   ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌───────────────────┐    │
│   │ 📊 Overview  │ │ 👥 Customers│ │ 📦 Products │ │  📣 Campaigns     │    │
│   │  KPI Cards  │ │  RFM Segs  │ │ Cat Analysis│ │  ROI Dashboard    │    │
│   └─────────────┘ └─────────────┘ └─────────────┘ └───────────────────┘    │
│   ┌─────────────┐ ┌─────────────────────────────┐ ┌───────────────────┐    │
│   │ 🛡️ Quality  │ │  🤖 AI/ML Insights           │ │  💬 AI Agent      │    │
│   │  Null/Dup   │ │  Forecast · Cluster · Anomaly│ │  NLP Chat Agent   │    │
│   └─────────────┘ └─────────────────────────────┘ └───────────────────┘    │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## ✨ Key Features

### 🔧 Data Engineering Pipeline
- **Multi-Channel Ingestion** — Unified processing of Web, Mobile, In-Store transactions
- **Schema Enforcement** — Strict PySpark StructType schemas to prevent type errors at scale
- **Data Quality Engine** — Null detection, deduplication, outlier analysis, referential integrity
- **Delta Lake Integration** — ACID transactions, time travel, ZORDER optimization, VACUUM
- **Modular Architecture** — Clean separation: `config → loader → cleaner → analytics → delta`

### 🤖 AI / Machine Learning
- **Revenue Forecasting** — Linear Regression on monthly aggregates with 95% confidence intervals
- **Customer Segmentation** — K-Means clustering on RFM (Recency, Frequency, Monetary) features
- **Anomaly Detection** — Isolation Forest model to flag suspicious/fraudulent transactions
- **Product Recommendations** — Content-based filtering using cosine similarity on product features
- **Elbow Method** — Automated optimal k selection visualization

### 🧠 Generative AI & Agentic AI
- **AI Analytics Agent** — Natural language query engine with 13 intent types
- **Automated Insights** — AI-generated narrative summaries of trends, anomalies, and opportunities
- **Pluggable LLM Interface** — Ready for OpenAI / Azure OpenAI upgrade with one config change

### 📊 Interactive Dashboard (Streamlit)
- **7 full pages** with dark-themed glassmorphism design
- **Plotly interactive charts** — bar, line, pie, scatter, histogram, gauge, treemap
- **Real-time filters** — search, category filter, forecast period sliders
- **AI Chat Interface** — session-persistent chat with suggestion shortcuts

---

## 📁 Project Structure

```
Azure-Transaction-Analytics-Platform/
│
├── app.py                          # Streamlit entry point + global CSS
├── data_generator.py               # Synthetic data generator (demo mode)
├── analytics_engine.py             # Pandas-based analytics (mirrors PySpark)
├── ml_engine.py                    # AI/ML models (K-Means, IsoForest, LR, Cosine Sim)
├── ai_agent.py                     # Agentic AI / NLP query engine
├── requirements.txt                # Python dependencies
│
├── pages/                          # Streamlit multi-page app
│   ├── 1_📊_Dashboard.py          # KPI overview, revenue trend, channel split
│   ├── 2_👥_Customers.py          # Customer LTV, RFM segmentation
│   ├── 3_📦_Products.py           # Product & category analytics
│   ├── 4_📣_Campaigns.py          # Campaign ROI dashboard
│   ├── 5_🛡️_Data_Quality.py      # Quality scores, null/outlier analysis
│   ├── 6_🤖_AI_ML_Insights.py    # Forecast, Segmentation, Anomaly, Recs
│   └── 7_💬_AI_Agent.py          # NLP chat interface
│
├── .streamlit/
│   └── config.toml                 # Dark theme configuration
│
├── src/                            # Azure Databricks / PySpark modules
│   ├── config.py                   # ADLS Gen2 connection + secret scope
│   ├── data_loader.py              # Schema-enforced CSV ingestion
│   ├── data_cleaner.py             # Null removal, deduplication, outlier detection
│   ├── analytics.py                # Business KPI computation engine
│   ├── visualizations.py           # Matplotlib charts (Databricks)
│   ├── delta_utils.py              # Delta Lake read/write/optimize operations
│   ├── pipeline.py                 # End-to-end orchestration
│   └── ml_models.py                # PySpark MLlib ML models (NEW)
│
├── notebook/
│   └── Azure_Transaction_Analytics.ipynb  # Full pipeline notebook
│
└── Image/                          # Architecture and output screenshots
```

---

## 📊 Data Schema

### Transactions (`transactions/*.csv`)

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `transaction_id` | String | NOT NULL, UNIQUE | Prefix: WEB\_, MOB\_, STR\_ |
| `customer_id` | String | NOT NULL | Customer reference |
| `product_id` | String | FK | Links to product catalog |
| `quantity` | Integer | > 0 | Units purchased |
| `price` | Double | > 0.0 | Unit price (USD) |
| `transaction_date` | Timestamp | NOT NULL | UTC timestamp |
| `campaign_id` | String | NULLABLE | Marketing campaign |

### Products (`products.csv`)

| Column | Type | Description |
|--------|------|-------------|
| `product_id` | String | PK, unique identifier |
| `description` | String | Product name |
| `category` | String | Electronics, Clothing, Home & Kitchen, etc. |
| `unit_price` | Double | Standard price (USD) |

---

## 🚀 Quick Start — Streamlit Dashboard

### Prerequisites

```bash
Python 3.8+
```

### 1. Clone Repository

```bash
git clone https://github.com/Sangam919/Azure-Transaction-Analytics-Platform.git
cd Azure-Transaction-Analytics-Platform
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the Dashboard

```bash
streamlit run app.py
```

The dashboard opens at **http://localhost:8501** 🎉

---

## ☁️ Azure Databricks Pipeline Setup

### Prerequisites

- Azure Data Lake Storage Gen2 account
- Azure Databricks Premium workspace
- Apache Spark 3.4+ with Delta Lake 2.4

### 1. Configure Credentials

```bash
databricks secrets create-scope --scope azure-storage
databricks secrets put --scope azure-storage --key storage-access-key
```

### 2. Upload Data

```
/transaction-data/
├── transactions/
│   ├── transaction_1.csv
│   └── transaction_2.csv
├── products.csv
└── archive/
```

### 3. Run Pipeline

```python
# In Databricks notebook
%run /Repos/<username>/Azure-Transaction-Analytics-Platform/src/pipeline.py
```

### 4. Databricks Cluster Config

```json
{
  "cluster_name": "transaction-analytics-cluster",
  "spark_version": "14.3.x-scala2.12",
  "node_type_id": "Standard_DS3_v2",
  "autoscale": { "min_workers": 2, "max_workers": 8 },
  "spark_conf": {
    "spark.jars.packages": "io.delta:delta-core_2.12:2.4.0",
    "spark.sql.extensions": "io.delta.sql.DeltaSparkSessionExtension",
    "spark.sql.catalog.spark_catalog": "org.apache.spark.sql.delta.catalog.DeltaCatalog"
  }
}
```

---

## 📈 Analytics Capabilities

### Customer Intelligence
- Lifetime Value (LTV), avg order value, purchase frequency
- RFM segmentation: Champions, Loyal, Potential Loyalists, At-Risk
- Revenue outlier detection using 3-sigma rule

### Product Performance
- Top products by revenue and transaction volume
- Cross-category comparison with treemap visualizations
- Content-based product recommendation engine

### Marketing Campaign ROI
- Revenue attribution per campaign
- Unique customer reach and avg revenue per customer
- Multi-channel conversion analysis

### AI/ML Models
| Model | Purpose | Library |
|-------|---------|---------|
| Linear Regression | Revenue forecasting + 95% CI | scikit-learn |
| K-Means (k=4) | RFM customer segmentation | scikit-learn |
| Isolation Forest | Transaction anomaly detection | scikit-learn |
| Cosine Similarity | Product recommendations | scikit-learn |
| PySpark KMeans | Scalable segmentation on Databricks | MLlib |

### Agentic AI Query Engine
```
User: "Top 5 customers by revenue"      → Customer leaderboard response
User: "Show campaign performance"        → Campaign ROI breakdown
User: "How many anomalies detected?"     → Anomaly detection summary
User: "What is the data quality score?"  → Quality report
```

---

## 🔍 Sample SQL Queries (Delta Lake)

```sql
-- Top customers by revenue
SELECT customer_id, total_revenue, total_transactions
FROM analytics_db.customer_analytics
WHERE total_revenue > 1000
ORDER BY total_revenue DESC;

-- Campaign performance
SELECT campaign_id, campaign_revenue, unique_customers, avg_revenue_per_customer
FROM analytics_db.campaign_analytics
ORDER BY campaign_revenue DESC;

-- Anomalous transactions
SELECT transaction_id, customer_id, price, quantity
FROM analytics_db.transactions_insights
WHERE price_is_outlier = true OR quantity_is_outlier = true;

-- Data quality summary
SELECT * FROM analytics_db.data_quality_summary;
```

---

## 🛠️ Future Roadmap

- **Real-time Streaming** — Apache Kafka + Spark Structured Streaming integration
- **LLM Integration** — OpenAI / Azure OpenAI upgrade for the AI Agent
- **Unity Catalog** — Data governance and lineage tracking
- **Power BI** — Live Delta Lake connector for BI dashboards
- **Databricks Workflows** — Automated daily pipeline scheduling
- **Docker** — Containerized deployment for the Streamlit app
- **dbt** — Transformation layer for the analytics models

---

## 🙌 Acknowledgments

Developed as a capstone project during a **Data Engineering Internship at Celebal Technologies**.
Special thanks to the Data Engineering mentorship team for guidance on enterprise Azure architecture.

---

*Built with ❤️ by **Sangam Srivastav** during Data Engineering Internship at Celebal Technologies*
