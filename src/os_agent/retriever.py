"""Evidence retrieval utilities."""

from __future__ import annotations

import re
from dataclasses import asdict, dataclass, field

from .analyzer import DIMENSIONS, KERNEL_PATH_HINTS, LOW_PRIORITY_PATH_HINTS, SUPPORT_PATH_HINTS
from .indexer import EvidenceIndex, SourceDocument


QUERY_SPLIT_RE = re.compile(r"[\s,，/、;；|]+")

DIMENSION_ALIASES = {
    "调度": "scheduler",
    "调度器": "scheduler",
    "任务": "scheduler",
    "线程": "scheduler",
    "进程": "scheduler",
    "scheduler": "scheduler",
    "schedule": "scheduler",
    "内存": "memory",
    "页表": "memory",
    "分页": "memory",
    "物理页": "memory",
    "虚拟内存": "memory",
    "page table": "memory",
    "pagetable": "memory",
    "pte": "memory",
    "系统调用": "syscall",
    "syscall": "syscall",
    "ecall": "syscall",
    "文件系统": "filesystem",
    "文件": "filesystem",
    "vfs": "filesystem",
    "inode": "filesystem",
    "同步": "sync",
    "锁": "sync",
    "互斥": "sync",
    "mutex": "sync",
    "spinlock": "sync",
    "中断": "interrupt",
    "异常": "interrupt",
    "trap": "interrupt",
    "irq": "interrupt",
    "驱动": "driver",
    "设备": "driver",
    "driver": "driver",
    "uart": "driver",
    "virtio": "driver",
}


@dataclass
class QueryPlan:
    query: str
    raw_terms: list[str]
    expanded_terms: list[str]
    dimensions: list[str]

    @property
    def terms(self) -> list[str]:
        seen: set[str] = set()
        terms: list[str] = []
        for term in self.raw_terms + self.expanded_terms:
            normalized = term.lower().strip()
            if len(normalized) < 2 or normalized in seen:
                continue
            seen.add(normalized)
            terms.append(normalized)
        return terms


@dataclass
class EvidenceHit:
    repo_id: str
    repo_name: str
    source_tier: str
    award_level: str | None
    file: str
    line_start: int
    line_end: int
    lang: str
    score: float
    matched_terms: list[str]
    snippet: str

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class EvidenceQueryResult:
    query: str
    repo_count: int
    file_count: int
    hits: list[EvidenceHit] = field(default_factory=list)
    skipped_repos: list[str] = field(default_factory=list)
    skipped_files: int = 0

    def to_dict(self) -> dict:
        return {
            "query": self.query,
            "summary": {
                "repos": self.repo_count,
                "files": self.file_count,
                "hits": len(self.hits),
                "skipped_repos": len(self.skipped_repos),
                "skipped_files": self.skipped_files,
            },
            "skipped_repos": self.skipped_repos,
            "hits": [hit.to_dict() for hit in self.hits],
        }


