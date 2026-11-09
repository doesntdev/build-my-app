# Spec-driven, reviewed SDLC

This is the application delivery policy taught by the skill. It is an agent
instruction, not a new hosted CI system or permission to change repository rules.
Preserve actual destination controls and user authority. A conflict with this
policy needs an explicit resolution, never a quiet bypass.

## 1. Build spec.md and derive tracked work

Create the application's root `spec.md` from [the template](../templates/spec.md)
and refine it with the user throughout ideation. Keep stable requirement IDs
(such as `REQ-001`), observable acceptance, decisions, non-goals, feasibility
risks and explicit unknowns. Mark requirements draft, accepted or deferred;
implementation may use an accepted slice without pretending the whole idea is final.
A changed requirement keeps its identity and records the decision; do not recycle IDs.

**Use GitHub Issues or another issue tracker before implementation.** Prefer an
existing user-selected tracker, including Jira, Linear, GitLab or another real
tracker, over inventing a second backlog. Verify the intended project/account and
required read/write access through its supported tools. A tracker must provide
stable work-item IDs, ownership, acceptance, state/history and dependency links.
An approved offline-capable issue tracker can satisfy this; a temporary Markdown
intake or the spec itself is not a substitute. If none is available, continue
ideation and read-only discovery while resolving tracking access; do not invent
an issue URL or begin untracked coding, including implementation spikes.

The spec defines **what and why**; the tracker defines **owned, executable work
and its progress**. Derive small vertical work items from accepted requirements:

- Link `spec.md`, requirement IDs and the exact spec revision/section being used.
- State outcome, acceptance and failure paths, scope/non-goals, risk/change class,
  dependencies, owner, priority, verification, rollout and recovery.
- Track a feasibility experiment as an experiment with its own acceptance, not
  an implicitly approved product feature. An explicitly accepted experiment scope
  can investigate a draft requirement without accepting that feature. Hold
  dependent work when its result is unknown.
- Deduplicate against existing/all-state work and PRs before creating tickets.
  Map each in-scope requirement to tracked implementation/proof or an explicit
  deferred decision; a ticket existing is not evidence that the requirement passed.
- Update spec and affected items when the user changes scope. Preserve completed
  evidence and identify impacted reviews/tests rather than rewriting history.

Use [the work-item template](../templates/github-issue.md) in the selected tracker.
Choose one lifecycle representation, for example triage -> ready -> in progress
-> in review -> release pending -> done. A blocked item names the reason, owner
and next action. Keep product decisions in the spec and progress in the tracker.

**Exit:** accepted slice, current spec revision, real work-item IDs and traceable
acceptance; no untracked implementation or competing backlog.

## 2. Coordinate ownership and branch for work

Before editing application code, inspect repository instructions, Git/index/
untracked state, remotes, branches, worktrees, open PRs, active claims and overlapping
paths. Complete pagination; a capped or failed lookup is unknown, not an empty
queue. Shared login does not mean shared ownership. Record/read back an execution
claim in the selected work item: owner, scope, base, work branch, exclusions and
dependencies. Recheck at resume, scope changes, PR update and integration boundaries.
Preserve other writers; do not auto-stash/reset their files or force-push their work.

Use persistent `dev`, `staging` and `main` branches and the following PR edges:

| Change | Source | Target | Purpose |
| --- | --- | --- | --- |
| Work PR | work/<work-item> | dev | A bounded tracked implementation, fix, experiment or documentation change |
| Staging promotion PR | dev | staging | An explicit integrated release candidate |
| Production promotion PR | staging | main | The qualified staging candidate for production |

Create work branches from current `dev`, using `work/<work-item>` or the existing
issue-key naming convention. Never develop directly on the persistent branches or
merge a work branch straight to `staging`/`main`. If integration branches are missing,
choose their verified seed and establish them within the user's repository authority;
resolve conflicting existing branch/deploy policy first. Remote branch creation and
its deployment effects are separate from safe local branching.

Use an owned worktree where isolation is useful, not a full repository/build copy
per attempt. Arrange merged-head/worktree cleanup authority and dependency handling
**before merge** using [workspace hygiene](workspace-hygiene.md). Preserve all three
persistent branches during promotion; their source branches are not disposable heads.

**Exit:** claimed tracked work, isolated work branch from the correct base, no
unresolved overlap, and a safe eventual cleanup plan.

## 3. Implement and verify the bounded work

Start from the intended green base. Reproduce the defect or add a failing behavior
test, implement a complete small slice, refactor while green. Use the selected
runtime and actual adapters; do not add Postgres/container tests to a Workers-only
change. Use synthetic data, captured mail and deterministic AI fixtures by default.

Run targeted local format/lint/type, unit/integration and relevant user-flow checks
for the changed behavior and affected consumers. Include applicable permission,
concurrency/idempotency, migration and recovery paths. Review secrets/dependencies
and licenses where touched. Record exact commands, revision and actual results.
Keep routine work/dev checks targeted; comprehensive release regression belongs
to the post-staging and post-main steps below. Existing genuine repository-required
checks still apply; resolve an incompatible control with the owner rather than bypass it.
No new hosted CI vendor or workflow is required by this policy.

Classify work proportionately: ordinary bounded changes use normal checks;
auth/data/money/infrastructure changes require threat/recovery and appropriate
review; incidents need a named owner and authorized containment. Containment does
not silently authorize an unreviewed direct-to-main feature or permanent policy exception.

**Exit:** work-item acceptance proved at the requested local scope, no unexplained
failures, and actual evidence ready for review. Local success is not production success.

## 4. Review every PR before merge

