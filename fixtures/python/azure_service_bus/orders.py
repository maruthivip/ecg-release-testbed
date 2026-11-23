from azure.servicebus import ServiceBusClient, ServiceBusMessage


def publish_order(connection_string: str, order_id: str) -> None:
    with ServiceBusClient.from_connection_string(connection_string) as client:
        with client.get_queue_sender(queue_name="release-orders") as sender:
            sender.send_messages(ServiceBusMessage(order_id))


def receive_orders(connection_string: str) -> None:
    with ServiceBusClient.from_connection_string(connection_string) as client:
        with client.get_queue_receiver(queue_name="release-orders") as receiver:
            for message in receiver.receive_messages(max_message_count=1):
                receiver.complete_message(message)
