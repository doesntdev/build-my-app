# Changelog

## 0.2.0

- Start with general application feasibility: technical fit, performance/scalability, security/privacy, complexity, integrations, correctness, development/test effort, usability, cost and operations; reuse accepted decisions on resume.
- Recommend Cloudflare Workers/Static Assets with D1 and private R2 only as needed, rather than a mandatory multi-vendor stack.
- Use one feature-risk loop to surface problems, recommend alternatives/proofs and decide build/prove first/reshape/defer. Keep material risks and development constraints in the charter and onboarding record.
- Retain AI quality, privacy, limits and economics as a conditional specialist reference, including the sourced book-generation example, not the organizing principle of ideation.
- Add workload-based expansion triggers for Cloudflare services, Neon, Railway, Resend and model APIs; preserve existing supported stacks.
- Align onboarding, architecture, local development, publishing and records with the selected subset.
- Default MCP fragments to Cloudflare only; retain explicit provider selections. Default doctor to Git/Node prerequisites; select `--profile container` for Podman checks.
- Validate optional-provider and container paths locally; retain historical release evidence without claiming new hosted certification.

## 0.1.1

- Renamed the skill, source package, installer identity and user prompts to Build My App (`build-my-app`).
- Block sensitive/generated manifest entries, unsafe/case-colliding paths, malformed metadata and unreviewed provider endpoints.
- Refuse customized installs with extra files instead of reporting them unchanged.
- Align Cursor and generic onboarding with policy-before-use ordering.
- Run CI on any branch and manual dispatch with nonpersistent checkout credentials.
- Expand to 58 regression tests and record public-release findings and validation limits.

## 0.1.0

- Standalone Agent Skills package with local-first, framework-neutral delivery.
- Guided/resumable official MCP setup for the selected stack.
- Codex, Claude Code, Cursor, and Hermes config fragments with secret indirection.
- Issue-to-release SDLC, environment separation, recovery and operational ownership.
- Standard-library helpers, manifest-based installation, tests and CI matrix.
