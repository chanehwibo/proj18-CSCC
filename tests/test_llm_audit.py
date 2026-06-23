import unittest

from os_agent.llm_audit import LLMReportAuditor


def prompt_with_evidence(unique_points="[]"):
    return (
        "# System\n\n"
        "system\n\n"
        "# User\n\n"
        "CompareResult JSON:\n"
        "```json\n"
        "{\n"
        '  "overlap_points": [\n'
        "    {\n"
        '      "statement": "功能重合",\n'
        '      "evidence": [\n'
        '        {"file": "kernel/syscall.c", "line_start": 10, "line_end": 14, "snippet": "syscall"}\n'
        "      ]\n"
        "    }\n"
        "  ],\n"
        f'  "unique_points": {unique_points},\n'
        '  "self_check": {"key_findings": 1, "with_evidence": 1, "coverage": 100.0}\n'
        "}\n"
        "```\n"
    )


def prompt_with_unicode_path_evidence():
    return (
        "# System\n\n"
        "system\n\n"
        "# User\n\n"
        "CompareResult JSON:\n"
        "```json\n"
        "{\n"
        '  "overlap_points": [\n'
        "    {\n"
        '      "statement": "中断重合",\n'
        '      "evidence": [\n'
        '        {"file": "LAB4 内存管理/trap.c", "line_start": 9, "line_end": 13, "snippet": "trap"}\n'
        "      ]\n"
        "    }\n"
        "  ],\n"
        '  "unique_points": [],\n'
        '  "self_check": {"key_findings": 1, "with_evidence": 1, "coverage": 100.0}\n'
        "}\n"
        "```\n"
    )


def prompt_with_adjacent_line_evidence():
    return (
        "# System\n\n"
        "system\n\n"
        "# User\n\n"
        "CompareResult JSON:\n"
        "```json\n"
        "{\n"
        '  "code_similarity_points": [\n'
        "    {\n"
        '      "statement": "宏名重合",\n'
        '      "evidence": [\n'
        '        {"file": "kernel/dev/uart.c", "line_start": 11, "line_end": 11, "snippet": "RHR"},\n'
        '        {"file": "kernel/dev/uart.c", "line_start": 12, "line_end": 12, "snippet": "THR"}\n'
        "      ]\n"
        "    }\n"
        "  ],\n"
        '  "unique_points": [],\n'
        '  "self_check": {"key_findings": 1, "with_evidence": 1, "coverage": 100.0}\n'
        "}\n"
        "```\n"
    )


def profile_prompt_with_evidence():
    return (
        "# System\n\n"
        "system\n\n"
        "# User\n\n"
        "KernelProfile JSON:\n"
        "```json\n"
        "{\n"
        '  "meta": {"repo_id": "demo-os"},\n'
        '  "dimensions": {\n'
        '    "scheduler": {\n'
        '      "findings": [\n'
        "        {\n"
        '          "statement": "调度器证据",\n'
        '          "evidence": [\n'
        '            {"file": "kernel/proc.c", "line_start": 3, "line_end": 6, "snippet": "schedule"}\n'
        "          ]\n"
        "        }\n"
        "      ]\n"
        "    }\n"
        "  },\n"
        '  "self_check": {"key_findings": 1, "with_evidence": 1, "coverage": 100.0}\n'
        "}\n"
        "```\n"
    )


