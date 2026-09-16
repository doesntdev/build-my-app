# Publish and operate an application

## Before provisioning

Confirm chosen accounts, repository owner/visibility, region, environment,
owned domain, controlled email recipient, budget ceiling, and release authority.
Read current plan/pricing/quotas; do not promise a permanently free stack. Never
buy a domain, upgrade a plan, create billable services, expose a private repo,
or send real mail without bounded authorization. Read back every external write.

Document missing product capabilities such as authentication, billing, search,
analytics, and independent monitoring. Choose existing/application capabilities
first, or get explicit approval for additional vendors. No hidden sixth SaaS.

## Dependency-ordered bootstrap

1. **GitHub:** approved repo visibility, canonical issue, protected default branch,
   CI checks and minimal environment-scoped secrets. Private is the default unless
   public source is requested. Verify permissions and rule availability.
2. **Neon:** sanitized development/staging and isolated production, compatible
   PostgreSQL major/region, least-privilege runtime/migration identities, committed
   migrations, verified recovery coverage. Obtain secret URLs through protected
   channels without returning them to chat. Production is outside Neon MCP.
3. **Railway:** separate environments/services for web and worker if needed,
   explicit deploy source, `PORT`, health checks, environment secret injection,
   restart/shutdown behavior, logs and resource/budget limits. Use Neon for data.
4. **Cloudflare:** read exact Railway hostname/verification requirements, create
   only intended records, verify proxied HTTPS and origin protection. Never guess
   CNAME values, bypass requirements, apex support, or current certificate state.
5. **Resend:** if the app sends mail, verify a user-owned sending domain/subdomain
   using exact Resend DNS values, set runtime key/sender and signed webhook,
   verify controlled provider test behavior. Real recipient testing is approved.

For an app without email or uploads, defer Resend/R2 and record why. Offer the MCP
setup but do not create unused billable infrastructure just to tick a box.

## Choose and prove one artifact path

### Preferred: immutable OCI promotion

Build the production `Containerfile` with Podman in CI, push to GHCR under an
approved visibility, capture the immutable digest, target architecture, scan/SBOM
and provenance evidence. Deploy that exact digest to staging and production where
Railway's current image source supports it. Verify private-registry plan support
and a scoped read credential before adopting this path. If CI cannot run Podman,
use a supported runner or document the blocker rather than sneaking in a Docker
daemon. Do not publish private application images publicly to bypass pull auth.

Test the final artifact, not only the pre-merge code. If merge/rebase changes the
candidate, build once again and restage that **new final artifact** before promotion.
Verify Railway's source resolves to the intended digest, not just a mutable tag.

### Explicit alternative: Railway GitHub source build

Enable and verify **Wait for CI** for the intended branch, including a push CI
workflow on that branch. Set the remote builder's custom Containerfile path
(`RAILWAY_DOCKERFILE_PATH=Containerfile` or current config-as-code equivalent),
and equivalent `.dockerignore` exclusions for secrets. Verify builder selection
in actual logs. A local `.containerignore` is not proof of remote exclusion.

Record the exact source commit and Railway build/deployment ID. Railway rebuilds
from source: this is **not** promotion of the Podman/GHCR digest. Stage and validate
the resulting Railway artifact; document the weaker reproducibility/rebuild
boundary and rollback method. Do not label a newly rebuilt production artifact
“the identical tested image” without provider evidence.

## Migrations and release gates

Use committed migrations and expand/contract compatibility. Apply expand changes
before dependent code; delay drops until old code and backfills are retired.
Use direct/session connections if the migration runner needs them. Rehearse from
empty schema and from sanitized prior schema on a disposable Neon branch. Verify
PITR/backup coverage and perform a restore rehearsal before destructive operations.
Make migration locking/concurrency explicit; no multiple replicas racing migrations.

Write the release record from `templates/release-evidence.md`: candidate identity,
CI/review, migration order, config/secret names, staging evidence, owner/approval,
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
- direct-origin bypass attempt and the resulting control or disclosed limitation;
- Resend message/event state when mail changed, not just API acceptance;
- redacted logs, errors, latency, resource spend during a defined observation window.

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
