"""Render the KernelSage contest-works review site from site-data.

Produces a self-contained static site (no external/CDN dependencies) with an
interactive review console: KPI panel, multi-dimension filter + sort, live
result counter, maturity/risk visualisation, side-by-side comparison, judge
scoring (localStorage + CSV export), dark mode, copy-to-clipboard clone command,
an enhanced report modal, back-to-top, and a searchable baseline library.
"""

from __future__ import annotations

import html
import json
import re
from pathlib import Path
from typing import Any


# ---------------------------------------------------------------------------
# Minimal, dependency-free Markdown -> HTML for our report dialect.
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


def _grade(score: float) -> str:
    if score >= 85:
        return "A"
    if score >= 70:
        return "B"
    if score >= 50:
        return "C"
    return "D"


STYLE_CSS = r"""
:root{
  --ink:#1a2230; --muted:#64748b; --line:#e2e8f0; --panel:#f8fafc; --card:#ffffff;
  --brand:#0f766e; --brand-dark:#115e59; --brand-soft:#ccfbf1;
  --ok:#15803d; --warn:#b45309; --bad:#b91c1c; --bg:#eef2f6;
  --chip:#eef2ff; --chip-ink:#3730a3; --shadow:rgba(15,23,42,.10);
}
html[data-theme="dark"]{
  --ink:#e6edf3; --muted:#9aa7b4; --line:#2b3440; --panel:#161b22; --card:#1c232c;
  --brand:#2dd4bf; --brand-dark:#5eead4; --brand-soft:#134e4a;
  --ok:#4ade80; --warn:#fbbf24; --bad:#f87171; --bg:#0d1117;
  --chip:#1e293b; --chip-ink:#a5b4fc; --shadow:rgba(0,0,0,.5);
}
*{box-sizing:border-box;}
body{margin:0;font-family:"Segoe UI","Microsoft YaHei",Arial,sans-serif;color:var(--ink);background:var(--bg);line-height:1.6;transition:background .25s,color .25s;}
a{color:var(--brand-dark);}
header.topbar{position:sticky;top:0;z-index:30;background:linear-gradient(120deg,var(--brand) 0%,var(--brand-dark) 100%);color:#fff;
  padding:18px 28px;box-shadow:0 2px 10px rgba(15,23,42,.18);}
.topbar h1{margin:0;font-size:24px;font-weight:800;letter-spacing:1px;display:flex;align-items:center;gap:12px;}
.topbar .sub{margin-top:4px;font-size:13px;opacity:.85;}
.topbar .nav{margin-left:auto;display:flex;gap:14px;align-items:center;}
.topbar .nav a{color:#fff;text-decoration:none;font-size:18px;font-weight:700;padding:12px 28px;border-radius:12px;
  background:rgba(255,255,255,.15);border:2px solid rgba(255,255,255,.35);transition:all .25s ease;
  display:inline-flex;align-items:center;gap:8px;letter-spacing:.5px;cursor:pointer;}
.topbar .nav a:hover{background:rgba(255,255,255,.35);border-color:rgba(255,255,255,.7);transform:translateY(-2px);box-shadow:0 6px 20px rgba(0,0,0,.3);}
.topbar .nav a.active{background:#fff;color:var(--brand-dark);border-color:#fff;font-weight:800;box-shadow:0 4px 16px rgba(0,0,0,.2);transform:scale(1.02);}
.topbar .nav .iconbtn{font-size:18px;padding:11px 14px;cursor:pointer;}
.topbar .row{display:flex;align-items:flex-end;gap:18px;max-width:1320px;margin:0 auto;}
main{max-width:1320px;margin:0 auto;padding:20px 24px 70px;}

/* KPI panel */
.kpis{display:grid;grid-template-columns:repeat(auto-fit,minmax(190px,1fr));gap:14px;margin:18px 0 6px;}
.kpi{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:16px 18px;box-shadow:0 1px 3px var(--shadow);}
.kpi .k{font-size:13px;color:var(--muted);display:flex;align-items:center;gap:6px;}
.kpi .v{font-size:30px;font-weight:800;color:var(--brand-dark);margin-top:6px;line-height:1;}
.kpi .v small{font-size:14px;color:var(--muted);font-weight:600;margin-left:4px;}
.overview{display:grid;grid-template-columns:minmax(0,1fr) 360px;gap:16px;margin:18px 0;}
.overview .panel,.history-filter{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:16px;box-shadow:0 1px 3px var(--shadow);}
.overview h2,.history-filter h2{margin:0 0 12px;font-size:17px;color:var(--brand-dark);}
.overview-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:12px;}
.overview-item{border:1px solid var(--line);border-radius:10px;padding:11px 12px;background:var(--panel);}
.overview-item .k{font-size:12px;color:var(--muted);}
.overview-item .v{font-size:22px;font-weight:800;color:var(--ink);margin-top:3px;}
.overview-item .s{font-size:12px;color:var(--muted);margin-top:2px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;}
.radar-wrap{display:grid;grid-template-columns:190px 1fr;gap:12px;align-items:center;}
.radar-wrap svg{width:190px;height:190px;display:block;}
.radar-legend{display:grid;gap:6px;font-size:12px;color:var(--muted);}
.radar-legend b{color:var(--ink);}
.quick-links{display:flex;gap:8px;flex-wrap:wrap;margin-top:12px;}
.quick-links a{display:inline-flex;align-items:center;gap:5px;border:1px solid var(--line);border-radius:8px;padding:7px 10px;background:var(--card);text-decoration:none;font-size:13px;font-weight:650;color:var(--brand-dark);}
.quick-links a:hover{border-color:var(--brand);background:var(--brand);color:#fff;}

.tabs{display:flex;gap:10px;margin:18px 0 6px;flex-wrap:wrap;align-items:center;}
.tab{padding:9px 22px;border:1px solid var(--line);background:var(--card);border-radius:999px;cursor:pointer;font-size:15px;font-weight:600;color:var(--muted);transition:all .2s;}
.tab.active{background:var(--brand);color:#fff;border-color:var(--brand);box-shadow:0 2px 8px rgba(15,118,110,.3);}
.tab .n{font-size:12px;opacity:.8;margin-left:6px;}

.toolbar{display:flex;gap:10px;align-items:center;flex-wrap:wrap;margin:10px 0 4px;padding:12px 14px;background:var(--card);border:1px solid var(--line);border-radius:12px;}
.toolbar input,.toolbar select{padding:8px 12px;border:1px solid var(--line);border-radius:8px;font-size:14px;background:var(--card);color:var(--ink);}
.toolbar input[type=text]{min-width:240px;flex:1;}
.toolbar .seg{display:inline-flex;border:1px solid var(--line);border-radius:8px;overflow:hidden;}
.toolbar .seg button{border:0;background:var(--card);color:var(--muted);padding:7px 12px;font-size:13px;cursor:pointer;border-right:1px solid var(--line);}
.toolbar .seg button:last-child{border-right:0;}
.toolbar .seg button.on{background:var(--brand);color:#fff;font-weight:700;}
.toolbar .lbl{font-size:12.5px;color:var(--muted);margin-right:-4px;}
.toolbar .count{margin-left:auto;font-size:13px;color:var(--muted);}
.toolbar .count b{color:var(--brand-dark);font-size:15px;}
.toolbar .exp{margin-left:8px;}
.btn-mini{border:1px solid var(--brand);background:var(--card);color:var(--brand-dark);border-radius:8px;padding:7px 12px;font-size:13px;font-weight:600;cursor:pointer;}
.btn-mini:hover{background:var(--brand);color:#fff;}

.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(370px,1fr));gap:18px;margin-top:14px;}
.empty{padding:50px;text-align:center;color:var(--muted);background:var(--card);border:1px dashed var(--line);border-radius:12px;}

.card{background:var(--card);border:1px solid var(--line);border-radius:14px;overflow:visible;display:flex;flex-direction:column;
  box-shadow:0 1px 3px var(--shadow);transition:transform .15s ease,box-shadow .15s ease,border-color .15s;position:relative;}
.card:hover,.card:focus-within{transform:translateY(-3px);box-shadow:0 12px 28px var(--shadow);border-color:var(--brand-soft);z-index:20;}
.card.picked{border-color:var(--brand);box-shadow:0 0 0 2px var(--brand-soft);}
.card .hd{background:linear-gradient(120deg,#0f766e0d,#0f766e1a);padding:16px 18px 12px;border-bottom:1px solid var(--line);border-radius:14px 14px 0 0;}
.card .pick{position:absolute;top:12px;right:12px;display:flex;align-items:center;gap:5px;font-size:12px;color:var(--muted);cursor:pointer;user-select:none;}
.card .pick input{width:16px;height:16px;cursor:pointer;accent-color:var(--brand);}
.card .entry{font-size:22px;font-weight:800;letter-spacing:.5px;color:var(--brand-dark);word-break:break-all;padding-right:54px;}
.card .chips{margin-top:8px;display:flex;flex-wrap:wrap;gap:6px;align-items:center;}
.chip{font-size:12px;padding:2px 9px;border-radius:999px;background:var(--chip);color:var(--chip-ink);font-weight:600;}
.chip.ok{background:#dcfce7;color:#166534;} .chip.warn{background:#fef3c7;color:#92400e;} .chip.bad{background:#fee2e2;color:#991b1b;}
.chip.tier{background:#e0f2fe;color:#075985;}
html[data-theme="dark"] .chip.ok{background:#14532d;color:#86efac;}
html[data-theme="dark"] .chip.warn{background:#451a03;color:#fcd34d;}
html[data-theme="dark"] .chip.bad{background:#450a0a;color:#fca5a5;}
html[data-theme="dark"] .chip.tier{background:#0c4a6e;color:#7dd3fc;}

.meters{margin-top:10px;display:grid;gap:7px;}
.meter{display:grid;grid-template-columns:62px 1fr 52px;align-items:center;gap:8px;font-size:12px;color:var(--muted);}
.metric-label{display:inline-flex;align-items:center;gap:4px;white-space:nowrap;}
.info-tip{position:relative;display:inline-flex;align-items:center;justify-content:center;width:15px;height:15px;border:1px solid var(--muted);border-radius:50%;font-size:10px;font-weight:800;line-height:1;color:var(--muted);cursor:help;background:var(--card);}
.info-tip::after{content:attr(data-tip);position:absolute;left:-10px;bottom:calc(100% + 8px);z-index:80;width:240px;max-width:min(260px,calc(100vw - 48px));transform:none;padding:8px 10px;border:1px solid var(--line);border-radius:8px;background:var(--ink);color:var(--card);font-size:12px;font-weight:500;line-height:1.45;white-space:normal;box-shadow:0 10px 24px var(--shadow);opacity:0;pointer-events:none;visibility:hidden;transition:opacity .12s ease,visibility .12s ease;}
.info-tip::before{content:"";position:absolute;left:2px;bottom:calc(100% + 3px);z-index:81;transform:rotate(45deg);width:8px;height:8px;background:var(--ink);opacity:0;visibility:hidden;transition:opacity .12s ease,visibility .12s ease;}
.info-tip:hover::after,.info-tip:hover::before,.info-tip:focus::after,.info-tip:focus::before{opacity:1;visibility:visible;}
.meter .bar{height:9px;border-radius:999px;background:var(--line);overflow:hidden;}
.meter .bar>span{display:block;height:100%;border-radius:999px;}
.meter .bar.mat>span{background:linear-gradient(90deg,#22c55e,#0f766e);}
.meter .bar.risk>span{background:linear-gradient(90deg,#f59e0b,#dc2626);}
.meter .val{text-align:right;font-weight:700;color:var(--ink);}

.card .info{padding:12px 18px;font-size:13.5px;}
.card .info dl{display:grid;grid-template-columns:78px 1fr;gap:6px 10px;margin:0;}
.card .info dt{color:var(--muted);}
.card .info dd{margin:0;word-break:break-word;}
.card .info dd a{word-break:break-all;}
.clone{display:flex;align-items:center;gap:6px;}
.clone code{flex:1;background:var(--panel);padding:3px 7px;border-radius:5px;font-size:12px;word-break:break-all;}
.copybtn{border:1px solid var(--line);background:var(--card);border-radius:6px;padding:3px 8px;font-size:12px;cursor:pointer;color:var(--muted);white-space:nowrap;}
.copybtn:hover{background:var(--brand);color:#fff;border-color:var(--brand);}

.card .reports{padding:12px 18px 16px;border-top:1px dashed var(--line);margin-top:auto;}
.card .reports .grp{margin-bottom:10px;}
.card .reports .grp:last-child{margin-bottom:0;}
.card .reports .gt{font-size:12.5px;font-weight:700;color:var(--muted);text-transform:uppercase;letter-spacing:.5px;margin-bottom:6px;}
.dims{display:flex;flex-wrap:wrap;gap:6px;padding:0 18px 12px;}
.dim{font-size:11.5px;border:1px solid var(--line);border-radius:999px;padding:2px 8px;background:var(--panel);color:var(--muted);}
.dim.ok{border-color:#bbf7d0;background:#f0fdf4;color:#166534;}
.dim.no{border-color:#fecaca;background:#fef2f2;color:#991b1b;}
html[data-theme="dark"] .dim.ok{background:#052e16;color:#86efac;border-color:#166534;}
html[data-theme="dark"] .dim.no{background:#450a0a;color:#fca5a5;border-color:#7f1d1d;}
.explain{border-top:1px dashed var(--line);padding:10px 18px 2px;}
.explain summary{cursor:pointer;font-size:13px;font-weight:800;color:var(--brand-dark);list-style:none;}
.explain summary::-webkit-details-marker{display:none;}
.explain summary::after{content:"展开";float:right;font-size:12px;color:var(--muted);font-weight:600;}
.explain[open] summary::after{content:"收起";}
.explain-list{display:grid;gap:8px;margin-top:10px;}
.explain-item{border:1px solid var(--line);border-radius:10px;background:var(--panel);padding:9px 10px;}
.explain-item .top{display:flex;justify-content:space-between;gap:10px;align-items:flex-start;font-size:13px;font-weight:800;}
.explain-item .meta{font-size:12px;color:var(--muted);margin-top:4px;}
.explain-item .why{display:flex;flex-wrap:wrap;gap:5px;margin-top:8px;}
.explain-item .why span{font-size:11.5px;border-radius:999px;padding:2px 7px;background:var(--chip);color:var(--chip-ink);}
.explain-item .acts{margin-top:8px;display:flex;gap:6px;flex-wrap:wrap;}
.download-row{display:flex;flex-wrap:wrap;gap:6px;margin-top:4px;}
.btn{display:inline-flex;align-items:center;gap:6px;padding:7px 13px;border:1px solid var(--brand);background:var(--card);color:var(--brand-dark);
  border-radius:8px;font-size:13px;font-weight:600;cursor:pointer;margin:0 6px 6px 0;transition:all .15s;}
.btn:hover{background:var(--brand);color:#fff;transform:translateY(-1px);}
.btn.solid{background:var(--brand);color:#fff;}
.btn.solid:hover{background:var(--brand-dark);}
.btn.score{border-color:#7c3aed;color:#7c3aed;}
.btn.score:hover{background:#7c3aed;color:#fff;}
.btn small{font-weight:500;opacity:.8;}
.scored-badge{font-size:11px;background:#7c3aed;color:#fff;padding:1px 7px;border-radius:999px;margin-left:6px;}

/* modal */
.modal{position:fixed;inset:0;background:rgba(15,23,42,.55);display:none;z-index:100;}
.modal.open{display:flex;}
.modal .panel{margin:auto;width:min(1060px,94vw);height:88vh;background:var(--card);border-radius:12px;display:flex;flex-direction:column;overflow:hidden;box-shadow:0 18px 50px rgba(0,0,0,.4);}
.modal .panel.full{width:100vw;height:100vh;border-radius:0;}
.modal .mhd{display:flex;align-items:center;gap:10px;padding:11px 16px;border-bottom:1px solid var(--line);background:var(--panel);}
.modal .mhd .t{font-weight:700;font-size:15px;flex:1;color:var(--ink);}
.modal .mhd button{cursor:pointer;background:var(--card);border:1px solid var(--line);border-radius:8px;padding:6px 11px;font-size:13px;color:var(--ink);}
.modal .mhd button:hover{background:var(--brand);color:#fff;border-color:var(--brand);}
.modal .body{flex:1;position:relative;}
.modal iframe{position:absolute;inset:0;border:0;width:100%;height:100%;background:#fff;}
.modal .spin{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;color:var(--muted);font-size:14px;}
.spinner{width:34px;height:34px;border:3px solid var(--line);border-top-color:var(--brand);border-radius:50%;animation:spin .8s linear infinite;}
@keyframes spin{to{transform:rotate(360deg);}}

/* compare drawer */
.cmpbar{position:fixed;left:50%;transform:translateX(-50%);bottom:20px;z-index:60;background:var(--brand-dark);color:#fff;
  padding:10px 18px;border-radius:999px;box-shadow:0 8px 24px rgba(0,0,0,.3);display:none;align-items:center;gap:14px;font-size:14px;}
.cmpbar.show{display:flex;}
.cmpbar button{background:#fff;color:var(--brand-dark);border:0;border-radius:999px;padding:7px 16px;font-weight:700;cursor:pointer;}
.cmpbar .clear{background:transparent;color:#fff;text-decoration:underline;padding:4px 6px;}
.cmptable{width:100%;border-collapse:collapse;font-size:13.5px;}
.cmptable th,.cmptable td{border:1px solid var(--line);padding:9px 11px;text-align:left;vertical-align:top;}
.cmptable th{background:var(--panel);}
.cmptable td.yes{color:var(--ok);font-weight:700;} .cmptable td.no{color:var(--muted);}
.cmptable .rowhead{background:var(--panel);font-weight:700;color:var(--muted);width:130px;}

/* scoring */
.scorebox{padding:4px 2px;}
.scorebox .crit{margin:12px 0;}
.scorebox .crit .top{display:flex;justify-content:space-between;font-size:14px;margin-bottom:5px;}
.scorebox .crit .top b{color:var(--brand-dark);}
.scorebox .crit .desc{font-size:12px;color:var(--muted);margin-bottom:6px;}
.scorebox input[type=range]{width:100%;accent-color:var(--brand);}
.scorebox .total{font-size:16px;font-weight:800;color:var(--brand-dark);text-align:right;margin-top:6px;}
.scorebox textarea{width:100%;min-height:70px;border:1px solid var(--line);border-radius:8px;padding:8px;font-size:13px;background:var(--card);color:var(--ink);resize:vertical;}
.scorebox .acts{display:flex;gap:10px;margin-top:12px;}

/* doc/baseline */
.doc{max-width:1040px;margin:0 auto;background:var(--card);padding:30px 40px 60px;}
.doc h1{font-size:26px;border-bottom:2px solid var(--brand);padding-bottom:8px;}
.doc h2{font-size:20px;margin-top:28px;border-left:4px solid var(--brand);padding-left:10px;}
.doc h3{font-size:16px;margin-top:20px;color:var(--brand-dark);}
.doc table{border-collapse:collapse;width:100%;margin:12px 0;font-size:14px;}
.doc th,.doc td{border:1px solid var(--line);padding:7px 10px;text-align:left;vertical-align:top;}
.doc th{background:var(--panel);}
.doc code{background:var(--panel);padding:1px 5px;border-radius:4px;font-family:Consolas,monospace;font-size:.92em;}
.doc blockquote{margin:10px 0;padding:8px 14px;background:#fffbeb;border-left:4px solid var(--warn);color:#78350f;}
html[data-theme="dark"] .doc blockquote{background:#1f2937;color:#fcd34d;}
.doc ul{padding-left:22px;} .doc li.sub{list-style:circle;margin-left:18px;}
.bsearch{margin:14px 0;display:flex;gap:10px;flex-wrap:wrap;}
.bsearch input{flex:1;min-width:220px;padding:9px 12px;border:1px solid var(--line);border-radius:8px;font-size:14px;background:var(--card);color:var(--ink);}
.bsearch .count{align-self:center;font-size:13px;color:var(--muted);}
.history-controls{display:flex;gap:10px;flex-wrap:wrap;margin-bottom:12px;}
.history-controls input,.history-controls select{padding:8px 12px;border:1px solid var(--line);border-radius:8px;font-size:14px;background:var(--card);color:var(--ink);}
.history-controls input{min-width:220px;flex:1;}
.history-table-wrap{max-height:360px;overflow:auto;border:1px solid var(--line);border-radius:10px;}
.history-table{width:100%;border-collapse:collapse;font-size:13px;}
.history-table th,.history-table td{border-bottom:1px solid var(--line);padding:8px 10px;text-align:left;vertical-align:top;}
.history-table th{position:sticky;top:0;background:var(--panel);z-index:1;}
.history-table td small{color:var(--muted);}
.split-compare{display:grid;grid-template-columns:1fr 1fr;gap:14px;padding:18px;}
.split-compare .side{border:1px solid var(--line);border-radius:10px;background:var(--panel);padding:14px;}
.split-compare h3{margin:0 0 10px;color:var(--brand-dark);font-size:16px;}
.split-compare dl{display:grid;grid-template-columns:96px 1fr;gap:7px 10px;margin:0;font-size:13px;}
.split-compare dt{color:var(--muted);}.split-compare dd{margin:0;word-break:break-word;}
.hint{font-size:12px;color:var(--muted);margin-top:8px;}
.evidence-mini{margin-top:8px;border-top:1px dashed var(--line);padding-top:8px;font-size:12px;color:var(--muted);}
.evidence-mini summary{cursor:pointer;color:var(--brand-dark);font-weight:700;}
.evidence-mini ul{margin:6px 0 0;padding-left:18px;}

#toTop{position:fixed;right:22px;bottom:22px;z-index:55;width:46px;height:46px;border-radius:50%;border:0;background:var(--brand);color:#fff;
  font-size:20px;cursor:pointer;box-shadow:0 6px 18px rgba(0,0,0,.25);display:none;}
#toTop.show{display:block;}
#toast{position:fixed;left:50%;bottom:80px;transform:translateX(-50%);background:#111827;color:#fff;padding:10px 18px;border-radius:10px;font-size:14px;z-index:200;opacity:0;transition:opacity .25s;pointer-events:none;}
#toast.show{opacity:1;}
.footer{color:var(--muted);font-size:12px;text-align:center;padding:24px;}
@media(max-width:920px){.overview{grid-template-columns:1fr;}.radar-wrap{grid-template-columns:1fr;}.radar-wrap svg{margin:auto;}.split-compare{grid-template-columns:1fr;}}
@media(max-width:640px){.grid{grid-template-columns:1fr;}.topbar .row{flex-wrap:wrap;}.toolbar input[type=text]{min-width:140px;}.history-table-wrap{max-height:420px;}.overview-grid{grid-template-columns:1fr 1fr;}}
"""

