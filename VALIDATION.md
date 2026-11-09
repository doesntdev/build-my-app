# Build My App — validation record

## 0.2.0 — general application feasibility refinement

This refines the same unpublished local candidate on 2026-11-09. General
application and development feasibility now drives ideation; AI is one optional
specialist branch. No new helper runtime or provider behavior was introduced.

| Check | Observed result |
| --- | --- |
| Manifest-only installation | 41 allowlisted files; dry run, apply, identical rerun and exact source-byte parity passed |
| Installed package validator | Valid on Python 3.14.9 and 3.11.15 |
| Installed offline unittest suite | 75 tests passed on each interpreter |
| New general-feasibility contracts | Non-AI risk coverage, conditional AI loading, unresolved-risk state and non-AI scenarios covered; missing contracts observed failing before edits |
| AI reference extraction | Existing specialist questions, numerical example and dated sources preserved byte-for-byte; SHA-256 of the relocated section is `934bfc7afbc5c6c1f324c62e140ef13e9f9e6f3a1bec369655da1af967cc5fce` |
| Existing installation safety | Customized SKILL.md refused without overwriting it |
| Artifact lifecycle | Qualification directories removed; no new project bytecode/build cache retained; existing graph kept |

The current tested source-core SHA-256 is
`cf257c308ee8b35b4397b1fbcd8c4beffd22e43569078a9b630f041cf8d3441d`,
using the sorted manifest-path/NUL/file-digest procedure described below and
excluding this validation record. Revalidate this record-only update afterward.

The entrypoint, general ideation guide, onboarding, platform selection, SDLC,
charter/state, release evidence and README now share the general feature-risk
loop. Non-AI scenario rubrics include offline conflicts, concurrent booking and
payment, inaccessible integrations, large uploads, CPU-heavy reports, constrained
solo delivery, sensitive multi-user records and delivery/relevance quality.
They received instruction-level review, not live model-behavior or application
execution. The earlier tabletop examples below remain historical; they are not
new behavioral proof for this refinement. Deterministic text checks cannot certify
future agent reasoning, legal compliance or a generated app's real-world feasibility.

At this qualification checkpoint, source changes were local/uncommitted. No push,
active-client installation, cloud resource, paid inference, live OAuth or GitHub
Actions run was part of these checks. Subsequent source publication is a separate,
owner-authorized operation recorded in Git history.

## 0.2.0 — earlier Cloudflare-first candidate qualification

The following receipt predates the general-feasibility refinement above.

Local qualification performed on 2026-11-09. The source update is local and
uncommitted; no source publication, release, active-client installation, cloud
mutation or paid inference is implied.

| Check | Observed result |
| --- | --- |
| Manifest-only installation | 40 allowlisted files; dry run, apply, identical rerun and byte/hash parity passed |
| Installed `python scripts/verify.py` | Valid on Python 3.14.9 and 3.11.15; no structure, syntax, link, endpoint or privacy errors |
| Installed `python -m unittest discover -s tests -q` | 71 tests passed on each of Python 3.14.9 and 3.11.15 |
| Customized-install refusal | Differing SKILL.md refused without overwriting the local fixture |
| Cloudflare prerequisite doctor | Passed Git/Node availability; Node 24.15.0; global Wrangler absent and explicitly optional, project tooling/auth/app not tested |
| Container prerequisite doctor | Passed with rootless Podman; no new Postgres container started |
| Full-provider config paths | Four clients, HTTP/stdio parsing, explicit selections and existing secret/approval controls covered by the offline suite |
| Cloudflare private-state boundaries | `.dev.vars` and `.wrangler` rejected as package inputs; application Git/build exclusions covered |
| Independent read-only source review | Core behavior supported; one leftover Neon-specific rehearsal instruction identified |
| Review repair | Parent verified the finding, made Postgres rehearsal use the selected platform and added a regression; final suite rerun |
| Tabletop behavior examples | Static portfolio omits unused services; book-generator fixture explains budget mismatch first; unchanged existing Postgres/Railway fix preserves its stack |
| Book-example arithmetic | Calculated with Decimal; repeated input, two text passes and retry reserve included; dated official price sources linked in ideation |
| Temporary installation cleanup | Owned qualification directories removed; no active client or provider configuration changed |
| Existing source controls | Workflow, provider endpoint registry, license/attribution and Compose template unchanged |

The tested source core is SHA-256
`43843f626de60aa2d537f1ad75b351a23708ca57c7b81c07e3dcec80d1ab79d2`:
sort MANIFEST paths except this validation record, then hash the concatenation
of UTF-8 relative path, NUL and SHA-256 digest bytes of each file. The record-only
update is checked afterward with the strict package validator.

The developer checkout's direct validator initially rejected its existing,
unallowlisted `graphify-out` artifacts. This is an intentional distribution
boundary, not a package failure or permission to delete the graph. Qualification
used the manifest-only installed package; no validator exclusions were weakened.
The narrowed helper contracts were observed failing before implementation.

