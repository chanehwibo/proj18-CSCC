import tempfile
import time
import unittest
from pathlib import Path

from os_agent.models import KernelProfile, RepoMeta
from os_agent.profile_cache import ProfileCache


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


if __name__ == "__main__":
    unittest.main()
