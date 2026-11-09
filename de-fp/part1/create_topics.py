from kafka.admin import KafkaAdminClient, NewTopic

from common import INPUT_TOPIC, MY_NAME, OUTPUT_TOPIC, kafka_python_params


def main() -> None:
    admin_client = KafkaAdminClient(**kafka_python_params())

    existing = set(admin_client.list_topics())
    new_topics = [
        NewTopic(name=name, num_partitions=2, replication_factor=1)
        for name in (INPUT_TOPIC, OUTPUT_TOPIC)
        if name not in existing
    ]
    if new_topics:
        admin_client.create_topics(new_topics=new_topics, validate_only=False)

    for topic in admin_client.list_topics():
        if topic.startswith(f"{MY_NAME}_athlete"):
            print(topic)

    admin_client.close()


if __name__ == "__main__":
    main()
