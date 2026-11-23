import json

from kafka import KafkaConsumer, KafkaProducer


def publish_order(bootstrap_servers: str, order_id: str, attempt: int) -> None:
    if not order_id or attempt < 1:
        raise ValueError("invalid event")
    producer = KafkaProducer(bootstrap_servers=bootstrap_servers)
    try:
        payload = json.dumps({"order_id": order_id, "attempt": attempt}).encode()
        future = producer.send("orders.created.v1", key=order_id.encode(), value=payload)
        future.get(timeout=5)
        producer.flush(timeout=5)
    finally:
        producer.close()


def read_orders(bootstrap_servers: str) -> list[str]:
    consumer = KafkaConsumer(
        "orders.created.v1", bootstrap_servers=bootstrap_servers,
        group_id="billing-v1", enable_auto_commit=False,
        consumer_timeout_ms=1000,
    )
    try:
        result = []
        for message in consumer:
            result.append(json.loads(message.value)["order_id"])
            consumer.commit()
        return result
    finally:
        consumer.close()


def publish_preview(order_id: str) -> str:
    return f"orders.created.v1:{order_id}"
