"""Render the KernelSage contest-works review site from site-data.

Produces a self-contained static site (no external/CDN dependencies):

    index.html                      card grid with year tabs
    assets/style.css, app.js        shared styling + interactions
    reports/<id>.describe.html      per-work describe report
    reports/<id>.devhistory.html    per-work development-history report
    reports/<id>.compareN.html      per-work 1v1 comparison reports
    baseline.html                   baseline reference library
    data/site_data.json             raw site data (for the scoring server / reuse)

Reports open inside a modal <iframe>, which keeps the index light and works both
over http(s) and (best-effort) over file://.
"""

from __future__ import annotations

import html
import json
import re
from pathlib import Path
from typing import Any


# ---------------------------------------------------------------------------
# Minimal, dependency-free Markdown -> HTML for our report dialect.
# Supports: # headings, > blockquote, - lists, | tables |, **bold**, `code`,
# --- rules, and paragraphs. Good enough for describe/compare/dev-history docs.
# ---------------------------------------------------------------------------
_BOLD_RE = re.compile(r"\*\*(.+?)\*\*")
_CODE_RE = re.compile(r"`([^`]+)`")
_LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")


def _inline(text: str) -> str:
    out = html.escape(text, quote=False)
    out = _CODE_RE.sub(lambda m: f"<code>{m.group(1)}</code>", out)
    out = _BOLD_RE.sub(lambda m: f"<strong>{m.group(1)}</strong>", out)
    out = _LINK_RE.sub(lambda m: f'<a href="{html.escape(m.group(2), quote=True)}" target="_blank" rel="noopener">{m.group(1)}</a>', out)
    return out


def markdown_to_html(md: str) -> str:
    lines = md.splitlines()
    html_parts: list[str] = []
    i = 0
    n = len(lines)
    list_open = False
    para: list[str] = []

    def flush_para() -> None:
        nonlocal para
        if para:
            html_parts.append(f"<p>{_inline(' '.join(para))}</p>")
            para = []

    def close_list() -> None:
        nonlocal list_open
        if list_open:
            html_parts.append("</ul>")
            list_open = False

    while i < n:
        line = lines[i]
        stripped = line.strip()

        if not stripped:
            flush_para()
            close_list()
            i += 1
            continue

        heading = re.match(r"^(#{1,6})\s+(.*)$", stripped)
        if heading:
            flush_para(); close_list()
            level = len(heading.group(1))
            html_parts.append(f"<h{level}>{_inline(heading.group(2))}</h{level}>")
            i += 1
            continue

        if stripped.startswith(">"):
            flush_para(); close_list()
            html_parts.append(f"<blockquote>{_inline(stripped.lstrip('> ').rstrip())}</blockquote>")
            i += 1
            continue

        if re.match(r"^(-{3,}|\*{3,})$", stripped):
            flush_para(); close_list()
            html_parts.append("<hr>")
            i += 1
            continue

        # Tables: a header row followed by a |---|---| separator.
        if stripped.startswith("|") and i + 1 < n and re.match(r"^\|?[\s:|-]+\|?$", lines[i + 1].strip()) and "-" in lines[i + 1]:
            flush_para(); close_list()
            header = [c.strip() for c in stripped.strip("|").split("|")]
            i += 2
            rows: list[list[str]] = []
            while i < n and lines[i].strip().startswith("|"):
                rows.append([c.strip() for c in lines[i].strip().strip("|").split("|")])
                i += 1
            thead = "".join(f"<th>{_inline(c)}</th>" for c in header)
            tbody = "".join("<tr>" + "".join(f"<td>{_inline(c)}</td>" for c in row) + "</tr>" for row in rows)
            html_parts.append(f"<table><thead><tr>{thead}</tr></thead><tbody>{tbody}</tbody></table>")
            continue

        bullet = re.match(r"^[-*]\s+(.*)$", stripped)
        if bullet:
            flush_para()
            if not list_open:
                html_parts.append("<ul>")
                list_open = True
            html_parts.append(f"<li>{_inline(bullet.group(1))}</li>")
            i += 1
            continue

        # indented sub-bullet -> treat as nested-ish list item
        sub = re.match(r"^\s+[-*]\s+(.*)$", line)
        if sub and list_open:
            html_parts.append(f"<li class=\"sub\">{_inline(sub.group(1))}</li>")
            i += 1
            continue

        para.append(stripped)
        i += 1

    flush_para()
    close_list()
    return "\n".join(html_parts)


