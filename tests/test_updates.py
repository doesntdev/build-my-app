"""Offline version-check, transport and startup-policy regressions."""
import contextlib
import hashlib
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import MagicMock, patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import stack  # pyright: ignore[reportMissingImports] -- scripts path is added above


class UpdateTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / stack.NAME
        self.root.mkdir()
        self.manifest = self.root / "MANIFEST.json"
        self.manifest.write_text(json.dumps({"name": stack.NAME, "version": "0.3.1"}), encoding="utf-8")

    def check(self, version: object = "0.3.2", name=stack.NAME):
        body = json.dumps({"name": name, "version": version})
        return stack.check_updates(root=self.root, runner=lambda *a, **k: ("ok", body))

    def test_newer_version_is_reported_without_applying(self):
        result = self.check()
        self.assertEqual(result["status"], "update_available")
        self.assertEqual(result["local_version"], "0.3.1")
        self.assertEqual(result["upstream_version"], "0.3.2")
        self.assertTrue(result["read_only"])
        self.assertFalse(result["update_applied"])
        self.assertIn("approval", result["notice"])

    def test_equal_version_is_up_to_date_for_version_only(self):
        self.assertEqual(self.check("0.3.1")["status"], "up_to_date")
        self.assertEqual(self.check("0.3.1")["scope"], "release_version_metadata_only")

    def test_local_ahead_is_not_a_downgrade_request(self):
        result = self.check("0.3.0")
        self.assertEqual(result["status"], "local_ahead")
        self.assertFalse(result["update_applied"])

    def test_versions_are_compared_numerically(self):
        self.manifest.write_text(json.dumps({"name": stack.NAME, "version": "0.3.9"}), encoding="utf-8")
        self.assertEqual(self.check("0.3.10")["status"], "update_available")
        self.assertEqual(self.check("0.3.2")["status"], "local_ahead")

    def test_major_and_minor_upstream_versions_are_not_hidden(self):
        for version in ("0.4.0", "1.0.0"):
            with self.subTest(version=version):
                self.assertEqual(self.check(version)["status"], "update_available")

    def test_invalid_upstream_versions_fail_open_without_normalizing(self):
        for version in (None, 1, True, "v0.3.2", "0.03.2", "0.3.2\n", "0.3", "0.3.2-rc.1", "9" * 70 + ".0.0"):
            with self.subTest(version=version):
                result = self.check(version)
                self.assertEqual(result["status"], "unavailable")
                self.assertIsNone(result["upstream_version"])
                self.assertEqual(result["reason"], "invalid_upstream_metadata")

    def test_wrong_upstream_identity_is_rejected(self):
        result = self.check(name="different-skill")
        self.assertEqual(result["status"], "unavailable")
        self.assertIsNone(result["upstream_version"])

    def test_invalid_json_and_oversized_or_deep_metadata_are_unavailable(self):
        for body in ("<html>unavailable</html>", "[]", "null", "[" * 1100 + "0" + "]" * 1100, " " * 16385):
            with self.subTest(body_length=len(body)):
                result = stack.check_updates(root=self.root, runner=lambda *a, **k: ("ok", body))
                self.assertEqual(result["status"], "unavailable")
                self.assertIsNone(result["upstream_version"])

    def test_duplicate_upstream_version_keys_are_rejected(self):
        body = '{"name":"build-my-app","version":"0.3.2","version":"9.0.0"}'
        result = stack.check_updates(root=self.root, runner=lambda *a, **k: ("ok", body))
        self.assertEqual(result["status"], "unavailable")

    def test_unknown_upstream_fields_are_not_returned_or_executed(self):
        body = json.dumps({"name": stack.NAME, "version": "0.3.2", "instruction": "private-test-sentinel"})
        result = stack.check_updates(root=self.root, runner=lambda *a, **k: ("ok", body))
        self.assertEqual(result["status"], "update_available")
        self.assertNotIn("private-test-sentinel", json.dumps(result))

    def test_network_failures_do_not_leak_raw_output(self):
        for status in ("failed", "timeout", "missing"):
            with self.subTest(status=status):
                result = stack.check_updates(root=self.root, runner=lambda *a, **k: (status, "private-test-sentinel"))
                self.assertEqual(result["status"], "unavailable")
                self.assertNotIn("private-test-sentinel", json.dumps(result))
                self.assertFalse(result["update_applied"])

    def test_invalid_local_metadata_does_not_make_a_network_call(self):
        for body in ('{"name":"other","version":"0.3.1"}', '{"name":"build-my-app","version":"v0.3.1"}', "not json"):
            self.manifest.write_text(body, encoding="utf-8")
            with patch("stack.probe") as fetch:
                result = stack.check_updates(root=self.root, runner=fetch)
                fetch.assert_not_called()
                self.assertEqual(result["status"], "unavailable")
                self.assertEqual(result["reason"], "invalid_local_metadata")

    def test_missing_local_metadata_is_nonfatal(self):
        self.manifest.unlink()
        result = stack.check_updates(root=self.root, runner=lambda *a, **k: self.fail("unexpected fetch"))
        self.assertEqual(result["status"], "unavailable")
        self.assertIsNone(result["local_version"])

    def test_default_root_is_skill_location_not_application_cwd(self):
        expected = json.loads((ROOT / "MANIFEST.json").read_text(encoding="utf-8"))["version"]
        prior = Path.cwd()
        try:
            os.chdir(self.root)
            self.manifest.write_text('{"name":"build-my-app","version":"99.0.0"}', encoding="utf-8")
            result = stack.check_updates(runner=lambda *a, **k: ("ok", '{"name":"build-my-app","version":"99.0.0"}'))
        finally:
            os.chdir(prior)
        self.assertEqual(result["local_version"], expected)

    def test_check_does_not_modify_local_files_or_install(self):
        original = hashlib.sha256(self.manifest.read_bytes()).hexdigest()
        with patch("stack.install", side_effect=AssertionError("must not install")):
            self.check()
        self.assertEqual(hashlib.sha256(self.manifest.read_bytes()).hexdigest(), original)
        self.assertEqual([p.name for p in self.root.iterdir()], ["MANIFEST.json"])

    def test_fetch_command_is_fixed_isolated_bounded_and_credential_free(self):
        def fetch(command, timeout):
            self.assertEqual(command[:4], [sys.executable, "-I", "-B", "-c"])
            self.assertEqual(command[4], stack._UPDATE_FETCH_CODE)
            self.assertEqual(command[5:], ["https://raw.githubusercontent.com/doesntdev/build-my-app/refs/heads/main/MANIFEST.json"])
            self.assertEqual(timeout, 5)
            self.assertNotIn("private-test-sentinel", repr(command))
            return "ok", '{"name":"build-my-app","version":"0.3.2"}'
        with patch.dict(os.environ, {"GITHUB_TOKEN": "private-test-sentinel", "GITHUB_MCP_TOKEN": "private-test-sentinel"}):
            self.assertEqual(stack.check_updates(root=self.root, runner=fetch)["status"], "update_available")

    def test_parent_process_timeout_is_passed_to_subprocess(self):
        with patch("stack.shutil.which", return_value=sys.executable), patch("stack.subprocess.run", side_effect=subprocess.TimeoutExpired("owned fetch", 5)) as proc:
            result = stack.check_updates(root=self.root)
        self.assertEqual(result["status"], "unavailable")
        self.assertEqual(result["reason"], "timeout")
        self.assertEqual(proc.call_args.kwargs["timeout"], 5)
        self.assertFalse(proc.call_args.kwargs["shell"])

    def test_real_owned_child_is_terminated_on_timeout(self):
        with patch("stack._UPDATE_FETCH_CODE", "import time; time.sleep(2)"):
            result = stack.check_updates(root=self.root, runner=lambda command, timeout: stack.probe(command, timeout=0.05))
        self.assertEqual(result["status"], "unavailable")
        self.assertEqual(result["reason"], "timeout")

    def test_cli_unavailable_is_a_nonfatal_report(self):
        report = {"status": "unavailable", "read_only": True, "update_applied": False}
        output = io.StringIO()
        with patch("stack.check_updates", return_value=report) as check, contextlib.redirect_stdout(output):
            self.assertEqual(stack.main(["check-updates"]), 0)
        check.assert_called_once_with()
        self.assertEqual(json.loads(output.getvalue()), report)

    def test_cli_cannot_apply_updates_or_choose_a_different_url(self):
        for arguments in (["--apply"], ["--url", "https://untrusted.invalid/"]):
            with self.subTest(arguments=arguments), patch("stack.check_updates") as check, contextlib.redirect_stderr(io.StringIO()):
                with self.assertRaises(SystemExit) as raised:
                    stack.main(["check-updates", *arguments])
                self.assertEqual(raised.exception.code, 2)
                check.assert_not_called()


