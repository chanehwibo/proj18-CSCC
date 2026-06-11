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

    def test_c_macro_definitions_are_reported_as_symbols(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "syscall.h").write_text(
                "#define SYS_fork 1\n"
                "#define PTE_P 0x001\n"
                "void sys_fork(void) {}\n",
                encoding="utf-8",
            )
            snapshot = RepoCollector().from_local(root, repo_id="parser-macro")
            symbols = SymbolParser().parse_repo(snapshot).symbols

        macro_names = {symbol.name for symbol in symbols if symbol.kind == "macro"}
        self.assertIn("SYS_fork", macro_names)
        self.assertIn("PTE_P", macro_names)

    def test_c_struct_usage_is_not_reported_as_definition(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "proc.c").write_text(
                "struct proc *p = myproc();\n"
                "struct trapframe *tf;\n"
                "struct cpu {\n"
                "  int id;\n"
                "};\n",
                encoding="utf-8",
            )
            snapshot = RepoCollector().from_local(root, repo_id="parser-struct-usage")
            symbols = SymbolParser().parse_repo(snapshot).symbols

        struct_names = {symbol.name for symbol in symbols if symbol.kind == "struct"}
        self.assertIn("cpu", struct_names)
        self.assertNotIn("proc", struct_names)
        self.assertNotIn("trapframe", struct_names)


if __name__ == "__main__":
    unittest.main()