APP_JS = r"""
var WORKS = window.__WORKS__ || {};
var CRITERIA = window.__CRITERIA__ || [];
var BASELINE = window.__BASELINE__ || [];

function toast(msg){
  var t=document.getElementById('toast'); if(!t)return;
  t.textContent=msg; t.classList.add('show');
  clearTimeout(window.__toastT); window.__toastT=setTimeout(function(){t.classList.remove('show');},1600);
}

/* ---- theme ---- */
function toggleTheme(){
  var h=document.documentElement;
  var dark=h.getAttribute('data-theme')==='dark';
  h.setAttribute('data-theme', dark?'light':'dark');
  try{localStorage.setItem('ks-theme', dark?'light':'dark');}catch(e){}
  var b=document.getElementById('themeBtn'); if(b)b.textContent=dark?'🌙':'☀️';
}

/* ---- year tabs ---- */
function showYear(y){
  document.querySelectorAll('.year-panel').forEach(function(p){p.style.display=(p.dataset.year===y)?'block':'none';});
  document.querySelectorAll('.tab').forEach(function(t){t.classList.toggle('active', t.dataset.year===y);});
  try{localStorage.setItem('ks-year', y);}catch(e){}
  applyFilters();
  if(typeof renderDashboard==='function')renderDashboard();
}

/* ---- filter + sort + counter ---- */
function setSeg(group, val, el){
  document.querySelectorAll('.seg[data-group="'+group+'"] button').forEach(function(b){b.classList.toggle('on', b===el);});
  applyFilters();
}
function activePanel(){
  var y=null; document.querySelectorAll('.tab').forEach(function(t){if(t.classList.contains('active'))y=t.dataset.year;});
  return document.querySelector('.year-panel[data-year="'+y+'"]');
}
function segVal(group){
  var on=document.querySelector('.seg[data-group="'+group+'"] button.on');
  return on?on.dataset.val:'all';
}
function applyFilters(){
  var panel=activePanel(); if(!panel){if(typeof renderDashboard==='function')renderDashboard();return;}
  var q=(document.getElementById('q')||{}).value||''; q=q.trim().toLowerCase();
  var level=segVal('level'), risk=segVal('risk');
  var school=(document.getElementById('schoolSel')||{}).value||'all';
  var sortKey=(document.getElementById('sortSel')||{}).value||'maturity-desc';
  var grid=panel.querySelector('.grid'); if(!grid){if(typeof renderDashboard==='function')renderDashboard();return;}
  var cards=Array.prototype.slice.call(grid.querySelectorAll('.card'));
  var shown=0;
  cards.forEach(function(c){
    var ok=(!q||c.dataset.search.indexOf(q)>=0)
      && (level==='all'||c.dataset.level===level)
      && (risk==='all'||c.dataset.risk===risk)
      && (school==='all'||c.dataset.school===school);
    c.style.display=ok?'':'none'; if(ok)shown++;
  });
  // sort visible
  var vis=cards.filter(function(c){return c.style.display!=='none';});
  vis.sort(function(a,b){
    if(sortKey==='maturity-desc')return b.dataset.maturity-a.dataset.maturity;
    if(sortKey==='maturity-asc')return a.dataset.maturity-b.dataset.maturity;
    if(sortKey==='overlap-desc')return b.dataset.overlap-a.dataset.overlap;
    if(sortKey==='name')return a.dataset.name.localeCompare(b.dataset.name);
    return 0;
  });
  vis.forEach(function(c){grid.appendChild(c);});
  var cnt=panel.querySelector('.count'); if(cnt)cnt.innerHTML='显示 <b>'+shown+'</b> / 共 '+cards.length+' 个';
  if(typeof renderDashboard==='function')renderDashboard();
}

/* ---- report modal ---- */
function openReport(src,title){
  var m=document.getElementById('modal');
  document.getElementById('modal-title').textContent=title||'报告';
  var f=document.getElementById('modal-frame'); var sp=document.getElementById('modal-spin');
  if(sp)sp.style.display='flex';
  f.onload=function(){if(sp)sp.style.display='none';};
  f.src=src; m.dataset.src=src;
  m.classList.add('open');
}
function closeReport(){var m=document.getElementById('modal');m.classList.remove('open');document.getElementById('modal-frame').src='about:blank';m.querySelector('.panel').classList.remove('full');}
function modalNewTab(){var s=document.getElementById('modal').dataset.src;if(s)window.open(s,'_blank');}
function modalFull(){document.querySelector('#modal .panel').classList.toggle('full');}
function modalPrint(){try{document.getElementById('modal-frame').contentWindow.print();}catch(e){toast('打印失败，请在新标签打开后打印');}}

/* ---- copy ---- */
function copyText(text){
  if(navigator.clipboard&&navigator.clipboard.writeText){
    navigator.clipboard.writeText(text).then(function(){toast('已复制到剪贴板');},function(){fallbackCopy(text);});
  }else{fallbackCopy(text);}
}
function fallbackCopy(text){
  var ta=document.createElement('textarea');ta.value=text;document.body.appendChild(ta);ta.select();
  try{document.execCommand('copy');toast('已复制到剪贴板');}catch(e){toast('复制失败');}
  document.body.removeChild(ta);
}

/* ---- compare ---- */
var picked=[];
function togglePick(repo,el){
  var card=el.closest('.card');
  if(el.checked){
    if(picked.length>=3){el.checked=false;toast('最多对比 3 个作品');return;}
    picked.push(repo);card.classList.add('picked');
  }else{
    picked=picked.filter(function(r){return r!==repo;});card.classList.remove('picked');
  }
  var bar=document.getElementById('cmpbar');
  document.getElementById('cmpcount').textContent=picked.length;
  bar.classList.toggle('show', picked.length>=2);
}
function clearPicks(){
  picked=[];document.querySelectorAll('.card.picked').forEach(function(c){c.classList.remove('picked');});
  document.querySelectorAll('.pick input:checked').forEach(function(i){i.checked=false;});
  document.getElementById('cmpbar').classList.remove('show');
}
function openCompare(){
  if(picked.length<2)return;
  var rows=[['维度']];
  var works=picked.map(function(r){return WORKS[r];});
  var head='<tr><th class="rowhead">对比项</th>'+works.map(function(w){return '<th>'+esc(w.entry_no)+'<br><small>'+esc(w.name)+'</small></th>';}).join('')+'</tr>';
  function metricLabel(label,tip){return '<span class="metric-label">'+label+'<span class="info-tip" tabindex="0" data-tip="'+esc(tip)+'" aria-label="'+esc(tip)+'">!</span></span>';}
  function row(label, fn, cls){
    return '<tr><td class="rowhead">'+label+'</td>'+works.map(function(w){var v=fn(w);return '<td class="'+(cls?cls(w):'')+'">'+v+'</td>';}).join('')+'</tr>';
  }
  var body='';
  body+=row(metricLabel('成熟度','基于七类 OS 核心机制覆盖、源码证据可信度、工程质量、创新性和相似风险折算的参考分，不等同于赛题官方完成度。'), function(w){return w.maturity_score+'/100 ('+w.grade+'级)';});
  body+=row(metricLabel('最高重合度','表示当前作品与历史基线中最接近样本的功能、结构、语言和代码线索重合程度，只提示复核优先级，不直接判定抄袭。'), function(w){return w.top_overlap+' ('+riskLabel(w.risk_level)+')';});
  body+=row('代码行数', function(w){return (w.loc||0).toLocaleString();});
  body+=row('文件数', function(w){return w.file_count||0;});
  body+=row('学校', function(w){return esc(w.school||'-');});
  // dimensions
  var dims=works[0].dimensions||[];
  dims.forEach(function(d,idx){
    body+='<tr><td class="rowhead">'+esc(d.title)+'</td>'+works.map(function(w){
      var dd=(w.dimensions||[])[idx]; var ok=dd&&dd.status==='confirmed';
      return '<td class="'+(ok?'yes':'no')+'">'+(ok?('✓ '+(dd.confidence||'')):'—')+'</td>';
    }).join('')+'</tr>';
  });
  var htmlc='<table class="cmptable"><thead>'+head+'</thead><tbody>'+body+'</tbody></table>';
  document.getElementById('modal-title').textContent='作品并排对比';
  var m=document.getElementById('modal');
  document.getElementById('modal-frame').style.display='none';
  var bodyEl=document.getElementById('modal-body');
  var cont=document.getElementById('modal-cmp');
  if(!cont){cont=document.createElement('div');cont.id='modal-cmp';cont.style.cssText='position:absolute;inset:0;overflow:auto;padding:20px;';bodyEl.appendChild(cont);}
  cont.innerHTML=htmlc;cont.style.display='block';
  var sp=document.getElementById('modal-spin');if(sp)sp.style.display='none';
  m.dataset.src='';
  m.classList.add('open');
}
function riskLabel(r){return r==='high'?'高':r==='medium'?'中':r==='low'?'低':'无';}
function esc(s){var d=document.createElement('div');d.textContent=(s==null?'':s);return d.innerHTML;}

/* restore iframe view when reopening normal reports */
function openReport2(src,title){document.getElementById('modal-frame').style.display='';var c=document.getElementById('modal-cmp');if(c)c.style.display='none';var h=document.getElementById('modal-html');if(h)h.style.display='none';var sc=document.getElementById('modal-score');if(sc)sc.style.display='none';openReport(src,title);}

/* ---- scoring ---- */
function scoreKey(repo){return 'ks-score-'+repo;}
function loadScore(repo){try{return JSON.parse(localStorage.getItem(scoreKey(repo))||'null');}catch(e){return null;}}
function openScore(repo){
  var w=WORKS[repo]||{}; var saved=loadScore(repo)||{};
  var m=document.getElementById('modal');
  document.getElementById('modal-title').textContent='评委打分 · '+(w.entry_no||repo);
  document.getElementById('modal-frame').style.display='none';
  var c=document.getElementById('modal-cmp');if(c)c.style.display='none';
  var bodyEl=document.getElementById('modal-body');
  var box=document.getElementById('modal-score');
  if(!box){box=document.createElement('div');box.id='modal-score';box.style.cssText='position:absolute;inset:0;overflow:auto;padding:24px;';bodyEl.appendChild(box);}
  var html='<div class="scorebox"><p style="color:var(--muted);font-size:13px">参考系统成熟度 '+(w.maturity_score||0)+'/100、最高重合度 '+(w.top_overlap||0)+'。评分仅保存在本浏览器，可导出 CSV。</p>';
  CRITERIA.forEach(function(cr){
    var v=(saved.scores&&saved.scores[cr.key]!=null)?saved.scores[cr.key]:Math.round(cr.max*0.6);
    html+='<div class="crit"><div class="top"><span>'+esc(cr.label)+'</span><b><span id="sv-'+cr.key+'">'+v+'</span> / '+cr.max+'</b></div>'
      +'<div class="desc">'+esc(cr.desc)+'</div>'
      +'<input type="range" min="0" max="'+cr.max+'" value="'+v+'" data-key="'+cr.key+'" data-max="'+cr.max+'" oninput="onScoreInput(this)"></div>';
  });
  html+='<div class="total">总分：<span id="scoreTotal">0</span> / 100</div>';
  html+='<textarea id="scoreComment" placeholder="评语（可选）">'+esc(saved.comment||'')+'</textarea>';
  html+='<div class="acts"><button class="btn solid" onclick="saveScore(\''+repo+'\')">保存评分</button>'
    +'<button class="btn" onclick="clearScore(\''+repo+'\')">清除</button>'
    +'<button class="btn" onclick="closeReport()">关闭</button></div></div>';
  box.innerHTML=html;box.style.display='block';
  m.dataset.src='';m.classList.add('open');
  recalcTotal();
}
function onScoreInput(el){document.getElementById('sv-'+el.dataset.key).textContent=el.value;recalcTotal();}
function recalcTotal(){var t=0;document.querySelectorAll('#modal-score input[type=range]').forEach(function(i){t+=parseInt(i.value||0);});var el=document.getElementById('scoreTotal');if(el)el.textContent=t;}
function saveScore(repo){
  var scores={};document.querySelectorAll('#modal-score input[type=range]').forEach(function(i){scores[i.dataset.key]=parseInt(i.value||0);});
  var total=Object.keys(scores).reduce(function(a,k){return a+scores[k];},0);
  var data={repo:repo,entry_no:(WORKS[repo]||{}).entry_no,name:(WORKS[repo]||{}).name,scores:scores,total:total,comment:(document.getElementById('scoreComment')||{}).value||'',ts:new Date().toISOString()};
  try{localStorage.setItem(scoreKey(repo),JSON.stringify(data));}catch(e){}
  toast('已保存评分：'+total+'/100');markScored();closeReport();
}
function clearScore(repo){try{localStorage.removeItem(scoreKey(repo));}catch(e){}toast('已清除评分');markScored();closeReport();}
function markScored(){
  document.querySelectorAll('.card').forEach(function(c){
    var repo=c.dataset.repo;var s=loadScore(repo);var b=c.querySelector('.scored-badge');
    if(s){if(!b){b=document.createElement('span');b.className='scored-badge';var btn=c.querySelector('.btn.score');if(btn)btn.appendChild(b);}b.textContent='已评 '+s.total;}
    else if(b){b.remove();}
  });
}
function exportScores(){
  var rows=[['参赛编号','作品','总分'].concat(CRITERIA.map(function(c){return c.label;})).concat(['评语'])];
  Object.keys(WORKS).forEach(function(repo){
    var s=loadScore(repo);if(!s)return;
    rows.push([s.entry_no||repo, s.name||'', s.total].concat(CRITERIA.map(function(c){return (s.scores&&s.scores[c.key]!=null)?s.scores[c.key]:'';})).concat([(s.comment||'').replace(/\n/g,' ')]));
  });
  if(rows.length<2){toast('暂无已保存的评分');return;}
  var csv='﻿'+rows.map(function(r){return r.map(function(x){return '"'+String(x).replace(/"/g,'""')+'"';}).join(',');}).join('\n');
  var blob=new Blob([csv],{type:'text/csv;charset=utf-8'});
  var a=document.createElement('a');a.href=URL.createObjectURL(blob);a.download='kernelsage_scores.csv';a.click();
  toast('已导出 '+(rows.length-1)+' 条评分');
}


/* ---- overview dashboard + history tools ---- */
function activeWorks(){var p=activePanel();var a=[];if(p){p.querySelectorAll('.card').forEach(function(c){if(c.style.display!=='none'&&WORKS[c.dataset.repo])a.push(WORKS[c.dataset.repo]);});return a;}return Object.keys(WORKS).map(function(k){return WORKS[k];});}
function topLanguage(w){var l=w.languages||{},b='-',n=-1;Object.keys(l).forEach(function(k){if(l[k]>n){b=k;n=l[k];}});return b;}
function dimScore(ws,i){if(!ws.length)return 0;var ok=0;ws.forEach(function(w){var d=(w.dimensions||[])[i];if(d&&d.status==='confirmed')ok++;});return Math.round(ok*100/ws.length);}
function radarSvg(ws){var ds=(ws[0]&&ws[0].dimensions)||[];if(!ds.length)return '<div class="hint">当前筛选结果没有可绘制的能力维度。</div>';var cx=95,cy=95,r=72,pts=[],axis='';ds.forEach(function(d,i){var a=-Math.PI/2+i*2*Math.PI/ds.length,x=cx+Math.cos(a)*r,y=cy+Math.sin(a)*r,sc=dimScore(ws,i),rx=cx+Math.cos(a)*r*sc/100,ry=cy+Math.sin(a)*r*sc/100,label=String(d.title||d.key||'').slice(0,4);pts.push(rx+','+ry);axis+='<line x1="95" y1="95" x2="'+x.toFixed(1)+'" y2="'+y.toFixed(1)+'" stroke="var(--line)"/><text x="'+(cx+Math.cos(a)*(r+15)).toFixed(1)+'" y="'+(cy+Math.sin(a)*(r+15)).toFixed(1)+'" text-anchor="middle" dominant-baseline="middle" font-size="10" fill="var(--muted)">'+esc(label)+'</text>';});return '<svg viewBox="0 0 190 190" role="img" aria-label="本年度作品能力覆盖雷达图"><circle cx="95" cy="95" r="72" fill="none" stroke="var(--line)"/><circle cx="95" cy="95" r="48" fill="none" stroke="var(--line)"/>'+axis+'<polygon points="'+pts.join(' ')+'" fill="rgba(15,118,110,.22)" stroke="var(--brand)" stroke-width="2"/></svg>';}
function renderDashboard(){var ws=activeWorks(),loc=0,langs={},ok=0,total=0;ws.forEach(function(w){loc+=w.loc||0;Object.keys(w.languages||{}).forEach(function(k){langs[k]=(langs[k]||0)+(w.languages[k]||0);});(w.dimensions||[]).forEach(function(d){total++;if(d.status==='confirmed')ok++;});});var top='-',v=-1;Object.keys(langs).forEach(function(k){if(langs[k]>v){top=k;v=langs[k];}});function set(id,val){var e=document.getElementById(id);if(e)e.textContent=val;}set('ov-current',ws.length);set('ov-loc',loc.toLocaleString());set('ov-lang',top);set('ov-cover',total?Math.round(ok*100/total)+'%':'-');var r=document.getElementById('abilityRadar');if(r)r.innerHTML=radarSvg(ws);var l=document.getElementById('abilityLegend'),ds=(ws[0]&&ws[0].dimensions)||[];if(l)l.innerHTML=ds.map(function(d,i){return '<div><b>'+esc(d.title||d.key)+'</b>：'+dimScore(ws,i)+'% 作品有可追溯实现证据</div>';}).join('')||'<div>暂无维度数据</div>';applyHistoryFilters();}
function baselineScore(w,tr){if(!w)return 0;var sc=0;if((tr.dataset.lang||'')&&topLanguage(w)===tr.dataset.lang)sc+=38;var loc=parseInt(tr.dataset.loc||'0'),wl=w.loc||0;if(loc>0&&wl>0)sc+=Math.max(0,32-Math.abs(Math.log((wl+1)/(loc+1)))*18);if((tr.dataset.tier||'').indexOf('获奖')>=0)sc+=12;if((tr.dataset.text||'').indexOf((w.arch||[])[0]||'')>=0)sc+=10;return Math.max(0,Math.min(100,Math.round(sc)));}
function applyHistoryFilters(){var rows=document.querySelectorAll('#historyRows tr');if(!rows.length)return;var q=((document.getElementById('histQ')||{}).value||'').trim().toLowerCase(),year=(document.getElementById('histYear')||{}).value||'all',award=(document.getElementById('histAward')||{}).value||'all',lang=(document.getElementById('histLang')||{}).value||'all',dim=(document.getElementById('histDim')||{}).value||'all',sim=(document.getElementById('histSim')||{}).value||'all',w=activeWorks()[0]||WORKS[Object.keys(WORKS)[0]],shown=0;rows.forEach(function(tr){var score=baselineScore(w,tr),se=tr.querySelector('.simscore');if(se)se.textContent=score;var ok=(!q||(tr.dataset.text||'').indexOf(q)>=0)&&(year==='all'||tr.dataset.year===year)&&(award==='all'||(tr.dataset.award||'').indexOf(award)>=0)&&(lang==='all'||tr.dataset.lang===lang)&&(dim==='all'||(tr.dataset.dims||'').indexOf(dim)>=0)&&(sim==='all'||(sim==='high'&&score>=70)||(sim==='medium'&&score>=40&&score<70)||(sim==='low'&&score<40));tr.style.display=ok?'':'none';if(ok)shown++;});var c=document.getElementById('histCount');if(c)c.textContent='显示 '+shown+' / 共 '+rows.length+' 个历史样本';}
function openHistoryCompare(repo,idx){var w=WORKS[repo]||{},cmp=(w.compares||[]).filter(function(c){return String(c.index)===String(idx);})[0]||{},target=cmp.target_name||'历史样本',b=BASELINE.filter(function(x){return x.repo_id===cmp.target_repo_id;})[0]||{},dims=(w.dimensions||[]).map(function(d){return '<span class="dim '+(d.status==='confirmed'?'ok':'no')+'">'+esc(d.title||d.key)+'</span>';}).join('');var html='<div class="split-compare"><div class="side"><h3>当前作品</h3>'+workSummary(w,1,cmp)+'<div class="dims" style="padding:8px 0 0">'+dims+'</div></div><div class="side"><h3>历史作品</h3>'+workSummary(b,0,cmp)+'<div class="hint">重合维度 '+(cmp.overlap_dimensions||0)+' / 7，代码级线索 '+(cmp.code_similarity_count||0)+' 条。完整源码路径、行号与片段请点击比较报告核验。</div><button class="btn solid" onclick="openReport2(&quot;reports/'+esc(repo)+'.compare'+esc(idx)+'.html&quot;,&quot;'+esc(w.name||repo)+' vs '+esc(target)+'&quot;)">查看完整证据报告</button></div></div>';showHtmlModal('当前作品 vs 历史作品',html);}
function workSummary(w,cur,cmp){if(cur)return '<dl><dt>名称</dt><dd>'+esc(w.name||'-')+'</dd><dt>编号</dt><dd>'+esc(w.entry_no||'-')+'</dd><dt>学校</dt><dd>'+esc(w.school||'-')+'</dd><dt>主语言</dt><dd>'+esc(topLanguage(w))+'</dd><dt>代码规模</dt><dd>'+((w.loc||0).toLocaleString())+' LOC</dd><dt>成熟度</dt><dd>'+esc(w.maturity_score||0)+'/100</dd><dt>重合风险</dt><dd>'+riskLabel(w.risk_level)+'</dd></dl>';return '<dl><dt>名称</dt><dd>'+esc((cmp&&cmp.target_name)||w.name||'-')+'</dd><dt>来源</dt><dd>'+esc((cmp&&cmp.target_tier_label)||w.source_tier_label||'-')+'</dd><dt>年份</dt><dd>'+esc(w.year||'-')+'</dd><dt>学校</dt><dd>'+esc(w.school||'-')+'</dd><dt>主语言</dt><dd>'+esc(w.language_primary||'-')+'</dd><dt>代码规模</dt><dd>'+esc(w.loc||'-')+'</dd><dt>仓库 ID</dt><dd>'+esc(w.repo_id||'-')+'</dd></dl>';}
function showHtmlModal(title,htmlc){var m=document.getElementById('modal');document.getElementById('modal-title').textContent=title||'详情';document.getElementById('modal-frame').style.display='none';var c=document.getElementById('modal-cmp');if(c)c.style.display='none';var sc=document.getElementById('modal-score');if(sc)sc.style.display='none';var body=document.getElementById('modal-body'),box=document.getElementById('modal-html');if(!box){box=document.createElement('div');box.id='modal-html';box.style.cssText='position:absolute;inset:0;overflow:auto;';body.appendChild(box);}box.innerHTML=htmlc;box.style.display='block';var sp=document.getElementById('modal-spin');if(sp)sp.style.display='none';m.dataset.src='';m.classList.add('open');}
function saveBlob(name,content,type){var blob=new Blob([content],{type:type||'text/plain;charset=utf-8'}),a=document.createElement('a');a.href=URL.createObjectURL(blob);a.download=name;a.click();setTimeout(function(){URL.revokeObjectURL(a.href);},500);}
function downloadReport(repo,kind,idx){var w=WORKS[repo]||{};saveBlob((repo||'work')+'-'+kind+'.json',JSON.stringify({work:w,kind:kind,compare_index:idx||null},null,2),'application/json;charset=utf-8');}

/* ---- baseline search ---- */
function filterBaseline(q){
  q=(q||'').trim().toLowerCase();var shown=0,total=0;
  document.querySelectorAll('.doc table tbody tr').forEach(function(tr){
    total++;var ok=!q||tr.textContent.toLowerCase().indexOf(q)>=0;tr.style.display=ok?'':'none';if(ok)shown++;
  });
  var c=document.getElementById('bcount');if(c)c.textContent='显示 '+shown+' / 共 '+total+' 个';
}

document.addEventListener('keydown',function(e){if(e.key==='Escape')closeReport();});
window.addEventListener('scroll',function(){var b=document.getElementById('toTop');if(b)b.classList.toggle('show',window.scrollY>400);});
function toTop(){window.scrollTo({top:0,behavior:'smooth'});}

document.addEventListener('DOMContentLoaded',function(){
  // theme
  var t=null;try{t=localStorage.getItem('ks-theme');}catch(e){}
  if(t){document.documentElement.setAttribute('data-theme',t);var b=document.getElementById('themeBtn');if(b)b.textContent=t==='dark'?'☀️':'🌙';}
  // year
  var tabs=document.querySelectorAll('.tab');
  var saved=null;try{saved=localStorage.getItem('ks-year');}catch(e){}
  var first=(saved&&document.querySelector('.tab[data-year="'+saved+'"]'))?saved:(tabs[0]?tabs[0].dataset.year:null);
  if(first)showYear(first);
  var m=document.getElementById('modal');if(m)m.addEventListener('click',function(e){if(e.target===m)closeReport();});
  markScored();
  renderDashboard();
  applyHistoryFilters();
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

        for year in site_data.get("years", []):
            for project in year.get("projects", []):
                self._write_reports(out_dir, project)

        (out_dir / "index.html").write_text(self._index_page(site_data), encoding="utf-8")
        (out_dir / "baseline.html").write_text(self._baseline_page(site_data), encoding="utf-8")
        (out_dir / "insights.html").write_text(self._insights_page(site_data), encoding="utf-8")

    # ---- report files -----------------------------------------------------
    def _write_reports(self, out_dir: Path, project: dict[str, Any]) -> None:
        rid = project["repo_id"]
        reports = project["reports"]
        rdir = out_dir / "reports"
        rdir.joinpath(f"{rid}.describe.html").write_text(
            self._doc_page(f"{project['name']} 描述报告", markdown_to_html(reports["describe_md"])), encoding="utf-8")
        rdir.joinpath(f"{rid}.describe.md").write_text(reports["describe_md"], encoding="utf-8")
        rdir.joinpath(f"{rid}.devhistory.html").write_text(
            self._doc_page(f"{project['name']} 开发历史报告", markdown_to_html(reports["dev_history_md"])), encoding="utf-8")
        rdir.joinpath(f"{rid}.devhistory.md").write_text(reports["dev_history_md"], encoding="utf-8")
        rdir.joinpath(f"{rid}.json").write_text(json.dumps(project, ensure_ascii=False, indent=2), encoding="utf-8")
        for cmp in reports["compares"]:
            rdir.joinpath(f"{rid}.compare{cmp['index']}.html").write_text(
                self._doc_page(f"{project['name']} vs {cmp['target_name']} 比较报告", markdown_to_html(cmp["report_md"])),
                encoding="utf-8")
            rdir.joinpath(f"{rid}.compare{cmp['index']}.md").write_text(cmp["report_md"], encoding="utf-8")

    # ---- index ------------------------------------------------------------
    def _index_page(self, site_data: dict[str, Any]) -> str:
        years = site_data.get("years", [])
        tabs = "".join(
            f'<button class="tab" data-year="{_esc(y["year"])}" onclick="showYear(\'{_esc(y["year"])}\')">'
            f'{_esc(y["year"])} <span class="n">{y["count"]} 个作品</span></button>'
            for y in years
        )
        panels = "".join(self._year_panel(y) for y in years)
        works = self._works_json(years)
        criteria = site_data.get("criteria") or self._default_criteria()
        baseline = site_data.get("baseline", {}).get("repos", [])
        data_script = (
            "<script>window.__WORKS__=" + json.dumps(works, ensure_ascii=False)
            + ";window.__CRITERIA__=" + json.dumps(criteria, ensure_ascii=False)
            + ";window.__BASELINE__=" + json.dumps(baseline, ensure_ascii=False) + ";</script>"
        )
        body = f"""
{data_script}
<main>
{self._overview_panel(site_data, years)}
  <div class="tabs">{tabs}</div>
  <div class="toolbar">
    <input type="text" id="q" placeholder="🔍 搜索 编号 / 学校 / 队伍 / 作品…" oninput="applyFilters()">
    <span class="lbl">排序</span>
    <select id="sortSel" onchange="applyFilters()">
      <option value="maturity-desc">成熟度 高→低</option>
      <option value="maturity-asc">成熟度 低→高</option>
      <option value="overlap-desc">重合度 高→低</option>
      <option value="name">名称</option>
    </select>
    <span class="lbl">等级</span>
    <div class="seg" data-group="level">
      <button class="on" data-val="all" onclick="setSeg('level','all',this)">全部</button>
      <button data-val="A" onclick="setSeg('level','A',this)">A</button>
      <button data-val="B" onclick="setSeg('level','B',this)">B</button>
      <button data-val="C" onclick="setSeg('level','C',this)">C</button>
      <button data-val="D" onclick="setSeg('level','D',this)">D</button>
    </div>
    <span class="lbl">重合风险</span>
    <div class="seg" data-group="risk">
      <button class="on" data-val="all" onclick="setSeg('risk','all',this)">全部</button>
      <button data-val="high" onclick="setSeg('risk','high',this)">高</button>
      <button data-val="medium" onclick="setSeg('risk','medium',this)">中</button>
      <button data-val="low" onclick="setSeg('risk','low',this)">低</button>
    </div>
    <span class="lbl">学校</span>
    <select id="schoolSel" onchange="applyFilters()">{self._school_options(years)}</select>
    <button class="btn-mini exp" onclick="exportScores()">⬇ 导出评分CSV</button>
    <span class="count"></span>
  </div>
{self._history_filter_panel(site_data, years)}
{panels}
</main>
{self._modal()}
{self._compare_bar()}
<button id="toTop" onclick="toTop()" title="返回顶部">↑</button>
<div id="toast"></div>
"""
        return self._shell(site_data, body, active="works")


    def _overview_panel(self, site_data: dict[str, Any], years: list[dict[str, Any]]) -> str:
        projects = [p for y in years for p in y.get("projects", [])]
        baseline = site_data.get("baseline", {})
        repos = baseline.get("repos", [])
        covered_years = sorted({str(y.get("year")) for y in years if y.get("year")} | {str(r.get("year")) for r in repos if r.get("year")})
        verified_awards = sum(1 for r in repos if "获奖" in str(r.get("source_tier_label", "")) or r.get("award_level"))
        loc = sum(int(p.get("loc") or 0) for p in projects)
        langs: dict[str, int] = {}
        for p in projects:
            for k, v in (p.get("languages") or {}).items():
                langs[k] = langs.get(k, 0) + int(v or 0)
        top_lang = max(langs.items(), key=lambda kv: kv[1])[0] if langs else "-"
        total_dims = sum(len(p.get("dimensions", [])) for p in projects)
        ok_dims = sum(1 for p in projects for d in p.get("dimensions", []) if d.get("status") == "confirmed")
        cover = f"{round(ok_dims * 100 / total_dims)}%" if total_dims else "-"
        cards = [("历史样本", baseline.get("count", len(repos)), "用于相似性与获奖样本参考"),("覆盖年份", len(covered_years), " / ".join(covered_years[:6]) + (" ..." if len(covered_years) > 6 else "")),("已核验获奖作品", verified_awards, "只按带来源的获奖样本统计"),("本年度作品数", f'<span id="ov-current">{len(projects)}</span>', "当前年份/筛选下的作品总数"),("本年度代码总规模", f'<span id="ov-loc">{loc:,}</span>', "全部作品 LOC 之和"),("主要语言", f'<span id="ov-lang">{_esc(top_lang)}</span>', "按当前筛选作品聚合"),("核心 OS 覆盖", f'<span id="ov-cover">{cover}</span>', "全部作品×七维已确认占比")]
        grid = "".join(f'<div class="overview-item"><div class="k">{k}</div><div class="v">{v}</div><div class="s">{_esc(s)}</div></div>' for k, v, s in cards)
        links = [("README", "https://github.com/chanehwibo/proj18-CSCC/blob/main/README.md"),("设计技术文档", "https://github.com/chanehwibo/proj18-CSCC/blob/main/docs/DESIGN_TECHNICAL_DOCUMENT.md"),("操作手册", "https://github.com/chanehwibo/proj18-CSCC/blob/main/BEGINNER_OPERATION_MANUAL1.md"),("答辩 PPT", "https://github.com/chanehwibo/proj18-CSCC/blob/main/KernelSage_%E7%AD%94%E8%BE%A9%E6%BC%94%E7%A4%BAPPT.pptx"),("演示视频", "https://github.com/chanehwibo/proj18-CSCC/blob/main/%E4%B8%80%E5%AE%9A%E8%A6%81%E4%BB%A5%E4%BA%BA%E7%B1%BB%E7%9A%84%E8%BA%AB%E4%BB%BD%E8%B5%A2%E5%95%8A_%E6%BC%94%E7%A4%BA%E8%A7%86%E9%A2%91.mp4"),("历史基线库", "baseline.html")]
        quick = "".join(f'<a href="{href}" target="_blank" rel="noopener">{_esc(label)}</a>' for label, href in links)
        return f'''\n  <section class="overview" aria-label="作品总览仪表盘">\n    <div class="panel"><h2>作品总览仪表盘</h2><div class="overview-grid">{grid}</div><div class="quick-links">{quick}</div></div>\n    <div class="panel"><h2>本年度作品能力覆盖雷达图</h2><div class="radar-wrap"><div id="abilityRadar"></div><div class="radar-legend" id="abilityLegend"></div></div></div>\n  </section>'''

    def _history_filter_panel(self, site_data: dict[str, Any], years: list[dict[str, Any]]) -> str:
        repos = site_data.get("baseline", {}).get("repos", [])
        year_opts = '<option value="all">全部年份</option>' + "".join(f'<option value="{_esc(y)}">{_esc(y)}</option>' for y in sorted({str(r.get("year")) for r in repos if r.get("year")}))
        awards = sorted({str(r.get("award_level") or r.get("source_tier_label") or "未标注") for r in repos})
        award_opts = '<option value="all">全部奖项/来源</option>' + "".join(f'<option value="{_esc(a)}">{_esc(a)}</option>' for a in awards)
        langs = sorted({str(r.get("language_primary")) for r in repos if r.get("language_primary")})
        lang_opts = '<option value="all">全部语言</option>' + "".join(f'<option value="{_esc(a)}">{_esc(a)}</option>' for a in langs)
        dims = sorted({d.get("title", d.get("key", "")) for y in years for p in y.get("projects", []) for d in p.get("dimensions", []) if d.get("title") or d.get("key")})
        dim_opts = '<option value="all">全部功能维度</option>' + "".join(f'<option value="{_esc(d)}">{_esc(d)}</option>' for d in dims)
        rows = []
        for r in repos:
            text = " ".join(str(r.get(k) or "") for k in ["repo_id", "name", "source_tier_label", "language_primary", "school", "award_level", "note"]).lower()
            award = str(r.get("award_level") or r.get("source_tier_label") or "未标注")
            rows.append(f'<tr data-text="{_esc(text)}" data-dims="{_esc(text)}" data-year="{_esc(r.get("year") or "")}" data-award="{_esc(award)}" data-lang="{_esc(r.get("language_primary") or "")}" data-loc="{_esc(r.get("loc") or 0)}" data-tier="{_esc(r.get("source_tier_label") or "")}"><td><code>{_esc(r.get("repo_id") or "-")}</code><br><small>{_esc(r.get("source_tier_label") or "-")}</small></td><td>{_esc(r.get("name") or "-")}<br><small>{_esc(r.get("school") or "-")}</small></td><td>{_esc(r.get("year") or "-")}</td><td>{_esc(award)}</td><td>{_esc(r.get("language_primary") or "-")}</td><td>{_esc(r.get("loc") if r.get("loc") is not None else "-")}</td><td><b class="simscore">-</b></td></tr>')
        return f'''\n  <section class="history-filter"><h2>历史作品对比筛选器</h2>\n    <div class="history-controls"><input id="histQ" type="text" placeholder="搜索历史项目 / 学校 / 来源 / 语言..." oninput="applyHistoryFilters()"><select id="histYear" onchange="applyHistoryFilters()">{year_opts}</select><select id="histAward" onchange="applyHistoryFilters()">{award_opts}</select><select id="histLang" onchange="applyHistoryFilters()">{lang_opts}</select><select id="histDim" onchange="applyHistoryFilters()">{dim_opts}</select><select id="histSim" onchange="applyHistoryFilters()"><option value="all">全部相似度</option><option value="high">高相似</option><option value="medium">中相似</option><option value="low">低相似</option></select><span class="count" id="histCount"></span></div>\n    <div class="history-table-wrap"><table class="history-table"><thead><tr><th>仓库</th><th>名称</th><th>年份</th><th>奖项/来源</th><th>主语言</th><th>LOC</th><th>相似参考</th></tr></thead><tbody id="historyRows">{"".join(rows)}</tbody></table></div><div class="hint">相似参考分根据当前筛选作品与历史样本的语言、代码规模、架构和来源信息估算，用于快速定位复核对象。</div>\n  </section>'''

    def _dimension_tags(self, p: dict[str, Any]) -> str:
        tags = [f'<span class="dim {"ok" if d.get("status") == "confirmed" else "no"}">{_esc(d.get("title") or d.get("key") or "-")}</span>' for d in p.get("dimensions", [])]
        return '<div class="dims">' + "".join(tags) + '</div>' if tags else ""

    def _evidence_lines(self, report_md: str, limit: int = 4) -> list[str]:
        out: list[str] = []
        for line in report_md.splitlines():
            s = line.strip()
            if s.startswith("- `") and (":L" in s or "代码片段" in s):
                out.append(s)
            if len(out) >= limit:
                break
        return out


    def _explain_panel(self, p: dict[str, Any]) -> str:
        items = []
        for c in p.get("reports", {}).get("compares", [])[:3]:
            reasons = ["语言构成", "目录/结构", "功能维度"]
            if int(c.get("code_similarity_count") or 0) > 0:
                reasons.extend(["符号/路径", "证据片段"])
            why = "".join(f"<span>{_esc(r)}</span>" for r in reasons)
            ev = self._evidence_lines(c.get("report_md", ""))
            ev_html = "".join(f"<li>{_inline(e)}</li>" for e in ev) or "<li>完整源码路径、行号和代码片段见比较报告。</li>"
            idx = int(c.get("index") or 0)
            items.append(f'''<div class="explain-item"><div class="top"><span>{_esc(c.get("target_name") or "历史样本")}</span><span>{_esc(c.get("overlap_score") or 0)}</span></div><div class="meta">来源：{_esc(c.get("target_tier_label") or "-")}；重合维度 {int(c.get("overlap_dimensions") or 0)} / 7；代码级线索 {int(c.get("code_similarity_count") or 0)} 条</div><div class="why">{why}</div><details class="evidence-mini"><summary>查看证据摘要</summary><ul>{ev_html}</ul></details><div class="acts"><button class="btn" onclick="openReport2('reports/{_esc(p["repo_id"])}.compare{idx}.html','{_esc(p["name"])} vs {_esc(c.get("target_name") or "历史样本")}')">完整证据报告</button><button class="btn" onclick="openHistoryCompare('{_esc(p["repo_id"])}','{idx}')">双栏对比</button></div></div>''')
        return f'<details class="explain"><summary>相似度解释面板</summary><div class="explain-list">{"".join(items)}</div></details>' if items else ""


    def _downloads(self, p: dict[str, Any]) -> str:
        rid = _esc(p["repo_id"])
        comps = p.get("reports", {}).get("compares", [])
        cmp_links = ""
        if comps:
            idx = int(comps[0].get("index") or 0)
            cmp_links = f'<a class="btn" href="reports/{rid}.compare{idx}.html" download>HTML 对比</a><a class="btn" href="reports/{rid}.compare{idx}.md" download>Markdown 对比</a>'
        return f'<div class="download-row"><a class="btn" href="reports/{rid}.describe.md" download>Markdown 描述</a><a class="btn" href="reports/{rid}.describe.html" download>HTML 描述</a>{cmp_links}<a class="btn" href="reports/{rid}.json" download>JSON 数据</a></div>'

    def _year_panel(self, year: dict[str, Any]) -> str:
        projects = year["projects"]
        if not projects:
            inner = '<div class="empty">本年度暂无输入作品。<br>将今年的参赛仓库放入输入目录并重新生成站点即可在此显示。</div>'
            return f'<section class="year-panel" data-year="{_esc(year["year"])}" style="display:none">{inner}</section>'
        kpi = self._kpi_panel(projects)
        cards = '<div class="grid">' + "".join(self._card(p) for p in projects) + "</div>"
        return f'<section class="year-panel" data-year="{_esc(year["year"])}" style="display:none">{kpi}{cards}</section>'

    def _kpi_panel(self, projects: list[dict[str, Any]]) -> str:
        n = len(projects)
        avg = round(sum(p["maturity"]["score"] for p in projects) / n, 1) if n else 0
        high = sum(1 for p in projects if p.get("risk_level") == "high")
        schools = len({p["school"] for p in projects if p["school"] and p["school"] != "未提供"})
        items = [
            ("📦 本年作品", f'{n}<small>个</small>'),
            ("⭐ 平均成熟度", f'{avg}<small>/100</small>'),
            ("⚠️ 高重合风险", f'{high}<small>个</small>'),
            ("🏫 覆盖学校", f'{schools}<small>所</small>'),
        ]
        cards = "".join(f'<div class="kpi"><div class="k">{k}</div><div class="v">{v}</div></div>' for k, v in items)
        return f'<div class="kpis">{cards}</div>'

    def _card(self, p: dict[str, Any]) -> str:
        search = " ".join(str(x).lower() for x in [p["entry_no"], p["name"], p["school"], p["team_name"], p["year"]])
        score = p["maturity"]["score"]
        grade = _grade(score)
        risk = p.get("risk_level", "none")
        overlap = p.get("top_overlap", 0)
        risk_chip = {
            "high": '<span class="chip bad">最高重合度 高</span>',
            "medium": '<span class="chip warn">最高重合度 中</span>',
            "low": '<span class="chip ok">最高重合度 低</span>',
        }.get(risk, "")
        repo_url = p["repo_url"]
        repo_html = f'<a href="{_esc(repo_url)}" target="_blank" rel="noopener">{_esc(repo_url)}</a>' if str(repo_url).startswith("http") else _esc(repo_url)
        compares = p["reports"]["compares"]
        cmp_btns = "".join(
            f'<button class="btn" onclick="openReport2(\'reports/{_esc(p["repo_id"])}.compare{c["index"]}.html\','
            f"'{_esc(p['name'])} vs {_esc(c['target_name'])}')\">"
            f'{_esc(c["label"])}<small>vs {_esc(c["target_name"])}</small></button>'
            for c in compares
        ) or '<span class="chip">暂无可比较的历史仓库</span>'
        clone = _esc(p["clone_cmd"])
        risk_pct = min(100, overlap)
        return f"""
