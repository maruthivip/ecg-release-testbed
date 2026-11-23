from .contracts import OrderRequest
from .order_service import OrderService


class Gateway:
    def __init__(self, orders: OrderService) -> None:
        self.orders = orders

    def submit(self, order: OrderRequest) -> str:
        return self.orders.place_order(order)
