import json

from aiokafka import AIOKafkaConsumer, AIOKafkaProducer


async def publish_order(bootstrap_servers: str, order_id: str) -> None:
    if not order_id:
        raise ValueError("missing order ID")
    producer = AIOKafkaProducer(bootstrap_servers=bootstrap_servers)
    await producer.start()
    try:
        await producer.send_and_wait(
            "orders.created.v2",
            key=order_id.encode(),
            value=json.dumps({"order_id": order_id, "version": 2}).encode(),
        )
    finally:
        await producer.stop()


async def consume_one(bootstrap_servers: str) -> str:
    consumer = AIOKafkaConsumer(
        "orders.created.v2", bootstrap_servers=bootstrap_servers,
        group_id="fulfilment-v2", enable_auto_commit=False,
    )
    await consumer.start()
    try:
        message = await consumer.getone()
        order_id = json.loads(message.value)["order_id"]
        await consumer.commit()
        return order_id
    finally:
        await consumer.stop()
