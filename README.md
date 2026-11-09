# Build My App

**An agent skill that helps ground an idea, recommends the smallest suitable
stack, and carries an agreed app through local development and release.**

Start with Cloudflare. Add services when the workload warrants them.

Bring an idea and your coding agent. First explore feasibility, performance,
scalability, security, complexity, dependencies, cost and the practical difficulty
of building and maintaining it. The skill recommends Cloudflare Workers/Static
Assets, D1 for relational state and private R2 for files **only as needed**. Neon,
Railway, Resend and AI providers are options with explicit reasons, not required
accounts. Existing supported stacks stay intact. Account consent, spending,
publishing and production authority remain the user's decisions.

## What you get

- A framework-neutral `SKILL.md` following the [Agent Skills standard](https://agentskills.io/specification).
- Progressive onboarding: a useful local app before cloud setup becomes necessary.
- General application feasibility review before scaffolding or logins: technical
  constraints, scalability, security, complexity, integrations, correctness,
  development/test effort, usability, cost and ongoing operations.
- Feature-specific exploration and small proof experiments for the risks that
  matter. AI economics is one conditional branch, not the whole interview.
- Official MCP recipes and configuration generators for **Claude Code, Codex,
  Cursor, and Hermes**, plus a generic-client adaptation procedure.
- Local Workers/D1/R2 development without cloud credentials; rootless Podman and
  local Postgres only for the selected container/database extension.
- Spec-derived tracked work in GitHub Issues or another issue tracker; ownership,
  reviewed work/promotions through dev -> staging -> main, cleanup, rollback,
  incidents, and ongoing operations.
- Portable Python helpers, templates, deterministic tests, and a package/privacy check.
- A bounded, read-only upstream version check once per invocation; newer releases
  are a notice, not permission to overwrite an installation.

This is **not** an app generator executable, a hosted service, an agent runtime,
or a promise that every client supports every OAuth flow. Your agent reads the
workflow and does the work through its own tools. No broker, author's account,
private skill, or additional model API subscription is required by this package.

“Local-first” describes the development workflow. Application-level offline sync
is an explicit product requirement, not something this stack supplies for free.

## Ideation, then a growth path

The first interaction is a conversation, not a five-provider setup checklist.
Ask a few consequential questions, follow the answers, explain material trade-offs,
then agree a first slice. On resume, reuse prior decisions and revisit changes.

Every meaningful feature gets the same review: what could prevent it working,
what makes it difficult to develop/support, how that affects the user, and what
small proof or alternative reduces the risk. Offline editing exposes conflict
resolution; booking/payment exposes races and duplicate events; integrations
expose real access, contract and rate-limit dependencies; large uploads expose
transfer, security, retention and resource costs. The agent recommends what to
build, prove first, reshape or defer rather than just collecting features.

See [ideation](references/ideation.md) for the general process. A 100,000-word
AI-generated book remains a worked example in the conditional
[AI reference](references/ai-feasibility.md), not a special gate that other apps skip.

A static site may need only Static Assets. A small stateful app may use Workers
and D1; add private R2 for files. Queues/Workflows, Durable Objects, Workers AI,
Neon or Railway are added for actual needs. There is no invented user-count
threshold or mandatory migration away from Cloudflare. See
[stack selection](references/stack-selection.md) for triggers and trade-offs.

## Spec-driven, reviewed delivery

Ideation continuously creates/updates the application's root `spec.md`: stable
requirements, acceptance, decisions, risks and explicit unknowns. Before coding,
derive bounded work items in GitHub Issues or the user's selected issue tracker.
Link requirement IDs and spec revision; use the tracker for execution status and
ownership, not the spec or a temporary parallel backlog.

Work branches start from `dev` and enter it through reviewed PRs. Releases use
reviewed `dev` -> `staging` -> `main` promotion PRs, with comprehensive acceptance
on the actual resulting staging and main revisions. Every PR is reviewed before
merge: request named eligible non-author developers in a team; in a genuinely
solo project, record a substantive separate self-review. Native self-approval
is not fabricated and actual independent/CODEOWNER requirements still apply.

Clean inactive regenerable caches during work and retire incorporated disposable
work branches/worktrees after merges. Verify exact absence and source/runtime
preservation; retain persistent integration branches, active/unique work and user
data. Unresolved cleanup is explicitly incomplete, never a hidden leftover.
See [SDLC](references/sdlc.md), [the spec template](templates/spec.md) and
[workspace hygiene](references/workspace-hygiene.md).

## Install

[Source repository](https://github.com/doesntdev/build-my-app) ·
[Releases](https://github.com/doesntdev/build-my-app/releases) ·
[CI results](https://github.com/doesntdev/build-my-app/actions)

```text
git clone https://github.com/doesntdev/build-my-app.git
cd build-my-app
```

Download/extract or clone a reviewed copy. Keep the directory name
`build-my-app`. Use a release/commit you trust; do not run an unreviewed
remote installer. From the extracted skill directory, with Python 3.11+:

```text
python scripts/verify.py
python -m unittest discover -s tests -v
python scripts/stack.py install --destination ../my-app/.agents/skills/build-my-app
python scripts/stack.py install --destination ../my-app/.agents/skills/build-my-app --apply
```

The first install command is a dry run. The second copies the manifest-listed
files, verifies their hashes, and refuses to overwrite a differing installation.
Choose the destination for **your** client:

| Client | Typical project installation |
| --- | --- |
| Codex | `<app>/.agents/skills/build-my-app` |
| Claude Code | `<app>/.claude/skills/build-my-app` |
| Cursor | `<app>/.cursor/skills/build-my-app` |
| Hermes | Active profile's `skills/build-my-app`; use its supported skill installer/approval flow where available |
| Other | Its documented skills directory; or ask it to read `SKILL.md` and follow relative references |

On systems where the command is named `python3`, substitute that for `python`.
For user-level installation, use the client's documented user skill directory.
Confirm the active profile and target path rather than assuming a global home.
Reload skills/start a new agent session and verify the skill appears. Copying a
folder does not register MCPs or grant access to any service.

## Start with one prompt

> Use build-my-app to build my app. First inspect this workspace and
> explore the idea with me. Challenge feasibility, scalability, security,
> complexity, integration, development and cost assumptions for every major feature.
> Surface problems early and propose practical alternatives or proofs. Recommend the minimum
> Cloudflare-first stack and build spec.md with me as we ideate. Derive tracked
> work in the selected issue tracker, branch from dev, review every PR and promote
> through staging to main. Clean caches and merged worktrees. Connect only needed
> services; ask before spending or publishing.

For an existing app:

> Adopt build-my-app in this repository. Preserve the framework and
> current work. Reconcile the idea, workload and cost assumptions; preserve the
> supported stack. Audit gaps and ship one agreed slice without unused providers.

For just setup:

> Use build-my-app to connect my provider MCPs in this agent. Discover
> what already exists, back up config, and verify each with a read-only call.

For a resume:

> Resume build-my-app from spec.md, the onboarding record and selected tracker
> work item. Recheck ownership, reviews and next promotion; don't repeat completed setup.

## Helpers

```text
python -B scripts/stack.py check-updates
python scripts/stack.py doctor --stage local
python scripts/stack.py doctor --stage publish
python scripts/stack.py doctor --stage local --profile container
python scripts/stack.py mcp-config --client codex
python scripts/stack.py mcp-config --client claude-code --providers github cloudflare
python scripts/stack.py mcp-config --client cursor --providers railway --railway-transport stdio
python scripts/stack.py mcp-config --client hermes --providers neon
```

`check-updates` compares the loaded skill's version with its canonical upstream
main metadata. It does not use the application's Git remote or modify files.
Newer versions trigger a brief notice; offline/invalid checks remain unverified
without blocking work. Applying an update still requires approval and preservation
of customizations. See [update behavior](references/updates.md), including why
older installed versions first need a deliberate manual upgrade.

`doctor` defaults to Cloudflare Git/Node prerequisites. Global Wrangler is optional:
the agent separately verifies the project's installed Wrangler, supported runtime
and local bindings. `--profile container` requires Podman and checks its readiness.
Neither profile certifies cloud auth or app health; optional CLIs are not mandatory
when an approved MCP path exists. `mcp-config` defaults to **Cloudflare only**;
select other providers explicitly. It prints a **fragment**, never edits live
configuration or reads secrets. Selected Railway defaults to remote OAuth; use stdio to reuse
an authenticated Railway CLI. Authenticate through your actual agent after
reviewing and merging the selected entries. See [client setup](references/mcp-clients.md).

## Boundaries

- Cloud services, model inference, domains, storage and email can cost money. Your agent must
  inspect current pricing and get your budget approval before provisioning.
- Local development needs initial runtime/package/image downloads; it does not
  need production credentials or cloud services for core tests.
- Neon MCP is for development/testing only. Production changes use reviewed
  migrations and release credentials, never an agent's ad hoc SQL tool.
- A source repository stays private unless you explicitly choose public. A public
  deployment is also a separate approval from pushing source.
- Framework support is procedural, not a tested matrix of every web framework.
  Client config tests are not proof of live OAuth in every client/OS combination.
- No automatic update application, background service, telemetry or subscription
  is bundled. The startup check reads only bounded public version metadata.

## Releases and contributions

The public source is [doesntdev/build-my-app](https://github.com/doesntdev/build-my-app).
This is a standalone, MIT-licensed package; its runtime does not depend on the
maintainer's accounts or infrastructure. The version check reads this skill's
canonical public repository metadata, not a private update service. Forks can use
their own source/release process and deliberately review changing the pinned
upstream constant/tests. The checker never downloads or installs executable code.

The pre-existing package CI configuration is retained; this update is verified
locally, not a claim of a new hosted run. Application delivery follows the selected
repository's policy; hosted CI is not a prerequisite for the Cloudflare minimum.
See [the historical audit](PUBLICATION-AUDIT.md) and [contributing](CONTRIBUTING.md)
for package checks and known limits.

## Validation

See [the validation record](VALIDATION.md) for executed checks and explicit gaps.
The historical 0.1.1 [hosted validation suite](https://github.com/doesntdev/build-my-app/actions/runs/35139096695)
passed 58 tests on Linux, macOS and Windows with Python 3.11 and 3.14.
A real isolated Podman/Postgres smoke test also passed locally on Linux.
Live provider OAuth and cloud deployment are not certified by those tests.

## License

[MIT](LICENSE). [Attribution](NOTICE.md). Provider names identify integrations;
this project is not endorsed by or affiliated with those providers.
