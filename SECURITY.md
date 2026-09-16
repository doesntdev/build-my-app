# Security

This skill gives an agent instructions, not a sandbox or access-control system.
Enforce boundaries through your client, provider scopes and human approvals.
Inspect releases before installation and keep credentials outside this package.

Report vulnerabilities privately through
[GitHub private vulnerability reporting](https://github.com/doesntdev/build-my-app/security/advisories/new).
Private reporting is enabled for this repository. For a fork, use that maintainer's
private channel instead. Do not post exploits, tokens, customer data, account IDs,
live OAuth URLs or full environment/log dumps in public issues. Revoke exposed
credentials through the provider and use your incident process.

No telemetry, credential collection, provider login, account provisioning or
cloud writes are performed by the bundled scripts. The agent can perform those
actions only through separately authorized tools and user-owned credentials.
