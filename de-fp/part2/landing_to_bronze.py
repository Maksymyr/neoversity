from pathlib import Path

import requests
from pyspark.sql import SparkSession

BASE_DIR = Path(__file__).resolve().parent
TABLES = ["athlete_bio", "athlete_event_results"]


def download_data(local_file_path: Path) -> None:
    url = "https://ftp.goit.study/neoversity/"
    downloading_url = url + local_file_path.stem + ".csv"
    print(f"Downloading from {downloading_url}")
    response = requests.get(downloading_url, timeout=300)

    if response.status_code == 200:
        local_file_path.parent.mkdir(parents=True, exist_ok=True)
        with open(local_file_path, "wb") as file:
            file.write(response.content)
        print(f"File downloaded successfully and saved as {local_file_path}")
    else:
        exit(f"Failed to download the file. Status code: {response.status_code}")


def main() -> None:
    spark = SparkSession.builder.appName("LandingToBronze").getOrCreate()

    for table in TABLES:
        csv_path = BASE_DIR / "landing" / f"{table}.csv"
        download_data(csv_path)

        df = spark.read.csv(str(csv_path), header=True, inferSchema=True)
        df.write.mode("overwrite").parquet(str(BASE_DIR / "bronze" / table))

        bronze_df = spark.read.parquet(str(BASE_DIR / "bronze" / table))
        print(f"bronze/{table}: {bronze_df.count()} rows")
        bronze_df.show()

    spark.stop()


if __name__ == "__main__":
    main()