def _esc(value: Any) -> str:
    return html.escape(str(value), quote=True)


# ---------------------------------------------------------------------------
# Static asset payloads
# ---------------------------------------------------------------------------
STYLE_CSS = """
:root{
  --ink:#1a2230; --muted:#64748b; --line:#e2e8f0; --panel:#f8fafc;
  --brand:#0f766e; --brand-dark:#115e59; --brand-soft:#ccfbf1;
  --ok:#15803d; --warn:#b45309; --bad:#b91c1c; --bg:#eef2f6;
  --chip:#eef2ff; --chip-ink:#3730a3;
}
*{box-sizing:border-box;}
body{margin:0;font-family:"Segoe UI","Microsoft YaHei",Arial,sans-serif;color:var(--ink);background:var(--bg);line-height:1.6;}
a{color:var(--brand-dark);}
header.topbar{position:sticky;top:0;z-index:30;background:linear-gradient(120deg,var(--brand) 0%,var(--brand-dark) 100%);color:#fff;
  padding:18px 28px;box-shadow:0 2px 10px rgba(15,23,42,.18);}
.topbar h1{margin:0;font-size:24px;font-weight:800;letter-spacing:1px;display:flex;align-items:center;gap:12px;}
.topbar .sub{margin-top:4px;font-size:13px;opacity:.85;}
.topbar .nav{margin-left:auto;display:flex;gap:14px;align-items:center;}
.topbar .nav a{color:#fff;text-decoration:none;font-size:18px;font-weight:700;padding:12px 28px;border-radius:12px;
  background:rgba(255,255,255,.15);border:2px solid rgba(255,255,255,.35);transition:all .25s ease;
  display:inline-flex;align-items:center;gap:8px;letter-spacing:.5px;cursor:pointer;}
.topbar .nav a:hover{background:rgba(255,255,255,.35);border-color:rgba(255,255,255,.7);
  transform:translateY(-2px);box-shadow:0 6px 20px rgba(0,0,0,.3);}
.topbar .nav a.active{background:#fff;color:var(--brand-dark);border-color:#fff;font-weight:800;
  box-shadow:0 4px 16px rgba(0,0,0,.2);transform:scale(1.02);}
.topbar .nav a.active:hover{background:#f0fdfa;box-shadow:0 6px 22px rgba(0,0,0,.25);}
.topbar .row{display:flex;align-items:flex-end;gap:18px;max-width:1320px;margin:0 auto;}
main{max-width:1320px;margin:0 auto;padding:20px 24px 60px;}

.tabs{display:flex;gap:10px;margin:18px 0 6px;flex-wrap:wrap;align-items:center;}
.tab{padding:9px 22px;border:1px solid var(--line);background:#fff;border-radius:999px;cursor:pointer;font-size:15px;font-weight:600;color:var(--muted);}
.tab.active{background:var(--brand);color:#fff;border-color:var(--brand);box-shadow:0 2px 8px rgba(15,118,110,.3);}
.tab .n{font-size:12px;opacity:.8;margin-left:6px;}
.toolbar{margin-left:auto;display:flex;gap:10px;align-items:center;}
.toolbar input{padding:8px 12px;border:1px solid var(--line);border-radius:8px;font-size:14px;min-width:220px;}

.year-meta{color:var(--muted);font-size:13px;margin:4px 0 14px;}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(360px,1fr));gap:18px;}
.empty{padding:50px;text-align:center;color:var(--muted);background:#fff;border:1px dashed var(--line);border-radius:12px;}

.card{background:#fff;border:1px solid var(--line);border-radius:14px;overflow:hidden;display:flex;flex-direction:column;
  box-shadow:0 1px 3px rgba(15,23,42,.06);transition:transform .12s ease,box-shadow .12s ease;}
.card:hover{transform:translateY(-2px);box-shadow:0 8px 22px rgba(15,23,42,.12);}
.card .hd{background:linear-gradient(120deg,#0f766e0d,#0f766e1a);padding:16px 18px 12px;border-bottom:1px solid var(--line);}
.card .entry{font-size:22px;font-weight:800;letter-spacing:.5px;color:var(--brand-dark);word-break:break-all;}
.card .chips{margin-top:8px;display:flex;flex-wrap:wrap;gap:6px;}
.chip{font-size:12px;padding:2px 9px;border-radius:999px;background:var(--chip);color:var(--chip-ink);font-weight:600;}
.chip.ok{background:#dcfce7;color:var(--ok);} .chip.warn{background:#fef3c7;color:var(--warn);} .chip.bad{background:#fee2e2;color:var(--bad);}
.chip.tier{background:#e0f2fe;color:#075985;}

.card .info{padding:12px 18px;font-size:13.5px;}
.card .info dl{display:grid;grid-template-columns:84px 1fr;gap:6px 10px;margin:0;}
.card .info dt{color:var(--muted);}
.card .info dd{margin:0;word-break:break-word;}
.card .info dd a{word-break:break-all;}

.card .reports{padding:12px 18px 16px;border-top:1px dashed var(--line);margin-top:auto;}
.card .reports .grp{margin-bottom:10px;}
.card .reports .grp:last-child{margin-bottom:0;}
.card .reports .gt{font-size:12.5px;font-weight:700;color:var(--muted);text-transform:uppercase;letter-spacing:.5px;margin-bottom:6px;}
.btn{display:inline-flex;align-items:center;gap:6px;padding:7px 13px;border:1px solid var(--brand);background:#fff;color:var(--brand-dark);
  border-radius:8px;font-size:13px;font-weight:600;cursor:pointer;margin:0 6px 6px 0;}
.btn:hover{background:var(--brand);color:#fff;}
.btn.solid{background:var(--brand);color:#fff;}
.btn.solid:hover{background:var(--brand-dark);}
.btn small{font-weight:500;opacity:.8;}

/* modal */
.modal{position:fixed;inset:0;background:rgba(15,23,42,.55);display:none;z-index:100;}
.modal.open{display:flex;}
.modal .panel{margin:auto;width:min(1040px,94vw);height:88vh;background:#fff;border-radius:12px;display:flex;flex-direction:column;overflow:hidden;box-shadow:0 18px 50px rgba(0,0,0,.4);}
.modal .mhd{display:flex;align-items:center;gap:12px;padding:12px 18px;border-bottom:1px solid var(--line);background:var(--panel);}
.modal .mhd .t{font-weight:700;font-size:15px;}
.modal .mhd .x{margin-left:auto;cursor:pointer;border:none;background:#fff;border:1px solid var(--line);border-radius:8px;padding:6px 12px;font-size:14px;}
.modal iframe{flex:1;border:0;width:100%;}

/* baseline + report pages */
.doc{max-width:1040px;margin:0 auto;background:#fff;padding:30px 40px 60px;}
.doc h1{font-size:26px;border-bottom:2px solid var(--brand);padding-bottom:8px;}
.doc h2{font-size:20px;margin-top:28px;border-left:4px solid var(--brand);padding-left:10px;}
.doc h3{font-size:16px;margin-top:20px;color:var(--brand-dark);}
.doc table{border-collapse:collapse;width:100%;margin:12px 0;font-size:14px;}
.doc th,.doc td{border:1px solid var(--line);padding:7px 10px;text-align:left;vertical-align:top;}
.doc th{background:#eef3f8;}
.doc code{background:#f1f5f9;padding:1px 5px;border-radius:4px;font-family:Consolas,monospace;font-size:.92em;}
.doc blockquote{margin:10px 0;padding:8px 14px;background:#fffbeb;border-left:4px solid var(--warn);color:#78350f;}
.doc ul{padding-left:22px;} .doc li.sub{list-style:circle;margin-left:18px;}
.doc hr{border:none;border-top:1px solid var(--line);margin:18px 0;}
.footer{color:var(--muted);font-size:12px;text-align:center;padding:24px;}
@media(max-width:640px){.grid{grid-template-columns:1fr;}.topbar .row{flex-wrap:wrap;}.toolbar input{min-width:140px;}}
"""

