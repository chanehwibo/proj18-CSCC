import unittest

from os_agent.cli import build_parser, cmd_audit_llm_report, cmd_demo


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


if __name__ == "__main__":
    unittest.main()
