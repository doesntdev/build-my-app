# MCP setup by client

Read onboarding and provider rules before applying these recipes. Use the current
client `--version` and `mcp --help` to verify flags. All examples carry endpoint
URLs or secret **names**, not secret values. Render only the services being added:

```text
python scripts/stack.py mcp-config --client codex --providers cloudflare
```

Generated fragments are not merge tools or authorization enforcement. They must
be reviewed, merged without duplicate server keys, and verified in the live host.
Omitting `--providers` now renders Cloudflare only. Add `github`, `neon`, `railway`
or `resend` explicitly when selected; the recipes below are alternatives, not a
setup sequence requiring every server. An existing working client connection
can be reused without rendering a second one.
The GitHub fragment deliberately sets `X-MCP-Readonly: true`. Leave it during
onboarding; routine issue/PR writes need a separately approved capability change
or a scoped `gh` workflow. Do not use a read-only config as a reason to silently
bypass the agreed write boundary through a different tool.

## Codex

Docs: https://developers.openai.com/codex/mcp

Inspect `codex mcp list` and the active config source. The user config normally is
`~/.codex/config.toml`; trusted projects can have `.codex/config.toml`. Do not
modify plugin-provided servers by inventing incomplete global entries.

```text
codex mcp add cloudflare --url https://mcp.cloudflare.com/mcp
codex mcp add neon --url https://mcp.neon.tech/mcp
codex mcp add railway --url https://mcp.railway.com
codex mcp add resend --url https://mcp.resend.com/mcp
codex mcp add github --url https://api.githubcopilot.com/mcp/ --bearer-token-env-var GITHUB_MCP_TOKEN
```

Run only the selected add command. It registers a server, not the safety policy.
If adding starts OAuth, complete that single consent flow without invoking any
provider tools. Then complete the checkpoint below before continuing.

### CLI safety checkpoint

After every CLI add, render and **merge** that provider's complete fields into its
existing table, preserving unrelated settings. For example, GitHub:

```text
python scripts/stack.py mcp-config --client codex --providers github
```

Require `http_headers` with `X-MCP-Readonly` set to the string `true` for GitHub,
and `default_tools_approval_mode = "prompt"` for every server. The bare add commands
above do not install these controls. Verify the current client supports them and
that higher-scope configuration has not overridden them; read back the effective
fields through targeted config inspection without displaying secret values.
Some `codex mcp get --json` versions omit approval-mode fields: their absence in
that output does not prove enforcement or rejection. Check the supported schema
and the running host's effective approval policy separately; parsing TOML alone
is insufficient. If enforcement cannot be established, keep writes blocked.
Complete this checkpoint **before tool discovery** in the operator session or
any provider tool call. If the CLI automatically discovers metadata during add,
that is not approval to use the tools. For policy-before-connect requirements,
merge the rendered configuration directly instead of using the add command.

For OAuth servers use `codex mcp login <name>` if adding did not complete login.
For GitHub hosted MCP, default to a fine-grained PAT referenced with
`bearer_token_env_var`; do not assume generic OAuth registration works. The user
injects the token into the agent's environment securely. An arbitrary `.env`
file is not automatically loaded by every client.

After discovery, set `enabled_tools` for narrow access before the first scoped
read. Broad Cloudflare `execute` is reviewed per operation, regardless of any
misleading read-only annotation. If the installed client cannot enforce the
required boundary, keep that server blocked or use an approved constrained path.

To reuse an existing Railway CLI session instead:

```text
codex mcp add railway -- railway mcp
```

Use `/mcp` in the running host to confirm actual tools, then call the provider's
safe read. `codex mcp list` alone proves neither discovery nor authorization.

## Claude Code

Docs: https://code.claude.com/docs/en/mcp

Inspect `claude mcp list`. Choose local (user + project), project (`.mcp.json`),
or user scope intentionally; `local` is the safe default for personal setup.

```text
claude mcp add --scope local --transport http cloudflare https://mcp.cloudflare.com/mcp
claude mcp add --scope local --transport http neon https://mcp.neon.tech/mcp
claude mcp add --scope local --transport http railway https://mcp.railway.com
claude mcp add --scope local --transport http resend https://mcp.resend.com/mcp
claude mcp add --scope local --transport stdio railway -- railway mcp
```