class EvidenceRetriever:
    def query_terms(self, query: str) -> list[str]:
        return self._build_plan(query).terms

    def query(self, index: EvidenceIndex, query: str, *, limit: int = 10) -> EvidenceQueryResult:
        plan = self._build_plan(query)
        result = EvidenceQueryResult(
            query=query,
            repo_count=index.repo_count,
            file_count=index.file_count,
            skipped_repos=index.skipped_repos,
            skipped_files=index.skipped_files,
        )
        if not plan.terms:
            return result

        hits: list[EvidenceHit] = []
        for document in index.documents:
            hits.extend(self._query_document(document, plan))
        hits.sort(key=lambda hit: (-hit.score, hit.repo_id.lower(), hit.file.lower(), hit.line_start))
        result.hits = hits[: max(0, limit)]
        return result

    def _build_plan(self, query: str) -> QueryPlan:
        lowered = query.lower()
        raw_terms = [term.strip().lower() for term in QUERY_SPLIT_RE.split(lowered) if term.strip()]
        dimensions = []
        for alias, dimension in DIMENSION_ALIASES.items():
            if alias in lowered and dimension not in dimensions:
                dimensions.append(dimension)

        expanded: list[str] = []
        for dimension in dimensions:
            spec = DIMENSIONS[dimension]
            expanded.extend(spec.get("keywords", []))
            expanded.extend(spec.get("hints", []))
            expanded.append(dimension)
            expanded.append(str(spec.get("title", "")))
        return QueryPlan(query=query, raw_terms=raw_terms, expanded_terms=expanded, dimensions=dimensions)

    def _query_document(self, document: SourceDocument, plan: QueryPlan) -> list[EvidenceHit]:
        lines = document.lines
        if not lines:
            return []
        path_terms = self._matched_terms(document.file.lower(), plan.terms)
        path_score = self._path_score(document.file.lower(), path_terms)
        candidates: list[EvidenceHit] = []
        seen_ranges: set[tuple[int, int]] = set()
        for line_no, line in enumerate(lines, start=1):
            line_terms = self._matched_terms(line.lower(), plan.terms)
            if not line_terms:
                continue
            hit = self._make_hit(document, lines, line_no, line_terms, path_terms, path_score)
            candidates.append(hit)

        candidates.sort(key=lambda hit: (-hit.score, hit.line_start))
        hits: list[EvidenceHit] = []
        for hit in candidates:
            key = (hit.line_start, hit.line_end)
            if self._overlaps_seen(key, seen_ranges):
                continue
            seen_ranges.add(key)
            hits.append(hit)

        if not hits and path_terms:
            line_no = self._first_nonempty_line(lines)
            hits.append(self._make_hit(document, lines, line_no, [], path_terms, path_score))
        return hits

    def _make_hit(
        self,
        document: SourceDocument,
        lines: list[str],
        line_no: int,
        line_terms: list[str],
        path_terms: list[str],
        path_score: float,
    ) -> EvidenceHit:
        start = max(1, line_no - 2)
        end = min(len(lines), line_no + 2)
        matched_terms = self._ordered_terms(line_terms + path_terms)
        score = self._line_score(line_terms, path_terms) + path_score
        return EvidenceHit(
            repo_id=document.repo_id,
            repo_name=document.repo_name,
            source_tier=document.source_tier,
            award_level=document.award_level,
            file=document.file,
            line_start=start,
            line_end=end,
            lang=document.lang,
            score=score,
            matched_terms=matched_terms,
            snippet="\n".join(lines[start - 1:end])[:2000],
        )

    def _matched_terms(self, text: str, terms: list[str]) -> list[str]:
        return [term for term in terms if term in text]

    def _overlaps_seen(self, current: tuple[int, int], seen_ranges: set[tuple[int, int]]) -> bool:
        start, end = current
        return any(start <= seen_end and end >= seen_start for seen_start, seen_end in seen_ranges)

    def _ordered_terms(self, terms: list[str]) -> list[str]:
        seen: set[str] = set()
        ordered: list[str] = []
        for term in sorted(terms, key=lambda item: (-len(item), item)):
            if term in seen:
                continue
            seen.add(term)
            ordered.append(term)
        return ordered

    def _line_score(self, line_terms: list[str], path_terms: list[str]) -> float:
        score = 0.0
        for term in line_terms:
            score += 4.0 if len(term) >= 5 else 2.5
        score += min(3.0, len(path_terms) * 1.0)
        return score

    def _path_score(self, lowered_path: str, path_terms: list[str]) -> float:
        score = min(3.0, len(path_terms) * 1.0)
        if any(hint in lowered_path for hint in KERNEL_PATH_HINTS):
            score += 2.0
        elif any(hint in lowered_path for hint in SUPPORT_PATH_HINTS):
            score += 1.0
        if any(hint in lowered_path for hint in LOW_PRIORITY_PATH_HINTS):
            score -= 2.0
        return score

    def _first_nonempty_line(self, lines: list[str]) -> int:
        for index, line in enumerate(lines, start=1):
            if line.strip():
                return index
        return 1


def render_query_result(result: EvidenceQueryResult) -> str:
    lines = [
        f"Evidence query: {result.query}",
        f"- repos scanned: {result.repo_count}",
        f"- source files scanned: {result.file_count}",
        f"- hits: {len(result.hits)}",
    ]
    if result.skipped_repos:
        lines.append(f"- skipped repos: {len(result.skipped_repos)}")
    if result.skipped_files:
        lines.append(f"- skipped files: {result.skipped_files}")
    if not result.hits:
        lines.append("")
        lines.append("No evidence hits.")
        return "\n".join(lines) + "\n"

    lines.append("")
    for index, hit in enumerate(result.hits, start=1):
        source = hit.source_tier
        if hit.award_level:
            source = f"{source}/{hit.award_level}"
        lines.append(
            f"{index}. [{hit.score:.1f}] {hit.repo_id} ({source}) "
            f"{hit.file}:L{hit.line_start}-L{hit.line_end}"
        )
        if hit.matched_terms:
            lines.append(f"   matched: {', '.join(hit.matched_terms[:10])}")
        snippet = " ".join(line.strip() for line in hit.snippet.splitlines() if line.strip())
        if len(snippet) > 220:
            snippet = snippet[:217].rstrip() + "..."
        lines.append(f"   snippet: {snippet}")
    return "\n".join(lines) + "\n"
