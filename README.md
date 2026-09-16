# Build My App

**An agent skill for building an app locally, connecting your own cloud accounts,
and taking it through a real development and release lifecycle.**

Podman · GitHub · Neon · Cloudflare · Railway · Resend

Bring your coding agent and your accounts. Ask for an app. The skill guides the
agent through local setup, official MCP connections, implementation, testing,
review, deployment, and maintenance. It keeps human consent where it belongs:
account login, spending, publishing, and production changes.

## What you get

- A framework-neutral `SKILL.md` following the [Agent Skills standard](https://agentskills.io/specification).
- Progressive onboarding: a useful local app before cloud setup becomes necessary.
- Official MCP recipes and configuration generators for **Claude Code, Codex,
  Cursor, and Hermes**, plus a generic-client adaptation procedure.
- Rootless Podman development, local PostgreSQL, mail capture, and container smoke tests.
- GitHub issue ownership, branch/PR coordination, CI, staged releases, rollback,
  incidents, and ongoing operations.
- Portable Python helpers, templates, deterministic tests, and a package/privacy check.

This is **not** an app generator executable, a hosted service, an agent runtime,
or a promise that every client supports every OAuth flow. Your agent reads the
workflow and does the work through its own tools. No broker, author's account,
private skill, or additional model API subscription is required by this package.

“Local-first” describes the development workflow. Application-level offline sync
is an explicit product requirement, not something this stack supplies for free.

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
> help me define the smallest useful version. Get it running locally with Podman,
> then walk me through the official MCP connections for GitHub, Neon, Railway,
> Cloudflare, and Resend. Run the SDLC, and ask before spending or publishing.

For an existing app:

> Adopt build-my-app in this repository. Preserve the framework and
> current work. Audit the gaps, connect missing MCPs, and ship one agreed slice.

For just setup:

> Use build-my-app to connect my provider MCPs in this agent. Discover
> what already exists, back up config, and verify each with a read-only call.

For a resume:

> Resume build-my-app from the onboarding record and current GitHub
> issue. Recheck access and ownership; don't repeat completed setup.

## Helpers

```text
python scripts/stack.py doctor --stage local
python scripts/stack.py doctor --stage publish
python scripts/stack.py mcp-config --client codex
python scripts/stack.py mcp-config --client claude-code --providers github cloudflare
python scripts/stack.py mcp-config --client cursor --providers railway --railway-transport stdio
python scripts/stack.py mcp-config --client hermes --providers neon
```

`doctor` checks command availability and Podman readiness, not cloud auth or app
readiness. `mcp-config` prints a **fragment**, never edits live configuration or
reads secret values. It defaults Railway to remote OAuth; select stdio to reuse
an authenticated Railway CLI. Authenticate through your actual agent after
reviewing and merging the selected entries. See [client setup](references/mcp-clients.md).

## Boundaries

- Cloud services, domains, CI, storage, and email can cost money. Your agent must
  inspect current pricing and get your budget approval before provisioning.
- Local development needs initial runtime/package/image downloads; it does not
  need production credentials or cloud services for core tests.
- Neon MCP is for development/testing only. Production changes use reviewed
  migrations and release credentials, never an agent's ad hoc SQL tool.
- A source repository stays private unless you explicitly choose public. A public
  deployment is also a separate approval from pushing source.
- Framework support is procedural, not a tested matrix of every web framework.
  Client config tests are not proof of live OAuth in every client/OS combination.
- No automatic updater, background service, telemetry, or subscription is bundled.

## Releases and contributions

The public source is [doesntdev/build-my-app](https://github.com/doesntdev/build-my-app).
This is a standalone, MIT-licensed package; its runtime does not depend on the
maintainer's accounts or infrastructure. Forks can use their own repository and
release process. No automatic update endpoint is built in.

CI is configured for PRs, pushes on any branch and manual dispatch across Linux,
macOS and Windows. Check the [actual runs](https://github.com/doesntdev/build-my-app/actions),
not merely the workflow file. See [the audit](PUBLICATION-AUDIT.md) and
[contributing](CONTRIBUTING.md) for the release checks and known limits.

## Validation

See [the validation record](VALIDATION.md) for executed checks and explicit gaps.
Version 0.1.1 passed 58 tests on Python 3.11 and 3.14 and a real isolated
Podman/Postgres smoke test. Live provider OAuth and cloud deployment are not
certified by those tests.

## License

[MIT](LICENSE). [Attribution](NOTICE.md). Provider names identify integrations;
this project is not endorsed by or affiliated with those providers.
