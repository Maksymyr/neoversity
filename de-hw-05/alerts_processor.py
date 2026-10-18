from kafka import KafkaConsumer, KafkaProducer

from kafka_common import (
    BUILDING_SENSORS_TOPIC,
    HUMIDITY_ALERTS_TOPIC,
    HUMIDITY_MAX,
    HUMIDITY_MIN,
    MY_NAME,
    TEMPERATURE_ALERTS_TOPIC,
    TEMPERATURE_MAX,
    connection_params,
    deserialize,
    now_iso,
    serialize,
)


def build_alerts(reading: dict) -> list[tuple[str, dict]]:
    """Повертає список пар (топік, сповіщення) для одного виміру. Якщо все в нормі, список порожній."""
    alerts = []
    base = {
        "sensor_id": reading["sensor_id"],
        "timestamp": reading["timestamp"],
        "temperature": reading["temperature"],
        "humidity": reading["humidity"],
        "alert_time": now_iso(),
    }

    if reading["temperature"] > TEMPERATURE_MAX:
        alerts.append((TEMPERATURE_ALERTS_TOPIC, {
            **base,
            "message": f"Temperature {reading['temperature']:.1f}°C exceeds {TEMPERATURE_MAX}°C",
        }))

    if reading["humidity"] > HUMIDITY_MAX:
        alerts.append((HUMIDITY_ALERTS_TOPIC, {
            **base,
            "message": f"Humidity {reading['humidity']:.1f}% exceeds {HUMIDITY_MAX}%",
        }))
    elif reading["humidity"] < HUMIDITY_MIN:
        alerts.append((HUMIDITY_ALERTS_TOPIC, {
            **base,
            "message": f"Humidity {reading['humidity']:.1f}% is below {HUMIDITY_MIN}%",
        }))

    return alerts


def main() -> None:
    # Автокоміт вимкнено. Offset комітиться після того, як брокер прийняв сповіщення,
    # тому збій посередині не призведе до втрати сповіщень
    consumer = KafkaConsumer(
        BUILDING_SENSORS_TOPIC,
        **connection_params(),
        key_deserializer=deserialize,
        value_deserializer=deserialize,
        auto_offset_reset="earliest",
        enable_auto_commit=False,
        group_id=f"{MY_NAME}_alerts_processor",
    )
    producer = KafkaProducer(
        **connection_params(),
        key_serializer=serialize,
        value_serializer=serialize,
    )

    print(f"Processor subscribed to '{BUILDING_SENSORS_TOPIC}'")
    try:
        for message in consumer:
            reading = message.value
            print(
                f"Received sensor {reading['sensor_id']} [{reading['timestamp']}]: "
                f"t={reading['temperature']:.1f}°C h={reading['humidity']:.1f}% "
                f"(partition {message.partition}, offset {message.offset})"
            )

            alerts = build_alerts(reading)
            if not alerts:
                print("  OK, within limits")
            for topic, alert in alerts:
                metadata = producer.send(topic, key=alert["sensor_id"], value=alert).get(timeout=10)
                print(
                    f"  ALERT: {alert['message']} "
                    f"-> sent to '{topic}' (partition {metadata.partition}, offset {metadata.offset})"
                )

            consumer.commit()
    except KeyboardInterrupt:
        pass
    finally:
        consumer.close()
        producer.close()


if __name__ == "__main__":
    main()
