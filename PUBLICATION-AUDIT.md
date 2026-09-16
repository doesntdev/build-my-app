# Build My App — public-publication audit

Version: **0.1.1**. Review date: **2026-09-16**.

## Verdict

**Suitable for a public early release with the documented limits.** The concrete
code and documentation defects found in this audit were corrected and regression
tested. No unresolved high-severity finding was identified in the reviewed scope.
This is not a claim of comprehensive security certification, universal agent
compatibility, or completed end-to-end cloud onboarding.

This audit records the pre-publication package review. The public repository is
[doesntdev/build-my-app](https://github.com/doesntdev/build-my-app), with
[private vulnerability reporting](https://github.com/doesntdev/build-my-app/security/advisories/new)
enabled. Hosted CI and release evidence are recorded separately in
[Actions](https://github.com/doesntdev/build-my-app/actions) and
[Releases](https://github.com/doesntdev/build-my-app/releases); the local review
alone does not establish those remote results.

## Scope and method

Reviewed the entry skill, all bundled instructions/templates, helper scripts and
tests, manifest, license/attribution, CI workflow, installation behavior and naming.
An independent read-only reviewer covered documentation, setup/security sequencing,
licensing and publication experience. The controller reproduced code defects with
safe temporary fixtures and added failing tests before fixes. Read-only official
provider documentation and GitHub Action release refs were checked directly.

No real credentials were requested, no live agent configuration was changed,
and no authenticated provider mutations or application deployment occurred.

## Findings corrected

| Area | Finding | Correction and evidence |
| --- | --- | --- |
| Distribution guard | An explicit manifest entry could include `.env`, private/config files or generated material, bypassing the intended public-package exclusions. | `scripts/stack.py` rejects sensitive/generated filenames even when allowlisted. Negative tests cover environment, private state, key, backup, cache and archive paths. |
| Metadata validation | Regex extraction accepted malformed/duplicate frontmatter and ignored a directory/name mismatch. Invalid UTF-8 could raise an uncaught error. | `scripts/verify.py` enforces the documented narrow YAML subset, required fields, uniqueness, bounds, version/name agreement and readable input. Compared its successful parse with a native YAML parser. |
| Provider metadata | Malformed registry shapes could raise exceptions; an arbitrary HTTPS MCP endpoint passed structural validation. | Validate types and exact reviewed official endpoints through an independent code allowlist. Unknown endpoints and credential-reference changes fail closed. This is not protection against a maliciously modified executable. |
| Installer integrity | Extra destination files were ignored when reporting an existing installation unchanged. | Refuse additional/customized files while preserving them; harmless Python bytecode caches are the explicit exception. |
| Cross-platform paths | Path checks did not explicitly enforce case-insensitive uniqueness or Windows-reserved names. | Reject case collisions, reserved/ambiguous/nonportable names and invalid manifest versions. These rules run on every host, not only Windows. |
| Cursor onboarding | Approval checks were described after the first safe provider read. | Verify effective approvals and disable blanket auto-execution before connection/use; discover then restrict tools before the first scoped read. Generic onboarding now follows the same ordering. |
| CI portability | Push checks assumed the branch was named `main`. | Check pushes on any branch plus PRs/manual dispatch. Keep read-only permissions, pinned actions, nonpersistent checkout credentials and bounded job duration. |
| Public identity | Package identity and prompts used the working title. | Canonical name is `build-my-app`; display name is Build My App. Metadata, install examples, helper/tests and new local-state path are aligned. Version advanced to 0.1.1. |

See [validation evidence](VALIDATION.md) for the commands and boundaries actually
exercised. Regression tests guard the helper behavior and selected documentation
invariants; text checks are not proof of future model adherence.

## Privacy and license

- No personal workstation paths, private account/resource identifiers, private
  infrastructure endpoints or live credential values were identified in the
  reviewed distribution. The bundled scanner is a bounded indicator check, not a
  comprehensive secret scanner. Inspect future releases and repository history.
- PostgreSQL credentials in the templates are intentional, matching local-only
  fixtures. Loopback publication, mail capture, isolation and cleanup were tested.
  They must not become production credentials.
- The project is distributed under the MIT License with copyright attributed to
  build-my-app contributors. No provider implementation, logo or third-party
  runtime is bundled. Provider names describe integrations and carry an explicit
  non-affiliation statement.
- The chosen name is not a trademark-clearance opinion or proof that a desired
  GitHub repository/domain is available.

## Remaining limits — disclose, do not hide

1. **Provider onboarding:** official endpoints/auth recipes are documentation-
   checked. Live OAuth, actual account scopes and tool approvals must be verified
   for the user's account and agent. Codex CLI config readback omits approval-mode
   fields in the tested version; accepted TOML does not prove runtime enforcement.
2. **End-to-end behavior:** an agent has not yet built and cloud-published a complete
   application by following this new skill. Do not market it as fully certified
   across every framework or provider configuration.
3. **Platforms:** local runtime/tests were executed on Linux with Python 3.11/3.14.
   The macOS/Windows CI matrix is configured, not remotely executed. Native Podman
   VM and interactive client behavior on those hosts remain untested.
4. **Security:** instructions are not a sandbox. Provider least privilege, client
   policy and human consent are the enforcement layers. Helper path checks do not
   promise protection against an actively hostile local filesystem race.

## Publication checklist

This is a repeatable release checklist, not a substitute for live CI/release state.

- [x] Choose the owner/repository and explicitly authorize public publication.
- [x] Review the exact upload set and license; start with a clean initial history.
      If importing history later, audit that history separately.
- [x] Enable private vulnerability reporting or provide a real private contact.
- [ ] Push reviewed source, run the hosted CI matrix and investigate failures.
- [ ] Tag the approved version; publish the verified archive and checksum.
- [ ] Add the real source/download URLs to the README after they exist.
- [ ] Read back repo visibility, release files, checksum and CI results.
- [ ] Run a fresh-user pilot with consented non-production accounts before claiming
      end-to-end onboarding or deployment validation.

Each remaining release operation requires observed results for the exact candidate.
Use the public repository links above to verify live state rather than treating
an unchecked historical checklist or a local package test as the current result.
