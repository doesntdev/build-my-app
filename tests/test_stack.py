"""Deterministic tests: no provider credentials, network calls, or live config edits."""
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import tomllib
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import stack


class ConfigTests(unittest.TestCase):
    def test_all_clients_and_transports_parse(self):
        for client in stack.CLIENTS:
            for transport in ("http", "stdio"):
                with self.subTest(client=client, transport=transport):
                    text = stack.render_config(client, stack.PROVIDER_NAMES, railway_transport=transport)
                    value = tomllib.loads(text) if client == "codex" else json.loads(text)
                    key = "mcp_servers" if client in ("codex", "hermes") else "mcpServers"
                    servers = value[key]
                    self.assertEqual(set(servers), set(stack.PROVIDER_NAMES))
                    if transport == "stdio":
                        self.assertEqual(servers["railway"]["command"], "railway")
                        self.assertEqual(servers["railway"]["args"], ["mcp"])
                        self.assertNotIn("url", servers["railway"])
                    else:
                        self.assertEqual(servers["railway"]["url"], "https://mcp.railway.com")

    def test_exact_provider_urls(self):
        result = json.loads(stack.render_config("claude-code", stack.PROVIDER_NAMES))["mcpServers"]
        expected = {
            "github": "https://api.githubcopilot.com/mcp/",
            "neon": "https://mcp.neon.tech/mcp",
            "railway": "https://mcp.railway.com",
            "cloudflare": "https://mcp.cloudflare.com/mcp",
            "resend": "https://mcp.resend.com/mcp",
        }
        self.assertEqual({k: v["url"] for k, v in result.items()}, expected)

    def test_all_selections_are_restricted(self):
        for provider in stack.PROVIDER_NAMES:
            value = json.loads(stack.render_config("cursor", [provider]))
            self.assertEqual(list(value["mcpServers"]), [provider])

    def test_claude_explicit_transport(self):
        value = json.loads(stack.render_config("claude-code", stack.PROVIDER_NAMES))["mcpServers"]
        self.assertTrue(all(s["type"] == "http" for s in value.values()))

    def test_client_specific_secret_references(self):
        claude = json.loads(stack.render_config("claude-code", ["github"]))["mcpServers"]["github"]
        cursor = json.loads(stack.render_config("cursor", ["github"]))["mcpServers"]["github"]
        codex = tomllib.loads(stack.render_config("codex", ["github"]))["mcp_servers"]["github"]
        self.assertEqual(claude["headers"]["Authorization"], "Bearer ${GITHUB_MCP_TOKEN}")
        self.assertEqual(cursor["headers"]["Authorization"], "Bearer ${env:GITHUB_MCP_TOKEN}")
        self.assertEqual(codex["bearer_token_env_var"], "GITHUB_MCP_TOKEN")

    def test_never_interpolates_environment(self):
        with patch.dict(os.environ, {"GITHUB_MCP_TOKEN": "private-test-sentinel-do-not-render"}):
            for client in stack.CLIENTS:
                self.assertNotIn("private-test-sentinel", stack.render_config(client, stack.PROVIDER_NAMES))

    def test_github_readonly_in_every_client(self):
        for client in stack.CLIENTS:
            text = stack.render_config(client, stack.PROVIDER_NAMES)
            value = tomllib.loads(text) if client == "codex" else json.loads(text)
            key = "mcp_servers" if client in ("codex", "hermes") else "mcpServers"
            header_key = "http_headers" if client == "codex" else "headers"
            self.assertEqual(value[key]["github"][header_key]["X-MCP-Readonly"], "true")

    def test_codex_approval_prompts(self):
        value = tomllib.loads(stack.render_config("codex", stack.PROVIDER_NAMES))["mcp_servers"]
        self.assertTrue(all(v["default_tools_approval_mode"] == "prompt" for v in value.values()))

    def test_codex_cli_documentation_gates_discovery_on_policy(self):
        text = (ROOT / "references/mcp-clients.md").read_text(encoding="utf-8")
        codex = text.split("## Codex\n", 1)[1].split("## Claude Code\n", 1)[0]
        self.assertIn("### CLI safety checkpoint", codex)
        checkpoint = codex.split("### CLI safety checkpoint", 1)[1]
        for required in ("merge", "X-MCP-Readonly", 'default_tools_approval_mode = "prompt"',
                         "read back", "before tool discovery"):
            self.assertIn(required, checkpoint)
        self.assertLess(codex.index("### CLI safety checkpoint"), codex.index("Use `/mcp`"))

    def test_documented_github_fragment_command_contains_complete_policy(self):
        result = subprocess.run([sys.executable, str(ROOT / "scripts/stack.py"),
                                 "mcp-config", "--client", "codex", "--providers", "github"],
                                capture_output=True, text=True, check=True)
        servers = tomllib.loads(result.stdout)["mcp_servers"]
        self.assertEqual(list(servers), ["github"])
        github = servers["github"]
        self.assertEqual(github["http_headers"]["X-MCP-Readonly"], "true")
        self.assertEqual(github["default_tools_approval_mode"], "prompt")
        self.assertEqual(github["bearer_token_env_var"], "GITHUB_MCP_TOKEN")

    def test_hermes_trust_and_sampling(self):
        value = json.loads(stack.render_config("hermes", stack.PROVIDER_NAMES))["mcp_servers"]
        for name, server in value.items():
            self.assertEqual(server["trust"], "untrusted")
            self.assertFalse(server["sampling"]["enabled"])
            if name != "github":
                self.assertEqual(server["auth"], "oauth")

    def test_reject_invalid_client_provider_and_transport(self):
        for args, kwargs in [(("unknown",), {}), (("codex", ["unknown"]), {}),
                             (("codex", []), {}), (("codex", ["github", "github"]), {}),
                             (("codex",), {"railway_transport": "sse"})]:
            with self.subTest(args=args, kwargs=kwargs), self.assertRaises(ValueError):
                stack.render_config(*args, **kwargs)


    def test_default_config_selects_only_cloudflare_for_every_client(self):
        for client in stack.CLIENTS:
            with self.subTest(client=client):
                text = stack.render_config(client)
                value = tomllib.loads(text) if client == "codex" else json.loads(text)
                key = "mcp_servers" if client in ("codex", "hermes") else "mcpServers"
                self.assertEqual(list(value[key]), ["cloudflare"])
                self.assertNotIn("GITHUB_MCP_TOKEN", text)

    def test_cli_default_config_selects_only_cloudflare(self):
        result = subprocess.run([sys.executable, str(ROOT / "scripts/stack.py"),
                                 "mcp-config", "--client", "hermes"],
                                capture_output=True, text=True, check=True)
        self.assertEqual(list(json.loads(result.stdout)["mcp_servers"]), ["cloudflare"])


