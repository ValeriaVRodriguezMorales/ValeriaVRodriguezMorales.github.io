const toggle=document.querySelector('.nav-toggle');
const nav=document.querySelector('.main-nav');
toggle?.addEventListener('click',()=>{const expanded=toggle.getAttribute('aria-expanded')==='true';toggle.setAttribute('aria-expanded',String(!expanded));nav?.classList.toggle('is-open',!expanded)});
document.querySelectorAll('.main-nav a').forEach(a=>a.addEventListener('click',()=>{nav?.classList.remove('is-open');toggle?.setAttribute('aria-expanded','false')}));
const search=document.querySelector('#publication-search');
const kind=document.querySelector('#publication-kind');
function filterPubs(){
 const q=(search?.value||'').trim().toLocaleLowerCase();const type=kind?.value||'';let visible=0;
 document.querySelectorAll('[data-record]').forEach(el=>{const show=(!type||el.dataset.kind===type)&&(!q||(el.dataset.search||'').includes(q));el.hidden=!show;if(show)visible++});
 document.querySelectorAll('[data-group]').forEach(el=>{el.hidden=!el.querySelector('[data-record]:not([hidden])')});
 const noResults=document.querySelector('#pub-no-results');if(noResults)noResults.hidden=visible>0;
}
search?.addEventListener('input',filterPubs);
kind?.addEventListener('change',filterPubs);
