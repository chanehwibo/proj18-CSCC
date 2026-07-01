"""Build site-data for the KernelSage contest-works review web console.

The web layer is card-oriented: every contest work becomes one card showing the
team metadata plus on-demand reports (describe / development-history / per-repo
comparison). All analytical conclusions still come from the rule-based pipeline
(KernelProfile + CompareResult); this module only assembles and packages them.
"""

from __future__ import annotations

import re
import subprocess
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .agent import CompareAgent
from .analyzer import DIMENSIONS, KernelAnalyzer
from .collector import RepoCollector, SOURCE_TIER_BY_CATEGORY, load_manifest
from .models import CompareResult, KernelProfile, is_verified_award_case
from .parser import SymbolParser
from .profile_cache import ProfileCache
from .reporter import Reporter
from .selector import HistorySelector
from .selfcheck import EvidenceChecker


SOURCE_TIER_LABELS = {
    "verified_award": "已核验获奖案例",
    "competition_sample": "比赛作品样本（获奖等级未核验）",
    "competition_history": "赛事历史作品",
    "teaching_baseline": "教学基线",
    "architecture_reference": "架构参考样本",
    "unknown": "未标注",
}

CONTEST_NAME = "操作系统大赛"
DEFAULT_SUBTRACK = "内核实现赛道"
ENTRY_NO_RE = re.compile(r"T\d{6,}[-\d]*", re.IGNORECASE)
ENTRY_YEAR_RE = re.compile(r"T(\d{4})", re.IGNORECASE)

# Code-similarity category weights used to rank "重合/重复率最高" history repos.
_RISK_CATEGORY_WEIGHT = {"snippet": 1.0, "function": 0.8, "macro": 0.5, "type": 0.6, "path": 0.35}
_RISK_CONFIDENCE_WEIGHT = {"high": 1.0, "medium": 0.6, "low": 0.3}


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def source_tier_label(meta) -> str:
    label = SOURCE_TIER_LABELS.get(meta.source_tier, meta.source_tier or "未标注")
    if is_verified_award_case(meta) and meta.award_level:
        return f"{label}/{meta.award_level}"
    return label


def manifest_source_tier_label(manifest_meta: dict[str, Any]) -> str:
    source_tier = manifest_meta.get("source_tier")
    if not source_tier:
        source_tier = SOURCE_TIER_BY_CATEGORY.get(manifest_meta.get("category"), "unknown")
    return SOURCE_TIER_LABELS.get(source_tier, source_tier or "未标注")


def entry_number(meta) -> str:
    """Derive a contest entry number from the repo url or fall back to repo_id."""
    if meta.url:
        match = ENTRY_NO_RE.search(meta.url)
        if match:
            return match.group(0)
    return meta.repo_id


def year_from_entry(entry_no: str) -> str | None:
    """Extract the 4-digit year from an entry number like T202410003993220."""
    match = ENTRY_YEAR_RE.search(entry_no)
    return match.group(1) if match else None


def clone_command(url: str | None) -> str:
    """Build a git clone command string from a repo URL."""
    if url and str(url).startswith("http"):
        return f"git clone {url}"
    return "未提供"


