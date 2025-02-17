import asyncio

import fastavro
from aiokafka import AIOKafkaProducer
from config import KAFKA_BOOTSTRAP_SERVERS, TOPIC_TRANSACTIONS
from models import Transaction
from utils import TransactionGenerator


async def produce():
    producer = AIOKafkaProducer(bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS)

    await producer.start()

    transaction_generator = TransactionGenerator(trans_per_sec=10)

    try:
        for tx in transaction_generator.generate_transactions():
            transaction = Transaction(**tx.__dict__)

            schema = fastavro.schema.load_schema("schemas/transaction.avsc")
            message = fastavro.schemaless_writer(transaction.to_dict(), schema)

            await producer.send_and_wait(TOPIC_TRANSACTIONS, message)

            print(f"Mensagem produzida: {transaction}")

            # Intervalo entre transações
            await asyncio.sleep(0.1)

    finally:
        await producer.stop()


if __name__ == "__main__":
    asyncio.run(produce())
