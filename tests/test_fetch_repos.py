import importlib.util
import sys
import unittest
from pathlib import Path


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


if __name__ == "__main__":
    unittest.main()
