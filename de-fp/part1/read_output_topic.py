import json

from kafka import KafkaConsumer

from common import OUTPUT_TOPIC, kafka_python_params


def main() -> None:
    # без group_id: просто читаємо топік з початку для перевірки
    consumer = KafkaConsumer(
        OUTPUT_TOPIC,
        **kafka_python_params(),
        auto_offset_reset="earliest",
        consumer_timeout_ms=10000,
        value_deserializer=lambda raw: json.loads(raw.decode("utf-8")),
    )

    print(f"Reading '{OUTPUT_TOPIC}'")
    count = 0
    for message in consumer:
        count += 1
        if count <= 20:
            print(message.value)
    print(f"Total messages: {count}")
    consumer.close()


if __name__ == "__main__":
    main()
