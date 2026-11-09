# Application architecture defaults

Use the agreed [ideation](ideation.md) and [stack recommendation](stack-selection.md).
Start new compatible apps on Cloudflare Workers/Static Assets, D1 for relational
state and private R2 for files only as needed. Preserve existing supported stacks.
Neon/Postgres, Railway and extra Cloudflare services need explicit workload or
security/capability justification; neither user count nor AI alone requires them.

Choose the smallest complete vertical slice that satisfies product, security,
data, latency and recovery constraints. Keep one repo, one authoritative domain
implementation, and one deployable modular monolith; add a worker only for durable
asynchronous work. Extra services/languages/vendors require measured need and a
short architecture decision with trade-offs, owner, and reversal path.

## Secure boundaries

Define authentication before exposing private data. Prefer a maintained framework
or vetted auth library; provider MCP login is not application-user authentication.
Authorize on the server, deny by default, and recheck sensitive actions near the
mutation. Separate runtime, migration, worker, human admin, and CI identities.
Validate inputs, bound output/body/time/concurrency, use TLS remotely, redact logs,
and make credentials revocable. Never trust actor/role/price/result fields supplied
by a client or model as authority.

If the app is multi-user or organizational, make tenant/resource ownership explicit
from the first business table. For multi-tenant data: non-null tenant scope,
tenant-safe foreign keys/uniqueness/cache/object keys, server-verified membership,
a permission catalog, and two-tenant allow/deny tests. With Postgres, use RLS as
defense in depth where practical, testing owner/privileged bypass behavior. D1 is
SQLite-based and does not supply PostgreSQL RLS: scope application queries and
test cross-user/tenant access explicitly. A genuinely
single-user application may record that constraint instead of inventing tenants
and RBAC bureaucracy. Reassess before adding shared data or additional users.

## Atomic state and durable side effects

A command performs one authorized state transition in a database transaction.
Use the selected database's actual atomic API and verify its semantics; do not
copy a Postgres transaction client or `LISTEN/NOTIFY` into D1. D1 batch operations
and supported consistency behavior need real local/runtime tests.
Where the transition requires durable side effects, write its event intent to a
transactional outbox in the **same transaction**. After commit, a worker delivers
it with bounded attempts/backoff; consumers deduplicate with inbox/unique keys.
Use stable idempotency scopes and request identity for retryable external commands.
No claim of cross-process exactly-once delivery. External network calls do not
belong inside the database transaction.

For Cloudflare, use Workflows/Queues only when durable jobs or retries require
them. A D1 commit and a Queue send are not one atomic transaction; preserve event
intent and define recovery for a crash between them. Check per-step/job limits,
duplicate deliveries, idempotency, bounded concurrency, cancellation and dead
letters. Do not replace one durable-work requirement with an unbounded HTTP call.

Default to event-driven triggers, webhooks and push updates instead of application
poll loops. For a PostgreSQL outbox, use wake-up notifications where a verified
session-capable connection supports them; the durable table remains truth.
`LISTEN/NOTIFY` alone is not durable and transaction pooling is not a persistent
listener. Drain pending work on startup/reconnect and define an explicit bounded
reconciliation/retry trigger for missed wakeups. If provider constraints require
periodic scanning, disclose the trade-off and obtain an architecture decision;
do not disguise a polling worker as purely push-based. Add another broker only
when workload evidence justifies it and the user approves the dependency.

Test rollback creates neither state nor event; retries don't duplicate transitions;
concurrent claims use leases/locking safely; crashes allow recovery; replay is
idempotent; dead letters are visible and safely replayable. Version event schemas,
include correlation/causation and needed tenant context, and minimize PII.

## Programmatic interfaces

Meaningful capabilities use versioned application services with thin transport
adapters. Prefer a documented JSON HTTP API with strict schemas, stable errors,
bounded pagination, concurrency preconditions, rate limits and idempotency.
The UI must not be the only home of authorization or business logic.

Provider MCPs are the **operator control plane**. An MCP endpoint **inside the
application** is a separate product decision. Add it when agent/operator access
has real value; don't expose a database administration tool by default. If added,
use the same domain façade/permissions as HTTP, the current MCP authorization
standard, narrow tools, audience-bound tokens, no token passthrough, safe output,
explicit destructive-action controls, cancellation, and real protocol tests.
Record the decision to include/defer application MCP. Never imply provider MCPs
make the application itself MCP-accessible.

## Performance and operations

Set practical acceptance budgets for user-flow latency, critical queries, errors,
resource cost, and event lag when asynchronous work exists. Measure before adding
caches, queues, or microservices. Avoid unbounded queries/logs, N+1 access and
connection storms. Keep liveness dependency-free; make readiness checks bounded
and non-leaking. Plan retention, exports, deletion, and restoration with data
classification and applicable privacy obligations in mind.

## Decision record

Record: constraint → considered alternatives → chosen design → security/data/cost
impact → tests → recovery/rollback → revisit trigger. Use this for auth/tenancy,
new providers, event delivery, public API/MCP, storage and artifact-promotion changes.
Do not require an enterprise architecture dossier for a small non-sensitive app.
