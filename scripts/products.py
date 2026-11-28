"""Окрема сторінка для кожної моделі: /catalog/m/<АРТИКУЛ>/ (SEO + посилання для клієнта).
Запуск після seo.py: python3 scripts/products.py"""
import json, os, re, html, shutil
from urllib.parse import quote

SITE = 'https://accenter.agency'
D = json.load(open('catalog/data.json', encoding='utf-8'))
import glob as _g
for _f in sorted(_g.glob('catalog/pending*.json')):
    D += json.load(open(_f, encoding='utf-8'))
NOP = lambda d: d['p'][0][1] is None
MINP = lambda d: 10**9 if NOP(d) else min(r[1] for r in d['p'])
STYLE = open('scripts/seo_style.css', encoding='utf-8').read()
GTAG = open('scripts/gtag.html', encoding='utf-8').read()
SLUG = {'Консолі': 'konsoli', 'Журнальні столи': 'zhurnalni-stoly', 'Буфети': 'bufety', 'Обідні столи': 'obidni-stoly',
        'Приставні столики': 'prystavni-stolyky', 'Комоди': 'komody', 'Туалетні столики': 'tualetni-stolyky',
        'Шафи й вітрини': 'shafy-vitryny', 'ТВ-тумби': 'tv-tumby'}
# Та сама модель розрахунку, що й у калькуляторі каталогу
SHIP_LO, SHIP_HI, PAD = 300, 450, 10
DEF = {'Консолі': [120, 35, 80], 'Журнальні столи': [100, 60, 45], 'Буфети': [160, 45, 85], 'Комоди': [100, 45, 100],
       'ТВ-тумби': [180, 40, 50], 'Обідні столи': [160, 90, 76], 'Приставні столики': [50, 50, 55],
       'Туалетні столики': [100, 45, 140], 'Шафи й вітрини': [100, 45, 200], 'Інше': [100, 50, 80]}
esc = lambda s: html.escape(str(s), quote=True)
fmt = lambda n: f'{round(n):,}'.replace(',', ' ')

def dims(label, cat):
    df = DEF.get(cat, [100, 50, 80])
    n = [float(x.replace(',', '.')) for x in re.findall(r'\d+(?:[.,]\d+)?', label)]
    n = [x for x in n if 15 <= x <= 400]
    if 'Ø' in label and n: return [n[0], n[0], n[1] if len(n) > 1 else df[2]]
    if len(n) >= 3: return n[:3]
    if len(n) == 2: return [n[0], n[1], df[2]]
    if len(n) == 1: return [n[0], min(df[1], n[0]), df[2]]
    return df

def ship(lab, cat):
    x = dims(lab, cat)
    v = (x[0] + PAD) * (x[1] + PAD) * (x[2] + PAD) / 1e6
    return v, v * (SHIP_LO + SHIP_HI) / 2

def price(a, b): return 'за запитом' if a is None else f'${fmt(a)}' if a == b else f'від ${fmt(a)}'

