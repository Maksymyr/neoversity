from pathlib import Path

from pyspark.sql import SparkSession
import pyspark.sql.functions as F

BASE_DIR = Path(__file__).resolve().parent


def main() -> None:
    spark = SparkSession.builder.appName("SilverToGold").getOrCreate()

    bio_df = spark.read.parquet(str(BASE_DIR / "silver" / "athlete_bio"))
    results_df = spark.read.parquet(str(BASE_DIR / "silver" / "athlete_event_results"))

    # вага й зріст до числа, try_cast дає NULL замість помилки
    # вага понад 300 це склеєні діапазони ("100-104" -> "100104")
    bio_df = (
        bio_df
        .withColumn("height", F.expr("try_cast(height AS DOUBLE)"))
        .withColumn("weight", F.expr("try_cast(weight AS DOUBLE)"))
        .where(F.col("height").isNotNull() & F.col("weight").isNotNull() & (F.col("weight") <= 300))
        .select("athlete_id", "sex", "country_noc", "height", "weight")
    )

    # country_noc з athlete_bio, країна походження
    gold_df = (
        results_df.drop("country_noc")
        .join(bio_df, "athlete_id")
        .groupBy("sport", "medal", "sex", "country_noc")
        .agg(
            F.avg("height").alias("avg_height"),
            F.avg("weight").alias("avg_weight"),
        )
        .withColumn("timestamp", F.current_timestamp())
    )

    gold_df.write.mode("overwrite").parquet(str(BASE_DIR / "gold" / "avg_stats"))

    gold_df = spark.read.parquet(str(BASE_DIR / "gold" / "avg_stats"))
    print(f"gold/avg_stats: {gold_df.count()} rows")
    gold_df.show()

    spark.stop()


if __name__ == "__main__":
    main()
