import importlib.util
import json
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

    def test_windows_git_cmd_is_wrapped_with_cmd(self):
        git_cmd = r"C:\Users\demo\AppData\Local\Microsoft\WindowsApps\git.cmd"
        comspec = r"C:\Windows\System32\cmd.exe"

        with patch.object(fetch_repos.shutil, "which", return_value=git_cmd), \
             patch.object(fetch_repos.sys, "platform", "win32"), \
             patch.dict(fetch_repos.os.environ, {"COMSPEC": comspec}):
            command = fetch_repos.resolve_git_command()

        self.assertEqual(command, [comspec, "/c", git_cmd])

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

    def test_write_repo_meta_preserves_award_source_fields(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo_dir = Path(tmp) / "repo"
            repo_dir.mkdir()
            fetch_repos.write_repo_meta(
                repo_dir,
                {
                    "repo_id": "award2024-demo",
                    "name": "Demo Award OS",
                    "url": "https://example.com/demo.git",
                    "year": 2024,
                    "category": "competition",
                    "source_tier": "verified_award",
                    "award_level": "一等奖",
                    "award_source_url": "https://example.com/winners.md",
                    "style": "componentized",
                    "arch": ["riscv64"],
                    "language_primary": "Rust",
                    "team": "demo team",
                    "school": "demo school",
                    "license": "MIT",
                    "note": "verified from official winners list",
                },
                head="abc123",
                depth=1,
            )

            meta = json.loads((repo_dir / ".kernelsage_meta.json").read_text(encoding="utf-8"))

        self.assertEqual(meta["year"], 2024)
        self.assertEqual(meta["source_tier"], "verified_award")
        self.assertEqual(meta["award_level"], "一等奖")
        self.assertEqual(meta["award_source_url"], "https://example.com/winners.md")


if __name__ == "__main__":
    unittest.main()
