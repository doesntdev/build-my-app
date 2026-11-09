# Project charter

- User and first useful workflow:
- Measurable acceptance and non-goals:
- Accepted first slice and deferred ambition (do not silently shrink the outcome):
- Active users at launch/growth, actions per user, peak concurrency and retention:
- Data volume, input/output sizes and critical read/write or job shape:
- Existing repo/runtime/constraints:
- Development/delivery constraints: builder skills, available time, target platforms, test data/environments and support owner:
- Feasibility recommendation by feature: build / prove first / reshape / defer:
- Complexity drivers, critical-path dependencies and required access/approvals:
- Local-only or publication target:
- Data classification, region and retention:
- Auth, authorization and tenant model:
- API and application MCP decision:
- Durable side effects/events and recovery:
- Performance/reliability targets and RPO/RTO:
- Selected stack/services and purpose (start with Cloudflare; provision only needed parts):
- Alternatives, excluded services and reasons; preserve existing supported investments:
- Concrete upgrade triggers and next validation experiment:
- AI task/quality target, model/version, privacy, context/output limits and review (if applicable):
- Cost per completed action/user/month, expected/growth/burst cases and uncertainty:
- Price/limit source URLs, units/currency, date checked, assumptions and exclusions:
- Per-user/job/global budgets, admission/reservation, concurrency and retry/revision limits:
- Provider account/resource labels (no secrets; keep private if sensitive):
- Budget ceiling and cost owner:
- Repository visibility and source license (separate from public deployment):
- Release owner and approval boundaries:
- Routine agent authority (specific repos, paths, environments, operations):
- Known gaps and unresolved decisions:
- User-accepted trade-offs and unverified/provisional decisions:
- Canonical GitHub issue, or temporary bootstrap record and migration trigger:

## Material feasibility risks

Keep this short and proportional. Record technical, scaling, security, correctness,
integration, development, usability, cost or operational concerns that could
materially affect the outcome. This is not an AI-only register or a second backlog.

| Concern and user/development impact | Evidence or unknown | Severity | Recommendation / alternatives | Proof or mitigation | Owner / next step | Disposition |
| --- | --- | --- | --- | --- | --- | --- |

Use resolved, accepted, experiment, deferred or blocked; never mark an unknown as
accepted by default. Move actionable unfinished acceptance into the existing issue
workflow when available, keeping this charter as the concise decision context.

## Canonical commands

Document the actual project-specific commands after verifying them: start local,
check/test, selected-storage migration rehearsal, Workers bundle/runtime or selected
Podman build/run, staged release, rollback. Mark irrelevant paths N/A with reasons.
Do not fill this section with invented working commands.
