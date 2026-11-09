# Guided, resumable onboarding

## Conversation contract

Make setup feel like an operator sitting beside the user, not a wall of forms.
Inspect first; ask only what cannot be discovered. Group independent questions,
then execute. Explain a new service in one sentence before asking for consent.
Never ask the user to install five things manually when the agent can safely do
that work with an approved package manager and verified commands.

## Stage 0 — agreed idea and stack

Run [ideation](ideation.md) first; reuse its answers instead of duplicating the
interview here. Confirm outcome, workload, technical/scaling/security constraints,
complexity, integrations, development/support burden, cost assumptions and material
risks/trade-offs in the application's evolving root `spec.md`. Capture a
build/prove-first/reshape/defer recommendation for the affected requirements.
Use [stack selection](stack-selection.md)
to record services needed now, exclusions and upgrade triggers. Do not begin five
OAuth flows before discovering whether the project needs those services.

Then ask only remaining setup questions: existing repo or new folder, selected
runtime, local-only or publish, account/organization and release owner, source
visibility, budget authorization, and domain/email only when actually needed.
An owned custom domain is not necessary for a local app or every Workers preview.

Choose low-risk defaults visibly: private repo, loopback local ports, capture mail,
non-production data, modular monolith. Do not invent account IDs or a budget.

## Before local proof — tracker, reviews and branches

Select and verify the issue tracker/project; prefer the existing choice. Follow
[SDLC](sdlc.md) to derive real work items from the accepted spec slice before
implementation. If tracker login is missing, run Stage C for that connection now,
using its supported native/API/CLI path, then return here; optional runtime-service
setup can wait. Verify the intended account/project and actual required access.

Determine team/solo review mode from actual contributors and destination policy,
eligible named reviewers, and persistent dev/staging/main branch/deploy mapping.
Verify review assignment/request capability without test mutations. Resolve missing
branch setup under actual authority and start tracked work from dev; a hosted
tracker is coordination, not an application runtime dependency.

## Stage A — tracked local proof

Inspect the selected runtime, Git and repository. The default local doctor checks
the Cloudflare Git/Node profile, not app health, project-local Wrangler or auth.
Use `--profile container` only when container dependencies are selected. Recommend
current official installation steps only for missing prerequisites; installing
software, starting a VM, or enabling services requires user scope/consent.
Require a tracker-backed work item before implementation, including a local
vertical slice or coding experiment. Use GitHub Issues or the user's selected
real issue tracker and link accepted spec requirement IDs/revision. If tracking
is unavailable, continue ideation and read-only discovery while resolving access;
do not invent an issue or substitute a temporary text backlog. App runtime tests
can remain cloud-independent even when coordination uses a remote tracker.

Exit: tracked runnable local app, deterministic tests, no required runtime-provider credentials.

## Stage B — account and connection inventory

Resolve the active client and profile. Inspect server metadata without dumping
config values or secret files. Include plugin/project/global sources to avoid
duplicates. Reuse a matching official server rather than reauthenticating blindly.

Show a table for selected/considered providers, using Cloudflare as the minimum
runtime recommendation and GitHub or the chosen tracker for work. Neon, Railway,
Resend and a model API are conditional additions, not setup requirements.
Each row has:
needed now / deferred / not applicable; account scope; configured; connected;
authorized; scoped; write gate; next action. `not applicable` needs a reason
(e.g. no email feature). Connect all five only if requested or justified by the
accepted design; otherwise record exclusions without nagging for unused logins.
There is no false claim that deferred equals verified.

## Stage C — connect one provider

1. Verify endpoint/transport/client support against official docs.
2. Resolve precise account/org/project and minimum permissions. If unknown, ask.
3. Explain proposed config path and scope. Obtain approval for this bounded change.
4. Securely back up config outside Git. Backups may contain existing secrets:
   protect them with restrictive permissions and never attach/publish them.
5. Configure and verify client approval controls before connecting, then merge
   one entry through native client tools or a targeted edit. Complete the selected
   client's policy checkpoint; a native add command alone is not a write gate.
   Preserve the complete config and unrelated servers; do not invent universal JSON.
6. Start one OAuth flow. User completes login, MFA and scope consent through the
   provider UI. For tokens, use secure client/OS secret storage or a masked prompt;
   never paste them into conversation, process arguments, or committed files.
7. Reinspect after failed add/login: config can persist even if authentication fails.
8. Reload the client as needed, with approval before restarting shared services.
9. Run tools discovery without invoking provider tools. Enable only necessary
   read-only tools and verify effective provider scopes and client approval/
   allowlist policy without executing a test mutation.
10. Perform one safe account/target read. Verify the returned identity/target
    with the user or previously established authoritative mapping.
11. Record stage evidence and stop stale login listeners. Proceed to next provider.

Exit for each provider: configured → connected → authorized → scoped → write-gated.
A browser opening, OAuth client registration, empty tool list, or CLI exit zero
alone cannot satisfy this ladder. `gh`/provider CLI success is not MCP success.

## State and handoff

Copy `templates/onboarding-state.json` to `.build-my-app/onboarding.json` in the
application, add `.build-my-app/` to `.gitignore`, and store only non-secret evidence.
Use booleans only for observed completed checks; use pending/blocked/deferred for
others. Include timestamp, client, provider, intended environment, safe evidence
summary, fallback, blocker, and next action. Never save tokens, login URLs,
callback codes, environment dumps, private customer data, or connection strings.
Account/resource labels may still be sensitive: keep this record local by default.

For legacy schema-1/2 records, preserve provider evidence, accepted product
decisions, AI findings, old `canonical_issue` links and any `temporary_intake`
content. Reconcile requirements into root `spec.md` and deduplicate unfinished
items into the selected tracker before new implementation. Set the schema-3 spec,
tracker and delivery fields only from observed facts; missing review mode/access
is pending, not solo or verified by default. Reuse valid legacy evidence without
resetting setup, losing saved work or inferring new authority.

On resume, recheck the workspace, identity, target environment, config, current
permissions, and recent remote changes. Reuse valid evidence; stale evidence does
not authorize writes. If the user declines or cancels, stop that flow without
repeated prompts. Continue tracked independent local work when possible, or
ideation/read-only discovery while tracker access is unavailable.

On resume, reconcile spec revision/requirement IDs, selected tracker work,
branch/PR and actual review state. Preserve outcome, acceptance, dependencies,
ownership and valid completion evidence; deduplicate against closed work. Keep
requirements in `spec.md`, execution authority in the charter and progress in
the tracker. A changed requirement reopens affected work/review, not every login.

## Permission model for an agent-operated SDLC

Record the bounded authority in the charter:

- local edits/tests/branches;
- issue/comment/PR writes in specified repositories;
- non-production resource creation with cost/region limits;
- publishing/production actions that still need confirmation.

“Operate my SDLC” can authorize routine work within this scope, not arbitrary
spending, permanent automation, account-wide admin access, real-recipient sends,
or production destruction. Keep user progress visible at meaningful boundaries.

If a connection fails, report the exact stage and safe error category. Use a
supported CLI/API only with equivalent scope and user approval; record MCP as
blocked rather than verified. No substitute integration broker by default.
