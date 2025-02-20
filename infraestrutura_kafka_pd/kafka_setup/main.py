import logging
from os import getenv

from kafka.admin import KafkaAdminClient, NewTopic
from kafka.errors import TopicAlreadyExistsError

"""Component responsible for setting up the Kafka topics."""


def main():
    logging.basicConfig(level=logging.INFO)

    try:
        logging.info("Initializing Kafka setup...")

        admin_client = KafkaAdminClient(
            bootstrap_servers=getenv("KAFKA_BOOTSTRAP_SERVERS")
        )

        topics = [
            NewTopic(
                name=getenv("TOPIC_TRANSACTIONS"),
                num_partitions=3,
                replication_factor=3,
            ),
            NewTopic(
                name=getenv("TOPIC_FRAUDULENT_TRANSACTIONS"),
                num_partitions=3,
                replication_factor=3,
            ),
        ]

        logging.info("Creating topics...")
        admin_client.create_topics(topics)

    except TopicAlreadyExistsError:
        logging.info("Topics already exist. Exiting...")

    except Exception as e:
        logging.error(f"Error while creating topics: {e}")

    finally:
        logging.info("Closing Kafka admin client...")
        admin_client.close()


if __name__ == "__main__":
    main()
