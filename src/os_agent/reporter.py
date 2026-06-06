"""Report generation utilities."""

from __future__ import annotations

from .analyzer import DIMENSIONS
from .models import CompareResult, Finding, KernelProfile
from .selfcheck import EvidenceChecker


class Reporter:
    def __init__(self):
        self.checker = EvidenceChecker()

    def render_profile(self, profile: KernelProfile) -> str:
        lines = [
            f"# {profile.meta.name} 项目描述报告",
            "",
            "## 基本信息",
            "",
            f"- 仓库 ID：`{profile.meta.repo_id}`",
            f"- 风格：{profile.meta.style}",
            f"- 架构：{', '.join(profile.meta.arch) if profile.meta.arch else '未确认'}",
            f"- 文件数：{profile.meta.file_count}",
            f"- 代码/文本行数：{profile.meta.loc_total}",
            f"- 主要语言：{self._lang_summary(profile)}",
            "",
            "## 总览",
            "",
            profile.overview,
            "",
            "## 构建系统",
            "",
            self._finding_text(profile.build_system),
            "",
        ]
        for dim, spec in DIMENSIONS.items():
            lines.extend([f"## {spec['title']}", ""])
            for finding in profile.dimensions.get(dim, []):
                lines.extend(self._render_finding(finding))
            lines.append("")
        lines.extend(self._check_summary(profile))
        return "\n".join(lines).rstrip() + "\n"

    def render_compare(self, result: CompareResult) -> str:
        lines = [
            f"# {result.new_repo} 比较报告",
            "",
            f"- 对比历史仓库：{', '.join(result.history_repos)}",
            f"- 生成时间：{result.generated_at}",
            "",
        ]
        if result.selection_notes:
            lines.extend(["## 历史样本选择", ""])
            for note in result.selection_notes:
                lines.append(f"- {note}")
            lines.append("")
        lines.extend(["## 相似点", ""])
        lines.extend(self._render_findings_or_empty(result.similarities))
        lines.extend(["", "## 差异点", ""])
        lines.extend(self._render_findings_or_empty(result.differences))
        lines.extend(["", "## 可能创新点", ""])
        lines.extend(self._render_findings_or_empty(result.unique_points))
        lines.extend(["", "## 附录：核验摘要", ""])
        summary = self.checker.compare_summary(result)
        lines.extend(self._summary_lines(summary))
        return "\n".join(lines).rstrip() + "\n"

    def _render_findings_or_empty(self, findings: list[Finding]) -> list[str]:
        if not findings:
            return ["- 未确认。"]
        lines: list[str] = []
        for finding in findings:
            lines.extend(self._render_finding(finding))
        return lines

    def _render_finding(self, finding: Finding) -> list[str]:
        lines = [f"- {finding.statement}（置信度：{finding.confidence}）"]
        if finding.evidence:
            lines.append("  证据：")
            for ev in finding.evidence:
                lines.append(f"  - `{ev.file}:L{ev.line_start}-L{ev.line_end}`：{ev.note}")
        return lines

    def _finding_text(self, finding: Finding | None) -> str:
        if not finding:
            return "未确认。"
        return "\n".join(self._render_finding(finding))

    def _lang_summary(self, profile: KernelProfile) -> str:
        items = sorted(profile.meta.languages.items(), key=lambda item: -item[1])[:5]
        return ", ".join(f"{k} {v} LOC" for k, v in items) if items else "未识别"

    def _check_summary(self, profile: KernelProfile) -> list[str]:
        summary = self.checker.profile_summary(profile)
        return [
            "## 附录：核验摘要",
            "",
            *self._summary_lines(summary),
        ]

    def _summary_lines(self, summary: dict[str, int | float]) -> list[str]:
        return [
            f"- 关键结论数：{summary['key_findings']}",
            f"- 含证据关键结论数：{summary['with_evidence']}（{summary['coverage']:.1f}%）",
            f"- 无效证据引用数：{summary['invalid_evidence']}",
            f"- 未确认结论数：{summary['unconfirmed']}",
            "- 统计口径：关键结论指需要源码证据支撑的设计判断；语言构成、风格标签和汇总性描述不计入证据率。",
        ]
