"""Manifest trust audit utilities."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any
from urllib.parse import urlparse


SAFE_REPO_ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$")


@dataclass
class ManifestAuditIssue:
    repo_id: str
    severity: str
    code: str
    message: str

    def to_dict(self) -> dict[str, str]:
        return {
            "repo_id": self.repo_id,
            "severity": self.severity,
            "code": self.code,
            "message": self.message,
        }


@dataclass
class ManifestAuditResult:
    manifest: str
    samples_dir: str
    total_repos: int
    checked_at: str = ""
    issues: list[ManifestAuditIssue] = field(default_factory=list)

    @property
    def errors(self) -> int:
        return sum(1 for issue in self.issues if issue.severity == "error")

    @property
    def warnings(self) -> int:
        return sum(1 for issue in self.issues if issue.severity == "warning")

    @property
    def ok(self) -> bool:
        return self.errors == 0

    def to_dict(self) -> dict[str, Any]:
        return {
            "manifest": self.manifest,
            "samples_dir": self.samples_dir,
            "total_repos": self.total_repos,
            "summary": {
                "ok": self.ok,
                "errors": self.errors,
                "warnings": self.warnings,
            },
            "issues": [issue.to_dict() for issue in self.issues],
        }


class ManifestAuditor:
    """Validate sample manifest metadata without network access."""

    def audit(self, manifest_path: Path, samples_dir: Path) -> ManifestAuditResult:
        manifest_path = manifest_path.resolve()
        samples_dir = samples_dir.resolve()
        data = self._load_manifest(manifest_path)
        repos = data.get("repos", [])
        result = ManifestAuditResult(
            manifest=str(manifest_path),
            samples_dir=str(samples_dir),
            total_repos=len(repos) if isinstance(repos, list) else 0,
        )
        if not isinstance(repos, list):
            result.issues.append(
                ManifestAuditIssue("<manifest>", "error", "repos_not_list", "manifest repos must be a list")
            )
            return result

        seen: set[str] = set()
        for index, entry in enumerate(repos):
            repo_id = str(entry.get("repo_id") or f"<missing:{index}>")
            self._audit_entry(entry, repo_id, seen, manifest_path, samples_dir, result)
        return result

    def _load_manifest(self, manifest_path: Path) -> dict[str, Any]:
        if not manifest_path.exists():
            raise FileNotFoundError(f"manifest not found: {manifest_path}")
        return json.loads(manifest_path.read_text(encoding="utf-8"))

    def _audit_entry(
        self,
        entry: dict[str, Any],
        repo_id: str,
        seen: set[str],
        manifest_path: Path,
        samples_dir: Path,
        result: ManifestAuditResult,
    ) -> None:
        def add(severity: str, code: str, message: str) -> None:
            result.issues.append(ManifestAuditIssue(repo_id, severity, code, message))

        if not entry.get("repo_id"):
            add("error", "repo_id_missing", "repo_id is required")
            return
        if repo_id in seen:
            add("error", "repo_id_duplicate", "repo_id is duplicated")
        seen.add(repo_id)
        if not self._is_safe_repo_id(repo_id):
            add("error", "repo_id_unsafe", "repo_id may escape data/samples or break local paths")

        url = entry.get("url")
        if not isinstance(url, str) or not url.strip():
            add("error", "url_missing", "repository url is required")
        elif not self._looks_like_remote_url(url):
            add("warning", "url_unusual", "repository url is not an http(s), ssh, or git remote")

        if entry.get("source_tier") == "verified_award":
            if not entry.get("award_level"):
                add("error", "award_level_missing", "verified_award sample must include award_level")
            if not entry.get("award_source_url"):
                add("error", "award_source_missing", "verified_award sample must include award_source_url")
            elif not self._award_source_exists(str(entry["award_source_url"]), manifest_path):
                add("warning", "award_source_unresolved", "award_source_url is recorded but not found locally")

        repo_dir = self._repo_dir(samples_dir, repo_id)
        if repo_dir is None:
            add("error", "sample_path_escape", "resolved sample path escapes samples_dir")
            return
        if not repo_dir.exists():
            add("warning", "sample_dir_missing", "sample directory has not been fetched locally")
            return
        if not repo_dir.is_dir():
            add("error", "sample_path_not_dir", "sample path exists but is not a directory")
            return
        if not self._head_recorded(repo_dir):
            add("warning", "head_missing", "sample HEAD is not recorded in .kernelsage_meta.json or .git/HEAD")

    def _is_safe_repo_id(self, repo_id: str) -> bool:
        if not SAFE_REPO_ID_RE.fullmatch(repo_id):
            return False
        path = Path(repo_id)
        return repo_id not in {".", ".."} and not path.is_absolute() and ".." not in path.parts

    def _repo_dir(self, samples_dir: Path, repo_id: str) -> Path | None:
        try:
            root = samples_dir.resolve(strict=False)
            path = (root / repo_id).resolve(strict=False)
        except (OSError, RuntimeError):
            return None
        if path == root or root not in path.parents:
            return None
        return path

    def _looks_like_remote_url(self, url: str) -> bool:
        parsed = urlparse(url)
        if parsed.scheme in {"http", "https", "ssh", "git"} and parsed.netloc:
            return True
        return bool(re.match(r"^[A-Za-z0-9_.-]+@[^:]+:.+\.git$", url))

    def _award_source_exists(self, source: str, manifest_path: Path) -> bool:
        parsed = urlparse(source)
        if parsed.scheme and parsed.netloc:
            return True
        path = Path(source)
        if path.is_absolute():
            return path.exists()
        candidates = [
            manifest_path.parent / source,
            manifest_path.parents[2] / source if len(manifest_path.parents) > 2 else manifest_path.parent / source,
            manifest_path.parents[3] / source if len(manifest_path.parents) > 3 else manifest_path.parent / source,
        ]
        return any(candidate.exists() for candidate in candidates)

    def _head_recorded(self, repo_dir: Path) -> bool:
        meta_path = repo_dir / ".kernelsage_meta.json"
        if meta_path.exists():
            try:
                meta = json.loads(meta_path.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError):
                return False
            if meta.get("head_sha"):
                return True
        return (repo_dir / ".git" / "HEAD").exists()


def render_manifest_audit(result: ManifestAuditResult) -> str:
    lines = [
        "Manifest audit summary",
        f"- manifest: {result.manifest}",
        f"- samples_dir: {result.samples_dir}",
        f"- repos: {result.total_repos}",
        f"- errors: {result.errors}",
        f"- warnings: {result.warnings}",
    ]
    if not result.issues:
        lines.append("- issues: none")
        return "\n".join(lines) + "\n"

    lines.extend(["", "Issues:"])
    for issue in result.issues:
        lines.append(f"- [{issue.severity}] {issue.repo_id}: {issue.code} - {issue.message}")
    return "\n".join(lines) + "\n"
