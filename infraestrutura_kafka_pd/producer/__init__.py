import asyncio
import logging

from aiokafka import AIOKafkaProducer
from config import KAFKA_BOOTSTRAP_SERVERS, TOPIC_TRANSACTIONS
from models import Transaction

from .transaction_generator import TransactionGenerator


async def produce():
    producer = AIOKafkaProducer(bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS)

    await producer.start()

    transaction_generator = TransactionGenerator(trans_per_sec=10)

    try:
        for tx in transaction_generator.generate_transactions():
            transaction = Transaction(**tx.__dict__)

            await producer.send_and_wait(TOPIC_TRANSACTIONS, transaction.to_dict())

            logging.info(f"Message produced: {transaction}")

            # Interval between transactions
            await asyncio.sleep(0.1)

    finally:
        await producer.stop()


if __name__ == "__main__":
    asyncio.run(produce())
