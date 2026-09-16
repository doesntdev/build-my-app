# Local-first development

## Prerequisites and portability

Use the chosen runtime/package manager, Git, and rootless Podman. Python 3.11+
is needed only for this skill's optional helpers. Discover live versions before
recommending installation. Use official package/installer instructions with
approval; never execute a fetched installer blindly.

On Linux, check `podman info` reports rootless. On macOS/Windows inspect
`podman machine list`; initialize only if no suitable machine exists, and start
only the intended machine with approval. Verify host reachability across the VM
boundary. Windows uses PowerShell commands; a WSL-backed VM does not require the
user to perform normal development inside a WSL shell.

Portable checks:

```text
podman version
podman info
```

Compose is optional. `podman compose` delegates to an external provider. If using
the template, install/verify `podman-compose`, explicitly select it with
`PODMAN_COMPOSE_PROVIDER=podman-compose` in the process environment, and run
`podman compose version`. Do not silently select a Docker executable. A language-
native wrapper can set that environment on Linux/macOS/Windows without Bash-only
scripts. `podman run` is the straightforward alternative for a single service.

## Fast local loop

1. Run the application directly with its existing development/watch command.
2. Use ignored `.env.local` (or runtime equivalent); tracked examples contain
   safe local defaults/names only. Never import production secrets.
3. Start PostgreSQL under Podman and match the selected Neon PostgreSQL major.
   `templates/compose.local.yaml` starts at major 17 as a local baseline; update
   deliberately if the cloud target differs. Pin an approved patch/digest for
   releases. The template does not create a cloud database.
4. Use captured mail and deterministic fixtures. Store captures only in a safe
   local sink; sensitive message content should not go to production logs.
5. Run one real user flow and verify database persistence, not just HTTP 200.

From the **application directory**, after adapting/copying the template:

```text
podman compose -f compose.local.yaml up -d
podman compose -f compose.local.yaml ps
podman compose -f compose.local.yaml down
```

Select an available loopback port instead of assuming the template's default is
free. Preserve the normal development volume. Destructive tests use a unique
Compose project and disposable volume/database per run; remove only those test
resources in guaranteed cleanup. `down --volumes` is not routine dev cleanup.

Expose the canonical start/test commands through the project's runtime scripts
or a cross-platform script. Keep normal workflows independent of Make/Bash,
absolute paths, user IDs, host networking, and container-engine sockets.

## Production-parity loop

Build a minimal supported image with a non-root application user, pinned base,
reproducible lockfile install, graceful shutdown, and injected `PORT` support.
Exclude `.env*`, credentials, `.git`, local evidence, and unnecessary files with
`.containerignore`. When Railway builds from source, also supply equivalent
`.dockerignore` for its remote builder: `.containerignore` alone is insufficient.
The compatibility filename does not require a local Docker engine.

```text
podman build --file Containerfile --tag localhost/app:smoke .
podman run --rm --name app-smoke --env-file .env.local --publish 127.0.0.1:8080:8080 localhost/app:smoke
```

Adapt names/ports to avoid collisions. App binding inside the container normally
is `0.0.0.0:$PORT`; **published host binding** remains loopback. For a containerized
app and database, use a Podman network and service names. A host database URL
containing `127.0.0.1` points at the app container itself when copied unchanged;
provide distinct host-process and container-network URLs.

Wait for bounded health readiness, then exercise liveness/readiness, core API/UI,
permissions, migrations, worker behavior, and shutdown. Clean up your smoke
containers/networks, not unrelated services. A successful image build is not a
successful runtime test. Build/check the target CPU architecture for Railway;
an image tested only on ARM is not proof for an x86 deployment.

## Realistic boundaries

- Local PostgreSQL proves application/SQL behavior, not Neon branch APIs, pooling,
  extensions, TLS, suspend/resume, or recovery. Rehearse these on isolated Neon.
- Local email capture proves intent/format, not Resend delivery or deliverability.
- Local HTTP proves neither Cloudflare edge policy nor origin protection.
- Use a temporary Cloudflare tunnel only for a necessary non-production callback,
  with approval and scoped callback cleanup. Never point production callbacks at
  a laptop. Verify current tunnel limits for streaming/SSE requirements.
- Do not assume `railway dev` supports Podman. Use the native process plus Podman
  path unless current official docs and a real test establish compatibility.

## Verification ladder

Static checks → network-free unit tests → real isolated PostgreSQL integration →
Podman image runtime smoke → browser/API acceptance → changed-provider integration →
staging → production acceptance. Run every layer touched by the change, label
inapplicable layers with reasons, and keep failures observable in CI.