@dataclass
class WebConsoleBuilder:
    samples_dir: Path
    profiles_dir: Path | None = None

    def __post_init__(self) -> None:
        self.samples_dir = Path(self.samples_dir)
        self.reporter = Reporter()
        self.checker = EvidenceChecker()
        self.selector = HistorySelector()
        self.compare_agent = CompareAgent()
        self._cache = ProfileCache(Path(self.profiles_dir)) if self.profiles_dir else None
        self._profile_cache: dict[str, KernelProfile] = {}

    # ---- profile building -------------------------------------------------
    def build_profile(self, repo_path: Path, repo_id: str | None = None) -> KernelProfile:
        repo_path = Path(repo_path)
        repo_id = repo_id or repo_path.name
        if repo_id in self._profile_cache:
            return self._profile_cache[repo_id]
        if self._cache is not None:
            result = self._cache.get_or_build(
                repo_path, repo_id, lambda: self._analyze(repo_path, repo_id)
            )
            profile = result.profile
        else:
            profile = self._analyze(repo_path, repo_id)
        self._profile_cache[repo_id] = profile
        return profile

    def _analyze(self, repo_path: Path, repo_id: str) -> KernelProfile:
        collector = RepoCollector(self.samples_dir)
        snapshot = collector.from_local(repo_path, repo_id=repo_id)
        parsed = SymbolParser().parse_repo(snapshot)
        return KernelAnalyzer().analyze(snapshot, parsed)

    # ---- public API -------------------------------------------------------
    def build_site_data(
        self,
        inputs_by_year: dict[str, list[dict[str, Any]]],
        history_root: Path,
        *,
        years: list[str] | None = None,
        top_n: int = 3,
    ) -> dict[str, Any]:
        """Assemble the full site data.

        inputs_by_year maps a year label -> list of input descriptors. Each
        descriptor needs at least {"repo_id", "path"} and may carry overrides such
        as members/team/school/subtrack/url.
        """
        all_input_paths = {
            Path(item["path"]).resolve()
            for items in inputs_by_year.values()
            for item in items
        }
        history_profiles = self._history_profiles(history_root, exclude=all_input_paths)

        # Build all cards first, then re-group by the year actually resolved
        # from each card's entry number (T<YYYY>...), not from the input key.
        all_cards: list[dict[str, Any]] = []
        for fallback_year, items in inputs_by_year.items():
            for item in items:
                card = self._project_card(item, fallback_year, history_profiles, top_n=top_n)
                all_cards.append(card)

        cards_by_year: dict[str, list[dict[str, Any]]] = {}
        for card in all_cards:
            cards_by_year.setdefault(card["year"], []).append(card)

        year_labels = set(years or [])
        year_labels.update(cards_by_year.keys())
        year_labels = sorted(year_labels)

        years_payload: list[dict[str, Any]] = []
        for year in year_labels:
            cards = cards_by_year.get(year, [])
            cards.sort(key=lambda c: c["maturity"]["score"], reverse=True)
            years_payload.append({"year": str(year), "count": len(cards), "projects": cards})

        return {
            "generated_at": _utc_now(),
            "contest_name": CONTEST_NAME,
            "years": years_payload,
            "baseline": self._baseline_payload(history_root, history_profiles),
            "insights": self._insights_payload(all_cards, history_root),
        }

    def _history_profiles(self, history_root: Path, *, exclude: set[Path]) -> list[KernelProfile]:
        history_root = Path(history_root)
        profiles: list[KernelProfile] = []
        manifest = load_manifest(history_root)
        manifest_ids = set(manifest)
        for repo_dir in sorted(history_root.iterdir(), key=lambda p: p.name.lower()):
            if not repo_dir.is_dir() or repo_dir.name.startswith("."):
                continue
            if manifest_ids and repo_dir.name not in manifest_ids:
                continue
            if repo_dir.resolve() in exclude:
                continue
            profiles.append(self.build_profile(repo_dir, repo_id=repo_dir.name))
        return profiles

    # ---- per project card -------------------------------------------------
    def _project_card(
        self,
        item: dict[str, Any],
        year: str,
        history_profiles: list[KernelProfile],
        *,
        top_n: int,
    ) -> dict[str, Any]:
        repo_path = Path(item["path"])
        repo_id = item.get("repo_id") or repo_path.name
        profile = self.build_profile(repo_path, repo_id=repo_id)
        meta = profile.meta

        compares = self._top_compares(profile, history_profiles, top_n=top_n)
        maturity = self.reporter.maturity(profile)

        eno = item.get("entry_no") or entry_number(meta)
        resolved_year = item.get("year") or year_from_entry(eno) or meta.year or year
        repo_url = item.get("url") or meta.url or "未提供"
        top_overlap = compares[0]["overlap_score"] if compares else 0.0
        risk_level = "high" if top_overlap >= 60 else ("medium" if top_overlap >= 30 else ("low" if compares else "none"))

        return {
            "repo_id": repo_id,
            "entry_no": eno,
            "name": meta.name,
            "year": str(resolved_year),
            "school": item.get("school") or meta.school or "未提供",
            "team_name": item.get("team") or meta.team or meta.name,
            "members": item.get("members") or "未提供",
            "contest_name": CONTEST_NAME,
            "subtrack": item.get("subtrack") or DEFAULT_SUBTRACK,
            "repo_url": repo_url,
            "clone_cmd": clone_command(repo_url if str(repo_url).startswith("http") else meta.url),
            "arch": meta.arch,
            "languages": meta.languages,
            "loc": meta.loc_total,
            "file_count": meta.file_count,
            "symbol_count": len(profile.symbols),
            "source_tier_label": source_tier_label(meta),
            "maturity": maturity,
            "dimensions": self._dimensions_summary(profile),
            "top_overlap": round(top_overlap, 1),
            "risk_level": risk_level,
            "selfcheck": self._round_selfcheck(self.checker.profile_summary(profile)),
            "reports": {
                "describe_md": self.reporter.render_profile(profile),
                "dev_history_md": self._dev_history_md(repo_path, meta),
                "compares": compares,
            },
        }

    def _dimensions_summary(self, profile: KernelProfile) -> list[dict[str, Any]]:
        out: list[dict[str, Any]] = []
        for dim, spec in DIMENSIONS.items():
            findings = [f for f in profile.dimensions.get(dim, []) if f.confidence != "unconfirmed"]
            confidence = self.reporter.dimension_confidence(findings)
            out.append({
                "key": dim,
                "title": spec["title"],
                "status": "confirmed" if findings else "unconfirmed",
                "confidence": confidence,
            })
        return out

    # ---- top-N "重合/重复率最高" 1v1 compares -----------------------------
    def _top_compares(
        self, profile: KernelProfile, history_profiles: list[KernelProfile], *, top_n: int
    ) -> list[dict[str, Any]]:
        # Pre-filter to a manageable candidate set by profile similarity, then run
        # full 1v1 compare on each candidate and rank by overlap + duplication.
        prelim = self.selector.select(profile, history_profiles, limit=max(top_n * 2, 6))
        scored: list[tuple[float, CompareResult, Any]] = []
        for ranked in prelim:
            result = self.compare_agent.compare(profile, [ranked.profile], limit=1)
            overlap_score = self._overlap_score(result)
            scored.append((overlap_score, result, ranked))
        scored.sort(key=lambda t: t[0], reverse=True)

        compares: list[dict[str, Any]] = []
        for index, (overlap_score, result, ranked) in enumerate(scored[:top_n], start=1):
            result.selection_notes = [
                f"{ranked.profile.meta.name}（来源：{source_tier_label(ranked.profile.meta)}）："
                f"画像相似度 score={ranked.score:.2f}；{'; '.join(ranked.reasons)}"
            ]
            compares.append({
                "index": index,
                "label": f"比较报告{index}",
                "target_repo_id": ranked.profile.meta.repo_id,
                "target_name": ranked.profile.meta.name,
                "target_tier_label": source_tier_label(ranked.profile.meta),
                "overlap_dimensions": len(result.overlap_points),
                "code_similarity_count": len(result.code_similarity_points),
                "overlap_score": round(overlap_score, 1),
                "report_md": self.reporter.render_compare(result),
            })
        return compares

    def _overlap_score(self, result: CompareResult) -> float:
        raw = len(result.overlap_points) * 1.0
        for finding in result.code_similarity_points:
            category = self.compare_agent._code_similarity_category(finding)  # noqa: SLF001
            raw += _RISK_CATEGORY_WEIGHT.get(category, 0.3) * _RISK_CONFIDENCE_WEIGHT.get(finding.confidence, 0.3)
        return min(100.0, raw / 14.0 * 100.0)

    # ---- development history ---------------------------------------------
    def _dev_history_md(self, repo_path: Path, meta) -> str:
        repo_path = Path(repo_path)
        lines = [f"# {meta.name} 开发历史报告", ""]
        info = self._git_history(repo_path)
        if info is None:
            lines.extend([
                "> 当前样本目录不是有效 Git 仓库，或采集时未保留提交历史，无法生成研发历程。",
                "",
                "建议：使用 `python scripts/fetch_repos.py --depth 0` 完整克隆后重新生成本报告。",
            ])
            return "\n".join(lines) + "\n"

        lines.extend([
            "## 提交概览",
            "",
            f"- 总提交数：{info['total']}{'（浅克隆，可能不完整）' if info['shallow'] else ''}",
            f"- 参与作者数：{len(info['authors'])}",
            f"- 时间跨度：{info['first_date'] or '未知'} ~ {info['last_date'] or '未知'}",
            f"- HEAD：`{info['head'] or '未知'}`",
            "",
        ])
        if info["authors"]:
            lines.extend(["## 贡献者", ""])
            for author, count in info["authors"]:
                lines.append(f"- {author}：{count} 次提交")
            lines.append("")
        if info["commits"]:
            lines.extend(["## 最近提交记录", "", "| 提交 | 作者 | 日期 | 说明 |", "| --- | --- | --- | --- |"])
            for commit in info["commits"]:
                subject = commit["subject"].replace("|", "\\|")
                lines.append(f"| `{commit['hash']}` | {commit['author']} | {commit['date']} | {subject} |")
            lines.append("")
        lines.append("> 说明：开发历史来自仓库本地 Git 记录，仅作研发过程参考，不代表作品功能结论。")
        return "\n".join(lines) + "\n"

    def _git_history(self, repo_path: Path) -> dict[str, Any] | None:
        if not (repo_path / ".git").exists():
            return None
        commits = self._git_log(repo_path)
        if commits is None:
            return None
        author_counts: dict[str, int] = {}
        for commit in commits:
            author_counts[commit["author"]] = author_counts.get(commit["author"], 0) + 1
        authors = sorted(author_counts.items(), key=lambda kv: (-kv[1], kv[0]))
        dates = [c["date"] for c in commits if c["date"]]
        return {
            "total": self._git_count(repo_path) or len(commits),
            "shallow": (repo_path / ".git" / "shallow").exists(),
            "authors": authors,
            "first_date": min(dates) if dates else None,
            "last_date": max(dates) if dates else None,
            "head": self._git_head(repo_path),
            "commits": commits[:40],
        }

    def _git_log(self, repo_path: Path) -> list[dict[str, str]] | None:
        out = self._run_git(repo_path, ["log", "-n", "200", "--date=short", "--pretty=format:%h\x1f%an\x1f%ad\x1f%s"])
        if out is None:
            return None
        commits: list[dict[str, str]] = []
        for line in out.splitlines():
            parts = line.split("\x1f")
            if len(parts) == 4:
                commits.append({"hash": parts[0], "author": parts[1], "date": parts[2], "subject": parts[3]})
        return commits

    def _git_count(self, repo_path: Path) -> int | None:
        out = self._run_git(repo_path, ["rev-list", "--count", "HEAD"])
        try:
            return int(out.strip()) if out is not None else None
        except ValueError:
            return None

    def _git_head(self, repo_path: Path) -> str | None:
        out = self._run_git(repo_path, ["rev-parse", "--short", "HEAD"])
        return out.strip() if out else None

    def _run_git(self, repo_path: Path, args: list[str]) -> str | None:
        try:
            proc = subprocess.run(
                ["git", "-C", str(repo_path), *args],
                capture_output=True, text=True, timeout=15, encoding="utf-8", errors="replace",
            )
        except (OSError, subprocess.TimeoutExpired):
            return None
        return proc.stdout if proc.returncode == 0 else None

    # ---- baseline ---------------------------------------------------------
    def _baseline_payload(self, history_root: Path, history_profiles: list[KernelProfile]) -> dict[str, Any]:
        manifest = load_manifest(Path(history_root))
        by_id = {p.meta.repo_id: p for p in history_profiles}
        repos: list[dict[str, Any]] = []
        for repo_id, m in manifest.items():
            profile = by_id.get(repo_id)
            repos.append({
                "repo_id": repo_id,
                "name": m.get("name", repo_id),
                "source_tier_label": source_tier_label(profile.meta) if profile else SOURCE_TIER_LABELS.get(m.get("source_tier", ""), m.get("category", "未标注")),
                "arch": m.get("arch", []),
                "language_primary": m.get("language_primary"),
                "year": m.get("year"),
                "school": m.get("school"),
                "award_level": m.get("award_level"),
                "url": m.get("url"),
                "loc": profile.meta.loc_total if profile else None,
                "note": m.get("note", ""),
            })
        repos.sort(key=lambda r: (str(r["source_tier_label"]), r["repo_id"]))
        return {"count": len(repos), "repos": repos}

    def _round_selfcheck(self, summary: dict[str, Any]) -> dict[str, Any]:
        out = dict(summary)
        if "coverage" in out:
            out["coverage"] = round(float(out["coverage"]), 1)
        return out

    # ---- insights (查重矩阵 / 关系图 / 跨年份 / 学校聚合) ------------------
    def _insights_payload(
        self,
        all_cards: list[dict[str, Any]],
        history_root: Path,
    ) -> dict[str, Any]:
        return {
            "matrix": self._similarity_matrix(all_cards),
            "year_evolution": self._year_evolution(history_root, all_cards),
            "schools": self._school_aggregate(history_root, all_cards),
        }

    def _pair_similarity(self, a: KernelProfile, b: KernelProfile) -> float:
        """Lightweight symmetric profile similarity 0-100 (reuses HistorySelector)."""
        ranked = self.selector.rank_one(a, b)
        return round(min(100.0, ranked.score / 12.0 * 100.0), 1)

    def _similarity_matrix(self, all_cards: list[dict[str, Any]]) -> dict[str, Any]:
        profiles = [self._profile_cache.get(c["repo_id"]) for c in all_cards]
        labels = [
            {"repo_id": c["repo_id"], "entry_no": c["entry_no"], "name": c["name"], "year": c["year"]}
            for c in all_cards
        ]
        n = len(profiles)
        rows: list[list[float]] = [[0.0] * n for _ in range(n)]
        links: list[dict[str, Any]] = []
        pairs: list[dict[str, Any]] = []
        for i in range(n):
            for j in range(i + 1, n):
                if profiles[i] is None or profiles[j] is None:
                    continue
                score = self._pair_similarity(profiles[i], profiles[j])
                rows[i][j] = score
                rows[j][i] = score
                if score >= 40:
                    links.append({"source": i, "target": j, "score": score})
                pairs.append({
                    "i": i, "j": j, "score": score,
                    "a_repo": labels[i]["repo_id"], "a_entry": labels[i]["entry_no"], "a_name": labels[i]["name"], "a_year": labels[i]["year"],
                    "b_repo": labels[j]["repo_id"], "b_entry": labels[j]["entry_no"], "b_name": labels[j]["name"], "b_year": labels[j]["year"],
                })
        for i in range(n):
            rows[i][i] = 100.0
        # keep only meaningful pairs (>=25), sorted desc, capped for payload size
        pairs = [p for p in pairs if p["score"] >= 25]
        pairs.sort(key=lambda p: -p["score"])
        pairs = pairs[:300]
        return {"labels": labels, "rows": rows, "links": links, "pairs": pairs}

    def _year_evolution(self, history_root: Path, all_cards: list[dict[str, Any]]) -> list[dict[str, Any]]:
        manifest = load_manifest(Path(history_root))
        agg: dict[str, dict[str, Any]] = {}

        def bucket(year: str) -> dict[str, Any]:
            return agg.setdefault(str(year), {"year": str(year), "count": 0, "awards": 0, "langs": {}})

        for _rid, m in manifest.items():
            yr = m.get("year")
            if not yr:
                continue
            b = bucket(str(yr))
            b["count"] += 1
            if m.get("award_level"):
                b["awards"] += 1
            lang = (m.get("language_primary") or "其他").lower()
            b["langs"][lang] = b["langs"].get(lang, 0) + 1
        # include this-year input works
        for c in all_cards:
            b = bucket(c["year"])
            b["count"] += 1
            langs = c.get("languages") or {}
            primary = max(langs, key=langs.get).lower() if langs else "其他"
            b["langs"][primary] = b["langs"].get(primary, 0) + 1

        out = []
        for yr in sorted(agg.keys()):
            b = agg[yr]
            total = sum(b["langs"].values()) or 1
            rust = b["langs"].get("rust", 0)
            c_lang = b["langs"].get("c", 0) + b["langs"].get("cpp", 0)
            out.append({
                "year": b["year"],
                "count": b["count"],
                "awards": b["awards"],
                "rust_ratio": round(rust / total * 100, 1),
                "c_ratio": round(c_lang / total * 100, 1),
                "langs": b["langs"],
            })
        return out

    def _school_aggregate(self, history_root: Path, all_cards: list[dict[str, Any]]) -> list[dict[str, Any]]:
        manifest = load_manifest(Path(history_root))
        agg: dict[str, dict[str, Any]] = {}

        def bucket(school: str) -> dict[str, Any]:
            return agg.setdefault(school, {"school": school, "count": 0, "awards": 0, "years": set()})

        for _rid, m in manifest.items():
            school = m.get("school")
            if not school:
                continue
            b = bucket(school)
            b["count"] += 1
            if m.get("award_level"):
                b["awards"] += 1
            if m.get("year"):
                b["years"].add(str(m["year"]))
        for c in all_cards:
            school = c.get("school")
            if school and school != "未提供":
                b = bucket(school)
                b["count"] += 1
                b["years"].add(c["year"])

        out = [
            {"school": b["school"], "count": b["count"], "awards": b["awards"], "years": sorted(b["years"])}
            for b in agg.values()
        ]
        out.sort(key=lambda x: (-x["count"], x["school"]))
        return out
