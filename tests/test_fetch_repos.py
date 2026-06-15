import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


SCRIPT_PATH = Path(__file__).resolve().parents[1] / "scripts" / "fetch_repos.py"
SPEC = importlib.util.spec_from_file_location("fetch_repos_script", SCRIPT_PATH)
fetch_repos = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = fetch_repos
SPEC.loader.exec_module(fetch_repos)


class FetchReposCloneArgsTest(unittest.TestCase):
    def test_positive_depth_uses_shallow_single_branch_clone(self):
        args = fetch_repos.build_clone_args(
            "https://example.com/repo.git",
            Path("samples") / "repo",
            depth=1,
        )

        self.assertEqual(
            args,
            [
                "clone",
                "--depth",
                "1",
                "--single-branch",
                "https://example.com/repo.git",
                str(Path("samples") / "repo"),
            ],
        )

    def test_non_positive_depth_uses_full_clone(self):
        for depth in (0, -1):
            with self.subTest(depth=depth):
                normalized_depth = fetch_repos.normalize_clone_depth(depth)
                args = fetch_repos.build_clone_args(
                    "https://example.com/repo.git",
                    Path("samples") / "repo",
                    depth=normalized_depth,
                )

                self.assertEqual(normalized_depth, 0)
                self.assertEqual(
                    args,
                    ["clone", "https://example.com/repo.git", str(Path("samples") / "repo")],
                )
                self.assertNotIn("--depth", args)
                self.assertNotIn("--single-branch", args)

    def test_resolve_repo_dir_rejects_unsafe_repo_ids(self):
        bad_repo_ids = ("../evil", "nested/repo", r"nested\repo", "C:evil", ".hidden", "")

        with tempfile.TemporaryDirectory() as tmp:
            out_dir = Path(tmp) / "samples"
            for repo_id in bad_repo_ids:
                with self.subTest(repo_id=repo_id):
                    with self.assertRaises(ValueError):
                        fetch_repos.resolve_repo_dir(out_dir, repo_id)

    def test_clone_one_rejects_unsafe_repo_id_without_git_or_delete(self):
        with tempfile.TemporaryDirectory() as tmp:
            out_dir = Path(tmp) / "samples"
            outside = Path(tmp) / "outside"
            outside.mkdir()
            marker = outside / "keep.txt"
            marker.write_text("do not delete", encoding="utf-8")

            with patch.object(fetch_repos, "run_git") as run_git:
                result = fetch_repos.clone_one(
                    {"repo_id": "../outside", "url": "https://example.com/repo.git"},
                    out_dir,
                    depth=1,
                    reclone=True,
                )

            self.assertEqual(result.status, "failed")
            self.assertIn("unsafe repo_id", result.error)
            self.assertTrue(marker.exists())
            run_git.assert_not_called()


if __name__ == "__main__":
    unittest.main()
