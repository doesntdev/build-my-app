# Build My App 0.1.1 — validation record

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

## Not executed or not claimed

- Live OAuth or authenticated MCP calls for the five providers.
- End-to-end app creation and deployment by an agent following this new skill.
- Real email sends, DNS mutations, purchases, or cloud resource provisioning.
- Native macOS/Windows Podman or client integrations.
- Hosted CI or publication status inferred from these local checks; verify the
  separate live Actions and Releases records linked above.
- Comprehensive security audit or proof of all scanner false-negative cases.

These remain target-user or post-publication validation steps. No live agent
configuration or provider account was changed to validate this distribution.
