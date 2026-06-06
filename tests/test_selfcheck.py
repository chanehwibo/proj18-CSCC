import tempfile
import unittest
from pathlib import Path

from os_agent.models import Evidence, Finding, KernelProfile, RepoMeta
from os_agent.selfcheck import EvidenceChecker


class EvidenceCheckerTest(unittest.TestCase):
    def test_profile_summary_counts_invalid_evidence(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "kernel.rs"
            source.write_text("fn main() {}\nfn syscall() {}\n", encoding="utf-8")
            profile = KernelProfile(
                meta=RepoMeta(repo_id="sample", name="sample", root_path=str(root)),
                dimensions={
                    "syscall": [
                        Finding(
                            "项目包含系统调用入口。",
                            confidence="high",
                            evidence=[Evidence("kernel.rs", 1, 2, "fn main() {}", note="测试证据")],
                        ),
                        Finding(
                            "项目包含无效证据引用。",
                            confidence="medium",
                            evidence=[Evidence("missing.rs", 1, 1, "", note="缺失文件")],
                        ),
                        Finding("未确认文件系统实现。", confidence="unconfirmed"),
                    ]
                },
            )

            summary = EvidenceChecker().profile_summary(profile)

        self.assertEqual(summary["key_findings"], 2)
        self.assertEqual(summary["with_evidence"], 2)
        self.assertEqual(summary["invalid_evidence"], 1)
        self.assertEqual(summary["unconfirmed"], 1)


if __name__ == "__main__":
    unittest.main()
