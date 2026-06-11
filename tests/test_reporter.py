import tempfile
import unittest
from pathlib import Path

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
            code_similarity_points=[
                Finding(
                    "与 hist-os 在“系统调用”维度发现片段级代码相似度 0.82。",
                    confidence="high",
                    evidence=[
                        Evidence("kernel/trap.c", 10, 12, "void syscall(void) {\n dispatch();\n}", note="new evidence"),
                        Evidence("hist/trap.c", 20, 22, "void syscall(void) {\n dispatch();\n}", note="history evidence"),
                    ],
                )
            ],
        )

        report = Reporter().render_compare(result)

        self.assertIn("未核验比赛样本不作为特奖/一等奖背书", report)
        self.assertIn("功能重合与疑似重复证据", report)
        self.assertIn("代码级相似线索检测", report)
        self.assertIn("片段级代码相似度 0.82", report)
        self.assertIn("不直接判定代码抄袭", report)
        self.assertIn("kernel/trap.c:L10-L12", report)
        self.assertIn("代码片段：`void syscall(void) { dispatch(); }`", report)

    def test_profile_report_renders_dimension_review_with_evidence_table(self):
        profile = KernelProfile(
            meta=RepoMeta(
                repo_id="new-os",
                name="new-os",
                source_tier="competition_sample",
                languages={"c": 10},
                file_count=1,
                loc_total=10,
            ),
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
        self.assertIn("样本来源等级：比赛作品样本（获奖等级未核验）", report)
        self.assertIn("关键代码片段", report)
        self.assertIn("复核建议", report)
        self.assertIn("kernel/syscall.c", report)

    def test_profile_report_renders_evidence_bound_maturity_score(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for filename in ["Makefile", "sched.c", "vm.c", "syscall.c", "fs.c", "lock.c", "trap.c", "uart.c"]:
                (root / filename).write_text("void marker(void) {}\n", encoding="utf-8")
            profile = KernelProfile(
                meta=RepoMeta(repo_id="mature-os", name="mature-os", root_path=str(root), languages={"c": 80}, file_count=8, loc_total=80),
                overview="overview",
                build_system=Finding("仓库包含构建入口：Makefile。", confidence="high", evidence=[Evidence("Makefile", 1, 1, "all:\n", note="构建入口")]),
                dimensions={
                    "scheduler": [Finding("包含调度实现。", confidence="high", evidence=[Evidence("sched.c", 1, 1, "void marker(void) {}\n")])],
                    "memory": [Finding("包含内存管理实现。", confidence="high", evidence=[Evidence("vm.c", 1, 1, "void marker(void) {}\n")])],
                    "syscall": [Finding("包含系统调用实现。", confidence="high", evidence=[Evidence("syscall.c", 1, 1, "void marker(void) {}\n")])],
                    "filesystem": [Finding("包含文件系统实现。", confidence="high", evidence=[Evidence("fs.c", 1, 1, "void marker(void) {}\n")])],
                    "sync": [Finding("包含同步实现。", confidence="high", evidence=[Evidence("lock.c", 1, 1, "void marker(void) {}\n")])],
                    "interrupt": [Finding("包含中断实现。", confidence="high", evidence=[Evidence("trap.c", 1, 1, "void marker(void) {}\n")])],
                    "driver": [Finding("包含驱动实现。", confidence="high", evidence=[Evidence("uart.c", 1, 1, "void marker(void) {}\n")])],
                },
            )

            report = Reporter().render_profile(profile)

        self.assertIn("## 摘要评分", report)
        self.assertIn("综合成熟度：A 级：机制完整、证据充分（100/100）", report)
        self.assertIn("| OS 机制覆盖 | 80/80 |", report)
        self.assertIn("| 构建入口 | 10/10 |", report)
        self.assertIn("| 证据健康度 | 10/10 |", report)
        self.assertIn("| 调度与任务管理 | 已确认 | high | 1 |", report)
        self.assertIn("不代表比赛官方评分，也不调用 LLM", report)


if __name__ == "__main__":
    unittest.main()
