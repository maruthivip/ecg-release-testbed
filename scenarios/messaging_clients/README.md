# Messaging client fixtures

These are independent source fixtures for kafka-python, aiokafka,
confluent-kafka and pika. Their topics differ intentionally: v1, v2 and v3
are not the same Kafka topic. The pika publisher targets an exchange and
routing key; the consumer reads a queue. No exchange-to-queue binding is
declared here, so delivery between them must not be inferred.

Connection settings are supplied by callers; there are no credentials or
brokers included. These files are static-analysis fixtures, not a deployed
system. The questions in `questions.json` record source-based expectations
and negative controls, not observed ECG results. A Kafka commit or AMQP ack
does not guarantee exactly-once processing.

Run the repository unit suite for evidence-anchor checks and stubbed client
behavior tests. Real broker integration and ECG graph assertions remain
unexecuted.
