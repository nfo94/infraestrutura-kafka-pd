import asyncio
import json
import logging
from os import getenv

from aiokafka import AIOKafkaConsumer
from sqlalchemy import Column, Integer, MetaData, String, Table, create_engine
from sqlalchemy.orm import sessionmaker

"""
Component responsible for consuming messages from the Kafka topic `fraudulent_transactions`
and sending them to the PostgreSQL database.
"""

metadata = MetaData()

DB_NAME = "fraudulent_transactions"

fraudulent_transactions_table = Table(
    DB_NAME,
    metadata,
    Column("user_id", Integer),
    Column("fraud_type", String(255)),
    Column("fraud_params", json.JSON),
    Column("timestamp", String(255)),
)


def get_engine():
    db_uri = (
        f"postgresql://{getenv('DB_USER')}:{getenv('DB_PASSWORD')}"
        f"@{getenv('DB_HOST')}/{DB_NAME}"
    )
    return create_engine(db_uri)


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=get_engine())


async def consume():
    logging.basicConfig(level=logging.INFO)

    try:
        consumer = AIOKafkaConsumer(
            getenv("TOPIC_FRAUDULENT_TRANSACTIONS"),
            bootstrap_servers=getenv("KAFKA_BOOTSTRAP_SERVERS"),
            group_id="fraudulent_transactions_group",
            auto_offset_reset="earliest",
        )
        logging.info(f"Subscribing to topic: {getenv('TOPIC_FRAUDULENT_TRANSACTIONS')}")
        await consumer.start()
        logging.info("Finished subscribing.")

        engine = get_engine()
        logging.info("Creating fraudulent_transactions table...")
        metadata.create_all(engine)

        session = SessionLocal()

        async for msg in consumer:
            raw_data = msg.value
            transaction_data = json.loads(raw_data.decode("utf-8"))
            logging.info(f"Message received: {transaction_data}")

            logging.info("Inserting transaction into the database...")
            insert_stmt = fraudulent_transactions_table.insert().values(
                transaction_id=transaction_data["transaction_id"],
                timestamp=transaction_data["timestamp"],
                user_id=transaction_data["user_id"],
                card_id=transaction_data["card_id"],
                site_id=transaction_data["site_id"],
                value=transaction_data["value"],
                location_id=transaction_data["location_id"],
                country=transaction_data["country"],
            )
            session.execute(insert_stmt)
            session.commit()

    except Exception as e:
        logging.error(f"Error in consumer_to_db: {e}")

    finally:
        logging.info("Stoping consumer_to_db...")
        await consumer.stop()
        session.close()


if __name__ == "__main__":
    asyncio.run(consume())
