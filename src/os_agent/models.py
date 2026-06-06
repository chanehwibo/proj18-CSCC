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
    profile_version: str = "0.1"


@dataclass
class CompareResult:
    new_repo: str
    history_repos: list[str]
    selection_notes: list[str] = field(default_factory=list)
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
