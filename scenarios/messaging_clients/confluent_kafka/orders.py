import json

from confluent_kafka import Consumer, KafkaException, Producer


def publish_order(bootstrap_servers: str, order_id: str) -> None:
    if not order_id:
        raise ValueError("missing order ID")
    producer = Producer({"bootstrap.servers": bootstrap_servers})
    failures: list[str] = []

    def on_delivery(error, message):
        if error is not None:
            failures.append(str(error))

    producer.produce(
        "orders.created.v3", key=order_id.encode(),
        value=json.dumps({"order_id": order_id}).encode(), callback=on_delivery,
    )
    remaining = producer.flush(5)
    if remaining or failures:
        raise RuntimeError(f"delivery failed: remaining={remaining}; errors={failures}")


def consume_one(bootstrap_servers: str) -> str | None:
    consumer = Consumer({
        "bootstrap.servers": bootstrap_servers,
        "group.id": "analytics-v3",
        "enable.auto.commit": False,
    })
    try:
        consumer.subscribe(["orders.created.v3"])
        message = consumer.poll(5)
        if message is None:
            return None
        if message.error():
            raise KafkaException(message.error())
        order_id = json.loads(message.value())["order_id"]
        consumer.commit(message=message, asynchronous=False)
        return order_id
    finally:
        consumer.close()
