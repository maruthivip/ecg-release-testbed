from azure.servicebus import ServiceBusClient, ServiceBusMessage

from events import OrderCreated


def publish_order(client: ServiceBusClient, event: OrderCreated) -> None:
    with client.get_topic_sender(topic_name="order-events") as sender:
        message = ServiceBusMessage(
            event.to_json(),
            message_id=event.event_id,
            subject="order.created",
            content_type="application/json",
        )
        sender.send_messages(message)
