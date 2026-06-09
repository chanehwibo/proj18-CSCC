import tempfile
import unittest
from pathlib import Path

from os_agent.collector import RepoCollector
from os_agent.parser import SymbolParser


class SymbolParserTest(unittest.TestCase):
    def test_c_control_flow_is_not_reported_as_function(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "kernel.c").write_text(
                "void real_function(void) {}\n"
                "else if (condition) {\n"
                "    return;\n"
                "}\n"
                "if (condition) {\n"
                "    return;\n"
                "}\n",
                encoding="utf-8",
            )
            snapshot = RepoCollector().from_local(root, repo_id="parser-control-flow")
            symbols = SymbolParser().parse_repo(snapshot).symbols

        names = [symbol.name for symbol in symbols]
        self.assertIn("real_function", names)
        self.assertNotIn("if", names)
        self.assertNotIn("else", names)


if __name__ == "__main__":
    unittest.main()
