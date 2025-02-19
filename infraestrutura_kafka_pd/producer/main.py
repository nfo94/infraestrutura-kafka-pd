import asyncio
import json
import logging
import time
from os import getenv

from aiokafka import AIOKafkaProducer

from .transaction_generator import TransactionGenerator

"""Component responsible for producing transactions to the Kafka topic."""


async def produce():
    logging.basicConfig(level=logging.INFO)

    producer = AIOKafkaProducer(bootstrap_servers=getenv("KAFKA_BOOTSTRAP_SERVERS"))
    await producer.start()

    transaction_generator = TransactionGenerator(trans_per_sec=10)

    start_time = time.time()

    try:
        for tx in transaction_generator.generate_transactions():
            # Will produce transactions for 10 seconds
            if time.time() - start_time > 10:
                break

            tx_to_dict = tx.model_dump()

            await producer.send_and_wait(
                getenv("TOPIC_TRANSACTIONS"), json.dumps(tx_to_dict).encode("utf-8")
            )

            logging.info(f"Message produced: {tx_to_dict}")

            # Interval between transactions
            await asyncio.sleep(0.1)

    except Exception as e:
        logging.error(f"Error while producing transactions: {e}")

    finally:
        await producer.stop()


if __name__ == "__main__":
    asyncio.run(produce())
