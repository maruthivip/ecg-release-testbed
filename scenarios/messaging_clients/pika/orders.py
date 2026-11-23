import json

import pika


def publish_order(connection: pika.BlockingConnection, order_id: str) -> None:
    if not order_id:
        raise ValueError("missing order ID")
    channel = connection.channel()
    channel.confirm_delivery()
    channel.basic_publish(
        exchange="commerce.orders", routing_key="orders.created",
        body=json.dumps({"order_id": order_id}).encode(), mandatory=True,
        properties=pika.BasicProperties(delivery_mode=2, content_type="application/json"),
    )


def consume_one(connection: pika.BlockingConnection) -> str | None:
    channel = connection.channel()
    method, _properties, body = channel.basic_get(queue="billing.orders", auto_ack=False)
    if method is None:
        return None
    try:
        order_id = json.loads(body)["order_id"]
    except (ValueError, KeyError, TypeError):
        channel.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
        raise
    channel.basic_ack(delivery_tag=method.delivery_tag)
    return order_id


def preview_route() -> str:
    return "commerce.orders:orders.created"
