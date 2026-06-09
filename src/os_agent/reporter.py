"""Report generation utilities."""

from __future__ import annotations

from .analyzer import DIMENSIONS
from .models import CompareResult, Evidence, Finding, KernelProfile
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
            lines.extend(self._render_dimension_review(dim, spec, profile.dimensions.get(dim, [])))
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

        lines.extend([
            "## 功能重合与疑似重复证据",
            "",
            "本节只说明功能维度和实现线索的重合，不直接判定代码抄袭。是否构成代码级重复，需要结合完整代码、提交历史和人工复核进一步确认。",
            "",
        ])
        lines.extend(self._render_findings_or_empty(result.overlap_points))
        lines.extend(["", "## 相似点", ""])
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

    def _render_dimension_review(self, dim: str, spec: dict, findings: list[Finding]) -> list[str]:
        confirmed = [finding for finding in findings if finding.confidence != "unconfirmed"]
        evidence_items = [ev for finding in confirmed for ev in finding.evidence]
        status = "已确认" if confirmed else "未确认"
        confidence = self._dimension_confidence(confirmed)
        lines = [
            f"- 结论：{status}该维度存在可追溯实现线索。（综合置信度：{confidence}）",
            f"- 分析口径：本维度主要关注 `{dim}` 相关的源码路径、符号定义和关键词证据；文档命中不直接作为实现证据。",
        ]
        if confirmed:
            lines.append("- 设计判断：")
            for finding in confirmed:
                lines.append(f"  - {finding.statement}（置信度：{finding.confidence}）")
        else:
            lines.append(f"- 设计判断：当前未在核心源码路径中确认 {spec['title']} 的实现证据。")

        if evidence_items:
            lines.extend(["", "### 证据表", ""])
            lines.extend(self._evidence_table(evidence_items[:6]))
            lines.extend(["", "### 关键代码片段", ""])
            for ev in evidence_items[:4]:
                lines.extend(self._render_evidence(ev))
        else:
            lines.extend([
                "",
                "### 证据表",
                "",
                "| 证据 | 说明 |",
                "| --- | --- |",
                "| 未确认 | 当前未找到可引用的源码证据 |",
            ])

        symbols = self._symbol_summary(findings)
        if symbols:
            lines.extend(["", "### 相关符号", "", symbols])

        lines.extend(["", "### 复核建议", ""])
        if confirmed:
            lines.append("- 建议人工检查上述代码片段所在文件，确认关键词命中是否确实对应完整机制，而不是仅出现名称或注释。")
        else:
            lines.append("- 建议人工补查目录命名不典型的源码文件，或在后续版本中扩展该维度关键词。")
        return lines

    def _dimension_confidence(self, findings: list[Finding]) -> str:
        if any(finding.confidence == "high" for finding in findings):
            return "high"
        if any(finding.confidence == "medium" for finding in findings):
            return "medium"
        if findings:
            return findings[0].confidence
        return "unconfirmed"

    def _evidence_table(self, evidences: list[Evidence]) -> list[str]:
        lines = ["| 文件 | 行号 | 说明 |", "| --- | --- | --- |"]
        for ev in evidences:
            lines.append(f"| `{ev.file}` | L{ev.line_start}-L{ev.line_end} | {ev.note or ev.kind} |")
        return lines

    def _symbol_summary(self, findings: list[Finding]) -> str:
        symbols: list[str] = []
        for finding in findings:
            if "符号" not in finding.statement and "symbol" not in finding.statement.lower():
                continue
            for ev in finding.evidence:
                if ev.note:
                    symbols.append(f"`{ev.note}` at `{ev.file}:L{ev.line_start}`")
        return "、".join(symbols[:8])

    def _render_finding(self, finding: Finding) -> list[str]:
        lines = [f"- {finding.statement}（置信度：{finding.confidence}）"]
        if finding.evidence:
            lines.append("  证据：")
            for ev in finding.evidence:
                lines.extend(self._render_evidence(ev))
        return lines

    def _render_evidence(self, ev: Evidence) -> list[str]:
        lines = [f"  - `{ev.file}:L{ev.line_start}-L{ev.line_end}`：{ev.note or ev.kind}"]
        snippet = self._compact_snippet(ev.snippet)
        if snippet:
            lines.append(f"    代码片段：`{snippet}`")
        return lines

    def _compact_snippet(self, snippet: str, limit: int = 180) -> str:
        text = " ".join(line.strip() for line in snippet.splitlines() if line.strip())
        text = text.replace("`", "'")
        if len(text) > limit:
            return text[: limit - 3].rstrip() + "..."
        return text

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
