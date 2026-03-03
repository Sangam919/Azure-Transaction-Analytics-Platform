# 🚀 Azure Transaction Analytics Platform

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Apache Spark](https://img.shields.io/badge/Apache%20Spark-3.4+-orange.svg)](https://spark.apache.org/)
[![Delta Lake](https://img.shields.io/badge/Delta%20Lake-2.4.0+-green.svg)](https://delta.io/)
[![Azure](https://img.shields.io/badge/Azure-Data%20Lake%20Gen2-blue.svg)](https://azure.microsoft.com/en-us/services/storage/data-lake-storage/)

A production-grade data engineering pipeline for analyzing multi-channel transaction data (web, mobile, in-store) using **Azure Databricks**, **Delta Lake**, and **Azure Data Lake Storage Gen2**. Developed as a capstone project during a Data Engineering Internship at **Celebal Technologies**.

---

## 🌟 Project Overview

This platform solves real-world data engineering challenges in multi-channel retail analytics. The pipeline ingests raw transaction data from multiple channels, applies enterprise-grade data quality checks, and delivers actionable business insights using scalable Apache Spark and Delta Lake architecture on Azure cloud.

---

## 🏗️ Solution Architecture

```
┌──────────────┐    ┌──────────────┐    ┌──────────────────────┐    ┌──────────────┐
│ Data Sources │───▶│  ADLS Gen2   │───▶│   Azure Databricks   │───▶│ Delta Tables │
│ • Web        │    │ • Raw CSV    │    │ • Data Ingestion     │    │ • Analytics  │
│ • Mobile     │    │ • Staging    │    │ • Data Cleaning      │    │ • Insights   │
│ • In-Store   │    │ • Archive    │    │ • Analytics Engine   │    │ • Reports    │
└──────────────┘    └──────────────┘    └──────────────────────┘    └──────────────┘
```

**Data Flow:**
1. Raw CSVs land in ADLS Gen2
2. `data_loader.py` ingests and schemas the data
3. `data_cleaner.py` validates quality and removes anomalies
4. `analytics.py` computes business KPIs
5. `delta_utils.py` persists results as Delta tables
6. `pipeline.py` orchestrates the full end-to-end run

---

## ✨ Key Features

- **Multi-Channel Ingestion** — Unified processing of web, mobile, and in-store transaction data
- **Enterprise Data Quality** — Null detection, outlier analysis, referential integrity validation
- **Delta Lake Integration** — ACID transactions, time travel, and optimized Parquet storage
- **Business Intelligence Engine** — Customer LTV, product performance, campaign ROI analytics
- **Modular Architecture** — Clean separation of concerns across ingestion, cleaning, analytics layers
- **Scalable Spark Processing** — Distributed computing for large-scale transaction volumes
- **Production-Ready Code** — Comprehensive error handling, logging, and configurable parameters

---

## 📁 Project Structure

```
Azure-Transaction-Analytics-Platform/
├── src/
│   ├── config.py           # Azure storage & Spark configuration
│   ├── data_loader.py      # Data ingestion from ADLS Gen2
│   ├── data_cleaner.py     # Data quality & validation logic
│   ├── analytics.py        # Business KPI computation engine
│   ├── delta_utils.py      # Delta Lake read/write/upsert operations
│   └── pipeline.py         # End-to-end orchestration
├── notebooks/              # Exploratory analysis & output screenshots
├── Images/                 # Architecture and output visuals
├── requirements.txt        # Python dependencies
├── .gitignore
└── README.md
```

---

## 📊 Data Schema

### Transaction Data (`transactions/*.csv`)

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| transaction_id | String | NOT NULL, UNIQUE | Unique transaction identifier |
| customer_id | String | NOT NULL | Customer identifier |
| product_id | String | NOT NULL, FK | Links to product catalog |
| quantity | Integer | > 0 | Units purchased |
| price | Double | > 0.0 | Unit price (USD) |
| transaction_date | Timestamp | NOT NULL | Transaction timestamp (UTC) |
| campaign_id | String | NULLABLE | Marketing campaign reference |

### Product Catalog (`products.csv`)

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| product_id | String | PK, NOT NULL | Unique product identifier |
| description | String | NOT NULL | Product description |
| category | String | NOT NULL | Product category |
| unit_price | Double | > 0.0 | Standard price (USD) |

---

## 📈 Analytics Capabilities

### Customer Intelligence
- Average order value, purchase frequency, customer lifetime value (LTV)
- Revenue segmentation and behavioral pattern analysis
- Statistical outlier detection for anomaly/fraud flagging

### Product Performance
- Top products by revenue and transaction volume
- Category-level cross comparison
- Demand trend analysis for inventory planning

### Marketing Campaign ROI
- Revenue attribution per campaign
- Customer acquisition cost tracking
- Multi-channel conversion analysis

### Data Quality Assurance
- Completeness checks (null/missing value reports)
- Referential integrity validation (transaction ↔ product joins)
- Statistical outlier scoring and correction
- Quality scorecards stored as Delta tables

---

## 🔧 Setup & Configuration

### Prerequisites

- Azure Data Lake Storage Gen2 account
- Azure Databricks Premium workspace
- Apache Spark 3.4+ with Scala 2.12
- Delta Lake 2.4.0
- Python 3.8+

### 1. Clone Repository

```bash
git clone https://github.com/Sangam919/Azure-Transaction-Analytics-Platform.git
cd Azure-Transaction-Analytics-Platform
```

### 2. Configure Azure Credentials

```bash
databricks secrets create-scope --scope azure-storage
databricks secrets put --scope azure-storage --key storage-access-key
```

Update `src/config.py` with your storage account name and container.

### 3. ADLS Data Structure

```
/transaction-data/
├── transactions/
│   ├── transaction_1.csv
│   ├── transaction_2.csv
│   └── ...
├── products.csv
└── archive/
```

### 4. Run the Pipeline

```python
# In Databricks notebook
%run /Repos/<your-username>/Azure-Transaction-Analytics-Platform/src/pipeline.py
```

---

## 🖥️ Databricks Cluster Configuration

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

## 🔍 Sample Queries

```sql
-- Top customers by revenue
SELECT customer_id, total_revenue, total_transactions
FROM analytics_db.customer_analytics
WHERE total_revenue > 1000
ORDER BY total_revenue DESC;

-- Campaign performance
SELECT campaign_id, total_revenue, unique_customers, avg_revenue_per_customer
FROM analytics_db.campaign_analytics
ORDER BY total_revenue DESC;

-- Data quality check
SELECT table_name, quality_score, issues_detected, last_updated
FROM analytics_db.data_quality_summary
ORDER BY check_timestamp DESC LIMIT 10;
```

---

## 🛠️ Future Roadmap

- **Real-time Streaming** — Apache Kafka integration for live transaction processing
- **RFM Segmentation** — Recency, Frequency, Monetary customer clustering
- **Data Governance** — Lineage tracking and Unity Catalog integration
- **Power BI Integration** — Live dashboard connectivity
- **Automated Scheduling** — Databricks Workflows for daily pipeline runs

---

## 🙌 Acknowledgments

Developed during a **Data Engineering Internship at Celebal Technologies**. Special thanks to the Data Engineering team for mentorship and guidance on enterprise-grade Azure cloud architecture.

**Project Details:**
- **Developer:** Sangam Srivastav
- **Internship:** Celebal Technologies — Data Engineering
- **Tech Stack:** Python · PySpark · Azure Databricks · ADLS Gen2 · Delta Lake · SQL

---

*Built with ❤️ during Data Engineering Internship at Celebal Technologies*
