from celery import Celery

app = Celery("release_orders")


@app.task
def process_order(order_id: str) -> str:
    return order_id


def queue_order(order_id: str):
    return process_order.delay(order_id)
