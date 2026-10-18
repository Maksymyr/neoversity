import json
from datetime import datetime, timezone
from typing import Any

from configs import kafka_config

# префікс, бо кластер спільний
MY_NAME = "maksym_popov"

BUILDING_SENSORS_TOPIC = f"{MY_NAME}_hw6_building_sensors"
ALERTS_TOPIC = f"{MY_NAME}_hw6_alerts"

ALL_TOPICS = [BUILDING_SENSORS_TOPIC, ALERTS_TOPIC]


def connection_params() -> dict[str, Any]:
    return {
        "bootstrap_servers": kafka_config["bootstrap_servers"],
        "security_protocol": kafka_config["security_protocol"],
        "sasl_mechanism": kafka_config["sasl_mechanism"],
        "sasl_plain_username": kafka_config["username"],
        "sasl_plain_password": kafka_config["password"],
    }


def spark_kafka_options() -> dict[str, str]:
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


def serialize(value: Any) -> bytes:
    return json.dumps(value).encode("utf-8")



def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")
