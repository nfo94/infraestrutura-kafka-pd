import asyncio
import json
import logging
from os import getenv

from aiokafka import AIOKafkaConsumer, AIOKafkaProducer

from .fraud_detector import detector

"""
Component responsible for consuming messages from the Kafka topic `transactions`,
producing messages to the topic `fraudulent_transactions`.
"""


async def consume():
    logging.basicConfig(level=logging.INFO)

    try:
        consumer = AIOKafkaConsumer(
            getenv("TOPIC_TRANSACTIONS"),
            bootstrap_servers=getenv("KAFKA_BOOTSTRAP_SERVERS"),
            group_id="transactions_group",
            auto_offset_reset="earliest",
        )
        logging.info(f"Subscribing to topic: {getenv('TOPIC_TRANSACTIONS')}")
        await consumer.start()
        logging.info("Finished subscribing.")

        producer = AIOKafkaProducer(bootstrap_servers=getenv("KAFKA_BOOTSTRAP_SERVERS"))
        logging.info("Initializing producer...")
        await producer.start()
        logging.info("Producer initialized successfully.")

        async for msg in consumer:
            logging.info(f"Message received: {msg}")
            raw_data = msg.value
            transaction_data = json.loads(raw_data.decode("utf-8"))
            logging.info(f"Message decoded: {transaction_data}")

            logging.info("Calling fraud detector...")
            fraud, fraud_message = await detector(transaction_data)
            if fraud:
                logging.info("Fraud detected")
                await producer.send_and_wait(
                    getenv("TOPIC_FRAUDULENT_TRANSACTIONS"),
                    json.dumps(fraud_message).encode("utf-8"),
                    key=str(transaction_data["user_id"]).encode(),
                )

    except Exception as e:
        logging.error(f"Error while consuming transactions: {e}")

    finally:
        logging.info("Stopping consumer and producer...")
        await consumer.stop()
        await producer.stop()


if __name__ == "__main__":
    asyncio.run(consume())
