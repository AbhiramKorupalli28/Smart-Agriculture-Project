# Validation Log

## 1. Environment & Runtime Validation
- **Operating System**: Windows 11 64-bit
- **Python Version**: Python 3.13.x
- **Java Runtime**: OpenJDK 21
- **Hadoop Environment**: Hadoop winutils 3.3.0 (`HADOOP_HOME=C:\Users\ABHIRAM\hadoop`)
- **Apache Spark**: PySpark 3.5.3 (Multi-thread Local Cluster `local[*]`)
- **UI Framework**: Streamlit 1.40.1

---

## 2. Big Data Distributed Execution (Apache Spark)
- **Script**: `src/spark_job.py`
- **Source Dataset**: `data/raw/agricultural_production_census_2002.csv` (1.20 GB / 1,202,410,555 bytes) downloaded directly from Kaggle.
- **Ingestion Telemetry**:
  - Partition count: 12 distributed workers
  - Spark Read Time: 2.59 seconds
  - Aggregation & Parquet Emission: 36.99 seconds
  - Distributed Throughput: 86,354 records/second
- **Parquet Outputs**:
  - `data/processed/spark/census_state_summary/`
  - `data/processed/spark/census_commodity_summary/`
  - `data/processed/spark/season_summary/`
  - `data/processed/spark/recommendation_clusters/`
- **Benchmark Artifact**: Saved to `outputs/spark_benchmark.json`.

---

## 3. Machine Learning Evaluation
- **Random Forest 22-Class Crop Recommendation**:
  - Accuracy: `99.32%`
  - Weighted F1 Score: `0.9932`
  - Weighted Precision: `0.9935`
  - Weighted Recall: `0.9932`
  - Feature Importance: Rainfall (23.03%), Humidity (21.87%), Potassium (17.60%), Phosphorus (14.56%), Nitrogen (10.53%), Temperature (7.04%), Soil pH (5.35%).
- **Unsupervised K-Means Clustering**:
  - k = 5 agro-climatic clusters
  - WCSS Inertia: `4,204.62`
- **Yield Regressor**:
  - MAE: `0.8412`

---

## 4. Web Application Validation
- **Command**: `streamlit run dashboard/app.py --server.port 8501`
- **Status**: Live on `http://localhost:8501`
- **Modules Verified**:
  1. Executive Command Center Overview
  2. Big Data & Spark Engine Benchmarks
  3. Geospatial Farm Explorer (India agro-climatic map)
  4. Smart IoT Irrigation Radar (real-time telemetry)
  5. Precision Crop Recommender (7D Spider Radar profile)
  6. ML Model Evaluation Arena
  7. Soil & Nutrient Analytics
  8. Crop Yield & Seasonal Trends
  9. K-Means Pattern Clusters
  10. Distributed Architecture & HDFS
- **Visual Themes**: Verified with 4 themes: Emerald AgriTech (Default), Golden Harvest, Cyber Midnight, and Clean Modern Porcelain.
