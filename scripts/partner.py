"""Партнерський каталог для дизайн-агенцій: без цін, контактів і логотипа.
Неіндексована сторінка за прихованою адресою. Запуск: python3 scripts/partner.py"""
import json, os, html

SLUG = 'p/6b6aaeb3'
ORDER = ['Консолі', 'Журнальні столи', 'Буфети', 'Обідні столи', 'Приставні столики', 'Комоди',
         'Туалетні столики', 'Шафи й вітрини', 'ТВ-тумби', 'Інше']

data = json.load(open('catalog/data.json'))
items = [{'a': d['a'], 'n': d['n'], 'd': d.get('d', ''), 'c': d['c'],
          'z': [r[0] for r in d['p'] if any(ch.isdigit() for ch in r[0])], 'v': [r[0] for r in d['p'] if not any(ch.isdigit() for ch in r[0]) and r[0] not in ('Ціна','')], 'o': d.get('o', [])[:8], 'm': d.get('m', []), 's': d.get('s', [])}
         for d in data]
cats = [c for c in ORDER if any(i['c'] == c for i in items)] + \
       sorted({i['c'] for i in items} - set(ORDER))
styles = sorted({s for i in items for s in i['s']})

page = r'''<!doctype html>
<html lang="uk"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex,nofollow,noarchive">
<title>Колекція меблів — каталог для дизайнерів</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Lora:wght@400;500&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<style>
:root{--bg:#f7f5f1;--card:#fff;--ink:#1b1a18;--mute:#6f685e;--line:#e8e2d8;--acc:#94723e}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:15px/1.5 Inter,system-ui,sans-serif}
header{padding:28px 18px 10px;max-width:1240px;margin:0 auto}
h1{font:400 clamp(28px,4.4vw,44px)/1.1 Lora,serif;margin:0 0 6px}
.sub{color:var(--mute);margin:0;max-width:62ch}
.bar{position:sticky;top:0;z-index:5;background:rgba(247,245,241,.96);backdrop-filter:blur(8px);border-bottom:1px solid var(--line)}
.bi{max-width:1240px;margin:0 auto;padding:10px 18px;display:flex;flex-wrap:wrap;gap:8px;align-items:center}
.tabs{display:flex;gap:4px;overflow-x:auto;scrollbar-width:none;width:100%}
.tabs button,.chips button{flex:none;border:1px solid var(--line);background:#fff;color:var(--ink);font:500 13px Inter,sans-serif;padding:7px 12px;border-radius:99px;cursor:pointer;white-space:nowrap}
.tabs button.on,.chips button.on{background:var(--ink);color:#fff;border-color:var(--ink)}
.tabs b{font-weight:500;opacity:.55;margin-left:4px}
.q{flex:1;min-width:160px;font:15px Inter,sans-serif;padding:8px 14px;border-radius:99px;border:1px solid var(--line);background:#fff}
.chips{display:flex;gap:4px;overflow-x:auto;scrollbar-width:none;width:100%}
.chips button{font-size:12px;padding:5px 10px}
main{max-width:1240px;margin:0 auto;padding:16px 18px 120px}
.cnt{color:var(--mute);font-size:13px;margin:0 0 12px}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:16px}
.c{background:var(--card);border:1px solid var(--line);border-radius:14px;overflow:hidden;display:flex;flex-direction:column}
.c img{width:100%;aspect-ratio:1;object-fit:cover;display:block;background:#eee}
.cb{padding:12px 14px 14px;display:flex;flex-direction:column;gap:4px;flex:1}
.art{font:600 12px Inter,sans-serif;color:var(--acc);letter-spacing:.03em}
.nm{font:500 20px/1.2 Lora,serif}
.ds{color:var(--mute);font-size:13px}
.k{font-size:13px;margin-top:6px}.k span{color:var(--mute)}
.sel{margin-top:auto;align-self:flex-start;border:1px solid var(--ink);background:none;font:500 13px Inter,sans-serif;padding:7px 14px;border-radius:99px;cursor:pointer;margin-top:10px}
.sel.on{background:var(--ink);color:#fff}
.dock{position:fixed;left:50%;bottom:16px;transform:translateX(-50%);background:var(--ink);color:#fff;border-radius:99px;padding:8px 8px 8px 18px;display:flex;gap:10px;align-items:center;box-shadow:0 8px 30px rgba(0,0,0,.25);font-size:14px;z-index:9;max-width:calc(100% - 24px)}
.dock span{white-space:nowrap}@media(max-width:480px){.dock{font-size:13px;padding-left:14px;gap:6px}.dock button{padding:8px 10px;font-size:12px}}
.dock button{border:0;background:#fff;color:var(--ink);font:600 13px Inter,sans-serif;padding:8px 14px;border-radius:99px;cursor:pointer;white-space:nowrap}
.dock button.g{background:none;color:#fff;border:1px solid #555}
.empty{color:var(--mute);padding:40px 0;text-align:center}
.toast{position:fixed;left:50%;bottom:80px;transform:translateX(-50%);background:#fff;border:1px solid var(--line);padding:8px 14px;border-radius:10px;font-size:13px;box-shadow:0 4px 16px rgba(0,0,0,.1)}
</style></head><body>
<header><h1>Колекція корпусних меблів</h1>
<p class="sub">Консолі, столи, буфети, комоди, тумби. Більшість моделей виготовляються в інших розмірах і кольорах на замовлення. Вартість і терміни — за запитом. Додайте моделі до добірки й поділіться посиланням із клієнтом.</p></header>
<div class="bar"><div class="bi">
<div class="tabs" id="tabs"></div>
<input class="q" id="q" type="search" placeholder="Пошук: артикул, назва, стиль" aria-label="Пошук">
<div class="chips" id="chips"></div>
</div></div>
<main><p class="cnt" id="cnt"></p><div class="grid" id="g"></div></main>
<div class="dock" id="dock" hidden><span id="dn"></span><button class="g" id="only">Показати</button><button id="copy">Поділитися</button></div>
<script>
const D=__DATA__,CATS=__CATS__,STY=__STY__;
const $=id=>document.getElementById(id),esc=s=>String(s).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
let cat='',sty='',q='',only=false;
const url=new URL(location.href);
let sel=new Set((url.searchParams.get('sel')||'').split(',').filter(Boolean));
if(!sel.size){try{JSON.parse(localStorage.getItem('pSel')||'[]').forEach(a=>sel.add(a))}catch(e){}}
else only=true;
function save(){try{localStorage.setItem('pSel',JSON.stringify([...sel]))}catch(e){}}
function tabs(){const n=c=>D.filter(d=>!c||d.c===c).length;
 $('tabs').innerHTML=[['','Усі'],...CATS.map(c=>[c,c])].map(([v,l])=>`<button data-c="${esc(v)}" class="${v===cat?'on':''}">${esc(l)}</button>`).join('');
 $('chips').innerHTML=['',...STY].map(s=>`<button data-s="${esc(s)}" class="${s===sty?'on':''}">${s?esc(s):'Усі стилі'}</button>`).join('');}
function card(d){const on=sel.has(d.a);
 return `<article class="c"><img loading="lazy" src="/catalog/img/${d.a}.jpg" alt="${esc(d.n)}"><div class="cb">
 <div class="art">${d.a}</div><div class="nm">${esc(d.n)}</div>${d.d?`<div class="ds">${esc(d.d)}</div>`:''}
 ${d.z.length?`<div class="k"><span>Розміри:</span> ${d.z.map(esc).join(' · ')}</div>`:''}${d.v.length?`<div class="k"><span>Варіанти:</span> ${d.v.map(esc).join(' · ')}</div>`:''}
 ${d.m.length?`<div class="k"><span>Матеріали:</span> ${d.m.map(esc).join(', ')}</div>`:''}
 ${d.o.length?`<div class="k"><span>Кольори:</span> ${d.o.length} варіант${d.o.length>4?'ів':d.o.length>1?'и':''}</div>`:''}
 <button class="sel${on?' on':''}" data-a="${d.a}">${on?'✓ У добірці':'+ До добірки'}</button></div></article>`}
function draw(){const ql=q.toLowerCase();
 const L=D.filter(d=>(only?sel.has(d.a):(!cat||d.c===cat)&&(!sty||d.s.includes(sty)))&&(!ql||(d.a+' '+d.n+' '+d.d+' '+d.s.join(' ')).toLowerCase().includes(ql)));
 $('cnt').textContent=only?'Ваша добірка':'';
 $('g').innerHTML=L.map(card).join('')||'<p class="empty">Нічого не знайдено</p>';
 $('dock').hidden=!sel.size;$('dn').textContent=`У добірці: ${sel.size}`;$('only').textContent=only?'Усі':'Показати';}
$('tabs').onclick=e=>{const b=e.target.closest('button');if(!b)return;cat=b.dataset.c;only=false;tabs();draw();scrollTo(0,0)};
$('chips').onclick=e=>{const b=e.target.closest('button');if(!b)return;sty=b.dataset.s;only=false;tabs();draw()};
$('q').oninput=e=>{q=e.target.value.trim();draw()};
$('g').onclick=e=>{const b=e.target.closest('.sel');if(!b)return;const a=b.dataset.a;sel.has(a)?sel.delete(a):sel.add(a);save();
 b.classList.toggle('on',sel.has(a));b.textContent=sel.has(a)?'✓ У добірці':'+ До добірки';$('dock').hidden=!sel.size;$('dn').textContent=`У добірці: ${sel.size}`};
$('only').onclick=()=>{only=!only;draw();scrollTo(0,0)};
$('copy').onclick=async()=>{const u=location.origin+location.pathname+'?sel='+[...sel].join(',');
 if(navigator.share){try{await navigator.share({title:'Добірка меблів',url:u});return}catch(e){}}
 try{await navigator.clipboard.writeText(u);toast('Посилання на добірку скопійовано')}catch(e){prompt('Скопіюйте посилання:',u)}};
function toast(t){const d=document.createElement('div');d.className='toast';d.textContent=t;document.body.append(d);setTimeout(()=>d.remove(),2200)}
tabs();draw();
</script></body></html>
'''
page = (page.replace('__DATA__', json.dumps(items, ensure_ascii=False, separators=(',', ':')))
            .replace('__CATS__', json.dumps(cats, ensure_ascii=False))
            .replace('__STY__', json.dumps(styles, ensure_ascii=False))
            .replace('__N__', str(len(items))))
os.makedirs(SLUG, exist_ok=True)
open(f'{SLUG}/index.html', 'w').write(page)
print('ok', SLUG, len(items), 'models', len(page) // 1024, 'KB')
