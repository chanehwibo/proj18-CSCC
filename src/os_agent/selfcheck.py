"""Lightweight evidence self-check utilities."""

from __future__ import annotations

from pathlib import Path

from .models import CompareResult, Evidence, Finding, KernelProfile


class EvidenceChecker:
    """Check whether key findings are backed by readable local evidence."""

    def profile_summary(self, profile: KernelProfile) -> dict[str, int | float]:
        findings = self._profile_findings(profile)
        return self._summary(findings, Path(profile.meta.root_path))

    def compare_summary(self, result: CompareResult, evidence_root: Path | None = None) -> dict[str, int | float]:
        findings = result.overlap_points + result.similarities + result.differences + result.unique_points
        return self._summary(findings, evidence_root)

    def invalid_evidence(self, findings: list[Finding], root: Path | None = None) -> list[Evidence]:
        invalid: list[Evidence] = []
        for finding in findings:
            for evidence in finding.evidence:
                if not self._evidence_exists(evidence, root):
                    invalid.append(evidence)
        return invalid

    def _profile_findings(self, profile: KernelProfile) -> list[Finding]:
        findings: list[Finding] = []
        if profile.build_system:
            findings.append(profile.build_system)
        for dim_findings in profile.dimensions.values():
            findings.extend(dim_findings)
        return findings

    def _summary(self, findings: list[Finding], root: Path | None) -> dict[str, int | float]:
        key_findings = [finding for finding in findings if self._is_key_finding(finding)]
        with_evidence = [finding for finding in key_findings if finding.evidence]
        invalid = self.invalid_evidence(key_findings, root)
        coverage = (len(with_evidence) / len(key_findings) * 100) if key_findings else 0.0
        return {
            "key_findings": len(key_findings),
            "with_evidence": len(with_evidence),
            "coverage": coverage,
            "invalid_evidence": len(invalid),
            "unconfirmed": sum(1 for finding in findings if finding.confidence == "unconfirmed"),
        }

    def _evidence_exists(self, evidence: Evidence, root: Path | None) -> bool:
        if not evidence.file:
            return False
        if root is None:
            return True
        path = root / evidence.file
        if not path.exists():
            return False
        try:
            line_count = len(path.read_text(encoding="utf-8", errors="ignore").splitlines())
        except OSError:
            return False
        return 1 <= evidence.line_start <= evidence.line_end <= max(line_count, 1)

    def _is_key_finding(self, finding: Finding) -> bool:
        if finding.confidence == "unconfirmed":
            return False
        statement = finding.statement
        meta_markers = (
            "同属",
            "语言构成不同",
            "等维度均有可确认实现",
            "鍚屽睘",
            "璇█鏋勬垚涓嶅悓",
            "绛夌淮搴﹀潎鏈夊彲纭瀹炵幇",
        )
        return not any(marker in statement for marker in meta_markers)
