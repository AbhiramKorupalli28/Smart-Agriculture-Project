#!/usr/bin/env bash
set -euo pipefail
: "${HADOOP_HOME:?Set HADOOP_HOME to Hadoop 3.3.6}"
export PATH="$HADOOP_HOME/bin:$HADOOP_HOME/sbin:$PATH"
hdfs namenode -format -force
start-dfs.sh
hdfs dfs -mkdir -p /smart-agri/raw /smart-agri/processed
hdfs dfs -put -f data/raw/*.csv /smart-agri/raw/
hdfs dfs -ls -h /smart-agri/raw
