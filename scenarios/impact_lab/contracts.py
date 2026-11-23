from dataclasses import dataclass


@dataclass(frozen=True)
class OrderRequest:
    order_id: str
    sku: str
    quantity: int
    total_cents: int

    def validate(self) -> None:
        if not self.order_id or not self.sku or self.quantity <= 0 or self.total_cents <= 0:
            raise ValueError("invalid order")


@dataclass(frozen=True)
class Event:
    event_id: str
    order_id: str
    namespace: str
    topic: str
    kind: str
    version: int
