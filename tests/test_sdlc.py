"""Instruction/package contracts, not proof of live tracker or PR enforcement."""
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


def text(path):
    return (ROOT / path).read_text(encoding="utf-8")


class SpecDrivenDeliveryTests(unittest.TestCase):
    def test_spec_hygiene_and_tests_ship_in_the_manifest(self):
        manifest = json.loads(text("MANIFEST.json"))
        for path in ("templates/spec.md", "references/workspace-hygiene.md", "tests/test_sdlc.py"):
            with self.subTest(path=path):
                self.assertIn(path, manifest["files"])
                self.assertTrue((ROOT / path).is_file())

    def test_spec_is_created_during_ideation_not_afterward(self):
        guide = text("references/ideation.md")
        for contract in ("spec.md", "throughout ideation", "REQ-001", "accepted", "tracker"):
            with self.subTest(contract=contract):
                self.assertIn(contract, guide)
        self.assertIn("templates/spec.md", text("SKILL.md"))

    def test_tracker_is_required_and_an_existing_alternative_is_supported(self):
        guide = text("references/sdlc.md")
        for contract in ("GitHub Issues", "another issue tracker", "before implementation",
                         "stable work-item", "spec.md", "spec revision"):
            with self.subTest(contract=contract):
                self.assertIn(contract, guide)
        state = json.loads(text("templates/onboarding-state.json"))
        self.assertNotIn("temporary_intake", state)

    def test_delivery_state_starts_unverified_with_no_invented_reviewer(self):
        state = json.loads(text("templates/onboarding-state.json"))
        self.assertEqual(state["specification"]["path"], "spec.md")
        self.assertEqual(state["specification"]["status"], "draft")
        self.assertIsNone(state["specification"]["accepted_revision"])
        self.assertIsNone(state["work_tracking"]["provider"])
        self.assertFalse(state["work_tracking"]["verified"])
        delivery = state["delivery"]
        self.assertEqual((delivery["work_base"], delivery["integration_branch"],
                          delivery["staging_branch"], delivery["production_branch"]),
                         ("dev", "dev", "staging", "main"))
        self.assertIsNone(delivery["review_mode"])
        self.assertEqual(delivery["reviewers"], [])
        self.assertEqual(delivery["cleanup_status"], "pending")

    def test_spec_template_separates_requirements_from_execution_status(self):
        spec = text("templates/spec.md")
        for contract in ("REQ-001", "Acceptance", "Draft", "tracker", "revision", "Non-goals"):
            with self.subTest(contract=contract):
                self.assertIn(contract, spec)
        self.assertIn("not a task backlog", spec)

    def test_only_the_prescribed_pr_edges_are_documented(self):
        guide = text("references/sdlc.md")
        rows = []
        for line in guide.splitlines():
            cells = [c.strip().strip("`") for c in line.strip().strip("|").split("|")]
            if cells and cells[0] in ("Work PR", "Staging promotion PR", "Production promotion PR"):
                rows.append(tuple(cells[:3]))
        self.assertEqual(rows, [("Work PR", "work/<work-item>", "dev"),
                                ("Staging promotion PR", "dev", "staging"),
                                ("Production promotion PR", "staging", "main")])
        self.assertIn("persistent", guide)

    def test_all_prs_including_promotions_require_review_before_merge(self):
        guide = text("references/sdlc.md")
        for contract in ("Every PR must be reviewed before merge", "promotion PRs",
                         "reviewed head", "unresolved", "source changes"):
            with self.subTest(contract=contract):
                self.assertIn(contract, guide)

    def test_team_review_is_requested_from_named_non_author_developers(self):
        guide = text("references/sdlc.md")
        for contract in ("named eligible non-author", "request their review",
                         "assignee alone", "read back", "cannot silently switch"):
            with self.subTest(contract=contract):
                self.assertIn(contract, guide)

    def test_solo_self_review_is_recorded_without_fake_native_approval(self):
        guide = text("references/sdlc.md")
        for contract in ("solo", "self-review", "separate pass", "cannot approve its own PR",
                         "required independent", "head SHA"):
            with self.subTest(contract=contract):
                self.assertIn(contract, guide)

    def test_stage_and_main_have_fresh_post_merge_acceptance(self):
        guide = text("references/sdlc.md")
        for contract in ("after the staging merge", "after the main merge", "comprehensive suite",
                         "targeted", "failed staging", "production authorization"):
            with self.subTest(contract=contract):
                self.assertIn(contract, guide)

    def test_cleanup_is_mandatory_exact_and_preserves_live_or_unique_work(self):
        guide = text("references/workspace-hygiene.md")
        for contract in ("before merge", "after each merge", "git worktree list --porcelain",
                         "exact", "absent", "dirty", "active", "unique", "dev", "staging", "main",
                         "cache", "measured", "BLOCKED/INCOMPLETE", "do not rebuild"):
            with self.subTest(contract=contract):
                self.assertIn(contract, guide)
        self.assertIn("references/workspace-hygiene.md", text("SKILL.md"))

    def test_work_item_and_pr_templates_bind_spec_acceptance_and_review(self):
        issue = text("templates/github-issue.md")
        pr = text("templates/pull-request.md")
        for contract in ("spec.md", "requirement IDs", "spec revision", "Acceptance"):
            with self.subTest(contract=contract):
                self.assertIn(contract, issue)
        for contract in ("work item", "spec.md", "Review", "head SHA", "Cleanup", "promotion"):
            with self.subTest(contract=contract):
                self.assertIn(contract, pr)

    def test_tracker_outage_does_not_reintroduce_untracked_coding(self):
        guide = text("references/onboarding.md")
        self.assertIn("tracker-backed work item before implementation", guide)
        self.assertIn("ideation and read-only discovery", guide)
        self.assertIn("legacy", guide)
        self.assertNotIn("This is a bootstrap exception", guide)

    def test_onboarding_resolves_tracking_and_review_before_local_proof(self):
        guide = text("references/onboarding.md")
        before_local = guide.split("## Stage A", 1)[0]
        for contract in ("Select and verify the issue tracker/project", "Stage C",
                         "team/solo review mode", "dev/staging/main", "from dev"):
            with self.subTest(contract=contract):
                self.assertIn(contract, before_local)

    def test_supporting_guides_keep_the_spec_and_review_lane_authoritative(self):
        publishing = text("references/publishing.md")
        for contract in ("[SDLC](sdlc.md)", "spec.md", "tracker work items",
                         "Every PR needs current qualified review", "staging -> main"):
            with self.subTest(contract=contract):
                self.assertIn(contract, publishing)
        ai = text("references/ai-feasibility.md")
        self.assertIn("spec.md", ai)
        self.assertIn("affected requirement IDs", ai)
        self.assertNotIn("into the general project charter", ai)

    def test_state_upgrade_preserves_legacy_evidence_without_guessing_acceptance(self):
        state = json.loads(text("templates/onboarding-state.json"))
        self.assertEqual(state["schema_version"], 3)
        self.assertIsNone(state["canonical_work_item"])
        guide = text("references/onboarding.md")
        for contract in ("legacy schema-1/2", "preserve provider evidence",
                         "canonical_issue", "temporary_intake", "observed facts"):
            with self.subTest(contract=contract):
                self.assertIn(contract, guide)


if __name__ == "__main__":
    unittest.main()
