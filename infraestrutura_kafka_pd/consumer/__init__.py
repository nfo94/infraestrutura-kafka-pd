import asyncio
from datetime import datetime

import fastavro
import json
from aiokafka import AIOKafkaConsumer, AIOKafkaProducer
from config import (
    KAFKA_BOOTSTRAP_SERVERS,
    TOPIC_FRAUDULENT_TRANSACTIONS,
    TOPIC_TRANSACTIONS,
)
from models import Transaction

# Estruturas para armazenar o contexto do usuário
user_context = {}


async def detect_fraud(transaction):
    """Aplica as regras de fraude."""
    user_id = transaction.user_id
    if user_id not in user_context:
        user_context[user_id] = {
            "last_transaction": None,
            "max_value": 0,
            "last_country": None,
        }

    context = user_context[user_id]
    fraud_type = None
    fraud_params = {}

    # Regra 1: Alta Frequência
    if (
        context["last_transaction"]
        and (transaction.timestamp - context["last_transaction"].timestamp) < 300
    ):
        fraud_type = "Alta Frequência"
        fraud_params = {
            "interval": transaction.timestamp - context["last_transaction"].timestamp
        }

    # Regra 2: Alto Valor
    if transaction.value > 2 * context["max_value"]:
        fraud_type = "Alto Valor"
        fraud_params = {"value": transaction.value, "max_value": context["max_value"]}

    # Regra 3: Outro País
    if context["last_country"] and context["last_country"] != transaction.country:
        fraud_type = "Outro País"
        fraud_params = {
            "last_country": context["last_country"],
            "current_country": transaction.country,
        }

    # Atualiza o contexto do usuário
    context["last_transaction"] = transaction
    context["max_value"] = max(context["max_value"], transaction.value)
    context["last_country"] = transaction.country

    return fraud_type, fraud_params


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
            schema = fastavro.schema.load_schema("schemas/transaction.avsc")
            transaction_data = fastavro.schemaless_reader(msg.value, schema)
            transaction = Transaction(**transaction_data)

            fraud_type, fraud_params = await detect_fraud(transaction)
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

                print(f"Fraude detectada: {fraud_message}")
    finally:
        await consumer.stop()
        await producer.stop()


if __name__ == "__main__":
    asyncio.run(consume())