class LLMReportAuditorTest(unittest.TestCase):
    def test_accepts_report_with_allowed_reference_and_required_sections(self):
        report = (
            "## 比较对象选择\n"
            "## 功能重合与疑似重复证据\n"
            "系统调用证据来自 `kernel/syscall.c:L10-L14`。\n"
            "## 代码级相似线索检测\n"
            "仅作为可复核线索。\n"
            "## 相似点\n"
            "## 差异点\n"
            "## 可能创新点\n"
            "当前证据不足，未自动确认创新点。\n"
            "## 待人工复核项\n"
            "## 核验摘要\n"
            "self_check coverage=100.0。\n"
        )

        result = LLMReportAuditor().audit(prompt_with_evidence(), report)

        self.assertTrue(result.ok)
        self.assertEqual(result.cited_reference_count, 1)

    def test_missing_compare_self_check_summary_is_error(self):
        report = (
            "## 比较对象选择\n"
            "## 功能重合\n"
            "`kernel/syscall.c:L10-L14`\n"
            "## 代码级相似\n"
            "## 相似点\n"
            "## 差异点\n"
            "## 可能创新点\n"
            "当前证据不足，未自动确认创新点。\n"
            "## 待人工复核\n"
        )

        result = LLMReportAuditor().audit(prompt_with_evidence(), report)

        self.assertFalse(result.ok)
        self.assertIn("missing_section", {issue.code for issue in result.issues})
        self.assertTrue(any(issue.severity == "error" and "核验摘要" in issue.message for issue in result.issues))

    def test_profile_audit_does_not_require_compare_sections(self):
        report = "调度器证据来自 `kernel/proc.c:L3-L6`。\n\n## 核验摘要\n\n- 关键结论数：1\n"

        result = LLMReportAuditor().audit(profile_prompt_with_evidence(), report)

        self.assertTrue(result.ok)
        messages = "\n".join(issue.message for issue in result.issues)
        self.assertNotIn("比较对象选择", messages)
        self.assertNotIn("可能创新点", messages)

    def test_profile_missing_self_check_summary_is_error(self):
        report = "调度器证据来自 `kernel/proc.c:L3-L6`。"

        result = LLMReportAuditor().audit(profile_prompt_with_evidence(), report)

        self.assertFalse(result.ok)
        self.assertTrue(any(issue.severity == "error" and "核验摘要" in issue.message for issue in result.issues))

    def test_accepts_range_covered_by_adjacent_evidence_items(self):
        report = (
            "## 比较对象选择\n"
            "## 功能重合\n"
            "`kernel/dev/uart.c:L11-L12`\n"
            "## 代码级相似\n"
            "## 相似点\n"
            "## 差异点\n"
            "## 可能创新点\n"
            "当前证据不足，未自动确认创新点。\n"
            "## 待人工复核\n"
            "## 核验摘要\n"
        )

        result = LLMReportAuditor().audit(prompt_with_adjacent_line_evidence(), report)

        self.assertTrue(result.ok)
        self.assertEqual(result.cited_reference_count, 1)

    def test_accepts_unicode_path_reference(self):
        report = (
            "## 比较对象选择\n"
            "## 功能重合\n"
            "中断证据来自 `LAB4 内存管理/trap.c:L9-L13`。\n"
            "## 代码级相似\n"
            "## 相似点\n"
            "## 差异点\n"
            "## 可能创新点\n"
            "当前证据不足，未自动确认创新点。\n"
            "## 待人工复核\n"
            "## 核验摘要\n"
        )

        result = LLMReportAuditor().audit(prompt_with_unicode_path_evidence(), report)

        self.assertTrue(result.ok)
        self.assertEqual(result.cited_reference_count, 1)

    def test_flags_unknown_reference(self):
        report = (
            "## 比较对象选择\n"
            "## 功能重合\n"
            "`kernel/syscall.c:L99-L100`\n"
            "## 代码级相似\n"
            "## 相似点\n"
            "## 差异点\n"
            "## 可能创新点\n"
            "当前证据不足，未自动确认创新点。\n"
            "## 待人工复核\n"
            "## 核验摘要\n"
        )

        result = LLMReportAuditor().audit(prompt_with_evidence(), report)

        self.assertFalse(result.ok)
        self.assertIn("unknown_reference", {issue.code for issue in result.issues})

    def test_flags_forbidden_plagiarism_claim(self):
        report = (
            "## 比较对象选择\n"
            "## 功能重合\n"
            "`kernel/syscall.c:L10-L14`\n"
            "## 代码级相似\n"
            "该项目确认抄袭历史项目。\n"
            "## 相似点\n"
            "## 差异点\n"
            "## 可能创新点\n"
            "当前证据不足，未自动确认创新点。\n"
            "## 待人工复核\n"
            "## 核验摘要\n"
        )

        result = LLMReportAuditor().audit(prompt_with_evidence(), report)

        self.assertFalse(result.ok)
        self.assertIn("forbidden_claim", {issue.code for issue in result.issues})

    def test_allows_negated_plagiarism_boundary_statement(self):
        report = (
            "## 比较对象选择\n"
            "## 功能重合\n"
            "`kernel/syscall.c:L10-L14`\n"
            "## 代码级相似\n"
            "该线索不构成抄袭裁定，只能人工复核。\n"
            "## 相似点\n"
            "## 差异点\n"
            "## 可能创新点\n"
            "当前证据不足，未自动确认创新点。\n"
            "## 待人工复核\n"
            "## 核验摘要\n"
        )

        result = LLMReportAuditor().audit(prompt_with_evidence(), report)

        self.assertTrue(result.ok)
        self.assertNotIn("forbidden_claim", {issue.code for issue in result.issues})


if __name__ == "__main__":
    unittest.main()
