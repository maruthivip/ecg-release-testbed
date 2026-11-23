import json
from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class OrderCreated:
    event_id: str
    order_id: str
    total_cents: int

    def to_json(self) -> str:
        return json.dumps(asdict(self), sort_keys=True)

    @classmethod
    def from_json(cls, payload: str) -> "OrderCreated":
        data = json.loads(payload)
        event = cls(**data)
        if not event.event_id or not event.order_id or event.total_cents <= 0:
            raise ValueError("invalid order event")
        return event