APP_JS = """
function openReport(src, title){
  var m=document.getElementById('modal');
  document.getElementById('modal-title').textContent=title||'报告';
  document.getElementById('modal-frame').src=src;
  m.classList.add('open');
}
function closeReport(){
  var m=document.getElementById('modal');
  m.classList.remove('open');
  document.getElementById('modal-frame').src='about:blank';
}
function showYear(y){
  document.querySelectorAll('.year-panel').forEach(function(p){p.style.display = (p.dataset.year===y)?'block':'none';});
  document.querySelectorAll('.tab').forEach(function(t){t.classList.toggle('active', t.dataset.year===y);});
  try{localStorage.setItem('ks-year', y);}catch(e){}
}
function filterCards(q){
  q=(q||'').trim().toLowerCase();
  document.querySelectorAll('.year-panel').forEach(function(panel){
    panel.querySelectorAll('.card').forEach(function(c){
      c.style.display = (!q || c.dataset.search.indexOf(q)>=0) ? '' : 'none';
    });
  });
}
document.addEventListener('keydown',function(e){if(e.key==='Escape')closeReport();});
document.addEventListener('DOMContentLoaded',function(){
  var tabs=document.querySelectorAll('.tab');
  var saved=null; try{saved=localStorage.getItem('ks-year');}catch(e){}
  var first = (saved && document.querySelector('.tab[data-year="'+saved+'"]')) ? saved : (tabs[0]?tabs[0].dataset.year:null);
  if(first) showYear(first);
  var m=document.getElementById('modal');
  if(m) m.addEventListener('click',function(e){if(e.target===m)closeReport();});
});
"""


