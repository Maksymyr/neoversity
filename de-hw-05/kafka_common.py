import json
from datetime import datetime, timezone
from typing import Any

from configs import kafka_config

# Префікс робить імена топіків унікальними на спільному кластері
MY_NAME = "maksym_popov"

BUILDING_SENSORS_TOPIC = f"{MY_NAME}_building_sensors"
TEMPERATURE_ALERTS_TOPIC = f"{MY_NAME}_temperature_alerts"
HUMIDITY_ALERTS_TOPIC = f"{MY_NAME}_humidity_alerts"

ALL_TOPICS = [BUILDING_SENSORS_TOPIC, TEMPERATURE_ALERTS_TOPIC, HUMIDITY_ALERTS_TOPIC]

# Порогові значення для сповіщень
TEMPERATURE_MAX = 40
HUMIDITY_MIN = 20
HUMIDITY_MAX = 80


def connection_params() -> dict[str, Any]:
    """Параметри підключення й автентифікації, спільні для admin, producer і consumer."""
    return {
        "bootstrap_servers": kafka_config["bootstrap_servers"],
        "security_protocol": kafka_config["security_protocol"],
        "sasl_mechanism": kafka_config["sasl_mechanism"],
        "sasl_plain_username": kafka_config["username"],
        "sasl_plain_password": kafka_config["password"],
    }


def serialize(value: Any) -> bytes:
    return json.dumps(value).encode("utf-8")


def deserialize(raw: bytes) -> Any:
    return json.loads(raw.decode("utf-8"))


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")
