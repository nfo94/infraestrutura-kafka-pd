import logging

# Structure to save the context of the user
user_context = {}


async def detector(transaction: dict):
    logging.info(f"Detecting fraud for transaction: {transaction}")

    user_id = transaction["user_id"]
    if user_id not in user_context:
        user_context[user_id] = {
            "last_transaction": None,
            "max_value": 0,
            "last_country": None,
        }

    context = user_context[user_id]
    fraud_type = None
    fraud_params = {}

    logging.info("Analyzing rule 1: high frequency...")
    if (
        context["last_transaction"]
        and (transaction["timestamp"] - context["last_transaction"]["timestamp"]) < 300
    ):
        fraud_type = "Alta Frequência"
        fraud_params = {
            "interval": transaction["timestamp"] - context["last_transaction"]["timestamp"]
        }

    logging.info("Analyzing rule 2: high value...")
    if transaction["value"] > 2 * context["max_value"]:
        fraud_type = "High value"
        fraud_params = {
            "value": transaction["value"],
            "max_value": context["max_value"],
        }

    logging.info("Analyzing rule 3: another country...")
    if context["last_country"] and context["last_country"] != transaction["country"]:
        fraud_type = "Another country"
        fraud_params = {
            "last_country": context["last_country"],
            "current_country": transaction["country"],
        }

    logging.info("Updating user context...")
    context["last_transaction"] = transaction
    context["max_value"] = max(context["max_value"], transaction["value"])
    context["last_country"] = transaction["country"]

    logging.info("Returning detector result...")
    return fraud_type, fraud_params
