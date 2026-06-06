import tempfile
import unittest
from pathlib import Path

from os_agent.analyzer import KernelAnalyzer
from os_agent.collector import RepoCollector
from os_agent.parser import SymbolParser


class KernelAnalyzerEvidenceTest(unittest.TestCase):
    def test_markdown_keyword_does_not_confirm_os_dimension(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "README.md").write_text("This document mentions syscall and scheduler.\n", encoding="utf-8")
            snapshot = RepoCollector().from_local(root, repo_id="doc-only")
            parsed = SymbolParser().parse_repo(snapshot)

            profile = KernelAnalyzer().analyze(snapshot, parsed)

        self.assertEqual(profile.dimensions["syscall"][0].confidence, "unconfirmed")
        self.assertEqual(profile.dimensions["scheduler"][0].confidence, "unconfirmed")


if __name__ == "__main__":
    unittest.main()
