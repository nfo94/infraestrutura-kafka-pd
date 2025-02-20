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

    try:
        producer = AIOKafkaProducer(bootstrap_servers=getenv("KAFKA_BOOTSTRAP_SERVERS"))
        await producer.start()

        transaction_generator = TransactionGenerator(trans_per_sec=10)

        start_time = time.time()

        for tx in transaction_generator.generate_transactions():
            # Will produce transactions for 10 seconds
            if time.time() - start_time > 10:
                break

            tx_to_dict = tx.model_dump()

            await producer.send_and_wait(
                getenv("TOPIC_TRANSACTIONS"),
                json.dumps(tx_to_dict).encode("utf-8"),
                key=str(tx_to_dict["user_id"]).encode(),
            )

            logging.info(f"Message produced: {tx_to_dict}")

            # Interval between transactions
            await asyncio.sleep(0.1)

    except Exception as e:
        logging.error(f"Error while producing transactions: {e}")

    finally:
        logging.info("Stoping producer...")
        await producer.stop()


if __name__ == "__main__":
    asyncio.run(produce())
