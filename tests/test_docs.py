"""Regression checks for the public package's documented setup contracts."""
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class DocumentationTests(unittest.TestCase):
    def test_cursor_policy_precedes_discovery_and_calls(self):
        text = (ROOT / "references/mcp-clients.md").read_text(encoding="utf-8")
        cursor = text.split("## Cursor\n", 1)[1].split("## Hermes\n", 1)[0]
        self.assertIn("Before connecting", cursor)
        self.assertIn("verify the effective approval policy", cursor)
        self.assertIn("disable blanket automatic execution", cursor)
        self.assertLess(cursor.index("verify the effective approval policy"),
                        cursor.index("then discover tools"))
        self.assertLess(cursor.index("then discover tools"), cursor.index("perform a safe read"))

    def test_ci_covers_arbitrary_branch_and_manual_dispatch(self):
        text = (ROOT / ".github/workflows/ci.yml").read_text(encoding="utf-8")
        triggers = text.split("on:\n", 1)[1].split("permissions:\n", 1)[0]
        self.assertIn("  pull_request:\n", triggers)
        self.assertIn("  push:\n", triggers)
        self.assertIn("  workflow_dispatch:\n", triggers)
        self.assertNotIn("branches:", triggers)
        self.assertNotIn("branches-ignore:", triggers)
        self.assertIn("contents: read", text)
        self.assertIn("persist-credentials: false", text)
        self.assertNotIn("pull_request_target", triggers)

    def test_public_identity_is_consistent(self):
        manifest = json.loads((ROOT / "MANIFEST.json").read_text(encoding="utf-8"))
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertEqual(manifest["name"], "build-my-app")
        self.assertIn("name: build-my-app\n", skill)
        self.assertTrue(readme.startswith("# Build My App\n"))
        self.assertIn("Use build-my-app", readme)
        self.assertIn("skills/build-my-app", readme)
        self.assertIn('  version: "' + manifest["version"] + '"', skill)


if __name__ == "__main__":
    unittest.main()
