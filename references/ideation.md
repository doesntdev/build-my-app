# Grounded ideation and application feasibility

Read this at the start of every invocation. Help the user discover whether the
application can be built, scaled, secured, paid for and maintained under their
actual constraints. AI is one possible concern, not the organizing principle.
Be an opinionated engineering partner, not a passive feature recorder or a
vendor salesperson. Preserve the intended outcome and explain trade-offs before
they become implementation commitments.

## Run an adaptive conversation

Inspect the workspace and accepted charter first. New ideas get a short discovery
conversation; resume/ship/fix/connect tasks reconcile changed assumptions rather
than replaying discovery. Setup-only tasks need a scoped fit check, not a product
interview. Don't delay urgent authorized incident containment.

Identify the engineering traps yourself using source, tools and documentation;
don't expect the user to diagnose races, database semantics or platform limits.
Ask the user about outcomes, constraints and consequential trade-offs.

Start with who the application serves, the first useful workflow, its quality
bar and the user's constraints. Ask two or three consequential questions at a
time and follow the answers. Reuse information already provided. Do not start
with framework selection, provider logins or a giant questionnaire.

Screen broadly, investigate selectively. The lenses below are **not an exhaustive checklist**
and need not become ten questions for every app. Identify other plausible traps
from the actual proposal. A static portfolio needs a light review; offline
collaboration, financial state or sensitive records needs deeper examination.
Do not invent enterprise requirements or frighten users with unlikely edge cases.

| Lens | What could cause trouble? | Engineering response |
| --- | --- | --- |
| Outcome and product fit | Unclear user, success criterion or first complete workflow; proposed mechanism doesn't solve the need | Define observable acceptance and compare a simpler mechanism without silently cutting the desired outcome |
| Technical feasibility | Unsupported runtime/library/device capability, missing source data, infeasible latency or platform restriction | Verify the actual API/runtime/data path; isolate the decisive technical unknown before building around it |
| Performance | Large payloads, slow critical queries, browser memory, CPU-heavy work, geography or unacceptable waiting | Define response/completion targets; measure a representative path; stream, index or move work off the request only when needed |
| Scalability | Burst/concurrent demand, write hotspots, fan-out, connection/rate limits, growth and retention | Translate active use into requests/jobs/rows/bytes and peak concurrency; find the limiting component rather than invent a user-count threshold |
| Security and privacy | Public uploads, authentication/tenant boundaries, sensitive data, abuse, third-party processing or destructive actions | Identify trust/data boundaries, server-side authorization, secret handling, retention/residency and abuse controls before exposing the affected flow |
| Complexity | Cross-system state, offline merge rules, many moving parts, unclear source of truth, custom infrastructure or operational coupling | Explain the complexity drivers and development burden; prefer one coherent domain and existing capabilities, not a new service per feature |
| Integrations | No supported API, inaccessible scopes, vendor approval, unreliable webhooks, terms/licensing, quotas or incompatible contracts | Prove authorized access and a representative contract; design failure/retry/reconciliation or recommend an honest alternative |
| Correctness and reliability | Duplicate actions, concurrent edits/bookings, partial failures, lost work, migrations or irrecoverable state | Name invariants and failure paths; test atomicity/idempotency, recovery and safe replay before relying on the happy path |
| Development and delivery | Builder skills/time, target platforms, dependency maturity, test data, reproducible setup, account/device access or a critical external approval | Identify critical-path dependencies, testing difficulty and maintenance effort; propose a small end-to-end proof and realistic sequence |
| Cost and resource use | Hosting, storage/operations, network transfer, background work, paid APIs or unbounded anonymous activity | Model cost per useful outcome and expected/growth/burst usage, including fixed charges and enforced limits; include development and support burden |
| Operations | Nobody can support it, invisible failures, no restore path, fragile jobs, expiring credentials or vendor lock-in | Match backups/restore, observability, retention, export and ownership to the risk; no perpetual agent loop by implication |
| Usability and accessibility | Unsupported browser/device, slow network, confusing error/progress/cancellation flows or inaccessible controls | Check the real user environment and failure experience; include relevant accessibility and recovery behavior in acceptance |

