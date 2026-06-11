import tempfile
import unittest
from pathlib import Path

from os_agent.collector import RepoCollector


class RepoCollectorSourceTierTest(unittest.TestCase):
    def test_manifest_category_maps_to_source_tier(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            samples = root / "samples"
            repo = samples / "case-os"
            repo.mkdir(parents=True)
            (repo / "kernel.c").write_text("int main(void) { return 0; }\n", encoding="utf-8")
            (samples / "manifest.json").write_text(
                "{\n"
                '  "repos": [\n'
                "    {\n"
                '      "repo_id": "case-os",\n'
                '      "name": "Case OS",\n'
                '      "category": "contest-case",\n'
                '      "url": "https://example.test/case-os.git"\n'
                "    }\n"
                "  ]\n"
                "}\n",
                encoding="utf-8",
            )

            snapshot = RepoCollector(samples).from_local(repo, repo_id="case-os")

        self.assertEqual(snapshot.meta.source_tier, "competition_sample")
        self.assertIsNone(snapshot.meta.award_level)
        self.assertIsNone(snapshot.meta.award_source_url)


if __name__ == "__main__":
    unittest.main()
