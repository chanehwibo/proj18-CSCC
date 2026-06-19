import tempfile
import time
import unittest
from pathlib import Path
from unittest.mock import patch

from os_agent.models import KernelProfile, RepoMeta
from os_agent.profile_cache import ProfileCache, SourceFingerprint


class ProfileCacheTest(unittest.TestCase):
    def test_cache_hits_until_source_changes(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            repo = root / "repo"
            repo.mkdir()
            source = repo / "kernel.c"
            source.write_text("int main(void) { return 0; }\n", encoding="utf-8")
            cache = ProfileCache(root / "profiles")
            calls = {"count": 0}

            def builder() -> KernelProfile:
                calls["count"] += 1
                return KernelProfile(meta=RepoMeta(repo_id="repo", name="repo", root_path=str(repo)))

            first = cache.get_or_build(repo, "repo", builder)
            second = cache.get_or_build(repo, "repo", builder)

            self.assertFalse(first.hit)
            self.assertTrue(second.hit)
            self.assertEqual(calls["count"], 1)

            time.sleep(0.01)
            source.write_text("int main(void) { return 1; }\n", encoding="utf-8")
            third = cache.get_or_build(repo, "repo", builder)

            self.assertFalse(third.hit)
            self.assertEqual(calls["count"], 2)

    def test_force_rebuild_bypasses_valid_cache(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            repo = root / "repo"
            repo.mkdir()
            (repo / "kernel.c").write_text("int main(void) { return 0; }\n", encoding="utf-8")
            cache = ProfileCache(root / "profiles")
            calls = {"count": 0}

            def builder() -> KernelProfile:
                calls["count"] += 1
                return KernelProfile(meta=RepoMeta(repo_id="repo", name="repo", root_path=str(repo)))

            cache.get_or_build(repo, "repo", builder)
            rebuilt = cache.get_or_build(repo, "repo", builder, force_rebuild=True)

            self.assertFalse(rebuilt.hit)
            self.assertEqual(calls["count"], 2)

    def test_clean_git_repo_uses_fast_fingerprint_without_tree_scan(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            repo = root / "repo"
            repo.mkdir()
            cache = ProfileCache(root / "profiles")

            with (
                patch.object(cache, "_git_head", return_value="abc123"),
                patch.object(cache, "_git_worktree_clean", return_value=True),
                patch.object(cache, "_git_tracked_file_count", return_value=7),
                patch.object(cache, "_full_tree_fingerprint") as full_scan,
            ):
                fingerprint = cache.fingerprint(repo)

        self.assertEqual(fingerprint.commit, "git-clean:abc123")
        self.assertEqual(fingerprint.file_count, 7)
        self.assertEqual(fingerprint.total_size, 0)
        self.assertEqual(fingerprint.newest_mtime_ns, 0)
        full_scan.assert_not_called()

    def test_dirty_git_repo_falls_back_to_full_tree_fingerprint(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            repo = root / "repo"
            repo.mkdir()
            cache = ProfileCache(root / "profiles")
            full = SourceFingerprint(
                root_path=str(repo),
                commit="abc123",
                file_count=1,
                total_size=32,
                newest_mtime_ns=99,
            )

            with (
                patch.object(cache, "_git_head", return_value="abc123"),
                patch.object(cache, "_git_worktree_clean", return_value=False),
                patch.object(cache, "_full_tree_fingerprint", return_value=full) as full_scan,
            ):
                fingerprint = cache.fingerprint(repo)

        self.assertEqual(fingerprint, full)
        full_scan.assert_called_once_with(repo)


if __name__ == "__main__":
    unittest.main()
