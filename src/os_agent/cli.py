"""Command line interface for KernelSage MVP."""

from __future__ import annotations

import argparse
import json
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

from .agent import CompareAgent
from .analyzer import KernelAnalyzer
from .collector import RepoCollector
from .llm import LLMReportGenerator
from .llm_audit import LLMReportAuditor
from .models import KernelProfile, is_verified_award_case, to_dict
from .parser import SymbolParser
from .profile_cache import ProfileCache
from .reporter import Reporter
from .selector import HistorySelector


PROJECT_ROOT = Path(__file__).resolve().parents[2]
SAMPLES_DIR = PROJECT_ROOT / "data" / "samples"
PROFILES_DIR = PROJECT_ROOT / "data" / "profiles"
REPORTS_DIR = PROJECT_ROOT / "data" / "reports"

SOURCE_TIER_LABELS = {
    "verified_award": "已核验获奖案例",
    "competition_sample": "比赛作品样本（获奖等级未核验）",
    "teaching_baseline": "教学基线",
    "architecture_reference": "架构参考样本",
    "unknown": "未标注",
}


def build_profile(repo_path: Path, repo_id: str | None = None) -> KernelProfile:
    collector = RepoCollector(SAMPLES_DIR)
    snapshot = collector.from_local(repo_path, repo_id=repo_id)
    parsed = SymbolParser().parse_repo(snapshot)
    return KernelAnalyzer().analyze(snapshot, parsed)


def build_profile_cached(
    repo_path: Path,
    repo_id: str | None = None,
    *,
    use_cache: bool = True,
    force_rebuild: bool = False,
    quiet: bool = False,
) -> KernelProfile:
    repo_path = Path(repo_path)
    effective_repo_id = repo_id or repo_path.name
    cache = ProfileCache(PROFILES_DIR)
    result = cache.get_or_build(
        repo_path,
        effective_repo_id,
        lambda: build_profile(repo_path, repo_id=effective_repo_id),
        use_cache=use_cache,
        force_rebuild=force_rebuild,
    )
    if not quiet:
        status = "hit" if result.hit else "rebuilt"
        print(f"profile cache {status}: {effective_repo_id} -> {result.profile_path}")
    return result.profile


def _history_repo_dirs(history_root: Path, new_path: Path) -> list[Path]:
    repo_dirs = []
    for repo_dir in history_root.iterdir():
        if not repo_dir.is_dir() or repo_dir.name.startswith(".") or repo_dir.resolve() == new_path:
            continue
        repo_dirs.append(repo_dir)
    return sorted(repo_dirs, key=lambda path: path.name.lower())


def _build_history_profile(
    repo_dir: Path,
    *,
    use_cache: bool,
    force_rebuild: bool,
) -> tuple[KernelProfile, bool]:
    cache = ProfileCache(PROFILES_DIR)
    result = cache.get_or_build(
        repo_dir,
        repo_dir.name,
        lambda repo_dir=repo_dir: build_profile(repo_dir, repo_id=repo_dir.name),
        use_cache=use_cache,
        force_rebuild=force_rebuild,
    )
    return result.profile, result.hit


def build_history_profiles(
    history_root: Path,
    new_path: Path,
    *,
    jobs: int = 1,
    use_cache: bool = True,
    force_rebuild: bool = False,
) -> tuple[list[KernelProfile], int, int]:
    repo_dirs = _history_repo_dirs(history_root, new_path)
    if not repo_dirs:
        return [], 0, 0

    workers = max(1, jobs)
    results: list[tuple[KernelProfile, bool] | None] = [None] * len(repo_dirs)
    if workers == 1:
        for index, repo_dir in enumerate(repo_dirs):
            results[index] = _build_history_profile(
                repo_dir,
                use_cache=use_cache,
                force_rebuild=force_rebuild,
            )
    else:
        with ThreadPoolExecutor(max_workers=workers) as executor:
            futures = {
                executor.submit(
                    _build_history_profile,
                    repo_dir,
                    use_cache=use_cache,
                    force_rebuild=force_rebuild,
                ): index
                for index, repo_dir in enumerate(repo_dirs)
            }
            for future in as_completed(futures):
                results[futures[future]] = future.result()

    loaded = [result for result in results if result is not None]
    profiles = [profile for profile, _hit in loaded]
    cache_hits = sum(1 for _profile, hit in loaded if hit)
    cache_rebuilt = len(loaded) - cache_hits
    return profiles, cache_hits, cache_rebuilt


def write_json(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(to_dict(value), ensure_ascii=False, indent=2), encoding="utf-8")


def source_tier_label(profile: KernelProfile) -> str:
    label = SOURCE_TIER_LABELS.get(profile.meta.source_tier, profile.meta.source_tier or "未标注")
    if is_verified_award_case(profile.meta) and profile.meta.award_level:
        return f"{label}/{profile.meta.award_level}"
    if profile.meta.source_tier == "verified_award":
        return "比赛作品样本（获奖来源未填写，暂不作为获奖案例）"
    return label


