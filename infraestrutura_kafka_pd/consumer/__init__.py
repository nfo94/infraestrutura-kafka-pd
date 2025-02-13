import asyncio
import logging

import config
from aiokafka import AIOKafkaConsumer


async def main():
    consumer = AIOKafkaConsumer(
        topic=config.KAFKA_TOPIC,
        bootstrap_server=config.KAFKA_BOOTSTRAP_SERVERS,
        group_id=config.KAFKA_CONSUMER_GROUP,
    )
    await consumer.start()

    try:
        while True:
            async for msg in consumer:
                logging.info(
                    "----------Message consumed by Consumer 1!----------\n"
                    f"Offset: {msg.offset}\n"
                    f"Topic: {msg.topic}\n"
                    f"Partition: {msg.partition}\n"
                    f"Timestamp: {msg.timestamp}\n"
                    f"Key: {msg.key}\n"
                    f"Value: {msg.value}"
                )
    except Exception as e:
        logging.error(f"Error consuming message: {e}")
    finally:
        await consumer.stop()


if __name__ == "__main__":
    asyncio.run(main())
