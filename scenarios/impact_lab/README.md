# Impact lab

This is a runnable, deliberately synthetic **in-process** service simulation,
not a distributed deployment. `Gateway.submit` calls `OrderService.place_order`;
that orchestrator calls inventory and payment services, then stores an order and
an outbox event in one SQLite transaction. `Relay.publish_pending` publishes via
an injected callback. The tests explicitly wire it to consumers; there is no
actual broker, HTTP route, deployment topology or automatic cross-application
connection in this code.

The flow includes validation, idempotent retries, compensation, transaction
rollback, outbox replay and duplicate suppression. Its `AuditConsumer` accepts
the same topic and event kind as `FulfilmentConsumer` but in a **different
namespace**. The decoy module has same-named unrelated functions. Reporting
reads the order store but is not called by order placement.

Ground truth for impact questions is in `questions.json`. Each case includes
evidence anchors, required facts and forbidden claims. These are source-level
facts and conservative inferences, not a promise about ECG's graph semantics.
In particular, changing the store affects its direct users; it does not mean
every service that the order service calls is a *dependent* of the store.

Run `python -m unittest discover -s tests -v` from the repository root.
The tests execute the scenario in memory; no environment credentials, live
services, cloud resources, network, or external dependencies are required.

Latency measured on this small in-memory fixture is **not** an ECG performance
benchmark. For ECG, record build, ingestion commit, environment, graph query,
worker count, sample size, p50/p95/p99 latency, timeout/error rate, and graph
recall/precision against reviewed ground truth. Agree thresholds before a run.