class SiteRenderer:
    def render(self, site_data: dict[str, Any], out_dir: Path) -> None:
        out_dir = Path(out_dir)
        (out_dir / "assets").mkdir(parents=True, exist_ok=True)
        (out_dir / "reports").mkdir(parents=True, exist_ok=True)
        (out_dir / "data").mkdir(parents=True, exist_ok=True)

        (out_dir / "assets" / "style.css").write_text(STYLE_CSS, encoding="utf-8")
        (out_dir / "assets" / "app.js").write_text(APP_JS, encoding="utf-8")
        (out_dir / "data" / "site_data.json").write_text(
            json.dumps(site_data, ensure_ascii=False, indent=2), encoding="utf-8"
        )

        # per-work report pages
        for year in site_data.get("years", []):
            for project in year.get("projects", []):
                self._write_reports(out_dir, project)

        (out_dir / "index.html").write_text(self._index_page(site_data), encoding="utf-8")
        (out_dir / "baseline.html").write_text(self._baseline_page(site_data), encoding="utf-8")

    # ---- report files -----------------------------------------------------
    def _write_reports(self, out_dir: Path, project: dict[str, Any]) -> None:
        rid = project["repo_id"]
        reports = project["reports"]
        rdir = out_dir / "reports"
        rdir.joinpath(f"{rid}.describe.html").write_text(
            self._doc_page(f"{project['name']} 描述报告", markdown_to_html(reports["describe_md"])), encoding="utf-8")
        rdir.joinpath(f"{rid}.devhistory.html").write_text(
            self._doc_page(f"{project['name']} 开发历史报告", markdown_to_html(reports["dev_history_md"])), encoding="utf-8")
        for cmp in reports["compares"]:
            rdir.joinpath(f"{rid}.compare{cmp['index']}.html").write_text(
                self._doc_page(f"{project['name']} vs {cmp['target_name']} 比较报告", markdown_to_html(cmp["report_md"])),
                encoding="utf-8")

    # ---- index ------------------------------------------------------------
    def _index_page(self, site_data: dict[str, Any]) -> str:
        years = site_data.get("years", [])
        tabs = "".join(
            f'<button class="tab" data-year="{_esc(y["year"])}" onclick="showYear(\'{_esc(y["year"])}\')">'
            f'{_esc(y["year"])} <span class="n">{y["count"]} 个作品</span></button>'
            for y in years
        )
        panels = "".join(self._year_panel(y) for y in years)
        body = f"""
<main>
  <div class="tabs">
    {tabs}
    <div class="toolbar">
      <input type="text" placeholder="搜索 编号/学校/队伍/作品…" oninput="filterCards(this.value)">
    </div>
  </div>
  {panels}
</main>
{self._modal()}
"""
        return self._shell(site_data, body, active="works")

    def _year_panel(self, year: dict[str, Any]) -> str:
        if not year["projects"]:
            cards = '<div class="empty">本年度暂无输入作品。<br>将今年的参赛仓库放入输入目录并重新生成站点即可在此显示。</div>'
        else:
            cards = '<div class="grid">' + "".join(self._card(p) for p in year["projects"]) + "</div>"
        return f'<section class="year-panel" data-year="{_esc(year["year"])}" style="display:none">{cards}</section>'

    def _card(self, p: dict[str, Any]) -> str:
        search = " ".join(str(x).lower() for x in [p["entry_no"], p["name"], p["school"], p["team_name"], p["year"]])
        risk_chip = ""
        compares = p["reports"]["compares"]
        top_overlap = compares[0]["overlap_score"] if compares else 0
        if top_overlap >= 60:
            risk_chip = '<span class="chip bad">最高重合度 高</span>'
        elif top_overlap >= 30:
            risk_chip = '<span class="chip warn">最高重合度 中</span>'
        elif compares:
            risk_chip = '<span class="chip ok">最高重合度 低</span>'

        repo_url = p["repo_url"]
        repo_html = f'<a href="{_esc(repo_url)}" target="_blank" rel="noopener">{_esc(repo_url)}</a>' if str(repo_url).startswith("http") else _esc(repo_url)

        # report buttons
        cmp_btns = "".join(
            f'<button class="btn" onclick="openReport(\'reports/{_esc(p["repo_id"])}.compare{c["index"]}.html\','
            f"'{_esc(p['name'])} vs {_esc(c['target_name'])}')\">"
            f'{_esc(c["label"])}<small>vs {_esc(c["target_name"])}</small></button>'
            for c in compares
        ) or '<span class="chip">暂无可比较的历史仓库</span>'

        return f"""
<article class="card" data-search="{_esc(search)}">
  <div class="hd">
    <div class="entry">{_esc(p["entry_no"])}</div>
    <div class="chips">
      <span class="chip tier">{_esc(p["source_tier_label"])}</span>
      <span class="chip">成熟度 {_esc(p["maturity"]["level_short"])} · {_esc(p["maturity"]["score"])}/100</span>
      {risk_chip}
    </div>
  </div>
  <div class="info">
    <dl>
      <dt>年份</dt><dd>{_esc(p["year"])}</dd>
      <dt>学校</dt><dd>{_esc(p["school"])}</dd>
      <dt>队伍名称</dt><dd>{_esc(p["team_name"])}</dd>
      <dt>比赛名称</dt><dd>{_esc(p["contest_name"])}</dd>
      <dt>子赛道</dt><dd>{_esc(p["subtrack"])}</dd>
      <dt>Repo 地址</dt><dd>{repo_html}</dd>
      <dt>镜像克隆</dt><dd><code>{_esc(p["clone_cmd"])}</code></dd>
    </dl>
  </div>
  <div class="reports">
    <div class="grp">
      <div class="gt">作品描述报告</div>
      <button class="btn solid" onclick="openReport('reports/{_esc(p["repo_id"])}.describe.html','{_esc(p["name"])} 描述报告')">查看描述报告</button>
    </div>
    <div class="grp">
      <div class="gt">开发历史报告</div>
      <button class="btn" onclick="openReport('reports/{_esc(p["repo_id"])}.devhistory.html','{_esc(p["name"])} 开发历史')">查看开发历史</button>
    </div>
    <div class="grp">
      <div class="gt">比较报告（与重合/重复率最高的仓库）</div>
      {cmp_btns}
    </div>
  </div>
</article>
"""

    def _modal(self) -> str:
        return """
<div class="modal" id="modal">
  <div class="panel">
    <div class="mhd"><span class="t" id="modal-title">报告</span>
      <button class="x" onclick="closeReport()">关闭 ✕</button></div>
    <iframe id="modal-frame" src="about:blank"></iframe>
  </div>
</div>
"""

    # ---- baseline ---------------------------------------------------------
    def _baseline_page(self, site_data: dict[str, Any]) -> str:
        baseline = site_data.get("baseline", {})
        repos = baseline.get("repos", [])

        groups: dict[str, list[dict[str, Any]]] = {}
        for r in repos:
            yr = str(r.get("year") or "经典/教学基线")
            groups.setdefault(yr, []).append(r)
        sorted_years = sorted(groups.keys(), key=lambda y: (0 if y[0].isdigit() else 1, y))

        sections: list[str] = []
        for yr in sorted_years:
            items = groups[yr]
            rows = "".join(
                f"<tr><td><code>{_esc(r['repo_id'])}</code></td><td>{_esc(r['name'])}</td>"
                f"<td>{_esc(r['source_tier_label'])}</td><td>{_esc('/'.join(r['arch']) if r['arch'] else '-')}</td>"
                f"<td>{_esc(r.get('language_primary') or '-')}</td><td>{_esc(r.get('school') or '-')}</td>"
                f"<td>{_esc(r.get('loc') if r.get('loc') is not None else '-')}</td></tr>"
                for r in items
            )
            sections.append(
                f"<h2>{_esc(yr)}（{len(items)} 个）</h2>"
                f"<table><thead><tr><th>仓库 ID</th><th>名称</th><th>来源等级</th><th>架构</th><th>主语言</th><th>学校</th><th>LOC</th></tr></thead>"
                f"<tbody>{rows}</tbody></table>"
            )

        body = f"""
<main><div class="doc">
  <h1>历史基线参考库（{baseline.get('count',0)} 个）</h1>
  <blockquote>基线库收录历届操作系统大赛参赛作品及经典教学内核，用于对今年输入作品进行相似性与重合度比较。其中 <code>已核验获奖案例</code> 已确认获奖信息，其余均为确认的历届参赛作品或经典教学/架构参考样本。</blockquote>
  {"".join(sections)}
</div></main>
"""
        return self._shell(site_data, body, active="baseline")

    # ---- shared shell / report doc ---------------------------------------
    def _shell(self, site_data: dict[str, Any], body: str, *, active: str) -> str:
        nav = (
            f'<a href="index.html" class="{"active" if active=="works" else ""}">📋 作品展示</a>'
            f'<a href="baseline.html" class="{"active" if active=="baseline" else ""}">📚 基线库</a>'
        )
        return f"""<!doctype html>
<html lang="zh-CN"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{_esc(site_data.get('contest_name','操作系统竞赛'))}作品展示</title>
<link rel="stylesheet" href="assets/style.css">
</head><body>
<header class="topbar"><div class="row">
  <div>
    <h1>🖥️ 操作系统竞赛作品展示</h1>
    <div class="sub">{_esc(site_data.get('contest_name','操作系统大赛'))} · 内核实现赛道作品智能分析与比较 · 生成时间 {_esc(site_data.get('generated_at',''))}</div>
  </div>
  <nav class="nav">{nav}</nav>
</div></header>
{body}
<div class="footer">KernelSage 评审辅助系统生成 · 所有相似/重合线索均为人工复核入口，系统不直接裁定抄袭。</div>
<script src="assets/app.js"></script>
</body></html>"""

    def _doc_page(self, title: str, body_html: str) -> str:
        return f"""<!doctype html>
<html lang="zh-CN"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{_esc(title)}</title>
<style>{STYLE_CSS}</style>
</head><body style="background:#fff">
<div class="doc">{body_html}</div>
</body></html>"""
