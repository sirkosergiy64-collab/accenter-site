"""Генерує SEO-сторінки категорій (/catalog/<slug>/), sitemap.xml, robots.txt.
Запуск з кореня репозиторію: python3 scripts/seo.py"""
import json, os, html, collections, datetime

SITE = 'https://accenter.agency'
D = json.load(open('catalog/data.json', encoding='utf-8'))
import glob as _g
for _f in sorted(_g.glob('catalog/pending*.json')):
    D += json.load(open(_f, encoding='utf-8'))
CATS = list(dict.fromkeys(d['c'] for d in D))
TODAY = datetime.date.today().isoformat()

PAGES = [  # категорія, slug, H1, ключова фраза для title, де стоїть
    ('Консолі', 'konsoli', 'Дизайнерські консолі', 'Дизайнерські консолі купити', 'у вітальню, передпокій чи за диван'),
    ('Журнальні столи', 'zhurnalni-stoly', 'Дизайнерські журнальні столи', 'Журнальні столи з мармуру та керамограніту', 'у вітальню'),
    ('Буфети', 'bufety', 'Дизайнерські буфети', 'Дизайнерські буфети у вітальню', 'у вітальню та їдальню'),
    ('Обідні столи', 'obidni-stoly', 'Дизайнерські обідні столи', 'Обідні столи з керамограніту та мармуру', 'для кухні та їдальні'),
    ('Приставні столики', 'prystavni-stolyky', 'Приставні столики', 'Дизайнерські приставні столики', 'біля дивана чи ліжка'),
    ('Комоди', 'komody', 'Дизайнерські комоди', 'Дизайнерські комоди купити', 'у спальню чи вітальню'),
    ('Туалетні столики', 'tualetni-stolyky', 'Туалетні столики', 'Дизайнерські туалетні столики', 'для спальні та гардеробної'),
    ('Шафи й вітрини', 'shafy-vitryny', 'Шафи й вітрини', 'Дизайнерські шафи та вітрини', 'для вітальні та їдальні'),
    ('ТВ-тумби', 'tv-tumby', 'Дизайнерські ТВ-тумби', 'Дизайнерські ТВ-тумби', 'у вітальню'),
]
esc = lambda s: html.escape(str(s), quote=True)
fmt = lambda n: f'{n:,}'.replace(',', ' ')
def price(a, b): return 'за запитом' if a is None else f'${fmt(a)}' if a == b else f'від ${fmt(a)}'
def pl(n,a,b,c):
    m,h=n%10,n%100
    return f'{n} '+(a if m==1 and h!=11 else b if 2<=m<=4 and not 12<=h<=14 else c)
def low(items): return min(r[1] for d in items for r in d['p'] if r[1] is not None)
def top(items, key, n):
    return [k for k, _ in collections.Counter(x for d in items for x in d[key]).most_common(n)]

STYLE = open('scripts/seo_style.css', encoding='utf-8').read()
GTAG = open('scripts/gtag.html', encoding='utf-8').read()