class DoctorTests(unittest.TestCase):
    @staticmethod
    def healthy(command, timeout=10):
        if command[1:2] == ["info"]:
            return "ok", json.dumps({"host": {"security": {"rootless": True}}})
        return "ok", "tool version 5.44.0"

    def test_local_ready_without_cloud_clis(self):
        def run(command, timeout=10):
            if command[0] in ("gh", "railway", "podman-compose"):
                return "missing", ""
            return self.healthy(command, timeout)
        report = stack.doctor("local", runner=run, system="Linux", profile="container")
        self.assertTrue(report["ready"])
        self.assertEqual(report["provider_authentication"], "not_tested")
        self.assertEqual(report["application_health"], "not_tested")

    def test_missing_required_fails(self):
        report = stack.doctor("local", runner=lambda *a, **k: ("missing", ""), system="Linux")
        self.assertFalse(report["ready"])

    def test_publish_does_not_require_optional_cli_when_mcp_can_be_used(self):
        def run(command, timeout=10):
            return ("missing", "") if command[0] == "gh" else self.healthy(command, timeout)
        self.assertTrue(stack.doctor("publish", runner=run, system="Linux")["ready"])

    def test_rootful_linux_not_approved(self):
        def run(command, timeout=10):
            if command[1:2] == ["info"]:
                return "ok", '{"host":{"security":{"rootless":false}}}'
            return self.healthy(command, timeout)
        self.assertFalse(stack.doctor("local", runner=run, system="Linux", profile="container")["ready"])

    def test_bad_podman_json_fails_safely(self):
        def run(command, timeout=10):
            return "ok", "not-json secret-sentinel"
        report = stack.doctor("local", runner=run, system="Linux", profile="container")
        self.assertFalse(report["ready"])
        self.assertNotIn("secret-sentinel", json.dumps(report))

    def test_wrong_podman_json_type_fails_safely(self):
        for value in ("[]", "null", '{"host":null}', '{"host":{"security":[]}}'):
            with self.subTest(value=value):
                report = stack.doctor("local", runner=lambda *a, **k: ("ok", value), system="Linux", profile="container")
                self.assertFalse(report["ready"])

    def test_failed_probe_does_not_leak_output(self):
        report = stack.doctor("local", runner=lambda *a, **k: ("failed", "secret-sentinel"), system="Linux")
        self.assertNotIn("secret-sentinel", json.dumps(report))

    def test_vm_stopped_is_not_ready(self):
        def run(command, timeout=10):
            return ("failed", "") if command[1:2] == ["info"] else self.healthy(command, timeout)
        for system in ("Windows", "Darwin"):
            report = stack.doctor("local", runner=run, system=system, profile="container")
            self.assertFalse(report["ready"])
            self.assertIn("machine", report["next_action"])

    def test_timeout_is_reported(self):
        report = stack.doctor("local", runner=lambda *a, **k: ("timeout", ""), system="Linux")
        self.assertFalse(report["ready"])
        self.assertEqual(report["checks"][0]["status"], "timeout")

    def test_no_mutating_probe(self):
        calls = []
        def run(command, timeout=10):
            calls.append(command)
            return self.healthy(command, timeout)
        for profile in ("cloudflare", "container"):
            stack.doctor("publish", runner=run, system="Linux", profile=profile)
        allowed = [[c, "--version"] for c in ("git", "node", "wrangler", "podman", "gh", "railway", "podman-compose")]
        allowed.append(["podman", "info", "--format", "json"])
        self.assertTrue(all(c in allowed for c in calls))

    def test_probe_never_uses_shell(self):
        fake = subprocess.CompletedProcess(["git", "--version"], 0, stdout="git 2.0", stderr="")
        with patch("stack.shutil.which", return_value="/safe/git"), patch("stack.subprocess.run", return_value=fake) as call:
            self.assertEqual(stack.probe(["git", "--version"])[0], "ok")
            self.assertFalse(call.call_args.kwargs["shell"])
            self.assertGreater(call.call_args.kwargs["timeout"], 0)

    def test_cloudflare_default_never_probes_container_or_optional_vendor_tools(self):
        calls = []
        def run(command, timeout=10):
            calls.append(command)
            if command[0] in ("git", "node"):
                return "ok", "tool version 24.0.0"
            return "missing", ""
        report = stack.doctor(runner=run, system="Linux")
        self.assertTrue(report["ready"])
        self.assertEqual(report["profile"], "cloudflare")
        self.assertEqual({c["check"] for c in report["checks"] if c["required"]}, {"git", "node"})
        self.assertFalse(any(c[0] in ("podman", "podman-compose", "railway") for c in calls))
        self.assertIn("project-local Wrangler", report["next_action"])

    def test_cloudflare_needs_node_but_not_podman_on_all_platforms(self):
        for system in ("Linux", "Darwin", "Windows"):
            def run(command, timeout=10):
                return ("missing", "") if command[0] == "node" else self.healthy(command, timeout)
            with self.subTest(system=system):
                report = stack.doctor(runner=run, system=system)
                self.assertFalse(report["ready"])
                self.assertNotIn("podman", report["next_action"].lower())

    def test_node_v_prefix_preserves_the_full_version(self):
        def run(command, timeout=10):
            return ("ok", "v24.15.0\n") if command[0] == "node" else self.healthy(command, timeout)
        report = stack.doctor(runner=run, system="Linux")
        node = next(c for c in report["checks"] if c["check"] == "node")
        self.assertEqual(node["version"], "24.15.0")

    def test_invalid_doctor_profile_or_stage_rejected(self):
        with self.assertRaises(ValueError):
            stack.doctor(profile="unknown")
        with self.assertRaises(ValueError):
            stack.doctor(stage="unknown")

    def test_doctor_cli_accepts_explicit_profiles(self):
        for profile in ("cloudflare", "container"):
            with self.subTest(profile=profile), patch("stack.doctor", return_value={"ready": True}) as check:
                with patch("builtins.print"):
                    self.assertEqual(stack.main(["doctor", "--profile", profile]), 0)
                check.assert_called_once_with("local", profile=profile)


