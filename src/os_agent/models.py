"""Core data models for KernelSage."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


@dataclass
class Evidence:
    file: str
    line_start: int
    line_end: int
    snippet: str
    kind: str = "code"
    note: str = ""


@dataclass
class Finding:
    statement: str
    confidence: str = "medium"
    evidence: list[Evidence] = field(default_factory=list)


@dataclass
class RepoMeta:
    repo_id: str
    name: str
    root_path: str = ""
    url: str | None = None
    year: int | None = None
    team: str | None = None
    school: str | None = None
    style: str = "unknown"
    arch: list[str] = field(default_factory=list)
    languages: dict[str, int] = field(default_factory=dict)
    loc_total: int = 0
    file_count: int = 0
    commit: str | None = None
    license: str | None = None


@dataclass
class FileEntry:
    path: str
    size: int
    lang: str
    loc: int


@dataclass
class RepoSnapshot:
    meta: RepoMeta
    files: list[FileEntry]
    readme_text: str = ""
    docs_texts: dict[str, str] = field(default_factory=dict)


@dataclass
class SymbolDef:
    name: str
    kind: str
    file: str
    line_start: int
    line_end: int
    signature: str = ""


@dataclass
class ParsedRepo:
    repo_id: str
    symbols: list[SymbolDef] = field(default_factory=list)


@dataclass
class KernelProfile:
    meta: RepoMeta
    overview: str = ""
    build_system: Finding | None = None
    dimensions: dict[str, list[Finding]] = field(default_factory=dict)
    symbols: list[SymbolDef] = field(default_factory=list)
    generated_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    profile_version: str = "0.2"


@dataclass
class CompareResult:
    new_repo: str
    history_repos: list[str]
    selection_notes: list[str] = field(default_factory=list)
    overlap_points: list[Finding] = field(default_factory=list)
    code_similarity_points: list[Finding] = field(default_factory=list)
    similarities: list[Finding] = field(default_factory=list)
    differences: list[Finding] = field(default_factory=list)
    unique_points: list[Finding] = field(default_factory=list)
    generated_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


def to_dict(value: Any) -> Any:
    if hasattr(value, "__dataclass_fields__"):
        return asdict(value)
    if isinstance(value, Path):
        return str(value)
    return value


def evidence_from_dict(data: dict[str, Any]) -> Evidence:
    return Evidence(
        file=data["file"],
        line_start=data["line_start"],
        line_end=data["line_end"],
        snippet=data.get("snippet", ""),
        kind=data.get("kind", "code"),
        note=data.get("note", ""),
    )


def finding_from_dict(data: dict[str, Any]) -> Finding:
    return Finding(
        statement=data["statement"],
        confidence=data.get("confidence", "medium"),
        evidence=[evidence_from_dict(item) for item in data.get("evidence", [])],
    )


def repo_meta_from_dict(data: dict[str, Any]) -> RepoMeta:
    return RepoMeta(
        repo_id=data["repo_id"],
        name=data["name"],
        root_path=data.get("root_path", ""),
        url=data.get("url"),
        year=data.get("year"),
        team=data.get("team"),
        school=data.get("school"),
        style=data.get("style", "unknown"),
        arch=list(data.get("arch", [])),
        languages=dict(data.get("languages", {})),
        loc_total=data.get("loc_total", 0),
        file_count=data.get("file_count", 0),
        commit=data.get("commit"),
        license=data.get("license"),
    )


def symbol_from_dict(data: dict[str, Any]) -> SymbolDef:
    return SymbolDef(
        name=data["name"],
        kind=data["kind"],
        file=data["file"],
        line_start=data["line_start"],
        line_end=data["line_end"],
        signature=data.get("signature", ""),
    )


def kernel_profile_from_dict(data: dict[str, Any]) -> KernelProfile:
    build_system = data.get("build_system")
    return KernelProfile(
        meta=repo_meta_from_dict(data["meta"]),
        overview=data.get("overview", ""),
        build_system=finding_from_dict(build_system) if build_system else None,
        dimensions={
            dim: [finding_from_dict(item) for item in findings]
            for dim, findings in data.get("dimensions", {}).items()
        },
        symbols=[symbol_from_dict(item) for item in data.get("symbols", [])],
        generated_at=data.get("generated_at", ""),
        profile_version=data.get("profile_version", "0.2"),
    )
