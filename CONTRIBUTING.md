# Contributing

Keep the entry skill small, self-contained and client-neutral. Put branch-specific
instructions in references. Use official provider endpoints and current primary
sources; never hardcode personal accounts, private URLs, machine paths or secrets.
Preserve MIT attribution. Changes to endpoint/auth/authority policy need careful
review, not only a text-match test.

The dev/staging/main policy taught by the skill governs application delivery.
Editing/publishing this instruction package does not itself adopt that branch
policy in this repository, create integration branches/resources or change native
rules. Package publication follows the owner's actual scope and repository controls.
Use a work branch and record qualified review for package PRs; never infer a native
self-approval or permission to publish from local tests.

## Required checks

From the package directory with Python 3.11+:

```text
python scripts/verify.py
python -m unittest discover -s tests -v
python scripts/stack.py doctor --stage local
```

The first two are deterministic and require no cloud credentials. The doctor is
a live diagnostic: absent/unready prerequisites return exit 1 rather than a fake
pass; its result is not app or provider authentication evidence.
Doctor defaults to the Cloudflare Git/Node profile; use `--profile container` only
for the container extension. It does not install or verify project-local Wrangler.
The MCP generator now defaults to Cloudflare; preserve full explicit-provider
and security-policy coverage when testing its narrower default.

Validate a manifest-only installation when the developer checkout contains local
graphs or other non-distributable files. The strict validator correctly refuses
unallowlisted source-tree extras; do not weaken it or delete useful local state to
manufacture PASS. Run the installed package's validator and complete offline suite.

Run package checks locally. Existing workflow assets remain prior repository
content, not a new hosted-CI requirement or evidence of this candidate's acceptance.
Do not query/dispatch hosted workflows for local qualification. Native destination
controls still apply to authorized publication; resolve real conflicts explicitly.
Native Podman VM behavior and live client OAuth require testing on the target host.
Do not upgrade “syntax tested” into “fully integrated” in reports.

The bundled validator is package-specific, not a general YAML or Agent Skills
implementation. Its frontmatter subset supports single-line plain/JSON-quoted
strings and a two-space-indented metadata mapping of JSON-quoted strings.
Unsupported syntax and duplicate keys fail closed. If extending that subset,
add negative tests and compare with a real YAML parser or the official skill
validator. Distribution paths are deliberately restricted to portable names;
private/config/generated filenames remain blocked even if added to the manifest.
The official endpoint allowlist in `scripts/stack.py` is independent of the
provider metadata: changes require reviewing both, not just changing a URL.

## Behavior evaluation

Use `tests/scenarios.md` in an actual agent session for an instruction review.
Record actions, evidence and violations. Deterministic helper tests cannot prove
a model always follows a prompt. Never use real production writes to run an eval.

When changing ideation/stack selection, review general application feasibility,
scaling, security, complexity, correctness, dependencies, development effort,
usability, cost and operations. Include non-AI cases such as offline sync, concurrent
booking/payment, unavailable APIs, large uploads and a constrained solo build,
as well as existing stacks, optional providers, resume and uncertain pricing.
Load AI details only for an AI case. Check actual arithmetic; text assertions
are regression guards, not behavioral proof or a substitute for targeted experiments.

For SDLC edits, reconcile progressive spec creation, alternative tracker access,
spec-to-ticket traceability, branch/promotion edges, team reviewer requests, solo
self-review, review invalidation and safe merged-worktree/cache retirement. Cover
blocked/dirty/unique-state paths as well as happy-path text markers. Package tests
do not prove live provider/PR behavior or mechanically enforce the taught policy.

When changing container runtime commands/templates, validate the Compose template with the
selected Podman provider and run a unique isolated PostgreSQL instance through
readiness and a real query, then verify cleanup. Application Containerfiles and
selected local/deploy commands are project-specific and must be exercised when generated.

## Release

Use patch increments within the current major/minor series unless the owner
explicitly requests a minor/major change. Workflow/feature scope alone does not
authorize incrementing the second component. Keep the declared version aligned
across entrypoint, manifest and changelog.

1. Update `metadata.version` in `SKILL.md`, `MANIFEST.json` and changelog together.
2. Keep `MANIFEST.json` an explicit allowlist. Include new files deliberately;
   never distribute `.git`, caches, credentials, local onboarding or raw logs.
3. Run checks; inspect the full diff and optional dedicated secret scanner.
   The bundled regex/privacy validator is defense in depth, not a comprehensive
   security or licensing audit.
4. Test installation into a temporary destination: dry-run, apply, identical
   rerun, modified-file refusal. Existing customized installations must be backed
   up and upgraded deliberately, not overwritten by this installer.
5. Publish only after the owner approves the actual public repo and release.
   Never infer source visibility from deployment visibility.
6. Read back exactly the authorized remote refs/files and any requested tag/release
   archive. Source publication, release creation and active-client installation are
   distinct operations; none follows automatically from local qualification.

The read-only update check is informational, not a silent auto-updater. Fetch only
canonical public metadata under the documented deadline/size/redirect limits;
ordinary offline tests mock that boundary, and real checks are separately labeled.
Test version comparisons, invalid input, offline/timeout, no local mutation and
consent-only upgrade instructions. A user can inspect a newer release/commit and
ask their agent to review/apply it while preserving customizations. No maintainer
login is required, and an unavailable lookup must not block normal application work.
