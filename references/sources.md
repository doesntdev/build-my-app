# Authoritative sources

Documentation reviewed on 2026-09-16. Re-read the relevant source at setup/release
time; provider behavior and client configuration can change. The registry's
`reviewed_on` is a documentation-review date, not proof of live OAuth or deployment.

The Cloudflare-first and AI-economics references were reviewed on 2026-11-09;
this does not refresh the older endpoint/auth review or certify live integration.

| Stack/feasibility area | Source |
| --- | --- |
| Workers app and assets | https://developers.cloudflare.com/workers/static-assets/ |
| Workers local bindings | https://developers.cloudflare.com/workers/local-development/ |
| Workers limits and pricing | https://developers.cloudflare.com/workers/platform/limits/ and https://developers.cloudflare.com/workers/platform/pricing/ |
| D1 local SQLite | https://developers.cloudflare.com/d1/best-practices/local-development/ |
| D1 limits and pricing | https://developers.cloudflare.com/d1/platform/limits/ and https://developers.cloudflare.com/d1/platform/pricing/ |
| R2 pricing | https://developers.cloudflare.com/r2/pricing/ |
| Workflows limits | https://developers.cloudflare.com/workflows/reference/limits/ |
| Workers AI model prices | https://developers.cloudflare.com/workers-ai/platform/pricing/ |
| OpenAI API prices | https://developers.openai.com/api/docs/pricing |

For each AI estimate also retrieve the selected model's current context/output,
rate and data-handling documentation; a price table is not capability evidence.

| Area | Source |
| --- | --- |
| Skill format | https://agentskills.io/specification |
| GitHub MCP | https://github.com/github/github-mcp-server |
| GitHub hosted configuration | https://github.com/github/github-mcp-server/blob/main/docs/remote-server.md |
| GitHub Codex setup | https://github.com/github/github-mcp-server/blob/main/docs/installation-guides/install-codex.md |
| Cloudflare MCP | https://developers.cloudflare.com/agents/model-context-protocol/cloudflare/servers-for-cloudflare/ |
| Neon MCP and dev/test boundary | https://neon.com/docs/ai/connect-mcp-clients-to-neon |
| Railway MCP and auth | https://docs.railway.com/ai/mcp-server |
| Resend MCP | https://resend.com/docs/mcp-server |
| Codex MCP | https://developers.openai.com/codex/mcp |
| Claude Code MCP | https://code.claude.com/docs/en/mcp |
| Cursor MCP | https://cursor.com/docs/context/mcp |
| Hermes MCP | https://hermes-agent.nousresearch.com/docs/user-guide/features/mcp |
| Hermes schema | https://hermes-agent.nousresearch.com/docs/reference/mcp-config-reference |
| Codex skills | https://developers.openai.com/codex/skills |
| Claude Code skills | https://code.claude.com/docs/en/skills |
| Cursor skills | https://cursor.com/docs/skills |
| Podman installation | https://podman.io/docs/installation |
| Railway Containerfile path | https://docs.railway.com/guides/dockerfiles |
| Railway private registry | https://docs.railway.com/guides/private-container-registry |

Additional references to verify when the corresponding feature is in scope:

- Railway CI gating: https://docs.railway.com/deployments/github-autodeploys
- GitHub Actions: https://docs.github.com/actions
- GHCR: https://docs.github.com/packages/working-with-a-github-packages-registry/working-with-the-container-registry
- Neon connections: https://neon.com/docs/connect/connect-from-any-app
- PostgreSQL RLS: https://www.postgresql.org/docs/current/ddl-rowsecurity.html
- Cloudflare DNS: https://developers.cloudflare.com/dns/manage-dns-records/how-to/create-dns-records/
- Resend domains: https://resend.com/docs/add-a-domain
- Resend test recipients: https://resend.com/docs/dashboard/emails/send-test-emails
- MCP authorization: https://modelcontextprotocol.io/specification/latest/basic/authorization
- MCP security: https://modelcontextprotocol.io/specification/latest/basic/security_best_practices

Current pricing, quotas, plan-only features, account region and retention are
live discoveries, deliberately not hardcoded promises in this skill.
