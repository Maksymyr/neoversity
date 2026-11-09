import os

# пакети для JDBC і Kafka, мають бути задані до створення SparkSession
os.environ["PYSPARK_SUBMIT_ARGS"] = (
    "--packages com.mysql:mysql-connector-j:8.0.32,"
    "org.apache.spark:spark-sql-kafka-0-10_2.13:4.2.0 pyspark-shell"
)

from pyspark.sql import SparkSession

from configs import kafka_config, mysql_config

MY_NAME = "maksym_popov"

INPUT_TOPIC = f"{MY_NAME}_athlete_event_results"
OUTPUT_TOPIC = f"{MY_NAME}_athlete_enriched_agg"

SOURCE_DB = "olympic_dataset"
TARGET_DB = "neo_data"
TARGET_TABLE = f"{MY_NAME}_athlete_enriched_agg"


def create_spark(app_name: str) -> SparkSession:
    spark = (
        SparkSession.builder
        .appName(app_name)
        .master("local[*]")
        .config("spark.sql.shuffle.partitions", "8")
        .config("spark.ui.showConsoleProgress", "false")
        .getOrCreate()
    )
    spark.sparkContext.setLogLevel("ERROR")
    return spark


def jdbc_options(database: str, table: str) -> dict[str, str]:
    return {
        "url": f"jdbc:mysql://{mysql_config['host']}:{mysql_config['port']}/{database}",
        "driver": "com.mysql.cj.jdbc.Driver",
        "dbtable": table,
        "user": mysql_config["user"],
        "password": mysql_config["password"],
    }


def kafka_options() -> dict[str, str]:
    jaas = (
        "org.apache.kafka.common.security.plain.PlainLoginModule required "
        f'username="{kafka_config["username"]}" password="{kafka_config["password"]}";'
    )
    return {
        "kafka.bootstrap.servers": ",".join(kafka_config["bootstrap_servers"]),
        "kafka.security.protocol": kafka_config["security_protocol"],
        "kafka.sasl.mechanism": kafka_config["sasl_mechanism"],
        "kafka.sasl.jaas.config": jaas,
    }


def kafka_python_params() -> dict:
    return {
        "bootstrap_servers": kafka_config["bootstrap_servers"],
        "security_protocol": kafka_config["security_protocol"],
        "sasl_mechanism": kafka_config["sasl_mechanism"],
        "sasl_plain_username": kafka_config["username"],
        "sasl_plain_password": kafka_config["password"],
    }
