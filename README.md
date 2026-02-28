# 🚀 Azure Transaction Analytics Platform

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Apache Spark](https://img.shields.io/badge/Apache%20Spark-3.4+-orange.svg)](https://spark.apache.org/)
[![Delta Lake](https://img.shields.io/badge/Delta%20Lake-2.4.0+-green.svg)](https://delta.io/)
[![Azure](https://img.shields.io/badge/Azure-Data%20Lake%20Gen2-blue.svg)](https://azure.microsoft.com/en-us/services/storage/data-lake-storage/)

A powerful data engineering pipeline for analyzing multi-channel transaction data (web, mobile, in-store) using Azure Databricks, Delta Lake, and Azure Data Lake Storage Gen2. This project was developed as part of a Data Engineering Internship at **Celebal Technologies**, tackling real-world big data challenges and delivering actionable business insights. 

## 🌟 Project Overview

This platform was designed to address complex data engineering challenges in multi-channel retail analytics. Built during my internship at Celebal Technologies, this solution demonstrates enterprise-grade data processing capabilities using modern cloud technologies. The pipeline processes large-scale transaction data, delivering actionable insights for businesses through scalable Apache Spark and Delta Lake architecture.

## ✨ Key Features

* **Multi-Channel Analytics**: Combines web, mobile, and in-store data seamlessly
* **Actionable Business Insights**: Tracks customer spending patterns, top-performing products, and marketing campaign ROI
* **Enterprise Data Quality**: Advanced validation with missing value detection and outlier analysis
* **Scalable Cloud Processing**: Leverages Spark's distributed computing for big data workloads
* **Delta Lake Integration**: ACID transactions, time travel, and optimized storage performance
* **Production-Ready Code**: Modular, maintainable Python architecture with comprehensive error handling
* **Real-time Analytics**: Fast query performance for business intelligence dashboards

## 🏗️ Solution Architecture

```
┌──────────────┐    ┌──────────────┐    ┌─────────────────┐    ┌──────────────┐
│ Data Sources │───▶│ ADLS Gen2    │───▶│ Azure Databricks │───▶│ Delta Tables │
│ • Web        │    │ • Raw CSV    │    │ • Data Pipeline │    │ • Analytics  │
│ • Mobile     │    │ • Staging    │    │ • ML Processing │    │ • Insights   │
│ • In-Store   │    │ • Archive    │    │ • Quality Checks│    │ • Reports    │
└──────────────┘    └──────────────┘    └─────────────────┘    └──────────────┘
```

## 📋 Prerequisites

### Azure Cloud Environment:
* Azure Data Lake Storage Gen2 account
* Azure Databricks premium workspace
* Proper IAM roles and permissions

### Databricks Cluster Configuration:
* Apache Spark 3.4+ with Scala 2.12
* Delta Lake 2.4.0 (io.delta:delta-core_2.12:2.4.0)
* Python 3.8+ runtime
* Optimized cluster sizing for workload

### Data Lake Setup:
* Configured secret scope: `azure-storage` with `storage-access-key`
* Structured data directory: `transactions/*.csv` and `products.csv`
* Proper data governance and access controls

## 🚀 Quick Start Guide

### 1. Repository Setup

```bash
git clone https://github.com/Sangam919/Final-Project-Pyspark-problem-statement-.git
cd azure-transaction-analytics
```

### 2. Azure Authentication

Configure Databricks secret scope for secure ADLS access:

```bash
databricks secrets create-scope --scope azure-storage
databricks secrets put --scope azure-storage --key storage-access-key
```

Update `src/config.py` with your Azure storage account details (default: mydatalake2004, transaction-data).

### 3. Data Preparation

Ensure your ADLS Gen2 container follows this structure:

```
/transaction-data/
├── transactions/
│   ├── transaction_1.csv
│   ├── transaction_2.csv
│   ├── transaction_3.csv
│   └── ...
├── products.csv
└── archive/
```

### 4. Pipeline Deployment

1. Import repository to Databricks using Repos feature
2. Create and configure your cluster (see Configuration section)
3. Execute the complete pipeline:

```python
%run /Repos/<your-username>/azure-transaction-analytics/src/pipeline.py
```

## 📊 Comprehensive Data Schema

### Transaction Data (transactions/*.csv)

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| transaction_id | String | NOT NULL, UNIQUE | Unique transaction identifier |
| customer_id | String | NOT NULL | Customer identifier for analytics |
| product_id | String | NOT NULL, FK | Links to products table |
| quantity | Integer | > 0 | Number of units purchased |
| price | Double | > 0.0 | Unit price in USD |
| transaction_date | Timestamp | NOT NULL | Transaction timestamp (UTC) |
| campaign_id | String | NULLABLE | Marketing campaign reference |

### Product Catalog (products.csv)

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| product_id | String | NOT NULL, UNIQUE, PK | Unique product identifier |
| description | String | NOT NULL | Detailed product description |
| category | String | NOT NULL | Product category classification |
| unit_price | Double | > 0.0 | Standard unit price in USD |

## 🔧 Advanced Configuration

### Production Databricks Cluster

```json
{
  "cluster_name": "celebal-analytics-cluster",
  "spark_version": "14.3.x-scala2.12",
  "node_type_id": "Standard_DS3_v2",
  "num_workers": 4,
  "autoscale": {
    "min_workers": 2,
    "max_workers": 8
  },
  "spark_conf": {
    "spark.jars.packages": "io.delta:delta-core_2.12:2.4.0",
    "spark.sql.extensions": "io.delta.sql.DeltaSparkSessionExtension",
    "spark.sql.catalog.spark_catalog": "org.apache.spark.sql.delta.catalog.DeltaCatalog",
    "spark.databricks.delta.preview.enabled": "true"
  },
  "init_scripts": []
}
```

### Enterprise Project Structure

```
azure-transaction-analytics/
├── src/                          # Core application code
│   ├── __init__.py              # Package initialization
│   ├── config.py                # Azure connection configuration
│   ├── data_loader.py           # Data ingestion module
│   ├── data_cleaner.py          # Data quality and validation
│   ├── analytics.py             # Business intelligence engine
│   ├── delta_utils.py           # Delta Lake operations
│   └── pipeline.py              # Main orchestration pipeline
├── tests/                       # Unit and integration tests
├── docs/                        # Technical documentation
├── notebooks/                   # Exploration and analysis
├── README.md                    # Project documentation
├── requirements.txt             # Python dependencies
├── .gitignore                   # Version control exclusions
└── LICENSE                      # MIT license
```

## 📈 Advanced Analytics Capabilities

### Customer Intelligence:
* **Behavioral Analytics**: Average order value, purchase frequency, customer lifetime value
* **Revenue Analytics**: Total revenue tracking, transaction volume analysis
* **Anomaly Detection**: Statistical outlier identification for fraud detection
* **Segmentation**: Customer clustering based on spending patterns

### Product Performance:
* **Sales Analytics**: Top-performing products by volume and revenue
* **Category Intelligence**: Cross-category performance comparison
* **Inventory Insights**: Product demand forecasting support
* **Pricing Analytics**: Price elasticity and optimization insights

### Marketing Campaign ROI:
* **Campaign Performance**: Revenue attribution, customer acquisition cost
* **Channel Analytics**: Multi-channel conversion tracking
* **Customer Journey**: Campaign touchpoint analysis
* **Performance Benchmarking**: Campaign comparison and optimization

### Data Quality Assurance:
* **Completeness Checks**: Comprehensive null value analysis
* **Consistency Validation**: Cross-table referential integrity
* **Accuracy Metrics**: Statistical outlier detection and correction
* **Reliability Reports**: Data quality scorecards and trending

## 🏃‍♂️ Production Deployment

### Pipeline Execution

Execute in Databricks production environment:

```python
# Main pipeline execution
%run /Repos/<your-repo>/src/pipeline.py

# Verify data quality
%sql
SELECT * FROM analytics_db.data_quality_summary 
ORDER BY check_timestamp DESC LIMIT 10;

# Review analytics results
%sql
SELECT * FROM analytics_db.customer_analytics 
WHERE total_revenue > 1000 
ORDER BY total_revenue DESC;
```

### Performance Monitoring

```sql
-- Campaign performance dashboard
SELECT 
  campaign_id,
  total_revenue,
  total_transactions,
  unique_customers,
  avg_revenue_per_customer
FROM analytics_db.campaign_analytics
ORDER BY total_revenue DESC;

-- Data quality monitoring
SELECT 
  table_name,
  quality_score,
  issues_detected,
  last_updated
FROM analytics_db.data_quality_summary;
```

## 🛠️ Future Enhancement Roadmap

### Phase 1 - Advanced Analytics:
* **Machine Learning Integration**: Predictive analytics for customer churn and lifetime value
* **Real-time Streaming**: Apache Kafka integration for live transaction processing
* **Advanced Segmentation**: RFM analysis and behavioral clustering algorithms

### Phase 2 - Operational Excellence:
* **MLOps Pipeline**: Automated model training and deployment workflows
* **Data Governance**: Comprehensive data lineage and catalog integration
* **Performance Optimization**: Query optimization and cost management strategies

### Phase 3 - Enterprise Features:
* **Multi-tenant Architecture**: Support for multiple business units
* **Advanced Visualization**: Integration with Power BI and Tableau
* **Automated Reporting**: Scheduled insights delivery and alerting systems

## 🙌 Acknowledgments

I would like to express my heartfelt gratitude to **Celebal Technologies** for providing me with this incredible opportunity to work on cutting-edge data engineering challenges during my internship. This project represents the culmination of intensive learning and hands-on experience with enterprise-grade cloud technologies.

**Special thanks to:**
- The Celebal Technologies Data Engineering team for their mentorship and guidance
- My project supervisors for their continuous support and technical insights
- The company's commitment to fostering innovation and professional growth in emerging technologies

This internship experience at Celebal Technologies has been instrumental in developing my expertise in Azure cloud technologies, big data processing, and enterprise data architecture patterns.

**Project Details:**
- **Intern**: Sangam Srivastav
- **Company**: Celebal Technologies
- **Program**: Data Engineering Internship
- **Tech Stack**: Apache Spark, Delta Lake, Azure Databricks, Python
- **Focus Areas**: Big Data Processing, Cloud Analytics, Data Quality Engineering


*Developed with ❤️ during Data Engineering Internship at Celebal Technologies*
