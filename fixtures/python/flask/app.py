from flask import Flask

app = Flask(__name__)


@app.get("/release/orders/<order_id>")
def get_order(order_id: str) -> str:
    return order_id
