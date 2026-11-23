import threading


class InventoryService:
    def __init__(self, available: dict[str, int]) -> None:
        self.available = dict(available)
        self.reservations: dict[str, tuple[str, int]] = {}
        self.lock = threading.Lock()

    def reserve(self, order_id: str, sku: str, quantity: int) -> bool:
        if not order_id or not sku or quantity <= 0:
            raise ValueError("invalid reservation")
        with self.lock:
            prior = self.reservations.get(order_id)
            if prior is not None:
                if prior != (sku, quantity):
                    raise ValueError("reservation conflict")
                return True
            if self.available.get(sku, 0) < quantity:
                return False
            self.available[sku] -= quantity
            self.reservations[order_id] = (sku, quantity)
            return True

    def release(self, order_id: str) -> None:
        with self.lock:
            reservation = self.reservations.pop(order_id, None)
            if reservation is not None:
                sku, quantity = reservation
                self.available[sku] += quantity
