# Contributing

Keep the entry skill small, self-contained and client-neutral. Put branch-specific
instructions in references. Use official provider endpoints and current primary
sources; never hardcode personal accounts, private URLs, machine paths or secrets.
Preserve MIT attribution. Changes to endpoint/auth/authority policy need careful
review, not only a text-match test.

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

CI is configured for pull requests, pushes on any branch, and manual dispatch,
with Linux/macOS/Windows and Python 3.11/3.14. It uses a read-only GitHub token,
does not persist checkout credentials, and caps each job at ten minutes.
Native Podman VM behavior and live client OAuth still require manual testing on
the target host. Do not upgrade “syntax tested” into “fully integrated” in reports.

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

When changing local container guidance, validate the Compose template with the
selected Podman provider and run a unique isolated PostgreSQL instance through
readiness and a real query, then verify cleanup. Application Containerfiles and
CI commands are project-specific and must be exercised when generated.

## Release

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
6. Verify the public files, CI, tag and release archive by reading them back.

No silent auto-updater. A user can inspect a newer release/commit and ask their
agent to review and apply it. Avoid requiring a particular maintainer account.
