# -*- coding: utf-8 -*-
"""Apply extracted 2026 team/school metadata to the site input manifest.

The input files under data/inputs are local working data and are ignored by git.
This script is intentionally conservative:
  * school uses direct document evidence first;
  * if a team-id school prefix has non-conflicting direct evidence, remaining
    works with that prefix can inherit that school with an explicit source note;
  * team names only come from explicit labels or official-looking table rows.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INPUTS = ROOT / "data" / "inputs"
SITE_INPUTS = INPUTS / "2026-site-inputs.json"
EXTRACT = INPUTS / "2026-extract-report.json"
AUDIT = INPUTS / "2026-metadata-audit.json"
SAMPLES = ROOT / "data" / "samples" / "2026"

FALSE_SCHOOL = {
    # School mention comes from imported xv6-k210 historical report, not this team.
    "collected2026-t2026100019911468-282",
}
DROP_TEAM = {
    # Captured from boilerplate: "???????..."
    "collected2026-t2026104229910571-2627",
}
TEAM_OVERRIDES = {
    # PDF extraction confused ? with ?; markdown speech has the correct spelling.
    "collected2026-t202610359999721-2135": "\u9676\u9149\u518c",
    "collected2026-t202610486999642-1278": "WHUSP",
}
SCHOOL_OVERRIDES = {
    # README logo alt is hdu; LaTeX title page contains ????????.
    "collected2026-t2026103369910030-2019": "\u676d\u5dde\u7535\u5b50\u79d1\u6280\u5927\u5b66",
}
TEAM_BAD_SUBSTR = (
    "\u8d5b\u9053", "\u6bd4\u8d5b", "\u7ade\u8d5b", "\u64cd\u4f5c\u7cfb\u7edf", "\u5185\u6838",
    "\u63d0\u4ea4", "\u7f16\u53f7", "\u4fe1\u606f", "\u9875\u9762\u663e\u793a", "\u5b66\u6821",
)
ENTRY_RE = re.compile(r"T\d{4}(\d{5})")
FULL_ENTRY_RE = re.compile(r"T2026\d{9,}(?:-\d+)?", re.I)


def entry_prefix(entry_no: str | None) -> str | None:
    if not entry_no:
        return None
    m = ENTRY_RE.match(entry_no)
    return m.group(1) if m else None


def clean(v: str | None) -> str | None:
    if not v:
        return None
    v = re.sub(r"<[^>]+>", "", v)
    v = re.sub(r"[*_`#>]", "", v).strip()
    v = re.sub(r"^[\-\u2014\uff1a:|\s]+", "", v)
    v = re.split(r"[\uff0c,\u3002\uff1b;\n\r]", v, maxsplit=1)[0]
    v = v.strip(" \t\uff1a:-\u2014|)\uff09(\uff08\u3010\u3011[]")
    return v or None


def valid_team(v: str | None) -> str | None:
    v = clean(v)
    if not v or len(v) < 2 or len(v) > 24:
        return None
    if any(b in v for b in TEAM_BAD_SUBSTR):
        return None
    if re.fullmatch(r"T\d{6,}[-\d]*", v, re.I):
        return None
    return v


def valid_title(v: str | None) -> str | None:
    v = clean(v)
    if not v or len(v) > 90:
        return None
    if v.startswith("1.") or v.startswith("1\uff0e"):
        return None
    if v in {"README", "readme"}:
        return None
    return v


def direct_school_map(extract: dict[str, dict]) -> dict[str, str]:
    direct: dict[str, str] = {}
    for repo_id, info in extract.items():
        if repo_id in FALSE_SCHOOL:
            continue
        school = clean(info.get("school"))
        if school and info.get("school_confidence") in {"high", "medium"}:
            direct[repo_id] = school
    direct.update(SCHOOL_OVERRIDES)
    return direct


def prefix_school_map(inputs: list[dict], direct: dict[str, str]) -> dict[str, str]:
    by_prefix: dict[str, dict[str, int]] = {}
    for item in inputs:
        repo_id = item["repo_id"]
        school = direct.get(repo_id)
        prefix = entry_prefix(item.get("entry_no"))
        if not school or not prefix:
            continue
        by_prefix.setdefault(prefix, {})[school] = by_prefix.setdefault(prefix, {}).get(school, 0) + 1
    out: dict[str, str] = {}
    for prefix, counts in by_prefix.items():
        if len(counts) == 1:
            out[prefix] = next(iter(counts))
    return out


def table_team_map() -> dict[str, str]:
    rows: dict[str, str] = {}
    for p in SAMPLES.rglob("*.md"):
        if any(part in {".git", "vendor", "target", "node_modules"} for part in p.parts):
            continue
        try:
            text = p.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        for line in text.splitlines():
            if "|" not in line or "T2026" not in line:
                continue
            parts = [x.strip(" *`") for x in line.strip().strip("|").split("|")]
            idx = None
            entry = None
            for i, part in enumerate(parts):
                m = FULL_ENTRY_RE.search(part)
                if m:
                    idx = i
                    entry = m.group(0).split("-")[0]
                    break
            if idx is None or not entry or idx + 1 >= len(parts):
                continue
            team = valid_team(parts[idx + 1])
            school = clean(parts[idx + 2]) if idx + 2 < len(parts) else None
            if team and school and school.endswith(("\u5927\u5b66", "\u5b66\u9662")):
                rows.setdefault(entry, team)
    return rows


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    site_data = json.loads(SITE_INPUTS.read_text(encoding="utf-8"))
    extract = json.loads(EXTRACT.read_text(encoding="utf-8"))
    items = site_data.get("2026", [])
    direct = direct_school_map(extract)
    prefix_map = prefix_school_map(items, direct)
    team_by_entry = table_team_map()

    audit = {"items": [], "school_counts": {}, "team_counts": {}}
    school_direct = school_prefix = school_missing = 0
    team_label = team_table = team_missing = 0

    for item in items:
        repo_id = item["repo_id"]
        info = extract.get(repo_id, {})
        source = None
        school = direct.get(repo_id)
        if school:
            source = "direct"
            school_direct += 1
        else:
            prefix = entry_prefix(item.get("entry_no"))
            if prefix and prefix in prefix_map:
                school = prefix_map[prefix]
                source = f"entry-prefix:{prefix}"
                school_prefix += 1
        if school:
            item["school"] = school
        else:
            item.pop("school", None)
            school_missing += 1

        team = TEAM_OVERRIDES.get(repo_id)
        if not team and repo_id not in DROP_TEAM:
            team = valid_team(info.get("label_team"))
        team_source = None
        if team:
            team_source = "label"
            team_label += 1
        elif item.get("entry_no") in team_by_entry:
            team = team_by_entry[item["entry_no"]]
            team_source = "table"
            team_table += 1
        else:
            team_missing += 1
        if team:
            item["team"] = team
        else:
            # keep original entry-number fallback already present in the manifest
            pass

        title = valid_title(info.get("label_project")) or valid_title(info.get("readme_h1"))
        if title:
            item["name"] = title

        audit["items"].append({
            "repo_id": repo_id,
            "entry_no": item.get("entry_no"),
            "school": school,
            "school_source": source,
            "team": team,
            "team_source": team_source,
            "title": title,
        })

    audit["school_counts"] = {"direct": school_direct, "entry_prefix": school_prefix, "missing": school_missing}
    audit["team_counts"] = {"label": team_label, "table": team_table, "missing": team_missing}
    SITE_INPUTS.write_text(json.dumps(site_data, ensure_ascii=False, indent=2), encoding="utf-8")
    AUDIT.write_text(json.dumps(audit, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"school": audit["school_counts"], "team": audit["team_counts"], "audit": str(AUDIT)}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
