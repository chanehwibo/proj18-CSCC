"""Persistent KernelProfile cache utilities."""

from __future__ import annotations

import json
import subprocess
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Callable

from .collector import SKIP_DIRS
from .models import KernelProfile, kernel_profile_from_dict, to_dict


CACHE_SCHEMA_VERSION = "1.9"


@dataclass
class SourceFingerprint:
    root_path: str
    commit: str | None
    file_count: int
    total_size: int
    newest_mtime_ns: int


@dataclass
class CacheMeta:
    schema_version: str
    repo_id: str
    fingerprint: SourceFingerprint
    profile_path: str


@dataclass
class CacheResult:
    profile: KernelProfile
    hit: bool
    profile_path: Path


class ProfileCache:
    def __init__(self, profiles_dir: Path):
        self.profiles_dir = profiles_dir
        self.meta_dir = profiles_dir / ".cache_meta"

    def get_or_build(
        self,
        repo_path: Path,
        repo_id: str,
        builder: Callable[[], KernelProfile],
        *,
        use_cache: bool = True,
        force_rebuild: bool = False,
    ) -> CacheResult:
        repo_path = repo_path.resolve()
        profile_path = self.profile_path(repo_id)
        fingerprint = self.fingerprint(repo_path)

        if use_cache and not force_rebuild:
            cached = self._load_if_valid(repo_id, fingerprint, profile_path)
            if cached:
                return CacheResult(cached, hit=True, profile_path=profile_path)

        profile = builder()
        self.write(profile, fingerprint, profile_path)
        return CacheResult(profile, hit=False, profile_path=profile_path)

    def profile_path(self, repo_id: str) -> Path:
        return self.profiles_dir / f"{repo_id}.json"

    def write(self, profile: KernelProfile, fingerprint: SourceFingerprint, profile_path: Path | None = None) -> None:
        profile_path = profile_path or self.profile_path(profile.meta.repo_id)
        profile_path.parent.mkdir(parents=True, exist_ok=True)
        profile_path.write_text(json.dumps(to_dict(profile), ensure_ascii=False, indent=2), encoding="utf-8")

        meta = CacheMeta(
            schema_version=CACHE_SCHEMA_VERSION,
            repo_id=profile.meta.repo_id,
            fingerprint=fingerprint,
            profile_path=str(profile_path),
        )
        self.meta_dir.mkdir(parents=True, exist_ok=True)
        self._meta_path(profile.meta.repo_id).write_text(
            json.dumps(asdict(meta), ensure_ascii=False, indent=2), encoding="utf-8"
        )

    def fingerprint(self, repo_path: Path) -> SourceFingerprint:
        fast = self._git_fast_fingerprint(repo_path)
        if fast:
            return fast
        return self._full_tree_fingerprint(repo_path)

    def _full_tree_fingerprint(self, repo_path: Path) -> SourceFingerprint:
        file_count = 0
        total_size = 0
        newest_mtime_ns = 0
        for file in repo_path.rglob("*"):
            if not file.is_file():
                continue
            rel = file.relative_to(repo_path)
            if any(part in SKIP_DIRS for part in rel.parts):
                continue
            try:
                stat = file.stat()
            except OSError:
                continue
            file_count += 1
            total_size += stat.st_size
            newest_mtime_ns = max(newest_mtime_ns, stat.st_mtime_ns)
        return SourceFingerprint(
            root_path=str(repo_path),
            commit=self._git_head(repo_path) or self._local_meta_head(repo_path),
            file_count=file_count,
            total_size=total_size,
            newest_mtime_ns=newest_mtime_ns,
        )

    def _git_fast_fingerprint(self, repo_path: Path) -> SourceFingerprint | None:
        head = self._git_head(repo_path)
        if not head:
            return None
        if not self._git_worktree_clean(repo_path):
            return None
        tracked_count = self._git_tracked_file_count(repo_path)
        if tracked_count is None:
            return None
        return SourceFingerprint(
            root_path=str(repo_path),
            commit=f"git-clean:{head}",
            file_count=tracked_count,
            total_size=0,
            newest_mtime_ns=0,
        )

    def _load_if_valid(
        self,
        repo_id: str,
        fingerprint: SourceFingerprint,
        profile_path: Path,
    ) -> KernelProfile | None:
        meta_path = self._meta_path(repo_id)
        if not profile_path.exists() or not meta_path.exists():
            return None
        try:
            meta_data = json.loads(meta_path.read_text(encoding="utf-8"))
            profile_data = json.loads(profile_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return None
        if meta_data.get("schema_version") != CACHE_SCHEMA_VERSION:
            return None
        if meta_data.get("repo_id") != repo_id:
            return None
        if meta_data.get("fingerprint") != asdict(fingerprint):
            return None
        return kernel_profile_from_dict(profile_data)

    def _meta_path(self, repo_id: str) -> Path:
        return self.meta_dir / f"{repo_id}.json"

    def _git_head(self, repo_path: Path) -> str | None:
        try:
            proc = subprocess.run(
                ["git", "rev-parse", "HEAD"],
                cwd=str(repo_path),
                capture_output=True,
                text=True,
                timeout=5,
                encoding="utf-8",
                errors="replace",
            )
        except (OSError, subprocess.TimeoutExpired):
            return None
        return proc.stdout.strip() if proc.returncode == 0 else None

    def _git_worktree_clean(self, repo_path: Path) -> bool:
        try:
            proc = subprocess.run(
                ["git", "status", "--porcelain", "--untracked-files=normal"],
                cwd=str(repo_path),
                capture_output=True,
                text=True,
                timeout=5,
                encoding="utf-8",
                errors="replace",
            )
        except (OSError, subprocess.TimeoutExpired):
            return False
        return proc.returncode == 0 and not proc.stdout.strip()

    def _git_tracked_file_count(self, repo_path: Path) -> int | None:
        try:
            proc = subprocess.run(
                ["git", "ls-files", "-z"],
                cwd=str(repo_path),
                capture_output=True,
                text=True,
                timeout=10,
                encoding="utf-8",
                errors="replace",
            )
        except (OSError, subprocess.TimeoutExpired):
            return None
        if proc.returncode != 0:
            return None
        if not proc.stdout:
            return 0
        return sum(1 for item in proc.stdout.split("\0") if item)

    def _local_meta_head(self, repo_path: Path) -> str | None:
        meta_path = repo_path / ".kernelsage_meta.json"
        if not meta_path.exists():
            return None
        try:
            return json.loads(meta_path.read_text(encoding="utf-8")).get("head_sha")
        except (OSError, json.JSONDecodeError):
            return None