<article class="card" data-search="{_esc(search)}" data-repo="{_esc(p["repo_id"])}" data-level="{grade}"
  data-risk="{risk}" data-maturity="{score}" data-overlap="{overlap}" data-school="{_esc(p["school"])}" data-name="{_esc(p["name"])}">
  <label class="pick"><input type="checkbox" onchange="togglePick('{_esc(p["repo_id"])}',this)">对比</label>
  <div class="hd">
    <div class="entry">{_esc(p["entry_no"])}</div>
    <div class="chips">
      <span class="chip tier">{_esc(p["source_tier_label"])}</span>
      <span class="chip">{grade} 级</span>
      {risk_chip}
    </div>
    <div class="meters">
      <div class="meter"><span class="metric-label">成熟度<span class="info-tip" tabindex="0" data-tip="基于七类 OS 核心机制覆盖、源码证据可信度、工程质量、创新性和相似风险折算的参考分，不等同于赛题官方完成度。" aria-label="成熟度说明">!</span></span><div class="bar mat"><span style="width:{score}%"></span></div><span class="val">{score}</span></div>
      <div class="meter"><span class="metric-label">重合度<span class="info-tip" tabindex="0" data-tip="表示当前作品与历史基线中最接近样本的功能、结构、语言和代码线索重合程度，只提示复核优先级，不直接判定抄袭。" aria-label="重合度说明">!</span></span><div class="bar risk"><span style="width:{risk_pct}%"></span></div><span class="val">{overlap}</span></div>
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
      <dt>镜像克隆</dt><dd class="clone"><code>{clone}</code><button class="copybtn" onclick="copyText('{clone}')">复制</button></dd>
    </dl>
  </div>
  {self._dimension_tags(p)}
  {self._explain_panel(p)}
  <div class="reports">
    <div class="grp">
      <div class="gt">作品描述报告</div>
      <button class="btn solid" onclick="openReport2('reports/{_esc(p["repo_id"])}.describe.html','{_esc(p["name"])} 描述报告')">查看描述报告</button>
    </div>
    <div class="grp">
      <div class="gt">开发历史报告</div>
      <button class="btn" onclick="openReport2('reports/{_esc(p["repo_id"])}.devhistory.html','{_esc(p["name"])} 开发历史')">查看开发历史</button>
    </div>
    <div class="grp">
      <div class="gt">比较报告（与重合/重复率最高的仓库）</div>
      {cmp_btns}
    </div>
    <div class="grp">
      <div class="gt">一键下载报告</div>
      {self._downloads(p)}
    </div>
    <div class="grp">
      <div class="gt">评审打分</div>
      <button class="btn score" onclick="openScore('{_esc(p["repo_id"])}')">评委打分</button>
    </div>
  </div>
