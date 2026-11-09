# Application specification

Copy/adapt this to the application's root `spec.md` and update it throughout
ideation with the user. Start as **Draft**. Record accepted requirements and
explicit unknowns as decisions emerge; don't fill gaps with invented approval.
This is the requirements source, **not a task backlog**. The selected issue
tracker owns implementation status, claims, assignments, PRs and delivery progress.

## Outcome and users

- Intended users, problem and current workaround:
- First useful end-to-end outcome and observable success:
- Intended longer-term ambition and accepted first slice:
- Non-goals and explicitly deferred scope:

## Requirements and Acceptance

Use stable requirement IDs such as `REQ-001` for functional and non-functional
requirements. Preserve IDs across edits and retire rather than recycle them.
Use Draft / Accepted / Deferred with the user's decision context, not a guessed
implementation status. Each accepted requirement needs testable acceptance,
including relevant negative/failure behavior and constraints.

| Requirement ID | Requirement / user outcome | Decision status | Acceptance and failure paths | Dependencies / risks |
| --- | --- | --- | --- | --- |

## Workload, performance and scalability

- Active users, frequency, payload/data/job shape, burst/peak concurrency:
- Response/completion targets, growth/retention assumptions and evidence:
- Critical bottlenecks, provider/runtime limits, capacity proof and upgrade triggers:

## Security, privacy and correctness

- Data classification/location/retention, authentication and user/tenant access:
- Trust boundaries, abuse controls, secrets and external processing:
- Invariants, concurrent changes, retry/idempotency, partial failure and recovery:
- Data rights, licenses, applicable regulatory review and unresolved approvals:

## Feasibility, complexity and delivery constraints

- Technical/platform/data/API access assumptions and evidence:
- Integration dependencies and critical path:
- Complexity drivers, builder time/skills, target devices and test environments:
- Material risk, user/development impact, recommendation, next proof and owner:
- Build / prove first / reshape / defer decisions and accepted limitations:

## Recommended architecture and economics

- Selected stack/services and why each is needed now; excluded alternatives:
- Existing supported investments to preserve:
- Fixed/usage cost per outcome/user/month, growth/burst cases and limits:
- Sources, units/currency, date checked and unknowns; quality/AI review if relevant:
- Operational owner, observability, retention/export, backup/restore and support:

## Verification and delivery

- Requirement-level test strategy and representative end-to-end proofs:
- Work branches from dev; reviewed work PRs to dev:
- Reviewed dev -> staging -> main promotion PRs and stage-specific acceptance:
- Team reviewer responsibility or recorded solo self-review; actual destination controls:
- Rollout/recovery, production authority, cache and merged-worktree cleanup:

## Traceability to the selected issue tracker

- Selected tracker/project and verified access (no credentials):
- Spec revision and accepted slice used to derive work:

| Requirement IDs | Canonical tracker work-item links | Explicit deferred decision, if not being implemented |
| --- | --- | --- |

Use real tracker identifiers after creating/deduplicating the work items. Keep
progress and execution claims in the tracker, not a parallel checklist here.
A spec-to-ticket link or a merged PR does not itself prove acceptance.

## Decision and change history

Record the user-confirmed decision, affected requirement IDs, rationale, current
spec revision, assumptions/unknowns and which tracked work/reviews need updating.
Keep this concise; do not copy raw conversations, secrets or personal account data.
