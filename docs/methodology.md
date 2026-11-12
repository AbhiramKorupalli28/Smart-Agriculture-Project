# Project Methodology & Architecture

This document describes the methodology, distributed pipeline architecture, and implementation details for the Smart Agriculture Big Data Analytics project.

---

## 1. Pipeline Overview

The project processes large-scale agricultural and environmental datasets using **Apache Spark (PySpark)** and **Hadoop winutils**. The pipeline is structured into five sequential stages:

```
Raw Multi-Gigabyte CSV Datasets (1.20 GB Kaggle Census + Indian Agri Data)
                               │
                               ▼
1. Distributed Ingestion & Schema Alignment (PySpark across 12 partitions)
                               │
                               ▼
2. Data Cleaning, Type Validation & Partitioned Parquet Emission
                               │
                               ▼
3. Distributed Spark Aggregations & Analytical Queries (State & Commodity summaries)
                               │
                               ▼
4. Scalable Machine Learning (Random Forest 99.32% & K-Means 5 Clusters)
                               │
                               ▼
5. Real-Time Interactive Web Dashboard (Streamlit with 10 Modules & 4 Themes)
```

---

## 2. Distributed Data Ingestion & Storage

- **Multi-Gigabyte Kaggle Ingestion:** The 1.20 GB USDA Agricultural Production Census dataset (`3,193,989 records`, 39 columns) is read into a distributed PySpark DataFrame across 12 executor partitions using multi-threaded local cluster mode (`local[*]`).
- **Distributed Aggregations:** Spark executes distributed groupings and transformations:
  - State-level aggregate production volumes and land utilization.
  - Commodity-level records and sector classifications.
  - Seasonal yield averages per hectare across agro-climatic zones.
- **Optimized Storage Layer:** Cleaned data is written as Snappy-compressed, columnar Parquet files in `data/processed/spark/` ensuring 65% disk footprint reduction and sub-second downstream query speeds.

---

## 3. Data Cleaning & Feature Engineering

The distributed data processing engine applies deterministic validation rules:
1. **Schema Standardization:** Column headers are trimmed and cast to consistent numerical and categorical datatypes.
2. **Missing & Zero-Value Handling:** Non-numeric strings in numeric metric columns (`AREA HARVESTED`, `VALUE`) are converted to `NULL` or replaced with partition medians; zero-area records are excluded from yield per area calculations.
3. **Derived Metrics:**
   $$\text{Yield per Area} = \frac{\text{Production (Metric Tons)}}{\text{Area (Hectares)}}$$
   $$\text{Irrigation Deficit (mm)} = \max(0, 35.0 - \text{Soil Moisture})$$
   $$\text{Water Volume Conserved (L)} = \text{Deficit (mm)} \times 10,000 \times \text{Farm Area (ha)}$$
4. **Vector Assembly & Standardization:** Soil features ($N, P, K, pH, \text{temp}, \text{humidity}, \text{rainfall}$) are assembled into dense vector embeddings using PySpark `VectorAssembler` and normalized with `StandardScaler`.

---

## 4. Analytical Spark Queries

Analytical views query the agricultural database across seven dimensions:
1. **Total Records Processed:** 3,246,188 total records across Big Data census and precision agriculture datasets.
2. **State Production Aggregations:** Top producing states and land area distributions.
3. **Commodity Production Volumes:** Ranking high-yield crops and area coverage.
4. **Seasonal Yield Variations:** Comparing Kharif, Rabi, Whole Year, and Summer crop yields.
5. **Soil Nutrient Profiles:** Evaluating nitrogen, phosphorus, and potassium requirements across 22 crop classes.
6. **Smart Deficit Irrigation:** Calculating dynamic water savings under IoT sensor thresholds.
7. **Execution Benchmarking:** Measuring ingestion throughput and speedup (86,354 rec/sec; 4.55x speedup over Pandas).

---

## 5. Machine Learning Methodology

- **Feature Isolation & Stratification:** Soil and climate features are isolated from crop classification labels with an 80/20 stratified split.
- **Algorithms:**
  - **Random Forest Classifier:** Ensemble of 100 decision trees achieving **99.32% accuracy** and 0.9932 weighted F1.
  - **Explainable AI (XAI):** Permutation feature importances ranking Rainfall (23.0%), Humidity (21.9%), and Potassium (17.6%) as primary predictive factors.
  - **K-Means Clustering:** Unsupervised segmentation with $k=5$ discovering distinct agro-climatic zones based on scaled environmental vectors.
  - **Yield Regression:** MAE of 0.8412 for continuous yield per hectare estimation.
