import unittest

from os_agent.cli import SOURCE_TIER_LABELS, build_parser, cmd_audit_llm_report, cmd_demo, source_tier_label
from os_agent.models import KernelProfile, RepoMeta


class CliParserTest(unittest.TestCase):
    def test_demo_parser_includes_llm_and_history_options(self):
        args = build_parser().parse_args(
            [
                "demo",
                "data/samples/rcore-tutorial-v3",
                "--repo-id",
                "rcore-tutorial-v3",
                "--history",
                "data/samples",
                "--limit",
                "2",
                "--llm-dry-run",
            ]
        )

        self.assertIs(args.func, cmd_demo)
        self.assertEqual(args.repo_id, "rcore-tutorial-v3")
        self.assertEqual(args.history, "data/samples")
        self.assertEqual(args.limit, 2)
        self.assertTrue(args.llm_dry_run)
        self.assertFalse(args.use_llm)

    def test_compare_parser_includes_profile_cache_options(self):
        args = build_parser().parse_args(
            [
                "compare",
                "data/samples/xv6-public",
                "--repo-id",
                "xv6-public",
                "--no-profile-cache",
                "--rebuild-profile-cache",
            ]
        )

        self.assertTrue(args.no_profile_cache)
        self.assertTrue(args.rebuild_profile_cache)

    def test_audit_llm_report_parser(self):
        args = build_parser().parse_args(
            [
                "audit-llm-report",
                "--prompt",
                "data/reports/prompts/xv6-public.compare.prompt.md",
                "--report",
                "data/reports/compare/xv6-public_vs_history.md",
            ]
        )

        self.assertIs(args.func, cmd_audit_llm_report)
        self.assertEqual(args.prompt, "data/reports/prompts/xv6-public.compare.prompt.md")
        self.assertEqual(args.report, "data/reports/compare/xv6-public_vs_history.md")

    def test_verified_award_label_requires_award_source_url(self):
        profile = KernelProfile(
            meta=RepoMeta(
                repo_id="missing-source-award",
                name="missing-source-award",
                source_tier="verified_award",
                award_level="一等奖",
            )
        )

        label = source_tier_label(profile)

        self.assertNotIn(SOURCE_TIER_LABELS["verified_award"], label)
        self.assertIn("获奖来源未填写", label)


if __name__ == "__main__":
    unittest.main()
