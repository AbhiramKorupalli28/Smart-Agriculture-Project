# Validation log

The local pipeline was executed with Python and scikit-learn against the two copied public CSV files. It creates Parquet where `pyarrow` is available, CSV fallback otherwise, and writes `outputs/metrics.json` plus PNG figures.

The environment inspection found Python 3.12.3, OpenJDK 21, and LibreOffice. `hdfs` and `spark-submit` were not on PATH. Therefore HDFS operations and Spark MLlib execution were not claimed as completed. `src/spark_job.py` and `scripts/hdfs_setup.sh` are runnable on a Hadoop 3.3.6/Spark host.

Dashboard validation can be performed with:

```bash
streamlit run dashboard/app.py
```

Troubleshooting:

- If `pyspark` cannot start under Java 21, use a supported Java runtime such as Java 8/11/17 for the selected Spark distribution.
- If Parquet support is unavailable, install `pyarrow`; the local pipeline emits CSV fallback files.
- If the dashboard is opened before the pipeline, execute `python -m src.pipeline` first so metrics, models, and figures exist.
