"""History repository selection for comparison tasks."""

from __future__ import annotations

import math
from dataclasses import dataclass

from .models import KernelProfile


@dataclass(frozen=True)
class RankedProfile:
    profile: KernelProfile
    score: float
    reasons: list[str]


class HistorySelector:
    """Rank history profiles by OS-profile similarity instead of directory order."""

    def select(self, target: KernelProfile, candidates: list[KernelProfile], limit: int) -> list[RankedProfile]:
        ranked = [self.rank_one(target, candidate) for candidate in candidates]
        ranked.sort(key=lambda item: (-item.score, item.profile.meta.repo_id))
        return ranked[:limit]

    def rank_one(self, target: KernelProfile, candidate: KernelProfile) -> RankedProfile:
        score = 0.0
        reasons: list[str] = []

        if target.meta.style != "unknown" and target.meta.style == candidate.meta.style:
            score += 3.0
            reasons.append(f"同属 {target.meta.style} 风格")

        arch_score = self._jaccard(set(target.meta.arch), set(candidate.meta.arch))
        if arch_score:
            score += arch_score * 2.0
            reasons.append(f"架构重合度 {arch_score:.2f}")

        lang_score = self._language_similarity(target, candidate)
        if lang_score:
            score += lang_score * 2.0
            reasons.append(f"语言构成相似度 {lang_score:.2f}")

        dim_score = self._dimension_similarity(target, candidate)
        if dim_score:
            score += dim_score * 4.0
            reasons.append(f"OS 维度重合度 {dim_score:.2f}")

        size_score = self._size_similarity(target.meta.loc_total, candidate.meta.loc_total)
        if size_score:
            score += size_score
            reasons.append(f"代码规模接近度 {size_score:.2f}")

        if not reasons:
            reasons.append("未发现明显画像相似特征")
        return RankedProfile(profile=candidate, score=score, reasons=reasons)

    def _dimension_similarity(self, left: KernelProfile, right: KernelProfile) -> float:
        return self._jaccard(self._confirmed_dims(left), self._confirmed_dims(right))

    def _confirmed_dims(self, profile: KernelProfile) -> set[str]:
        return {
            dim
            for dim, findings in profile.dimensions.items()
            if any(finding.confidence != "unconfirmed" for finding in findings)
        }

    def _language_similarity(self, left: KernelProfile, right: KernelProfile) -> float:
        left_total = sum(left.meta.languages.values())
        right_total = sum(right.meta.languages.values())
        if not left_total or not right_total:
            return 0.0
        langs = set(left.meta.languages) | set(right.meta.languages)
        overlap = 0.0
        for lang in langs:
            left_ratio = left.meta.languages.get(lang, 0) / left_total
            right_ratio = right.meta.languages.get(lang, 0) / right_total
            overlap += min(left_ratio, right_ratio)
        return overlap

    def _size_similarity(self, left_loc: int, right_loc: int) -> float:
        if left_loc <= 0 or right_loc <= 0:
            return 0.0
        ratio = max(left_loc, right_loc) / min(left_loc, right_loc)
        return 1.0 / (1.0 + math.log(ratio))

    def _jaccard(self, left: set[str], right: set[str]) -> float:
        if not left or not right:
            return 0.0
        return len(left & right) / len(left | right)
