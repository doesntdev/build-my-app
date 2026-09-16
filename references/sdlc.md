# Agent-operated SDLC

GitHub Issues is the durable ledger once connected. Projects is optional; a solo
builder needs one understandable lifecycle, not a portfolio platform. Use either
a Project status field or one `status:*` label family, not competing sources:
triage → ready → in progress → in review → release pending → done; blocked always
carries an owner, reason and next action.

## 1. Discover and coordinate

Read explicit user intent first. Search existing issues and relevant closed work
before creating duplicates. Then reconcile repo plans/specs for untracked work.
If no work exists, ask one concrete user-problem question rather than inventing
features. Inaccessible or entirely blocked work is not an empty backlog.

Before edits, inspect Git status/staged/untracked files, remotes, branches,
worktrees, open PRs (including drafts/forks), remote branches without PRs, active
issue claims, intended base/head SHAs, and changed-file/semantic overlap. Complete
pagination and reconcile provider totals; capped/failed lookups are unknown.
For new local repositories with no remote, mark remote inventory not yet applicable
and repeat after connection. Do not touch another checkout to make yours clean.

Within authorized GitHub scope, record and read back a scoped issue claim: owner,
agent execution label, intended branch/base, owned paths/capabilities, exclusions,
dependencies. Shared GitHub login does not mean shared ownership. Comments are
cooperative claims, not atomic locks; arbitrate simultaneous claims. Recheck at
first edit, resume, scope changes, push, merge and handoff rather than polling.
Unknown/overlapping ownership blocks that work until disjoint scope, handoff, or
a stacked dependency and merge order are agreed. Never auto-stash/reset/clean or
force-push another writer's work.

Exit: testable issue acceptance, explicit owner, no unresolved overlap, isolated
branch/worktree. A new offline prototype may use the onboarding bootstrap exception;
collaboration/cloud publication may not.

## 2. Define a small change

Use `templates/github-issue.md`. State outcome, non-goals, acceptance, security/data
impact, tests, observability, deploy order and recovery. Classify:

- **Standard:** bounded non-sensitive feature/fix; normal review and checks.
- **Sensitive:** auth/tenant access, data migrations, dependencies, infrastructure,
  secrets, DNS, email recipients, money or retention; threat review, recovery,
  isolated staging, independent review where available, production confirmation.
- **Emergency:** named incident owner, minimal reversible containment, captured
  evidence, explicit production authority, immediate follow-up issue.

Define the smallest end-to-end slice, not a pile of disconnected scaffolding.
Existing plans remain design references; ownership/progress live on the issue.

Exit: ready acceptance, known dependencies and authority, implementable test plan.

## 3. Implement and prove locally

Start from the intended green base. Reproduce the bug or add a failing behavior
test, implement the smallest slice, refactor while green. Use architecture and
local-development references. Exercise actual adapters and database constraints,
authorization failures, idempotency/concurrency and event recovery where relevant.
Use capture mail by default; never use production data in tests.

Run canonical format/lint/type checks, unit/integration tests, migrations from
zero and upgrade state, production build, Podman runtime smoke, relevant browser
flows, secrets/dependency/license checks, and diff review. Adapt commands to the
existing language; don't add Python to the app merely because skill helpers use it.
Skipped required tests fail the gate; record legitimate N/A reasons explicitly.

Exit: acceptance proven in the local production-shaped runtime, clean cleanup,
no unexplained failures. Record actual commands/results, not an agent's assertion.

## 4. Pull request and CI

Use `templates/pull-request.md`. Keep a small PR linked to its issue, tests,
security/data/infrastructure effects, migration compatibility, new secret **names**,
observability, deploy and recovery. `Closes #...` is appropriate only when merge
really satisfies completion; deployment-dependent issues should not auto-close
before release acceptance. Use a non-closing link otherwise.

CI reruns checks independently on PRs and pushes to the protected default branch.
Set minimal token permissions, pin/review third-party actions, and never grant
untrusted fork PR code deployment secrets. Do not run untrusted code under a
privileged `pull_request_target` workflow. Record review requirements based on
available humans and risk; agent self-review is not independent human approval.
Check current CI/head SHA and resolve comments before merge. Recheck coordination.
For stacked PRs, integrate in order, retarget/rebase dependents and rerun checks.

Exit: current reviewed head is green and mergeable; no protection bypass.

## 5. Stage, authorize and release

Read publishing before infrastructure changes. Test the candidate in isolated
staging with sanitized data and controlled mail. Record exact artifact/commit,
migrations, environment/config changes, observed acceptance and recovery readiness.
Get bounded production authorization. Promote/release and read back exact targets,
then verify the public app and security boundaries. Failure stops promotion.

Exit: production acceptance plus observation window is green. Close issue only
when its full acceptance is true; create linked follow-ups for deferred risks.
If the user requested local-only delivery, close the local-scoped issue honestly
without inventing a requirement to deploy every change.

## 6. Operate and improve

Maintain named owners, logs/metrics/error visibility, uptime, dependency updates,
backup/restore drills, credential rotation, provider budgets and cleanup. Track
incidents and durable follow-ups as issues. Scheduled automation is opt-in,
visible, bounded, with permissions, failure delivery and a disable path; never
install a cron job just because this skill mentions maintenance.

During incidents: read-only diagnosis first, record deployment/change timing and
safe request IDs, choose the smallest reversible authorized mitigation, verify
recovery through a real user flow, then reconcile manual changes into Git and
migrations. App rollback does not reverse destructive database changes.

## Handoff and evidence

At pause/completion, update/release only your claim. Link issue, branch/PR, tested
commit, CI, artifact and deployment evidence plus blocker/next action. Preserve
review-pending branches and other agents' work. Do not dump secrets or raw logs.
A useful report says exactly what is usable now and what remains unverified.