Behavior examples are tabletop responses from an isolated review, not a benchmark
of model reliability. No end-to-end generated Cloudflare application, live OAuth,
hosted capacity, model quality/latency, real book generation, actual invoice or
production deployment was validated. The worked costs are explicit planning
assumptions, not measured usage. No GitHub Actions were queried or run for this
update; the previous package workflow was left unchanged.

## 0.1.1 — historical validation

Local checks performed on 2026-09-16 before the first public release. This is
bounded evidence, not certification of every client, provider, operating system,
or possible generated application. Current hosted CI is available in
[GitHub Actions](https://github.com/doesntdev/build-my-app/actions), and published
artifacts are listed under [Releases](https://github.com/doesntdev/build-my-app/releases).
The [publication audit](PUBLICATION-AUDIT.md) records findings, fixes and open limits.

## Executed on the renamed package

| Check | Observed result |
| --- | --- |
| `python scripts/verify.py` | Valid: package frontmatter/identity, syntax, links, safe paths, allowlist, official MCP endpoints and privacy indicators |
| `python -m unittest discover -s tests -q` on Python 3.14.4 | 58 tests passed |
| Same validator and test suite on Python 3.11.15 | 58 tests passed |
| Agent Skills frontmatter via a native YAML parser | Matched the strict package validator; supported fields, name, version and string metadata passed |
| Codex, Claude Code, Cursor and Hermes generated fragments | Parsed as TOML/JSON; Hermes fragment also parsed as YAML |
| Codex CLI 0.154.0 using an isolated temporary config | All five server entries read successfully; no login or provider call |
| Codex GitHub config readback | Exact hosted URL, token environment-variable name and read-only header returned |
| Rootless Podman 5.7.0 and podman-compose 1.6.0 | Local prerequisite diagnostic passed |
| Compose template with an isolated project and dynamic loopback port | Parsed, started PostgreSQL, passed readiness and a real SQL query |
| SQL `SELECT current_database(),current_user;` | Returned `app_local|app_local` |
| Host connectivity and published container port inspection | Host reachable; PostgreSQL published only on loopback |
| Temporary Compose cleanup | Zero matching containers, volumes or networks remained |
| Install dry run / apply / identical rerun / customized-install refusal | Passed in disposable directories; manifest-file bytes verified; user customization preserved |
| Native YAML check of CI | PR, any-branch push and manual triggers parsed; read-only permission, nonpersistent checkout credential and timeout checked |
| Pinned GitHub Actions | Both full commit pins matched the stated official release tags |
| Current official provider documentation | All five MCP URLs and the Neon development/testing restriction reconfirmed |
| Naming sweep | No working-title package slug remained in the allowlisted distribution |

The test count refers to unittest test methods, some of which exercise multiple
invalid inputs. Negative cases were observed failing before their fixes, including
private manifest entries, malformed metadata, unreviewed endpoints, customized
installs, Cursor policy ordering and branch-specific CI assumptions.

The Codex CLI readback did **not** expose its approval-mode field. The generated
TOML carries `default_tools_approval_mode = "prompt"`, documented by the client,
but live enforcement still needs verification in the user's actual host. Setup
instructions distinguish that gate from parsing a config.

## Review boundaries

An independent read-only reviewer inspected instructions/templates/attribution
and identified Cursor policy ordering and the CI branch assumption. The controller
verified and corrected those findings, reviewed helper failure paths, and reran
all tests.

Scenario coverage in `tests/scenarios.md` received instruction-level review,
not actual model-behavior execution. Deterministic tests check helpers and selected
instruction/config invariants; they cannot establish a model's future behavior.

## Hosted CI

The [first public CI run](https://github.com/doesntdev/build-my-app/actions/runs/35139096695)
passed for source commit `b885ebd408b067663a0dbc55f411344e4c55bd37` on Linux,
macOS and Windows with both Python 3.11 and 3.14. All six jobs ran the package
validator and 58 tests successfully. The release record links the exact final
candidate's CI run; subsequent revisions must earn their own green checks.

Hosted helper tests do not validate interactive OAuth, Podman VM networking,
provider account scope or an agent-generated application's cloud deployment.

## Not executed or not claimed

- Live OAuth or authenticated MCP calls for the five providers.
- End-to-end app creation and deployment by an agent following this new skill.
- Real email sends, DNS mutations, purchases, or cloud resource provisioning.
- Native macOS/Windows Podman or client integrations.
- Publication or deployment success inferred from tests alone; verify the
  separate live Releases record and any application deployment evidence.
- Comprehensive security audit or proof of all scanner false-negative cases.

These remain target-user or post-publication validation steps. No live agent
configuration or provider account was changed to validate this distribution.
