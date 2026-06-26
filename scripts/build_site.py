"""Build the KernelSage contest-works review website.

Usage examples
--------------
# 1) Quick demo using repos already in data/samples as this-year inputs:
python scripts/build_site.py --demo --out site

# 2) Real inputs from a folder of year subdirectories:
#    inputs/2025/<repo>/...  inputs/2026/<repo>/...
python scripts/build_site.py --inputs inputs --history data/samples --out site

# 3) Real inputs described by a JSON manifest (richest metadata):
python scripts/build_site.py --inputs-manifest inputs/works.json --out site

Inputs manifest format:
{
  "2025": [
    {"repo_id": "team-xxx", "path": "inputs/2025/team-xxx",
     "entry_no": "T202510003995291", "school": "清华大学", "team": "Starry",
     "members": "张三、李四、王五", "subtrack": "内核实现赛道",
     "url": "https://gitlab.eduxiji.net/..."}
  ],
  "2026": []
}
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from os_agent.web_console import WebConsoleBuilder  # noqa: E402
from os_agent.web_render import SiteRenderer  # noqa: E402

SAMPLES_DIR = ROOT / "data" / "samples"
PROFILES_DIR = ROOT / "data" / "profiles"

# For --demo: which local sample repos act as each year's "input" batch.
DEMO_INPUTS = {
    "2025": ["oskernel2024-aabcb", "oskernel2024-hfut666", "oskernel2024-nqos", "oskernel2024-ouye"],
    "2026": ["award2024-huster-proj306", "award2024-moca-mola-proj207", "award2024-tangram-proj226"],
}


def _meta_overrides(repo_dir: Path) -> dict:
    meta_path = repo_dir / ".kernelsage_meta.json"
    if not meta_path.exists():
        return {}
    try:
        data = json.loads(meta_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    return {
        "team": data.get("team"),
        "school": data.get("school"),
        "members": data.get("members"),
        "subtrack": data.get("subtrack"),
        "url": data.get("url"),
        "year": data.get("year"),
    }


def discover_inputs(args: argparse.Namespace) -> dict[str, list[dict]]:
    if args.inputs_manifest:
        data = json.loads(Path(args.inputs_manifest).read_text(encoding="utf-8"))
        # normalise: ensure each item has an absolute path
        for items in data.values():
            for item in items:
                item["path"] = str(Path(item["path"]).resolve())
        return data

    if args.demo:
        out: dict[str, list[dict]] = {}
        for year, repo_ids in DEMO_INPUTS.items():
            out[year] = []
            for repo_id in repo_ids:
                repo_dir = SAMPLES_DIR / repo_id
                if not repo_dir.exists():
                    continue
                item = {"repo_id": repo_id, "path": str(repo_dir.resolve())}
                item.update({k: v for k, v in _meta_overrides(repo_dir).items() if v})
                out[year].append(item)
        return out

    if args.inputs:
        base = Path(args.inputs)
        out = {}
        for year_dir in sorted(p for p in base.iterdir() if p.is_dir()):
            year = year_dir.name
            out[year] = []
            for repo_dir in sorted(p for p in year_dir.iterdir() if p.is_dir() and not p.name.startswith(".")):
                item = {"repo_id": repo_dir.name, "path": str(repo_dir.resolve())}
                item.update({k: v for k, v in _meta_overrides(repo_dir).items() if v})
                out[year].append(item)
        return out

    raise SystemExit("provide one of --demo / --inputs <dir> / --inputs-manifest <json>")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build the contest-works review website")
    parser.add_argument("--demo", action="store_true", help="use repos in data/samples as this-year inputs")
    parser.add_argument("--inputs", help="folder with <year>/<repo> subdirectories")
    parser.add_argument("--inputs-manifest", help="JSON manifest describing input works by year")
    parser.add_argument("--history", default=str(SAMPLES_DIR), help="baseline (history) samples dir")
    parser.add_argument("--out", default=str(ROOT / "site"), help="output site directory")
    parser.add_argument("--years", nargs="*", default=["2025", "2026"], help="year tabs to always render")
    parser.add_argument("--top-n", type=int, default=3, help="number of comparison reports per work")
    parser.add_argument("--no-cache", action="store_true", help="disable KernelProfile cache")
    args = parser.parse_args(argv)

    inputs_by_year = discover_inputs(args)
    builder = WebConsoleBuilder(
        samples_dir=Path(args.history),
        profiles_dir=None if args.no_cache else PROFILES_DIR,
    )
    print(f"building site data (history={args.history}) ...")
    site_data = builder.build_site_data(
        inputs_by_year, Path(args.history), years=list(args.years), top_n=args.top_n
    )
    out_dir = Path(args.out)
    SiteRenderer().render(site_data, out_dir)

    total = sum(y["count"] for y in site_data["years"])
    print(f"rendered {total} work card(s) across {len(site_data['years'])} year tab(s)")
    for y in site_data["years"]:
        print(f"  - {y['year']}: {y['count']} works")
    print(f"site written to: {out_dir.resolve()}")
    print(f"open: {(out_dir / 'index.html').resolve()}")
    print("serve locally: python scripts/serve_site.py --site " + str(out_dir))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
