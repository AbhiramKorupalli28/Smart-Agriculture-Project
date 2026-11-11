# Smart Agriculture Data Analytics Platform

Undergraduate Big Data Analytics mini case study using real Indian agriculture data, a CATCrops acquisition plan, PySpark-compatible transformations, ML experiments, and a Streamlit dashboard.

## What was executed

The local validation run ingested 49,999 Indian crop-production records and 2,200 soil/weather crop-recommendation records. It produced Parquet outputs, K-Means clustering, Random Forest classification, a yield regression experiment, metrics, figures, and an interactive dashboard entry point.

Hadoop HDFS and Apache Spark binaries were not present in the execution environment. The source includes explicit `hdfs` and `spark-submit` commands for a Hadoop/Spark host, while the local run uses pandas/scikit-learn fallbacks so no unexecuted distributed result is presented as successful.

## Quick start

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m src.pipeline --data-dir data/raw --output-dir outputs
streamlit run dashboard/app.py
```

## Distributed execution

Install Hadoop 3.3.6 and Spark on a Linux host, set `HADOOP_HOME`, `SPARK_HOME`, and `JAVA_HOME`, then run:

```bash
bash scripts/hdfs_setup.sh
spark-submit --master local[*] src/spark_job.py --input data/raw --output data/processed/spark
```

## Evidence and limitations

See `docs/dataset_inventory.md`, `docs/research_sources.md`, and `docs/validation_log.md`. CATCrops is documented as an external acquisition because its Kaggle page reports 32.49 GB and the present environment could not authenticate to download it.
