import asyncio
import json
import logging
from datetime import datetime

from aiokafka import AIOKafkaConsumer, AIOKafkaProducer
from config import (
    KAFKA_BOOTSTRAP_SERVERS,
    TOPIC_FRAUDULENT_TRANSACTIONS,
    TOPIC_TRANSACTIONS,
)
from models import Transaction

from .fraud_detector import detector


async def consume():
    consumer = AIOKafkaConsumer(
        TOPIC_TRANSACTIONS,
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        group_id="fraud-detection-group",
    )
    producer = AIOKafkaProducer(bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS)

    await consumer.start()
    await producer.start()

    try:
        async for msg in consumer:
            transaction_data = msg.value
            transaction = Transaction(**transaction_data)

            fraud_type, fraud_params = await detector(transaction)
            if fraud_type:
                fraud_message = {
                    "user_id": transaction.user_id,
                    "fraud_type": fraud_type,
                    "fraud_params": fraud_params,
                    "timestamp": datetime.now().isoformat(),
                }

                await producer.send_and_wait(
                    TOPIC_FRAUDULENT_TRANSACTIONS, json.dumps(fraud_message).encode()
                )

                logging.info(f"Fraude detectada: {fraud_message}")
    finally:
        await consumer.stop()
        await producer.stop()


if __name__ == "__main__":
    asyncio.run(consume())
