import threading


class PaymentService:
    def __init__(self, limit_cents: int) -> None:
        self.limit_cents = limit_cents
        self.authorizations: dict[str, int] = {}
        self.lock = threading.Lock()

    def authorize(self, order_id: str, total_cents: int) -> bool:
        if not order_id or total_cents <= 0:
            raise ValueError("invalid payment")
        with self.lock:
            prior = self.authorizations.get(order_id)
            if prior is not None:
                if prior != total_cents:
                    raise ValueError("authorization conflict")
                return True
            if total_cents > self.limit_cents:
                return False
            self.authorizations[order_id] = total_cents
            return True

    def void(self, order_id: str) -> None:
        with self.lock:
            self.authorizations.pop(order_id, None)
