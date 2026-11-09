#!/usr/bin/env python3
"""Read-only diagnostics, secret-free config rendering, explicit skill installation."""
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import platform
import re
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
NAME = "build-my-app"
CLIENTS = ("codex", "claude-code", "cursor", "hermes")
PROVIDER_NAMES = ("github", "neon", "railway", "cloudflare", "resend")
DEFAULT_PROVIDERS = ("cloudflare",)
PROFILES = ("cloudflare", "container")
# Security allowlist, intentionally independent of editable provider metadata.
# Changing an endpoint requires reviewing both the source and this policy.
OFFICIAL_MCP_URLS = {
    "github": "https://api.githubcopilot.com/mcp/",
    "neon": "https://mcp.neon.tech/mcp",
    "railway": "https://mcp.railway.com",
    "cloudflare": "https://mcp.cloudflare.com/mcp",
    "resend": "https://mcp.resend.com/mcp",
}


def registry(root=ROOT):
    value = json.loads((Path(root) / "references/providers.json").read_text(encoding="utf-8"))
    providers = value.get("providers") if isinstance(value, dict) else None
    if not isinstance(providers, dict) or set(providers) != set(PROVIDER_NAMES):
        raise ValueError("Provider registry does not match the supported stack")
    for name, provider in providers.items():
        if not isinstance(provider, dict) or provider.get("url") != OFFICIAL_MCP_URLS[name]:
            raise ValueError("Provider endpoint is not on the reviewed official allowlist")
    if providers["github"].get("token_env") != "GITHUB_MCP_TOKEN":
        raise ValueError("GitHub credential reference must be the documented environment name")
    return providers


def render_config(client, providers=None, railway_transport="http"):
    """Return a fragment only. Never resolve credentials or change client files."""
    if client not in CLIENTS or railway_transport not in ("http", "stdio"):
        raise ValueError("Unsupported client or transport")
    names = list(DEFAULT_PROVIDERS if providers is None else providers)
    if not names or len(names) != len(set(names)) or any(n not in PROVIDER_NAMES for n in names):
        raise ValueError("Select unique, supported providers")
    entries = {}
    providers_by_name = registry()
    for name in names:
        provider = providers_by_name[name]
        is_stdio = name == "railway" and railway_transport == "stdio"
        entry = {"command": "railway", "args": ["mcp"]} if is_stdio else {"url": provider["url"]}
        if client == "claude-code":
            entry["type"] = "stdio" if is_stdio else "http"
        if name == "github":
            if client == "codex":
                entry["bearer_token_env_var"] = provider["token_env"]
                entry["http_headers"] = {"X-MCP-Readonly": "true"}
            else:
                variable = "${env:GITHUB_MCP_TOKEN}" if client == "cursor" else "${GITHUB_MCP_TOKEN}"
                entry["headers"] = {"Authorization": "Bearer " + variable, "X-MCP-Readonly": "true"}
        if client == "codex":
            entry["default_tools_approval_mode"] = "prompt"
            entry["startup_timeout_sec"] = 60
            entry["tool_timeout_sec"] = 120
        elif client == "hermes":
            if not is_stdio and name != "github":
                entry["auth"] = "oauth"
            entry.update(enabled=True, trust="untrusted", connect_timeout=60, timeout=120)
            entry["sampling"] = {"enabled": False}
        entries[name] = entry
    if client != "codex":
        key = "mcp_servers" if client == "hermes" else "mcpServers"
        return json.dumps({key: entries}, indent=2) + "\n"
    lines = ["# Review and merge these tables; never overwrite the complete client config."]
    for name, entry in entries.items():
        lines.extend(["", f"[mcp_servers.{name}]"])
        for key, value in entry.items():
            if isinstance(value, dict):
                rendered = "{ " + ", ".join(json.dumps(k) + " = " + json.dumps(v) for k, v in value.items()) + " }"
            else:
                rendered = json.dumps(value)
            lines.append(f"{key} = {rendered}")
    return "\n".join(lines) + "\n"


def probe(command, timeout=10):
    """Bounded noninteractive subprocess; callers must not return raw output."""
    executable = shutil.which(command[0])
    if not executable:
        return "missing", ""
    try:
        result = subprocess.run([executable, *command[1:]], capture_output=True, text=True, errors="replace",
                                timeout=timeout, check=False, shell=False)
    except subprocess.TimeoutExpired:
        return "timeout", ""
    except OSError:
        return "failed", ""
    return ("ok", result.stdout) if result.returncode == 0 else ("failed", "")


