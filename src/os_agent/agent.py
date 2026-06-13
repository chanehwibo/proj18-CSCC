"""Agent workflow orchestration."""

from __future__ import annotations

from dataclasses import replace
from pathlib import PurePosixPath

from .analyzer import DIMENSIONS
from .models import CompareResult, Evidence, Finding, KernelProfile, SymbolDef
from .similarity import CodeSimilarityDetector

LOW_VALUE_PATH_NAMES = {
    "defs.h",
    "types.h",
    "param.h",
    "config.h",
    "lib.rs",
    "mod.rs",
    "main.c",
    "main.rs",
}
LOW_VALUE_SYMBOL_NAMES = {
    "init",
    "main",
    "start",
    "end",
    "panic",
    "printf",
    "print",
    "debug",
    "test",
    "true",
    "false",
}
MAX_CODE_SIMILARITY_POINTS = 30
MAX_CODE_SIMILARITY_POINTS_PER_CATEGORY = 6


class CompareAgent:
    def __init__(self, similarity_detector: CodeSimilarityDetector | None = None):
        self.similarity_detector = similarity_detector or CodeSimilarityDetector()

    def compare(self, new_profile: KernelProfile, history_profiles: list[KernelProfile], limit: int = 3) -> CompareResult:
        selected = history_profiles[:limit]
        result = CompareResult(
            new_repo=new_profile.meta.name,
            history_repos=[profile.meta.name for profile in selected],
            evidence_roots=self._evidence_roots([new_profile, *selected]),
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
            evidence = (
                self._tag_evidence_list(new_finding.evidence[:2], new_profile)
                + self._tag_evidence_list(hist_finding.evidence[:2], history)
            )
            statement = (
                f"与 {history.meta.name} 在“{dim_title}”维度存在功能重合："
                "双方均有可追溯源码证据，属于需要重点复核的相似实现线索。"
            )
            result.overlap_points.append(Finding(statement, confidence="medium", evidence=evidence))
            self._append_code_similarity(result, new_profile, history, dim, dim_title)
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
                    evidence=self._tag_evidence_list(new_finding.evidence[:2], new_profile),
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

    def _append_code_similarity(
        self,
        result: CompareResult,
        new_profile: KernelProfile,
        history: KernelProfile,
        dim: str,
        dim_title: str,
    ) -> None:
        new_evidence = self._dimension_evidence(new_profile, dim, limit=8)
        history_evidence = self._dimension_evidence(history, dim, limit=8)
        self._append_path_overlap(result, history, dim_title, new_evidence, history_evidence)
        self._append_symbol_overlap(result, new_profile, history, dim, dim_title, {"fn"}, "函数/符号名重合")
        self._append_symbol_overlap(result, new_profile, history, dim, dim_title, {"struct", "enum", "trait"}, "结构体/类型重合")
        self._append_symbol_overlap(result, new_profile, history, dim, dim_title, {"macro"}, "宏名重合")
        matches = self.similarity_detector.compare_evidence(new_evidence, history_evidence, limit=2)
        for match in matches:
            statement = (
                f"与 {history.meta.name} 在“{dim_title}”维度发现片段级代码相似度 {match.score:.2f} "
                f"（token={match.token_score:.2f}, structure={match.structure_score:.2f}）。"
                "这属于代码级相似线索，不等同于抄袭结论，需要人工结合完整文件和提交历史复核。"
            )
            if match.shared_tokens:
                statement += f" 共同 token：{', '.join(match.shared_tokens[:8])}。"
            result.code_similarity_points.append(
                Finding(
                    statement,
                    confidence=match.confidence,
                    evidence=[match.left, match.right],
                )
            )

    def _append_path_overlap(
        self,
        result: CompareResult,
        history: KernelProfile,
        dim_title: str,
        new_evidence: list[Evidence],
        history_evidence: list[Evidence],
    ) -> None:
        pairs = self._path_overlap_pairs(new_evidence, history_evidence, limit=2)
        for left, right, match_kind in pairs:
            statement = (
                f"文件路径重合：与 {history.meta.name} 在“{dim_title}”维度出现{match_kind}源码路径 "
                f"`{left.file}` / `{right.file}`。"
                "这说明实现位置或文件命名存在可复核相似线索，不等同于代码重复裁定。"
            )
            confidence = "high" if match_kind == "同路径" else "medium"
            result.code_similarity_points.append(Finding(statement, confidence=confidence, evidence=[left, right]))

    def _append_symbol_overlap(
        self,
        result: CompareResult,
        new_profile: KernelProfile,
        history: KernelProfile,
        dim: str,
        dim_title: str,
        kinds: set[str],
        label: str,
    ) -> None:
        pairs = self._symbol_overlap_pairs(
            self._dimension_symbols(new_profile, dim, kinds, limit=120),
            self._dimension_symbols(history, dim, kinds, limit=120),
            limit=4,
        )
        if not pairs:
            return
        names = ", ".join(left.name for left, _ in pairs)
        statement = (
            f"{label}：与 {history.meta.name} 在“{dim_title}”维度发现 {len(pairs)} 个同名定义：{names}。"
            "该结果表示命名和局部结构存在可复核相似线索，不直接表示代码复制。"
        )
        evidence: list[Evidence] = []
        for left, right in pairs[:2]:
            evidence.extend([self._symbol_evidence(left, new_profile), self._symbol_evidence(right, history)])
        confidence = "high" if len(pairs) >= 3 else "medium"
        result.code_similarity_points.append(Finding(statement, confidence=confidence, evidence=evidence))

    def _dimension_evidence(self, profile: KernelProfile, dim: str, limit: int) -> list[Evidence]:
        evidence: list[Evidence] = []
        for finding in profile.dimensions.get(dim, []):
            if finding.confidence == "unconfirmed":
                continue
            evidence.extend(self._tag_evidence_list(finding.evidence, profile))
            if len(evidence) >= limit:
                break
        return evidence[:limit]

    def _path_overlap_pairs(self, left_items: list[Evidence], right_items: list[Evidence], limit: int) -> list[tuple[Evidence, Evidence, str]]:
        pairs: list[tuple[Evidence, Evidence, str]] = []
        seen: set[tuple[str, str]] = set()
        for left in left_items:
            left_parts = self._path_parts(left.file)
            if not left_parts or left_parts[-1] in LOW_VALUE_PATH_NAMES:
                continue
            for right in right_items:
                right_parts = self._path_parts(right.file)
                if not right_parts or right_parts[-1] in LOW_VALUE_PATH_NAMES:
                    continue
                if left_parts == right_parts:
                    match_kind = "同路径"
                elif left_parts[-1] == right_parts[-1]:
                    match_kind = "同名文件"
                else:
                    continue
                key = (left.file, right.file)
                if key in seen:
                    continue
                seen.add(key)
                pairs.append((left, right, match_kind))
                if len(pairs) >= limit:
                    return pairs
        return pairs

    def _path_parts(self, path: str) -> tuple[str, ...]:
        normalized = path.replace("\\", "/").lower()
        return PurePosixPath(normalized).parts

    def _dimension_symbols(self, profile: KernelProfile, dim: str, kinds: set[str], limit: int) -> list[SymbolDef]:
        evidence_files = {evidence.file for evidence in self._dimension_evidence(profile, dim, limit=20)}
        spec = DIMENSIONS.get(dim, {})
        hint_words = [word.lower() for word in spec.get("hints", []) + spec.get("keywords", [])]
        symbols: list[SymbolDef] = []
        for symbol in profile.symbols:
            if symbol.kind not in kinds:
                continue
            normalized = self._normalize_symbol_name(symbol.name)
            if self._is_low_value_symbol(normalized):
                continue
            haystack = f"{symbol.name} {symbol.file} {symbol.signature}".lower()
            if symbol.file in evidence_files or any(word and word.lower() in haystack for word in hint_words):
                symbols.append(symbol)
                if len(symbols) >= limit:
                    break
        return symbols

    def _symbol_overlap_pairs(self, left_symbols: list[SymbolDef], right_symbols: list[SymbolDef], limit: int) -> list[tuple[SymbolDef, SymbolDef]]:
        right_by_name: dict[str, SymbolDef] = {}
        for symbol in right_symbols:
            right_by_name.setdefault(self._normalize_symbol_name(symbol.name), symbol)
        pairs: list[tuple[SymbolDef, SymbolDef]] = []
        seen: set[str] = set()
        for left in left_symbols:
            name = self._normalize_symbol_name(left.name)
            if name in seen or name not in right_by_name:
                continue
            seen.add(name)
            pairs.append((left, right_by_name[name]))
            if len(pairs) >= limit:
                break
        return pairs

    def _normalize_symbol_name(self, name: str) -> str:
        return name.strip().lower()

    def _is_low_value_symbol(self, name: str) -> bool:
        return len(name) < 3 or name in LOW_VALUE_SYMBOL_NAMES

    def _symbol_evidence(self, symbol: SymbolDef, profile: KernelProfile) -> Evidence:
        return Evidence(
            file=symbol.file,
            line_start=symbol.line_start,
            line_end=symbol.line_end,
            snippet=symbol.signature,
            kind="code",
            note=f"{symbol.kind} {symbol.name}",
            repo_id=self._repo_id(profile),
        )

    def _tag_evidence_list(self, evidences: list[Evidence], profile: KernelProfile) -> list[Evidence]:
        repo_id = self._repo_id(profile)
        return [replace(evidence, repo_id=evidence.repo_id or repo_id) for evidence in evidences]

    def _evidence_roots(self, profiles: list[KernelProfile]) -> dict[str, str]:
        roots: dict[str, str] = {}
        for profile in profiles:
            repo_id = self._repo_id(profile)
            if repo_id and profile.meta.root_path:
                roots[repo_id] = profile.meta.root_path
        return roots

    def _repo_id(self, profile: KernelProfile) -> str:
        return profile.meta.repo_id or profile.meta.name

    def _first_confirmed(self, profile: KernelProfile, dim: str) -> Finding | None:
        for finding in profile.dimensions.get(dim, []):
            if finding.confidence != "unconfirmed":
                return finding
        return None

    def _dedupe(self, result: CompareResult) -> None:
        for attr in ("overlap_points", "code_similarity_points", "similarities", "differences", "unique_points"):
            seen: set[str] = set()
            deduped = []
            for finding in getattr(result, attr):
                if finding.statement in seen:
                    continue
                seen.add(finding.statement)
                deduped.append(finding)
            setattr(result, attr, deduped)
        result.code_similarity_points = self._trim_code_similarity_points(result.code_similarity_points)

    def _trim_code_similarity_points(self, findings: list[Finding]) -> list[Finding]:
        ranked = sorted(
            enumerate(findings),
            key=lambda item: (-self._code_similarity_rank(item[1]), item[0]),
        )
        kept: list[Finding] = []
        category_counts: dict[str, int] = {}
        for _, finding in ranked:
            category = self._code_similarity_category(finding)
            if category_counts.get(category, 0) >= MAX_CODE_SIMILARITY_POINTS_PER_CATEGORY:
                continue
            kept.append(finding)
            category_counts[category] = category_counts.get(category, 0) + 1
            if len(kept) >= MAX_CODE_SIMILARITY_POINTS:
                break
        return kept

    def _code_similarity_rank(self, finding: Finding) -> int:
        confidence_score = {"high": 30, "medium": 20, "low": 10}.get(finding.confidence, 0)
        statement = finding.statement
        if "片段级代码相似度" in statement:
            return confidence_score + 50
        if "函数/符号名重合" in statement:
            return confidence_score + 40
        if "宏名重合" in statement:
            return confidence_score + 35
        if "结构体/类型重合" in statement:
            return confidence_score + 30
        if "文件路径重合" in statement:
            return confidence_score + 20
        return confidence_score

    def _code_similarity_category(self, finding: Finding) -> str:
        statement = finding.statement
        if "片段级代码相似度" in statement:
            return "snippet"
        if "函数/符号名重合" in statement:
            return "function"
        if "宏名重合" in statement:
            return "macro"
        if "结构体/类型重合" in statement:
            return "type"
        if "文件路径重合" in statement:
            return "path"
        return "other"
