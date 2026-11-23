import importlib.util
import sys
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).resolve().parents[1] / "scenarios/order_lifecycle/python_events/events.py"
SPEC = importlib.util.spec_from_file_location("order_lifecycle_events", MODULE_PATH)
assert SPEC is not None and SPEC.loader is not None
events = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = events
SPEC.loader.exec_module(events)


class OrderEventTests(unittest.TestCase):
    def test_round_trip(self):
        event = events.OrderCreated("evt-1", "order-1", 1250)
        self.assertEqual(events.OrderCreated.from_json(event.to_json()), event)

    def test_invalid_messages_are_rejected(self):
        for payload in (
            "{}",
            '{"event_id":"","order_id":"order-1","total_cents":1250}',
            '{"event_id":"evt-1","order_id":"order-1","total_cents":0}',
            "not json",
        ):
            with self.subTest(payload=payload), self.assertRaises((ValueError, TypeError)):
                events.OrderCreated.from_json(payload)


if __name__ == "__main__":
    unittest.main()
