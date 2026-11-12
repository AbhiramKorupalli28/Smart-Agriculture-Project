# 🌱 Smart Agriculture Big Data Analytics Platform

[![Python](https://img.shields.io/badge/Python-3.13-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Apache Spark](https://img.shields.io/badge/Apache%20Spark-3.5-E25A1C?style=for-the-badge&logo=apachespark&logoColor=white)](https://spark.apache.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.40+-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Kaggle Dataset](https://img.shields.io/badge/Kaggle%20Dataset-1.20%20GB-20BEFF?style=for-the-badge&logo=kaggle&logoColor=white)](https://www.kaggle.com/datasets/noeyislearning/agricultural-production)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

An enterprise-grade, distributed **Big Data Analytics & Precision Agritech Platform** designed to process multi-gigabyte agricultural datasets, train explainable machine learning models, simulate IoT sensor irrigation telemetry, and deliver real-time visual insights through an interactive 10-module dashboard.

---

## 📌 Executive Architecture & Highlights

- **1.20 GB Kaggle Big Data Pipeline**: Direct distributed ingestion of the official USDA Agricultural Production Census dataset (**3,193,989 records**, 39 columns) using **Apache Spark (PySpark 3.5)** across 12 executor partitions.
- **High-Throughput Distributed Processing**: Achieved a processing speed of **86,354 records/second**, ingesting 1.20 GB in **2.59 seconds** and delivering a **4.55x speedup** over single-threaded Pandas.
- **Precision Agritech Machine Learning**:
  - **Random Forest Classifier**: **99.32% Accuracy** for multi-factor crop recommendation with full XAI (Explainable AI) feature importance ranking.
  - **Unsupervised K-Means Clustering**: Segmenting 5 agro-ecological soil/climate clusters with PySpark `VectorAssembler` and `StandardScaler`.
  - **Yield Regressor**: Evaluating regional yield per hectare across Indian agricultural states.
- **IoT Smart Farm & Irrigation Radar**: Real-time simulation of soil moisture, ambient temperature, humidity, and solar radiation to trigger automated pulse drip irrigation and calculate dynamic water conservation (1.23M+ Liters conserved).
- **Interactive 10-Module Dashboard**: Built with Streamlit, Plotly, and Folium featuring glassmorphism cards, interactive Indian geospatial explorer, 7D polar spider charts, and 4 dynamic high-contrast UI themes.

---

## 📊 Big Data Processing & Spark Benchmarks

The core data engineering pipeline (`src/spark_job.py`) runs in a distributed mode (`local[*]`) utilizing native multi-core execution and Hadoop winutils integration on Windows.

| Metric / Stage | Apache Spark (Distributed) | Single-Node Pandas | Benchmark / Speedup |
| :--- | :---: | :---: | :---: |
| **Ingested File Size** | **1.20 GB** (`1,202,410,555 bytes`) | 1.20 GB | Kaggle USDA Census CSV |
| **Record Count** | **3,193,989 rows** | 3,193,989 rows | 39 Schema Attributes |
| **Ingestion Time** | **2.59 seconds** | 18.42 seconds | **7.11x Faster Ingestion** |
| **Aggregation & Transformations** | **36.99 seconds** | 168.40 seconds | **4.55x End-to-End Speedup** |
| **Distributed Throughput** | **86,354 records/sec** | ~18,900 records/sec | 12 Parallel Worker Partitions |
| **Storage Optimization** | **Snappy Columnar Parquet** | Uncompressed CSV | **65% Disk Footprint Reduction** |

The aggregated outputs are partitioned and written directly to `data/processed/spark/` (`census_state_summary`, `census_commodity_summary`, `season_summary`, `recommendation_clusters`).

---

## 🤖 Machine Learning Model Benchmarks

| Model | Target Task | Metric | Executed Value | Validation Method |
| :--- | :--- | :--- | :---: | :--- |
| **Random Forest** | 22-Class Crop Recommendation | **Accuracy** | **99.32%** | Stratified 80/20 Holdout |
| **Random Forest** | 22-Class Crop Recommendation | **Weighted F1** | **0.9932** | Stratified 80/20 Holdout |
| **Random Forest** | 22-Class Crop Recommendation | **Precision** | **0.9935** | Stratified 80/20 Holdout |
| **Random Forest** | 22-Class Crop Recommendation | **Recall** | **0.9932** | Stratified 80/20 Holdout |
| **K-Means (k=5)** | Agro-Climatic Soil Segmentation | **Inertia (WCSS)**| **4,204.62** | Scaled 7D Vector Embeddings |
| **Yield Regressor**| Yield per Area Estimation | **MAE** | **0.8412** | 80/20 Holdout Evaluation |

### Explainable AI (XAI) Feature Importance:
1. **Rainfall**: `23.03%`
2. **Humidity**: `21.87%`
3. **Potassium (K)**: `17.60%`
4. **Phosphorus (P)**: `14.56%`
5. **Nitrogen (N)**: `10.53%`
6. **Temperature**: `7.04%`
7. **Soil pH**: `5.35%`

---

## 🖥️ Interactive Web Dashboard (10 Modules)

The platform provides an interactive analytical web interface (`dashboard/app.py`):

1. **📊 Executive Command Center**: High-level platform KPIs (3.24M records, 86k throughput, 99.32% accuracy), seasonal distribution scatter plots, and top cultivar bar charts.
2. **⚡ Big Data & Spark Engine**: In-depth telemetry on the 1.20 GB Kaggle dataset, Spark vs Pandas runtime performance comparisons, and interactive Parquet querying.
3. **🗺️ Geospatial Farm Explorer**: Interactive Asia/India map detailing major agricultural belts (Punjab, Maharashtra, Andhra Pradesh, West Bengal), production volume, and soil health indices.
4. **💧 Smart IoT Irrigation Radar**: Interactive sensor sliders (Soil Moisture, Temp, Humidity, Solar Radiation), automated irrigation triggers, pest risk index, and water conservation calculators.
5. **🎯 Precision Crop Recommender**: Probabilistic top-3 crop recommendations with confidence bars and a **7-dimensional polar Radar (Spider) chart** comparing soil parameters to optimal crop centroids.
6. **🤖 ML Model Arena**: Detailed classification metrics, feature importance charts, and held-out confusion matrix visualizations.
7. **🧪 Soil & Nutrient Analytics**: Interactive NPK, pH, and climate variable histograms across crop cultivars.
8. **📈 Crop Yield & Seasonal Trends**: Regional yield per hectare distributions and seasonal box plots.
9. **🧬 K-Means Pattern Clusters**: 5-cluster climate-soil scatter plot and mean centroid tables.
10. **🏛️ Distributed Architecture & HDFS**: Distributed system topology, multi-node configuration specs, and cluster deployment documentation.

### 🎨 Available Themes:
- `🌿 Emerald AgriTech (Vibrant Dark)` *(Default)*: Deep twilight obsidian, electric emerald green, amber highlights, glowing title gradients.
- `🌾 Golden Harvest (Amber & Slate)`: Warm golden wheat, rich amber, and fertile bronze earth tones.
- `🌌 Cyber Midnight (Neon & Blue)`: Cosmic navy blue, electric neon mint, and vibrant cyan.
- `☀️ Clean Modern Porcelain (Light)`: High-contrast porcelain, crisp slate, and forest green accents.

---

## 📂 Project Repository Structure

```
Smart-Agriculture-Project/
├── dashboard/
│   └── app.py                     # 10-Module Streamlit interactive analytics platform
├── data/
│   ├── raw/
│   │   ├── agricultural_production_census_2002.csv  # 1.20 GB Kaggle Big Data (Git-ignored)
│   │   ├── crop_prediction_india.csv               # Indian crop production dataset
│   │   └── crop_recommendation.csv                 # Soil & environmental recommendation data
│   └── processed/
│       └── spark/                 # Partitioned Snappy Parquet outputs from PySpark
├── outputs/
│   ├── figures/                   # Confusion matrix, cluster plots, feature importances
│   ├── models/                    # Trained Random Forest & K-Means pipelines (.joblib)
│   ├── tables/                    # Curated prediction tables and cluster summaries
│   ├── metrics.json               # Model validation and evaluation metrics
│   └── spark_benchmark.json       # 1.20 GB Spark execution benchmark telemetry
├── scripts/
│   ├── create_documents.py        # Generates Word (.docx), PDF (.pdf), & Excel inventory
│   └── hdfs_setup.sh              # HDFS cluster directory initialization script
├── src/
│   ├── pipeline.py                # Scikit-learn data processing and model training
│   └── spark_job.py               # Apache PySpark 1.20 GB distributed ETL & ML pipeline
├── Dataset_Inventory.xlsx         # Multi-tab dataset inventory & executed metrics
├── requirements.txt               # Python package dependencies
├── .gitignore                     # Excludes >100MB datasets & college reports
└── README.md                      # Complete project documentation
```

---

## ⚡ Quick Start: Running in VS Code

### Prerequisites
- Python 3.10 – 3.13
- Java 8/11/17 (for Apache Spark execution)
- Git

### 1. Clone & Set Up Environment
```powershell
# Clone the repository
git clone https://github.com/AbhiramKorupalli28/Smart-Agriculture-Project.git
cd Smart-Agriculture-Project

# Create and activate a virtual environment
python -m venv .venv
.venv\Scripts\activate   # On Linux/macOS: source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Run the Apache Spark Big Data Pipeline
```powershell
# Executes distributed ingestion and Parquet generation across 12 partitions
python src/spark_job.py
```

### 3. Launch the Interactive Web Dashboard
```powershell
# Starts the Streamlit dashboard on http://localhost:8501
streamlit run dashboard/app.py
```
Open **[http://localhost:8501](http://localhost:8501)** in your web browser.

### 4. Regenerate Project Documents (Word, PDF, Excel)
```powershell
python scripts/create_documents.py
```

---

## 📜 Citations & References

1. **Abhishek Kandoi**, *Crop Yield Prediction based on Indian Agriculture Dataset*, GitHub.
2. **USDA / Kaggle**, *Agricultural Production Census Dataset (1.20 GB, 3.19M Records)*, Kaggle Datasets.
3. **IRTA Remote Sensing**, *CATCrops: Sentinel-2 Multi-spectral Time Series Dataset*, Kaggle.
4. **Tata-Cornell Institute (TCI) & ICRISAT**, *District-Level Database for Indian Agriculture and Allied Sectors (1966–2020)*.
5. **Directorate of Economics and Statistics (DES)**, *Area, Production and Yield (APY) Reports*, Ministry of Agriculture & Farmers Welfare, Govt. of India.
6. **Apache Spark Documentation**, *PySpark and MLlib Distributed Processing Guide*, Apache Software Foundation.
7. **Scikit-Learn Documentation**, *Random Forest Classifier & Regressor User Guide*.
8. **Streamlit Documentation**, *Interactive Data Applications and Dashboard Framework*.

---

## 📄 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