CSS = STYLE + '''
.pp{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:32px;align-items:start;padding:28px 0 8px}
@media(max-width:820px){.pp{grid-template-columns:minmax(0,1fr);gap:18px}}
.ph img{width:100%;aspect-ratio:1;object-fit:cover;border-radius:16px;display:block;background:var(--line)}
.gal{position:relative}.gs{display:flex;overflow-x:auto;scroll-snap-type:x mandatory;gap:8px;border-radius:16px;scrollbar-width:none}.gs::-webkit-scrollbar{display:none}
.gs img{flex:0 0 100%;width:100%;height:auto;aspect-ratio:1;object-fit:cover;scroll-snap-align:center;border-radius:16px}
.gn{position:absolute;right:12px;bottom:12px;background:rgba(20,18,15,.7);color:#fff;font:600 12px Inter,sans-serif;padding:4px 9px;border-radius:99px}
.gt{display:flex;gap:6px;overflow-x:auto;margin-top:8px;scrollbar-width:none}.gt img{flex:0 0 62px;width:62px;height:62px;aspect-ratio:1;border-radius:8px;cursor:pointer;opacity:.65;border:2px solid transparent}.gt img.on{opacity:1;border-color:#C9A063}
.gb{position:absolute;top:50%;transform:translateY(-50%);width:38px;height:38px;border-radius:50%;border:0;background:rgba(255,255,255,.85);font-size:20px;cursor:pointer}.gb.l{left:10px}.gb.r{right:10px}@media(max-width:820px){.gb{display:none}}
.pi .art{font-size:13px}.pi h1{font:400 clamp(30px,4vw,44px)/1.1 Lora,serif;margin:4px 0 6px;color:var(--ink)}
.pi .ds{color:#6f685e;margin:0 0 16px}
table.t{width:100%;border-collapse:collapse;font-size:15px;margin:0 0 6px}
.t th{text-align:left;font-size:12px;color:#8a8278;font-weight:600;padding:0 0 6px}
.t td{padding:10px 0;border-top:1px solid var(--line);vertical-align:top}.t td+td,.t th+th{text-align:right;white-space:nowrap;padding-left:12px}
.t small{display:block;color:#8a8278;font-size:12px}
.tot{font-weight:700}
.sn{font-size:12.5px;color:#8a8278;margin:6px 0 18px}
.real{margin:34px 0 0}.real h2{font:400 26px Lora,serif;margin:0 0 6px}.real p{color:#6b6357;margin:0 0 14px;font-size:14px}.rg{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:10px}.rg img{width:100%;height:260px;object-fit:cover;border-radius:12px;display:block}
.kv{margin:0 0 14px}.kv b{display:block;font-size:12px;color:#94723e;text-transform:uppercase;letter-spacing:.06em;margin-bottom:4px}
.kv ul{margin:0;padding-left:18px;color:#4a453e;font-size:14.5px}
.cta{display:flex;flex-wrap:wrap;gap:10px;margin:18px 0 6px}
.cta a{display:inline-flex;align-items:center;justify-content:center;min-height:46px;padding:0 20px;border-radius:99px;font-weight:600;font-size:15px;text-decoration:none}
.cta .p{background:var(--gold);color:#1d1a16}.cta .o{border:1px solid var(--gold);color:#94723e}
.trust{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:8px;margin:14px 0 0;padding:0;list-style:none;font-size:13.5px;color:#4a453e}
.trust li{background:#fff;border:1px solid var(--line);border-radius:12px;padding:10px 12px}
'''

DECOR = None
# Декор рекомендуємо тільки там, де він пасує за стилем, кольором і матеріалами меблів
DEC_TAGS = {'wood': ('дерев',), 'gold': ('золот', 'латун', 'бронз'), 'white': ('біл',), 'stone': ('камінь',)}
FUR_TAGS = {'wood': ('горіх', 'дерев', 'коричнев', 'натурал', 'тик', 'дуб'),
            'white': ('біл', 'кремов', 'бежев', 'світл', 'молочн'),
            'black': ('чорн', 'графіт'),
            'gold': ('золот', 'латун', 'бронз'),
            'stone': ('травертин', 'мармур', 'камін', 'керамограніт')}
# які «тони» декору пасують до тону меблів
AFF = {'wood': {'wood': 3, 'gold': 2}, 'white': {'white': 3, 'gold': 1, 'stone': 1},
       'black': {'gold': 3, 'wood': 1}, 'gold': {'gold': 3, 'white': 1}, 'stone': {'stone': 3, 'white': 2, 'wood': 1}}
# стилі меблів, до яких пасує наш декор (зараз увесь декор — ретро/вінтаж), і які тони декору там доречні
STY_OK = {'Ретро і вінтаж': None, 'Французький стиль': None,
          'Ваби-сабі': {'wood', 'white', 'stone'}, 'Кремовий стиль': {'white', 'stone', 'wood'},
          'Новий китайський': {'wood', 'stone'}}

def _tags(text, table):
    t = text.lower()
    return {k for k, ws in table.items() if any(w in t for w in ws)}

def _ftext(x):
    return ' '.join([x.get('n', ''), x.get('d', '')] + x.get('mt', []) + x.get('m', []) + x.get('o', []))

