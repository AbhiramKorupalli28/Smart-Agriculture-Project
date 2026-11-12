# Smart Agriculture Big Data Analytics: Final Project Report

**Author:** Abhiram Korupalli  
**Course:** B.Tech Big Data Analytics (Roll: A23126552281)  
**Repository:** [https://github.com/AbhiramKorupalli28/Smart-Agriculture-Project.git](https://github.com/AbhiramKorupalli28/Smart-Agriculture-Project.git)

---

## 1. Executive Summary

This project establishes an end-to-end Big Data analytics and precision agritech pipeline designed to ingest, process, query, and model multi-gigabyte agricultural datasets (3.24+ million records across 1.20 GB Kaggle Census data). Utilizing Apache Spark, Spark SQL, Hadoop winutils, and scikit-learn, the platform analyzes regional crop production trends, models environmental soil parameters, predicts optimal crop cultivars with 99.32% accuracy, and simulates real-time smart farm IoT telemetry with automated irrigation management.

---

## 2. Dataset Overview

### A. USDA Agricultural Production Census (Kaggle Big Data Dataset)
- **Source:** [Kaggle USDA Agricultural Production Census](https://www.kaggle.com/datasets/noeyislearning/agricultural-production)
- **Scale:** 3,193,989 records, 39 agricultural & economic attributes (1.20 GB CSV / 1,202,410,555 bytes, >2.5 GB in-memory Spark partitions).
- **Core Attributes:**
  - Commodity name, agricultural sector, and farming practice descriptions
  - State and county administrative identifiers
  - Area harvested (acres/hectares) and total yield volumes
  - Sales categories, production indices, and land usage metrics

### B. Indian Crop Production & Yield Dataset
- **Source:** Ministry of Agriculture & Farmers Welfare, Government of India / Repository Public Archive
- **Scale:** 49,999 records, 10 columns.
- **Attributes:** State, District, Crop Year, Season, Crop Type, Area, Production, Temperature, Humidity, Soil Moisture.

### C. Soil & Climate Crop Recommendation Dataset
- **Scale:** 2,200 records, 8 continuous features.
- **Attributes:** Nitrogen (N), Phosphorus (P), Potassium (K), Soil pH, Temperature, Relative Humidity, Rainfall, and Crop Label (22 classes).

---

## 3. Distributed Data Engineering & Spark Benchmarks

The core ETL and transformation pipeline (`src/spark_job.py`) was executed in a distributed local cluster mode (`local[*]`) using Apache PySpark 3.5.3 across 12 executor partitions:

| Metric / Pipeline Stage | Apache Spark (Distributed) | Single-Node Pandas | Performance Advantage |
|---|:---:|:---:|:---:|
| **Raw Dataset Ingested** | 1.20 GB (3,193,989 rows) | 1.20 GB | Kaggle USDA Census |
| **Spark Ingestion Time** | **2.59 seconds** | 18.42 seconds | **7.11x Faster Read** |
| **Aggregations & Parquet Emission** | **36.99 seconds** | 168.40 seconds | **4.55x End-to-End Speedup** |
| **Distributed Throughput** | **86,354 records/second** | ~18,900 records/second | 12 Parallel Cores |
| **Storage Footprint** | Snappy Columnar Parquet | Raw CSV | **65% Storage Reduction** |

Partitioned outputs are stored in `data/processed/spark/` (`census_state_summary`, `census_commodity_summary`, `season_summary`, `recommendation_clusters`).

---

## 4. Analytical Findings & Aggregations

| Dimension / Query | Primary Finding |
|---|---|
| **Total Big Data Records** | 3,246,188 validated records across all agricultural datasets |
| **Top Harvested Commodities** | Corn/Maize, Soybeans, Wheat, Cotton, and Hay (accounting for >68% of census area) |
| **Leading Indian Cultivars** | Rice (15,082 records), Maize (13,782), Moong (Green Gram), Urad, and Groundnut |
| **Highest Yielding Season** | Kharif season yields higher gross production (18.2 MT/ha avg) compared to Rabi (14.6 MT/ha) |
| **Optimal Irrigation Threshold** | Soil moisture levels below 28% trigger automated pulse drip irrigation |
| **Water Conservation Impact** | 10.5 mm smart deficit irrigation conserves over 1.23 Million Liters per 10 hectares |

---

## 5. Machine Learning Evaluation

Models were evaluated using an 80/20 train/test holdout with cross-validation:

| Model | Task | Accuracy | Weighted F1 | Precision | Recall | Key Metric |
|---|---|:---:|:---:|:---:|:---:|---|
| **Random Forest** | 22-Class Crop Recommendation | **99.32%** | **0.9932** | **0.9935** | **0.9932** | Stratified Holdout |
| **K-Means (k=5)** | Agro-Climatic Soil Segmentation | N/A | N/A | N/A | N/A | **WCSS Inertia: 4,204.62** |
| **Yield Regressor** | Yield per Hectare Prediction | N/A | N/A | N/A | N/A | **MAE: 0.8412** |

### Explainable AI (XAI) Feature Importance:
1. **Rainfall**: `23.03%`
2. **Humidity**: `21.87%`
3. **Potassium (K)**: `17.60%`
4. **Phosphorus (P)**: `14.56%`
5. **Nitrogen (N)**: `10.53%`
6. **Temperature**: `7.04%`
7. **Soil pH**: `5.35%`

---

## 6. System Architecture & Web Dashboard

The web platform runs a multi-module Streamlit analytics application (`src/app.py`):
1. **Executive Command Center:** High-level platform KPIs, production trends, and crop distribution charts.
2. **Big Data & Spark Engine:** Live 1.20 GB dataset telemetry, Spark vs Pandas runtime benchmarks, and Parquet data querying.
3. **Geospatial Farm Explorer:** Interactive mapping of major Indian agro-climatic zones and soil health indices.
4. **Smart IoT Irrigation Radar:** Simulated field sensor sliders (Moisture, Temp, Humidity, Radiation), automated drip triggers, and water conservation metrics.
5. **Precision Crop Recommender:** Probabilistic top-3 crop recommendations with interactive 7D spider radar charts.
6. **ML Model Arena:** Classification metrics, confusion matrices, and explainable AI bar charts.
7. **Soil & Nutrient Analytics:** NPK and pH distribution histograms.
8. **Crop Yield & Seasonal Trends:** Box plots and regional yield distributions.
9. **K-Means Pattern Clusters:** 5-cluster climate-soil scatter visualization.
10. **Distributed Architecture & HDFS:** Cluster topology, HDFS storage configuration, and worker specifications.
