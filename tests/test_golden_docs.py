from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class GoldenDocsTest(unittest.TestCase):
    def test_golden_docs_exist_and_keep_audit_contract(self):
        cases = {
            "docs/GOLDEN_CASES.md": [
                "Golden 判定标准",
                "xv6-public.describe.golden.md",
                "oskernel2024-aabcb.compare.golden.md",
            ],
            "docs/golden/xv6-public.describe.golden.md": [
                "人工审核结论：通过",
                "data/reports/describe/xv6-public.md",
                "proc.c:L315-L352",
                "syscall.c:L107-L145",
            ],
            "docs/golden/oskernel2024-aabcb.compare.golden.md": [
                "人工审核结论：通过",
                "data/reports/compare/oskernel2024-aabcb_vs_history.md",
                "include/memlayout.h:L43-L49",
                "不是抄袭裁定",
            ],
        }

        for relative_path, markers in cases.items():
            with self.subTest(path=relative_path):
                text = (ROOT / relative_path).read_text(encoding="utf-8")
                for marker in markers:
                    self.assertIn(marker, text)

    def test_golden_compare_keeps_similarity_boundary(self):
        text = (ROOT / "docs/golden/oskernel2024-aabcb.compare.golden.md").read_text(
            encoding="utf-8"
        )

        self.assertIn("不直接判定代码抄袭", text)
        self.assertIn("不能直接判定复制", text)
        self.assertIn("只能作为弱到中等线索", text)


if __name__ == "__main__":
    unittest.main()
