from azure.servicebus import ServiceBusClient

from events import OrderCreated


def receive_orders(client: ServiceBusClient) -> None:
    with client.get_subscription_receiver(
        topic_name="order-events", subscription_name="fulfilment"
    ) as receiver:
        for message in receiver.receive_messages(max_message_count=10, max_wait_time=5):
            try:
                event = OrderCreated.from_json(str(message))
            except (TypeError, ValueError, UnicodeError) as error:
                receiver.dead_letter_message(message, reason="InvalidOrderEvent", error_description=str(error))
                continue
            process_order(event)
            receiver.complete_message(message)


def process_order(event: OrderCreated) -> str:
    return event.order_id