For legal, regulatory or contractual uncertainty, identify the issue and the
needed qualified review/approval. Do not claim that choosing a vendor establishes
compliance, rights to data, or permission to scrape/process it.

## Review every meaningful feature

Apply one common loop, whether the feature is file upload, booking, search,
offline sync, payments, an integration, AI or something else:

1. **Clarify the promise:** What outcome, data, quality and response/completion
   time does the user expect? What must still work when demand or inputs change?
2. **Trace the mechanism:** Identify the data source and authority, state changes,
   dependencies, user/tenant boundaries, work per action and delivery path. Where
   can the flow fail, race, fan out or leave partial state?
3. **Find the material constraints:** Ask what breaks first if demand grows,
   inputs are large, a provider is unavailable or a user behaves maliciously.
   Include development difficulty, testing and support, not just the cloud bill.
4. **Ground the concern:** Distinguish observed behavior, documented constraints,
   planning assumptions and unverified unknowns. Consult relevant source/runtime
   evidence or official provider documentation. Don't present an assumption as
   a measured bottleneck, a confident effort estimate or a proved impossibility.
5. **Explain and recommend:** Describe the user/development consequence, a
   practical approach and credible alternatives. Separate necessary complexity
   from accidental complexity; name any requirement a simpler option drops.
6. **Resolve the next step:** Agree to build, prove first, reshape or defer the
   affected feature. Define the cheapest decisive experiment, its acceptance,
   owner and scope. Confirm material trade-offs, not each routine safe action.

## Explain the consequence now

Surface a material feasibility/security/scalability/complexity/cost issue as soon
as it emerges, **before** unrelated feature ideation or treating the affected
feature as accepted. Don't save a predictable development trap for deployment.
Use plain language: "This needs conflict resolution when two offline users edit
the same item; otherwise the last sync can overwrite their work. Here is the
simplest safe rule, what it sacrifices, and a small test we can run."

Keep the response useful: concern -> concrete impact -> evidence or uncertainty
-> recommendation/options -> next decision or experiment. A risk label without
an actionable response does not help the user. Rank concerns by plausible impact,
likelihood and when they need resolution. Don't drown out a decisive blocker with
minor issues, and don't promise that an interview catches every future problem.

Unknown is allowed. Use an explicit range or bounded experiment when evidence
is incomplete. Resolve high-impact uncertainty before expensive/dependent work;
continue independent safe work where possible. Unverified integration access is
not an accepted architecture, but it need not block an unrelated local screen.
A small budget or deadline never waives essential security or data correctness.

## Workload, cost and development burden

Calculate relevant quantities with a tool rather than intuiting scale from user
count. A useful starting model is:

```text
monthly_actions = active_users * actions_per_user_per_month
monthly_cost = fixed_plan_costs + sum(billable_usage_by_service * applicable_rate)
peak_work = peak_arrival_rate * work_per_action
retained_data = data_created_per_period * retention_period
```

Use matching time periods and explicit units in these estimates. Adapt units to
the actual workload: requests, CPU time, rows scanned/written,
file bytes and storage operations, transfer, messages, media minutes or model
tokens. Model average and burst concurrency separately; include retries,
failures, backfills, fan-out and support work. Don't assume all registered users
are active or that linear scaling holds past a component's limit. Avoid
multiplying rounded estimates into false precision.

Use current official prices/limits with source URL, date checked, units and
account/plan assumptions. Show per useful outcome/user/month where relevant,
plus growth and abuse/burst cases. A free allowance is conditional; an alert is
not a spend cutoff. Bound resource use, admissions, concurrency, storage/retention
and retries as the feature requires. If live evidence is unavailable, mark it
unverified and keep dependent decisions provisional instead of inventing a quote.