def decor_pick(d, decor):
    hit = [st for st in d.get('s', []) if st in STY_OK]
    if not hit: return []
    allowed = None if any(STY_OK[st] is None for st in hit) else set().union(*(STY_OK[st] for st in hit))
    ftone = _tags(_ftext(d), FUR_TAGS)
    dstyle = set(d.get('s', []))
    scored = []
    for x in decor:
        dt = _tags(x.get('d', '') + ' ' + ' '.join(x.get('mt', [])), DEC_TAGS)
        if allowed is not None and not (dt & allowed): continue
        sc = sum(AFF.get(f, {}).get(t, 0) for f in ftone for t in dt)
        sc += 2 * len(dstyle & set(x.get('s', [])))
        if set(m.lower() for m in d.get('m', [])) & set(m.lower() for m in x.get('m', [])): sc += 1
        if ftone and sc < 3: continue
        scored.append((-sc, NOP(x), hash(d['a'] + x['a']) % 97, x))
    scored.sort(key=lambda t: t[:3])
    return [t[3] for t in scored[:4]]

def decor_block(d):
    global DECOR
    if d['c'] == 'Декор': return ''
    if DECOR is None:
        DECOR = [x for x in json.load(open('catalog/data.json', encoding='utf-8')) if x['c'] == 'Декор']
    if not DECOR: return ''
    pool = decor_pick(d, DECOR)
    if len(pool) < 2: return ''
    cards = ''.join(f'<article class="c"><a href="/catalog/m/{esc(r["a"])}/"><img src="/catalog/img/{esc(r["a"])}.jpg" alt="{esc(r["n"])}" loading="lazy" width="400" height="400"></a>'
                    f'<div><h2><a href="/catalog/m/{esc(r["a"])}/" style="text-decoration:none">{esc(r["n"])}</a></h2>'
                    f'<p class="ds">{esc(r.get("d", ""))}</p><p><b>{price(None if NOP(r) else MINP(r), None if NOP(r) else MINP(r))}</b></p></div></article>' for r in pool)
    return f'<section class="more"><h2>Декор у тон до цієї моделі</h2><p style="color:#6b6357;margin:-4px 0 14px">Підібрали за стилем, кольором і матеріалами. Декор їде в тому ж контейнері, що й меблі. <a href="/catalog/dekor/">Увесь декор →</a></p><div class="grid">{cards}</div></section>'

GJS = '''<script>(()=>{const s=document.querySelector('.gs');if(!s)return;const t=[...document.querySelectorAll('.gt img')],n=document.querySelector('.gn'),N=s.children.length;
const go=i=>s.scrollTo({left:s.clientWidth*i+8*i,behavior:'smooth'});const cur=()=>Math.round(s.scrollLeft/(s.clientWidth+8));
s.addEventListener('scroll',()=>{const i=cur();n.textContent=(i+1)+' / '+N;t.forEach((x,j)=>x.classList.toggle('on',j===i))},{passive:true});
t.forEach((x,j)=>x.onclick=()=>go(j));document.querySelector('.gb.l').onclick=()=>go(Math.max(0,cur()-1));document.querySelector('.gb.r').onclick=()=>go(Math.min(N-1,cur()+1));})()</script>'''

def gallery(d):
    a, n, k = d['a'], d['n'], d.get('g')
    if not k:
        return f'<img src="/catalog/img/{a}.jpg" alt="{esc(n)}" width="400" height="400">'
    srcs = [f'/catalog/img/g/{a}/{i}.jpg' for i in range(1, k + 1)]
    big = ''.join(f'<img src="{s}" alt="{esc(n)} — фото {i}" width="800" height="800"{"" if i == 1 else " loading=\"lazy\""}>' for i, s in enumerate(srcs, 1))
    th = ''.join(f'<img src="{s}" alt="" loading="lazy"{" class=\"on\"" if i == 1 else ""}>' for i, s in enumerate(srcs, 1))
    return f'<div class="gal"><div class="gs">{big}</div><span class="gn">1 / {k}</span><button class="gb l" aria-label="Попереднє фото">‹</button><button class="gb r" aria-label="Наступне фото">›</button></div><div class="gt">{th}</div>{GJS}'

FABC = None
def fab_block(d):
    global FABC
    if FABC is None:
        FABC = {}
        for x in json.load(open('catalog/data.json', encoding='utf-8')): FABC[x['a'][3:5]] = FABC.get(x['a'][3:5], 0) + 1
    n = FABC.get(d['a'][3:5], 0)
    if n < 2: return ''
    return f'<p style="margin:22px 0 0"><a href="/catalog/?f={d["a"][3:5]}" style="display:inline-block;padding:12px 18px;border-radius:14px;background:#efe4cf;color:#7a5c25;font:600 15px Inter,sans-serif;text-decoration:none">Усі моделі цієї фабрики ({n}) →</a></p>'

