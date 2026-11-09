## Summary and requirements

User-visible change, non-goals, canonical work item and `spec.md` revision/
requirement IDs. PR type: work / staging promotion / production promotion.

## Source, target and coordination

Actual head/base and head SHA, ownership claim, scope, dependencies and latest
overlap/composition check. Work -> dev; dev -> staging; staging -> main.
List included work items for a promotion and exclude unintended scope explicitly.

## Evidence

Actual commands/results, current source identity, relevant negative/user-flow
checks and pending gates. Work/dev checks are targeted; comprehensive acceptance
runs on resulting staging/main revisions. Don't label an unrun later gate passed.

## Review — required before merge

- Mode: team review / documented solo self-review, with project-context reason.
- Assigned eligible non-author reviewers and native review-request links, if a team.
- Reviewed head SHA and comparison target; current verdict and findings/resolutions.
- Solo review: separate full-diff pass, requirements/acceptance, tests, security/data,
  deployment/recovery and cleanup findings. Link its record; do not fabricate native self-approval.
- [ ] Every applicable review is complete on the current candidate, not merely assigned.
- [ ] Material source/composition changes received renewed review as needed.
- [ ] Genuine required independent/CODEOWNER decisions and destination controls are satisfied.

## Security, data and release

Auth/tenant/API/MCP/event/migration effects, compatibility, new secret names only,
provider/config/email/DNS changes, release authority, observation/failure thresholds,
rollback/forward-fix and cost impact. Keep staging and production evidence separate.

## Cleanup and handoff

Exact disposable work head/worktree retirement plan and dependent PR handling;
inactive generated outputs to remove; protected source/runtime/evidence to retain.
After merge, link verified ref/worktree/path absence, preservation and measured
cleanup. Retain persistent dev/staging/main; unresolved cleanup is incomplete.

## Follow-ups and acceptance limits

Known risks, linked follow-ups, untested or later-stage behavior. Use non-closing
work-item links until merge truly completes the full acceptance; pending production
proof cannot be closed by a reviewed work PR alone.
