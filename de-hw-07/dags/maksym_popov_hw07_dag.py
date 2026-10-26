import random
import time
from datetime import datetime

from airflow import DAG
from airflow.models.param import Param
from airflow.operators.python import BranchPythonOperator, PythonOperator
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
from airflow.providers.common.sql.sensors.sql import SqlSensor
from airflow.utils.trigger_rule import TriggerRule

CONNECTION_ID = "goit_mysql_db"
SCHEMA = "maksym_popov"
RESULTS_TABLE = f"{SCHEMA}.hw_dag_results"
MEDALS = ["Bronze", "Silver", "Gold"]


def pick_medal() -> str:
    medal = random.choice(MEDALS)
    print(f"Picked medal: {medal}")
    return medal


def pick_medal_task(ti) -> str:
    medal = ti.xcom_pull(task_ids="pick_medal")
    return f"calc_{medal}"


def generate_delay(params) -> None:
    delay = params["delay_seconds"]
    print(f"Sleeping for {delay} seconds")
    time.sleep(delay)


with DAG(
    dag_id="maksym_popov_hw07",
    start_date=datetime(2026, 10, 1),
    schedule=None,
    catchup=False,
    tags=["maksym_popov"],
    # 35 секунд у тригері з конфігом показує падіння сенсора
    params={"delay_seconds": Param(10, type="integer", minimum=0)},
) as dag:

    create_table = SQLExecuteQueryOperator(
        task_id="create_table",
        conn_id=CONNECTION_ID,
        sql=[
            f"CREATE DATABASE IF NOT EXISTS {SCHEMA};",
            f"""
            CREATE TABLE IF NOT EXISTS {RESULTS_TABLE} (
                id INT AUTO_INCREMENT PRIMARY KEY,
                medal_type VARCHAR(10),
                count INT,
                created_at DATETIME
            );
            """,
        ],
    )

    pick_medal_op = PythonOperator(
        task_id="pick_medal",
        python_callable=pick_medal,
    )

    pick_medal_task_op = BranchPythonOperator(
        task_id="pick_medal_task",
        python_callable=pick_medal_task,
    )

    calc_tasks = [
        SQLExecuteQueryOperator(
            task_id=f"calc_{medal}",
            conn_id=CONNECTION_ID,
            sql=f"""
            INSERT INTO {RESULTS_TABLE} (medal_type, count, created_at)
            SELECT '{medal}', COUNT(*), NOW()
            FROM olympic_dataset.athlete_event_results
            WHERE medal = '{medal}';
            """,
        )
        for medal in MEDALS
    ]

    generate_delay_op = PythonOperator(
        task_id="generate_delay",
        python_callable=generate_delay,
        trigger_rule=TriggerRule.ONE_SUCCESS,
    )

    # 1, якщо найновіший запис не старший за 30 секунд
    check_for_correctness = SqlSensor(
        task_id="check_for_correctness",
        conn_id=CONNECTION_ID,
        sql=f"""
        SELECT TIMESTAMPDIFF(SECOND, MAX(created_at), NOW()) <= 30
        FROM {RESULTS_TABLE};
        """,
        mode="poke",
        poke_interval=5,
        timeout=6,
    )

    create_table >> pick_medal_op >> pick_medal_task_op >> calc_tasks
    calc_tasks >> generate_delay_op >> check_for_correctness