**Every PR must be reviewed before merge**, including work and promotion PRs.
Use [the PR template](../templates/pull-request.md), link the canonical work item
and spec requirements, and record source/base, head SHA, verification, risks,
release/recovery effects and cleanup plan. Default to non-closing tracker links;
merge must not auto-close acceptance that still depends on a later environment.

Determine the review mode from the real project contributors and policy:

| Situation | Required review |
| --- | --- |
| Other developers participate | Assign review responsibility to named eligible non-author developers and request their review through the host's reviewer field; obtain the required completed review decisions |
| Genuinely solo project | Perform and document a substantive self-review as a separate pass after implementation; record findings, repairs, checklist and reviewed head SHA |

For team review, a PR assignee alone is not a review request. Use CODEOWNERS/domain
ownership where required; request their review explicitly, then read back the
persisted request or actual completed review. Pending assignment, a bot summary
or silence is not approval. An agent cannot silently switch a team PR to solo
mode because a developer is busy, has not answered or the account has admin access.
Hold merge for unresolved review findings and actual required decisions.

For solo self-review, inspect the full diff against the live target, linked
requirements/acceptance, tests and negative paths, security/data effects, release
composition and cleanup. Repair findings and recheck. GitHub's author cannot approve its own PR;
record self-review in a comment/checklist or linked artifact instead of fabricating
native approval or switching accounts. This satisfies the documented solo process,
not required independent/CODEOWNER approval: genuine enforced requirements remain binding.

Bind review to the actual reviewed head and comparison target. Material source changes
require renewed review of affected changes; moving targets require composition
checks. Reuse valid unchanged-source technical evidence, but make a fresh explicit
review decision for each promotion PR's actual contents and destination. Verify all
blocking findings and required reviews are resolved before merging; "assigned" or
"tests passed" alone does not establish review completion.

**Exit:** each current PR has recorded qualified review, current relevant checks,
resolved findings and a verified target; no unreviewed merge or protection bypass.

## 5. Merge reviewed work to dev

Merge only the reviewed work PR into current `dev`. Verify the native merge target,
merged source inclusion and resulting commit/tree. A child merged into another
unmerged work branch is only merged-into-parent, not accepted into `dev`.
Run applicable targeted integration checks on the actual `dev` result and reconcile
stacked dependents, issue status and exact-source evidence. Resolve new composition
failures before promotion; an older green work branch is not proof of green integration.

Immediately perform the merged disposable-head/worktree and cache cleanup in
[workspace hygiene](workspace-hygiene.md). Reconcile dependent PRs before retiring
their source. Preserve `dev`, `staging`, `main`, other writers and unique work.
A merge is not a reason to leave redundant builds or disposable worktrees behind.

**Exit:** reviewed work is verified in `dev`, integration checks pass, the tracker
reflects the actual stage, and required cleanup is complete or explicitly blocked.

## 6. Promote dev to staging, then staging to main

Read [publishing](publishing.md) before infrastructure/release changes. Freeze the
intended candidate and included work items; resolve incomplete/unintended `dev`
content before promotion rather than quietly shipping it. Obtain the appropriate
promotion/environment authority; source branches do not grant spending or deployment
permissions. Local-only work can stop at its agreed scope without inventing a cloud release.

1. Open and review the **dev -> staging** promotion PR under the same review rule.
   Merge only after its applicable prerequisites pass. Run the comprehensive suite
   **after the staging merge** on the resulting staging revision; validate the selected
   runtime/environment, migrations/recovery, permissions, complete user flows and
   relevant failure/load/resource behavior with sanitized data. Record actual branch,
   artifact/deployment and results. An absent hosted environment is not a hosted PASS.
2. Hold a failed staging candidate. Repair through tracked work -> `dev` -> `staging`,
   repeat affected review and staging acceptance, and keep actual failures visible.
   A work-branch test or unrun check cannot substitute for staging acceptance.
3. With staging qualified and explicit production authorization, open and review
   the **staging -> main** promotion PR. Verify intended composition and current
   staging evidence; merge through the approved lane, never an unreviewed push.
4. Run a fresh comprehensive suite **after the main merge** on the resulting main
   revision, plus actual production acceptance and the agreed observation window
   when production delivery is in scope. Staging PASS does not replace this execution.
   Stop rollout/contain or recover within authority on failure; preserve source and
   data evidence and repair through the reviewed lane.

For every promotion, read back source/head/base/merge target and the resulting
source/artifact/deployment. Keep merged, tested, deployed and live acceptance
separate. Review and verify promotion composition even when its code was already
reviewed; do not replay an unchanged source-review campaign merely because the
merge metadata SHA changed. Retain all persistent integration branches.

**Exit:** requested promotion stage is actually verified, release authority and
recovery are known, applicable PR reviews/checks pass and cleanup is reconciled.
Close a work item only when its complete stated acceptance is true; otherwise keep
it release-pending/blocked with explicit follow-ups, not falsely "done" from merge alone.

## 7. Operate and close out cleanly

Keep named owners, useful logs/errors/latency and spend signals, retention,
backup/restore, credential rotation and dependency maintenance proportional to
risk. Scheduled automation is opt-in and bounded; use events/native alerts rather
than creating a perpetual polling agent. During incidents, start read-only, record
change timing, contain within authority, verify recovery, and reconcile source/data
changes into tracked work. App rollback does not reverse destructive data changes.

Run [workspace hygiene](workspace-hygiene.md) during work, after each merge and before
handoff. Link `spec.md` revision/requirements, tracker item, PR review evidence,
source/target commits, actual test/deployment outcomes, measured cleanup, blockers
and next action. Release only your ownership claim. Preserve pending reviews,
active work, protected data and necessary evidence. A useful completion report
states exactly which stage is usable and what remains unverified.
