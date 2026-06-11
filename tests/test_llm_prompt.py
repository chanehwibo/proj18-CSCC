import unittest

from os_agent.llm import LLMReportGenerator
from os_agent.models import CompareResult, Finding


class LLMComparePromptTest(unittest.TestCase):
    def test_compare_prompt_includes_selection_overlap_self_check_and_uncertain_unique_rule(self):
        result = CompareResult(
            new_repo="new-os",
            history_repos=["hist-os"],
            selection_notes=["hist-os：score=1.00；OS 维度重合度 1.00"],
            overlap_points=[Finding("与 hist-os 在系统调用维度存在功能重合。", confidence="medium")],
            code_similarity_points=[Finding("与 hist-os 在系统调用维度发现片段级代码相似度 0.82。", confidence="high")],
            similarities=[Finding("与 hist-os 在系统调用维度均有可确认实现。", confidence="medium")],
        )

        prompt = LLMReportGenerator.__new__(LLMReportGenerator)._compare_prompt(result)

        self.assertIn("selection_notes", prompt)
        self.assertIn("overlap_points", prompt)
        self.assertIn("code_similarity_points", prompt)
        self.assertIn("代码级相似线索检测", prompt)
        self.assertIn("代码级可复核线索", prompt)
        self.assertIn("不能直接判定代码抄袭", prompt)
        self.assertIn("self_check", prompt)
        self.assertIn("当前证据不足，未自动确认创新点", prompt)
        self.assertIn("不能强行总结创新点", prompt)
        self.assertIn("不得把未标注为 verified_award 的历史样本称为特奖、一等奖或优秀获奖案例", prompt)


if __name__ == "__main__":
    unittest.main()