</article>
"""

    def _modal(self) -> str:
        return """
<div class="modal" id="modal">
  <div class="panel">
    <div class="mhd">
      <span class="t" id="modal-title">报告</span>
      <button onclick="modalNewTab()" title="在新标签打开">↗ 新标签</button>
      <button onclick="modalFull()" title="全屏">⛶ 全屏</button>
      <button onclick="modalPrint()" title="打印/导出PDF">🖨 打印</button>
      <button onclick="closeReport()">关闭 ✕</button>
    </div>
    <div class="body" id="modal-body">
      <div class="spin" id="modal-spin" style="display:none"><div class="spinner"></div></div>
      <iframe id="modal-frame" src="about:blank"></iframe>
    </div>
  </div>
</div>
"""

    def _compare_bar(self) -> str:
        return """
<div class="cmpbar" id="cmpbar">
  <span>已选 <b id="cmpcount">0</b> 个作品</span>
  <button onclick="openCompare()">并排对比</button>
  <button class="clear" onclick="clearPicks()">清除</button>
</div>
"""

    def _works_json(self, years: list[dict[str, Any]]) -> dict[str, Any]:
        out: dict[str, Any] = {}
        for y in years:
            for p in y["projects"]:
                out[p["repo_id"]] = {
                    "entry_no": p["entry_no"],
                    "name": p["name"],
                    "school": p["school"],
                    "maturity_score": p["maturity"]["score"],
                    "grade": _grade(p["maturity"]["score"]),
                    "top_overlap": p.get("top_overlap", 0),
                    "risk_level": p.get("risk_level", "none"),
                    "loc": p.get("loc", 0),
                    "file_count": p.get("file_count", 0),
                    "symbol_count": p.get("symbol_count", 0),
                    "arch": p.get("arch", []),
                    "languages": p.get("languages", {}),
                    "source_tier_label": p.get("source_tier_label", ""),
                    "selfcheck": p.get("selfcheck", {}),
                    "dimensions": p.get("dimensions", []),
                    "compares": [
                        {
                            "index": c.get("index"),
                            "label": c.get("label"),
                            "target_repo_id": c.get("target_repo_id"),
                            "target_name": c.get("target_name"),
                            "target_tier_label": c.get("target_tier_label"),
                            "overlap_dimensions": c.get("overlap_dimensions"),
                            "code_similarity_count": c.get("code_similarity_count"),
                            "overlap_score": c.get("overlap_score"),
                        }
                        for c in p.get("reports", {}).get("compares", [])
                    ],
                }
        return out

    def _school_options(self, years: list[dict[str, Any]]) -> str:
        schools = sorted({p["school"] for y in years for p in y["projects"] if p["school"] and p["school"] != "未提供"})
        opts = '<option value="all">全部</option>'
        opts += "".join(f'<option value="{_esc(s)}">{_esc(s)}</option>' for s in schools)
        return opts

    def _default_criteria(self) -> list[dict[str, Any]]:
        return [
            {"key": "mechanism", "label": "机制完整性", "max": 30, "desc": "七维 OS 机制的覆盖与实现深度"},
            {"key": "evidence", "label": "证据可信度", "max": 20, "desc": "关键结论是否落到源码路径、行号与片段"},
            {"key": "engineering", "label": "工程质量", "max": 20, "desc": "构建系统、目录组织、代码规模与模块化"},
            {"key": "innovation", "label": "创新性", "max": 20, "desc": "相对历史基线是否有独特设计（保守评估）"},
            {"key": "originality", "label": "原创性/相似风险", "max": 10, "desc": "与历史基线的重合越高得分越低"},
        ]

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
  <div class="bsearch">
    <input type="text" placeholder="🔍 搜索仓库 ID / 名称 / 学校 / 架构 / 语言…" oninput="filterBaseline(this.value)">
    <span class="count" id="bcount"></span>
  </div>
  {"".join(sections)}
</div></main>
<button id="toTop" onclick="toTop()" title="返回顶部">↑</button>
<div id="toast"></div>
"""
        return self._shell(site_data, body, active="baseline")

    # ---- shared shell / report doc ---------------------------------------
    def _insights_page(self, site_data: dict[str, Any]) -> str:
        import math
        ins = site_data.get("insights", {})
        matrix = ins.get("matrix", {"labels": [], "rows": [], "links": []})
        labels = matrix.get("labels", [])
        rows = matrix.get("rows", [])
        evolution = ins.get("year_evolution", [])
        schools = ins.get("schools", [])

        # works summary for the JS (人机评分对照 / 汇总导出)
        works = []
        for y in site_data.get("years", []):
            for p in y["projects"]:
                works.append({
                    "repo_id": p["repo_id"], "entry_no": p["entry_no"], "name": p["name"],
                    "year": p["year"], "school": p.get("school", ""),
                    "maturity": p["maturity"]["score"], "grade": _grade(p["maturity"]["score"]),
                    "risk": p.get("risk_level", "none"), "overlap": p.get("top_overlap", 0),
                })

        # ---- 1) 重复检测热力矩阵 ----
        def cell_color(v: float) -> str:
            a = max(0.0, min(1.0, v / 100.0))
            return f"background:rgba(220,38,38,{a*0.82:.2f});" + ("color:#fff;" if a > 0.55 else "")
        if labels:
            head = "<th class=\"corner\">作品</th>" + "".join(
                f'<th class="vh"><span>{_esc(l["entry_no"])}</span></th>' for l in labels)
            body_rows = []
            for i, l in enumerate(labels):
                tds = "".join(
                    f'<td style="{cell_color(rows[i][j]) if i!=j else "background:var(--panel);color:var(--muted);"}">{("—" if i==j else rows[i][j])}</td>'
                    for j in range(len(labels)))
                body_rows.append(f'<tr><th class="rh">{_esc(l["entry_no"])}<small>{_esc(l["name"])}</small></th>{tds}</tr>')
            matrix_html = f'<table class="heat"><thead><tr>{head}</tr></thead><tbody>{"".join(body_rows)}</tbody></table>'
        else:
            matrix_html = '<p class="muted">本批作品不足，无法生成两两重合度矩阵。</p>'

        # ---- 2) 相似度关系图 (circular layout SVG) ----
        n = len(labels)
        graph_svg = ""
        if n >= 2:
            cx, cy, r = 430, 300, 215
            pos = []
            for i in range(n):
                ang = -math.pi / 2 + 2 * math.pi * i / n
                pos.append((cx + r * math.cos(ang), cy + r * math.sin(ang)))
            link_svg = ""
            for lk in matrix.get("links", []):
                s, t, sc = lk["source"], lk["target"], lk["score"]
                x1, y1 = pos[s]; x2, y2 = pos[t]
                op = min(0.9, sc / 100 + 0.15); w = 1 + sc / 22
                col = "#dc2626" if sc >= 60 else ("#d97706" if sc >= 45 else "#94a3b8")
                link_svg += f'<line x1="{x1:.0f}" y1="{y1:.0f}" x2="{x2:.0f}" y2="{y2:.0f}" stroke="{col}" stroke-width="{w:.1f}" stroke-opacity="{op:.2f}"/>'
            node_svg = ""
            ycolors = {"2021": "#0ea5e9", "2022": "#10b981", "2023": "#f59e0b", "2024": "#8b5cf6", "2025": "#ec4899", "2026": "#ef4444"}
            for i, l in enumerate(labels):
                x, yy = pos[i]
                c = ycolors.get(l["year"], "#0f766e")
                anchor = "start" if x >= cx else "end"
                tx = x + (12 if x >= cx else -12)
                node_svg += f'<circle cx="{x:.0f}" cy="{yy:.0f}" r="9" fill="{c}"/>'
                node_svg += f'<text x="{tx:.0f}" y="{yy+4:.0f}" text-anchor="{anchor}" font-size="12" fill="var(--ink)">{_esc(l["entry_no"])}</text>'
            graph_svg = (f'<svg viewBox="0 0 860 600" class="graph">{link_svg}{node_svg}</svg>'
                         '<p class="muted">节点=作品（颜色按年份），连线=画像相似度≥40；红≥60 / 橙≥45 / 灰≥40。仅作复核入口，不裁定抄袭。</p>')
        else:
            graph_svg = '<p class="muted">作品不足，无法生成关系图。</p>'

        # ---- 3) 跨年份技术演进 ----
        evo_max = max((e["count"] for e in evolution), default=1)
        evo_rows = "".join(
            f'<div class="evo"><span class="yr">{_esc(e["year"])}</span>'
            f'<div class="ebar"><span style="width:{e["count"]/evo_max*100:.0f}%"></span></div>'
            f'<span class="en">{e["count"]} 个</span>'
            f'<span class="etag">Rust {e["rust_ratio"]}% · C/C++ {e["c_ratio"]}% · 获奖 {e["awards"]}</span></div>'
            for e in evolution)

        # ---- 4) 学校/队伍聚合 ----
        smax = max((s["count"] for s in schools), default=1)
        school_rows = "".join(
            f'<div class="evo"><span class="yr sc">{_esc(s["school"])}</span>'
            f'<div class="ebar"><span style="width:{s["count"]/smax*100:.0f}%"></span></div>'
            f'<span class="en">{s["count"]} 个{("·获奖"+str(s["awards"])) if s["awards"] else ""}</span></div>'
            for s in schools[:15])

        data_script = "<script>window.__INSIGHT_WORKS__=" + json.dumps(works, ensure_ascii=False) + ";</script>"
        body = f"""
{data_script}
<main>
<style>
  .ins-sec{{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:18px 20px;margin:16px 0;box-shadow:0 1px 3px var(--shadow);}}
  .ins-sec h2{{margin:0 0 4px;font-size:19px;}}
  .ins-sec .hint{{color:var(--muted);font-size:13px;margin:0 0 14px;}}
  .muted{{color:var(--muted);font-size:13px;}}
  .ins-grid{{display:grid;grid-template-columns:1fr 1fr;gap:16px;}}
  @media(max-width:900px){{.ins-grid{{grid-template-columns:1fr;}}}}
  table.heat{{border-collapse:collapse;font-size:12px;}}
  table.heat td,table.heat th{{border:1px solid var(--line);padding:5px 7px;text-align:center;min-width:34px;}}
  table.heat th.rh{{text-align:left;white-space:nowrap;}}
  table.heat th.rh small{{display:block;color:var(--muted);font-weight:400;font-size:11px;max-width:160px;overflow:hidden;text-overflow:ellipsis;}}
  table.heat th.vh{{height:88px;}}
  table.heat th.vh span{{writing-mode:vertical-rl;transform:rotate(180deg);white-space:nowrap;font-weight:600;}}
  .heatwrap{{overflow:auto;}}
  svg.graph{{width:100%;max-width:860px;height:auto;display:block;margin:0 auto;}}
  .evo{{display:flex;align-items:center;gap:10px;margin:7px 0;font-size:13px;}}
  .evo .yr{{width:64px;font-weight:700;color:var(--brand-dark);}}
  .evo .yr.sc{{width:150px;font-weight:600;color:var(--ink);overflow:hidden;text-overflow:ellipsis;white-space:nowrap;}}
  .evo .ebar{{flex:1;height:14px;background:var(--line);border-radius:999px;overflow:hidden;}}
  .evo .ebar>span{{display:block;height:100%;background:linear-gradient(90deg,#22c55e,#0f766e);}}
  .evo .en{{width:120px;color:var(--muted);}}
  .evo .etag{{color:var(--muted);font-size:12px;}}
  table.review{{width:100%;border-collapse:collapse;font-size:13.5px;margin-top:8px;}}
  table.review th,table.review td{{border:1px solid var(--line);padding:7px 9px;text-align:left;}}
  table.review th{{background:var(--panel);}}
  .rev-btn{{border:1px solid var(--brand);background:var(--brand);color:#fff;border-radius:8px;padding:8px 16px;font-weight:600;cursor:pointer;}}
</style>

<div class="ins-sec">
  <h2>🔥 重复检测热力矩阵</h2>
  <p class="hint">本批 {n} 个作品两两画像相似度（0-100，越红越相似）。这是“查重”的总览入口；具体证据请在作品卡片的比较报告中逐行复核，系统不直接裁定抄袭。</p>
  <div class="heatwrap">{matrix_html}</div>
</div>

<div class="ins-grid">
  <div class="ins-sec">
    <h2>🕸️ 相似度关系图</h2>
    <p class="hint">作品相似度网络，自动浮现“抱团”线索。</p>
    {graph_svg}
  </div>
  <div class="ins-sec">
    <h2>📈 跨年份技术演进</h2>
    <p class="hint">基于 {site_data.get('baseline',{}).get('count',0)} 个历史基线 + 本批作品，观察规模与语言路线演进。</p>
    {evo_rows or '<p class="muted">暂无数据。</p>'}
    <h2 style="margin-top:18px">🏫 学校 / 队伍聚合</h2>
    <p class="hint">参赛活跃度 Top 15。</p>
    {school_rows or '<p class="muted">暂无数据。</p>'}
  </div>
</div>

<div class="ins-sec">
  <h2>🧮 评审汇总 · 人机评分对照</h2>
  <p class="hint">对照系统成熟度（机制+证据）与评委本地打分，并可一键导出整体评审汇总 CSV。评委打分存于本浏览器。</p>
  <button class="rev-btn" onclick="exportReview()">⬇ 导出评审汇总 CSV</button>
  <div id="review-table"></div>
</div>
</main>
<div id="toast"></div>
<script>
function rk(r){{return r==='high'?'高':r==='medium'?'中':r==='low'?'低':'无';}}
function loadJudge(repo){{try{{return JSON.parse(localStorage.getItem('ks-score-'+repo)||'null');}}catch(e){{return null;}}}}
function buildReview(){{
  var w=window.__INSIGHT_WORKS__||[];
  var h='<table class="review"><thead><tr><th>参赛编号</th><th>作品</th><th>年份</th><th>系统成熟度</th><th>重合风险</th><th>评委打分</th><th>差值(评委-成熟度)</th></tr></thead><tbody>';
  w.forEach(function(x){{
    var j=loadJudge(x.repo_id); var js=j?j.total:null;
    var diff=(js!=null)?(js-x.maturity):null;
    h+='<tr><td>'+x.entry_no+'</td><td>'+x.name+'</td><td>'+x.year+'</td>'
      +'<td>'+x.maturity+' ('+x.grade+')</td><td>'+rk(x.risk)+' '+x.overlap+'</td>'
      +'<td>'+(js!=null?js:'<span style=\"color:var(--muted)\">未评</span>')+'</td>'
      +'<td>'+(diff!=null?(diff>0?'+':'')+diff:'-')+'</td></tr>';
  }});
  h+='</tbody></table>';
  document.getElementById('review-table').innerHTML=h;
}}
function exportReview(){{
  var w=window.__INSIGHT_WORKS__||[];
  var rows=[['参赛编号','作品','年份','学校','系统成熟度','等级','重合风险','最高重合度','评委打分','差值']];
  w.forEach(function(x){{var j=loadJudge(x.repo_id);var js=j?j.total:'';
    rows.push([x.entry_no,x.name,x.year,x.school,x.maturity,x.grade,rk(x.risk),x.overlap,js,(js!==''?js-x.maturity:'')]);}});
  var csv='﻿'+rows.map(function(r){{return r.map(function(c){{return '"'+String(c).replace(/"/g,'""')+'"';}}).join(',');}}).join('\\n');
  var a=document.createElement('a');a.href=URL.createObjectURL(new Blob([csv],{{type:'text/csv;charset=utf-8'}}));a.download='kernelsage_review_summary.csv';a.click();
  var t=document.getElementById('toast');if(t){{t.textContent='已导出评审汇总';t.classList.add('show');setTimeout(function(){{t.classList.remove('show');}},1600);}}
}}
document.addEventListener('DOMContentLoaded',buildReview);
</script>
"""
        return self._shell(site_data, body, active="insights")

    def _shell(self, site_data: dict[str, Any], body: str, *, active: str) -> str:
        works_cls = "active" if active == "works" else ""
        base_cls = "active" if active == "baseline" else ""
        insights_cls = "active" if active == "insights" else ""
        nav = (
            f'<a href="index.html" class="{works_cls}">📋 作品展示</a>'
            f'<a href="insights.html" class="{insights_cls}">📊 分析洞察</a>'
            f'<a href="baseline.html" class="{base_cls}">📚 基线库</a>'
            f'<a class="iconbtn" id="themeBtn" onclick="toggleTheme()" title="深色/浅色模式">🌙</a>'
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
    <div class="sub">{_esc(site_data.get('contest_name','操作系统大赛'))} · 内核实现赛道作品智能分析与比较 · 由一定要以人类的身份赢啊--火山灰技术支持</div>
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
