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

.card{background:var(--card);border:1px solid var(--line);border-radius:14px;overflow:hidden;display:flex;flex-direction:column;
  box-shadow:0 1px 3px var(--shadow);transition:transform .15s ease,box-shadow .15s ease,border-color .15s;position:relative;}
.card:hover{transform:translateY(-3px);box-shadow:0 12px 28px var(--shadow);border-color:var(--brand-soft);}
.card.picked{border-color:var(--brand);box-shadow:0 0 0 2px var(--brand-soft);}
.card .hd{background:linear-gradient(120deg,#0f766e0d,#0f766e1a);padding:16px 18px 12px;border-bottom:1px solid var(--line);}
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

#toTop{position:fixed;right:22px;bottom:22px;z-index:55;width:46px;height:46px;border-radius:50%;border:0;background:var(--brand);color:#fff;
  font-size:20px;cursor:pointer;box-shadow:0 6px 18px rgba(0,0,0,.25);display:none;}
#toTop.show{display:block;}
#toast{position:fixed;left:50%;bottom:80px;transform:translateX(-50%);background:#111827;color:#fff;padding:10px 18px;border-radius:10px;font-size:14px;z-index:200;opacity:0;transition:opacity .25s;pointer-events:none;}
#toast.show{opacity:1;}
.footer{color:var(--muted);font-size:12px;text-align:center;padding:24px;}
@media(max-width:640px){.grid{grid-template-columns:1fr;}.topbar .row{flex-wrap:wrap;}.toolbar input[type=text]{min-width:140px;}}
"""

APP_JS = r"""
var WORKS = window.__WORKS__ || {};
var CRITERIA = window.__CRITERIA__ || [];

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
  var panel=activePanel(); if(!panel)return;
  var q=(document.getElementById('q')||{}).value||''; q=q.trim().toLowerCase();
  var level=segVal('level'), risk=segVal('risk');
  var school=(document.getElementById('schoolSel')||{}).value||'all';
  var sortKey=(document.getElementById('sortSel')||{}).value||'maturity-desc';
  var grid=panel.querySelector('.grid'); if(!grid)return;
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
  function row(label, fn, cls){
    return '<tr><td class="rowhead">'+label+'</td>'+works.map(function(w){var v=fn(w);return '<td class="'+(cls?cls(w):'')+'">'+v+'</td>';}).join('')+'</tr>';
  }
  var body='';
  body+=row('成熟度', function(w){return w.maturity_score+'/100 ('+w.grade+'级)';});
  body+=row('最高重合度', function(w){return w.top_overlap+' ('+riskLabel(w.risk_level)+')';});
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
function openReport2(src,title){document.getElementById('modal-frame').style.display='';var c=document.getElementById('modal-cmp');if(c)c.style.display='none';openReport(src,title);}

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
        works = self._works_json(years)
        criteria = site_data.get("criteria") or self._default_criteria()
        data_script = (
            "<script>window.__WORKS__=" + json.dumps(works, ensure_ascii=False)
            + ";window.__CRITERIA__=" + json.dumps(criteria, ensure_ascii=False) + ";</script>"
        )
        body = f"""
{data_script}
<main>
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
  {panels}
</main>
{self._modal()}
{self._compare_bar()}
<button id="toTop" onclick="toTop()" title="返回顶部">↑</button>
<div id="toast"></div>
"""
        return self._shell(site_data, body, active="works")

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
      <div class="meter"><span>成熟度</span><div class="bar mat"><span style="width:{score}%"></span></div><span class="val">{score}</span></div>
      <div class="meter"><span>重合度</span><div class="bar risk"><span style="width:{risk_pct}%"></span></div><span class="val">{overlap}</span></div>
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
                    "dimensions": p.get("dimensions", []),
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
    def _shell(self, site_data: dict[str, Any], body: str, *, active: str) -> str:
        works_cls = "active" if active == "works" else ""
        base_cls = "active" if active == "baseline" else ""
        nav = (
            f'<a href="index.html" class="{works_cls}">📋 作品展示</a>'
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
