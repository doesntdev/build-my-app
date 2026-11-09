# Recommend a stack that grows with the workload

Use after ideation and before setup. A stack is a recommendation based on the
current workload, not a graduation ladder every project must climb. The minimum
recommended hosted platform is **Cloudflare**. Use its relevant services before
adding another vendor, unless a verified requirement or existing investment
makes another choice better. Security and recovery requirements can justify a
different starting point even at low traffic; small does not mean low risk.

## Start with Cloudflare, provision only what is used

| Capability | Minimum recommendation | Evidence to check |
| --- | --- | --- |
| Static site or SPA | Workers Static Assets; Worker API only if needed | Routing, caching, asset limits, framework support |
| Dynamic HTTP/API | Workers in a supported language/framework | Runtime APIs, library compatibility, CPU/memory, request limits and latency |
| Structured persistent data | D1 (SQLite-based) when needed | Schema/query/transaction fit, per-database limits, rows scanned/written, recovery |
| Uploads, downloads, generated files | Private R2 when needed; Static Assets for bundled public files | File/operation volume, lifecycle/retention, access control, total charges |
| Local loop | Project-local Wrangler/workerd and local bindings | No remote bindings or production secrets; dependency/runtime compatibility |
| Source and coordination | Git; GitHub Issues/PRs when connected | User's repository, visibility and actual workflow policy |

A brochure site needs no SQL database. A CRUD app without files needs no R2.
Do not provision D1/R2 just because they appear in the baseline. R2 is not a SQL
database; KV is not a general replacement for transactional authoritative data.
Cloudflare hosting does not supply end-user authentication or application tenant
isolation automatically. Workers Static Assets is sufficient for bundled public
assets; never put private documents in a publicly served asset directory.

For a new app with no constraints, prefer a small supported Workers-compatible
modular application with one domain implementation and thin UI/API adapters.
Keep an existing supported framework, package manager and tested dependencies.
Don't rewrite a working application, downgrade Postgres to SQLite, or change
hosting just for stylistic consistency. Name any mismatch and migration cost.

## Escalation options, not mandatory tiers

| Add/change | Trigger | Do not add it merely because |
| --- | --- | --- |
| Paid Cloudflare plan/capacity | Documented free limits, required features or expected usage justify its minimum plus metered cost | The product might have users someday |
| Workflows and/or Queues | Durable multi-step jobs, controlled fan-out, retries and background delivery | A request makes one quick API call |
| Durable Objects | Per-entity coordination, realtime state or atomic admission that needs its model | Any app has more than one user |
| KV/cache | Measured cache/read benefit with acceptable consistency/staleness | It is in the service catalog |
| Workers AI or an external model API | A defined AI task passes quality, privacy, latency and unit-economics review | AI appears in the pitch or a model has the lowest sticker price |
| Vectorize/search service | Retrieval requirements and a representative relevance test exceed simpler indexed/search options | The app uses an LLM |
| Neon Postgres, optionally via Hyperdrive from Workers | Required Postgres features/extensions/tooling, data shape/size, recovery needs or measured D1 write/concurrency limits | Registered users pass an invented threshold |
| Railway runtime/worker | Required native library/process, long-running compute or always-on service does not fit a verified Workers/Workflows design | D1 was replaced by Postgres |
| Resend | Real transactional mail is an accepted feature | Login and five-vendor onboarding were inherited defaults |
| Another provider | Specific unmet requirement and a reviewed, approved substitution | A starter template mentions it |

These are composable choices. Workers + Neon can be enough without Railway;
Workers + D1 + Queues can be enough without Postgres. A container app may keep
Cloudflare at the edge and private R2 while using Neon/Railway. Each added service
needs an explicit purpose, current cost, authority, operational owner and revisit
trigger. Do not build the eventual migration architecture before the first slice.

## Check platform fit and delivery risk

