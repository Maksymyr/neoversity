from datetime import datetime
from pathlib import Path

from airflow import DAG
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator

# Spark-скрипти лежать поруч з цим файлом
DAGS_DIR = Path(__file__).resolve().parent

# обмеження ресурсів Spark
SPARK_CONF = {
    "spark.driver.memory": "768m",
    "spark.sql.shuffle.partitions": "8",
}

with DAG(
    dag_id="project_solution",
    start_date=datetime(2026, 11, 1),
    schedule=None,
    catchup=False,
    tags=["maksym_popov"],
) as dag:

    landing_to_bronze = SparkSubmitOperator(
        task_id="landing_to_bronze",
        application=str(DAGS_DIR / "landing_to_bronze.py"),
        conn_id="spark-default",
        conf=SPARK_CONF,
        verbose=1,
    )

    bronze_to_silver = SparkSubmitOperator(
        task_id="bronze_to_silver",
        application=str(DAGS_DIR / "bronze_to_silver.py"),
        conn_id="spark-default",
        conf=SPARK_CONF,
        verbose=1,
    )

    silver_to_gold = SparkSubmitOperator(
        task_id="silver_to_gold",
        application=str(DAGS_DIR / "silver_to_gold.py"),
        conn_id="spark-default",
        conf=SPARK_CONF,
        verbose=1,
    )

    landing_to_bronze >> bronze_to_silver >> silver_to_gold
