import asyncio
import importlib.util
import json
import sys
import types
import unittest
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch


ROOT = Path(__file__).resolve().parents[1] / "scenarios" / "messaging_clients"


def load_fixture(name, dependency):
    module_name = {"kafka_python": "kafka", "aiokafka": "aiokafka",
                   "confluent_kafka": "confluent_kafka", "pika": "pika"}[name]
    with patch.dict(sys.modules, {module_name: dependency}):
        spec = importlib.util.spec_from_file_location(f"fixture_{name}", ROOT / name / "orders.py")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
    return module


class MessagingFixtureTests(unittest.TestCase):
    def test_kafka_publish_waits_and_closes(self):
        producer = MagicMock()
        dependency = types.SimpleNamespace(KafkaProducer=MagicMock(return_value=producer),
                                           KafkaConsumer=MagicMock())
        fixture = load_fixture("kafka_python", dependency)
        fixture.publish_order("broker", "order-1", 2)
        args, kwargs = producer.send.call_args
        self.assertEqual(args[0], "orders.created.v1")
        self.assertEqual(kwargs["key"], b"order-1")
        self.assertEqual(json.loads(kwargs["value"]), {"order_id": "order-1", "attempt": 2})
        producer.send.return_value.get.assert_called_once_with(timeout=5)
        producer.close.assert_called_once()

    def test_kafka_parse_error_closes_without_commit(self):
        consumer = MagicMock()
        consumer.__iter__.return_value = [types.SimpleNamespace(value=b"{}")]
        dependency = types.SimpleNamespace(KafkaProducer=MagicMock(),
                                           KafkaConsumer=MagicMock(return_value=consumer))
        fixture = load_fixture("kafka_python", dependency)
        with self.assertRaises(KeyError):
            fixture.read_orders("broker")
        consumer.commit.assert_not_called()
        consumer.close.assert_called_once()

    def test_aiokafka_publish_stops_on_send_failure(self):
        producer = types.SimpleNamespace(start=AsyncMock(), stop=AsyncMock(),
                                         send_and_wait=AsyncMock(side_effect=RuntimeError("failed")))
        dependency = types.SimpleNamespace(AIOKafkaProducer=MagicMock(return_value=producer),
                                           AIOKafkaConsumer=MagicMock())
        fixture = load_fixture("aiokafka", dependency)
        with self.assertRaisesRegex(RuntimeError, "failed"):
            asyncio.run(fixture.publish_order("broker", "order-1"))
        producer.stop.assert_awaited_once()

    def test_confluent_reports_failed_delivery(self):
        producer = MagicMock()
        producer.flush.return_value = 1
        dependency = types.SimpleNamespace(Producer=MagicMock(return_value=producer),
                                           Consumer=MagicMock(), KafkaException=RuntimeError)
        fixture = load_fixture("confluent_kafka", dependency)
        with self.assertRaisesRegex(RuntimeError, "remaining=1"):
            fixture.publish_order("broker", "order-1")
        self.assertEqual(producer.produce.call_args.args[0], "orders.created.v3")

    def test_pika_rejects_bad_message_without_ack(self):
        channel = MagicMock()
        channel.basic_get.return_value = (types.SimpleNamespace(delivery_tag=7), None, b"{}")
        connection = MagicMock()
        connection.channel.return_value = channel
        fixture = load_fixture("pika", types.SimpleNamespace(BlockingConnection=object))
        with self.assertRaises(KeyError):
            fixture.consume_one(connection)
        channel.basic_nack.assert_called_once_with(delivery_tag=7, requeue=False)
        channel.basic_ack.assert_not_called()


if __name__ == "__main__":
    unittest.main()
