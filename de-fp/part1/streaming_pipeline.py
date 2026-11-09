import signal
import threading

from pyspark.sql import DataFrame
import pyspark.sql.functions as F
from pyspark.sql.types import IntegerType, LongType, StringType, StructField, StructType

from common import (
    INPUT_TOPIC,
    OUTPUT_TOPIC,
    SOURCE_DB,
    TARGET_DB,
    TARGET_TABLE,
    create_spark,
    jdbc_options,
    kafka_options,
)

CHECKPOINT_DIR = "checkpoints/streaming_pipeline"

RESULTS_SCHEMA = StructType([
    StructField("edition", StringType()),
    StructField("edition_id", IntegerType()),
    StructField("country_noc", StringType()),
    StructField("sport", StringType()),
    StructField("event", StringType()),
    StructField("result_id", LongType()),
    StructField("athlete", StringType()),
    StructField("athlete_id", IntegerType()),
    StructField("pos", StringType()),
    StructField("medal", StringType()),
    StructField("isTeamSport", StringType()),
])


def write_batch(batch_df: DataFrame, batch_id: int) -> None:
    if batch_df.isEmpty():
        return
    batch_df = batch_df.withColumn("timestamp", F.current_timestamp())
    batch_df.persist()

    # Етап 6.а): запис у вихідний Kafka-топік
    (
        batch_df
        .select(F.to_json(F.struct(*batch_df.columns)).alias("value"))
        .write
        .format("kafka")
        .options(**kafka_options())
        .option("topic", OUTPUT_TOPIC)
        .save()
    )

    # Етап 6.b): запис у базу даних
    (
        batch_df.write
        .format("jdbc")
        .options(**jdbc_options(TARGET_DB, TARGET_TABLE))
        .mode("append")
        .save()
    )

    print(f"Batch {batch_id}: {batch_df.count()} rows written to Kafka and MySQL")
    batch_df.unpersist()


def main() -> None:
    spark = create_spark("AthleteStreamingPipeline")

    # Етап 1: читання фізичних показників атлетів з MySQL
    bio_df = spark.read.format("jdbc").options(**jdbc_options(SOURCE_DB, "athlete_bio")).load()

    # Етап 2: лишаємо атлетів, у яких зріст і вага є числами
    # 'nan' дає NaN, а не NULL
    # вага понад 300 це склеєні діапазони ("210-218" -> "210218")
    bio_df = (
        bio_df
        .withColumn("height", F.expr("try_cast(height AS DOUBLE)"))
        .withColumn("weight", F.expr("try_cast(weight AS DOUBLE)"))
        .where(
            F.col("height").isNotNull() & ~F.isnan("height")
            & F.col("weight").isNotNull() & ~F.isnan("weight")
            & (F.col("weight") <= 300)
        )
        .select("athlete_id", "sex", "country_noc", "height", "weight")
    )

    # Етап 3, частина 3: читання результатів змагань з Kafka-топіку і розбір JSON у колонки
    results_df = (
        spark.readStream
        .format("kafka")
        .options(**kafka_options())
        .option("subscribe", INPUT_TOPIC)
        .option("startingOffsets", "earliest")
        .option("maxOffsetsPerTrigger", "100000")
        .load()
        .select(F.from_json(F.col("value").cast("string"), RESULTS_SCHEMA).alias("data"))
        .select("data.*")
    )

    # Етап 4: об'єднання з біологічними даними за athlete_id
    # country_noc з athlete_bio, країна походження
    enriched_df = results_df.drop("country_noc").join(bio_df, "athlete_id", "inner")

    # Етап 5: середній зріст і вага для кожного виду спорту, медалі, статі й країни
    agg_df = (
        enriched_df
        .groupBy("sport", "medal", "sex", "country_noc")
        .agg(
            F.avg("height").alias("avg_height"),
            F.avg("weight").alias("avg_weight"),
        )
    )
    # timestamp додаю у write_batch

    # Етап 6: стрим через forEachBatch у Kafka-топік і базу даних
    query = (
        agg_df.writeStream
        .foreachBatch(write_batch)
        .outputMode("update")
        .option("checkpointLocation", CHECKPOINT_DIR)
        .trigger(processingTime="10 seconds")
        .start()
    )

    # Ctrl+C зупиняє запит через прапорець
    stop_requested = threading.Event()
    signal.signal(signal.SIGINT, lambda signum, frame: stop_requested.set())
    print(f"Streaming '{INPUT_TOPIC}' -> '{OUTPUT_TOPIC}' and {TARGET_DB}.{TARGET_TABLE}")
    try:
        while not stop_requested.is_set():
            if spark.streams.awaitAnyTermination(timeout=1):
                break
    finally:
        query.stop()
        spark.stop()


if __name__ == "__main__":
    main()
