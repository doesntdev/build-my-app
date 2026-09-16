import json
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import stack
import verify


class ValidationTests(unittest.TestCase):
    def temporary_package(self, tmp):
        target = Path(tmp) / stack.NAME
        stack.install(target, apply=True)
        return target

    def test_real_package_valid(self):
        self.assertEqual(verify.validate(ROOT), [])

    def test_added_private_file_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = self.temporary_package(tmp)
            (target / ".env").write_text("EXAMPLE=local-fixture", encoding="utf-8")
            self.assertTrue(any("not allowlisted" in e for e in verify.validate(target)))

    def test_personal_path_fails_without_echoing_it(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = self.temporary_package(tmp)
            file = target / "README.md"
            with file.open("a", encoding="utf-8") as handle:
                handle.write("personal path: " + "/home/" + "private-fixture" + "\n")
            errors = verify.validate(target)
            self.assertTrue(any("privacy indicator" in e for e in errors))
            self.assertNotIn("private-fixture", json.dumps(errors))

    def test_token_indicator_fails_without_echoing_it(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = self.temporary_package(tmp)
            file = target / "README.md"
            with file.open("a", encoding="utf-8") as handle:
                handle.write("ghp_" + "x" * 30 + "\n")
            errors = verify.validate(target)
            self.assertTrue(any("github-token" in e for e in errors))
            self.assertNotIn("x" * 30, json.dumps(errors))

    def test_broken_reference_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = self.temporary_package(tmp)
            with (target / "README.md").open("a", encoding="utf-8") as handle:
                handle.write("[broken](references/does-not-exist.md)\n")
            self.assertTrue(any("broken/escaping" in e for e in verify.validate(target)))

    def test_version_drift_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = self.temporary_package(tmp)
            path = target / "MANIFEST.json"
            value = json.loads(path.read_text(encoding="utf-8"))
            value["version"] = "9.9.9"
            path.write_text(json.dumps(value) + "\n", encoding="utf-8")
            self.assertIn("Skill and manifest versions differ", verify.validate(target))

    def test_parse_error_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = self.temporary_package(tmp)
            (target / "scripts/stack.py").write_text("def invalid(:\n", encoding="utf-8")
            self.assertIn("scripts/stack.py: invalid Python", verify.validate(target))

    def test_escaping_reference_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = self.temporary_package(tmp)
            with (target / "README.md").open("a", encoding="utf-8") as handle:
                handle.write("[escape](../outside.md)\n")
            self.assertTrue(any("broken/escaping" in e for e in verify.validate(target)))

    def test_malformed_or_duplicate_frontmatter_rejected(self):
        mutations = (
            ("license: MIT", "license: MIT\nmetadata: [invalid"),
            ("license: MIT", "license: MIT\nlicense: MIT"),
            ("license: MIT", "license: MIT\nunknown-key: ignored"),
            ("license: MIT", "license: MIT\ncompatibility: " + "x" * 501),
        )
        for old, new in mutations:
            with self.subTest(new=new), tempfile.TemporaryDirectory() as tmp:
                target = self.temporary_package(tmp)
                path = target / "SKILL.md"
                path.write_text(path.read_text(encoding="utf-8").replace(old, new), encoding="utf-8")
                self.assertTrue(verify.validate(target))

    def test_directory_name_must_match_skill(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = self.temporary_package(tmp)
            other = Path(tmp) / "different-directory"
            target.rename(other)
            self.assertTrue(verify.validate(other))

    def test_non_utf8_skill_is_reported_without_exception(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = self.temporary_package(tmp)
            (target / "SKILL.md").write_bytes(b"\xff")
            self.assertTrue(verify.validate(target))

    def test_malformed_provider_registry_is_reported(self):
        for data in ({"providers": []}, [], {"providers": {"github": None}}):
            with self.subTest(data=data), tempfile.TemporaryDirectory() as tmp:
                target = self.temporary_package(tmp)
                (target / "references/providers.json").write_text(json.dumps(data) + "\n", encoding="utf-8")
                self.assertTrue(verify.validate(target))

    def test_https_unofficial_provider_endpoint_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = self.temporary_package(tmp)
            path = target / "references/providers.json"
            value = json.loads(path.read_text(encoding="utf-8"))
            value["providers"]["github"]["url"] = "https://example.com/mcp"
            path.write_text(json.dumps(value) + "\n", encoding="utf-8")
            self.assertTrue(verify.validate(target))

    def test_missing_manifest_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.assertTrue(verify.validate(Path(tmp)))


if __name__ == "__main__":
    unittest.main()
