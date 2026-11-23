import sqlite3
import unittest
from concurrent.futures import ThreadPoolExecutor
from unittest.mock import patch

from scenarios.impact_lab.contracts import Event, OrderRequest
from scenarios.impact_lab.event_relay import AuditConsumer, FulfilmentConsumer, Relay
from scenarios.impact_lab.gateway import Gateway
from scenarios.impact_lab.inventory_service import InventoryService
from scenarios.impact_lab.order_service import OrderService
from scenarios.impact_lab.order_store import OrderStore
from scenarios.impact_lab.payment_service import PaymentService
from scenarios.impact_lab.reporting import lookup_order


class ImpactLabTests(unittest.TestCase):
    def setUp(self):
        self.inventory = InventoryService({"SKU-1": 10})
        self.payment = PaymentService(5000)
        self.store = OrderStore()
        self.service = OrderService(self.inventory, self.payment, self.store)
        self.gateway = Gateway(self.service)
        self.order = OrderRequest("O-1", "SKU-1", 2, 1200)

    def tearDown(self):
        self.store.db.close()

    def test_gateway_success_and_duplicate_request(self):
        self.assertEqual(self.gateway.submit(self.order), "accepted")
        self.assertEqual(self.gateway.submit(self.order), "accepted")
        self.assertEqual(self.inventory.available["SKU-1"], 8)
        self.assertEqual(self.payment.authorizations, {"O-1": 1200})
        self.assertEqual(lookup_order(self.store, "O-1"), ("O-1", "SKU-1", 2, 1200))
        self.assertEqual(len(self.store.events()), 1)

    def test_conflicting_order_rejected_without_new_side_effects(self):
        self.gateway.submit(self.order)
        with self.assertRaisesRegex(ValueError, "order conflict"):
            self.gateway.submit(OrderRequest("O-1", "SKU-1", 3, 1200))
        self.assertEqual(self.inventory.available["SKU-1"], 8)
        self.assertEqual(len(self.store.events()), 1)

    def test_concurrent_duplicate_submissions_share_one_result(self):
        with ThreadPoolExecutor(max_workers=8) as pool:
            results = list(pool.map(self.gateway.submit, [self.order] * 16))
        self.assertEqual(results, ["accepted"] * 16)
        self.assertEqual(self.inventory.available["SKU-1"], 8)
        self.assertEqual(len(self.store.events()), 1)

    def test_relay_propagates_publisher_failure(self):
        self.gateway.submit(self.order)

        def failing_publisher(event):
            raise RuntimeError("broker unavailable")

        with self.assertRaisesRegex(RuntimeError, "broker unavailable"):
            Relay(self.store).publish_pending(failing_publisher)
        self.assertEqual(len(self.store.events()), 1)

    def test_out_of_stock_does_not_authorize_or_persist(self):
        self.assertEqual(self.gateway.submit(OrderRequest("O-2", "SKU-1", 20, 1200)), "out_of_stock")
        self.assertFalse(self.payment.authorizations)
        self.assertIsNone(self.store.get("O-2"))
        self.assertEqual(self.store.events(), [])

    def test_declined_payment_releases_inventory(self):
        self.assertEqual(self.gateway.submit(OrderRequest("O-2", "SKU-1", 2, 6000)), "payment_declined")
        self.assertEqual(self.inventory.available["SKU-1"], 10)
        self.assertIsNone(self.store.get("O-2"))
        self.assertEqual(self.store.events(), [])

    def test_authorization_exception_releases_inventory(self):
        with patch.object(self.payment, "authorize", side_effect=RuntimeError("unavailable")):
            with self.assertRaisesRegex(RuntimeError, "unavailable"):
                self.gateway.submit(self.order)
        self.assertEqual(self.inventory.available["SKU-1"], 10)
        self.assertEqual(self.store.events(), [])

    def test_outbox_insert_failure_rolls_back_order_and_compensates(self):
        original = Event("O-1:created:v1", "other", "x", "y", "x", 1)
        self.store.db.execute(
            "INSERT INTO outbox VALUES (?, ?, ?, ?, ?)",
            (original.event_id, original.order_id, original.namespace, original.topic, "{}"),
        )
        self.store.db.commit()
        with self.assertRaises(sqlite3.IntegrityError):
            self.gateway.submit(self.order)
        self.assertIsNone(self.store.get("O-1"))
        self.assertEqual(self.inventory.available["SKU-1"], 10)
        self.assertEqual(self.payment.authorizations, {})

    def test_event_replay_and_namespace_trap(self):
        self.gateway.submit(self.order)
        fulfilment, audit = FulfilmentConsumer(), AuditConsumer()
        relay = Relay(self.store)
        relay.publish_pending(fulfilment.handle)
        relay.publish_pending(fulfilment.handle)
        relay.publish_pending(audit.handle)
        self.assertEqual(fulfilment.orders, ["O-1"])
        self.assertEqual(audit.processed, set())
        self.assertTrue(audit.handle(Event("audit-1", "O-1", "audit-sandbox", "order-events", "order.created", 1)))
        self.assertEqual(fulfilment.orders, ["O-1"])

    def test_invalid_input_never_reserves(self):
        with self.assertRaisesRegex(ValueError, "invalid order"):
            self.gateway.submit(OrderRequest("O-1", "SKU-1", 0, 1200))
        self.assertEqual(self.inventory.available["SKU-1"], 10)


if __name__ == "__main__":
    unittest.main()
