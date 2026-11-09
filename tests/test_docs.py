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


class IdeationAndStackTests(unittest.TestCase):
    def test_postgres_rehearsal_preserves_the_selected_data_platform(self):
        text = (ROOT / "references/publishing.md").read_text(encoding="utf-8")
        migrations = text.split("## Migrations and release gates", 1)[1].split("## Verify staging", 1)[0]
        self.assertIn("selected data platform", migrations)
        self.assertIn("only when Neon is selected", migrations)

    def test_cloudflare_private_state_is_excluded_from_git_and_build_context(self):
        for name in ("app.gitignore", "app.containerignore"):
            text = (ROOT / "templates" / name).read_text(encoding="utf-8")
            with self.subTest(name=name):
                for private_path in (".dev.vars", ".dev.vars.*", ".wrangler"):
                    self.assertIn(private_path, text)

    def test_ideation_is_loaded_before_connection_setup(self):
        text = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        self.assertLess(text.index("references/ideation.md"), text.index("references/onboarding.md"))
        self.assertIn("On every invocation", text)
        self.assertIn("before implementation or provider setup", text)

    def test_minimum_and_escalation_guides_are_distributed(self):
        manifest = json.loads((ROOT / "MANIFEST.json").read_text(encoding="utf-8"))
        for path in ("references/ideation.md", "references/stack-selection.md", "references/ai-feasibility.md"):
            self.assertIn(path, manifest["files"])
            self.assertTrue((ROOT / path).is_file())
            self.assertIn(path, (ROOT / "SKILL.md").read_text(encoding="utf-8"))

    def test_llm_review_requires_economics_and_capability_checks(self):
        text = (ROOT / "references/ai-feasibility.md").read_text(encoding="utf-8")
        for contract in ("100,000-word", "input", "output", "retries", "revisions",
                         "concurrency", "per-user", "monthly", "context window",
                         "maximum output", "source", "checked", "unverified"):
            with self.subTest(contract=contract):
                self.assertIn(contract, text)

    def test_general_feasibility_covers_non_ai_development_risks(self):
        text = (ROOT / "references/ideation.md").read_text(encoding="utf-8")
        for contract in ("Technical feasibility", "Scalability", "Security and privacy",
                         "Complexity", "Integrations", "Correctness and reliability",
                         "Development and delivery", "Operations", "Usability and accessibility"):
            with self.subTest(contract=contract):
                self.assertIn(contract, text)
        self.assertLess(text.index("## Explain the consequence now"), text.index("## Ready to build"))

    def test_ai_is_one_conditional_branch_of_the_general_review(self):
        text = (ROOT / "references/ideation.md").read_text(encoding="utf-8")
        self.assertIn("[AI feasibility](ai-feasibility.md)", text)
        self.assertIn("not an exhaustive checklist", text)
        self.assertNotIn("model_cost_per_job", text)
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("every meaningful feature", skill)
        self.assertIn("complexity", skill)

    def test_feasibility_records_unknown_risks_without_implying_acceptance(self):
        record = json.loads((ROOT / "templates/onboarding-state.json").read_text(encoding="utf-8"))
        review = record["ideation"]["feasibility"]
        self.assertEqual(review["status"], "pending")
        self.assertIsNone(review["decision"])
        self.assertEqual(review["risks"], [])
        self.assertEqual(review["dependencies"], [])
        self.assertEqual(review["complexity_drivers"], [])
        self.assertIsNone(review["next_experiment"])

    def test_non_ai_scenarios_cover_delivery_and_data_failure_modes(self):
        text = (ROOT / "tests/scenarios.md").read_text(encoding="utf-8")
        for case in ("Offline inventory sync", "Last-seat booking", "Unavailable third-party API",
                     "Large public uploads", "Solo weekend build"):
            with self.subTest(case=case):
                self.assertIn(case, text)

    def test_onboarding_records_workload_and_stack_instead_of_assuming_five_providers(self):
        record = json.loads((ROOT / "templates/onboarding-state.json").read_text(encoding="utf-8"))
        self.assertEqual(record["stage"], "ideation")
        self.assertEqual(record["ideation"]["status"], "pending")
        self.assertIsNone(record["stack"]["selected_profile"])
        self.assertEqual(record["stack"]["recommended_profile"], "cloudflare")
        self.assertEqual(record["stack"]["required_providers"], [])
        self.assertIsNone(record["ideation"]["cost_estimate"])
        for provider in record["providers"].values():
            self.assertFalse(provider["configured"])
            self.assertFalse(provider["authorized"])


if __name__ == "__main__":
    unittest.main()
