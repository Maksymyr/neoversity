from kafka import KafkaConsumer

from kafka_common import ALERTS_TOPIC, MY_NAME, connection_params


def main() -> None:
    # value як текст, щоб бачити JSON від Spark як є
    consumer = KafkaConsumer(
        ALERTS_TOPIC,
        **connection_params(),
        key_deserializer=lambda raw: raw.decode("utf-8") if raw else None,
        value_deserializer=lambda raw: raw.decode("utf-8"),
        auto_offset_reset="earliest",
        enable_auto_commit=True,
        group_id=f"{MY_NAME}_hw6_alerts_monitor",
    )

    print(f"Reading alerts from '{ALERTS_TOPIC}'")
    try:
        for message in consumer:
            print(f"[partition {message.partition}, offset {message.offset}, key {message.key}] {message.value}")
    except KeyboardInterrupt:
        pass
    finally:
        consumer.close()


if __name__ == "__main__":
    main()