def page(cat, slug, h1, kw, where):
    items = [d for d in D if d['c'] == cat]
    i = CATS.index(cat)
    mats = [m if m.isupper() or '/' in m else m.lower() for m in top(items, 'mt', 3)]
    stys = [s.lower() for s in top(items, 's', 3)]
    lo = low(items)
    title = f'{kw} — ціни від ${fmt(lo)} | Accenter'
    desc = (f'{h1} {where}: ціни від ${fmt(lo)}. Матеріали: {", ".join(mats)}. '
            f'Стилі: {", ".join(stys)}. Виготовлення під замовлення, доставка в Україну та Європу.')
    lead = (f'{h1} {where} — ціни від ${fmt(lo)}. Найчастіші матеріали: {", ".join(mats)}; '
            f'стилі: {", ".join(stys)}. Виготовляємо під замовлення: змінимо розмір, колір чи оздоблення. '
            f'Доставка з фабрик Китаю в Україну та Європу.')
    cards = []
    for d in items:
        rows = ''.join(f'<li><span>{esc(r[0])}</span><b>{price(r[1], r[2])}</b></li>' for r in d['p'][:4]) if d['p'][0][1] is not None else ''.join(f'<li><span>{esc(r[0])}</span></li>' for r in d['p'][:4]) + '<li><span>Ціна</span><b>за запитом</b></li>'
        cards.append(
            f'<article class="c"><img src="/catalog/img/{esc(d["a"])}.jpg" alt="{esc(d["n"])}" loading="lazy" width="400" height="400">'
            f'<div><span class="art">{esc(d["a"])}</span><h2><a href="/catalog/m/{esc(d["a"])}/" style="text-decoration:none">{esc(d["n"])}</a></h2>{"<p class=ds>"+esc(d.get("d",""))+"</p>" if d.get("d") else ""}<ul>{rows}</ul>'
            f'{"<p>Матеріали: " + esc(", ".join(d["m"])) + "</p>" if d["m"] else ""}'
            f'<a class="q" href="/catalog/m/{esc(d["a"])}/">Деталі та запит</a></div></article>')
    ld = {
        '@context': 'https://schema.org', '@type': 'ItemList', 'name': h1,
        'itemListElement': [{'@type': 'ListItem', 'position': n + 1, 'item': {
            '@type': 'Product', 'name': d['n'], 'description': d.get('d', ''), 'sku': d['a'], 'image': f'{SITE}/catalog/img/{d["a"]}.jpg',
            'brand': {'@type': 'Brand', 'name': 'Accenter'},
            **({'offers': {'@type': 'Offer', 'priceCurrency': 'USD', 'price': min(r[1] for r in d['p']),
                       'availability': 'https://schema.org/PreOrder', 'url': f'{SITE}/catalog/m/{d["a"]}/'}} if d['p'][0][1] is not None else {})}}
            for n, d in enumerate(items)]}
    crumbs = {'@context': 'https://schema.org', '@type': 'BreadcrumbList', 'itemListElement': [
        {'@type': 'ListItem', 'position': 1, 'name': 'Accenter', 'item': SITE + '/'},
        {'@type': 'ListItem', 'position': 2, 'name': 'Каталог', 'item': SITE + '/catalog/'},
        {'@type': 'ListItem', 'position': 3, 'name': h1, 'item': f'{SITE}/catalog/{slug}/'}]}
    others = ''.join(f'<a href="/catalog/{s}/">{esc(h)}</a>' for c, s, h, *_ in PAGES if s != slug)
    out = f'''<!DOCTYPE html>
<html lang="uk">
<head>
{GTAG}<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{SITE}/catalog/{slug}/">
<meta property="og:type" content="website">
<meta property="og:title" content="{esc(h1)} — Accenter">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:image" content="{SITE}/catalog/img/{esc(items[0]["a"])}.jpg">
<meta property="og:url" content="{SITE}/catalog/{slug}/">
<link rel="icon" href="/assets/logo.jpg">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Lora:wght@400;500&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<script type="application/ld+json">{json.dumps(crumbs, ensure_ascii=False)}</script>
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
<style>{STYLE}</style>
</head>
<body>
<nav><div class="wrap"><a class="brand" href="/"><img src="/assets/logo.jpg" alt="">ACCENTER</a><a class="btn" href="/catalog/#cat-{i}">Фільтри й обране</a></div></nav>
<header><div class="wrap">
 <p class="crumbs"><a href="/">Головна</a> / <a href="/catalog/">Каталог</a> / {esc(h1)}</p>
 <h1>{esc(h1)}</h1>
 <p class="lead">{esc(lead)}</p>
 <p class="note">Ціни в доларах США під ключ — з доставкою до Львова. Оплата в доларах, гривнях, криптовалюті або на рахунок ФОП чи ТОВ — курс фіксуємо перед оплатою.</p>
</div></header>
<main class="wrap"><div class="grid">
{chr(10).join(cards)}
</div></main>
<section class="wrap more"><h2>Інші категорії</h2><div class="links">{others}</div></section>
<footer><div class="wrap"><span>Accenter · дизайнерські та авторські меблі · 073 505 85 04</span>
<span><a href="https://wa.me/380735058504">WhatsApp</a> · <a href="https://t.me/+380735058504">Telegram</a> · <a href="https://t.me/accentr_home">канал</a></span></div></footer>
</body>
</html>
'''
    os.makedirs(f'catalog/{slug}', exist_ok=True)
    open(f'catalog/{slug}/index.html', 'w', encoding='utf-8').write(out)
    return slug

slugs = [page(*p) for p in PAGES]
urls = [('/', '1.0'), ('/catalog/', '0.9'), ('/designers/', '0.8')] + [(f'/catalog/{s}/', '0.8') for s in slugs]
open('sitemap.xml', 'w').write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
    ''.join(f'  <url><loc>{SITE}{u}</loc><lastmod>{TODAY}</lastmod><priority>{p}</priority></url>\n' for u, p in urls) + '</urlset>\n')
open('robots.txt', 'w').write(f'User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n')
print('pages:', slugs)
