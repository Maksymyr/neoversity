FROM apache/airflow:2.9.3-python3.11

# Java для Spark
USER root
RUN apt-get update \
    && apt-get install -y --no-install-recommends openjdk-17-jre-headless \
    && rm -rf /var/lib/apt/lists/* \
    && ln -s /usr/lib/jvm/java-17-openjdk-* /usr/lib/jvm/java-17
ENV JAVA_HOME=/usr/lib/jvm/java-17

# провайдер зі SparkSubmitOperator і сам PySpark (spark-submit)
USER airflow
RUN pip install --no-cache-dir \
    "apache-airflow==2.9.3" \
    "apache-airflow-providers-apache-spark==4.8.2" \
    "pyspark==3.5.1" \
    --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-2.9.3/constraints-3.11.txt"
