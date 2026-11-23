from fastapi import FastAPI

app = FastAPI()


@app.get("/release/orders/{order_id}")
def get_order(order_id: str) -> str:
    return order_id
