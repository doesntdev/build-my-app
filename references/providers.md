# Provider contracts and connection verification

The machine-readable endpoints and source links are in `providers.json`.
These recipes were checked against official documentation on 2026-09-16; recheck
before setup. A documented integration is not a live-auth test on this machine.

## GitHub — work ledger and source

- Hosted Streamable HTTP: `https://api.githubcopilot.com/mcp/`.
- Prefer host-native OAuth **when that host's official GitHub integration supports
  it**. Generic OAuth works only with an appropriate registered application;
  the Codex/Claude/Hermes portable baseline is a fine-grained environment-backed PAT.
- Select the user's intended repository/organization, expiration, and only needed
  permissions. Begin with metadata and required read access; add issues/PR writes
  only for an approved SDLC scope. Never default to organization-wide admin scopes.
- Official alternative: GitHub's native MCP binary or the reviewed/pinned
  `ghcr.io/github/github-mcp-server` OCI image under Podman. The current local
  server documents OAuth as well as PAT support; verify its exact login/callback
  requirements rather than copying Docker commands or exposing callback ports.
- Smoke: `get_me`, then read a specific intended repository. Discover current tool
  names. Read-only mode plus token scope is preferable to a prompt-only limit.
- `gh auth status` and `gh repo view` remain useful CLI checks; they do not prove MCP.
- Protect the default branch with available rulesets/checks. Solo repos may need
  a documented self-review policy rather than an impossible second-human approval.
  If a plan lacks protection features, disclose the weaker control; do not claim
  it is enforced. CI gets its own minimal `GITHUB_TOKEN` permissions.

## Neon — non-production MCP, production Postgres

- Hosted Streamable HTTP: `https://mcp.neon.tech/mcp`; OAuth preferred.
- Select non-production projects and sanitized branches only. Neon says its MCP
  is for development/testing. Exclude production data even for “read-only” SQL.
- Smoke: list intended development projects/branches. Do not request or print a
  connection string merely to test connectivity. An empty account list needs
  identity/scope confirmation, not fabricated project evidence.
- Production is accessed through application runtime and reviewed migration
  workflows with separate least-privilege credentials. TLS is required; pooled
  runtime connections and direct/session migration connections when necessary.
- A database branch cloned from production still contains production-sensitive
  data. Prefer separate projects or demonstrably sanitized parents.
- Verify current region, PostgreSQL major, plan limits, retention and recovery
  before choosing paid resources. Never infer PITR coverage from the brand name.

## Railway — runtime, not a second database

- OAuth remote endpoint: `https://mcp.railway.com` (no invented `/mcp` suffix).
- An existing authenticated CLI can serve stdio with `railway mcp`; the current
  docs require CLI 5.44.0+ for this proxy. Verify live version and help. It connects
  to the remote service, not necessarily an in-process server.
- `railway mcp local` is the documented in-process alternative with a different
  tool catalog. Discover actual tools rather than assuming parity.
- `railway login` is user-interactive. Project tokens are not accepted by the MCP
  service; CI uses the provider's supported environment/project-scoped mechanism
  independently of interactive MCP credentials.
- Smoke: `whoami`, then `list-projects` or a scoped service list. Logs can contain
  secrets; retrieve bounded, redacted diagnostics. Avoid raw variable dumps.
- Treat `railway-agent` as a broad delegated operator, not a harmless log reader.
  Deploy/redeploy, accept-deploy, variables, services, domains, and deletions need
  precise targets and approved effects, followed by readback.
- Separate staging/production. Use Neon rather than provisioning Railway Postgres.
  Bind to injected `PORT`, persist uploads outside the ephemeral application disk.

## Cloudflare — DNS and the public edge

- Official API MCP: `https://mcp.cloudflare.com/mcp`, browser OAuth; scoped bearer
  token is available for approved noninteractive use.
- Select only intended accounts/zones and required permissions. Documentation-only
  MCP access is not authenticated account control-plane access.
- Smoke: discover `search` and `execute`, find the current API schema, then run an
  exact **GET** to read the intended account or zone. Never mutate to prove access.
- `execute` can call mutating APIs. A client cannot classify all its JavaScript by
  the tool name; require reviewed methods/paths/payloads and provider least privilege.
- Before DNS writes, read existing records, ownership, TTL/proxy state, and exact
  provider-supplied target. Preserve mail records. Never replace an entire zone.
- Proxied DNS is not origin protection. Test direct Railway origin access; add a
  supported origin-authentication control or disclose the accepted limitation.
- Admin/internal routes can use Access. API/webhook clients may need specifically
  scoped service authentication or bypass rules; test them rather than disabling
  the security layer globally. Keep R2 buckets private when used.

## Resend — transactional email

- Hosted Streamable HTTP: `https://mcp.resend.com/mcp`, OAuth preferred. API-key
  auth exists for headless use; keep it separate from the app's sending identity.
- Smoke: list sending domains or read the selected test domain. No send, contact
  import, API-key creation, domain mutation, or broadcast in onboarding tests.
- Sending-only API keys may not list domains. Report scope limits instead of
  broadening a production key or calling a send to “test” it.
- Verify a user-owned domain or sending subdomain. Copy exact current SPF/DKIM/MX
  records from Resend into Cloudflare, DNS-only. Preserve existing inbound mail
  and avoid conflicting duplicate SPF records. Plan DMARC deliberately.
- Capture mail in local/unit tests; approved provider tests use documented test
  recipients such as `delivered@resend.dev`. A real controlled recipient needs
  explicit permission, and any live key/send can incur cost.
- Use stable idempotency keys for retryable sends. Verify signatures on the raw
  webhook body, replay controls, deduplication, bounce/complaint/suppression handling.
- A returned message ID proves acceptance, not inbox delivery. Read its delivery
  event state; real inbox placement remains distinct from provider “delivered”.
- Runtime sending keys should be least-privilege and domain-scoped where supported.
  Do not use an admin MCP credential as the application's sending key.

## Cross-provider exit

Record configured/connected/authorized/scoped/write-gated separately. An empty
list, provider CLI success, docs page, or missing error is not enough. If a tool
cannot prove identity directly, confirm scope via the authoritative account UI
and one known allowed resource; document the limit. Revalidate at deployment.
