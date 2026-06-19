"""Source evidence index building utilities."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path

from .analyzer import DIMENSIONS, KERNEL_PATH_HINTS, LOW_PRIORITY_PATH_HINTS, PATH_TOKEN_RE, SUPPORT_PATH_HINTS
from .collector import LANG_BY_SUFFIX, SOURCE_TIER_BY_CATEGORY, SKIP_DIRS, load_manifest


INDEX_SOURCE_LANGS = {"rust", "c", "cpp", "asm"}
MAX_INDEX_FILE_SIZE = 500_000
DEFAULT_MAX_FILES_PER_REPO = 300
DIMENSION_PATH_HINTS = {
    str(hint).lower()
    for spec in DIMENSIONS.values()
    for hint in spec.get("hints", [])
}


@dataclass(frozen=True)
class SourceDocument:
    repo_id: str
    repo_name: str
    source_tier: str
    award_level: str | None
    root_path: str
    file: str
    lang: str
    text: str

    @property
    def lines(self) -> list[str]:
        return self.text.splitlines()


@dataclass
class EvidenceIndex:
    samples_dir: str
    documents: list[SourceDocument] = field(default_factory=list)
    repo_count: int = 0
    skipped_repos: list[str] = field(default_factory=list)
    skipped_files: int = 0

    @property
    def file_count(self) -> int:
        return len(self.documents)


class EvidenceIndexer:
    """Build an in-memory source index from local sample repositories."""

    def build_samples_index(
        self,
        samples_dir: Path,
        repo_ids: list[str] | None = None,
        *,
        max_files_per_repo: int = DEFAULT_MAX_FILES_PER_REPO,
        path_filter_terms: list[str] | None = None,
    ) -> EvidenceIndex:
        samples_dir = Path(samples_dir).resolve()
        if not samples_dir.exists():
            raise FileNotFoundError(f"samples directory not found: {samples_dir}")
        selected = {repo_id for repo_id in repo_ids or [] if repo_id}
        manifest = load_manifest(samples_dir)
        index = EvidenceIndex(samples_dir=str(samples_dir))
        for repo_dir in self._repo_dirs(samples_dir, selected):
            try:
                manifest_meta = manifest.get(repo_dir.name, {})
                local_meta = self._load_local_meta(repo_dir)
                candidates = self._source_candidates(
                    repo_dir,
                    max_files_per_repo=max_files_per_repo,
                    path_filter_terms=path_filter_terms,
                )
            except (OSError, json.JSONDecodeError, UnicodeError) as exc:
                index.skipped_repos.append(f"{repo_dir.name}: {exc}")
                continue
            index.repo_count += 1
            for rel, lang in candidates:
                path = repo_dir / rel
                try:
                    text = path.read_text(encoding="utf-8", errors="ignore")
                except OSError:
                    index.skipped_files += 1
                    continue
                if not text.strip():
                    continue
                index.documents.append(
                    SourceDocument(
                        repo_id=repo_dir.name,
                        repo_name=manifest_meta.get("name") or local_meta.get("name") or repo_dir.name,
                        source_tier=self._source_tier(manifest_meta, local_meta),
                        award_level=manifest_meta.get("award_level") or local_meta.get("award_level"),
                        root_path=str(repo_dir),
                        file=rel.as_posix(),
                        lang=lang,
                        text=text,
                    )
                )
        return index

    def _repo_dirs(self, samples_dir: Path, selected: set[str]) -> list[Path]:
        repo_dirs = []
        for path in samples_dir.iterdir():
            if not path.is_dir() or path.name.startswith("."):
                continue
            if selected and path.name not in selected:
                continue
            repo_dirs.append(path)
        return sorted(repo_dirs, key=lambda path: path.name.lower())

    def _source_candidates(
        self,
        repo_dir: Path,
        *,
        max_files_per_repo: int,
        path_filter_terms: list[str] | None,
    ) -> list[tuple[Path, str]]:
        path_terms = [term.lower() for term in path_filter_terms or [] if len(term) >= 2]
        candidates: list[tuple[tuple[int, int, str], Path, str]] = []
        for path in repo_dir.rglob("*"):
            if not path.is_file():
                continue
            rel = path.relative_to(repo_dir)
            if any(part in SKIP_DIRS for part in rel.parts):
                continue
            lang = self._detect_lang(path)
            if lang not in INDEX_SOURCE_LANGS:
                continue
            try:
                size = path.stat().st_size
            except OSError:
                continue
            if size <= 0 or size > MAX_INDEX_FILE_SIZE:
                continue
            rel_text = rel.as_posix().lower()
            candidates.append(((self._path_priority(rel_text), size, rel_text), rel, lang))
        candidates.sort(key=lambda item: item[0])
        if path_terms:
            filtered = [item for item in candidates if self._path_matches_terms(item[0][2], path_terms)]
            if filtered:
                candidates = filtered
        if max_files_per_repo > 0:
            candidates = candidates[:max_files_per_repo]
        return [(rel, lang) for _score, rel, lang in candidates]

    def _detect_lang(self, path: Path) -> str:
        return LANG_BY_SUFFIX.get(path.suffix, LANG_BY_SUFFIX.get(path.suffix.lower(), "unknown"))

    def _path_priority(self, lowered_path: str) -> int:
        if any(hint in lowered_path for hint in LOW_PRIORITY_PATH_HINTS):
            return 8
        if any(hint in lowered_path for hint in KERNEL_PATH_HINTS):
            return 0
        tokens = {token for token in PATH_TOKEN_RE.split(lowered_path) if token}
        if tokens & DIMENSION_PATH_HINTS:
            return 1
        if any(hint in lowered_path for hint in SUPPORT_PATH_HINTS):
            return 2
        return 4

    def _path_matches_terms(self, lowered_path: str, terms: list[str]) -> bool:
        return any(term in lowered_path for term in terms)

    def _load_local_meta(self, repo_dir: Path) -> dict:
        meta_path = repo_dir / ".kernelsage_meta.json"
        if not meta_path.exists():
            return {}
        return json.loads(meta_path.read_text(encoding="utf-8"))

    def _source_tier(self, manifest_meta: dict, local_meta: dict) -> str:
        explicit = manifest_meta.get("source_tier") or local_meta.get("source_tier")
        if explicit:
            return explicit
        category = manifest_meta.get("category") or local_meta.get("category")
        return SOURCE_TIER_BY_CATEGORY.get(category, "unknown")