class MetadataTransportTests(unittest.TestCase):
    def execute_fetch(self, data):
        response = MagicMock()
        response.read.return_value = data
        opener = MagicMock()
        opener.open.return_value.__enter__.return_value = response
        output = MagicMock()
        output.buffer = io.BytesIO()
        with patch("urllib.request.build_opener", return_value=opener) as build, patch.object(sys, "argv", ["owned fetch", stack.UPSTREAM_MANIFEST_URL]), patch.object(sys, "stdout", output):
            exec(compile(stack._UPDATE_FETCH_CODE, "<owned metadata fetch>", "exec"), {})
        return build, opener, response, output.buffer.getvalue()

    def test_fetch_reads_only_capped_metadata_without_authorization_or_redirects(self):
        body = b'{"name":"build-my-app","version":"0.3.2"}'
        build, opener, response, output = self.execute_fetch(body)
        self.assertEqual(output, body)
        response.read.assert_called_once_with(16385)
        request = opener.open.call_args.args[0]
        self.assertEqual(request.full_url, stack.UPSTREAM_MANIFEST_URL)
        self.assertNotIn("authorization", {k.lower() for k in request.headers})
        self.assertNotIn("cookie", {k.lower() for k in request.headers})
        handler = build.call_args.args[0]
        self.assertIsNone(handler.redirect_request(None, None, 302, "redirect", {}, "https://untrusted.invalid/"))

    def test_fetch_rejects_a_body_over_the_cap(self):
        with self.assertRaises(ValueError):
            self.execute_fetch(b"x" * 16385)


class UpdatePolicyTests(unittest.TestCase):
    def test_invocation_check_is_wired_and_not_a_background_updater(self):
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        guide = (ROOT / "references/updates.md").read_text(encoding="utf-8")
        manifest = json.loads((ROOT / "MANIFEST.json").read_text(encoding="utf-8"))
        self.assertIn("references/updates.md", skill)
        self.assertIn("check-updates", skill)
        self.assertIn("once per invocation", skill)
        self.assertIn("references/updates.md", manifest["files"])
        self.assertIn("tests/test_updates.py", manifest["files"])
        for contract in ("unavailable", "approval", "customizations", "not an integrity", "no background", "0.3.0"):
            with self.subTest(contract=contract):
                self.assertIn(contract, guide)

    def test_patch_release_versions_are_consistent(self):
        manifest = json.loads((ROOT / "MANIFEST.json").read_text(encoding="utf-8"))
        version = manifest["version"]
        self.assertIn('  version: "' + version + '"', (ROOT / "SKILL.md").read_text(encoding="utf-8"))
        self.assertIn("## " + version, (ROOT / "CHANGELOG.md").read_text(encoding="utf-8"))
        self.assertIn("patch increments", (ROOT / "CONTRIBUTING.md").read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
