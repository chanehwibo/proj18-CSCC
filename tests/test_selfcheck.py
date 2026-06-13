import tempfile
import unittest
from pathlib import Path

from os_agent.models import CompareResult, Evidence, Finding, KernelProfile, RepoMeta
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

    def test_compare_summary_without_roots_counts_evidence_as_invalid(self):
        result = CompareResult(
            new_repo="new",
            history_repos=["hist"],
            overlap_points=[
                Finding(
                    "对比证据缺少仓库 root 时不能默认通过。",
                    confidence="medium",
                    evidence=[Evidence("kernel.rs", 1, 1, "fn main() {}\n", repo_id="new")],
                )
            ],
        )

        summary = EvidenceChecker().compare_summary(result)

        self.assertEqual(summary["key_findings"], 1)
        self.assertEqual(summary["with_evidence"], 1)
        self.assertEqual(summary["invalid_evidence"], 1)

    def test_compare_summary_checks_repo_scoped_evidence_roots(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            new_root = root / "new"
            hist_root = root / "hist"
            (new_root / "kernel").mkdir(parents=True)
            (hist_root / "kernel").mkdir(parents=True)
            (new_root / "kernel" / "trap.c").write_text("void syscall(void) {}\n", encoding="utf-8")
            (hist_root / "kernel" / "sched.c").write_text("void schedule(void) {}\n", encoding="utf-8")

            result = CompareResult(
                new_repo="new",
                history_repos=["hist"],
                evidence_roots={"new": str(new_root), "hist": str(hist_root)},
                overlap_points=[
                    Finding(
                        "对比证据需要按仓库 root 校验。",
                        confidence="high",
                        evidence=[
                            Evidence("kernel/trap.c", 1, 1, "", repo_id="new"),
                            Evidence("kernel/sched.c", 1, 1, "", repo_id="hist"),
                            Evidence("kernel/trap.c", 1, 1, "", repo_id="hist"),
                        ],
                    )
                ],
            )

            summary = EvidenceChecker().compare_summary(result)

        self.assertEqual(summary["key_findings"], 1)
        self.assertEqual(summary["with_evidence"], 1)
        self.assertEqual(summary["invalid_evidence"], 1)


if __name__ == "__main__":
    unittest.main()