def audit_llm_report_or_raise(prompt_text: str, report: str) -> None:
    audit = LLMReportAuditor().audit(prompt_text, report)
    if audit.ok:
        return

    errors = [f"{issue.code}: {issue.message}" for issue in audit.issues if issue.severity == "error"]
    detail = "; ".join(errors) if errors else "LLM report audit failed"
    raise RuntimeError(detail)


def cmd_profile(args: argparse.Namespace) -> int:
    profile = build_profile_cached(
        Path(args.repo),
        repo_id=args.repo_id,
        use_cache=not args.no_profile_cache,
        force_rebuild=args.rebuild_profile_cache,
    )
    out = Path(args.out) if args.out else PROFILES_DIR / f"{profile.meta.repo_id}.json"
    write_json(out, profile)
    print(f"profile written: {out}")
    return 0


def cmd_describe(args: argparse.Namespace) -> int:
    profile = build_profile_cached(
        Path(args.repo),
        repo_id=args.repo_id,
        use_cache=not args.no_profile_cache,
        force_rebuild=args.rebuild_profile_cache,
    )
    profile_path = PROFILES_DIR / f"{profile.meta.repo_id}.json"
    write_json(profile_path, profile)
    if args.use_llm or args.llm_dry_run:
        dry_run_path = None
        if args.llm_dry_run:
            dry_run_path = REPORTS_DIR / "prompts" / f"{profile.meta.repo_id}.describe.prompt.md"
        try:
            generator = LLMReportGenerator()
            report = generator.render_profile(profile, dry_run_path=dry_run_path)
            if args.llm_dry_run:
                print(report)
                report = Reporter().render_profile(profile)
            elif args.use_llm:
                audit_llm_report_or_raise(generator.format_profile_prompt(profile), report)
        except RuntimeError as exc:
            print(f"LLM failed or audit rejected output, falling back to rule-based report: {exc}", file=sys.stderr)
            report = Reporter().render_profile(profile)
    else:
        report = Reporter().render_profile(profile)
    out = Path(args.out) if args.out else REPORTS_DIR / "describe" / f"{profile.meta.repo_id}.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(report, encoding="utf-8")
    print(f"profile written: {profile_path}")
    print(f"report written: {out}")
    return 0


def cmd_describe_all(args: argparse.Namespace) -> int:
    samples = Path(args.samples)
    repo_dirs = [path for path in samples.iterdir() if path.is_dir() and not path.name.startswith(".")]
    for repo_dir in repo_dirs:
        cmd_describe(
            argparse.Namespace(
                repo=str(repo_dir),
                repo_id=repo_dir.name,
                out=None,
                use_llm=args.use_llm,
                llm_dry_run=args.llm_dry_run,
                no_profile_cache=args.no_profile_cache,
                rebuild_profile_cache=args.rebuild_profile_cache,
            )
        )
    print(f"generated {len(repo_dirs)} describe reports")
    return 0


def cmd_demo(args: argparse.Namespace) -> int:
    repo_path = Path(args.repo)
    repo_id = args.repo_id or repo_path.name
    print(f"demo repo: {repo_path}")
    describe_code = cmd_describe(
        argparse.Namespace(
            repo=str(repo_path),
            repo_id=repo_id,
            out=None,
            use_llm=args.use_llm,
            llm_dry_run=args.llm_dry_run,
            no_profile_cache=args.no_profile_cache,
            rebuild_profile_cache=args.rebuild_profile_cache,
            jobs=getattr(args, "jobs", 1),
        )
    )
    if describe_code != 0:
        return describe_code
    compare_code = cmd_compare(
        argparse.Namespace(
            new=str(repo_path),
            history=args.history,
            repo_id=repo_id,
            limit=args.limit,
            out=None,
            use_llm=args.use_llm,
            llm_dry_run=args.llm_dry_run,
            no_profile_cache=args.no_profile_cache,
            rebuild_profile_cache=args.rebuild_profile_cache,
            jobs=getattr(args, "jobs", 1),
        )
    )
    if compare_code != 0:
        return compare_code
    print("demo outputs:")
    print(f"- profile: {PROFILES_DIR / f'{repo_id}.json'}")
    print(f"- describe report: {REPORTS_DIR / 'describe' / f'{repo_id}.md'}")
    print(f"- compare report: {REPORTS_DIR / 'compare' / f'{repo_id}_vs_history.md'}")
    return 0


