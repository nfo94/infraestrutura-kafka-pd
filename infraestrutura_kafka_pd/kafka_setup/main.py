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
        logging.info(f"Admin client: {admin_client}")

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
        logging.info(f"Topics: {topics}")

        admin_client.create_topics(topics)

        admin_client.close()

    except TopicAlreadyExistsError:
        logging.info("Topics already exist. Exiting...")
        return

    except Exception as e:
        logging.error(f"Error while creating topics: {e}")


if __name__ == "__main__":
    main()
