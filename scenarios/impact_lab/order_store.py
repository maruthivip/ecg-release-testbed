import json
import sqlite3
import threading

from .contracts import Event, OrderRequest


class OrderStore:
    def __init__(self) -> None:
        self.lock = threading.Lock()
        self.db = sqlite3.connect(":memory:", check_same_thread=False)
        self.db.executescript(
            """
            CREATE TABLE orders (
                order_id TEXT PRIMARY KEY, sku TEXT NOT NULL,
                quantity INTEGER NOT NULL, total_cents INTEGER NOT NULL
            );
            CREATE TABLE outbox (
                event_id TEXT PRIMARY KEY, order_id TEXT NOT NULL,
                namespace TEXT NOT NULL, topic TEXT NOT NULL,
                payload TEXT NOT NULL
            );
            """
        )

    def save_with_event(self, order: OrderRequest, event: Event) -> None:
        with self.lock, self.db:
            self.db.execute(
                "INSERT INTO orders VALUES (?, ?, ?, ?)",
                (order.order_id, order.sku, order.quantity, order.total_cents),
            )
            self.db.execute(
                "INSERT INTO outbox VALUES (?, ?, ?, ?, ?)",
                (event.event_id, event.order_id, event.namespace, event.topic,
                 json.dumps({"kind": event.kind, "version": event.version})),
            )

    def get(self, order_id: str) -> tuple | None:
        with self.lock:
            return self.db.execute(
                "SELECT order_id, sku, quantity, total_cents FROM orders WHERE order_id = ?",
                (order_id,),
            ).fetchone()

    def events(self) -> list[Event]:
        with self.lock:
            rows = self.db.execute(
                "SELECT event_id, order_id, namespace, topic, payload FROM outbox ORDER BY event_id"
            ).fetchall()
        return [
            Event(event_id, order_id, namespace, topic, data["kind"], data["version"])
            for event_id, order_id, namespace, topic, payload in rows
            for data in [json.loads(payload)]
        ]
