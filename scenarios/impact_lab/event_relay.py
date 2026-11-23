from .contracts import Event
from .order_store import OrderStore


class Relay:
    def __init__(self, store: OrderStore) -> None:
        self.store = store

    def publish_pending(self, publish) -> None:
        for event in self.store.events():
            publish(event)


class FulfilmentConsumer:
    def __init__(self) -> None:
        self.processed: set[str] = set()
        self.orders: list[str] = []

    def handle(self, event: Event) -> bool:
        if (event.namespace, event.topic, event.kind, event.version) != (
            "commerce-prod", "order-events", "order.created", 1
        ):
            return False
        if event.event_id in self.processed:
            return False
        self.processed.add(event.event_id)
        self.orders.append(event.order_id)
        return True


class AuditConsumer:
    def __init__(self) -> None:
        self.processed: set[str] = set()

    def handle(self, event: Event) -> bool:
        if (event.namespace, event.topic, event.kind) != (
            "audit-sandbox", "order-events", "order.created"
        ):
            return False
        self.processed.add(event.event_id)
        return True
