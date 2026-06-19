import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from os_agent.cli import (
    SOURCE_TIER_LABELS,
    _history_repo_dirs,
    build_parser,
    build_history_profiles,
    cmd_audit_llm_report,
    cmd_demo,
    source_tier_label,
)
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
        self.assertEqual(args.jobs, 1)
        self.assertTrue(args.llm_dry_run)
        self.assertFalse(args.use_llm)

    def test_compare_parser_includes_profile_cache_options(self):
        args = build_parser().parse_args(
            [
                "compare",
                "data/samples/xv6-public",
                "--repo-id",
                "xv6-public",
                "--jobs",
                "4",
                "--no-profile-cache",
                "--rebuild-profile-cache",
            ]
        )

        self.assertEqual(args.jobs, 4)
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

    def test_history_repo_dirs_are_sorted_and_skip_new_repo(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            history = root / "history"
            history.mkdir()
            new_repo = history / "new"
            z_repo = history / "zeta"
            a_repo = history / "alpha"
            hidden_repo = history / ".cache"
            for path in (new_repo, z_repo, a_repo, hidden_repo):
                path.mkdir()
            (history / "README.md").write_text("not a repo dir", encoding="utf-8")

            repo_dirs = _history_repo_dirs(history, new_repo.resolve())

        self.assertEqual([path.name for path in repo_dirs], ["alpha", "zeta"])

    def test_build_history_profiles_preserves_sorted_order_with_jobs(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            history = root / "history"
            history.mkdir()
            for name in ("beta", "alpha"):
                (history / name).mkdir()

            def fake_build(repo_dir, *, use_cache, force_rebuild):
                return (
                    KernelProfile(meta=RepoMeta(repo_id=repo_dir.name, name=repo_dir.name)),
                    repo_dir.name == "alpha",
                )

            with patch("os_agent.cli._build_history_profile", side_effect=fake_build):
                profiles, cache_hits, cache_rebuilt = build_history_profiles(
                    history,
                    (root / "new").resolve(),
                    jobs=2,
                    use_cache=True,
                    force_rebuild=False,
                )

        self.assertEqual([profile.meta.repo_id for profile in profiles], ["alpha", "beta"])
        self.assertEqual(cache_hits, 1)
        self.assertEqual(cache_rebuilt, 1)


if __name__ == "__main__":
    unittest.main()
