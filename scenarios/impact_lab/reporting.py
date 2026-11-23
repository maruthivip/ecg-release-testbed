from .order_store import OrderStore


def lookup_order(store: OrderStore, order_id: str) -> tuple | None:
    return store.get(order_id)
