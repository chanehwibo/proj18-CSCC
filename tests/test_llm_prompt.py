import unittest

from os_agent.llm import LLMReportGenerator
from os_agent.models import CompareResult, Finding


class LLMComparePromptTest(unittest.TestCase):
    def test_compare_prompt_includes_selection_self_check_and_uncertain_unique_rule(self):
        result = CompareResult(
            new_repo="new-os",
            history_repos=["hist-os"],
            selection_notes=["hist-os：score=1.00；OS 维度重合度 1.00"],
            similarities=[Finding("与 hist-os 在系统调用维度均有可确认实现。", confidence="medium")],
        )

        prompt = LLMReportGenerator.__new__(LLMReportGenerator)._compare_prompt(result)

        self.assertIn("selection_notes", prompt)
        self.assertIn("self_check", prompt)
        self.assertIn("当前证据不足，未自动确认创新点", prompt)
        self.assertIn("不能强行总结创新点", prompt)


if __name__ == "__main__":
    unittest.main()
