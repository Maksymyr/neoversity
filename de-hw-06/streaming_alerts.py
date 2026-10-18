import os
import signal
import threading
from pathlib import Path

# коннектор до Kafka під Spark 4.2.0 / Scala 2.13
os.environ["PYSPARK_SUBMIT_ARGS"] = "--packages org.apache.spark:spark-sql-kafka-0-10_2.13:4.2.0 pyspark-shell"

from pyspark.sql import DataFrame, SparkSession
import pyspark.sql.functions as F
from pyspark.sql.types import DoubleType, IntegerType, StringType, StructField, StructType

from kafka_common import ALERTS_TOPIC, BUILDING_SENSORS_TOPIC, spark_kafka_options

BASE_DIR = Path(__file__).resolve().parent
CONDITIONS_PATH = BASE_DIR / "alerts_conditions.csv"
CHECKPOINT_DIR = BASE_DIR / "checkpoints"

WINDOW_DURATION = "1 minute"
SLIDE_DURATION = "30 seconds"
WATERMARK_DELAY = "10 seconds"

# -999 у файлі умов: межа не використовується
NOT_USED = -999

SENSOR_SCHEMA = StructType([
    StructField("id", IntegerType()),
    StructField("temperature", DoubleType()),
    StructField("humidity", DoubleType()),
    StructField("timestamp", StringType()),
])


def within(value: F.Column, low: F.Column, high: F.Column) -> F.Column:
    return ((low == NOT_USED) | (value >= low)) & ((high == NOT_USED) | (value <= high))


def build_alerts(averages_df: DataFrame, conditions_df: DataFrame) -> DataFrame:
    return (
        averages_df.crossJoin(conditions_df)
        .where(
            within(F.col("h_avg"), F.col("humidity_min"), F.col("humidity_max"))
            & within(F.col("t_avg"), F.col("temperature_min"), F.col("temperature_max"))
        )
        .select(
            "window",
            "t_avg",
            "h_avg",
            F.col("code").cast("string").alias("code"),
            "message",
            F.date_format(F.current_timestamp(), "yyyy-MM-dd HH:mm:ss.SSSSSS").alias("timestamp"),
        )
    )


def print_batch(conditions_df: DataFrame):
    def handler(batch_df: DataFrame, batch_id: int) -> None:
        if batch_df.isEmpty():
            return
        print(f"\n===== Batch {batch_id}: closed windows =====")
        batch_df.select(
            F.date_format("window.start", "HH:mm:ss").alias("window_start"),
            F.date_format("window.end", "HH:mm:ss").alias("window_end"),
            F.round("t_avg", 2).alias("t_avg"),
            F.round("h_avg", 2).alias("h_avg"),
        ).orderBy("window_start").show(truncate=False)

        print(f"===== Batch {batch_id}: alerts =====")
        build_alerts(batch_df, conditions_df).select(
            F.date_format("window.start", "HH:mm:ss").alias("window_start"),
            F.date_format("window.end", "HH:mm:ss").alias("window_end"),
            F.round("t_avg", 2).alias("t_avg"),
            F.round("h_avg", 2).alias("h_avg"),
            "code",
            "message",
        ).orderBy("window_start", "code").show(truncate=False)

    return handler


def main() -> None:
    spark = (
        SparkSession.builder
        .appName("SensorAlertsStreaming")
        .master("local[*]")
        .config("spark.sql.shuffle.partitions", "4")
        .config("spark.ui.showConsoleProgress", "false")
        .getOrCreate()
    )
    spark.sparkContext.setLogLevel("ERROR")
    # Ctrl+C зупиняє запити через прапорець, без трейсбеків з py4j
    stop_requested = threading.Event()
    signal.signal(signal.SIGINT, lambda signum, frame: stop_requested.set())

    # умови алертів
    conditions_df = spark.read.csv(str(CONDITIONS_PATH), header=True, inferSchema=True)

    # дані датчиків з Kafka
    readings_df = (
        spark.readStream
        .format("kafka")
        .options(**spark_kafka_options())
        .option("subscribe", BUILDING_SENSORS_TOPIC)
        .option("startingOffsets", "earliest")
        .load()
        .select(F.from_json(F.col("value").cast("string"), SENSOR_SCHEMA).alias("data"))
        .select("data.*")
        .withColumn("event_time", F.to_timestamp("timestamp"))
    )

    # середні у вікні 1 хв, крок 30 с
    averages_df = (
        readings_df
        .withWatermark("event_time", WATERMARK_DELAY)
        .groupBy(F.window("event_time", WINDOW_DURATION, SLIDE_DURATION))
        .agg(
            F.avg("temperature").alias("t_avg"),
            F.avg("humidity").alias("h_avg"),
        )
    )

    # алерти
    alerts_df = build_alerts(averages_df, conditions_df)

    # запис алертів у Kafka, ключ = code
    kafka_query = (
        alerts_df
        .select(
            F.col("code").alias("key"),
            F.to_json(F.struct("window", "t_avg", "h_avg", "code", "message", "timestamp")).alias("value"),
        )
        .writeStream
        .format("kafka")
        .options(**spark_kafka_options())
        .option("topic", ALERTS_TOPIC)
        .option("checkpointLocation", str(CHECKPOINT_DIR / "alerts_to_kafka"))
        .outputMode("append")
        .trigger(processingTime="10 seconds")
        .start()
    )

    # вивід у консоль для перевірки
    console_query = (
        averages_df.writeStream
        .foreachBatch(print_batch(conditions_df))
        .option("checkpointLocation", str(CHECKPOINT_DIR / "console"))
        .outputMode("append")
        .trigger(processingTime="10 seconds")
        .start()
    )

    print(f"Streaming '{BUILDING_SENSORS_TOPIC}' -> '{ALERTS_TOPIC}'")
    try:
        while not stop_requested.is_set() and not spark.streams.awaitAnyTermination(timeout=1):
            pass
    finally:
        kafka_query.stop()
        console_query.stop()
        spark.stop()


if __name__ == "__main__":
    main()
