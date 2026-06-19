"""Lightweight evidence self-check utilities."""

from __future__ import annotations

from pathlib import Path

from .models import CompareResult, Evidence, Finding, KernelProfile


class EvidenceChecker:
    """Check whether key findings are backed by readable local evidence."""

    def profile_summary(self, profile: KernelProfile) -> dict[str, int | float]:
        findings = self._profile_findings(profile)
        root = Path(profile.meta.root_path) if profile.meta.root_path else None
        return self._summary(findings, root, require_root=True)

    def compare_summary(self, result: CompareResult, evidence_root: Path | None = None) -> dict[str, int | float]:
        findings = (
            result.overlap_points
            + result.code_similarity_points
            + result.similarities
            + result.differences
            + result.unique_points
        )
        evidence_roots = {
            repo_id: Path(root)
            for repo_id, root in result.evidence_roots.items()
            if repo_id and root
        }
        return self._summary(
            findings,
            evidence_root,
            evidence_roots=evidence_roots,
            require_root=evidence_root is None and not evidence_roots,
        )

    def invalid_evidence(
        self,
        findings: list[Finding],
        root: Path | None = None,
        *,
        evidence_roots: dict[str, Path] | None = None,
        require_root: bool = False,
    ) -> list[Evidence]:
        invalid: list[Evidence] = []
        for finding in findings:
            for evidence in finding.evidence:
                if not self._evidence_exists(
                    evidence,
                    root,
                    evidence_roots=evidence_roots,
                    require_root=require_root,
                ):
                    invalid.append(evidence)
        return invalid

    def _profile_findings(self, profile: KernelProfile) -> list[Finding]:
        findings: list[Finding] = []
        if profile.build_system:
            findings.append(profile.build_system)
        for dim_findings in profile.dimensions.values():
            findings.extend(dim_findings)
        return findings

    def _summary(
        self,
        findings: list[Finding],
        root: Path | None,
        *,
        evidence_roots: dict[str, Path] | None = None,
        require_root: bool = False,
    ) -> dict[str, int | float]:
        key_findings = [finding for finding in findings if self._is_key_finding(finding)]
        with_evidence = [finding for finding in key_findings if finding.evidence]
        invalid = self.invalid_evidence(
            key_findings,
            root,
            evidence_roots=evidence_roots,
            require_root=require_root,
        )
        coverage = (len(with_evidence) / len(key_findings) * 100) if key_findings else 0.0
        return {
            "key_findings": len(key_findings),
            "with_evidence": len(with_evidence),
            "coverage": coverage,
            "invalid_evidence": len(invalid),
            "unconfirmed": sum(1 for finding in findings if finding.confidence == "unconfirmed"),
        }

    def _evidence_exists(
        self,
        evidence: Evidence,
        root: Path | None,
        *,
        evidence_roots: dict[str, Path] | None = None,
        require_root: bool = False,
    ) -> bool:
        if not evidence.file:
            return False
        if evidence_roots:
            if evidence.repo_id:
                repo_root = evidence_roots.get(evidence.repo_id)
                return self._path_evidence_exists(evidence, repo_root) if repo_root else False
            return any(self._path_evidence_exists(evidence, repo_root) for repo_root in evidence_roots.values())
        if root is None:
            return not require_root
        return self._path_evidence_exists(evidence, root)

    def _path_evidence_exists(self, evidence: Evidence, root: Path) -> bool:
        try:
            root = root.resolve()
            path = (root / evidence.file).resolve()
        except (OSError, RuntimeError):
            return False
        if path != root and root not in path.parents:
            return False
        if not path.exists():
            return False
        try:
            line_count = len(path.read_text(encoding="utf-8", errors="ignore").splitlines())
        except OSError:
            return False
        if line_count == 0:
            return False
        return 1 <= evidence.line_start <= evidence.line_end <= line_count

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
