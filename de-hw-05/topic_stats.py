from kafka import KafkaConsumer, TopicPartition

from kafka_common import ALL_TOPICS, connection_params


def main() -> None:
    # Consumer без group_id лише читає метадані й нічого не комітить
    consumer = KafkaConsumer(**connection_params())

    print("Messages stored in topics:")
    for topic in ALL_TOPICS:
        partitions = [TopicPartition(topic, p) for p in sorted(consumer.partitions_for_topic(topic) or [])]
        begin = consumer.beginning_offsets(partitions)
        end = consumer.end_offsets(partitions)
        counts = {tp.partition: end[tp] - begin[tp] for tp in partitions}
        per_partition = ", ".join(f"p{p}: {n}" for p, n in counts.items())
        print(f"  {topic}: {sum(counts.values())} ({per_partition})")

    consumer.close()


if __name__ == "__main__":
    main()
