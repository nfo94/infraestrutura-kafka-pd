import asyncio
import logging
from time import sleep

import config
from aiokafka import AIOKafkaProducer

from ..models import KafkaMessageFactory


async def main():
    producer = AIOKafkaProducer(bootstrap_server=config.KAFKA_BOOTSTRAP_SERVERS)
    await producer.start()

    try:
        while True:
            new_message = KafkaMessageFactory().create_kafka_message()
            await producer.send_and_wait(
                topic=config.KAFKA_TOPIC, value=new_message.dict()
            )
            sleep(8)
    except Exception as e:
        logging.error(f"Error sending message to Kafka: {e}")
    finally:
        await producer.stop()


if __name__ == "__main__":
    asyncio.run(main())
