"""
KernelSage 仓库采集脚本

用法:
    python scripts/fetch_repos.py                          # 用默认 manifest 拉取全部
    python scripts/fetch_repos.py --only rcore-tutorial-v3 # 只拉一个
    python scripts/fetch_repos.py --manifest path.json --depth 1
    python scripts/fetch_repos.py --reclone               # 强制重新克隆已存在的仓库

约定:
- 浅克隆 (--depth=1) 以节省空间和时间。
- 克隆失败的条目记入 _fetch_report.json, 不中断整体流程。
- 单仓库克隆后写入 <repo_dir>/.kernelsage_meta.json, 记录采集时间与 HEAD SHA。
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MANIFEST = PROJECT_ROOT / "data" / "samples" / "manifest.json"
DEFAULT_OUT_DIR = PROJECT_ROOT / "data" / "samples"
SAFE_REPO_ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$")


@dataclass
class FetchResult:
    repo_id: str
    url: str
    status: str           # "ok" | "skipped" | "failed"
    path: str | None
    head_sha: str | None
    duration_sec: float
    error: str | None = None


def log(msg: str, *, level: str = "INFO") -> None:
    ts = datetime.now().strftime("%H:%M:%S")
    sys.stdout.write(f"[{ts}] {level:5s} {msg}\n")
    sys.stdout.flush()


def load_manifest(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(f"manifest not found: {path}")
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    if "repos" not in data or not isinstance(data["repos"], list):
        raise ValueError("manifest 缺少 repos 数组")
    return data


def run_git(args: list[str], cwd: Path | None = None, timeout: int = 600) -> tuple[int, str, str]:
    proc = subprocess.run(
        ["git", *args],
        cwd=str(cwd) if cwd else None,
        capture_output=True,
        text=True,
        timeout=timeout,
        encoding="utf-8",
        errors="replace",
    )
    return proc.returncode, proc.stdout, proc.stderr


def get_head_sha(repo_dir: Path) -> str | None:
    code, out, _ = run_git(["rev-parse", "HEAD"], cwd=repo_dir, timeout=10)
    return out.strip() if code == 0 else None


def normalize_clone_depth(depth: int) -> int:
    return depth if depth > 0 else 0


def clone_depth_label(depth: int) -> str:
    return str(depth) if depth > 0 else "full"


def build_clone_args(url: str, repo_dir: Path, depth: int) -> list[str]:
    args = ["clone"]
    if depth > 0:
        args.extend(["--depth", str(depth), "--single-branch"])
    args.extend([url, str(repo_dir)])
    return args


def validate_repo_id(repo_id: str) -> str:
    if not isinstance(repo_id, str) or not repo_id:
        raise ValueError("repo_id must be a non-empty string")
    if not SAFE_REPO_ID_RE.fullmatch(repo_id):
        raise ValueError(f"unsafe repo_id: {repo_id!r}")
    if repo_id in {".", ".."} or Path(repo_id).is_absolute():
        raise ValueError(f"unsafe repo_id: {repo_id!r}")
    return repo_id


def resolve_repo_dir(out_dir: Path, repo_id: str) -> Path:
    safe_repo_id = validate_repo_id(repo_id)
    out_root = out_dir.resolve(strict=False)
    repo_dir = (out_root / safe_repo_id).resolve(strict=False)
    if repo_dir == out_root or out_root not in repo_dir.parents:
        raise ValueError(f"repo path escapes output directory: {repo_id!r}")
    return repo_dir


def clone_one(entry: dict[str, Any], out_dir: Path, depth: int, reclone: bool) -> FetchResult:
    repo_id = entry["repo_id"]
    url = entry["url"]
    start = datetime.now(timezone.utc)
    try:
        repo_dir = resolve_repo_dir(out_dir, repo_id)
    except ValueError as exc:
        elapsed = (datetime.now(timezone.utc) - start).total_seconds()
        log(f"拒绝 {repo_id}: {exc}", level="ERROR")
        return FetchResult(
            repo_id=repo_id, url=url, status="failed",
            path=None, head_sha=None, duration_sec=elapsed, error=str(exc),
        )

    if repo_dir.exists():
        if reclone:
            log(f"重新克隆: 删除已存在目录 {repo_dir}")
            shutil.rmtree(repo_dir, ignore_errors=True)
        else:
            head = get_head_sha(repo_dir)
            elapsed = (datetime.now(timezone.utc) - start).total_seconds()
            log(f"跳过 {repo_id} (已存在, HEAD={head[:8] if head else '?'})")
            return FetchResult(
                repo_id=repo_id, url=url, status="skipped",
                path=str(repo_dir), head_sha=head, duration_sec=elapsed,
            )

    depth = normalize_clone_depth(depth)
    log(f"克隆 {repo_id}  <-  {url}  (depth={clone_depth_label(depth)})")
    args = build_clone_args(url, repo_dir, depth)
    try:
        code, _out, err = run_git(args, timeout=900)
    except subprocess.TimeoutExpired as e:
        elapsed = (datetime.now(timezone.utc) - start).total_seconds()
        log(f"超时 {repo_id}: {e}", level="ERROR")
        return FetchResult(
            repo_id=repo_id, url=url, status="failed",
            path=None, head_sha=None, duration_sec=elapsed,
            error=f"timeout after {e.timeout}s",
        )

    elapsed = (datetime.now(timezone.utc) - start).total_seconds()
    if code != 0:
        err_short = (err or "").strip().splitlines()[-1:][0] if err else "git clone failed"
        log(f"失败 {repo_id}: {err_short}", level="ERROR")
        if repo_dir.exists():
            shutil.rmtree(repo_dir, ignore_errors=True)
        return FetchResult(
            repo_id=repo_id, url=url, status="failed",
            path=None, head_sha=None, duration_sec=elapsed, error=err_short,
        )

    head = get_head_sha(repo_dir)
    write_repo_meta(repo_dir, entry, head, depth)
    log(f"完成 {repo_id}  HEAD={head[:8] if head else '?'}  耗时 {elapsed:.1f}s")
    return FetchResult(
        repo_id=repo_id, url=url, status="ok",
        path=str(repo_dir), head_sha=head, duration_sec=elapsed,
    )


def write_repo_meta(repo_dir: Path, entry: dict[str, Any], head: str | None, depth: int) -> None:
    meta = {
        "repo_id": entry["repo_id"],
        "name": entry.get("name"),
        "url": entry["url"],
        "year": entry.get("year"),
        "category": entry.get("category"),
        "source_tier": entry.get("source_tier"),
        "award_level": entry.get("award_level"),
        "award_source_url": entry.get("award_source_url"),
        "style": entry.get("style"),
        "arch": entry.get("arch", []),
        "language_primary": entry.get("language_primary"),
        "team": entry.get("team"),
        "school": entry.get("school"),
        "license": entry.get("license"),
        "note": entry.get("note"),
        "clone_depth": depth,
        "head_sha": head,
        "fetched_at": datetime.now(timezone.utc).isoformat(),
    }
    (repo_dir / ".kernelsage_meta.json").write_text(
        json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8"
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="KernelSage 仓库采集器")
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT_DIR)
    parser.add_argument("--depth", type=int, default=1, help="git clone --depth, 0 表示完整克隆")
    parser.add_argument("--only", action="append", default=[], help="只拉取指定 repo_id, 可多次")
    parser.add_argument("--reclone", action="store_true", help="强制重新克隆已存在仓库")
    args = parser.parse_args()

    manifest = load_manifest(args.manifest)
    repos = manifest["repos"]
    if args.only:
        wanted = set(args.only)
        repos = [r for r in repos if r["repo_id"] in wanted]
        missing = wanted - {r["repo_id"] for r in repos}
        if missing:
            log(f"manifest 中未找到: {sorted(missing)}", level="WARN")

    args.out.mkdir(parents=True, exist_ok=True)
    log(f"输出目录: {args.out}")
    log(f"将处理 {len(repos)} 个仓库")

    depth = normalize_clone_depth(args.depth)
    results: list[FetchResult] = []
    for entry in repos:
        results.append(clone_one(entry, args.out, depth=depth, reclone=args.reclone))

    ok = sum(1 for r in results if r.status == "ok")
    skipped = sum(1 for r in results if r.status == "skipped")
    failed = sum(1 for r in results if r.status == "failed")
    total_time = sum(r.duration_sec for r in results)

    report = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "manifest": str(args.manifest),
        "out_dir": str(args.out),
        "summary": {"ok": ok, "skipped": skipped, "failed": failed, "total": len(results)},
        "results": [asdict(r) for r in results],
    }
    report_path = args.out / "_fetch_report.json"
    report_path.write_text(
        json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    log(f"采集完成: ok={ok} skipped={skipped} failed={failed} 总耗时 {total_time:.1f}s")
    log(f"报告写入 {report_path}")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
