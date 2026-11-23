# Order lifecycle: multi-language static-analysis scenario

This scenario adds a deeper set of linked source shapes around a common
order-processing domain. It is **not** a deployable enterprise system: the
components are deliberately independent examples, with no infrastructure,
end-to-end transport wiring, or demonstrated cross-application ECG links.
Their shared domain vocabulary alone must never be treated as evidence of a
call or message edge. The TypeScript topic publisher and Python subscription
receiver use the same literal topic and compatible event fields, but have not
been connected to an actual broker or run together.

| Component | Real source paths exercised |
|---|---|
| `java_legacy` | JSF form, AJAX, EL property/action, EJB local interface injection, two bean calls and transaction annotation |
| `typescript_orders` | Express router prefix, create/read endpoints, separate Mongoose model and repository, explicit collection, chained read and update, and a standalone topic publisher |
| `python_events` | Azure Service Bus topic sender, subscription receiver, message metadata, completion and invalid-message dead-lettering |
| `go_inventory` | GORM model with explicit table name, context propagation, transactional insert, chained query and HTTP handler |
| `kotlin_orders` | Spring class-level prefix, GET/POST mappings and constructor-injected service calls |
| `mainframe` | Two-step conditional JCL with a temporary dataset, distinct DD bindings and two PL/I programs |

`assertions.json` records logical positive and negative relationships, source
and target file anchors, and the corresponding release matrix row. The anchors
are source truth, **not ECG node IDs**; they must be mapped to the observed
graph and the published release contract before execution. Checks for absent
edges use unrelated same-named functions or distinct JCL step scopes.

The local tests ensure each anchor exists and the synthetic event schema
round-trips; they do not prove ECG recognizes these cases, that external
frameworks compile, or that the components can run together. Capture actual
graph responses and exact product build alongside any future verdict.

Ingest the committed repository as a source to inspect intra-source facts.
For cross-application tests, provision separately addressable sourcesets with
explicitly wired producer and consumer code or shared-resource configuration,
including broker namespace and topic identity.
Subdirectories within a single ingestion do not prove cross-application
behavior, and the current scenario does not provide that configuration.
