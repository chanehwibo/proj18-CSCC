import unittest

from os_agent.analyzer import KernelAnalyzer


class KernelAnalyzerPathPriorityTest(unittest.TestCase):
    def test_kernel_paths_rank_before_docs_and_tools(self):
        analyzer = KernelAnalyzer()
        paths = [
            "outline.md",
            "xtask/src/arch.rs",
            "user/src/main.rs",
            "os/src/trap/mod.rs",
            "kernel/proc.c",
        ]

        ranked = sorted(paths, key=lambda path: analyzer._path_score(path, ["trap", "proc"]))

        self.assertEqual(ranked[:2], ["kernel/proc.c", "os/src/trap/mod.rs"])
        self.assertLess(ranked.index("kernel/proc.c"), ranked.index("outline.md"))
        self.assertLess(ranked.index("os/src/trap/mod.rs"), ranked.index("xtask/src/arch.rs"))
        self.assertLess(ranked.index("os/src/trap/mod.rs"), ranked.index("user/src/main.rs"))


if __name__ == "__main__":
    unittest.main()
