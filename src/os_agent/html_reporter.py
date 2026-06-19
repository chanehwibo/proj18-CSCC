"""HTML evidence report generation."""

from __future__ import annotations

import html
import re
from pathlib import Path

from .analyzer import DIMENSIONS
from .models import CompareResult, Evidence, Finding, KernelProfile
from .selfcheck import EvidenceChecker


class HTMLReporter:
    def __init__(self) -> None:
        self.checker = EvidenceChecker()

    def render_profile(self, profile: KernelProfile) -> str:
        findings = self._profile_findings(profile)
        summary = self.checker.profile_summary(profile)
        invalid = self._invalid_profile_evidence(profile, findings)
        rows = self._evidence_rows(findings, invalid)
        sections = [
            self._hero(profile.meta.name, "Profile evidence report"),
            self._summary_cards(
                [
                    ("Repository", profile.meta.repo_id),
                    ("Style", profile.meta.style),
                    ("Files", str(profile.meta.file_count)),
                    ("LOC", str(profile.meta.loc_total)),
                    ("Self-check", self._selfcheck_label(summary)),
                ]
            ),
            self._section("Overview", f"<p>{self._escape(profile.overview or 'No overview generated.')}</p>"),
            self._section("OS Dimensions", self._dimension_table(profile)),
            self._section("Evidence Files", self._evidence_table(rows)),
            self._section("Self-check", self._selfcheck_table(summary)),
        ]
        return self._document(f"{profile.meta.name} profile evidence", "\n".join(sections))

    def render_compare(self, result: CompareResult) -> str:
        findings = self._compare_findings(result)
        summary = self.checker.compare_summary(result)
        invalid = self._invalid_compare_evidence(result, findings)
        rows = self._evidence_rows(findings, invalid)
        sections = [
            self._hero(result.new_repo, "Compare evidence report"),
            self._summary_cards(
                [
                    ("History repos", str(len(result.history_repos))),
                    ("Overlap points", str(len(result.overlap_points))),
                    ("Code similarity", str(len(result.code_similarity_points))),
                    ("Self-check", self._selfcheck_label(summary)),
                ]
            ),
            self._section("Similarity Scores", self._score_bars(result)),
            self._section("Conclusions", self._finding_groups(result)),
            self._section("Evidence Files", self._evidence_table(rows)),
            self._section("Self-check", self._selfcheck_table(summary)),
        ]
        return self._document(f"{result.new_repo} compare evidence", "\n".join(sections))

    def _document(self, title: str, body: str) -> str:
        return (
            "<!doctype html>\n"
            "<html lang=\"zh-CN\">\n"
            "<head>\n"
            "  <meta charset=\"utf-8\">\n"
            "  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">\n"
            f"  <title>{self._escape(title)}</title>\n"
            "  <style>\n"
            "    :root { color-scheme: light; --ink:#17202a; --muted:#5d6875; --line:#d7dde5; --panel:#f8fafc; --accent:#1f7a8c; --ok:#1f8a5b; --warn:#b7791f; --bad:#b42318; }\n"
            "    * { box-sizing: border-box; }\n"
            "    body { margin:0; font-family: Segoe UI, Microsoft YaHei, Arial, sans-serif; color:var(--ink); background:#ffffff; line-height:1.55; }\n"
            "    header { padding:32px 40px 24px; border-bottom:1px solid var(--line); background:linear-gradient(180deg,#f8fafc 0%,#ffffff 100%); }\n"
            "    main { max-width:1180px; margin:0 auto; padding:28px 24px 48px; }\n"
            "    h1 { margin:0; font-size:28px; font-weight:700; letter-spacing:0; }\n"
            "    h2 { margin:30px 0 12px; font-size:20px; letter-spacing:0; }\n"
            "    p { margin:0 0 10px; }\n"
            "    table { width:100%; border-collapse:collapse; table-layout:fixed; margin-top:10px; }\n"
            "    th, td { border:1px solid var(--line); padding:9px 10px; text-align:left; vertical-align:top; word-break:break-word; }\n"
            "    th { background:#eef3f8; font-weight:650; }\n"
            "    code { font-family: Consolas, monospace; font-size:0.92em; }\n"
            "    .subtitle { color:var(--muted); margin-top:6px; }\n"
            "    .cards { display:grid; grid-template-columns:repeat(auto-fit,minmax(170px,1fr)); gap:10px; margin:18px 0 8px; }\n"
            "    .card { border:1px solid var(--line); border-radius:6px; padding:12px; background:var(--panel); min-height:74px; }\n"
            "    .label { color:var(--muted); font-size:12px; text-transform:uppercase; }\n"
            "    .value { margin-top:5px; font-size:17px; font-weight:650; }\n"
            "    .section { margin-top:18px; }\n"
            "    .status-ok { color:var(--ok); font-weight:650; }\n"
            "    .status-warn { color:var(--warn); font-weight:650; }\n"
            "    .status-bad { color:var(--bad); font-weight:650; }\n"
            "    .bar { height:12px; border-radius:999px; background:#e6ebf0; overflow:hidden; }\n"
            "    .bar > span { display:block; height:100%; background:var(--accent); }\n"
            "    .score-row { display:grid; grid-template-columns:minmax(160px,1fr) 90px minmax(180px,2fr); gap:12px; align-items:center; padding:8px 0; border-bottom:1px solid var(--line); }\n"
            "    .finding { border-left:3px solid var(--accent); padding:8px 10px; margin:8px 0; background:#fbfdff; }\n"
            "    @media (max-width: 720px) { header { padding:24px 18px; } main { padding:20px 14px 36px; } .score-row { grid-template-columns:1fr; gap:4px; } table { font-size:14px; } }\n"
            "  </style>\n"
            "</head>\n"
            "<body>\n"
            f"{body}\n"
            "</main>\n"
            "</body>\n"
            "</html>\n"
        )

    def _hero(self, title: str, subtitle: str) -> str:
        return (
            "<header>"
            f"<h1>{self._escape(title)}</h1>"
            f"<div class=\"subtitle\">{self._escape(subtitle)}</div>"
            "</header><main>"
        )

    def _section(self, title: str, content: str) -> str:
        return f"<section class=\"section\"><h2>{self._escape(title)}</h2>{content}</section>"

    def _summary_cards(self, items: list[tuple[str, str]]) -> str:
        cards = []
        for label, value in items:
            cards.append(
                "<div class=\"card\">"
                f"<div class=\"label\">{self._escape(label)}</div>"
                f"<div class=\"value\">{self._escape(value)}</div>"
                "</div>"
            )
        return "<div class=\"cards\">" + "".join(cards) + "</div>"

    def _dimension_table(self, profile: KernelProfile) -> str:
        rows = ["<table><thead><tr><th>Dimension</th><th>Status</th><th>Evidence</th></tr></thead><tbody>"]
        for dim, spec in DIMENSIONS.items():
            findings = [item for item in profile.dimensions.get(dim, []) if item.confidence != "unconfirmed"]
            status = "confirmed" if findings else "unconfirmed"
            evidence_count = sum(len(item.evidence) for item in findings)
            rows.append(
                "<tr>"
                f"<td>{self._escape(spec.get('title', dim))}</td>"
                f"<td>{self._escape(status)}</td>"
                f"<td>{evidence_count}</td>"
                "</tr>"
            )
        rows.append("</tbody></table>")
        return "".join(rows)

    def _finding_groups(self, result: CompareResult) -> str:
        groups = [
            ("Functional Overlap", result.overlap_points),
            ("Code Similarity", result.code_similarity_points),
            ("Similarities", result.similarities),
            ("Differences", result.differences),
            ("Unique Points", result.unique_points),
        ]
        parts: list[str] = []
        for title, findings in groups:
            parts.append(f"<h3>{self._escape(title)}</h3>")
            if not findings:
                parts.append("<p>No findings.</p>")
                continue
            for finding in findings[:8]:
                parts.append(
                    "<div class=\"finding\">"
                    f"<strong>{self._escape(finding.confidence)}</strong> "
                    f"{self._escape(finding.statement)}"
                    "</div>"
                )
        return "".join(parts)

    def _score_bars(self, result: CompareResult) -> str:
        scores: list[tuple[str, float]] = []
        for note in result.selection_notes:
            match = re.search(r"score=([0-9.]+)", note)
            if not match:
                continue
            label = note.split(":", 1)[0]
            scores.append((label, min(1.0, max(0.0, float(match.group(1))))))
        for finding in result.code_similarity_points:
            match = re.search(r"([01]\.\d+)", finding.statement)
            if match:
                scores.append((finding.statement[:80], min(1.0, max(0.0, float(match.group(1))))))
        if not scores:
            return "<p>No numeric similarity score available.</p>"
        rows = []
        for label, score in scores[:12]:
            rows.append(
                "<div class=\"score-row\">"
                f"<div>{self._escape(label)}</div>"
                f"<div>{score:.2f}</div>"
                f"<div class=\"bar\" aria-label=\"score {score:.2f}\"><span style=\"width:{score * 100:.0f}%\"></span></div>"
                "</div>"
            )
        return "".join(rows)

    def _selfcheck_table(self, summary: dict[str, int | float]) -> str:
        rows = ["<table><tbody>"]
        for key in ("key_findings", "with_evidence", "coverage", "invalid_evidence", "unconfirmed"):
            value = summary[key]
            if isinstance(value, float):
                text = f"{value:.1f}%"
            else:
                text = str(value)
            rows.append(f"<tr><th>{self._escape(key)}</th><td>{self._escape(text)}</td></tr>")
        rows.append("</tbody></table>")
        return "".join(rows)

    def _evidence_table(self, rows: list[dict[str, str]]) -> str:
        if not rows:
            return "<p>No evidence references.</p>"
        parts = [
            "<table><thead><tr>"
            "<th>Status</th><th>Repo</th><th>File</th><th>Lines</th><th>Note</th><th>Snippet</th>"
            "</tr></thead><tbody>"
        ]
        for row in rows:
            status_class = "status-ok" if row["status"] == "ok" else "status-bad"
            parts.append(
                "<tr>"
                f"<td class=\"{status_class}\">{self._escape(row['status'])}</td>"
                f"<td>{self._escape(row['repo_id'])}</td>"
                f"<td><code>{self._escape(row['file'])}</code></td>"
                f"<td>L{self._escape(row['line_start'])}-L{self._escape(row['line_end'])}</td>"
                f"<td>{self._escape(row['note'])}</td>"
                f"<td><code>{self._escape(row['snippet'])}</code></td>"
                "</tr>"
            )
        parts.append("</tbody></table>")
        return "".join(parts)

    def _evidence_rows(self, findings: list[Finding], invalid: set[tuple[str, str, int, int]]) -> list[dict[str, str]]:
        rows: list[dict[str, str]] = []
        seen: set[tuple[str, str, int, int]] = set()
        for finding in findings:
            for evidence in finding.evidence:
                key = self._evidence_key(evidence)
                if key in seen:
                    continue
                seen.add(key)
                rows.append(
                    {
                        "status": "invalid" if key in invalid else "ok",
                        "repo_id": evidence.repo_id,
                        "file": evidence.file,
                        "line_start": str(evidence.line_start),
                        "line_end": str(evidence.line_end),
                        "note": evidence.note or evidence.kind,
                        "snippet": self._compact(evidence.snippet),
                    }
                )
        return rows

    def _profile_findings(self, profile: KernelProfile) -> list[Finding]:
        findings: list[Finding] = []
        if profile.build_system:
            findings.append(profile.build_system)
        for items in profile.dimensions.values():
            findings.extend(items)
        return findings

    def _compare_findings(self, result: CompareResult) -> list[Finding]:
        return (
            result.overlap_points
            + result.code_similarity_points
            + result.similarities
            + result.differences
            + result.unique_points
        )

    def _invalid_profile_evidence(self, profile: KernelProfile, findings: list[Finding]) -> set[tuple[str, str, int, int]]:
        root = Path(profile.meta.root_path) if profile.meta.root_path else None
        invalid = self.checker.invalid_evidence(findings, root, require_root=True)
        return {self._evidence_key(item) for item in invalid}

    def _invalid_compare_evidence(self, result: CompareResult, findings: list[Finding]) -> set[tuple[str, str, int, int]]:
        roots = {repo_id: Path(root) for repo_id, root in result.evidence_roots.items() if repo_id and root}
        invalid = self.checker.invalid_evidence(findings, evidence_roots=roots, require_root=not roots)
        return {self._evidence_key(item) for item in invalid}

    def _evidence_key(self, evidence: Evidence) -> tuple[str, str, int, int]:
        return (evidence.repo_id, evidence.file, evidence.line_start, evidence.line_end)

    def _selfcheck_label(self, summary: dict[str, int | float]) -> str:
        return "ok" if int(summary["invalid_evidence"]) == 0 else "needs review"

    def _compact(self, snippet: str, limit: int = 140) -> str:
        text = " ".join(line.strip() for line in snippet.splitlines() if line.strip())
        if len(text) > limit:
            return text[: limit - 3].rstrip() + "..."
        return text

    def _escape(self, value: object) -> str:
        return html.escape(str(value), quote=True)
