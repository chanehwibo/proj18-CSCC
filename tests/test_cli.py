import unittest

from os_agent.cli import build_parser, cmd_demo


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


if __name__ == "__main__":
    unittest.main()
