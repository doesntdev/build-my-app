# Publish and operate an application

## Before provisioning

Reconcile the accepted ideation and selected stack first; a new AI/data/usage
assumption reopens its feasibility review. Confirm needed accounts, repository
owner/visibility, region, environment, budget ceiling and release authority.
Require an owned domain or controlled email recipient only for features using them.
Read current plan/pricing/quotas; do not promise a permanently free stack. Never
buy a domain, upgrade a plan, create billable services, expose a private repo,
or send real mail without bounded authorization. Read back every external write.

Document missing product capabilities such as authentication, billing, search,
analytics, and independent monitoring. Choose existing/application capabilities
first, or get explicit approval for additional vendors. No hidden sixth SaaS.

## Dependency-ordered bootstrap

1. **Source/work:** approved repository visibility, canonical issue, applicable
   checks/reviews and actual destination controls. Private is the default unless
   public source is requested; preserve the repository's selected release lane.
2. **Cloudflare minimum:** intended account, scoped deployment identity and
   isolated staging/production Worker configuration. Add separate D1 databases
   and private R2 buckets only if needed. Inspect every effective binding, route,
   secret name and remote flag: separate Worker names alone do not isolate data.
3. **Optional managed capabilities:** selected Workflows/Queues/Durable Objects
   or AI need environment separation, permissions, concurrency/retry limits,
   error visibility and reviewed cost controls. Qualify real model quality and
   metering only through a bounded approved experiment, never ordinary unit tests.
4. **Optional Postgres/runtime:** Neon requires sanitized non-production and
   isolated production, committed migrations and verified recovery. Production
   stays outside Neon MCP. Railway is needed only for its selected runtime/worker,
   with explicit source/branch, health/shutdown, secret injection and resource
   limits. Workers + Neon does not require a Railway service.
5. **Optional domain/mail:** read exact provider hostnames/verification values;
   change only intended DNS records, preserve mail records, and verify TLS and
   access controls. For Resend, verify sending domain, runtime sender/key and
   signed webhook; use controlled test recipients with permission.

Record omitted providers as not applicable/deferred with reasons. Do not create
unused infrastructure, demand five MCP connections or invent a domain to publish.

## Choose and prove one artifact path

### Default: Cloudflare Worker and assets

Pin the source, lockfile, compatibility date/flags, build command and approved
Wrangler/provider tool version. Build/test the actual Workers output and asset
manifest locally, then deploy through the chosen authorized source/deployment
lane. Read back the Worker version/deployment, routes/custom domains, asset and
binding identity for the target environment. A successful upload is not acceptance.

Stage the final candidate. If integration changes source/configuration, qualify
the changed result before promotion. Record whether production reuses a qualified
version or rebuilds from the same source; do not claim byte-identical promotion
without evidence. Worker code rollback does not roll back D1 data, R2 objects,
secrets or every binding/resource change. Rehearse recovery for that whole closure.

### Selected container extension: branch-triggered source build

Use the repository's configured Git-linked Railway release branch, normally
`staging` for staging and `main` for production, with required local/deploy-time
checks. Merge through the authorized lane; observe the branch-triggered deployment.
Do not manually deploy/redeploy, pin a commit/image or bypass failed source gates.
Verify the builder's Containerfile path (current Railway config), target architecture
and `.dockerignore` exclusions in actual logs. `.containerignore` alone does not
prove remote secret exclusion and its compatibility filename needs no Docker daemon.

Record exact source and build/deployment identity; test the actual result. A
Railway source rebuild is not promotion of a locally tested OCI digest. OCI image
publication is a separate explicit choice requiring registry visibility, immutable
digest, platform and supported pull credentials; never publish a private image
publicly to bypass auth or manually deploy it to evade the branch lane.

## Migrations and release gates

Use committed migrations and expand/contract compatibility. Apply expand changes
before dependent code; delay drops until old code and backfills are retired.
For D1, rehearse committed SQLite-compatible migrations against local D1 from
empty/prior state, then an isolated remote staging database. Confirm effective
environment/database identity before explicit remote mutations; verify the current
recovery/Time Travel plan and restore procedure. For selected Postgres, use the
needed direct/session migration connection and an isolated sanitized rehearsal
database on the selected data platform; use a Neon branch only when Neon is selected.
Verify recovery coverage and restore before destructive operations in either path.
Make migration locking/concurrency explicit; no multiple replicas racing migrations.

Write the release record from `templates/release-evidence.md`: candidate identity,
verification/review, migration order, config/secret names, staging evidence, owner/approval,
rollback/forward-fix, monitoring and acceptance. Secrets themselves stay in approved
provider secret stores. CI does not depend on interactive MCP OAuth credentials.

## Verify staging and production

Use isolated test principals/data and controlled mail. After each approved write,
read back the exact record/service/deployment/branch. Then check:

- correct commit or digest and environment;
- liveness, bounded readiness, critical user/API flow and persisted state;
- unauthorized, cross-user/cross-tenant and revoked-access failures as applicable;
- actual migration version and compatibility;
- worker backlog/lag, retries and dead letters when applicable;
- DNS, valid HTTPS, proxy/Access/WAF behavior, webhook reachability;
- alternate Worker preview/`workers.dev` route and R2 public-access bypass attempts;
- direct-origin protection if an external origin such as Railway is selected;
- Resend message/event state when mail changed, not just API acceptance;
- redacted logs, errors, latency, resource spend during a defined observation window.
- AI quality, observed tokens/charges versus estimates and server-side user/job/global
  quotas, retry/concurrency limits, atomic spend admission and failure behavior if used.

A provider dashboard green light or health 200 is insufficient. Report the real
user flow and remaining uncertainty. Do not use production test accounts that
could affect real customers or send mail outside the approved recipients.

## Recovery and ongoing ownership

Set failure thresholds before deployment. Stop promotion on failed gates. Roll
back to a known artifact/commit if schema-compatible; otherwise use an approved
forward fix or a rehearsed database recovery procedure. Database restoration can
lose later writes: define RPO/RTO, decision authority and reconciliation.

Assign ownership for logs/metrics/errors, independent uptime, email bounces/
complaints, credential expiry, dependency patches, capacity/cost alerts and restore
drills. Name what is not implemented rather than treating provider dashboards as
complete observability. Prefer events/webhooks and native alerts over custom
polling services. No perpetual agent loop without explicit schedule/scope approval.

Clean up only known owned temporary resources: test branches, staging previews,
Podman test volumes, callback URLs and temporary tunnels. Verify cleanup and retain
needed release evidence. Never delete shared developer data as “test cleanup”.
