# Cache and merged-worktree hygiene

Cleanup is part of every implementation, merge and handoff, not an optional
follow-up. Use this with the [SDLC](sdlc.md). Routine exact cleanup of task-owned,
inactive, regenerable outputs and incorporated disposable work is in scope; this
is not permission for a workspace/global purge, a cron job or another writer's data.

## Arrange retirement before merge

Before merge, enumerate branches/worktrees, owners, pending/dependent PRs and
runtime consumers. Use `git worktree list --porcelain` and inspect staged,
tracked and untracked state in each candidate worktree. Identify the exact merge
source and target and how inclusion will be proved after squash/rebase as well
as ordinary merges. Resolve deletion authority and dependent PR/worktree plans
before accepting a merge that cannot be closed out safely.

Preserve persistent `dev`, `staging` and `main`, the primary checkout, active
review/work branches, other writers' files and unique unmerged changes. A clean
worktree or matching login alone does not prove it is abandoned. A worktree with
an unrelated source edit is not disposable just because its old branch merged.
Arrange an owner-approved preservation/handoff before removing it; if unresolved,
hold the merge rather than assuming cleanup can wait indefinitely.

## Reuse one useful cache, remove superseded bulk

Measure the project and relevant output paths before expensive work. Reuse one
useful compatible current build cache when practical, not a full build copy per
attempt. During work and before handoff, remove verified inactive redundant
compiler/frontend/test caches, stale bytecode, timestamped agent runs, copied
build trees, redundant executable/library copies and intermediate archives whose
consumers have been resolved. Include outputs outside conventional build folders.

Use an exact allowlist. Establish project ownership, resolved path boundaries,
ignore/build declarations and active/saved runtime use before deletion. An ignored
path can still be a credential, database, fixture, offline dependency or saved
preview input. Preserve those, local D1/R2 state, `.wrangler` data, source,
required evidence and intentional release outputs. Preserve useful graph/index
artifacts. Reconcile historical evidence holds against current consumers; retain
compact useful records rather than every obsolete generated tree indefinitely.

Don't purge shared package/container/model caches as incidental project cleanup.
Do not change another writer's permissions or terminate their process to empty a
cache. Keep a concrete consumer/reason for any necessary retained generated output.

## Retire incorporated work after each merge

After each merge, read back the exact target and incorporated source, then:

1. Reconcile dependent PRs/branches and prove inclusion. Native MERGED into a parent
   is not proof of inclusion in `dev`/`staging`/`main`; closed-unmerged alone is not
   retirement authority. Preserve unique later commits if a source tip advanced.
2. Delete the incorporated disposable remote work head promptly, using its exact
   verified tip. Promotion sources `dev` and `staging` are persistent, not disposable.
   A failed later test does not excuse retaining a safely deletable merged work head.
3. Reinspect the exclusively owned disposable worktree for dirty index, tracked,
   untracked and protected local state, active processes and saved-runtime use.
   Confirm required proof is retained outside the soon-to-be-removed directory.
4. Remove only that safe merged worktree through native Git worktree removal,
   then retire its incorporated local/tracking work refs. If the primary checkout
   was on the merged work branch, switch it safely to the intended persistent
   branch after preservation; never delete the primary checkout. No forced removal,
   blanket `git clean`, force-push or deletion of integration branches.
5. Prune only the exact associated inactive generated outputs that remain after
   retirement, and retain no redundant worktree/build copy by default.

If dirty/active/unique work or a required saved input prevents removal, preserve it,
resolve with its owner and report cleanup as **BLOCKED/INCOMPLETE**, not successful
retention or completed delivery. A denied remote deletion is likewise incomplete.
Resolve these conditions before the next promotion/handoff; never silently expand
cleanup authority or discard work to satisfy a zero-leftovers count.

## Verify without recreating the bulk

Verify retired remote/local refs and worktree registrations are absent, along
with the selected physical paths. Compare protected source/index/runtime state
with the baseline and confirm persistent branches and primary checkout survive.
Report measured before/after allocation or bytes reclaimed, the exact retired
scope and any retained consumer/blocker. Keep directory allocation distinct from
actual filesystem free-space changes. Use non-regenerating checks: do not rebuild
deleted outputs just to validate cleanup. Passing code tests alone do not prove
cleanup, and successful deletion alone does not prove source preservation.
