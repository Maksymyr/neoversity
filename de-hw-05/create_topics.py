from kafka.admin import KafkaAdminClient, NewTopic

from kafka_common import ALL_TOPICS, MY_NAME, connection_params

NUM_PARTITIONS = 2
REPLICATION_FACTOR = 1


def main() -> None:
    admin_client = KafkaAdminClient(**connection_params())

    # Створюємо лише ті топіки, яких ще немає, щоб повторний запуск не падав
    existing = set(admin_client.list_topics())
    new_topics = [
        NewTopic(name=name, num_partitions=NUM_PARTITIONS, replication_factor=REPLICATION_FACTOR)
        for name in ALL_TOPICS
        if name not in existing
    ]

    if new_topics:
        admin_client.create_topics(new_topics=new_topics, validate_only=False)
        for topic in new_topics:
            print(f"Topic '{topic.name}' created successfully.")
    else:
        print("All topics already exist.")

    # Перевіряємо список своїх топіків
    print(f"\nTopics containing '{MY_NAME}':")
    [print(topic) for topic in admin_client.list_topics() if MY_NAME in topic]

    admin_client.close()


if __name__ == "__main__":
    main()
