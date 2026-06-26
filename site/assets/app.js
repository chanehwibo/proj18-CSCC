
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
