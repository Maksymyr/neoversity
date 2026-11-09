import re
from pathlib import Path

from pyspark.sql import SparkSession
from pyspark.sql.functions import udf
from pyspark.sql.types import StringType

BASE_DIR = Path(__file__).resolve().parent
TABLES = ["athlete_bio", "athlete_event_results"]


def clean_text(text: str | None) -> str | None:
    # None лишаємо як є, інакше str(None) дасть рядок "None"
    if text is None:
        return None
    return re.sub(r'[^a-zA-Z0-9,.\\"\']', '', str(text))


clean_text_udf = udf(clean_text, StringType())


def main() -> None:
    spark = SparkSession.builder.appName("BronzeToSilver").getOrCreate()

    for table in TABLES:
        df = spark.read.parquet(str(BASE_DIR / "bronze" / table))

        text_columns = [name for name, dtype in df.dtypes if dtype == "string"]
        for col_name in text_columns:
            df = df.withColumn(col_name, clean_text_udf(df[col_name]))

        df = df.dropDuplicates()
        df.write.mode("overwrite").parquet(str(BASE_DIR / "silver" / table))

        # показуємо записану таблицю, без повторного UDF
        silver_df = spark.read.parquet(str(BASE_DIR / "silver" / table))
        print(f"silver/{table}: {silver_df.count()} rows, cleaned columns: {text_columns}")
        silver_df.show()

    spark.stop()


if __name__ == "__main__":
    main()
