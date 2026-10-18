from kafka import KafkaConsumer

from kafka_common import (
    HUMIDITY_ALERTS_TOPIC,
    MY_NAME,
    TEMPERATURE_ALERTS_TOPIC,
    connection_params,
    deserialize,
)

LABELS = {
    TEMPERATURE_ALERTS_TOPIC: "TEMPERATURE",
    HUMIDITY_ALERTS_TOPIC: "HUMIDITY",
}


def main() -> None:
    consumer = KafkaConsumer(
        TEMPERATURE_ALERTS_TOPIC,
        HUMIDITY_ALERTS_TOPIC,
        **connection_params(),
        key_deserializer=deserialize,
        value_deserializer=deserialize,
        auto_offset_reset="earliest",
        enable_auto_commit=True,
        group_id=f"{MY_NAME}_alerts_monitor",
    )

    print(f"Monitoring '{TEMPERATURE_ALERTS_TOPIC}' and '{HUMIDITY_ALERTS_TOPIC}'")
    try:
        for message in consumer:
            alert = message.value
            print(
                f"[{LABELS[message.topic]}] sensor {alert['sensor_id']} at {alert['timestamp']}: "
                f"{alert['message']} (t={alert['temperature']:.1f}°C, h={alert['humidity']:.1f}%)"
            )
    except KeyboardInterrupt:
        pass
    finally:
        consumer.close()


if __name__ == "__main__":
    main()
