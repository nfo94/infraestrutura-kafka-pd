import os

KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
TOPIC_TRANSACTIONS = os.getenv("TOPIC_TRANSACTIONS", "transactions")
TOPIC_FRAUDULENT_TRANSACTIONS = os.getenv(
    "TOPIC_FRAUDULENT_TRANSACTIONS", "fraudulent_transactions"
)
