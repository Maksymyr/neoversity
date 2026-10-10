from functools import reduce
from operator import or_
from pathlib import Path

from pyspark.sql import DataFrame, SparkSession
import pyspark.sql.functions as F

DATA_DIR = Path(__file__).resolve().parent / "data"
TABLES = ["users", "purchases", "products"]

AGE_FROM, AGE_TO = 18, 25


def header(title: str) -> None:
    print(f"\n=== {title} ===")


def read_csv(spark: SparkSession, name: str) -> DataFrame:
    return spark.read.csv(str(DATA_DIR / f"{name}.csv"), header=True, inferSchema=True)


def main() -> None:
    # Створюємо сесію Spark
    spark = SparkSession.builder.appName("GoitDeHw03").getOrCreate()
    spark.sparkContext.setLogLevel("ERROR")

    # 1. Завантажуємо кожен CSV-файл як окремий DataFrame
    header("p1. Завантаження даних")
    raw = {name: read_csv(spark, name) for name in TABLES}
    for name, df in raw.items():
        print(f"{name}: {df.count()} рядків")
        df.printSchema()
        df.show(5)

    # 2. Очищаємо дані: видаляємо рядки, у яких є хоча б одне пропущене значення
    header("p2. Очищення від пропущених значень")
    clean = {name: df.dropna() for name, df in raw.items()}
    for name, df in raw.items():
        print(f"{name}: {df.count()} -> {clean[name].count()} рядків")

    for name, df in raw.items():
        has_null = reduce(or_, [F.col(c).isNull() for c in df.columns])
        print(f"Видалені рядки {name}:")
        df.where(has_null).show()

    users_df, purchases_df, products_df = clean["users"], clean["purchases"], clean["products"]

    # Сума кожної покупки = кількість одиниць × ціна одиниці товару
    purchases_amount_df = purchases_df \
        .join(products_df, "product_id", "inner") \
        .withColumn("purchase_amount", F.col("quantity") * F.col("price"))

    # 3. Загальна сума покупок за кожною категорією продуктів
    header("p3. Загальна сума покупок за категоріями")
    purchases_amount_df \
        .groupBy("category") \
        .agg(F.round(F.sum("purchase_amount"), 2).alias("total_amount")) \
        .orderBy(F.col("total_amount").desc()) \
        .show()

    # 4. Сума покупок за категоріями для вікової категорії 18–25 включно
    header(f"p4. Сума покупок за категоріями, вік {AGE_FROM}–{AGE_TO}")
    young_by_category_df = purchases_amount_df \
        .join(users_df, "user_id", "inner") \
        .where(F.col("age").between(AGE_FROM, AGE_TO)) \
        .groupBy("category") \
        .agg(F.sum("purchase_amount").alias("total_amount"))

    young_by_category_df \
        .withColumn("total_amount", F.round("total_amount", 2)) \
        .orderBy(F.col("total_amount").desc()) \
        .show()

    # 5. Частка кожної категорії від сумарних витрат вікової категорії 18–25
    header(f"p5. Частка категорій у витратах, вік {AGE_FROM}–{AGE_TO}")
    young_total = young_by_category_df.agg(F.sum("total_amount")).collect()[0][0]
    print(f"Сумарні витрати у віці {AGE_FROM}–{AGE_TO}: {young_total:.2f}")

    young_share_df = young_by_category_df \
        .withColumn("percentage", F.round(F.col("total_amount") / F.lit(young_total) * 100, 2)) \
        .withColumn("total_amount", F.round("total_amount", 2)) \
        .orderBy(F.col("percentage").desc())

    young_share_df.show()

    # 6. Топ-3 категорії з найвищим відсотком витрат у віці 18–25
    header(f"p6. Топ-3 категорії за відсотком витрат, вік {AGE_FROM}–{AGE_TO}")
    young_share_df \
        .select("category", "percentage") \
        .limit(3) \
        .show()

    # Закриваємо сесію Spark
    spark.stop()


if __name__ == "__main__":
    main()