def cmd_compare(args: argparse.Namespace) -> int:
    new_path = Path(args.new).resolve()
    new_profile = build_profile_cached(
        new_path,
        repo_id=args.repo_id,
        use_cache=not args.no_profile_cache,
        force_rebuild=args.rebuild_profile_cache,
    )
    history_root = Path(args.history)
    history_profiles, cache_hits, cache_rebuilt = build_history_profiles(
        history_root,
        new_path,
        jobs=getattr(args, "jobs", 1),
        use_cache=not args.no_profile_cache,
        force_rebuild=args.rebuild_profile_cache,
    )
    ranked = HistorySelector().select(new_profile, history_profiles, limit=args.limit)
    selected_profiles = [item.profile for item in ranked]
    result = CompareAgent().compare(new_profile, selected_profiles, limit=args.limit)
    result.selection_notes = [
        f"{item.profile.meta.name}（来源：{source_tier_label(item.profile)}）：score={item.score:.2f}；{'; '.join(item.reasons)}"
        for item in ranked
    ]
    out = Path(args.out) if args.out else REPORTS_DIR / "compare" / f"{new_profile.meta.repo_id}_vs_history.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    if args.use_llm or args.llm_dry_run:
        dry_run_path = None
        if args.llm_dry_run:
            dry_run_path = REPORTS_DIR / "prompts" / f"{new_profile.meta.repo_id}.compare.prompt.md"
        try:
            generator = LLMReportGenerator()
            report = generator.render_compare(result, dry_run_path=dry_run_path)
            if args.llm_dry_run:
                print(report)
                report = Reporter().render_compare(result)
            elif args.use_llm:
                audit_llm_report_or_raise(generator.format_compare_prompt(result), report)
        except RuntimeError as exc:
            print(f"LLM failed or audit rejected output, falling back to rule-based compare report: {exc}", file=sys.stderr)
            report = Reporter().render_compare(result)
    else:
        report = Reporter().render_compare(result)
    out.write_text(report, encoding="utf-8")
    write_json(PROFILES_DIR / f"{new_profile.meta.repo_id}.json", new_profile)
    if ranked:
        print("selected history repositories:")
        for item in ranked:
            reason_text = "; ".join(item.reasons[:3])
            print(f"- {item.profile.meta.repo_id}: score={item.score:.2f}; {reason_text}")
    print(f"profile cache summary: hits={cache_hits} rebuilt={cache_rebuilt} history_total={len(history_profiles)}")
    print(f"compare report written: {out}")
    return 0


def cmd_audit_llm_report(args: argparse.Namespace) -> int:
    result = LLMReportAuditor().audit_paths(Path(args.prompt), Path(args.report))
    print(json.dumps(result.to_dict(), ensure_ascii=False, indent=2))
    return 0 if result.ok else 1


def add_profile_cache_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--no-profile-cache", action="store_true", help="disable KernelProfile cache reads")
    parser.add_argument("--rebuild-profile-cache", action="store_true", help="force rebuilding cached KernelProfile files")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="KernelSage MVP CLI")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("profile", help="generate KernelProfile JSON")
    p.add_argument("repo")
    p.add_argument("--repo-id")
    p.add_argument("--out")
    add_profile_cache_args(p)
    p.set_defaults(func=cmd_profile)

    p = sub.add_parser("describe", help="generate profile and markdown report")
    p.add_argument("repo")
    p.add_argument("--repo-id")
    p.add_argument("--out")
    p.add_argument("--use-llm", action="store_true", help="call configured LLM API to generate the report")
    p.add_argument("--llm-dry-run", action="store_true", help="write the LLM prompt without calling the API")
    add_profile_cache_args(p)
    p.set_defaults(func=cmd_describe)

    p = sub.add_parser("describe-all", help="describe all sample repositories")
    p.add_argument("--samples", default=str(SAMPLES_DIR))
    p.add_argument("--use-llm", action="store_true", help="call configured LLM API to generate reports")
    p.add_argument("--llm-dry-run", action="store_true", help="write LLM prompts without calling the API")
    add_profile_cache_args(p)
    p.set_defaults(func=cmd_describe_all)

    p = sub.add_parser("demo", help="run the end-to-end MVP demo for one repository")
    p.add_argument("repo")
    p.add_argument("--history", default=str(SAMPLES_DIR))
    p.add_argument("--repo-id")
    p.add_argument("--limit", type=int, default=3)
    p.add_argument("--jobs", type=int, default=1, help="parallel workers for history profile building")
    p.add_argument("--use-llm", action="store_true", help="call configured LLM API to generate reports")
    p.add_argument("--llm-dry-run", action="store_true", help="write LLM prompts without calling the API")
    add_profile_cache_args(p)
    p.set_defaults(func=cmd_demo)

    p = sub.add_parser("compare", help="compare one repository with history samples")
    p.add_argument("new")
    p.add_argument("--history", default=str(SAMPLES_DIR))
    p.add_argument("--repo-id")
    p.add_argument("--limit", type=int, default=3)
    p.add_argument("--jobs", type=int, default=1, help="parallel workers for history profile building")
    p.add_argument("--out")
    p.add_argument("--use-llm", action="store_true", help="call configured LLM API to generate the report")
    p.add_argument("--llm-dry-run", action="store_true", help="write the LLM prompt without calling the API")
    add_profile_cache_args(p)
    p.set_defaults(func=cmd_compare)

    p = sub.add_parser("audit-llm-report", help="audit an LLM report against its dry-run prompt")
    p.add_argument("--prompt", required=True, help="path to the dry-run prompt markdown")
    p.add_argument("--report", required=True, help="path to the LLM generated report markdown")
    p.set_defaults(func=cmd_audit_llm_report)
    return parser


def main(argv: list[str] | None = None) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