class PackageTests(unittest.TestCase):
    def test_manifest_files_exist(self):
        manifest, files = stack.package_files(ROOT)
        self.assertEqual(manifest["name"], "build-my-app")
        self.assertIn("SKILL.md", files)
        self.assertIn("MANIFEST.json", files)

    def test_install_dry_run_then_apply_then_idempotent(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "build-my-app"
            self.assertEqual(stack.install(target, apply=False)["status"], "dry_run")
            self.assertFalse(target.exists())
            first = stack.install(target, apply=True)
            self.assertEqual(first["status"], "installed")
            self.assertEqual(stack.install(target, apply=True)["status"], "unchanged")
            _, files = stack.package_files(ROOT)
            for relative, source in files.items():
                self.assertEqual((target / relative).read_bytes(), source.read_bytes())

    def test_existing_modified_install_refused(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "build-my-app"
            stack.install(target, apply=True)
            (target / "SKILL.md").write_text("custom instructions", encoding="utf-8")
            with self.assertRaises(ValueError):
                stack.install(target, apply=True)
            self.assertEqual((target / "SKILL.md").read_text(encoding="utf-8"), "custom instructions")

    def test_install_into_source_refused(self):
        with self.assertRaises(ValueError):
            stack.install(ROOT / "build-my-app", apply=False)

    def test_wrong_destination_name_refused(self):
        with tempfile.TemporaryDirectory() as tmp, self.assertRaises(ValueError):
            stack.install(Path(tmp) / "wrong-name", apply=False)

    def test_manifest_path_traversal_rejected(self):
        for bad in ("../outside", "/absolute", "x/../../outside", "x\\outside", "C:/outside", "./SKILL.md", ""):
            with self.subTest(bad=bad), tempfile.TemporaryDirectory() as tmp:
                r = Path(tmp)
                manifest = {"name": "build-my-app", "version": "0.1.0", "files": [bad]}
                (r / "MANIFEST.json").write_text(json.dumps(manifest), encoding="utf-8")
                with self.assertRaises(ValueError):
                    stack.package_files(r)

    def test_duplicate_manifest_entries_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            r = Path(tmp)
            manifest = {"name": "build-my-app", "version": "0.1.0", "files": ["SKILL.md", "SKILL.md"]}
            (r / "MANIFEST.json").write_text(json.dumps(manifest), encoding="utf-8")
            with self.assertRaises(ValueError):
                stack.package_files(r)

    def test_symlink_source_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            r = Path(tmp)
            (r / "real").write_text("outside fixture", encoding="utf-8")
            try:
                (r / "SKILL.md").symlink_to(r / "real")
            except (OSError, NotImplementedError):
                self.skipTest("Symlink creation unavailable on this host")
            (r / "LICENSE").write_text("license", encoding="utf-8")
            (r / "MANIFEST.json").write_text(json.dumps({"name": "build-my-app", "version": "0.1.0", "files": ["SKILL.md", "LICENSE", "MANIFEST.json"]}), encoding="utf-8")
            with self.assertRaises(ValueError):
                stack.package_files(r)

    def test_parent_alias_resolves_without_overwriting(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            real = base / "real"
            real.mkdir()
            alias = base / "alias"
            try:
                alias.symlink_to(real, target_is_directory=True)
            except (OSError, NotImplementedError):
                self.skipTest("Symlink creation unavailable on this host")
            result = stack.install(alias / stack.NAME, apply=True)
            self.assertEqual(result["destination"], str((real / stack.NAME).resolve()))
            self.assertTrue((real / stack.NAME / "SKILL.md").is_file())

    def test_destination_symlink_refused(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            real = base / "real"
            real.mkdir()
            target = base / stack.NAME
            try:
                target.symlink_to(real, target_is_directory=True)
            except (OSError, NotImplementedError):
                self.skipTest("Symlink creation unavailable on this host")
            with self.assertRaises(ValueError):
                stack.install(target, apply=True)
            self.assertEqual(list(real.iterdir()), [])

    def test_failed_install_removes_only_new_target(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            target = base / stack.NAME
            unrelated = base / "keep"
            unrelated.write_text("keep", encoding="utf-8")
            with patch("stack.digest", side_effect=["different", "hash"]), self.assertRaises(OSError):
                stack.install(target, apply=True)
            self.assertFalse(target.exists())
            self.assertEqual(unrelated.read_text(encoding="utf-8"), "keep")

    def test_extra_destination_file_refused(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / stack.NAME
            stack.install(target, apply=True)
            (target / "extra-instructions.md").write_text("local customization\n", encoding="utf-8")
            with self.assertRaises(ValueError):
                stack.install(target, apply=True)
            self.assertTrue((target / "extra-instructions.md").is_file())

    def test_cache_files_do_not_block_idempotent_install(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / stack.NAME
            stack.install(target, apply=True)
            cache = target / "scripts" / "__pycache__"
            cache.mkdir()
            (cache / "stack.cpython-test.pyc").write_bytes(b"disposable-bytecode")
            self.assertEqual(stack.install(target, apply=True)["status"], "unchanged")

    def test_private_or_generated_allowlist_rejected(self):
        for bad in (".env", ".env.production", ".dev.vars", ".dev.vars.production", ".wrangler/state/db.sqlite", ".git/config", "__pycache__/x.pyc",
                    ".build-my-app/onboarding.json", "key.pem", "settings.bak", "dist/release.zip"):
            with self.subTest(bad=bad), tempfile.TemporaryDirectory() as tmp:
                r = Path(tmp) / stack.NAME
                stack.install(r, apply=True)
                p = r / "MANIFEST.json"
                manifest = json.loads(p.read_text(encoding="utf-8"))
                target = r / bad
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text("safe audit fixture\n", encoding="utf-8")
                manifest["files"].append(bad)
                p.write_text(json.dumps(manifest) + "\n", encoding="utf-8")
                with self.assertRaises(ValueError):
                    stack.package_files(r)

    def test_windows_path_aliases_and_case_collisions_rejected(self):
        for bad in ("CON", "aux.txt", "README.md.", "README.md ", "file?.md", "readme.md"):
            with self.subTest(bad=bad), tempfile.TemporaryDirectory() as tmp:
                r = Path(tmp) / stack.NAME
                stack.install(r, apply=True)
                p = r / "MANIFEST.json"
                manifest = json.loads(p.read_text(encoding="utf-8"))
                # Inspect path policy without creating OS-specific reserved files.
                manifest["files"].append(bad)
                p.write_text(json.dumps(manifest) + "\n", encoding="utf-8")
                with self.assertRaises(ValueError):
                    stack.package_files(r)

    def test_invalid_manifest_version_rejected(self):
        for bad in (None, 1, "not-semver"):
            with self.subTest(bad=bad), tempfile.TemporaryDirectory() as tmp:
                r = Path(tmp) / stack.NAME
                stack.install(r, apply=True)
                p = r / "MANIFEST.json"
                manifest = json.loads(p.read_text(encoding="utf-8"))
                manifest["version"] = bad
                p.write_text(json.dumps(manifest) + "\n", encoding="utf-8")
                with self.assertRaises(ValueError):
                    stack.package_files(r)

    def test_cli_config_roundtrip(self):
        result = subprocess.run([sys.executable, str(ROOT / "scripts/stack.py"), "mcp-config", "--client", "codex", "--providers", "neon"], capture_output=True, text=True, check=True)
        self.assertEqual(list(tomllib.loads(result.stdout)["mcp_servers"]), ["neon"])

    def test_cli_invalid_provider_nonzero(self):
        result = subprocess.run([sys.executable, str(ROOT / "scripts/stack.py"), "mcp-config", "--client", "cursor", "--providers", "evil"], capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(result.stdout, "")


if __name__ == "__main__":
    unittest.main()
