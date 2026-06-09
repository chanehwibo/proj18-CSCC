"""Agent workflow orchestration."""

from __future__ import annotations

from .analyzer import DIMENSIONS
from .models import CompareResult, Finding, KernelProfile


class CompareAgent:
    def compare(self, new_profile: KernelProfile, history_profiles: list[KernelProfile], limit: int = 3) -> CompareResult:
        selected = history_profiles[:limit]
        result = CompareResult(
            new_repo=new_profile.meta.name,
            history_repos=[profile.meta.name for profile in selected],
        )
        if not selected:
            result.differences.append(Finding("未提供历史仓库，无法进行比较。", confidence="unconfirmed"))
            return result

        for history in selected:
            self._compare_one(new_profile, history, result)
        self._dedupe(result)
        return result

    def _compare_one(self, new_profile: KernelProfile, history: KernelProfile, result: CompareResult) -> None:
        if new_profile.meta.style == history.meta.style and new_profile.meta.style != "unknown":
            result.similarities.append(Finding(
                f"与 {history.meta.name} 同属 {new_profile.meta.style} 风格。",
                confidence="medium",
            ))

        shared_dims: list[str] = []
        new_dims = set(new_profile.dimensions)
        hist_dims = set(history.dimensions)
        for dim in sorted(new_dims & hist_dims):
            new_finding = self._first_confirmed(new_profile, dim)
            hist_finding = self._first_confirmed(history, dim)
            if not new_finding or not hist_finding:
                continue

            shared_dims.append(dim)
            dim_title = DIMENSIONS.get(dim, {}).get("title", dim)
            evidence = new_finding.evidence[:2] + hist_finding.evidence[:2]
            statement = (
                f"与 {history.meta.name} 在“{dim_title}”维度存在功能重合："
                "双方均有可追溯源码证据，属于需要重点复核的相似实现线索。"
            )
            result.overlap_points.append(Finding(statement, confidence="medium", evidence=evidence))
            result.similarities.append(Finding(
                f"与 {history.meta.name} 在“{dim_title}”维度均有可确认实现。",
                confidence="medium",
                evidence=evidence[:2],
            ))

        if shared_dims:
            result.similarities.append(Finding(
                f"与 {history.meta.name} 在 {', '.join(shared_dims)} 等维度均有可确认实现，可作为进一步人工复核重点。",
                confidence="medium",
            ))

        for dim in sorted(new_dims):
            new_finding = self._first_confirmed(new_profile, dim)
            hist_finding = self._first_confirmed(history, dim)
            if new_finding and not hist_finding:
                dim_title = DIMENSIONS.get(dim, {}).get("title", dim)
                result.unique_points.append(Finding(
                    f"新项目在“{dim_title}”维度有可确认实现，而历史样本 {history.meta.name} 当前未确认该维度。",
                    confidence="low",
                    evidence=new_finding.evidence[:2],
                ))

        for dim in sorted(new_dims - hist_dims):
            result.unique_points.append(Finding(
                f"新项目包含历史样本 {history.meta.name} 中未建模的维度：{dim}。",
                confidence="low",
            ))

        if new_profile.meta.languages != history.meta.languages:
            result.differences.append(Finding(
                f"与 {history.meta.name} 的语言构成不同：新项目为 {new_profile.meta.languages}，历史项目为 {history.meta.languages}。",
                confidence="medium",
            ))

    def _first_confirmed(self, profile: KernelProfile, dim: str) -> Finding | None:
        for finding in profile.dimensions.get(dim, []):
            if finding.confidence != "unconfirmed":
                return finding
        return None

    def _dedupe(self, result: CompareResult) -> None:
        for attr in ("overlap_points", "similarities", "differences", "unique_points"):
            seen: set[str] = set()
            deduped = []
            for finding in getattr(result, attr):
                if finding.statement in seen:
                    continue
                seen.add(finding.statement)
                deduped.append(finding)
            setattr(result, attr, deduped)