1. **Performance:** Set user-flow targets, payload/job size and geographical
   assumptions. Test a representative critical query and path. Edge placement is
   not a guarantee of low latency to a central database or external model. CPU
   execution time is not identical to network wait time. Cache only appropriate
   public or correctly isolated data; don't hide an unbounded query behind a cache.
2. **Security:** Identify user/tenant authorization, secret boundaries, uploads,
   data location/retention and third-party AI processing. Protect private R2 through
   server checks or bounded scoped access. D1 does not provide PostgreSQL RLS:
   enforce ownership in application queries and test two-user/tenant denial paths.
   Cloudflare Access can protect operator routes; it is not automatically the
   product's consumer identity system. Use proportionate abuse/rate controls.
3. **Scale:** Model requests/jobs per user, peak concurrency, DB read/write shape,
   largest dataset/file, retention and growth. D1's per-database write/processing
   characteristics, SQL features and current size limits matter more than a
   marketing user count. Read replication does not remove write bottlenecks.
   Optimize/index/measure before introducing sharding or a database migration.
4. **Cost:** Separate fixed plans from metered CPU/requests, scanned/written rows,
   storage/operations, queues, inference, email and external data transfer. Price
   expected/growth/burst cases using current units and actual plan allowances.
   A free plan may reject excess work; a paid plan may bill overages. Set quotas
   and budgets rather than assuming the provider will cap the invoice.
5. **Feasibility and complexity:** Verify needed APIs, libraries, data access and
   target-device/runtime support. Include integration approval, state/consistency
   rules, development/test difficulty, deployment/recovery and the user's ability
   to operate it. A low monthly bill does not justify a stack that makes the
   product impossible or fragile to deliver. Use the broader [ideation review](ideation.md)
   for risks outside platform choice; add services only when they solve a real need.

A known incompatibility, regulatory boundary or recovery requirement can justify
an upgrade before a load test. Otherwise prefer a small experiment to a guessed
threshold. Do not promise that Cloudflare will fit every hobby project, nor that
leaving it is required to become a serious application.

## Record the recommendation and revisit triggers

Use the charter, not a separate heavyweight architecture dossier:

- Selected services, their purpose and why each is needed now.
- Alternatives considered and services intentionally excluded/not applicable.
- Launch and growth demand, measured or estimated bottleneck and confidence.
- Current pricing/limits source URLs and date checked; unresolved questions.
- Security/latency/quality/cost trade-offs the user accepted.
- Specific revisit trigger and next action, e.g. sustained write latency exceeds
  the agreed target, data nears a current per-database limit, required SQL feature
  is absent, or cost per completed job exceeds the product's budget.
- Migration/recovery outline only as detailed as that risk needs.

"Scale later" without a trigger is not a plan. "Add Postgres at 1,000 users" without
an actual workload model is not evidence. Continue with the chosen subset's local,
provider and publishing paths; do not offer five logins as a compulsory bundle.

## Primary references

Reviewed for this recommendation on 2026-11-09. Recheck for each real design:

- [Workers Static Assets](https://developers.cloudflare.com/workers/static-assets/)
- [Workers limits](https://developers.cloudflare.com/workers/platform/limits/)
- [Workers pricing](https://developers.cloudflare.com/workers/platform/pricing/)
- [Workers local development](https://developers.cloudflare.com/workers/local-development/)
- [D1 local development](https://developers.cloudflare.com/d1/best-practices/local-development/)
- [D1 limits](https://developers.cloudflare.com/d1/platform/limits/)
- [D1 pricing](https://developers.cloudflare.com/d1/platform/pricing/)
- [R2 pricing](https://developers.cloudflare.com/r2/pricing/)
- [Workflows limits](https://developers.cloudflare.com/workflows/reference/limits/)
- [Workers AI pricing](https://developers.cloudflare.com/workers-ai/platform/pricing/)

These are documentation sources, not authenticated account, live capacity,
quality or deployment proof. Check account-specific plans and selected features.
