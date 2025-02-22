from datetime import datetime, timedelta

user_transactions = {}


async def detector(transaction: dict):
    fraud = False
    fraud_message = None

    user_id = transaction["user_id"]
    timestamp = datetime.fromtimestamp(transaction["timestamp"])
    amount = transaction["value"]
    country = transaction["country"]

    if user_id not in user_transactions:
        user_transactions[user_id] = []

    transactions = user_transactions[user_id]

    if len(transactions) >= 1:
        last_transaction = transactions[-1]
        time_diff = timestamp - last_transaction["timestamp"]
        if time_diff < timedelta(minutes=5) and last_transaction["amount"] != amount:
            fraud = True
            fraud_message = {
                "user_id": user_id,
                "fraud_type": "high_frequency",
                "fraud_params": {
                    "last_amount": last_transaction["amount"],
                    "current_amount": amount,
                    "time_diff_seconds": time_diff.total_seconds(),
                },
                "timestamp": timestamp.isoformat(),
            }

    if not fraud and len(transactions) >= 1:
        max_amount = max(t["amount"] for t in transactions)
        if amount > 2 * max_amount:
            fraud = True
            fraud_message = {
                "user_id": user_id,
                "fraud_type": "high_value",
                "fraud_params": {"max_amount": max_amount, "current_amount": amount},
                "timestamp": timestamp.isoformat(),
            }

    if not fraud and len(transactions) >= 1:
        last_transaction = transactions[-1]
        time_diff = timestamp - last_transaction["timestamp"]
        if time_diff < timedelta(hours=2) and last_transaction["country"] != country:
            fraud = True
            fraud_message = {
                "user_id": user_id,
                "fraud_type": "other_country",
                "fraud_params": {
                    "last_country": last_transaction["country"],
                    "current_country": country,
                    "time_diff_seconds": time_diff.total_seconds(),
                },
                "timestamp": timestamp.isoformat(),
            }

    transactions.append({"timestamp": timestamp, "amount": amount, "country": country})

    return fraud, fraud_message