Also discuss implementation, debugging, test environments, migration, moderation,
operations and long-term maintenance. Label effort ranges and their assumptions;
do not equate low hosting cost or low code volume with an easy application.
Who must do the work, which external dependency can delay it, and how will the
user know the feature is genuinely working?

## Find the development traps

These examples illustrate the same process, not special privileges for one
technology. Explore only branches relevant to the proposal:

| Proposed feature | Explore before accepting it | Useful first proof or simpler option |
| --- | --- | --- |
| Offline inventory sync | Concurrent edits, deletions, identity, authoritative state and conflict policy | Two clients edit the same item offline, reconnect and exercise the agreed merge rule; alternatively start online-only with that limitation explicit |
| Last-seat booking or payments | Competing claims, duplicate submissions, expiry, webhook order, refunds and reconciliation | Race two clients and replay callbacks against isolated fixtures; use a provider-hosted payment flow where suitable, never client state as the ledger |
| Unavailable third-party API or scraping | Real authorized API/scope access, provider terms, data ownership, quotas, schema changes and fallback | Read current docs and prove one permitted integration contract or an approved manual import; don't build around an invented endpoint |
| Large public uploads/media | Size/frequency/retention, interrupted transfer, scanning/moderation, authorization, egress and storage cost | Bounded resumable upload plus private access and lifecycle tests; don't buffer the entire file in a request/browser or expose a public bucket by default |
| Large reports or CPU-heavy processing | Dataset/job size, query shape, memory/runtime limits, native dependencies, progress and cancellation | Run one representative dataset through the selected local runtime; consider chunked/background work before choosing new services |
| Solo weekend build with many coupled features | Available time/skills, integration approvals, testability, critical path and continuing support | Keep the full ambition visible, agree an achievable vertical slice and separately name what is deferred; don't promise the whole product because a scaffold is quick |
| Sensitive multi-user records | Identity, tenant isolation, access revocation, retention, export/deletion and residency | Two-user/tenant allow/deny and recovery tests with synthetic data before exposing real records |
| AI/LLM component | Task/quality, inputs/outputs, privacy, call volume, output/rate limits, latency, per-outcome economics and control | Read [AI feasibility](ai-feasibility.md) only for this branch; validate a bounded quality sample with consent before scaling paid inference |

Use the same logic for other concerns: search relevance, notification delivery,
mobile/device support, high availability, data imports, external automation or
whatever the actual idea depends on. Not mentioning AI must never skip the review.

## Ready to build

Give a short **feasibility recommendation**, not a sales pitch: accepted user
outcome and first slice; constraints/workload; main development and operational
risks; evidence versus unknowns; complexity and cost drivers; minimum stack;
trade-offs; next proof and concrete revisit triggers. The disposition can be:

- **Build:** enough evidence to implement the bounded slice with known safeguards.
- **Prove first:** resolve a decisive unknown through a small experiment first.
- **Reshape:** recommend a different mechanism, sequence or explicit scope change.
- **Defer:** keep the ambition visible but don't commit until a blocker is resolved.

Different features may have different dispositions. Hold only the unsafe or
unproved dependent work, not the whole project by default. Confirm consequential
choices with the user; don't silently accept a risk or replace their idea.

Record only material risks in the [charter](../templates/project-charter.md) and
non-secret onboarding state: concern, user/development impact, evidence/unknown,
severity, recommendation, validation/mitigation, owner/next step and disposition
(resolved, accepted, experiment, deferred or blocked). A small project needs a
short list, not a new governance system. Unresolved acceptance work belongs in
the existing issue workflow once connected, not a competing backlog.

Revisit affected risks when scope, platform, integrations, complexity, workload,
data sensitivity, budget or delivery constraints change, and when actual tests
contradict planning assumptions. Compare observed behavior/cost with estimates;
check failure paths as well as the happy path. Reuse valid evidence and don't
replay the whole interview for an unchanged fix or approved release.
