# Project execution charter

Product requirements, assumptions, acceptance and decisions live in the
application's `spec.md`. This charter records execution/authority context, not a
second spec or task backlog. Keep sensitive account/resource labels in ignored
local state and link safe references here rather than exposing secrets.

- Spec path, current revision and accepted first slice/requirement IDs:
- Selected issue tracker/project and canonical work-item links:
- Existing repo/runtime and authoritative checkout:
- Work branch convention/base; persistent dev, staging and main mapping:
- Team/solo review mode, eligible reviewers/CODEOWNERS and actual review requirements:
- Local-only, staging or production authority and release owner:
- Routine agent authority: repositories, paths, environments and allowed operations:
- Provider connection/resource scope (safe labels only):
- Budget owner and bounded spending/resource authorization:
- Development/support owner, time/device/access constraints:
- Data-sensitivity/privacy constraints and required qualified approvals:
- Cleanup ownership, disposable worktrees/caches and preserved runtime/evidence consumers:
- Unresolved execution blockers and next action:

For an existing charter containing product requirements or risk decisions,
reconcile them into `spec.md` with the user while preserving accepted decisions
and evidence. Don't discard the old context, infer fresh approval or silently
reinterpret completed work. Work status and ownership remain in the tracker.

## Canonical commands

Record project-specific commands only after verification: local start, targeted
checks, storage migration rehearsal, selected runtime build/smoke, comprehensive
staging/main acceptance, release and recovery. Mark irrelevant paths N/A with
reasons. Bind release/verification to actual revisions, not invented working commands.
