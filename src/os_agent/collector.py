"""Repository collection utilities."""

from __future__ import annotations

import json
from pathlib import Path

from .models import FileEntry, RepoMeta, RepoSnapshot


SKIP_DIRS = {
    ".git",
    ".github",
    ".vscode",
    "target",
    "build",
    "dist",
    "node_modules",
    "__pycache__",
}

LANG_BY_SUFFIX = {
    ".rs": "rust",
    ".c": "c",
    ".h": "c",
    ".S": "asm",
    ".s": "asm",
    ".asm": "asm",
    ".md": "markdown",
    ".txt": "text",
    ".toml": "toml",
    ".yaml": "yaml",
    ".yml": "yaml",
    ".json": "json",
    ".mk": "make",
}

BUILD_FILES = {"Makefile", "Kbuild", "Cargo.toml", "linker.ld", "build.rs"}


def load_manifest(samples_dir: Path) -> dict[str, dict]:
    manifest = samples_dir / "manifest.json"
    if not manifest.exists():
        return {}
    data = json.loads(manifest.read_text(encoding="utf-8"))
    return {item["repo_id"]: item for item in data.get("repos", [])}


class RepoCollector:
    def __init__(self, samples_dir: Path | None = None):
        self.samples_dir = samples_dir
        self.manifest = load_manifest(samples_dir) if samples_dir else {}

    def from_local(self, path: Path, repo_id: str | None = None) -> RepoSnapshot:
        path = path.resolve()
        repo_id = repo_id or path.name
        manifest_meta = self.manifest.get(repo_id, {})
        local_meta = self._load_local_meta(path)
        files = self._scan_files(path)
        languages: dict[str, int] = {}
        for item in files:
            languages[item.lang] = languages.get(item.lang, 0) + item.loc
        meta = RepoMeta(
            repo_id=repo_id,
            name=manifest_meta.get("name") or local_meta.get("name") or path.name,
            root_path=str(path),
            url=manifest_meta.get("url") or local_meta.get("url"),
            year=manifest_meta.get("year"),
            team=manifest_meta.get("team") or local_meta.get("team"),
            school=manifest_meta.get("school") or local_meta.get("school"),
            style=manifest_meta.get("style") or local_meta.get("style") or self._classify_style(path),
            arch=manifest_meta.get("arch") or local_meta.get("arch", []),
            languages=languages,
            loc_total=sum(item.loc for item in files),
            file_count=len(files),
            commit=local_meta.get("head_sha"),
            license=manifest_meta.get("license") or local_meta.get("license"),
        )
        return RepoSnapshot(
            meta=meta,
            files=files,
            readme_text=self._read_readme(path),
            docs_texts=self._read_docs(path),
        )

    def _scan_files(self, root: Path) -> list[FileEntry]:
        entries: list[FileEntry] = []
        for file in root.rglob("*"):
            if not file.is_file():
                continue
            rel = file.relative_to(root)
            if any(part in SKIP_DIRS for part in rel.parts):
                continue
            if file.stat().st_size > 1_000_000:
                continue
            lang = self._detect_lang(file)
            if lang == "unknown":
                continue
            loc = self._count_lines(file)
            entries.append(FileEntry(path=rel.as_posix(), size=file.stat().st_size, lang=lang, loc=loc))
        return entries

    def _detect_lang(self, path: Path) -> str:
        if path.name in BUILD_FILES:
            return "build"
        return LANG_BY_SUFFIX.get(path.suffix, "unknown")

    def _count_lines(self, path: Path) -> int:
        try:
            with path.open("r", encoding="utf-8", errors="ignore") as handle:
                return sum(1 for _ in handle)
        except OSError:
            return 0

    def _read_readme(self, root: Path) -> str:
        for name in ("README.md", "README", "README.txt", "readme.md"):
            path = root / name
            if path.exists():
                return path.read_text(encoding="utf-8", errors="ignore")[:80_000]
        return ""

    def _read_docs(self, root: Path) -> dict[str, str]:
        docs: dict[str, str] = {}
        for doc_dir_name in ("docs", "doc"):
            doc_dir = root / doc_dir_name
            if not doc_dir.exists():
                continue
            for path in doc_dir.rglob("*"):
                if path.is_file() and path.suffix.lower() in {".md", ".txt"} and path.stat().st_size < 500_000:
                    rel = path.relative_to(root).as_posix()
                    docs[rel] = path.read_text(encoding="utf-8", errors="ignore")[:40_000]
        return docs

    def _load_local_meta(self, root: Path) -> dict:
        path = root / ".kernelsage_meta.json"
        if path.exists():
            return json.loads(path.read_text(encoding="utf-8"))
        return {}

    def _classify_style(self, root: Path) -> str:
        names = " ".join(part.name.lower() for part in root.iterdir())
        text = (self._read_readme(root) or "").lower()
        if "rcore" in text or "easy-fs" in names:
            return "rcore-variant"
        if "ucore" in text or "kern" in names:
            return "ucore-variant"
        if "microkernel" in text or "zircon" in text:
            return "microkernel"
        return "unknown"
