import pyspark.sql.functions as F

from common import INPUT_TOPIC, SOURCE_DB, create_spark, jdbc_options, kafka_options


def main() -> None:
    spark = create_spark("MySqlToKafka")

    # Етап 3, частина 1: читання athlete_event_results з MySQL
    results_df = spark.read.format("jdbc").options(**jdbc_options(SOURCE_DB, "athlete_event_results")).load().distinct()

    # Етап 3, частина 2: запис у Kafka-топік, кожен рядок як JSON
    (
        results_df
        .select(
            F.col("athlete_id").cast("string").alias("key"),
            F.to_json(F.struct(*results_df.columns)).alias("value"),
        )
        .write
        .format("kafka")
        .options(**kafka_options())
        .option("topic", INPUT_TOPIC)
        .save()
    )
    print(f"Written to topic '{INPUT_TOPIC}'")

    spark.stop()


if __name__ == "__main__":
    main()
