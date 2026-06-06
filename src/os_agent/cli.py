"""Command line interface for KernelSage MVP."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .agent import CompareAgent
from .analyzer import KernelAnalyzer
from .collector import RepoCollector
from .llm import LLMReportGenerator
from .models import KernelProfile, to_dict
from .parser import SymbolParser
from .reporter import Reporter
from .selector import HistorySelector


PROJECT_ROOT = Path(__file__).resolve().parents[2]
SAMPLES_DIR = PROJECT_ROOT / "data" / "samples"
PROFILES_DIR = PROJECT_ROOT / "data" / "profiles"
REPORTS_DIR = PROJECT_ROOT / "data" / "reports"


def build_profile(repo_path: Path, repo_id: str | None = None) -> KernelProfile:
    collector = RepoCollector(SAMPLES_DIR)
    snapshot = collector.from_local(repo_path, repo_id=repo_id)
    parsed = SymbolParser().parse_repo(snapshot)
    return KernelAnalyzer().analyze(snapshot, parsed)


def write_json(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(to_dict(value), ensure_ascii=False, indent=2), encoding="utf-8")


def cmd_profile(args: argparse.Namespace) -> int:
    profile = build_profile(Path(args.repo), repo_id=args.repo_id)
    out = Path(args.out) if args.out else PROFILES_DIR / f"{profile.meta.repo_id}.json"
    write_json(out, profile)
    print(f"profile written: {out}")
    return 0


def cmd_describe(args: argparse.Namespace) -> int:
    profile = build_profile(Path(args.repo), repo_id=args.repo_id)
    profile_path = PROFILES_DIR / f"{profile.meta.repo_id}.json"
    write_json(profile_path, profile)
    if args.use_llm or args.llm_dry_run:
        dry_run_path = None
        if args.llm_dry_run:
            dry_run_path = REPORTS_DIR / "prompts" / f"{profile.meta.repo_id}.describe.prompt.md"
        try:
            report = LLMReportGenerator().render_profile(profile, dry_run_path=dry_run_path)
            if args.llm_dry_run:
                print(report)
                report = Reporter().render_profile(profile)
        except RuntimeError as exc:
            print(f"LLM failed, falling back to rule-based report: {exc}", file=sys.stderr)
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
    new_profile = build_profile(new_path, repo_id=args.repo_id)
    history_root = Path(args.history)
    history_profiles: list[KernelProfile] = []
    for repo_dir in history_root.iterdir():
        if not repo_dir.is_dir() or repo_dir.name.startswith(".") or repo_dir.resolve() == new_path:
            continue
        history_profiles.append(build_profile(repo_dir, repo_id=repo_dir.name))
    ranked = HistorySelector().select(new_profile, history_profiles, limit=args.limit)
    selected_profiles = [item.profile for item in ranked]
    result = CompareAgent().compare(new_profile, selected_profiles, limit=args.limit)
    result.selection_notes = [
        f"{item.profile.meta.name}：score={item.score:.2f}；{'; '.join(item.reasons)}"
        for item in ranked
    ]
    out = Path(args.out) if args.out else REPORTS_DIR / "compare" / f"{new_profile.meta.repo_id}_vs_history.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    if args.use_llm or args.llm_dry_run:
        dry_run_path = None
        if args.llm_dry_run:
            dry_run_path = REPORTS_DIR / "prompts" / f"{new_profile.meta.repo_id}.compare.prompt.md"
        try:
            report = LLMReportGenerator().render_compare(result, dry_run_path=dry_run_path)
            if args.llm_dry_run:
                print(report)
                report = Reporter().render_compare(result)
        except RuntimeError as exc:
            print(f"LLM failed, falling back to rule-based compare report: {exc}", file=sys.stderr)
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
    print(f"compare report written: {out}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="KernelSage MVP CLI")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("profile", help="generate KernelProfile JSON")
    p.add_argument("repo")
    p.add_argument("--repo-id")
    p.add_argument("--out")
    p.set_defaults(func=cmd_profile)

    p = sub.add_parser("describe", help="generate profile and markdown report")
    p.add_argument("repo")
    p.add_argument("--repo-id")
    p.add_argument("--out")
    p.add_argument("--use-llm", action="store_true", help="call configured LLM API to generate the report")
    p.add_argument("--llm-dry-run", action="store_true", help="write the LLM prompt without calling the API")
    p.set_defaults(func=cmd_describe)

    p = sub.add_parser("describe-all", help="describe all sample repositories")
    p.add_argument("--samples", default=str(SAMPLES_DIR))
    p.add_argument("--use-llm", action="store_true", help="call configured LLM API to generate reports")
    p.add_argument("--llm-dry-run", action="store_true", help="write LLM prompts without calling the API")
    p.set_defaults(func=cmd_describe_all)

    p = sub.add_parser("demo", help="run the end-to-end MVP demo for one repository")
    p.add_argument("repo")
    p.add_argument("--history", default=str(SAMPLES_DIR))
    p.add_argument("--repo-id")
    p.add_argument("--limit", type=int, default=3)
    p.add_argument("--use-llm", action="store_true", help="call configured LLM API to generate reports")
    p.add_argument("--llm-dry-run", action="store_true", help="write LLM prompts without calling the API")
    p.set_defaults(func=cmd_demo)

    p = sub.add_parser("compare", help="compare one repository with history samples")
    p.add_argument("new")
    p.add_argument("--history", default=str(SAMPLES_DIR))
    p.add_argument("--repo-id")
    p.add_argument("--limit", type=int, default=3)
    p.add_argument("--out")
    p.add_argument("--use-llm", action="store_true", help="call configured LLM API to generate the report")
    p.add_argument("--llm-dry-run", action="store_true", help="write the LLM prompt without calling the API")
    p.set_defaults(func=cmd_compare)
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