def real_block(d):
    k = d.get('rp')
    if not k: return ''
    imgs = ''.join(f'<a href="/assets/real/{d["a"]}/{i}.jpg" target="_blank"><img src="/assets/real/{d["a"]}/{i}.jpg" alt="Реальне фото {esc(d["n"])} від покупця" loading="lazy"></a>' for i in range(1, k + 1))
    return f'<section class="real" id="real"><h2>Реальні фото</h2><p>Фото цієї моделі, які зробили покупці у себе вдома. Не рендер і не студійна зйомка.</p><div class="rg">{imgs}</div></section>'

def page(d, rel):
    a, n, cat = d['a'], d['n'], d['c']
    nop = NOP(d)
    lo = None if nop else min(r[1] for r in d['p'])
    rows = []
    for lab, p1, p2 in ([] if nop else d['p']):
        rows.append(f'<tr><td>{esc(lab)}</td><td class="tot">{price(p1, p2)}</td></tr>')
    rows = ''.join(rows)
    if nop:
        rows = ''.join(f'<tr><td>{esc(lab)}</td><td colspan="3" style="text-align:right">за запитом</td></tr>' for lab, _, _ in d['p'])
    wa = 'https://wa.me/380735058504?text=' + quote(f'Добрий день! Цікавить модель {a} — {n}. {SITE}/catalog/m/{a}/')
    slug = SLUG.get(cat)
    crumbs = (f'<a href="/">Головна</a> / <a href="/catalog/">Каталог</a> / '
              + (f'<a href="/catalog/{slug}/">{esc(cat)}</a> / ' if slug else f'{esc(cat)} / ') + esc(a))
    kv = ''
    if d.get('o'): kv += '<div class="kv"><b>Варіанти</b><ul>' + ''.join(f'<li>{esc(o)}</li>' for o in d['o'][:12]) + '</ul></div>'
    if d.get('m'): kv += f'<div class="kv"><b>Матеріали</b>{esc(", ".join(d["m"]))}</div>'
    if d.get('s'): kv += f'<div class="kv"><b>Стиль</b>{esc(", ".join(d["s"]))}</div>'
    relh = ''.join(f'<article class="c"><a href="/catalog/m/{esc(r["a"])}/"><img src="/catalog/img/{esc(r["a"])}.jpg" alt="{esc(r["n"])}" loading="lazy" width="400" height="400"></a>'
                   f'<div><span class="art">{esc(r["a"])}</span><h2><a href="/catalog/m/{esc(r["a"])}/" style="text-decoration:none">{esc(r["n"])}</a></h2>'
                   f'<p class="ds">{esc(r.get("d", ""))}</p><p><b>{price(None if NOP(r) else MINP(r), None if NOP(r) else MINP(r))}</b></p></div></article>' for r in rel)
    desc = f'{n} ({a}) — {d.get("x") or d.get("d", "")}'[:240].rstrip('.') + f'. {'Ціна за запитом.' if nop else f'Ціна від ${fmt(lo)} з доставкою до Львова.'} Виготовлення під замовлення, доставка в Україну та Європу.'
    ld = {'@context': 'https://schema.org', '@type': 'Product', 'name': n, 'sku': a, 'description': desc,
          'image': f'{SITE}/catalog/img/{a}.jpg', 'brand': {'@type': 'Brand', 'name': 'Accenter'}, 'category': cat,
          **({} if nop else {'offers': {'@type': 'AggregateOffer', 'priceCurrency': 'USD', 'lowPrice': lo, 'highPrice': max(r[2] for r in d['p']),
                     'offerCount': len(d['p']), 'availability': 'https://schema.org/PreOrder', 'url': f'{SITE}/catalog/m/{a}/'}})}
    return f'''<!DOCTYPE html>
<html lang="uk">
<head>
{GTAG}<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(n)} {esc(a)} — {'ціна за запитом' if nop else f'ціна від ${fmt(lo)}'} | Accenter</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{SITE}/catalog/m/{a}/">
<meta property="og:title" content="{esc(n)} — Accenter"><meta property="og:image" content="{SITE}/catalog/img/{a}.jpg"><meta property="og:url" content="{SITE}/catalog/m/{a}/">
<link rel="icon" href="/assets/logo.jpg">
<link rel="preconnect" href="https://fonts.googleapis.com"><link href="https://fonts.googleapis.com/css2?family=Lora:wght@400;500&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>{CSS}</style>
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
</head>
<body>
<nav><div class="wrap"><a class="brand" href="/"><img src="/assets/logo.jpg" alt="">ACCENTER</a><a class="btn" href="/catalog/">Каталог</a></div></nav>
<main class="wrap">
 <p class="crumbs" style="margin-top:16px">{crumbs}</p>
 <div class="pp">
  <div class="ph">{gallery(d)}</div>
  <div class="pi">
   <span class="art">{esc(a)}</span>
   <h1>{esc(n)}</h1>
   {f'<p class="ds">{esc(d["d"])}</p>' if d.get('d') else ''}
   {f'<p style="margin:0 0 16px;line-height:1.6;color:#4a453e">{esc(d["x"])}</p>' if d.get('x') else ''}
   <table class="t"><thead><tr><th>Розмір</th>{'<th colspan="3" style="text-align:right">Ціна</th>' if nop else '<th>Ціна з доставкою в Україну</th>'}</tr></thead><tbody>{rows}</tbody></table>
   {'<p class="sn">Вартість і термін виготовлення назве менеджер — напишіть нам, розрахуємо з доставкою.</p>' if nop else '<p class="sn">Ціни в доларах США під ключ — з доставкою до Львова. Доставку по Україні сплачуєте за тарифом перевізника (Нова пошта або інший). Курс фіксуємо перед оплатою.</p>'}
   {kv}
   <div class="cta"><a class="p" href="{wa}" target="_blank" rel="noopener">Запитати про модель</a><a class="o" href="https://t.me/+380735058504" target="_blank" rel="noopener">Telegram</a><a class="o" href="/catalog/?m={a}">У каталозі · ₴ / €</a></div>
   <ul class="trust"><li>Виготовлення під замовлення: розмір, колір, оздоблення</li><li>Фото й відео саме вашого товару зі складу в Гуанчжоу перед відправкою</li><li>Передоплата 50%, решта — на етапі доставки</li><li>Оплата в $, ₴, криптовалюті, на рахунок ФОП / ТОВ або готівкою в офісі у Львові</li></ul>
  </div>
 </div>
 {fab_block(d)}
 {real_block(d)}
 {decor_block(d)}
 {f'<section class="more"><h2>Схожі моделі</h2><div class="grid">{relh}</div></section>' if rel else ''}
</main>
<footer><div class="wrap"><span>Accenter · дизайнерські та авторські меблі · 073 505 85 04</span>
<span><a href="https://wa.me/380735058504">WhatsApp</a> · <a href="https://t.me/+380735058504">Telegram</a> · <a href="https://t.me/accentr_home">канал</a></span></div></footer>
</body>
</html>
'''

if os.path.isdir('catalog/m'):
    shutil.rmtree('catalog/m')
for d in D:
    same = [x for x in D if x['c'] == d['c'] and x['a'] != d['a']]
    common = sorted(same, key=lambda x: (-len(set(x.get('s', [])) & set(d.get('s', []))), abs(MINP(x) - MINP(d))))[:4]
    os.makedirs(f'catalog/m/{d["a"]}', exist_ok=True)
    open(f'catalog/m/{d["a"]}/index.html', 'w', encoding='utf-8').write(page(d, common))

# sitemap: доповнюємо сторінками моделей
sm = open('sitemap.xml', encoding='utf-8').read()
sm = re.sub(r'\s*<url><loc>[^<]*/catalog/m/[^<]*</loc>.*?</url>', '', sm)
today = re.search(r'<lastmod>([^<]+)</lastmod>', sm).group(1)
add = ''.join(f'  <url><loc>{SITE}/catalog/m/{d["a"]}/</loc><lastmod>{today}</lastmod><priority>0.6</priority></url>\n' for d in D)
sm = sm.replace('</urlset>', add + '</urlset>')
open('sitemap.xml', 'w', encoding='utf-8').write(sm)
print('pages', len(D))
