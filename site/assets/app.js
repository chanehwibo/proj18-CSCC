
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
  body+=row(metricLabel('最高重合度','表示待测作品与历史基线中最接近样本的功能、结构、语言和代码线索重合程度，只提示复核优先级，不直接判定抄袭。'), function(w){return w.top_overlap+' ('+riskLabel(w.risk_level)+')';});
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
function renderDashboard(){var ws=activeWorks(),loc=0,langs={},ok=0,total=0;ws.forEach(function(w){loc+=w.loc||0;Object.keys(w.languages||{}).forEach(function(k){langs[k]=(langs[k]||0)+(w.languages[k]||0);});(w.dimensions||[]).forEach(function(d){total++;if(d.status==='confirmed')ok++;});});var top='-',v=-1;Object.keys(langs).forEach(function(k){if(langs[k]>v){top=k;v=langs[k];}});function set(id,val){var e=document.getElementById(id);if(e)e.textContent=val;}set('ov-current',ws.length);set('ov-loc',loc.toLocaleString());set('ov-lang',top);set('ov-cover',total?Math.round(ok*100/total)+'%':'-');var r=document.getElementById('abilityRadar');if(r)r.innerHTML=radarSvg(ws);var l=document.getElementById('abilityLegend'),ds=(ws[0]&&ws[0].dimensions)||[];if(l)l.innerHTML=ds.map(function(d,i){return '<div><b>'+esc(d.title||d.key)+'</b>：'+dimScore(ws,i)+'% 作品有可追溯实现证据</div>';}).join('')||'<div>暂无维度数据</div>';populateBaseWork();applyHistoryFilters();}
function baselineScore(w,tr){if(!w)return 0;var sc=0;if((tr.dataset.lang||'')&&topLanguage(w)===tr.dataset.lang)sc+=38;var loc=parseInt(tr.dataset.loc||'0'),wl=w.loc||0;if(loc>0&&wl>0)sc+=Math.max(0,32-Math.abs(Math.log((wl+1)/(loc+1)))*18);if((tr.dataset.tier||'').indexOf('获奖')>=0)sc+=12;if((tr.dataset.text||'').indexOf((w.arch||[])[0]||'')>=0)sc+=10;return Math.max(0,Math.min(100,Math.round(sc)));}
function applyHistoryFilters(){var tbody=document.getElementById('historyRows');if(!tbody)return;var rows=Array.prototype.slice.call(tbody.querySelectorAll('tr'));if(!rows.length)return;var q=((document.getElementById('histQ')||{}).value||'').trim().toLowerCase(),year=(document.getElementById('histYear')||{}).value||'all',award=(document.getElementById('histAward')||{}).value||'all',lang=(document.getElementById('histLang')||{}).value||'all',dim=(document.getElementById('histDim')||{}).value||'all',sim=(document.getElementById('histSim')||{}).value||'all',bw=(document.getElementById('histBaseWork')||{}).value||'',w=WORKS[bw]||activeWorks()[0]||WORKS[Object.keys(WORKS)[0]],shown=0;rows.forEach(function(tr){var score=baselineScore(w,tr);tr._sim=score;var se=tr.querySelector('.simscore');if(se)se.textContent=score;var ok=(!q||(tr.dataset.text||'').indexOf(q)>=0)&&(year==='all'||tr.dataset.year===year)&&(award==='all'||(tr.dataset.award||'').indexOf(award)>=0)&&(lang==='all'||tr.dataset.lang===lang)&&(dim==='all'||(tr.dataset.dims||'').indexOf(dim)>=0)&&(sim==='all'||(sim==='high'&&score>=70)||(sim==='medium'&&score>=40&&score<70)||(sim==='low'&&score<40));tr.style.display=ok?'':'none';if(ok)shown++;});rows.sort(function(a,b){return (b._sim||0)-(a._sim||0);});rows.forEach(function(tr){tbody.appendChild(tr);});var c=document.getElementById('histCount');if(c)c.textContent='显示 '+shown+' / 共 '+rows.length+' 个历史样本';}
function populateBaseWork(){var sel=document.getElementById('histBaseWork');if(!sel)return;var ws=activeWorks(),cur=sel.value;sel.innerHTML=ws.map(function(w){return '<option value="'+esc(w.repo_id)+'">'+esc(w.entry_no||w.repo_id)+'</option>';}).join('')||'<option value="">（本年度无作品）</option>';if(cur&&ws.some(function(w){return w.repo_id===cur;}))sel.value=cur;}
function openHistoryCompare(repo,idx){var w=WORKS[repo]||{},cmp=(w.compares||[]).filter(function(c){return String(c.index)===String(idx);})[0]||{},target=cmp.target_name||'历史样本',b=BASELINE.filter(function(x){return x.repo_id===cmp.target_repo_id;})[0]||{},dims=(w.dimensions||[]).map(function(d){return '<span class="dim '+(d.status==='confirmed'?'ok':'no')+'">'+esc(d.title||d.key)+'</span>';}).join('');var html='<div class="split-compare"><div class="side"><h3>待测作品</h3>'+workSummary(w,1,cmp)+'<div class="dims" style="padding:8px 0 0">'+dims+'</div></div><div class="side"><h3>历史作品</h3>'+workSummary(b,0,cmp)+'<div class="hint">重合维度 '+(cmp.overlap_dimensions||0)+' / 7，代码级线索 '+(cmp.code_similarity_count||0)+' 条。完整源码路径、行号与片段请点击比较报告核验。</div><button class="btn solid" onclick="openReport2(&quot;reports/'+esc(repo)+'.compare'+esc(idx)+'.html&quot;,&quot;'+esc(w.name||repo)+' vs '+esc(target)+'&quot;)">查看完整证据报告</button></div></div>';showHtmlModal('待测作品 vs 历史作品',html);}
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

function setupFloatTips(){
  var tip=document.getElementById('ks-floattip');
  if(!tip){tip=document.createElement('div');tip.id='ks-floattip';tip.className='ks-floattip';document.body.appendChild(tip);}
  function show(el){var txt=el.getAttribute('data-tip');if(!txt)return;tip.textContent=txt;tip.classList.add('show');
    var r=el.getBoundingClientRect(),pad=8,tw=tip.offsetWidth,th=tip.offsetHeight;
    var left=Math.max(pad,Math.min(r.left+r.width/2-tw/2,window.innerWidth-tw-pad));
    var top=r.top-th-8;if(top<pad)top=r.bottom+8;
    tip.style.left=left+'px';tip.style.top=top+'px';}
  function hide(){tip.classList.remove('show');}
  document.addEventListener('mouseover',function(e){var el=e.target.closest&&e.target.closest('.info-tip[data-tip]');if(el)show(el);});
  document.addEventListener('mouseout',function(e){var el=e.target.closest&&e.target.closest('.info-tip[data-tip]');if(el)hide();});
  document.addEventListener('focusin',function(e){var el=e.target.closest&&e.target.closest('.info-tip[data-tip]');if(el)show(el);});
  document.addEventListener('focusout',hide);
  window.addEventListener('scroll',hide,true);
}
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
  setupFloatTips();
});
