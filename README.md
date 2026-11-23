# November 2026 ECG release coverage

This is a local preparation package, not a release certification. The
[traceability matrix](traceability.csv) inventories the named slide scope,
including cases with no fixture yet. Every result is `NOT_RUN` and the release
build is `UNKNOWN`: no fixture has been ingested or evaluated.

## What is here

`fixtures/` contains small, intentionally focused source examples. They cover
one positive shape for EJB calls, JSF EL, Python Azure Service Bus, Mongoose,
GORM, Kotlin Spring, JCL/PL/I, .NET Azure messaging, Rails, Laravel, Axum, a
shared SQL table and several HTTP and data frameworks. They are static analysis
inputs, not deployable applications.
Dependencies are declared where useful to identify frameworks, but have not
been installed or built. A basic positive case is not complete coverage of a
framework or its edge cases; negative controls and variant cases are still
needed. See `NOT_PREPARED` matrix rows for the remaining scope.

[Order lifecycle](scenarios/order_lifecycle/README.md) adds deeper
multi-file examples for the priority release technologies. Its
[assertions](scenarios/order_lifecycle/assertions.json) contain explicit
positive and negative logical graph checks; all remain unexecuted.

Run `python -m unittest discover -s tests` from the repository root to check
matrix structure, referenced fixture directories, source assertion anchors,
event-schema behavior and Python/XML/JSON syntax. These checks do not run ECG
or validate the other source languages against their framework dependencies.

The source-specific rows specify the *logical* facts expected from the graph.
They do **not** assert particular ECG node kinds, node IDs or edge labels:
confirm those against the release's published graph schema and detection
contract before scoring. Some desired relationships may not be promised by the
product, particularly JSF expression resolution, JCL-to-PL/I and cross-source
SQL linking. Mark such checks `BLOCKED` pending a decision rather than
inventing a pass or treating an unspecified behavior as a defect.

## Running later

1. Complete missing fixtures, variants and negative controls. Confirm the
   expected node and edge semantics against the release specification and pin
   their exact forms in the matrix or a separate test definition.
2. Record this repository's exact commit before ingesting it. The public
   repository can be ingested without a GitHub credential. Do not change a
   shared ECG environment without the owner's approval.
3. For R07/R08, ensure the JCL and PL/I files are in the same relevant scope.
   For R11, place the SQL writer and reader in **separate applications and
   sourcesets** that point to the same explicitly identified database/table;
   two files in a single sourceset cannot prove cross-application linking.
4. Ingest the exact commits, record the ECG environment and **actual release
   build**, and collect the graph schema, source-set IDs, nodes and walks. The
   graph evaluator runbook in the ECG evaluation bundle describes graph access
   and the `ecg.sdk.write` permission. Its Python ground-truth generator does
   not validate these other language fixtures.
5. Record an evidence file or report and actual observed nodes and edges for
   each matrix case. Use `PASS` only when every specified positive and negative
   assertion is checked against the pinned build; use `FAIL` for an observed
   contract violation, `BLOCKED` for missing prerequisites or unspecified
   behavior, and `NOT_RUN` otherwise. Do not equate an HTTP 200 or an answer
   quality score with a detection pass.
6. For detection switches, compare identical inputs, build and configuration
   except for the switch. Define canonical output and verify the slide's
   off-equals-baseline requirement for each named switch. The slide does not
   supply the 119+ pattern-family or 41+ switch names, so their authoritative
   inventories are required before individual cases can be planned.

The matrix is a snapshot of preparation, not a history of prior Fineract,
Saleor or OFBiz Q&A runs. Existing historical results must be tied separately
to the relevant fixture/assertion and release build before using them as
evidence.
