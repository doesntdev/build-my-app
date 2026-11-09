# Tracked work item

Use these fields in GitHub Issues or the selected issue tracker. The filename is
an installation-compatible template name, not a requirement to use GitHub.

## Requirements source

Link `spec.md`, stable requirement IDs and the exact spec revision/sections.
State whether this is accepted implementation, a feasibility experiment, defect
or operational follow-up; an unresolved product decision is not implicit approval.

## Outcome and Acceptance

Who needs what behavior and why? List observable acceptance, relevant negative/
failure paths, measurable constraints and the proof expected for each requirement.

## Scope and ownership

Non-goals, dependencies, owner, lifecycle state, priority, change class, unresolved
risks and their next experiment/mitigation. Keep this the canonical execution
record rather than a copy of status in the spec or a local parallel backlog.

## Design and safety

Data/auth/tenant effects, invariants/events, APIs/MCP, migrations, provider/email/
DNS changes, secret names only, material feasibility and recovery decisions.

## Verification and delivery

Targeted local checks and affected consumers, integration into dev, staging/main
acceptance where in scope, observation, rollout/recovery and actual authority.
Use a work branch from dev; release promotions use dev -> staging -> main.

## Coordination and review

Execution owner/label, base SHA, owned paths/capabilities, overlap resolution,
work branch/PR, assigned eligible team reviewer(s) or explicit solo self-review,
reviewed source and outstanding findings. Verify claims and review state at handoffs.

## Completion evidence and cleanup

Requirement acceptance, reviewed PR/merge/artifact/deployment links, actual stage,
cache and merged-worktree/branch retirement with verified absence/preservation,
follow-ups and blockers. A dev merge is not production completion; use non-closing
links until the full stated acceptance is satisfied.
