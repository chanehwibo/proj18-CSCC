import unittest

from os_agent.models import CompareResult, Evidence, Finding, KernelProfile, RepoMeta
from os_agent.reporter import Reporter


class ReporterTest(unittest.TestCase):
    def test_compare_report_renders_overlap_and_code_snippets(self):
        result = CompareResult(
            new_repo="new-os",
            history_repos=["hist-os"],
            overlap_points=[
                Finding(
                    "与 hist-os 在“系统调用”维度存在功能重合。",
                    confidence="medium",
                    evidence=[
                        Evidence("kernel/trap.c", 10, 12, "void syscall(void) {\n dispatch();\n}", note="new evidence"),
                        Evidence("hist/trap.c", 20, 22, "void syscall(void) {\n handle();\n}", note="history evidence"),
                    ],
                )
            ],
        )

        report = Reporter().render_compare(result)

        self.assertIn("功能重合与疑似重复证据", report)
        self.assertIn("不直接判定代码抄袭", report)
        self.assertIn("kernel/trap.c:L10-L12", report)
        self.assertIn("代码片段：`void syscall(void) { dispatch(); }`", report)

    def test_profile_report_renders_dimension_review_with_evidence_table(self):
        profile = KernelProfile(
            meta=RepoMeta(repo_id="new-os", name="new-os", languages={"c": 10}, file_count=1, loc_total=10),
            overview="overview",
            dimensions={
                "syscall": [
                    Finding(
                        "项目包含系统调用分发逻辑。",
                        confidence="high",
                        evidence=[Evidence("kernel/syscall.c", 1, 3, "void syscall(void) {\n dispatch();\n}", note="keyword hit")],
                    )
                ]
            },
        )

        report = Reporter().render_profile(profile)

        self.assertIn("证据表", report)
        self.assertIn("关键代码片段", report)
        self.assertIn("复核建议", report)
        self.assertIn("kernel/syscall.c", report)


if __name__ == "__main__":
    unittest.main()
