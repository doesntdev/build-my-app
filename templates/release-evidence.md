# Release evidence

- Spec revision/requirement IDs, selected tracker work items, PRs, owner and change class:
- Work -> dev, dev -> staging and staging -> main source/target/merge identities:
- Recorded current-head review for every work and promotion PR; named team reviewers or documented solo self-review:
- Selected stack, required providers and justified exclusions:
- Material feasibility/development risks rechecked against actual behavior, mitigations and accepted limitations:
- Reviewed source commit and exact-source local/deploy checks (CI only if applicable):
- Artifact strategy: Workers version/assets OR selected container/source build:
- Workers version/deployment, asset manifest and D1/R2 binding/resource identity (if applicable):
- OCI image digest and target platform (if applicable):
- Build/scan/SBOM/provenance evidence:
- Migration version/order, rehearsal and recovery evidence:
- Config/secret names changed (never values):
- Staging deployment ID and actual acceptance results:
- Comprehensive suite execution after the actual staging merge, failures/repairs and qualified revision:
- Production approval, scope and release owner:
- Production deployment ID and read-back commit/digest:
- Fresh comprehensive suite after the actual main merge and production observation results:
- Critical user flow and persisted-state verification:
- Auth/tenant/failure-path verification:
- Cloudflare DNS/TLS/proxy/origin-control evidence:
- Resend controlled message/delivery event evidence (if applicable):
- Worker/retry/dead-letter evidence (if applicable):
- AI quality/latency/usage/spend versus estimate, quotas and admission controls (if applicable):
- Observation window, metrics and failure thresholds:
- Rollback/forward-fix and data-recovery readiness:
- Measured cache/temporary-resource cleanup and exact merged disposable branch/worktree absence/preservation:
- Follow-up issues, unverified areas and accepted limitations:

Use N/A with a reason for genuinely irrelevant checks. Keep sensitive identifiers
in private records; publish redacted evidence rather than tokens or raw logs.