def doctor(stage="local", runner=probe, system=None, profile="cloudflare"):
    """Check selected prerequisites only; never log in or download project tools."""
    if stage not in ("local", "publish"):
        raise ValueError("Unknown stage")
    if profile not in PROFILES:
        raise ValueError("Unknown profile")
    system = system or platform.system()
    checks = []
    required_names = ("git", "node") if profile == "cloudflare" else ("git", "podman")
    optional_names = ("wrangler", "gh") if profile == "cloudflare" else ("gh", "railway", "podman-compose")
    for name in (*required_names, *optional_names):
        required = name in required_names
        status, output = runner([name, "--version"], timeout=10)
        version = re.search(r"\bv?(\d+\.\d+(?:\.\d+)?)\b", output) if status == "ok" else None
        checks.append({"check": name, "required": required, "status": status,
                       "version": version.group(1) if version else None})
    if profile == "container":
        status, output = runner(["podman", "info", "--format", "json"], timeout=15)
        rootless = None
        if status == "ok":
            try:
                info = json.loads(output)
                rootless = info["host"]["security"]["rootless"]
                if not isinstance(rootless, bool):
                    raise ValueError("Invalid rootless field")
            except (ValueError, TypeError, KeyError):
                status = "invalid_response"
            if status == "ok" and system == "Linux" and rootless is not True:
                status = "rootful_not_approved"
        checks.append({"check": "podman-runtime", "required": True, "status": status,
                       "rootless": rootless if isinstance(rootless, bool) else None})
    ready = all(c["status"] == "ok" for c in checks if c["required"])
    if profile == "cloudflare":
        next_action = ("Verify project-local Wrangler, supported Node version, framework and local-only bindings; "
                       "run the actual application/tests. Provider authentication remains separate.")
        if not ready:
            next_action = "Resolve missing Git/Node prerequisites, then verify project-local Wrangler and local-only bindings."
    elif ready:
        next_action = "Verify project runtime and run the actual local application/tests; connect providers separately."
    elif system in ("Darwin", "Windows"):
        next_action = "Inspect missing prerequisites and podman machine list; obtain approval before initializing/starting a machine."
    else:
        next_action = "Resolve missing/unready prerequisites; verify rootless Podman before container work."
    return {"stage": stage, "profile": profile, "system": system, "ready": ready,
            "scope": "prerequisites_only", "checks": checks,
            "provider_authentication": "not_tested", "application_health": "not_tested",
            "next_action": next_action}


def package_path(relative):
    """A deliberately portable distribution subset, not arbitrary filesystem paths."""
    if not isinstance(relative, str) or not relative:
        raise ValueError("Unsafe package path")
    path = PurePosixPath(relative)
    if path.is_absolute() or ".." in path.parts or str(path) != relative:
        raise ValueError("Unsafe package path")
    reserved = {"con", "prn", "aux", "nul", *("com" + str(n) for n in range(1, 10)),
                *("lpt" + str(n) for n in range(1, 10))}
    private_dirs = {".git", "__pycache__", ".venv", "node_modules", "dist", ".wrangler", ".local-first",
                    ".build-my-app", ".codex", ".claude", ".cursor", ".hermes"}
    for part in path.parts:
        lower = part.lower()
        if not re.fullmatch(r"[A-Za-z0-9_.-]+", part) or part.endswith(".") or lower.split(".")[0] in reserved:
            raise ValueError("Non-portable package path")
        if (lower in private_dirs
                or (lower == ".env" or lower.startswith(".env.")) and lower != ".env.example"
                or (lower == ".dev.vars" or lower.startswith(".dev.vars.")) and lower != ".dev.vars.example"):
            raise ValueError("Private/generated paths cannot be distributed")
    if path.suffix.lower() in {".pyc", ".pyo", ".pem", ".key", ".bak", ".zip"}:
        raise ValueError("Private/generated files cannot be distributed")
    if path.name.lower() in {"auth.json", "credentials.json", "tokens.json", ".mcp.json"}:
        raise ValueError("Credential/config files cannot be distributed")
    return path


def safe_file(root, relative):
    path = package_path(relative)
    full = root.joinpath(*path.parts)
    for candidate in (full, *full.parents):
        if candidate == root.parent:
            break
        if candidate.is_symlink():
            raise ValueError("Package symlinks are not permitted")
    if not full.is_file() or not full.resolve().is_relative_to(root.resolve()):
        raise ValueError("Missing or escaped package file: " + relative)
    return full


