import logging
from config import (
    KAFKA_BOOTSTRAP_SERVERS,
    TOPIC_FRAUDULENT_TRANSACTIONS,
    TOPIC_TRANSACTIONS,
)
from kafka.admin import KafkaAdminClient, NewTopic


def main():
    try:
        admin_client = KafkaAdminClient(bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS)

        topics = [
            NewTopic(name=TOPIC_TRANSACTIONS, num_partitions=3, replication_factor=3),
            NewTopic(
                name=TOPIC_FRAUDULENT_TRANSACTIONS,
                num_partitions=3,
                replication_factor=3,
            ),
        ]

        admin_client.create_topics([topics], timeout_ms=6000)

        admin_client.close()
    except Exception as e:
        logging.error(f"Error while creating topics: {e}")


if __name__ == "__main__":
    main()
