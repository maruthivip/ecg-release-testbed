import threading

from .contracts import Event, OrderRequest
from .inventory_service import InventoryService
from .order_store import OrderStore
from .payment_service import PaymentService


class OrderService:
    def __init__(self, inventory: InventoryService, payment: PaymentService, store: OrderStore) -> None:
        self.inventory = inventory
        self.payment = payment
        self.store = store
        self.lock = threading.Lock()

    def place_order(self, order: OrderRequest) -> str:
        order.validate()
        with self.lock:
            prior = self.store.get(order.order_id)
            if prior is not None:
                if prior != (order.order_id, order.sku, order.quantity, order.total_cents):
                    raise ValueError("order conflict")
                return "accepted"
            if not self.inventory.reserve(order.order_id, order.sku, order.quantity):
                return "out_of_stock"
            try:
                if not self.payment.authorize(order.order_id, order.total_cents):
                    self.inventory.release(order.order_id)
                    return "payment_declined"
            except Exception:
                self.inventory.release(order.order_id)
                raise
            event = Event(
                event_id=f"{order.order_id}:created:v1",
                order_id=order.order_id,
                namespace="commerce-prod",
                topic="order-events",
                kind="order.created",
                version=1,
            )
            try:
                self.store.save_with_event(order, event)
            except Exception:
                self.payment.void(order.order_id)
                self.inventory.release(order.order_id)
                raise
            return "accepted"