def package_files(root=ROOT):
    root = Path(root).absolute()
    manifest_file = safe_file(root, "MANIFEST.json")
    manifest = json.loads(manifest_file.read_text(encoding="utf-8"))
    if not isinstance(manifest, dict) or manifest.get("name") != NAME:
        raise ValueError("Invalid package identity")
    version = manifest.get("version")
    if not isinstance(version, str) or not re.fullmatch(r"(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)", version):
        raise ValueError("Invalid package version")
    paths = manifest.get("files")
    if not isinstance(paths, list) or not paths or any(not isinstance(p, str) for p in paths):
        raise ValueError("Invalid package allowlist")
    if len(paths) != len({p.casefold() for p in paths}):
        raise ValueError("Duplicate or case-colliding package path")
    if not {"SKILL.md", "LICENSE", "MANIFEST.json"}.issubset(paths):
        raise ValueError("Required package files missing from allowlist")
    files = {p: safe_file(root, p) for p in paths}
    return manifest, files


def digest(data):
    return hashlib.sha256(data).hexdigest()


def install(destination, apply=False, root=ROOT):
    """Explicit-destination, no-overwrite installation; dry-run unless requested."""
    manifest, files = package_files(root)
    raw = Path(destination).expanduser().absolute()
    if raw.name != NAME:
        raise ValueError("Destination directory must be named " + NAME)
    # Resolve OS-managed parent aliases (e.g. macOS temporary directories), but
    # never follow an existing destination symlink. Dry-run shows the real target.
    if raw.is_symlink():
        raise ValueError("Destination must not be a symlink")
    target = raw.resolve()
    source_root = Path(root).resolve()
    if target.is_relative_to(source_root) or source_root.is_relative_to(target):
        raise ValueError("Source and destination must be disjoint")
    payloads = {relative: path.read_bytes() for relative, path in files.items()}
    result = {"status": "dry_run", "destination": str(target), "files": len(files),
              "version": manifest["version"]}
    if target.exists():
        for path in target.rglob("*"):
            relative = path.relative_to(target)
            if path.is_symlink():
                raise ValueError("Existing installation contains a symlink; refusing to modify it")
            is_bytecode = "__pycache__" in relative.parts and path.suffix in {".pyc", ".pyo"}
            if path.is_file() and not is_bytecode and relative.as_posix() not in payloads:
                raise ValueError("Existing installation has additional files; review before upgrading")
        for relative, payload in payloads.items():
            try:
                existing = safe_file(target, relative)
            except ValueError:
                raise ValueError("Existing installation differs; review and back it up before upgrading") from None
            if digest(existing.read_bytes()) != digest(payload):
                raise ValueError("Existing installation differs; refusing to overwrite " + relative)
        result["status"] = "unchanged"
        return result
    if not apply:
        return result
    target.parent.mkdir(parents=True, exist_ok=True)
    target.mkdir(exist_ok=False)
    try:
        for relative, payload in payloads.items():
            output = target / relative
            output.parent.mkdir(parents=True, exist_ok=True)
            with output.open("xb") as handle:
                handle.write(payload)
            if digest(output.read_bytes()) != digest(payload):
                raise OSError("Installed file verification failed")
    except BaseException:
        # This destination did not exist and was exclusively created by this call.
        shutil.rmtree(target)
        raise
    result["status"] = "installed"
    return result


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    diag = commands.add_parser("doctor", help="Noninteractive prerequisite probes only")
    diag.add_argument("--stage", choices=("local", "publish"), default="local")
    diag.add_argument("--profile", choices=PROFILES, default="cloudflare",
                      help="Cloudflare baseline (default), or explicitly selected container runtime")
    config = commands.add_parser("mcp-config", help="Print a secret-free fragment; never apply it")
    config.add_argument("--client", choices=CLIENTS, required=True)
    config.add_argument("--providers", nargs="+", choices=PROVIDER_NAMES,
                        help="Selected connections only; defaults to Cloudflare")
    config.add_argument("--railway-transport", choices=("http", "stdio"), default="http")
    copy = commands.add_parser("install", help="Copy allowlisted skill files only with --apply")
    copy.add_argument("--destination", required=True)
    copy.add_argument("--apply", action="store_true")
    args = parser.parse_args(argv)
    try:
        if args.command == "mcp-config":
            print(render_config(args.client, args.providers, args.railway_transport), end="")
            return 0
        if args.command == "doctor":
            report = doctor(args.stage, profile=args.profile)
            print(json.dumps(report, indent=2))
            return 0 if report["ready"] else 1
        print(json.dumps(install(args.destination, args.apply), indent=2))
        return 0
    except (ValueError, OSError) as error:
        print("Error: " + str(error), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