The last command is an alternative, not a second Railway server. Run `/mcp` to
complete OAuth and inspect discovery. Keep approval prompts and restrict tools
through the client's permission controls; never use blanket bypass mode.

For GitHub, the generated JSON contains `type: http`, the official URL, and the
literal string `Bearer ${GITHUB_MCP_TOKEN}`. Merge this fragment through a secure
file editor into the selected scope. Claude expands environment references at
runtime. Do not build a shell `--header` argument containing the real token.
Do not omit the HTTP `type`: Claude can otherwise interpret the entry as stdio.

## Cursor

Docs: https://cursor.com/docs/context/mcp

Merge the rendered `mcpServers` fragment into the chosen project
`.cursor/mcp.json` or user MCP config. OAuth servers need their `url`; GitHub uses
`Bearer ${env:GITHUB_MCP_TOKEN}`. Cursor interpolation differs from Claude's.
Supply the environment through a secure launcher/credential integration; a GUI
launched from a desktop may not inherit shell variables. Before connecting,
disable blanket automatic execution and verify the effective approval policy
in the installed client. Keep provider scopes minimal. Confirm the chosen server
in MCP settings, complete provider consent, then discover tools. Restrict tool
access to the required read-only surface before you perform a safe read. If the
host automatically fetches metadata during setup, that does not authorize a tool
call. Unverifiable approval controls block provider use, not independent local work.

## Hermes

Docs: https://hermes-agent.nousresearch.com/docs/user-guide/features/mcp
and https://hermes-agent.nousresearch.com/docs/reference/mcp-config-reference

Resolve the **active profile**, back up its config securely, and inspect native
CLI help. Do not install into another profile or replace the entire mapping.

```text
hermes mcp list
hermes mcp add cloudflare --url https://mcp.cloudflare.com/mcp --auth oauth
hermes mcp add neon --url https://mcp.neon.tech/mcp --auth oauth
hermes mcp add railway --url https://mcp.railway.com --auth oauth
hermes mcp add resend --url https://mcp.resend.com/mcp --auth oauth
```

For Railway stdio use `hermes mcp add railway --command railway --args mcp` instead.
After a native add, merge and verify the selected rendered fields below before
operator-session discovery/use; native add alone is not proof of trust, sampling
or tool policy. For policy-before-connect requirements, merge configuration first
instead of using an add command that may probe the server automatically.
Use `hermes mcp login <name>` if needed, `hermes mcp test <name>` for discovery,
and `hermes mcp configure <name>` to select tools. Then execute a live scoped read.

The helper emits a **JSON fragment valid as YAML**, under `mcp_servers`; merge
its fields into the existing YAML rather than replacing the whole file. It sets
`trust: untrusted`, sampling disabled, and runtime environment indirection for
GitHub. Confirm these fields against the live config reference. Keep tokens in
the active profile's secure secret source. Reload/reset the session as needed;
a long-running gateway restart needs approval.

## Other agents and unsupported flows

Inspect the actual client's official docs for Streamable HTTP, stdio, OAuth,
secret indirection, config scope, and reload procedure. Translate the provider
registry into its schema. A `mcpServers` object is **not** universal. VS Code,
OpenCode, Gemini and others have different wrappers/fields.

If the host lacks remote OAuth, use a documented official CLI/stdio path or a
least-privilege token only with secure storage and approval. A stdio-to-HTTP
bridge adds software and trust; explain it, pin a reviewed version, and ask first.
For a browser-only agent with no shell/filesystem, report that local build/Podman
needs a connected local coding environment. Do not pretend a connector can run
containers on the user's laptop.

## Failure and revocation

Distinguish: wrong endpoint/transport; network failure; provider consent pending;
callback failure; missing token; scope denied; tools filtered; stale running host.
An HTTP GET 404/405 is not an MCP handshake test. Use real initialize/tools/list.
Run one OAuth transaction at a time. Use the client's secure completion channel
for redirects; never request callback codes in ordinary chat. Do not delete a
shared auth cache or broaden scopes as a reflex.

On removal, revoke the provider grant/token separately, remove only the selected
server/config entry, clear only its credential cache via supported tools, and
verify absence. Removing a config entry does not itself revoke access.
