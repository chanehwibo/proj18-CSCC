"""Local audit utilities for LLM generated reports."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


JSON_BLOCK_RE = re.compile(r"```json\s*(?P<json>.*?)```", re.DOTALL)
REF_RE = re.compile(r"`(?P<file>[^`\r\n]+?):L(?P<start>\d+)(?:-L(?P<end>\d+))?`")

VALID_REPORT_TYPES = {"auto", "profile", "compare"}

REQUIRED_COMPARE_WARNING_SECTIONS = (
    "比较对象选择",
    "功能重合",
    "代码级相似",
    "相似点",
    "差异点",
    "可能创新点",
    "待人工复核",
)
REQUIRED_COMPARE_ERROR_SECTIONS = (
    "核验摘要",
)
REQUIRED_COMPARE_SECTIONS = REQUIRED_COMPARE_WARNING_SECTIONS + REQUIRED_COMPARE_ERROR_SECTIONS
REQUIRED_PROFILE_ERROR_SECTIONS = (
    "核验摘要",
)

COMPARE_HINT_KEYS = {
    "new_repo",
    "history_repos",
    "selection_notes",
    "overlap_points",
    "code_similarity_points",
    "similarities",
    "differences",
    "unique_points",
}
PROFILE_HINT_KEYS = {
    "meta",
    "overview",
    "build_system",
    "dimensions",
}

FORBIDDEN_CLAIM_PATTERNS = (
    "确认抄袭",
    "构成抄袭",
    "存在抄袭",
    "判定为抄袭",
    "可以判定抄袭",
    "代码重复已确认",
    "确认重复",
    "直接复制",
    "明显抄袭",
)
SAFE_FORBIDDEN_CLAIM_CONTEXTS = (
    "不确认抄袭",
    "未确认抄袭",
    "不能确认抄袭",
    "无法确认抄袭",
    "不构成抄袭",
    "未构成抄袭",
    "不能构成抄袭",
    "无法构成抄袭",
    "不能直接判定抄袭",
    "不直接判定抄袭",
    "不能判定为抄袭",
    "不判定为抄袭",
)


@dataclass(frozen=True)
class EvidenceRange:
    file: str
    line_start: int
    line_end: int

    def covers(self, file: str, line_start: int, line_end: int) -> bool:
        return self.file == file and self.line_start <= line_start <= line_end <= self.line_end


@dataclass
class LLMAuditIssue:
    code: str
    message: str
    severity: str = "error"


@dataclass
class LLMAuditResult:
    issues: list[LLMAuditIssue] = field(default_factory=list)
    allowed_evidence_count: int = 0
    cited_reference_count: int = 0

    @property
    def ok(self) -> bool:
        return not any(issue.severity == "error" for issue in self.issues)

    def to_dict(self) -> dict[str, Any]:
        return {
            "ok": self.ok,
            "allowed_evidence_count": self.allowed_evidence_count,
            "cited_reference_count": self.cited_reference_count,
            "issues": [issue.__dict__ for issue in self.issues],
        }


class LLMReportAuditor:
    """Audit whether an LLM report stays inside the prompt evidence boundary."""

    def audit_paths(self, prompt_path: Path, report_path: Path, *, report_type: str = "auto") -> LLMAuditResult:
        return self.audit(
            prompt_path.read_text(encoding="utf-8", errors="replace"),
            report_path.read_text(encoding="utf-8", errors="replace"),
            report_type=report_type,
        )

    def audit(self, prompt_text: str, report_text: str, *, report_type: str = "auto") -> LLMAuditResult:
        result = LLMAuditResult()
        if report_type not in VALID_REPORT_TYPES:
            result.issues.append(
                LLMAuditIssue(
                    "invalid_report_type",
                    f"未知 LLM 报告类型：{report_type}，应为 auto/profile/compare。",
                )
            )
            return result

        prompt_json = self._extract_prompt_json(prompt_text, result)
        resolved_report_type = self._resolve_report_type(prompt_json, report_type)
        evidence_ranges = self._extract_evidence_ranges(prompt_json)
        result.allowed_evidence_count = len(evidence_ranges)

        cited_refs = self._extract_report_refs(report_text)
        result.cited_reference_count = len(cited_refs)

        if evidence_ranges and not cited_refs:
            result.issues.append(
                LLMAuditIssue(
                    "missing_citations",
                    "LLM 报告没有发现 `path:Lx-Ly` 形式的源码证据引用，可能弱化了证据链。",
                )
            )

        for file, start, end in cited_refs:
            if not self._reference_allowed(file, start, end, evidence_ranges):
                result.issues.append(
                    LLMAuditIssue(
                        "unknown_reference",
                        f"LLM 报告引用了 prompt evidence 中不存在或未覆盖的行号：{file}:L{start}-L{end}。",
                    )
                )

        if resolved_report_type == "compare":
            self._check_required_sections(
                result,
                report_text,
                REQUIRED_COMPARE_ERROR_SECTIONS,
                severity="error",
            )
            self._check_required_sections(
                result,
                report_text,
                REQUIRED_COMPARE_WARNING_SECTIONS,
                severity="warning",
            )
        elif resolved_report_type == "profile":
            self._check_required_sections(
                result,
                report_text,
                REQUIRED_PROFILE_ERROR_SECTIONS,
                severity="error",
            )

        for pattern in FORBIDDEN_CLAIM_PATTERNS:
            if self._has_forbidden_claim(report_text, pattern):
                result.issues.append(
                    LLMAuditIssue(
                        "forbidden_claim",
                        f"LLM 报告出现越权判断措辞：{pattern}。",
                    )
                )

        unique_points = prompt_json.get("unique_points") if isinstance(prompt_json, dict) else None
        if (
            resolved_report_type == "compare"
            and unique_points == []
            and "当前证据不足，未自动确认创新点" not in report_text
        ):
            result.issues.append(
                LLMAuditIssue(
                    "missing_uncertain_unique_statement",
                    "prompt 中没有确认创新点，但 LLM 报告未保留“当前证据不足，未自动确认创新点”。",
                )
                )

        return result

    def _has_forbidden_claim(self, report_text: str, pattern: str) -> bool:
        for match in re.finditer(re.escape(pattern), report_text):
            window = report_text[max(0, match.start() - 8) : match.end() + 8]
            if any(context in window for context in SAFE_FORBIDDEN_CLAIM_CONTEXTS):
                continue
            return True
        return False

    def _resolve_report_type(self, prompt_json: dict[str, Any], requested: str) -> str:
        if requested != "auto":
            return requested
        keys = set(prompt_json.keys()) if isinstance(prompt_json, dict) else set()
        if keys & COMPARE_HINT_KEYS:
            return "compare"
        if keys & PROFILE_HINT_KEYS:
            return "profile"
        return "compare"

    def _check_required_sections(
        self,
        result: LLMAuditResult,
        report_text: str,
        sections: tuple[str, ...],
        *,
        severity: str,
    ) -> None:
        for section in sections:
            if section not in report_text:
                result.issues.append(
                    LLMAuditIssue(
                        "missing_section",
                        f"LLM 报告缺少建议章节或关键词：{section}。",
                        severity=severity,
                    )
                )

    def _reference_allowed(self, file: str, line_start: int, line_end: int, evidence_ranges: list[EvidenceRange]) -> bool:
        ranges = sorted(
            ((evidence.line_start, evidence.line_end) for evidence in evidence_ranges if evidence.file == file),
            key=lambda item: item[0],
        )
        if not ranges:
            return False
        merged: list[tuple[int, int]] = []
        for start, end in ranges:
            if not merged or start > merged[-1][1] + 1:
                merged.append((start, end))
            else:
                merged[-1] = (merged[-1][0], max(merged[-1][1], end))
        return any(start <= line_start <= line_end <= end for start, end in merged)

    def _extract_prompt_json(self, prompt_text: str, result: LLMAuditResult) -> dict[str, Any]:
        match = JSON_BLOCK_RE.search(prompt_text)
        if not match:
            result.issues.append(LLMAuditIssue("missing_prompt_json", "prompt 中没有找到 JSON 代码块。"))
            return {}
        try:
            data = json.loads(match.group("json"))
        except json.JSONDecodeError as exc:
            result.issues.append(LLMAuditIssue("invalid_prompt_json", f"prompt JSON 无法解析：{exc}。"))
            return {}
        return data if isinstance(data, dict) else {}

    def _extract_evidence_ranges(self, value: Any) -> list[EvidenceRange]:
        ranges: list[EvidenceRange] = []

        def walk(item: Any) -> None:
            if isinstance(item, dict):
                if {"file", "line_start", "line_end"}.issubset(item):
                    try:
                        ranges.append(
                            EvidenceRange(
                                file=str(item["file"]),
                                line_start=int(item["line_start"]),
                                line_end=int(item["line_end"]),
                            )
                        )
                    except (TypeError, ValueError):
                        pass
                for child in item.values():
                    walk(child)
            elif isinstance(item, list):
                for child in item:
                    walk(child)

        walk(value)
        return ranges

    def _extract_report_refs(self, report_text: str) -> list[tuple[str, int, int]]:
        refs: list[tuple[str, int, int]] = []
        for match in REF_RE.finditer(report_text):
            start = int(match.group("start"))
            end = int(match.group("end") or match.group("start"))
            refs.append((match.group("file").replace("\\", "/"), start, end))
        return refs
